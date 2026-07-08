"""Metrics for communication-system evaluation."""

from __future__ import annotations

from math import sqrt

import numpy as np
from numpy.typing import NDArray


def bit_error_rate(reference_bits: NDArray[np.integer], estimated_bits: NDArray[np.integer]) -> float:
    """Compute bit error rate between two binary sequences."""
    reference = np.asarray(reference_bits)
    estimated = np.asarray(estimated_bits)
    if reference.shape != estimated.shape:
        raise ValueError("reference_bits and estimated_bits must have the same shape.")
    if reference.size == 0:
        raise ValueError("bit arrays must be non-empty.")
    return float(np.mean(reference != estimated))


def symbol_error_rate(reference: NDArray[np.integer], estimated: NDArray[np.integer]) -> float:
    """Compute symbol error rate."""
    ref = np.asarray(reference)
    est = np.asarray(estimated)
    if ref.shape != est.shape:
        raise ValueError("reference and estimated arrays must have the same shape.")
    if ref.size == 0:
        raise ValueError("symbol arrays must be non-empty.")
    return float(np.mean(ref != est))


def confidence_interval_normal(value: float, samples: int, confidence: float = 0.95) -> tuple[float, float]:
    """Approximate a binomial confidence interval for BER/SER.

    The implementation uses a normal approximation and is intended for quick
    simulation reporting. For small error counts, exact or Wilson intervals are
    preferable and planned.
    """
    if samples <= 0:
        raise ValueError("samples must be positive.")
    if not 0.0 <= value <= 1.0:
        raise ValueError("value must be a probability.")
    if confidence != 0.95:
        raise NotImplementedError("Only 95% confidence is currently implemented.")
    radius = 1.96 * sqrt(value * (1.0 - value) / samples)
    return max(0.0, value - radius), min(1.0, value + radius)
