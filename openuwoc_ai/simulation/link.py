"""Configuration-driven end-to-end UWOC link simulations."""

from __future__ import annotations

from dataclasses import dataclass, replace

import numpy as np
from numpy.typing import NDArray

from openuwoc_ai.channel.models import ChannelConfig, UnderwaterOpticalChannel, WaterType
from openuwoc_ai.evaluation.metrics import bit_error_rate, wilson_interval
from openuwoc_ai.modulation.ook import bits_to_ook, random_bits, threshold_detect


@dataclass(frozen=True)
class LinkSimulationConfig:
    """Minimal reproducible OOK link simulation configuration."""

    n_bits: int = 10000
    water_type: WaterType = WaterType.COASTAL
    distance_m: float = 10.0
    tx_power_w: float = 1.0
    thermal_noise_std: float = 0.02
    shot_noise_scale: float = 0.0
    ambient_light_w: float = 0.0
    pointing_offset_m: float = 0.0
    beam_waist_m: float = 0.05
    turbulence_sigma: float = 0.0
    seed: int = 7


@dataclass(frozen=True)
class LinkSimulationResult:
    """Outputs from a baseline OOK simulation."""

    ber: float
    bit_errors: int
    n_bits: int
    ci95_low: float
    ci95_high: float
    deterministic_gain: float
    snr_linear: float


def run_ook_link(config: LinkSimulationConfig) -> LinkSimulationResult:
    """Run a deterministic-seed OOK transmitter-channel-threshold receiver chain."""
    bits = random_bits(config.n_bits, seed=config.seed)
    tx = bits_to_ook(bits, optical_power_w=config.tx_power_w)
    channel = UnderwaterOpticalChannel(
        ChannelConfig(
            water_type=config.water_type,
            distance_m=config.distance_m,
            tx_power_w=config.tx_power_w,
            thermal_noise_std=config.thermal_noise_std,
            shot_noise_scale=config.shot_noise_scale,
            ambient_light_w=config.ambient_light_w,
            pointing_offset_m=config.pointing_offset_m,
            beam_waist_m=config.beam_waist_m,
            turbulence_sigma=config.turbulence_sigma,
            seed=config.seed,
        )
    )
    rx = channel.propagate(tx)
    detected = threshold_detect(rx)
    errors = int(np.sum(bits != detected))
    ber = bit_error_rate(bits, detected)
    low, high = wilson_interval(errors, config.n_bits)
    return LinkSimulationResult(
        ber=ber,
        bit_errors=errors,
        n_bits=config.n_bits,
        ci95_low=low,
        ci95_high=high,
        deterministic_gain=channel.deterministic_gain,
        snr_linear=channel.snr_linear(),
    )


def snr_sweep(noise_stds: NDArray[np.float64], base_config: LinkSimulationConfig) -> list[LinkSimulationResult]:
    """Run a noise-standard-deviation sweep as a practical SNR sweep."""
    return [run_ook_link(replace(base_config, thermal_noise_std=float(std))) for std in noise_stds]


# Backward-compatible alias.
simulate_ook_link = run_ook_link
