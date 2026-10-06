"""Conservative probability adjustments."""

from __future__ import annotations
import math


def uncertainty_haircut(
    base_uncertainty_pp: float,
    *,
    correlation_risk: float = 0.0,
    model_disagreement_pp: float = 0.0,
    low_sample_penalty_pp: float = 0.0,
    late_news_penalty_pp: float = 0.0,
    leg_count: int = 1,
) -> float:
    """Return total uncertainty in probability points.

    The weights are deliberately transparent and provisional. Historical
    validation should replace them with empirically estimated values.
    """
    if not 0 <= correlation_risk <= 100:
        raise ValueError("correlation_risk must be between 0 and 100")
    if leg_count < 1:
        raise ValueError("leg_count must be >= 1")

    corr_penalty = 0.02 * correlation_risk  # 100 risk -> 2.0 pp
    parlay_penalty = max(0, leg_count - 1) * 0.5

    total = (
        base_uncertainty_pp
        + corr_penalty
        + max(0.0, model_disagreement_pp)
        + max(0.0, low_sample_penalty_pp)
        + max(0.0, late_news_penalty_pp)
        + parlay_penalty
    )
    return float(total)


def conservative_probability(
    calibrated_probability: float,
    uncertainty_pp: float,
    lambda_: float = 1.0,
) -> float:
    if not 0 <= calibrated_probability <= 1:
        raise ValueError("calibrated_probability must be between 0 and 1")
    if uncertainty_pp < 0:
        raise ValueError("uncertainty_pp cannot be negative")
    if lambda_ < 0:
        raise ValueError("lambda_ cannot be negative")
    return max(0.0, calibrated_probability - lambda_ * uncertainty_pp / 100.0)
