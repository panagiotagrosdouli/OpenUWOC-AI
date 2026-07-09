from __future__ import annotations

from pathlib import Path

from openuwoc_ai.channel.models import WATER_PROFILES, WaterType
from openuwoc_ai.datasets.synthetic import (
    DatasetGenerationConfig,
    dataset_metadata,
    generate_channel_dataset,
    write_dataset_csv,
    write_dataset_metadata,
)
from openuwoc_ai.digital_twin.core import (
    DigitalTwinState,
    TransferExperimentSpec,
    UWOCStateSynchronizer,
    UWOCSystemTwin,
)


def _state(timestamp_s: float, water_type: WaterType = WaterType.COASTAL) -> DigitalTwinState:
    profile = WATER_PROFILES[water_type]
    return DigitalTwinState(
        timestamp_s=timestamp_s,
        water_type=water_type,
        distance_m=10.0,
        tx_power_w=1.0,
        wavelength_nm=520.0,
        absorption_m_inv=profile.absorption_m_inv,
        scattering_m_inv=profile.scattering_m_inv,
        pointing_offset_m=0.01,
        turbulence_sigma=0.05,
        thermal_noise_std=0.02,
        snr_linear=15.0,
        ber=0.01,
    )


def test_synthetic_dataset_is_deterministic_and_schema_complete() -> None:
    cfg = DatasetGenerationConfig(n_samples=3, n_bits=128, seed=11)
    first = generate_channel_dataset(cfg)
    second = generate_channel_dataset(cfg)
    assert first == second
    assert len(first) == 3
    required = {"water_type", "distance_m", "tx_power_w", "ber", "snr_linear", "ci95_low"}
    assert required.issubset(first[0])


def test_dataset_writers_create_csv_and_metadata(tmp_path: Path) -> None:
    cfg = DatasetGenerationConfig(n_samples=2, n_bits=64, seed=5)
    rows = generate_channel_dataset(cfg)
    csv_path = tmp_path / "dataset.csv"
    metadata_path = tmp_path / "metadata.json"
    write_dataset_csv(rows, csv_path)
    write_dataset_metadata(dataset_metadata(cfg, tuple(rows[0].keys())), metadata_path)
    assert csv_path.read_text().startswith("sample_id,water_type")
    assert "simulation" in metadata_path.read_text()


def test_digital_twin_matches_states_and_computes_residuals() -> None:
    synchronizer = UWOCStateSynchronizer(max_time_delta_s=0.2)
    pairs = synchronizer.match([_state(0.0), _state(1.0)], [_state(1.1)])
    assert len(pairs) == 1
    residuals = pairs[0].residuals()
    assert residuals["distance_m"] == 0.0


def test_digital_twin_prediction_hook_and_transfer_spec() -> None:
    twin = UWOCSystemTwin(_state(0.0))
    twin.register_prediction_hook("risk", lambda state: {"link_margin_proxy": state.snr_linear or 0.0})
    prediction = twin.predict()
    assert prediction["risk"]["link_margin_proxy"] == 15.0
    updated = twin.update(distance_m=12.0)
    assert updated.distance_m == 12.0
    spec = TransferExperimentSpec(WaterType.CLEAR_OCEAN, WaterType.TURBID_HARBOR)
    assert "attenuation_m_inv" in spec.feature_fields
