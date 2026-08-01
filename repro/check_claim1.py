from fractions import Fraction


def fresh_binomial_tail(trials, required, probability):
    distribution = [Fraction(1)] + [Fraction() for _ in range(required - 1)]
    for _ in range(trials):
        updated = [Fraction() for _ in range(required)]
        for successes in range(required):
            updated[successes] += distribution[successes] * (1 - probability)
            if successes + 1 < required:
                updated[successes + 1] += distribution[successes] * probability
        distribution = updated
    return sum(distribution, Fraction())


def worst_adaptive_failure(trials, required, lower_probability):
    values = {successes: Fraction(successes < required) for successes in range(trials + 1)}
    choices = [lower_probability, (1 + lower_probability) / 2, Fraction(1)]
    for completed in range(trials - 1, -1, -1):
        next_values = {}
        for successes in range(completed + 1):
            next_values[successes] = max(
                (1 - probability) * values[successes] + probability * values[successes + 1]
                for probability in choices
            )
        values = next_values
    return values[0]


def independent_check(expected):
    calibration_checks = 0
    for item in expected["independent_resource_calibration"]:
        trials = item["binary_search_minimum_N"]
        required = item["required_transition_hits"]
        probability = Fraction(item["per_simulation_lower_bound"])
        limit = Fraction(item["per_transition_failure_limit"])
        at_n = fresh_binomial_tail(trials, required, probability)
        before = fresh_binomial_tail(trials - 1, required, probability)
        if not (at_n <= limit < before):
            return {"passed": False, "reason": "independent minimum-N check failed"}
        calibration_checks += 1

    adaptive_checks = 0
    for trials in range(1, 13):
        for required in range(1, min(4, trials) + 1):
            for probability in [Fraction(1, 4), Fraction(1, 2)]:
                worst = worst_adaptive_failure(trials, required, probability)
                iid_tail = fresh_binomial_tail(trials, required, probability)
                if worst != iid_tail:
                    return {"passed": False, "reason": "adaptive stochastic-domination check failed"}
                adaptive_checks += 1
    return {
        "passed": True,
        "method": "fresh Bernoulli convolution plus adversarial dynamic program over history-dependent hit probabilities",
        "minimum_N_calibrations_checked": calibration_checks,
        "adaptive_probability_processes_checked": adaptive_checks,
        "worst_case_is_lower_bound_probability": True,
    }
