"""Noise models for UWOC simulations."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray


@dataclass(frozen=True)
class NoiseConfig:
    """Noise configuration for simulation-only experiments.

    Attributes:
        snr_db: Target electrical SNR in dB for additive Gaussian noise.
        seed: Deterministic random seed.
    """

    snr_db: float
    seed: int = 42


def add_awgn(signal: NDArray[np.float64], config: NoiseConfig) -> NDArray[np.float64]:
    """Add real-valued additive white Gaussian noise at a target SNR."""
    power = float(np.mean(signal**2))
    if power == 0.0:
        return signal.copy()
    noise_power = power / (10.0 ** (config.snr_db / 10.0))
    rng = np.random.default_rng(config.seed)
    noise = rng.normal(0.0, np.sqrt(noise_power), size=signal.shape)
    return signal + noise


def estimate_snr_db(clean: NDArray[np.float64], noisy: NDArray[np.float64]) -> float:
    """Estimate SNR in dB from clean and noisy waveforms."""
    noise = noisy - clean
    signal_power = float(np.mean(clean**2))
    noise_power = float(np.mean(noise**2))
    if noise_power == 0.0:
        return float("inf")
    return float(10.0 * np.log10(signal_power / noise_power))
