from dataclasses import dataclass


@dataclass(frozen=True)
class ParlayAssessment:
    raw_probability: float
    calibrated_probability: float
    conservative_probability: float
    break_even_probability: float
    raw_ev: float
    conservative_ev: float
    classification: str
    correlation_risk_score: float


def conservative_probability(
    calibrated_probability: float,
    model_uncertainty: float,
    lambda_: float = 1.0,
) -> float:
    if not 0.0 <= calibrated_probability <= 1.0:
        raise ValueError("calibrated_probability must be between 0 and 1")
    if model_uncertainty < 0:
        raise ValueError("model_uncertainty cannot be negative")
    if lambda_ < 0:
        raise ValueError("lambda_ cannot be negative")
    return max(0.0, calibrated_probability - lambda_ * model_uncertainty)


def classify_wager(
    conservative_edge_pp: float,
    boosted_conservative_edge_pp: float | None = None,
    strong_threshold_pp: float = 6.0,
    bet_threshold_pp: float = 3.0,
) -> str:
    if boosted_conservative_edge_pp is not None:
        if conservative_edge_pp < bet_threshold_pp <= boosted_conservative_edge_pp:
            return "PROMO-ONLY BET"
    if conservative_edge_pp >= strong_threshold_pp:
        return "STRONG BET"
    if conservative_edge_pp >= bet_threshold_pp:
        return "BET"
    if conservative_edge_pp > 0:
        return "LEAN"
    return "PASS"
