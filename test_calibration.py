import numpy as np

from trueodds.calibration import (
    brier_score,
    log_loss,
    expected_calibration_error,
    HistogramCalibrator,
)


def test_scores_are_finite():
    p = np.array([0.2, 0.7, 0.9, 0.4])
    y = np.array([0, 1, 1, 0])
    assert 0 <= brier_score(p, y) <= 1
    assert log_loss(p, y) > 0
    assert expected_calibration_error(p, y, bins=4) >= 0


def test_histogram_calibrator_output_range():
    p = np.linspace(0.05, 0.95, 20)
    y = (p > 0.5).astype(int)
    cal = HistogramCalibrator(bins=5).fit(p, y)
    out = cal.predict(np.array([0.1, 0.5, 0.9]))
    assert np.all((out >= 0) & (out <= 1))
