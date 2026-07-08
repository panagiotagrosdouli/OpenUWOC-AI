"""Run reproducible UWOC experiments from YAML configs."""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

import yaml

from openuwoc_ai.channel.models import WaterType
from openuwoc_ai.simulation.link import LinkSimulationConfig, run_ook_link


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a YAML-configured OOK UWOC simulation")
    parser.add_argument("config", type=Path)
    parser.add_argument("--output", type=Path, default=Path("results/experiment.csv"))
    args = parser.parse_args()

    data = yaml.safe_load(args.config.read_text())
    config = LinkSimulationConfig(
        n_bits=int(data.get("n_bits", 10000)),
        water_type=WaterType(data.get("water_type", "coastal")),
        distance_m=float(data.get("distance_m", 10.0)),
        tx_power_w=float(data.get("tx_power_w", 1.0)),
        thermal_noise_std=float(data.get("thermal_noise_std", 0.02)),
        shot_noise_scale=float(data.get("shot_noise_scale", 0.0)),
        ambient_light_w=float(data.get("ambient_light_w", 0.0)),
        pointing_offset_m=float(data.get("pointing_offset_m", 0.0)),
        beam_waist_m=float(data.get("beam_waist_m", 0.05)),
        turbulence_sigma=float(data.get("turbulence_sigma", 0.0)),
        seed=int(data.get("seed", 7)),
    )
    result = run_ook_link(config)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(result.__dict__.keys()))
        writer.writeheader()
        writer.writerow(result.__dict__)
    print(f"wrote {args.output}")


if __name__ == "__main__":
    main()
