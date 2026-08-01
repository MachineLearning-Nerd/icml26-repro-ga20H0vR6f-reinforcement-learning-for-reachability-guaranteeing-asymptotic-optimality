from fractions import Fraction
from itertools import combinations, product
from math import gcd


def compositions(total, parts):
    for cuts in combinations(range(total + parts - 1), parts - 1):
        points = (-1, *cuts, total + parts - 1)
        yield tuple(points[i + 1] - points[i] - 1 for i in range(parts))


def transition_rows(denominator):
    return [tuple(Fraction(n, denominator) for n in nums) for nums in compositions(denominator, 4)]


def solve_policy(rows, policy):
    row0 = rows[policy[0]]
    row1 = rows[2 + policy[1]]
    a = 1 - row0[0]
    b = -row0[1]
    c = -row1[0]
    d = 1 - row1[1]
    determinant = a * d - b * c
    if determinant == 0:
        return None
    value0 = (row0[2] * d - b * row1[2]) / determinant
    value1 = (a * row1[2] - c * row0[2]) / determinant
    return value0, value1, Fraction(1), Fraction(0)


def lcm(left, right):
    return left * right // gcd(left, right)


def transition_complexity(rows):
    complexities = []
    for row in rows:
        common = 1
        for probability in row:
            common = lcm(common, probability.denominator)
        complexities.append(common)
    return max(complexities)


def policy_values(rows):
    values = []
    for policy in product(range(2), repeat=2):
        value = solve_policy(rows, policy)
        if value is None:
            return None
        values.append(value)
    return values


def l1(left, right):
    return sum(abs(a - b) for a, b in zip(left, right))
