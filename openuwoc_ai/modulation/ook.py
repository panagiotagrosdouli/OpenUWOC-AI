"""On-off keying modulation and threshold detection baselines."""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray


def bits_to_ook(bits: NDArray[np.integer], optical_power_w: float = 1.0) -> NDArray[np.float64]:
    """Map binary bits to OOK optical power levels {0, P_tx}."""
    bits = np.asarray(bits, dtype=int)
    if optical_power_w < 0:
        raise ValueError("optical_power_w must be non-negative")
    if not np.all((bits == 0) | (bits == 1)):
        raise ValueError("OOK modulation expects binary bits")
    return bits.astype(float) * optical_power_w


def threshold_detect(samples: NDArray[np.float64], threshold: float | None = None) -> NDArray[np.int_]:
    """Detect OOK symbols with a fixed threshold."""
    samples = np.asarray(samples, dtype=float)
    if samples.size == 0:
        raise ValueError("samples must not be empty")
    if threshold is None:
        threshold = 0.5 * (float(np.min(samples)) + float(np.max(samples)))
    return (samples >= threshold).astype(int)


def random_bits(n_bits: int, seed: int = 7) -> NDArray[np.int_]:
    """Generate deterministic random bits for reproducible experiments."""
    if n_bits <= 0:
        raise ValueError("n_bits must be positive")
    rng = np.random.default_rng(seed)
    return rng.integers(0, 2, size=n_bits, dtype=int)


# Backward-compatible aliases for earlier repository examples.
modulate_ook = bits_to_ook
demodulate_ook = threshold_detect
