"""Baseline AI models for UWOC channel prediction."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class RegressionMetrics:
    """Regression metrics for channel-prediction experiments."""

    mean_absolute_error: float
    root_mean_squared_error: float
    r2_score: float


class LinearChannelPredictor:
    """Ordinary least-squares baseline for UWOC channel prediction.

    This model is intentionally lightweight and dependency-free. It provides a
    transparent baseline that future deep learning, reinforcement learning, and
    transformer-based models should outperform.
    """

    def __init__(self) -> None:
        self._weights: np.ndarray | None = None
        self._feature_columns: list[str] | None = None

    @property
    def is_fitted(self) -> bool:
        """Return whether the model has been fitted."""
        return self._weights is not None

    def fit(
        self,
        data: pd.DataFrame,
        feature_columns: list[str],
        target_column: str,
    ) -> "LinearChannelPredictor":
        """Fit the predictor using ordinary least squares."""
        x = self._design_matrix(data, feature_columns)
        y = data[target_column].to_numpy(dtype=float)

        self._weights = np.linalg.pinv(x) @ y
        self._feature_columns = list(feature_columns)
        return self

    def predict(self, data: pd.DataFrame) -> np.ndarray:
        """Predict the target variable for a dataframe."""
        if self._weights is None or self._feature_columns is None:
            raise RuntimeError("LinearChannelPredictor must be fitted before prediction.")

        x = self._design_matrix(data, self._feature_columns)
        return x @ self._weights

    def evaluate(self, data: pd.DataFrame, target_column: str) -> RegressionMetrics:
        """Evaluate the predictor on a dataframe."""
        y_true = data[target_column].to_numpy(dtype=float)
        y_pred = self.predict(data)
        residuals = y_true - y_pred

        mae = float(np.mean(np.abs(residuals)))
        rmse = float(np.sqrt(np.mean(residuals**2)))
        total_sum_squares = float(np.sum((y_true - np.mean(y_true)) ** 2))
        residual_sum_squares = float(np.sum(residuals**2))
        r2 = 1.0 - residual_sum_squares / total_sum_squares if total_sum_squares > 0 else 0.0

        return RegressionMetrics(
            mean_absolute_error=mae,
            root_mean_squared_error=rmse,
            r2_score=float(r2),
        )

    @staticmethod
    def train_test_split(
        data: pd.DataFrame,
        test_fraction: float = 0.2,
        seed: int = 42,
    ) -> tuple[pd.DataFrame, pd.DataFrame]:
        """Split a dataframe into deterministic train and test partitions."""
        if not 0.0 < test_fraction < 1.0:
            raise ValueError("test_fraction must be between 0 and 1.")

        rng = np.random.default_rng(seed)
        indices = np.arange(len(data))
        rng.shuffle(indices)
        test_size = max(1, int(len(data) * test_fraction))
        test_indices = indices[:test_size]
        train_indices = indices[test_size:]

        return (
            data.iloc[train_indices].reset_index(drop=True),
            data.iloc[test_indices].reset_index(drop=True),
        )

    @staticmethod
    def _design_matrix(data: pd.DataFrame, feature_columns: list[str]) -> np.ndarray:
        features = data[feature_columns].to_numpy(dtype=float)
        bias = np.ones((features.shape[0], 1), dtype=float)
        return np.hstack([bias, features])
