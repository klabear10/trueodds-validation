def american_to_decimal(odds: float) -> float:
    if odds == 0:
        raise ValueError("American odds cannot be zero.")
    if odds > 0:
        return 1.0 + odds / 100.0
    return 1.0 + 100.0 / abs(odds)


def break_even_probability(american_odds: float) -> float:
    return 1.0 / american_to_decimal(american_odds)


def expected_value(probability: float, american_odds: float) -> float:
    if not 0.0 <= probability <= 1.0:
        raise ValueError("probability must be between 0 and 1")
    return probability * american_to_decimal(american_odds) - 1.0
