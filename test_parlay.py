import numpy as np

from trueodds.parlay import (
    joint_probability_from_simulations,
    pairwise_phi_matrix,
    correlation_risk_score,
)


def test_independent_like_simulation():
    rng = np.random.default_rng(1)
    x = rng.random((200000, 3)) < np.array([0.7, 0.6, 0.5])
    result = joint_probability_from_simulations(x)
    assert abs(result.joint_probability - 0.21) < 0.01
    assert abs(result.correlation_adjustment_pp) < 1.0


def test_positive_correlation_changes_joint_probability():
    rng = np.random.default_rng(2)
    latent = rng.normal(size=100000)
    a = latent + rng.normal(size=100000) > 0
    b = latent + rng.normal(size=100000) > 0
    x = np.column_stack([a, b])
    result = joint_probability_from_simulations(x)
    assert result.joint_probability > result.independent_probability
    assert correlation_risk_score(x) > 0
    assert pairwise_phi_matrix(x).shape == (2, 2)
