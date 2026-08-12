import contextlib
import importlib
import math
import os
import statistics
import sys
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from multiprocessing import get_context
from pathlib import Path

from repro.qvbs import acquire_sources, write_compatibility_layer


BENCHMARKS = (
    ("consensus.2", 0.01, 0.5, 5, 100, 0.0005, 1000, 1.00, 2),
    ("csma.2-2", 0.01, 0.25, 5, 50, 0.001, 200, 0.50, 2),
    ("firewire_abst", 0.01, 0.5, 5, 100, 0.0005, 1000, 1.00, 2),
    ("ij.10", 0.01, 0.5, 5, 50, 0.0005, 1000, 1.00, 2),
    ("ij.3", 0.01, 0.5, 5, 100, 0.0001, 1000, 1.00, 1),
    ("pacman.v2", 0.01, 0.08, 5, 100, 0.001, 200, 0.55, 7),
    ("philosophers-mdp.3", 0.01, 0.5, 5, 100, 0.0005, 1000, 1.00, 2),
    ("rabin.3", 0.01, 0.03125, 5, 100, 0.0005, 1000, 1.00, 2),
    ("zeroconf", 0.01, 0.0001025262467191601, 5, 100, 0.0005, 100, 0.00, 1),
)
TRIALS = 10
WORKERS = 32
BASE_SEED = 2026080200


def _modules(source_dir):
    source = str(source_dir)
    if source not in sys.path:
        sys.path.insert(0, source)
    numpy = importlib.import_module("numpy")
    converter = importlib.import_module("convert_jani_to_mdp")
    simulator = importlib.import_module("mdp_simulator")
    learner = importlib.import_module("ltl_reachability_learner")
    return numpy, converter, simulator, learner


def _policy_row(gt_mdp, learned_mdp, state):
    policy_state = learned_mdp.state_MEC.get(state, state)
    if policy_state not in learned_mdp.states:
        return {}
    action = learned_mdp.learned_policy.get(policy_state)
    if action is None:
        return {}
    if state in learned_mdp.state_MEC:
        selected_state, selected_action = action
        if state == selected_state:
            actions = [selected_action]
        else:
            actions = sorted(
                (
                    candidate
                    for candidate in gt_mdp.topology.get(state, ())
                    if (state, candidate) in learned_mdp.MEC_state_action_pairs[policy_state]
                ),
                key=repr,
            )
    else:
        actions = [action]
    if not actions:
        return {}
    row = {}
    weight = 1.0 / len(actions)
    for selected in actions:
        for successor, probability in gt_mdp.transition_probabilities[(state, selected)].items():
            row[successor] = row.get(successor, 0.0) + weight * probability
    return row


def _fixed_policy_interval(gt_mdp, learned_mdp, tolerance=1e-9, max_iterations=200000):
    initial = gt_mdp.initial_state
    goals = set(gt_mdp.goal_states)
    rows = {}
    reachable = {initial}
    frontier = [initial]
    while frontier:
        state = frontier.pop()
        if state in goals:
            rows[state] = {state: 1.0}
            continue
        row = _policy_row(gt_mdp, learned_mdp, state)
        rows[state] = row
        for successor, probability in row.items():
            if probability > 0 and successor not in reachable:
                reachable.add(successor)
                frontier.append(successor)

    reverse = {state: set() for state in reachable}
    for state, row in rows.items():
        for successor, probability in row.items():
            if probability > 0 and successor in reverse:
                reverse[successor].add(state)
    can_reach_goal = set(goals & reachable)
    frontier = list(can_reach_goal)
    while frontier:
        state = frontier.pop()
        for predecessor in reverse[state]:
            if predecessor not in can_reach_goal:
                can_reach_goal.add(predecessor)
                frontier.append(predecessor)

    lower = {state: float(state in goals) for state in reachable}
    upper = {state: float(state in can_reach_goal) for state in reachable}
    active = sorted(can_reach_goal - goals, key=repr)
    for iteration in range(1, max_iterations + 1):
        for state in active:
            row = rows[state]
            lower[state] = sum(probability * lower.get(successor, 0.0) for successor, probability in row.items())
            upper[state] = sum(probability * upper.get(successor, 0.0) for successor, probability in row.items())
        gap = upper.get(initial, 0.0) - lower.get(initial, 0.0)
        if gap <= tolerance:
            return {
                "lower": lower.get(initial, 0.0),
                "upper": upper.get(initial, 0.0),
                "gap": gap,
                "iterations": iteration,
                "reachable_states": len(reachable),
                "converged": True,
            }
    return {
        "lower": lower.get(initial, 0.0),
        "upper": upper.get(initial, 0.0),
        "gap": upper.get(initial, 0.0) - lower.get(initial, 0.0),
        "iterations": max_iterations,
        "reachable_states": len(reachable),
        "converged": False,
    }


