"""Train a baseline channel predictor on synthetic UWOC data."""

from __future__ import annotations

from openuwoc_ai.ai import LinearChannelPredictor
from openuwoc_ai.datasets import DatasetGenerationConfig, generate_link_budget_dataset


def main() -> None:
    dataset = generate_link_budget_dataset(
        DatasetGenerationConfig(environment="coastal", num_samples=1000, seed=42)
    )

    feature_columns = [
        "distance_m",
        "transmit_power_w",
        "attenuation_coefficient",
        "beam_divergence_rad",
        "receiver_aperture_m",
    ]
    target_column = "received_power_w"

    train_data, test_data = LinearChannelPredictor.train_test_split(dataset, seed=42)
    predictor = LinearChannelPredictor().fit(train_data, feature_columns, target_column)
    metrics = predictor.evaluate(test_data, target_column)

    print("Baseline channel-prediction results")
    print(f"MAE:  {metrics.mean_absolute_error:.3e}")
    print(f"RMSE: {metrics.root_mean_squared_error:.3e}")
    print(f"R2:   {metrics.r2_score:.4f}")


if __name__ == "__main__":
    main()
