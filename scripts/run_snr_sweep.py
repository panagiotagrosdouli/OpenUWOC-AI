"""Run a simulation-only OOK SNR sweep.

This script intentionally writes generated outputs to results/ and does not
ship precomputed benchmark numbers.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import yaml

from openuwoc_ai.simulation import LinkSimulationConfig, snr_sweep
from openuwoc_ai.visualization import plot_ber_vs_snr


def main() -> None:
    parser = argparse.ArgumentParser(description="Run OOK UWOC SNR sweep.")
    parser.add_argument("--config", default="configs/experiments/ook_snr_sweep.yaml")
    args = parser.parse_args()

    with Path(args.config).open("r", encoding="utf-8") as handle:
        config = yaml.safe_load(handle)

    base = LinkSimulationConfig(
        water_type=config["water_type"],
        distance_m=float(config["distance_m"]),
        snr_db=float(config["snr_values_db"][0]),
        num_bits=int(config["num_bits"]),
        transmit_amplitude=float(config["transmit_amplitude"]),
        threshold=float(config["threshold"]),
        seed=int(config["random_seed"]),
    )
    results = snr_sweep(base, [float(value) for value in config["snr_values_db"]])

    table_path = Path(config["outputs"]["table"])
    table_path.parent.mkdir(parents=True, exist_ok=True)
    results.to_csv(table_path, index=False)

    figure_path = plot_ber_vs_snr(results, config["outputs"]["figure"])
    print(f"Saved table: {table_path}")
    print(f"Saved figure: {figure_path}")


if __name__ == "__main__":
    main()
