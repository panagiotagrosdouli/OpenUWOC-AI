"""Baseline underwater optical wireless channel models."""

from __future__ import annotations

from dataclasses import dataclass
from math import exp, pi

from openuwoc_ai.environments import WaterEnvironment


@dataclass(frozen=True)
class LinkBudgetResult:
    """Output of a simple UWOC link-budget computation."""

    distance_m: float
    transmit_power_w: float
    received_power_w: float
    attenuation_loss: float
    geometric_loss: float
    signal_to_noise_ratio: float


@dataclass(frozen=True)
class UnderwaterOpticalChannel:
    """Simple line-of-sight UWOC channel.

    This initial model combines Beer-Lambert attenuation with a first-order
    geometric spreading term. It is deliberately compact so that future modules
    can add scattering, turbulence, pointing errors, mobility, and receiver
    field-of-view constraints without changing the public API.
    """

    environment: WaterEnvironment
    beam_divergence_rad: float = 1e-3
    receiver_aperture_m: float = 0.05

    def attenuation_loss(self, distance_m: float) -> float:
        """Return Beer-Lambert channel attenuation over distance."""
        self._validate_distance(distance_m)
        return exp(-self.environment.attenuation_coefficient * distance_m)

    def geometric_loss(self, distance_m: float) -> float:
        """Return receiver collection ratio due to beam spreading."""
        self._validate_distance(distance_m)
        beam_radius_m = max(self.beam_divergence_rad * distance_m, self.receiver_aperture_m / 2)
        receiver_area_m2 = pi * (self.receiver_aperture_m / 2) ** 2
        beam_area_m2 = pi * beam_radius_m**2
        return min(receiver_area_m2 / beam_area_m2, 1.0)

    def received_power(self, distance_m: float, transmit_power_w: float) -> float:
        """Compute received optical power in watts."""
        self._validate_power(transmit_power_w)
        return transmit_power_w * self.attenuation_loss(distance_m) * self.geometric_loss(distance_m)

    def link_budget(self, distance_m: float, transmit_power_w: float) -> LinkBudgetResult:
        """Compute a baseline UWOC link budget."""
        attenuation = self.attenuation_loss(distance_m)
        geometry = self.geometric_loss(distance_m)
        received = self.received_power(distance_m, transmit_power_w)
        snr = received / self.environment.background_noise_power_w
        return LinkBudgetResult(
            distance_m=distance_m,
            transmit_power_w=transmit_power_w,
            received_power_w=received,
            attenuation_loss=attenuation,
            geometric_loss=geometry,
            signal_to_noise_ratio=snr,
        )

    @staticmethod
    def _validate_distance(distance_m: float) -> None:
        if distance_m <= 0:
            raise ValueError("distance_m must be positive.")

    @staticmethod
    def _validate_power(power_w: float) -> None:
        if power_w < 0:
            raise ValueError("transmit_power_w must be non-negative.")
