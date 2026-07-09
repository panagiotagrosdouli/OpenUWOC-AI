"""Synthetic channel-state dataset generation for UWOC AI experiments.

The generator is intentionally simulation-first. It samples transparent physical
parameters, runs the repository's OOK link simulator, and records both inputs and
outputs so downstream notebooks can train or audit AI receivers without claiming
real measured-data performance.
"""

from __future__ import annotations

import csv
import json
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np

from openuwoc_ai.channel.models import WATER_PROFILES, WaterType
from openuwoc_ai.simulation.link import LinkSimulationConfig, run_ook_link


@dataclass(frozen=True)
class DatasetGenerationConfig:
    """Configuration for a deterministic synthetic UWOC channel dataset."""

    n_samples: int = 128
    n_bits: int = 4096
    seed: int = 7
    water_types: tuple[WaterType, ...] = (
        WaterType.CLEAR_OCEAN,
        WaterType.COASTAL,
        WaterType.TURBID_HARBOR,
    )
    distance_min_m: float = 2.0
    distance_max_m: float = 60.0
    tx_power_min_w: float = 0.2
    tx_power_max_w: float = 2.0
    wavelength_min_nm: float = 450.0
    wavelength_max_nm: float = 550.0
    thermal_noise_min: float = 0.005
    thermal_noise_max: float = 0.08
    pointing_offset_max_m: float = 0.05
    turbulence_sigma_max: float = 0.25

    def validate(self) -> None:
        """Validate ranges before sampling."""
        if self.n_samples <= 0:
            raise ValueError("n_samples must be positive")
        if self.n_bits <= 0:
            raise ValueError("n_bits must be positive")
        if not self.water_types:
            raise ValueError("at least one water type is required")
        if self.distance_min_m < 0 or self.distance_max_m <= self.distance_min_m:
            raise ValueError("distance range must be non-negative and increasing")
        if self.tx_power_min_w <= 0 or self.tx_power_max_w <= self.tx_power_min_w:
            raise ValueError("tx power range must be positive and increasing")
        if self.wavelength_max_nm <= self.wavelength_min_nm:
            raise ValueError("wavelength range must be increasing")
        if self.thermal_noise_min < 0 or self.thermal_noise_max < self.thermal_noise_min:
            raise ValueError("thermal noise range must be non-negative and increasing")
        if self.pointing_offset_max_m < 0 or self.turbulence_sigma_max < 0:
            raise ValueError("pointing and turbulence maxima must be non-negative")


@dataclass(frozen=True)
class DatasetMetadata:
    """Machine-readable assumptions attached to generated synthetic datasets."""

    generator: str
    version: str
    seed: int
    n_samples: int
    n_bits_per_sample: int
    assumptions: tuple[str, ...]
    fields: tuple[str, ...]


def _sample_config(index: int, rng: np.random.Generator, cfg: DatasetGenerationConfig) -> dict[str, float | str | int]:
    water_type = WaterType(rng.choice([water.value for water in cfg.water_types]))
    profile = WATER_PROFILES[water_type]
    distance_m = float(rng.uniform(cfg.distance_min_m, cfg.distance_max_m))
    tx_power_w = float(rng.uniform(cfg.tx_power_min_w, cfg.tx_power_max_w))
    wavelength_nm = float(rng.uniform(cfg.wavelength_min_nm, cfg.wavelength_max_nm))
    thermal_noise_std = float(rng.uniform(cfg.thermal_noise_min, cfg.thermal_noise_max))
    pointing_offset_m = float(rng.uniform(0.0, cfg.pointing_offset_max_m))
    turbulence_sigma = float(rng.uniform(0.0, cfg.turbulence_sigma_max))
    sample_seed = int(cfg.seed * 100_000 + index)
    return {
        "sample_id": index,
        "water_type": water_type.value,
        "distance_m": distance_m,
        "tx_power_w": tx_power_w,
        "wavelength_nm": wavelength_nm,
        "absorption_m_inv": profile.absorption_m_inv,
        "scattering_m_inv": profile.scattering_m_inv,
        "thermal_noise_std": thermal_noise_std,
        "shot_noise_scale": 0.002,
        "pointing_offset_m": pointing_offset_m,
        "beam_waist_m": 0.05,
        "turbulence_sigma": turbulence_sigma,
        "seed": sample_seed,
    }


def generate_channel_dataset(cfg: DatasetGenerationConfig) -> list[dict[str, float | str | int]]:
    """Generate rows containing sampled channel parameters and simulated labels.

    The label-like fields are `ber`, `snr_linear`, and `bit_errors`. They are
    produced by the same deterministic simulator used elsewhere in the repository
    and should be interpreted as synthetic supervision targets only.
    """
    cfg.validate()
    rng = np.random.default_rng(cfg.seed)
    rows: list[dict[str, float | str | int]] = []
    for index in range(cfg.n_samples):
        sample = _sample_config(index, rng, cfg)
        sim_config = LinkSimulationConfig(
            n_bits=cfg.n_bits,
            water_type=WaterType(str(sample["water_type"])),
            distance_m=float(sample["distance_m"]),
            tx_power_w=float(sample["tx_power_w"]),
            thermal_noise_std=float(sample["thermal_noise_std"]),
            shot_noise_scale=float(sample["shot_noise_scale"]),
            pointing_offset_m=float(sample["pointing_offset_m"]),
            beam_waist_m=float(sample["beam_waist_m"]),
            turbulence_sigma=float(sample["turbulence_sigma"]),
            seed=int(sample["seed"]),
        )
        result = run_ook_link(sim_config)
        rows.append(
            {
                **sample,
                "n_bits": cfg.n_bits,
                "deterministic_gain": result.deterministic_gain,
                "snr_linear": result.snr_linear,
                "ber": result.ber,
                "bit_errors": result.bit_errors,
                "ci95_low": result.ci95_low,
                "ci95_high": result.ci95_high,
            }
        )
    return rows


def dataset_metadata(cfg: DatasetGenerationConfig, fields: tuple[str, ...]) -> DatasetMetadata:
    """Return metadata documenting simulation assumptions and schema."""
    return DatasetMetadata(
        generator="openuwoc_ai.datasets.synthetic.generate_channel_dataset",
        version="0.1.0",
        seed=cfg.seed,
        n_samples=cfg.n_samples,
        n_bits_per_sample=cfg.n_bits,
        assumptions=(
            "Rows are synthetic simulations, not measured underwater experiments.",
            "Absorption/scattering coefficients use repository water-type presets.",
            "OOK threshold detection is the baseline receiver.",
            "BER and SNR are generated labels for AI prototyping only.",
            "Random sampling is deterministic for the configured seed.",
        ),
        fields=fields,
    )


def write_dataset_csv(rows: list[dict[str, float | str | int]], path: Path) -> None:
    """Write generated rows to CSV."""
    if not rows:
        raise ValueError("cannot write an empty dataset")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def write_dataset_metadata(metadata: DatasetMetadata, path: Path) -> None:
    """Write dataset metadata as JSON."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(asdict(metadata), indent=2, sort_keys=True) + "\n")
