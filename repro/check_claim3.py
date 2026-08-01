from fractions import Fraction

from repro.claim3 import geometric_tail


def independent_check():
    checks = 0
    for first_stage in range(1, 101):
        recurrence_sum = Fraction(1, 2**first_stage)
        term = recurrence_sum
        for _ in range(1, 512):
            term /= 2
            recurrence_sum += term
        exact = geometric_tail(first_stage)
        if not recurrence_sum < exact:
            return {"passed": False, "reason": "finite geometric prefix was not below the claimed infinite tail"}
        if exact != 2 * Fraction(1, 2**first_stage):
            return {"passed": False, "reason": "closed-form tail mismatch"}
        checks += 1
    return {
        "passed": True,
        "method": "independent exact-Fraction recurrence and closed-form comparison",
        "tail_start_values_checked": checks,
        "independence_used": False,
    }