def _run_trial(task):
    source_dir, model_dir, scratch_dir, benchmark_index, config, trial = task
    name, confidence, p_min, minimum_k, maximum_k, threshold, accuracy_sims, expected, paper_stage = config
    seed = BASE_SEED + benchmark_index * 100 + trial
    started = time.monotonic()
    with open(os.devnull, "w", encoding="utf-8") as sink, contextlib.redirect_stdout(sink), contextlib.redirect_stderr(sink):
        numpy, converter, simulator_module, learner_module = _modules(source_dir)
        numpy.random.seed(seed)
        gt_mdp = converter.convert_jani_to_mdp(str(Path(model_dir) / f"{name}.jani"))
        learner = learner_module.LTLReachabilityLearner(
            mdp_simulator=simulator_module.MDPSimulator(mdp=gt_mdp),
            min_num_iterations=minimum_k,
            max_num_iterations=maximum_k,
            convergence_threshold=threshold,
            num_policy_accuracy_sims=accuracy_sims,
            true_confidence_error=confidence,
            true_p_min=p_min,
        )
        audited_values = []
        original_accuracy = learner.calculate_policy_accuracy

        def audited_accuracy(mdp, max_steps=100):
            certificate = _fixed_policy_interval(gt_mdp, mdp)
            empirical = original_accuracy(mdp, max_steps=max_steps)
            audited_values.append(certificate)
            return empirical

        learner.calculate_policy_accuracy = audited_accuracy
        learner.learn(analysis_dir=str(Path(scratch_dir) / name / str(trial)))

    histories = []
    for learning, accuracy, exact_value in zip(learner.learning_history, learner.policy_accuracy_history, audited_values):
        histories.append(
            {
                "stage": int(learning[0]),
                "samples": int(learning[1]),
                "delta_k": learning[2],
                "p_k": learning[3],
                "bound_width": learning[4],
                "lower_bound": learning[5],
                "upper_bound": learning[6],
                "empirical_policy_reachability": accuracy[-1],
                "independent_policy_value": exact_value,
            }
        )
    transitions = sum(len(row) for row in gt_mdp.transition_probabilities.values())
    return {
        "benchmark": name,
        "trial": trial,
        "seed": seed,
        "paper_expected_accuracy": expected,
        "paper_convergence_stage": paper_stage,
        "states": len(gt_mdp.states),
        "state_action_pairs": len(gt_mdp.state_action_pairs),
        "transitions": transitions,
        "iterations": len(histories),
        "runtime_seconds": time.monotonic() - started,
        "history": histories,
    }


def _median_curve(trials, key):
    stages = sorted({row["stage"] for trial in trials for row in trial["history"]})
    curve = []
    for stage in stages:
        values = [row[key] for trial in trials for row in trial["history"] if row["stage"] == stage]
        if values:
            curve.append({"stage": stage, "median": statistics.median(values), "trials": len(values)})
    return curve


def _first_confident_stage(trials, expected, simulations):
    curve = _median_curve(trials, "empirical_policy_reachability")
    standard_error = math.sqrt(max(expected * (1 - expected), 0.25 / simulations) / simulations)
    tolerance = max(1.0 / simulations, 1.96 * standard_error)
    for index, row in enumerate(curve):
        if all(abs(item["median"] - expected) <= tolerance for item in curve[index:]):
            return row["stage"], tolerance
    return None, tolerance


def _first_certified_stage(trials, expected):
    stages = sorted({row["stage"] for trial in trials for row in trial["history"]})
    medians = []
    for stage in stages:
        intervals = [
            row["independent_policy_value"]
            for trial in trials
            for row in trial["history"]
            if row["stage"] == stage
        ]
        if intervals:
            medians.append(
                {
                    "stage": stage,
                    "lower": statistics.median(item["lower"] for item in intervals),
                    "upper": statistics.median(item["upper"] for item in intervals),
                    "all_converged": all(item["converged"] for item in intervals),
                }
            )
    for index, row in enumerate(medians):
        if all(
            item["all_converged"]
            and item["lower"] - 1e-8 <= expected <= item["upper"] + 1e-8
            and item["upper"] - item["lower"] <= 1e-8
            for item in medians[index:]
        ):
            return row["stage"], medians
    return None, medians


