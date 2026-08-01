from fractions import Fraction
from math import comb


def fraction_text(value):
    return f"{value.numerator}/{value.denominator}"


def binomial_lower_tail(trials, required_successes, probability):
    return sum(
        (
            Fraction(comb(trials, successes))
            * probability**successes
            * (1 - probability) ** (trials - successes)
            for successes in range(min(required_successes, trials + 1))
        ),
        Fraction(),
    )


def calibrated_minimum_trials(required_successes, probability, failure_limit):
    if probability <= 0 or failure_limit <= 0:
        return None
    low = required_successes - 1
    high = max(required_successes, 1)
    while binomial_lower_tail(high, required_successes, probability) > failure_limit:
        low = high
        high *= 2
    while high - low > 1:
        middle = (low + high) // 2
        if binomial_lower_tail(middle, required_successes, probability) <= failure_limit:
            high = middle
        else:
            low = middle
    return high


def smallest_pac_stage(p_min):
    stage = 0
    while Fraction(1, 2**stage) > p_min:
        stage += 1
    return stage


def run_pac_existence_certificate():
    stage_witnesses = []
    for p_min in [Fraction(1, 2), Fraction(1, 3), Fraction(1, 10), Fraction(1, 1024)]:
        stage = smallest_pac_stage(p_min)
        p_k = Fraction(1, 2**stage)
        prior = Fraction(1, 2 ** (stage - 1)) if stage else Fraction(1)
        stage_witnesses.append(
            {
                "p_min": fraction_text(p_min),
                "smallest_K_PAC": stage,
                "p_K": fraction_text(p_k),
                "p_K_at_most_p_min": p_k <= p_min,
                "prior_stage_too_large": stage == 0 or prior > p_min,
            }
        )

    calibrations = []
    scenarios = [
        (2, Fraction(1, 2), Fraction(1, 100)),
        (3, Fraction(1, 4), Fraction(1, 100)),
        (4, Fraction(1, 8), Fraction(1, 100)),
        (5, Fraction(1, 16), Fraction(1, 1000)),
        (6, Fraction(1, 32), Fraction(1, 1000)),
        (8, Fraction(1, 64), Fraction(1, 1000)),
    ]
    for required, probability, failure_limit in scenarios:
        trials = calibrated_minimum_trials(required, probability, failure_limit)
        tail = binomial_lower_tail(trials, required, probability)
        prior_tail = binomial_lower_tail(trials - 1, required, probability)
        calibrations.append(
            {
                "required_transition_hits": required,
                "per_simulation_lower_bound": fraction_text(probability),
                "per_transition_failure_limit": fraction_text(failure_limit),
                "binary_search_minimum_N": trials,
                "tail_at_N": fraction_text(tail),
                "tail_at_N_minus_1": fraction_text(prior_tail),
                "N_passes": tail <= failure_limit,
                "N_minus_1_fails": prior_tail > failure_limit,
            }
        )

    passed = (
        all(item["p_K_at_most_p_min"] and item["prior_stage_too_large"] for item in stage_witnesses)
        and all(item["N_passes"] and item["N_minus_1_fails"] for item in calibrations)
    )
    return {
        "claim": "There exists K_PAC such that for every k >= K_PAC a finite N_k gives an epsilon_k-optimal policy with probability at least 1-delta_k.",
        "exact_quantifier_certificate": {
            "K_PAC": "p_min>0 and p_k=2^-k imply a finite first K with p_K<=p_min",
            "finite_transition_requirement": "the two-sided PAC-BVI result supplies a finite s_k for fixed p_k, epsilon_k, and delta_TP+delta_EC",
            "positive_episode_probability": "mu>0 and p_k>0 give q_k=(mu*p_k/|A|)^|S|>0 for every relevant transition",
            "adaptive_sampling_repair": "conditional hit probability at least q_k permits a shared-uniform coupling; actual hit counts stochastically dominate Binomial(N_k,q_k)",
            "finite_N_k": "for finite s_k and q_k>0, the exact Binomial lower tail tends to zero, so a finite N_k meets each allocated error",
            "simultaneous_transitions": "at most |SA|/p_k relevant transitions; a union bound gives total sampling error delta_Nk",
            "error_composition": "delta_TP+delta_EC+delta_Nk=delta_k",
        },
        "stage_witnesses": stage_witnesses,
        "independent_resource_calibration": calibrations,
        "paper_implementation_audit": {
            "author_code_commit": "6ffec1273326aede50c8b6516cea1ceb8d920faa",
            "author_comment": "calculate_N_k is a heuristic and does not provide the same guarantees as the N_k in the paper",
            "heuristic_used_as_verification_evidence": False,
        },
        "passed": passed,
    }


def negative_control(result):
    hardest = result["independent_resource_calibration"][-1]
    zero_exploration_has_finite_witness = calibrated_minimum_trials(1, Fraction(0), Fraction(1, 10)) is not None
    return {
        "controls": [
            {
                "control": "use one fewer simulation than the exact binary-search minimum",
                "N": hardest["binary_search_minimum_N"] - 1,
                "failure_tail": hardest["tail_at_N_minus_1"],
                "limit": hardest["per_transition_failure_limit"],
                "verifier_accepted": not hardest["N_minus_1_fails"],
            },
            {
                "control": "set exploration probability mu to zero, hence q=0",
                "finite_N_witness_found": zero_exploration_has_finite_witness,
                "verifier_accepted": zero_exploration_has_finite_witness,
            },
        ],
        "control_rejected_as_intended": hardest["N_minus_1_fails"] and not zero_exploration_has_finite_witness,
    }
