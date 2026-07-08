"""Evaluation metrics for UWOC link simulations."""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray


def bit_error_rate(reference_bits: NDArray[np.integer], estimated_bits: NDArray[np.integer]) -> float:
    """Compute BER between two binary vectors."""
    ref = np.asarray(reference_bits, dtype=int)
    est = np.asarray(estimated_bits, dtype=int)
    if ref.shape != est.shape:
        raise ValueError("reference_bits and estimated_bits must have the same shape")
    if ref.size == 0:
        raise ValueError("bit arrays must not be empty")
    return float(np.mean(ref != est))


def symbol_error_rate(reference: NDArray[np.integer], estimated: NDArray[np.integer]) -> float:
    """Compute symbol error rate."""
    return bit_error_rate(reference, estimated)


def snr_db(signal_power: float, noise_power: float) -> float:
    """Convert linear signal and noise powers to SNR in dB."""
    if signal_power < 0 or noise_power < 0:
        raise ValueError("powers must be non-negative")
    if noise_power == 0:
        return float("inf")
    return float(10.0 * np.log10(signal_power / noise_power))


def wilson_interval(errors: int, trials: int, z: float = 1.96) -> tuple[float, float]:
    """Wilson score confidence interval for an error probability estimate."""
    if trials <= 0:
        raise ValueError("trials must be positive")
    if errors < 0 or errors > trials:
        raise ValueError("errors must be between 0 and trials")
    phat = errors / trials
    denom = 1 + z**2 / trials
    centre = (phat + z**2 / (2 * trials)) / denom
    margin = z * np.sqrt((phat * (1 - phat) + z**2 / (4 * trials)) / trials) / denom
    return float(max(0.0, centre - margin)), float(min(1.0, centre + margin))


def confidence_interval_normal(value: float, samples: int, confidence: float = 0.95) -> tuple[float, float]:
    """Backward-compatible normal approximation for a probability estimate."""
    if confidence != 0.95:
        raise NotImplementedError("Only 95% confidence is currently implemented.")
    errors = int(round(value * samples))
    return wilson_interval(errors, samples)
