"""Run a minimal UWOC link-budget example."""

from __future__ import annotations

from openuwoc_ai.channels import UnderwaterOpticalChannel
from openuwoc_ai.environments import WaterEnvironment


def main() -> None:
    water = WaterEnvironment.preset("coastal")
    channel = UnderwaterOpticalChannel(environment=water)
    result = channel.link_budget(distance_m=20.0, transmit_power_w=1.0)

    print(f"Environment: {water.name}")
    print(f"Received power: {result.received_power_w:.3e} W")
    print(f"SNR: {result.signal_to_noise_ratio:.3e}")


if __name__ == "__main__":
    main()
