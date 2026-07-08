"""On-off keying modulation and threshold detection."""

from __future__ import annotations

import numpy as np
from numpy.typing import NDArray


def modulate_ook(bits: NDArray[np.integer], amplitude: float = 1.0) -> NDArray[np.float64]:
    """Map bits to OOK optical intensity symbols.

    Bit 0 maps to 0 and bit 1 maps to ``amplitude``.
    """
    if amplitude <= 0:
        raise ValueError("amplitude must be positive.")
    values = np.asarray(bits)
    if not np.all((values == 0) | (values == 1)):
        raise ValueError("bits must contain only 0 and 1.")
    return values.astype(float) * amplitude


def demodulate_ook(samples: NDArray[np.float64], threshold: float = 0.5) -> NDArray[np.int_]:
    """Demodulate OOK samples with a fixed threshold detector."""
    return (np.asarray(samples) >= threshold).astype(int)
