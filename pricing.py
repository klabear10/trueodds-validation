"""Sportsbook price and expected-value utilities."""

from __future__ import annotations


def american_to_decimal(odds: float) -> float:
    if odds == 0:
        raise ValueError("American odds cannot be zero.")
    if odds > 0:
        return 1.0 + odds / 100.0
    return 1.0 + 100.0 / abs(odds)


def break_even_probability(american_odds: float) -> float:
    return 1.0 / american_to_decimal(american_odds)


def expected_value(probability: float, american_odds: float) -> float:
    """Expected return per unit staked. 0.08 means +8% EV."""
    if not 0.0 <= probability <= 1.0:
        raise ValueError("probability must be between 0 and 1")
    return probability * american_to_decimal(american_odds) - 1.0


def remove_two_way_vig(odds_a: float, odds_b: float) -> tuple[float, float]:
    """Normalize two implied probabilities so they sum to 1.

    This is a simple proportional-vig removal method.
    """
    pa = break_even_probability(odds_a)
    pb = break_even_probability(odds_b)
    total = pa + pb
    if total <= 0:
        raise ValueError("invalid two-way prices")
    return pa / total, pb / total
