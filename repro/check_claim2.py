from fractions import Fraction
from itertools import combinations_with_replacement

from repro.claim2 import near_optimal


def independent_check():
    spectra = 0
    strict_checks = 0
    equality_controls = 0
    for denominator in range(2, 13):
        grid = [Fraction(numerator, denominator) for numerator in range(denominator + 1)]
        for policy_count in range(2, 6):
            for values in combinations_with_replacement(grid, policy_count):
                distinct = sorted(set(values), reverse=True)
                if len(distinct) < 2:
                    continue
                spectra += 1
                optimum = distinct[0]
                gap = optimum - distinct[1]
                strict_indices = near_optimal(values, gap / 2)
                optimal_indices = [index for index, value in enumerate(values) if value == optimum]
                if strict_indices != optimal_indices:
                    return {"passed": False, "reason": "strict gap implication failed", "values": list(map(str, values))}
                strict_checks += 1
                equality_indices = near_optimal(values, gap)
                if equality_indices == optimal_indices:
                    return {"passed": False, "reason": "equality boundary did not expose runner-up", "values": list(map(str, values))}
                equality_controls += 1
    return {
        "passed": True,
        "method": "fresh exhaustive enumeration of all rational value multisets with 2-5 policies on denominator grids 2-12",
        "value_spectra_checked": spectra,
        "strict_implications_checked": strict_checks,
        "equality_boundary_controls_checked": equality_controls,
    }
