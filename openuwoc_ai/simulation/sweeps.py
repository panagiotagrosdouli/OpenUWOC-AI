"""Parameter sweeps for UWOC simulations."""

from __future__ import annotations

import pandas as pd

from openuwoc_ai.simulation.link import LinkSimulationConfig, simulate_ook_link


def snr_sweep(base_config: LinkSimulationConfig, snr_values_db: list[float]) -> pd.DataFrame:
    """Run an SNR sweep and return a tabular result."""
    rows: list[dict[str, float | str | int]] = []
    for snr_db in snr_values_db:
        config = LinkSimulationConfig(
            water_type=base_config.water_type,
            distance_m=base_config.distance_m,
            snr_db=snr_db,
            num_bits=base_config.num_bits,
            transmit_amplitude=base_config.transmit_amplitude,
            threshold=base_config.threshold,
            seed=base_config.seed,
        )
        result = simulate_ook_link(config)
        rows.append(
            {
                "water_type": result.water_type,
                "distance_m": result.distance_m,
                "snr_db": result.snr_db,
                "ber": result.ber,
                "channel_gain": result.channel_gain,
                "num_bits": result.num_bits,
            }
        )
    return pd.DataFrame(rows)
