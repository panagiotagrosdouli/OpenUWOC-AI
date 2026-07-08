"""Publication-oriented plotting utilities."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


def plot_ber_vs_snr(results: pd.DataFrame, output_path: str | Path) -> Path:
    """Plot BER versus SNR from a sweep result."""
    required = {"snr_db", "ber"}
    if not required.issubset(results.columns):
        raise ValueError(f"results must contain columns: {sorted(required)}")

    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.semilogy(results["snr_db"], results["ber"], marker="o")
    ax.set_xlabel("SNR (dB)")
    ax.set_ylabel("Bit Error Rate")
    ax.set_title("Simulation-only OOK UWOC BER Sweep")
    ax.grid(True, which="both", linestyle="--", alpha=0.4)
    fig.tight_layout()
    fig.savefig(path, dpi=200)
    plt.close(fig)
    return path
