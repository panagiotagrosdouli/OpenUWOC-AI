"""Physics-inspired UWOC channel models.

The implemented model is intentionally conservative: it provides deterministic
Beer-Lambert attenuation and documented scaffolds for turbulence, pointing
error, and multipath. It does not claim experimental validation.
"""

from __future__ import annotations

from dataclasses import dataclass
from math import exp


@dataclass(frozen=True)
class WaterProfile:
    """Optical properties of an underwater environment.

    Attributes:
        name: Human-readable water type.
        absorption_m_inv: Absorption coefficient a in 1/m.
        scattering_m_inv: Scattering coefficient b in 1/m.
        background_noise_w: Background optical noise power in watts.
    """

    name: str
    absorption_m_inv: float
    scattering_m_inv: float
    background_noise_w: float = 1e-9

    @property
    def attenuation_m_inv(self) -> float:
        """Return c = a + b in 1/m."""
        return self.absorption_m_inv + self.scattering_m_inv

    @classmethod
    def preset(cls, name: str) -> "WaterProfile":
        """Return a baseline water profile.

        These values are software placeholders for reproducible simulation.
        They must be replaced or calibrated before making physical claims.
        """
        profiles = {
            "clear": cls("clear", 0.114, 0.037),
            "coastal": cls("coastal", 0.179, 0.219),
            "harbor": cls("harbor", 0.295, 1.875),
            "lake": cls("lake", 0.200, 0.500),
            "river": cls("river", 0.250, 0.900),
        }
        key = name.lower().strip()
        if key not in profiles:
            raise ValueError(f"Unknown water profile '{name}'. Options: {sorted(profiles)}")
        return profiles[key]


@dataclass(frozen=True)
class ChannelState:
    """State variables for one UWOC link realization."""

    distance_m: float
    water: WaterProfile
    pointing_loss: float = 1.0
    turbulence_gain: float = 1.0

    @property
    def deterministic_gain(self) -> float:
        """Return Beer-Lambert gain multiplied by pointing and turbulence gains."""
        return (
            beer_lambert_gain(self.water.attenuation_m_inv, self.distance_m)
            * self.pointing_loss
            * self.turbulence_gain
        )


def beer_lambert_gain(attenuation_m_inv: float, distance_m: float) -> float:
    """Compute Beer-Lambert optical channel gain exp(-c d).

    Args:
        attenuation_m_inv: Total attenuation coefficient c = a + b in 1/m.
        distance_m: Link distance in meters.

    Returns:
        Dimensionless optical channel gain.
    """
    if attenuation_m_inv < 0:
        raise ValueError("attenuation_m_inv must be non-negative.")
    if distance_m < 0:
        raise ValueError("distance_m must be non-negative.")
    return exp(-attenuation_m_inv * distance_m)
