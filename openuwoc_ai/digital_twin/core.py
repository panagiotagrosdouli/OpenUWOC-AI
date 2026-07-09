"""Digital Twin primitives for adaptive UWOC research workflows.

The twin is deliberately lightweight: it stores simulated and observed channel
states, computes residuals, and exposes hooks for future AI predictors. This
keeps the repository useful for transfer-learning experiments while avoiding
unsupported claims about measured underwater deployments.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, replace

from openuwoc_ai.channel.models import WaterType


PredictionHook = Callable[["DigitalTwinState"], dict[str, float]]


@dataclass(frozen=True)
class DigitalTwinState:
    """State variables describing a UWOC system at one synchronization instant."""

    timestamp_s: float
    water_type: WaterType
    distance_m: float
    tx_power_w: float
    wavelength_nm: float
    absorption_m_inv: float
    scattering_m_inv: float
    pointing_offset_m: float
    turbulence_sigma: float
    thermal_noise_std: float
    snr_linear: float | None = None
    ber: float | None = None

    @property
    def attenuation_m_inv(self) -> float:
        """Beam attenuation coefficient c(lambda)=a(lambda)+b(lambda)."""
        return self.absorption_m_inv + self.scattering_m_inv


@dataclass(frozen=True)
class SimulatedObservedPair:
    """Pair a simulator state with an observed or logged state."""

    simulated: DigitalTwinState
    observed: DigitalTwinState

    def residuals(self) -> dict[str, float]:
        """Return simple observed-minus-simulated residuals for calibration."""
        fields = (
            "distance_m",
            "tx_power_w",
            "wavelength_nm",
            "absorption_m_inv",
            "scattering_m_inv",
            "pointing_offset_m",
            "turbulence_sigma",
            "thermal_noise_std",
        )
        residuals = {
            field: float(getattr(self.observed, field) - getattr(self.simulated, field))
            for field in fields
        }
        if self.simulated.snr_linear is not None and self.observed.snr_linear is not None:
            residuals["snr_linear"] = self.observed.snr_linear - self.simulated.snr_linear
        if self.simulated.ber is not None and self.observed.ber is not None:
            residuals["ber"] = self.observed.ber - self.simulated.ber
        return residuals


@dataclass(frozen=True)
class TransferExperimentSpec:
    """Describe a source-to-target water-domain transfer experiment."""

    source_water_type: WaterType
    target_water_type: WaterType
    feature_fields: tuple[str, ...] = (
        "distance_m",
        "tx_power_w",
        "wavelength_nm",
        "attenuation_m_inv",
        "pointing_offset_m",
        "turbulence_sigma",
        "thermal_noise_std",
    )
    target_fields: tuple[str, ...] = ("ber", "snr_linear")


class UWOCStateSynchronizer:
    """Synchronize simulated and observed UWOC state sequences by nearest time."""

    def __init__(self, max_time_delta_s: float = 0.5):
        if max_time_delta_s < 0:
            raise ValueError("max_time_delta_s must be non-negative")
        self.max_time_delta_s = max_time_delta_s

    def match(
        self,
        simulated: list[DigitalTwinState],
        observed: list[DigitalTwinState],
    ) -> list[SimulatedObservedPair]:
        """Match observed states to nearest simulated states within tolerance."""
        pairs: list[SimulatedObservedPair] = []
        if not simulated or not observed:
            return pairs
        for obs in observed:
            nearest = min(simulated, key=lambda sim: abs(sim.timestamp_s - obs.timestamp_s))
            if abs(nearest.timestamp_s - obs.timestamp_s) <= self.max_time_delta_s:
                pairs.append(SimulatedObservedPair(simulated=nearest, observed=obs))
        return pairs


class UWOCSystemTwin:
    """Stateful Digital Twin container with optional predictive hooks."""

    def __init__(self, initial_state: DigitalTwinState):
        self._state = initial_state
        self._history: list[DigitalTwinState] = [initial_state]
        self._hooks: dict[str, PredictionHook] = {}

    @property
    def state(self) -> DigitalTwinState:
        """Return the current twin state."""
        return self._state

    @property
    def history(self) -> tuple[DigitalTwinState, ...]:
        """Immutable view of state history."""
        return tuple(self._history)

    def update(self, **changes: object) -> DigitalTwinState:
        """Apply a calibrated state update and append it to history."""
        self._state = replace(self._state, **changes)
        self._history.append(self._state)
        return self._state

    def register_prediction_hook(self, name: str, hook: PredictionHook) -> None:
        """Register a named AI/model hook for predicted metrics or actions."""
        if not name:
            raise ValueError("hook name must be non-empty")
        self._hooks[name] = hook

    def predict(self) -> dict[str, dict[str, float]]:
        """Evaluate registered predictive hooks on the current state."""
        return {name: hook(self._state) for name, hook in self._hooks.items()}

    def calibration_summary(self, observed_state: DigitalTwinState) -> dict[str, float]:
        """Return residuals between current simulated state and one observed state."""
        return SimulatedObservedPair(self._state, observed_state).residuals()
