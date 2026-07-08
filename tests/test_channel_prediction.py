"""Tests for baseline UWOC channel prediction models."""

from __future__ import annotations

import pytest

from openuwoc_ai.ai import LinearChannelPredictor
from openuwoc_ai.datasets import DatasetGenerationConfig, generate_link_budget_dataset


def test_linear_channel_predictor_fit_predict_evaluate() -> None:
    dataset = generate_link_budget_dataset(
        DatasetGenerationConfig(environment="coastal", num_samples=100, seed=10)
    )
    feature_columns = [
        "distance_m",
        "transmit_power_w",
        "attenuation_coefficient",
        "beam_divergence_rad",
        "receiver_aperture_m",
    ]

    train_data, test_data = LinearChannelPredictor.train_test_split(dataset, seed=10)
    predictor = LinearChannelPredictor().fit(train_data, feature_columns, "received_power_w")
    predictions = predictor.predict(test_data)
    metrics = predictor.evaluate(test_data, "received_power_w")

    assert predictor.is_fitted
    assert len(predictions) == len(test_data)
    assert metrics.mean_absolute_error >= 0
    assert metrics.root_mean_squared_error >= 0


def test_predict_before_fit_raises_error() -> None:
    dataset = generate_link_budget_dataset(DatasetGenerationConfig(num_samples=5))
    predictor = LinearChannelPredictor()

    with pytest.raises(RuntimeError):
        predictor.predict(dataset)


def test_train_test_split_is_deterministic() -> None:
    dataset = generate_link_budget_dataset(DatasetGenerationConfig(num_samples=50, seed=5))

    first_train, first_test = LinearChannelPredictor.train_test_split(dataset, seed=5)
    second_train, second_test = LinearChannelPredictor.train_test_split(dataset, seed=5)

    assert first_train.equals(second_train)
    assert first_test.equals(second_test)
