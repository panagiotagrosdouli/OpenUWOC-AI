"""Pointing-error scaffolds for UWOC links."""

from __future__ import annotations

from dataclasses import dataclass
from math import exp


@dataclass(frozen=True)
class PointingErrorConfig:
    """Gaussian beam pointing-loss approximation.

    Attributes:
        jitter_std_rad: Angular pointing jitter standard deviation in radians.
        beam_divergence_rad: Beam divergence angle in radians.
    """

    jitter_std_rad: float
    beam_divergence_rad: float


def pointing_loss(misalignment_rad: float, config: PointingErrorConfig) -> float:
    """Return a bounded pointing-loss factor in [0, 1].

    The model is a simple Gaussian approximation and should be treated as a
    simulation scaffold until calibrated against optical alignment data.
    """
    if config.beam_divergence_rad <= 0:
        raise ValueError("beam_divergence_rad must be positive.")
    if config.jitter_std_rad < 0:
        raise ValueError("jitter_std_rad must be non-negative.")
    normalized = misalignment_rad / config.beam_divergence_rad
    return float(exp(-(normalized**2)))
