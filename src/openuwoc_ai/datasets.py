"""Synthetic dataset generation for AI-ready UWOC experiments."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

from openuwoc_ai.channels import UnderwaterOpticalChannel
from openuwoc_ai.environments import WaterEnvironment


@dataclass(frozen=True)
class DatasetGenerationConfig:
    """Configuration for synthetic UWOC dataset generation."""

    environment: str = "coastal"
    num_samples: int = 1_000
    min_distance_m: float = 1.0
    max_distance_m: float = 50.0
    min_transmit_power_w: float = 0.05
    max_transmit_power_w: float = 2.0
    beam_divergence_rad: float = 1e-3
    receiver_aperture_m: float = 0.05
    seed: int = 42

    def validate(self) -> None:
        """Validate dataset-generation parameters."""
        if self.num_samples <= 0:
            raise ValueError("num_samples must be positive.")
        if self.min_distance_m <= 0 or self.max_distance_m <= self.min_distance_m:
            raise ValueError("distance range must be positive and increasing.")
        if self.min_transmit_power_w < 0 or self.max_transmit_power_w <= self.min_transmit_power_w:
            raise ValueError("transmit power range must be non-negative and increasing.")
        if self.beam_divergence_rad <= 0:
            raise ValueError("beam_divergence_rad must be positive.")
        if self.receiver_aperture_m <= 0:
            raise ValueError("receiver_aperture_m must be positive.")


def generate_link_budget_dataset(config: DatasetGenerationConfig) -> pd.DataFrame:
    """Generate a synthetic link-budget dataset for UWOC AI experiments.

    The output is a tabular dataset where each row describes one simulated
    transmission condition and its corresponding received power and SNR.
    """
    config.validate()
    rng = np.random.default_rng(config.seed)

    environment = WaterEnvironment.preset(config.environment)
    channel = UnderwaterOpticalChannel(
        environment=environment,
        beam_divergence_rad=config.beam_divergence_rad,
        receiver_aperture_m=config.receiver_aperture_m,
    )

    distances = rng.uniform(config.min_distance_m, config.max_distance_m, config.num_samples)
    transmit_powers = rng.uniform(
        config.min_transmit_power_w,
        config.max_transmit_power_w,
        config.num_samples,
    )

    records: list[dict[str, float | str]] = []
    for distance_m, transmit_power_w in zip(distances, transmit_powers, strict=True):
        result = channel.link_budget(
            distance_m=float(distance_m),
            transmit_power_w=float(transmit_power_w),
        )
        records.append(
            {
                "environment": environment.name,
                "distance_m": result.distance_m,
                "transmit_power_w": result.transmit_power_w,
                "absorption_coefficient": environment.absorption_coefficient,
                "scattering_coefficient": environment.scattering_coefficient,
                "attenuation_coefficient": environment.attenuation_coefficient,
                "beam_divergence_rad": config.beam_divergence_rad,
                "receiver_aperture_m": config.receiver_aperture_m,
                "attenuation_loss": result.attenuation_loss,
                "geometric_loss": result.geometric_loss,
                "received_power_w": result.received_power_w,
                "signal_to_noise_ratio": result.signal_to_noise_ratio,
            }
        )

    return pd.DataFrame.from_records(records)


def export_dataset(data: pd.DataFrame, output_path: str | Path) -> Path:
    """Export a dataset to CSV or Parquet based on the file extension."""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    if path.suffix == ".csv":
        data.to_csv(path, index=False)
    elif path.suffix == ".parquet":
        data.to_parquet(path, index=False)
    else:
        raise ValueError("Unsupported output format. Use .csv or .parquet.")

    return path
