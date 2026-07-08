"""Visualization utilities for UWOC simulations."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from numpy.typing import NDArray


def plot_ber_vs_snr(results: pd.DataFrame, output_path: str | Path) -> Path:
    """Plot BER versus SNR from a sweep result."""
    required = {"snr_db", "ber"}
    if not required.issubset(results.columns):
        raise ValueError(f"results must contain columns: {sorted(required)}")
    return save_ber_curve(results["snr_db"].to_numpy(), results["ber"].to_numpy(), "SNR [dB]", output_path)


def save_ber_curve(x_values: NDArray[np.float64], ber_values: NDArray[np.float64], xlabel: str, output_path: str | Path) -> Path:
    """Save a BER curve with logarithmic y-axis."""
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(6.0, 4.0))
    ax.semilogy(np.asarray(x_values, dtype=float), np.asarray(ber_values, dtype=float), marker="o")
    ax.set_xlabel(xlabel)
    ax.set_ylabel("Bit error rate")
    ax.grid(True, which="both", alpha=0.3)
    fig.tight_layout()
    fig.savefig(output, dpi=200)
    plt.close(fig)
    return output


def save_attenuation_curve(distance_m: NDArray[np.float64], gain: NDArray[np.float64], output_path: str | Path) -> Path:
    """Save Beer-Lambert gain versus distance."""
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    fig, ax = plt.subplots(figsize=(6.0, 4.0))
    ax.plot(distance_m, gain)
    ax.set_xlabel("Distance [m]")
    ax.set_ylabel("Optical channel gain")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(output, dpi=200)
    plt.close(fig)
    return output


def save_received_waveform(samples: NDArray[np.float64], output_path: str | Path, max_points: int = 300) -> Path:
    """Save received sample waveform for debugging and demos."""
    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    y = np.asarray(samples, dtype=float)[:max_points]
    fig, ax = plt.subplots(figsize=(7.0, 3.0))
    ax.plot(np.arange(y.size), y)
    ax.set_xlabel("Sample index")
    ax.set_ylabel("Received signal")
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(output, dpi=200)
    plt.close(fig)
    return output
