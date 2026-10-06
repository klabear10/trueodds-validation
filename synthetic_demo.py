"""Synthetic example showing the validation engine end to end."""

import numpy as np

from trueodds.model import LogisticProbabilityModel
from trueodds.calibration import HistogramCalibrator, brier_score
from trueodds.parlay import joint_probability_from_simulations


rng = np.random.default_rng(7)
X = rng.normal(size=(1200, 4))
true_logit = 0.5 * X[:, 0] - 0.35 * X[:, 1] + 0.25 * X[:, 2]
true_p = 1 / (1 + np.exp(-true_logit))
y = rng.binomial(1, true_p)

train, cal, test = slice(0, 700), slice(700, 950), slice(950, None)

model = LogisticProbabilityModel().fit(X[train], y[train])
p_cal_raw = model.predict_proba(X[cal])
p_test_raw = model.predict_proba(X[test])

calibrator = HistogramCalibrator(bins=8).fit(p_cal_raw, y[cal])
p_test_cal = calibrator.predict(p_test_raw)

print("raw Brier:", round(brier_score(p_test_raw, y[test]), 4))
print("calibrated Brier:", round(brier_score(p_test_cal, y[test]), 4))

# A toy correlated 3-leg parlay simulation
latent = rng.normal(size=50000)
leg1 = latent + rng.normal(scale=1.1, size=50000) > 0.2
leg2 = 0.6 * latent + rng.normal(scale=1.1, size=50000) > 0.4
leg3 = -0.2 * latent + rng.normal(scale=1.2, size=50000) > 0.0

result = joint_probability_from_simulations(np.column_stack([leg1, leg2, leg3]))
print(result)