def independent_check(result):
    complete = len(result["trials"]) == len(BENCHMARKS) * TRIALS
    dimensions_match = all(
        len([trial for trial in result["trials"] if trial["benchmark"] == config[0]]) == TRIALS
        for config in BENCHMARKS
    )
    paper_stages = [row["paper_convergence_stage"] for row in result["benchmark_results"]]
    reconstructed = []
    aggregation_matches = True
    for config in BENCHMARKS:
        name, _, _, _, _, _, simulations, expected, _ = config
        trials = [row for row in result["trials"] if row["benchmark"] == name]
        stage, _ = _first_confident_stage(trials, expected, simulations)
        reconstructed.append(stage)
        stored = next(row for row in result["benchmark_results"] if row["benchmark"] == name)
        aggregation_matches = aggregation_matches and stage == stored["observed_empirical_convergence_stage"]
    observed = result["observed_summary"]
    empirical_alignment = (
        observed["empirical_median_stage"] == 2
        and observed["empirical_mean_stage"] is not None
        and abs(observed["empirical_mean_stage"] - 2.3) <= 0.2
    )
    certified_alignment = (
        observed["certified_median_stage"] == 2
        and observed["certified_mean_stage"] is not None
        and abs(observed["certified_mean_stage"] - 2.3) <= 0.2
    )
    intervals_converged = all(
        stage["independent_policy_value"]["converged"]
        for trial in result["trials"]
        for stage in trial["history"]
    )
    return {
        "complete_9_by_10": complete and dimensions_match,
        "paper_stage_median_recomputed": statistics.median(paper_stages),
        "paper_stage_mean_recomputed": statistics.mean(paper_stages),
        "observed_stages_recomputed": reconstructed,
        "aggregation_matches": aggregation_matches,
        "empirical_alignment": empirical_alignment,
        "certified_alignment": certified_alignment,
        "all_policy_intervals_converged": intervals_converged,
        "passed": complete
        and dimensions_match
        and aggregation_matches
        and empirical_alignment
        and certified_alignment
        and intervals_converged,
    }


def negative_control(result):
    mutated = dict(result)
    mutated["trials"] = result["trials"][:-1]
    rejected = not independent_check(mutated)["passed"]
    return {
        "control": "delete one of the required 90 trials",
        "control_rejected_as_intended": rejected,
        "verifier_accepted": not rejected,
    }


def run_full_benchmarks(work_dir):
    source_dir, model_dir, manifest = acquire_sources(work_dir / "inputs")
    write_compatibility_layer(source_dir)
    tasks = [
        (source_dir, model_dir, work_dir / "trials", benchmark_index, config, trial)
        for benchmark_index, config in enumerate(BENCHMARKS)
        for trial in range(1, TRIALS + 1)
    ]
    results = []
    with ProcessPoolExecutor(max_workers=WORKERS, mp_context=get_context("spawn")) as pool:
        futures = {pool.submit(_run_trial, task): (task[4][0], task[5]) for task in tasks}
        for future in as_completed(futures):
            result = future.result()
            results.append(result)
            print(
                f"QVBS_TRIAL benchmark={result['benchmark']} trial={result['trial']} "
                f"iterations={result['iterations']} runtime_seconds={result['runtime_seconds']:.3f}",
                flush=True,
            )
    results.sort(key=lambda row: (row["benchmark"], row["trial"]))
    benchmark_results = []
    for config in BENCHMARKS:
        name, _, _, _, _, _, simulations, expected, paper_stage = config
        trials = [row for row in results if row["benchmark"] == name]
        empirical_stage, empirical_tolerance = _first_confident_stage(trials, expected, simulations)
        certified_stage, exact_curve = _first_certified_stage(trials, expected)
        benchmark_results.append(
            {
                "benchmark": name,
                "paper_expected_accuracy": expected,
                "paper_convergence_stage": paper_stage,
                "observed_empirical_convergence_stage": empirical_stage,
                "empirical_tolerance": empirical_tolerance,
                "observed_certified_value_stage": certified_stage,
                "empirical_curve": _median_curve(trials, "empirical_policy_reachability"),
                "median_lower_bound_curve": _median_curve(trials, "lower_bound"),
                "median_upper_bound_curve": _median_curve(trials, "upper_bound"),
                "independent_value_curve": exact_curve,
            }
        )
    observed = [row["observed_empirical_convergence_stage"] for row in benchmark_results]
    exact = [row["observed_certified_value_stage"] for row in benchmark_results]
    return {
        "protocol": {
            "benchmarks": len(BENCHMARKS),
            "trials_per_benchmark": TRIALS,
            "total_trials": len(results),
            "workers": WORKERS,
            "deterministic_seed_base": BASE_SEED,
            "paper_hardware": "single CPU core, 1 GB, 2.4 GHz, 36-hour limit per trial",
            "reproduction_hardware": "HF cpu-upgrade; parallel trials, each author learner remains single-threaded",
            "deviations": [
                "stdlib-compatible numpy/tqdm/plotting layer because the baseline frozen uv lock has no third-party packages",
                "unweighted action candidates are repr-sorted before seeded sampling",
                "deterministic trial seeds were added; the author dispatcher did not seed trials",
            ],
            "input_manifest": manifest,
        },
        "paper_summary": {"median_stage": 2, "mean_stage": 2.3},
        "observed_summary": {
            "empirical_median_stage": statistics.median(observed) if all(value is not None for value in observed) else None,
            "empirical_mean_stage": statistics.mean(observed) if all(value is not None for value in observed) else None,
            "certified_median_stage": statistics.median(exact) if all(value is not None for value in exact) else None,
            "certified_mean_stage": statistics.mean(exact) if all(value is not None for value in exact) else None,
        },
        "benchmark_results": benchmark_results,
        "trials": results,
    }
