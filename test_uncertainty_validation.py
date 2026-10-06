from trueodds.uncertainty import conservative_probability, uncertainty_haircut
from trueodds.validation import classify_wager


def test_conservative_probability_haircut():
    assert conservative_probability(0.60, 3.0) == 0.57


def test_uncertainty_increases_for_parlays():
    single = uncertainty_haircut(2.0, leg_count=1)
    parlay = uncertainty_haircut(2.0, leg_count=4, correlation_risk=50)
    assert parlay > single


def test_promo_only_classification():
    # +120 requires ~45.45%; +180 requires ~35.71%.
    # 40% is not a base bet but is a strong promo edge.
    label = classify_wager(0.40, 120, boosted_american_odds=180, bet_threshold_pp=3.0)
    assert label == "PROMO-ONLY BET"
