"""End-to-end OOK UWOC link simulation."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

from openuwoc_ai.channel import NoiseConfig, WaterProfile, add_awgn, beer_lambert_gain
from openuwoc_ai.evaluation import bit_error_rate
from openuwoc_ai.modulation import demodulate_ook, modulate_ook


@dataclass(frozen=True)
class LinkSimulationConfig:
    """Configuration for a simulation-only OOK UWOC link."""

    water_type: str = "coastal"
    distance_m: float = 10.0
    snr_db: float = 20.0
    num_bits: int = 10_000
    transmit_amplitude: float = 1.0
    threshold: float = 0.5
    seed: int = 42


@dataclass(frozen=True)
class LinkSimulationResult:
    """Outputs from an OOK link simulation."""

    ber: float
    channel_gain: float
    snr_db: float
    distance_m: float
    water_type: str
    num_bits: int


def simulate_ook_link(config: LinkSimulationConfig) -> LinkSimulationResult:
    """Simulate OOK transmission through a Beer-Lambert UWOC channel.

    This is a simulation-only baseline using AWGN and threshold detection.
    """
    if config.num_bits <= 0:
        raise ValueError("num_bits must be positive.")
    if config.distance_m < 0:
        raise ValueError("distance_m must be non-negative.")

    rng = np.random.default_rng(config.seed)
    bits: NDArray[np.int_] = rng.integers(0, 2, size=config.num_bits)
    water = WaterProfile.preset(config.water_type)
    gain = beer_lambert_gain(water.attenuation_m_inv, config.distance_m)

    transmitted = modulate_ook(bits, amplitude=config.transmit_amplitude)
    clean_received = transmitted * gain
    noisy_received = add_awgn(clean_received, NoiseConfig(snr_db=config.snr_db, seed=config.seed + 1))
    estimated_bits = demodulate_ook(noisy_received, threshold=config.threshold * gain)
    ber = bit_error_rate(bits, estimated_bits)

    return LinkSimulationResult(
        ber=ber,
        channel_gain=gain,
        snr_db=config.snr_db,
        distance_m=config.distance_m,
        water_type=water.name,
        num_bits=config.num_bits,
    )
