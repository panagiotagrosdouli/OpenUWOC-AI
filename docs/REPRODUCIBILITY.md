# Reproducibility

## Deterministic seeds

All committed experiment configs include an explicit `seed`. Simulation functions use NumPy random generators initialized from that seed.

## Running an experiment

```bash
python scripts/run_experiment.py configs/coastal_ook_baseline.yaml --output results/coastal_ook_baseline.csv
```

## Result storage

Generated outputs should be written under `results/`. Do not commit large generated files unless they are lightweight examples required for documentation.

## Claims policy

A result is reportable only when the code, config, seed, data source, and evaluation metric are available. Simulation-only results must be labeled as simulation-only.
