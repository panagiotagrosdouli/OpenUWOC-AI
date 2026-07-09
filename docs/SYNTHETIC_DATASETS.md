# AI-Ready Synthetic Dataset Generation

OpenUWOC-AI now includes a deterministic synthetic dataset generator for supervised learning, generative modeling, and benchmark scaffolding.

## Command

```bash
python scripts/generate_synthetic_dataset.py \
  configs/synthetic_dataset_baseline.yaml \
  --csv results/datasets/synthetic_channel_states.csv \
  --metadata results/datasets/synthetic_channel_states.metadata.json
```

## Generated fields

Each row contains sampled channel inputs and simulator-derived labels:

- `water_type`
- `distance_m`
- `tx_power_w`
- `wavelength_nm`
- `absorption_m_inv`
- `scattering_m_inv`
- `thermal_noise_std`
- `pointing_offset_m`
- `turbulence_sigma`
- `deterministic_gain`
- `snr_linear`
- `ber`
- `bit_errors`
- Wilson confidence interval bounds for BER

## Reproducibility policy

The generator uses deterministic seeds and writes a metadata JSON file alongside the CSV.
The metadata documents the generator, seed, schema, and assumptions.

## Scientific interpretation

The generated rows are simulation outputs. They are suitable for:

- AI receiver prototyping;
- BER/SNR prediction baselines;
- transfer-learning experiments between water presets;
- smoke tests for downstream training pipelines.

They are not suitable for claiming real-water performance until replaced or calibrated with measured tank, pool, or sea-trial data.
