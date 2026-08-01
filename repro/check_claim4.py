from fractions import Fraction
from itertools import combinations, product

from repro.claim4 import GRID_DENOMINATOR, N_ACTIONS, N_STATES, fraction_text, theorem_bound
from repro.exact import transition_complexity, transition_rows


def cramer_values(rows, policy):
    first = rows[policy[0]]
    second = rows[2 + policy[1]]
    matrix = ((1 - first[0], -first[1]), (-second[0], 1 - second[1]))
    determinant = matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
    if determinant == 0:
        return None
    numerator0 = first[2] * matrix[1][1] - matrix[0][1] * second[2]
    numerator1 = matrix[0][0] * second[2] - first[2] * matrix[1][0]
    return numerator0 / determinant, numerator1 / determinant, Fraction(1), Fraction(0)


def independent_check(expected):
    rows = transition_rows(GRID_DENOMINATOR)
    halting = 0
    pairs = 0
    minimum = None
    for mdp_rows in product(rows, repeat=4):
        values = [cramer_values(mdp_rows, policy) for policy in product(range(2), repeat=2)]
        if any(value is None for value in values):
            continue
        halting += 1
        bound = theorem_bound(N_STATES, N_ACTIONS, transition_complexity(mdp_rows))
        for left, right in combinations(values, 2):
            gap = sum(abs(a - b) for a, b in zip(left, right))
            pairs += 1
            if gap != 0 and gap < bound:
                return {"passed": False, "reason": f"{gap} < {bound}"}
            if gap != 0 and (minimum is None or gap < minimum):
                minimum = gap
    passed = (
        halting == expected["mdps_halting"]
        and pairs == expected["policy_pairs_checked"]
        and fraction_text(minimum) == expected["minimum_positive_l1_gap"]
    )
    return {
        "passed": passed,
        "method": "independent two-by-two Cramer solver and fresh complete enumeration",
        "mdps_halting": halting,
        "policy_pairs_checked": pairs,
        "minimum_positive_l1_gap": fraction_text(minimum),
    }
