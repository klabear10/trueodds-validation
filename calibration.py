"""Probability calibration and proper scoring rules."""

from __future__ import annotations

from dataclasses import dataclass
import math
import numpy as np


def _validate(probabilities, outcomes):
    p = np.asarray(probabilities, dtype=float)
    y = np.asarray(outcomes, dtype=float)
    if p.shape != y.shape:
        raise ValueError("probabilities and outcomes must have the same shape")
    if p.ndim != 1:
        raise ValueError("inputs must be 1-D")
    if np.any((p < 0) | (p > 1)):
        raise ValueError("probabilities must be between 0 and 1")
    if np.any((y != 0) & (y != 1)):
        raise ValueError("outcomes must be binary")
    return p, y


def brier_score(probabilities, outcomes) -> float:
    p, y = _validate(probabilities, outcomes)
    if len(p) == 0:
        return float("nan")
    return float(np.mean((p - y) ** 2))


def log_loss(probabilities, outcomes, eps: float = 1e-12) -> float:
    p, y = _validate(probabilities, outcomes)
    if len(p) == 0:
        return float("nan")
    p = np.clip(p, eps, 1 - eps)
    return float(-np.mean(y * np.log(p) + (1 - y) * np.log(1 - p)))


def calibration_table(probabilities, outcomes, bins: int = 10) -> list[dict]:
    p, y = _validate(probabilities, outcomes)
    if bins < 2:
        raise ValueError("bins must be >= 2")
    edges = np.linspace(0.0, 1.0, bins + 1)
    idx = np.digitize(p, edges[1:-1], right=False)

    rows = []
    for b in range(bins):
        mask = idx == b
        n = int(mask.sum())
        if n == 0:
            continue
        rows.append({
            "bin": b,
            "lower": float(edges[b]),
            "upper": float(edges[b + 1]),
            "n": n,
            "mean_predicted": float(p[mask].mean()),
            "actual_rate": float(y[mask].mean()),
            "abs_error": float(abs(p[mask].mean() - y[mask].mean())),
        })
    return rows


def expected_calibration_error(probabilities, outcomes, bins: int = 10) -> float:
    rows = calibration_table(probabilities, outcomes, bins=bins)
    n = sum(r["n"] for r in rows)
    if n == 0:
        return float("nan")
    return float(sum(r["n"] * r["abs_error"] for r in rows) / n)


@dataclass
class HistogramCalibrator:
    """Simple leakage-safe calibrator when fit only on training data.

    Beta-binomial style shrinkage toward the global outcome rate prevents
    tiny calibration buckets from becoming overconfident.
    """

    bins: int = 10
    prior_strength: float = 20.0

    def fit(self, probabilities, outcomes):
        p, y = _validate(probabilities, outcomes)
        if len(p) == 0:
            raise ValueError("cannot fit on empty data")
        self.edges_ = np.linspace(0.0, 1.0, self.bins + 1)
        idx = np.digitize(p, self.edges_[1:-1], right=False)
        global_rate = float(y.mean())
        values = []
        counts = []
        for b in range(self.bins):
            mask = idx == b
            n = int(mask.sum())
            wins = float(y[mask].sum()) if n else 0.0
            posterior = (wins + self.prior_strength * global_rate) / (n + self.prior_strength)
            values.append(float(posterior))
            counts.append(n)
        self.values_ = np.array(values, dtype=float)
        self.counts_ = np.array(counts, dtype=int)
        self.global_rate_ = global_rate
        return self

    def predict(self, probabilities):
        if not hasattr(self, "values_"):
            raise RuntimeError("fit calibrator before predict")
        p = np.asarray(probabilities, dtype=float)
        if np.any((p < 0) | (p > 1)):
            raise ValueError("probabilities must be between 0 and 1")
        idx = np.digitize(p, self.edges_[1:-1], right=False)
        return self.values_[idx]
