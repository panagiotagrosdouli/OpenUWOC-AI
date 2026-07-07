"""Generate a synthetic UWOC dataset for AI experiments."""

from __future__ import annotations

from openuwoc_ai.datasets import DatasetGenerationConfig, export_dataset, generate_link_budget_dataset


def main() -> None:
    config = DatasetGenerationConfig(
        environment="coastal",
        num_samples=500,
        min_distance_m=1.0,
        max_distance_m=50.0,
        min_transmit_power_w=0.05,
        max_transmit_power_w=2.0,
        seed=7,
    )
    dataset = generate_link_budget_dataset(config)
    output_path = export_dataset(dataset, "experiments/outputs/coastal_link_budget.csv")

    print(dataset.head())
    print(f"Saved dataset to: {output_path}")


if __name__ == "__main__":
    main()
