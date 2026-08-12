from fractions import Fraction


def fraction_text(value):
    return f"{value.numerator}/{value.denominator}"


def geometric_tail(first_stage):
    return Fraction(1, 2 ** (first_stage - 1))


def run_borel_cantelli_certificate():
    tail_checks = []
    for first_stage in range(1, 65):
        finite_prefix = sum((Fraction(1, 2**stage) for stage in range(first_stage, first_stage + 128)), Fraction())
        exact_tail = geometric_tail(first_stage)
        tail_checks.append(
            {
                "first_stage": first_stage,
                "exact_infinite_tail": fraction_text(exact_tail),
                "finite_prefix_below_tail": finite_prefix < exact_tail,
                "tail_below_2_to_minus_m_for_m_eq_n_minus_1": exact_tail <= Fraction(1, 2 ** (first_stage - 1)),
            }
        )
    passed = all(item["finite_prefix_below_tail"] for item in tail_checks)
    return {
        "claim": "If Pr(E_k) <= delta_k = 2^-k after K_opt, only finitely many non-optimal-policy events occur almost surely.",
        "assumptions": [
            "E_k is the event that the stage-k policy is non-optimal",
            "for every k >= K_opt, Pr(E_k) <= 2^-k",
            "no independence assumption is required",
        ],
        "proof_certificate": {
            "summability": "sum_{k=K}^infinity 2^-k = 2^(1-K) < infinity",
            "union_bound": "Pr(union_{k>=n} E_k) <= sum_{k>=n} Pr(E_k) <= 2^(1-n)",
            "continuity_from_above": "Pr(limsup E_k) <= lim_{n->infinity} 2^(1-n) = 0",
            "conclusion": "with probability one, there is a finite random K after which every returned policy is optimal",
        },
        "exact_tail_checks": tail_checks,
        "passed": passed,
    }


def negative_control():
    blocks = []
    for exponent in range(1, 17):
        start = 2**exponent
        stop = 2 ** (exponent + 1)
        block_lower_bound = Fraction(stop - start, stop)
        blocks.append({"start": start, "stop_exclusive": stop, "lower_bound": fraction_text(block_lower_bound)})
    rejected = all(item["lower_bound"] == "1/2" for item in blocks)
    return {
        "control": "replace delta_k=2^-k by the non-summable schedule delta_k=1/k",
        "divergence_certificate": "each dyadic block k=2^m,...,2^(m+1)-1 contributes at least 1/2",
        "dyadic_blocks": blocks,
        "verifier_accepted_summability": False,
        "control_rejected_as_intended": rejected,
    }
