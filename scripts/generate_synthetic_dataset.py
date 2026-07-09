"""Generate AI-ready synthetic UWOC channel-state datasets."""

from __future__ import annotations

import argparse
from pathlib import Path

import yaml

from openuwoc_ai.channel.models import WaterType
from openuwoc_ai.datasets.synthetic import (
    DatasetGenerationConfig,
    dataset_metadata,
    generate_channel_dataset,
    write_dataset_csv,
    write_dataset_metadata,
)


def _load_config(path: Path) -> DatasetGenerationConfig:
    data = yaml.safe_load(path.read_text())
    if data is None:
        data = {}
    water_types = tuple(WaterType(item) for item in data.get("water_types", ["coastal"]))
    return DatasetGenerationConfig(
        n_samples=int(data.get("n_samples", 128)),
        n_bits=int(data.get("n_bits", 4096)),
        seed=int(data.get("seed", 7)),
        water_types=water_types,
        distance_min_m=float(data.get("distance_min_m", 2.0)),
        distance_max_m=float(data.get("distance_max_m", 60.0)),
        tx_power_min_w=float(data.get("tx_power_min_w", 0.2)),
        tx_power_max_w=float(data.get("tx_power_max_w", 2.0)),
        wavelength_min_nm=float(data.get("wavelength_min_nm", 450.0)),
        wavelength_max_nm=float(data.get("wavelength_max_nm", 550.0)),
        thermal_noise_min=float(data.get("thermal_noise_min", 0.005)),
        thermal_noise_max=float(data.get("thermal_noise_max", 0.08)),
        pointing_offset_max_m=float(data.get("pointing_offset_max_m", 0.05)),
        turbulence_sigma_max=float(data.get("turbulence_sigma_max", 0.25)),
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate deterministic synthetic UWOC datasets")
    parser.add_argument("config", type=Path)
    parser.add_argument("--csv", type=Path, default=Path("results/datasets/synthetic_channel_states.csv"))
    parser.add_argument(
        "--metadata",
        type=Path,
        default=Path("results/datasets/synthetic_channel_states.metadata.json"),
    )
    args = parser.parse_args()

    cfg = _load_config(args.config)
    rows = generate_channel_dataset(cfg)
    write_dataset_csv(rows, args.csv)
    write_dataset_metadata(dataset_metadata(cfg, tuple(rows[0].keys())), args.metadata)
    print(f"wrote {args.csv}")
    print(f"wrote {args.metadata}")


if __name__ == "__main__":
    main()
