# Experiments

## Included configs

- `configs/coastal_ook_baseline.yaml`: baseline coastal-water OOK simulation.
- `configs/turbid_pointing_stress.yaml`: turbidity, turbulence, and misalignment stress case.

## Running

```bash
python scripts/run_experiment.py configs/coastal_ook_baseline.yaml --output results/coastal_ook_baseline.csv
```

## Planned experiment suite

- Clear water.
- Coastal water.
- Turbid harbor water.
- Short-range link.
- Long-range link.
- High ambient light.
- Pointing error sweep.
- Turbulence noise sweep.
- SNR/noise sweep.
- AI equalizer versus threshold detector.

Every experiment must include a YAML config, deterministic seed, and output under `results/`.
