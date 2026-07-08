"""Physics-inspired underwater optical wireless channel models.

The implemented models are intentionally conservative: they provide reproducible
simulation baselines, not validated experimental claims. Coefficients should be
replaced with measured site-specific values before drawing scientific conclusions.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

import numpy as np
from numpy.typing import NDArray


class WaterType(str, Enum):
    """Canonical water presets used for simulation-only baselines."""

    CLEAR_OCEAN = "clear_ocean"
    COASTAL = "coastal"
    TURBID_HARBOR = "turbid_harbor"


@dataclass(frozen=True)
class WaterProfile:
    """Absorption and scattering profile at a nominal optical wavelength."""

    water_type: WaterType
    absorption_m_inv: float
    scattering_m_inv: float
    wavelength_nm: float = 520.0
    description: str = "simulation preset; replace with measured data for claims"

    @property
    def attenuation_m_inv(self) -> float:
        """Beam attenuation c(lambda)=a(lambda)+b(lambda)."""
        return self.absorption_m_inv + self.scattering_m_inv


WATER_PROFILES: dict[WaterType, WaterProfile] = {
    WaterType.CLEAR_OCEAN: WaterProfile(WaterType.CLEAR_OCEAN, 0.04, 0.01),
    WaterType.COASTAL: WaterProfile(WaterType.COASTAL, 0.12, 0.18),
    WaterType.TURBID_HARBOR: WaterProfile(WaterType.TURBID_HARBOR, 0.35, 0.75),
}


def beer_lambert_gain(distance_m: float | NDArray[np.float64], attenuation_m_inv: float) -> float | NDArray[np.float64]:
    """Return Beer-Lambert channel gain exp(-c d)."""
    distance = np.asarray(distance_m, dtype=float)
    if np.any(distance < 0) or attenuation_m_inv < 0:
        raise ValueError("distance and attenuation must be non-negative")
    gain = np.exp(-attenuation_m_inv * distance)
    return float(gain) if gain.ndim == 0 else gain


def pointing_error_gain(radial_offset_m: float, beam_waist_m: float) -> float:
    """Gaussian pointing-loss approximation for transmitter-receiver misalignment."""
    if beam_waist_m <= 0:
        raise ValueError("beam_waist_m must be positive")
    if radial_offset_m < 0:
        raise ValueError("radial_offset_m must be non-negative")
    return float(np.exp(-2.0 * (radial_offset_m / beam_waist_m) ** 2))


def lognormal_turbulence_gain(size: int, sigma: float, rng: np.random.Generator) -> NDArray[np.float64]:
    """Generate unit-mean lognormal irradiance fluctuations for weak turbulence."""
    if sigma < 0:
        raise ValueError("sigma must be non-negative")
    if sigma == 0:
        return np.ones(size)
    return rng.lognormal(mean=-(sigma**2) / 2.0, sigma=sigma, size=size)


def thermal_noise(size: int, std: float, rng: np.random.Generator) -> NDArray[np.float64]:
    """Generate additive thermal receiver noise."""
    if std < 0:
        raise ValueError("std must be non-negative")
    return rng.normal(0.0, std, size=size)


def shot_noise(signal_power: NDArray[np.float64], scale: float, rng: np.random.Generator) -> NDArray[np.float64]:
    """Gaussian shot-noise approximation with variance proportional to power."""
    if scale < 0:
        raise ValueError("scale must be non-negative")
    std = np.sqrt(np.maximum(signal_power, 0.0) * scale)
    return rng.normal(0.0, std)


@dataclass(frozen=True)
class ChannelConfig:
    """Configuration for an IM/DD UWOC link."""

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


class UnderwaterOpticalChannel:
    """End-to-end scalar UWOC channel for baseline link simulations."""

    def __init__(self, config: ChannelConfig):
        self.config = config
        self.profile = WATER_PROFILES[config.water_type]
        self.rng = np.random.default_rng(config.seed)

    @property
    def deterministic_gain(self) -> float:
        """Path gain including attenuation and pointing error."""
        attenuation = beer_lambert_gain(self.config.distance_m, self.profile.attenuation_m_inv)
        pointing = pointing_error_gain(self.config.pointing_offset_m, self.config.beam_waist_m)
        return float(attenuation * pointing)

    def propagate(self, optical_power_w: NDArray[np.float64]) -> NDArray[np.float64]:
        """Propagate optical power samples through attenuation, turbulence, and noise."""
        optical_power_w = np.asarray(optical_power_w, dtype=float)
        if np.any(optical_power_w < 0):
            raise ValueError("optical power samples must be non-negative")
        turbulence = lognormal_turbulence_gain(optical_power_w.size, self.config.turbulence_sigma, self.rng)
        received = optical_power_w * self.deterministic_gain * turbulence
        received = received + self.config.ambient_light_w
        received = received + shot_noise(received, self.config.shot_noise_scale, self.rng)
        received = received + thermal_noise(received.size, self.config.thermal_noise_std, self.rng)
        return received.astype(float)

    def snr_linear(self) -> float:
        """Approximate electrical SNR for the high OOK symbol level."""
        signal = self.config.tx_power_w * self.deterministic_gain
        variance = self.config.thermal_noise_std**2 + max(signal, 0.0) * self.config.shot_noise_scale
        if variance <= 0:
            return float("inf")
        return float(signal**2 / variance)
