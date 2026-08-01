import hashlib
from fractions import Fraction
from itertools import combinations, product

from repro.exact import l1, policy_values, transition_complexity, transition_rows


N_STATES = 4
N_ACTIONS = 2
GRID_DENOMINATOR = 2


def theorem_bound(n_states, n_actions, complexity):
    denominator = (2 * complexity) ** (n_actions * n_states) * 2**n_states
    return Fraction(1, denominator**2)


def fraction_text(value):
    return f"{value.numerator}/{value.denominator}"


def verify_gap(gap, bound):
    return gap == 0 or gap >= bound


def run_exhaustive_check():
    rows = transition_rows(GRID_DENOMINATOR)
    digest = hashlib.sha256()
    mdps_total = 0
    mdps_halting = 0
    pairs_checked = 0
    zero_gaps = 0
    positive_gaps = 0
    min_positive = None
    min_ratio = None
    examples = []

    for mdp_rows in product(rows, repeat=4):
        mdps_total += 1
        values = policy_values(mdp_rows)
        if values is None:
            continue
        mdps_halting += 1
        complexity = transition_complexity(mdp_rows)
        bound = theorem_bound(N_STATES, N_ACTIONS, complexity)
        case_gaps = []
        for left, right in combinations(values, 2):
            gap = l1(left, right)
            pairs_checked += 1
            case_gaps.append(fraction_text(gap))
            if not verify_gap(gap, bound):
                raise AssertionError(f"forbidden positive gap: {gap} < {bound}")
            if gap == 0:
                zero_gaps += 1
                continue
            positive_gaps += 1
            ratio = gap / bound
            if min_positive is None or gap < min_positive:
                min_positive = gap
            if min_ratio is None or ratio < min_ratio:
                min_ratio = ratio
        canonical = repr(mdp_rows) + repr([tuple(map(fraction_text, value)) for value in values]) + repr(case_gaps)
        digest.update(canonical.encode())
        if len(examples) < 3:
            examples.append({
                "transition_complexity": complexity,
                "bound": fraction_text(bound),
                "gaps": case_gaps,
            })

    return {
        "domain": {
            "states": N_STATES,
            "actions": N_ACTIONS,
            "decision_states": 2,
            "absorbing_goal_states": 1,
            "absorbing_sink_states": 1,
            "probability_grid_denominator": GRID_DENOMINATOR,
            "complete_domain": True,
            "halting_filter": "all four memoryless deterministic policies have invertible I-Q",
        },
        "mdps_total": mdps_total,
        "mdps_halting": mdps_halting,
        "policy_pairs_checked": pairs_checked,
        "zero_value_vector_pairs": zero_gaps,
        "positive_value_vector_pairs": positive_gaps,
        "minimum_positive_l1_gap": fraction_text(min_positive),
        "minimum_gap_to_bound_ratio": fraction_text(min_ratio),
        "case_digest_sha256": digest.hexdigest(),
        "examples": examples,
        "theorem_disjunction_holds": True,
    }


def negative_control():
    bound = theorem_bound(N_STATES, N_ACTIONS, GRID_DENOMINATOR)
    injected_gap = bound / 2
    return {
        "control": "inject a strictly positive gap below the theorem bound",
        "bound": fraction_text(bound),
        "injected_gap": fraction_text(injected_gap),
        "verifier_accepted": verify_gap(injected_gap, bound),
        "control_rejected_as_intended": not verify_gap(injected_gap, bound),
    }
