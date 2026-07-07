"""Underwater environment models for UWOC simulations."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class WaterEnvironment:
    """Physical parameters of an underwater optical propagation environment.

    Parameters are intentionally simple in the initial release. They can later be
    extended with wavelength-dependent absorption, scattering phase functions,
    turbulence statistics, salinity, temperature, and depth-dependent profiles.
    """

    name: str
    absorption_coefficient: float
    scattering_coefficient: float
    turbulence_strength: float = 0.0
    background_noise_power_w: float = 1e-9

    @property
    def attenuation_coefficient(self) -> float:
        """Return total attenuation coefficient c = a + b in 1/m."""
        return self.absorption_coefficient + self.scattering_coefficient

    @classmethod
    def preset(cls, name: str) -> "WaterEnvironment":
        """Create a commonly used underwater environment preset.

        The coefficients are baseline research placeholders intended for early
        simulation and software validation. Future versions should document and
        validate each preset against optical oceanography references.
        """
        presets = {
            "clear_ocean": cls(
                name="clear_ocean",
                absorption_coefficient=0.114,
                scattering_coefficient=0.037,
                turbulence_strength=0.01,
            ),
            "coastal": cls(
                name="coastal",
                absorption_coefficient=0.179,
                scattering_coefficient=0.219,
                turbulence_strength=0.03,
            ),
            "harbor": cls(
                name="harbor",
                absorption_coefficient=0.295,
                scattering_coefficient=1.875,
                turbulence_strength=0.08,
            ),
            "lake": cls(
                name="lake",
                absorption_coefficient=0.200,
                scattering_coefficient=0.500,
                turbulence_strength=0.04,
            ),
            "river": cls(
                name="river",
                absorption_coefficient=0.250,
                scattering_coefficient=0.900,
                turbulence_strength=0.06,
            ),
        }

        key = name.lower().strip()
        if key not in presets:
            valid = ", ".join(sorted(presets))
            raise ValueError(f"Unknown environment preset '{name}'. Valid presets: {valid}.")
        return presets[key]
