"""Tests for modulation, metrics, and end-to-end simulation."""

from __future__ import annotations

import numpy as np

from openuwoc_ai.evaluation.metrics import bit_error_rate, wilson_interval
from openuwoc_ai.modulation.ook import bits_to_ook, threshold_detect
from openuwoc_ai.simulation.link import LinkSimulationConfig, run_ook_link


def test_ook_mapping_and_detection() -> None:
    bits = np.array([0, 1, 1, 0])
    symbols = bits_to_ook(bits, optical_power_w=2.0)
    assert symbols.tolist() == [0.0, 2.0, 2.0, 0.0]
    assert threshold_detect(symbols, threshold=1.0).tolist() == bits.tolist()


def test_bit_error_rate() -> None:
    assert bit_error_rate(np.array([0, 1, 1]), np.array([0, 0, 1])) == 1 / 3


def test_wilson_interval_bounds() -> None:
    low, high = wilson_interval(errors=1, trials=100)
    assert 0.0 <= low <= high <= 1.0


def test_run_ook_link_returns_valid_result() -> None:
    result = run_ook_link(LinkSimulationConfig(n_bits=512, seed=5))
    assert 0.0 <= result.ber <= 1.0
    assert result.n_bits == 512
    assert result.ci95_low <= result.ber <= result.ci95_high or result.bit_errors == 0
