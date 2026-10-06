"""TrueOdds 2.1 validation framework."""

from .pricing import (
    american_to_decimal,
    break_even_probability,
    expected_value,
    remove_two_way_vig,
)
from .calibration import (
    brier_score,
    log_loss,
    calibration_table,
    expected_calibration_error,
    HistogramCalibrator,
)
from .uncertainty import (
    conservative_probability,
    uncertainty_haircut,
)
from .parlay import (
    JointProbabilityResult,
    joint_probability_from_simulations,
    pairwise_phi_matrix,
    correlation_risk_score,
)
from .validation import (
    BacktestSummary,
    summarize_backtest,
    edge_bucket_report,
    classify_wager,
)
from .model import LogisticProbabilityModel
from .schema import BetRecord

__all__ = [
    "american_to_decimal",
    "break_even_probability",
    "expected_value",
    "remove_two_way_vig",
    "brier_score",
    "log_loss",
    "calibration_table",
    "expected_calibration_error",
    "HistogramCalibrator",
    "conservative_probability",
    "uncertainty_haircut",
    "JointProbabilityResult",
    "joint_probability_from_simulations",
    "pairwise_phi_matrix",
    "correlation_risk_score",
    "BacktestSummary",
    "summarize_backtest",
    "edge_bucket_report",
    "classify_wager",
    "LogisticProbabilityModel",
    "BetRecord",
]
