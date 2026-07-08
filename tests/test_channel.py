"""Tests for UWOC channel behavior."""

from __future__ import annotations

import numpy as np
import pytest

from openuwoc_ai.channel.models import (
    ChannelConfig,
    UnderwaterOpticalChannel,
    WaterType,
    beer_lambert_gain,
    pointing_error_gain,
    thermal_noise,
)


def test_beer_lambert_gain_decreases_with_distance() -> None:
    near = beer_lambert_gain(5.0, 0.2)
    far = beer_lambert_gain(30.0, 0.2)
    assert near > far


def test_beer_lambert_rejects_negative_values() -> None:
    with pytest.raises(ValueError):
        beer_lambert_gain(-1.0, 0.2)
    with pytest.raises(ValueError):
        beer_lambert_gain(1.0, -0.2)


def test_pointing_error_gain_is_bounded() -> None:
    assert pointing_error_gain(0.0, 0.05) == pytest.approx(1.0)
    assert 0.0 < pointing_error_gain(0.01, 0.05) < 1.0


def test_noise_generation_shape() -> None:
    rng = np.random.default_rng(1)
    noise = thermal_noise(32, 0.1, rng)
    assert noise.shape == (32,)


def test_channel_propagation_shape() -> None:
    channel = UnderwaterOpticalChannel(ChannelConfig(water_type=WaterType.COASTAL, seed=3))
    rx = channel.propagate(np.ones(128))
    assert rx.shape == (128,)
    assert channel.deterministic_gain > 0
