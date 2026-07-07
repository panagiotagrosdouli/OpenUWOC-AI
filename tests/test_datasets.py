"""Tests for synthetic UWOC dataset generation."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest

from openuwoc_ai.datasets import DatasetGenerationConfig, export_dataset, generate_link_budget_dataset


def test_generate_link_budget_dataset_shape_and_columns() -> None:
    config = DatasetGenerationConfig(environment="coastal", num_samples=25, seed=1)

    dataset = generate_link_budget_dataset(config)

    assert len(dataset) == 25
    assert "distance_m" in dataset.columns
    assert "received_power_w" in dataset.columns
    assert "signal_to_noise_ratio" in dataset.columns


def test_dataset_generation_is_reproducible() -> None:
    config = DatasetGenerationConfig(environment="clear_ocean", num_samples=10, seed=123)

    first = generate_link_budget_dataset(config)
    second = generate_link_budget_dataset(config)

    pd.testing.assert_frame_equal(first, second)


def test_invalid_dataset_config_raises_error() -> None:
    config = DatasetGenerationConfig(num_samples=0)

    with pytest.raises(ValueError):
        generate_link_budget_dataset(config)


def test_export_dataset_to_csv(tmp_path: Path) -> None:
    config = DatasetGenerationConfig(environment="coastal", num_samples=5)
    dataset = generate_link_budget_dataset(config)
    output_path = tmp_path / "dataset.csv"

    exported = export_dataset(dataset, output_path)

    assert exported.exists()
    assert exported.suffix == ".csv"
