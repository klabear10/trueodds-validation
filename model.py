"""A transparent trainable baseline probability model.

This is intentionally simple. It lets TrueOdds consume pregame football
features without using sportsbook lines as predictors.
"""

from __future__ import annotations
import numpy as np


class LogisticProbabilityModel:
    def __init__(self, learning_rate: float = 0.05, epochs: int = 3000, l2: float = 1e-3):
        self.learning_rate = learning_rate
        self.epochs = epochs
        self.l2 = l2

    @staticmethod
    def _sigmoid(z):
        z = np.clip(z, -35, 35)
        return 1.0 / (1.0 + np.exp(-z))

    def fit(self, X, y):
        X = np.asarray(X, dtype=float)
        y = np.asarray(y, dtype=float)

        if X.ndim != 2:
            raise ValueError("X must be 2-D")
        if y.ndim != 1 or len(y) != len(X):
            raise ValueError("y must be 1-D and match X rows")
        if np.any((y != 0) & (y != 1)):
            raise ValueError("y must be binary")

        self.mean_ = X.mean(axis=0)
        self.scale_ = X.std(axis=0)
        self.scale_[self.scale_ == 0] = 1.0
        Z = (X - self.mean_) / self.scale_

        self.intercept_ = 0.0
        self.coef_ = np.zeros(Z.shape[1], dtype=float)

        n = len(Z)
        for _ in range(self.epochs):
            logits = self.intercept_ + Z @ self.coef_
            p = self._sigmoid(logits)
            error = p - y
            grad_b = float(error.mean())
            grad_w = (Z.T @ error) / n + self.l2 * self.coef_

            self.intercept_ -= self.learning_rate * grad_b
            self.coef_ -= self.learning_rate * grad_w

        return self

    def predict_proba(self, X):
        if not hasattr(self, "coef_"):
            raise RuntimeError("fit model before predict")
        X = np.asarray(X, dtype=float)
        Z = (X - self.mean_) / self.scale_
        return self._sigmoid(self.intercept_ + Z @ self.coef_)
