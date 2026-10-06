"""Joint-probability analysis for parlays."""

from __future__ import annotations

from dataclasses import dataclass
import numpy as np


@dataclass(frozen=True)
class JointProbabilityResult:
    joint_probability: float
    independent_probability: float
    correlation_adjustment_pp: float
    correlation_risk_score: float
    simulations: int


def _as_bool_matrix(simulated_leg_hits) -> np.ndarray:
    x = np.asarray(simulated_leg_hits)
    if x.ndim != 2:
        raise ValueError("simulated_leg_hits must be a 2-D matrix")
    if x.shape[0] < 1 or x.shape[1] < 1:
        raise ValueError("simulation matrix cannot be empty")
    return x.astype(bool)


def pairwise_phi_matrix(simulated_leg_hits) -> np.ndarray:
    """Phi/Pearson correlations between binary leg outcomes."""
    x = _as_bool_matrix(simulated_leg_hits).astype(float)
    if x.shape[1] == 1:
        return np.array([[1.0]])
    with np.errstate(invalid="ignore", divide="ignore"):
        corr = np.corrcoef(x, rowvar=False)
    corr = np.nan_to_num(corr, nan=0.0)
    np.fill_diagonal(corr, 1.0)
    return corr


def correlation_risk_score(simulated_leg_hits) -> float:
    """0–100 risk score based on absolute pairwise dependence.

    This is a model-risk indicator, not a claim that correlation itself is bad.
    """
    corr = pairwise_phi_matrix(simulated_leg_hits)
    if corr.shape[0] <= 1:
        return 0.0
    tri = np.abs(corr[np.triu_indices(corr.shape[0], k=1)])
    if len(tri) == 0:
        return 0.0
    mean_abs = float(np.mean(tri))
    max_abs = float(np.max(tri))
    score = 100.0 * min(1.0, 0.65 * mean_abs + 0.35 * max_abs)
    return float(score)


def joint_probability_from_simulations(simulated_leg_hits) -> JointProbabilityResult:
    """Estimate parlay joint probability from shared-state simulations.

    Each row is one simulated game/slate state.
    Each column is a parlay leg.
    """
    x = _as_bool_matrix(simulated_leg_hits)
    marginals = x.mean(axis=0)
    joint = float(np.all(x, axis=1).mean())
    independent = float(np.prod(marginals))
    adjustment_pp = (joint - independent) * 100.0
    return JointProbabilityResult(
        joint_probability=joint,
        independent_probability=independent,
        correlation_adjustment_pp=float(adjustment_pp),
        correlation_risk_score=correlation_risk_score(x),
        simulations=int(x.shape[0]),
    )
