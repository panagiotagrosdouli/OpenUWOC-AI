"""Generate a simple code-created UWOC demo animation.

The animation is intentionally illustrative. It visualizes attenuation, received
waveform, BER estimate, confidence, and a rule-based adaptive decision. It does
not contain measured experimental results.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np

from openuwoc_ai.channel.models import WaterType
from openuwoc_ai.simulation.link import LinkSimulationConfig, run_ook_link


def main() -> None:
    assets = Path("assets")
    videos = Path("results/videos")
    assets.mkdir(parents=True, exist_ok=True)
    videos.mkdir(parents=True, exist_ok=True)

    distances = np.linspace(1.0, 20.0, 40)
    fig, axes = plt.subplots(2, 1, figsize=(7, 6))

    def update(frame: int):
        for ax in axes:
            ax.clear()
        distance = float(distances[frame])
        water = WaterType.COASTAL if frame < len(distances) // 2 else WaterType.TURBID_HARBOR
        config = LinkSimulationConfig(n_bits=3000, water_type=water, distance_m=distance, seed=frame + 1)
        result = run_ook_link(config)
        confidence = max(0.0, 1.0 - result.ber)
        decision = "OOK" if result.ber < 0.1 else "reduce rate / increase power"

        axes[0].plot([0, distance], [0, 0], linewidth=3)
        axes[0].scatter([0, distance], [0, 0], s=[160, 160])
        axes[0].set_xlim(0, 21)
        axes[0].set_ylim(-1, 1)
        axes[0].set_title(f"UWOC link: {water.value}, distance={distance:.1f} m")
        axes[0].text(0, 0.25, "Tx")
        axes[0].text(distance, 0.25, "Rx")
        axes[0].text(1, -0.55, f"gain={result.deterministic_gain:.2e}")

        t = np.arange(80)
        waveform = result.deterministic_gain * (np.sin(0.3 * t) > 0).astype(float)
        waveform += np.random.default_rng(frame).normal(0, config.thermal_noise_std, size=t.size)
        axes[1].plot(t, waveform)
        axes[1].set_title(
            f"BER={result.ber:.3f} | AI confidence proxy={confidence:.2f} | policy={decision}"
        )
        axes[1].set_xlabel("sample")
        axes[1].set_ylabel("received signal")
        axes[1].grid(True, alpha=0.3)
        fig.tight_layout()

    ani = animation.FuncAnimation(fig, update, frames=len(distances), interval=120)
    ani.save(assets / "demo.gif", writer="pillow", fps=8)
    try:
        ani.save(videos / "demo.mp4", writer="ffmpeg", fps=8)
    except Exception:
        pass
    plt.close(fig)


if __name__ == "__main__":
    main()
