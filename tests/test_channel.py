"""Tests for baseline UWOC channel behavior."""

from __future__ import annotations

import pytest

from openuwoc_ai.channels import UnderwaterOpticalChannel
from openuwoc_ai.environments import WaterEnvironment


def test_environment_preset_has_positive_attenuation() -> None:
    water = WaterEnvironment.preset("coastal")

    assert water.attenuation_coefficient > 0


def test_received_power_decreases_with_distance() -> None:
    water = WaterEnvironment.preset("clear_ocean")
    channel = UnderwaterOpticalChannel(environment=water)

    near = channel.received_power(distance_m=5.0, transmit_power_w=1.0)
    far = channel.received_power(distance_m=30.0, transmit_power_w=1.0)

    assert near > far


def test_link_budget_returns_positive_snr() -> None:
    water = WaterEnvironment.preset("coastal")
    channel = UnderwaterOpticalChannel(environment=water)

    result = channel.link_budget(distance_m=10.0, transmit_power_w=0.5)

    assert result.received_power_w >= 0
    assert result.signal_to_noise_ratio >= 0


def test_unknown_environment_raises_error() -> None:
    with pytest.raises(ValueError):
        WaterEnvironment.preset("unknown")
