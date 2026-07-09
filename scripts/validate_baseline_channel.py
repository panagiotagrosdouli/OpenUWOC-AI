"""Generate publication-style baseline UWOC channel validation tables.

The script sweeps distance for each repository water preset and writes a CSV
with attenuation, deterministic gain, SNR, and BER from the deterministic OOK
simulator. It does not create measured benchmark claims.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

import numpy as np

from openuwoc_ai.channel.models import WATER_PROFILES, WaterType, beer_lambert_gain
from openuwoc_ai.simulation.link import LinkSimulationConfig, run_ook_link


def build_rows(distances_m: np.ndarray, n_bits: int, seed: int) -> list[dict[str, float | str | int]]:
    rows: list[dict[str, float | str | int]] = []
    for water_type in WaterType:
        profile = WATER_PROFILES[water_type]
        for distance_m in distances_m:
            result = run_ook_link(
                LinkSimulationConfig(
                    n_bits=n_bits,
                    water_type=water_type,
                    distance_m=float(distance_m),
                    seed=seed,
                )
            )
            rows.append(
                {
                    "water_type": water_type.value,
                    "wavelength_nm": profile.wavelength_nm,
                    "absorption_m_inv": profile.absorption_m_inv,
                    "scattering_m_inv": profile.scattering_m_inv,
                    "attenuation_m_inv": profile.attenuation_m_inv,
                    "distance_m": float(distance_m),
                    "beer_lambert_gain": beer_lambert_gain(
                        float(distance_m), profile.attenuation_m_inv
                    ),
                    "deterministic_gain": result.deterministic_gain,
                    "snr_linear": result.snr_linear,
                    "ber": result.ber,
                    "bit_errors": result.bit_errors,
                    "n_bits": result.n_bits,
                }
            )
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate baseline UWOC attenuation sweeps")
    parser.add_argument("--output", type=Path, default=Path("results/baseline_channel_sweep.csv"))
    parser.add_argument("--min-distance", type=float, default=1.0)
    parser.add_argument("--max-distance", type=float, default=60.0)
    parser.add_argument("--steps", type=int, default=25)
    parser.add_argument("--n-bits", type=int, default=4096)
    parser.add_argument("--seed", type=int, default=7)
    args = parser.parse_args()

    distances = np.linspace(args.min_distance, args.max_distance, args.steps)
    rows = build_rows(distances, n_bits=args.n_bits, seed=args.seed)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"wrote {args.output}")


if __name__ == "__main__":
    main()
