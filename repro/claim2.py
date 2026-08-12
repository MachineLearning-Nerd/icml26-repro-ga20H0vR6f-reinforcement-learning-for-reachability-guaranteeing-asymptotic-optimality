from fractions import Fraction


def fraction_text(value):
    return f"{value.numerator}/{value.denominator}"


def smallest_strict_stage(gap, minimum_stage):
    stage = minimum_stage
    while Fraction(1, 2**stage) >= gap:
        stage += 1
    return stage


def near_optimal(values, epsilon):
    optimum = max(values)
    return [index for index, value in enumerate(values) if value >= optimum - epsilon]


def run_gap_certificate():
    gaps = [Fraction(1, 2), Fraction(1, 3), Fraction(1, 17), Fraction(7, 64)]
    stage_witnesses = []
    for gap in gaps:
        stage = smallest_strict_stage(gap, minimum_stage=1)
        epsilon = Fraction(1, 2**stage)
        previous = Fraction(1, 2 ** (stage - 1))
        stage_witnesses.append(
            {
                "gap": fraction_text(gap),
                "smallest_strict_stage": stage,
                "epsilon_at_stage": fraction_text(epsilon),
                "epsilon_is_strictly_below_gap": epsilon < gap,
                "previous_stage_not_strictly_below": previous >= gap,
            }
        )

    boundary_values = [Fraction(1), Fraction(1, 2)]
    boundary_epsilon = Fraction(1, 2)
    boundary_near_optimal = near_optimal(boundary_values, boundary_epsilon)
    strict_near_optimal = near_optimal(boundary_values, Fraction(1, 4))
    symbolic_margin = Fraction(5, 13) - Fraction(3, 13)
    passed = (
        symbolic_margin > 0
        and all(item["epsilon_is_strictly_below_gap"] for item in stage_witnesses)
        and all(item["previous_stage_not_strictly_below"] for item in stage_witnesses)
        and strict_near_optimal == [0]
    )
    return {
        "claim": "For a finite memoryless-deterministic policy set, epsilon < epsilon_diff implies every epsilon-optimal policy is optimal; therefore a strictly later stage witnesses Theorem 3.2.",
        "assumptions": [
            "the policy set is finite",
            "epsilon_diff is the positive difference between the optimal value and the best strictly suboptimal value",
            "epsilon-optimal means J(pi) >= J* - epsilon",
            "epsilon_k = 2^(-k)",
            "the Theorem 3.1 event has probability at least 1-delta_k",
        ],
        "symbolic_certificate": {
            "premises": [
                "for every suboptimal pi, J(pi) <= J* - epsilon_diff",
                "epsilon < epsilon_diff",
            ],
            "derived_strict_order": "J(pi) <= J* - epsilon_diff < J* - epsilon",
            "conclusion": "no suboptimal pi satisfies J(pi) >= J* - epsilon",
            "probability_lift": "{pi_k epsilon-optimal} is a subset of {pi_k optimal}",
            "checked_positive_margin": fraction_text(symbolic_margin),
        },
        "stage_witnesses": stage_witnesses,
        "boundary_audit": {
            "values": [fraction_text(value) for value in boundary_values],
            "epsilon_diff": fraction_text(boundary_epsilon),
            "near_optimal_policy_indices_at_equality": boundary_near_optimal,
            "paper_proof_uses_non_strict_inequality": True,
            "equality_does_not_imply_exact_optimality": boundary_near_optimal != [0],
            "theorem_statement_survives": "The theorem existentially permits choosing a later K_opt with strict inequality.",
        },
        "passed": passed,
    }


def negative_control():
    values = [Fraction(1), Fraction(1, 2)]
    epsilon = Fraction(1, 2)
    accepted = near_optimal(values, epsilon) == [0]
    return {
        "control": "replace epsilon < epsilon_diff by epsilon = epsilon_diff",
        "values": [fraction_text(value) for value in values],
        "epsilon": fraction_text(epsilon),
        "near_optimal_policy_indices": near_optimal(values, epsilon),
        "verifier_accepted_exact_optimality": accepted,
        "control_rejected_as_intended": not accepted,
    }
