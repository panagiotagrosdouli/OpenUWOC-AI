# Reproducibility Report

## Reproducibility Position

This repository is simulation-first. Any numeric output produced by the code should be interpreted as a result of the documented simulator configuration, random seed, package versions, and hardware/software environment. It should not be presented as physical UWOC performance unless validated against calibrated measurements.

## Required Metadata for Experiments

Every experiment should store:

- configuration file path and full resolved parameters;
- deterministic random seed;
- package versions;
- execution timestamp;
- command-line invocation;
- output metrics;
- generated plots;
- logs and warnings;
- explicit status: `Implemented`, `Prototype`, `Pending`, or `Failed`.

## Baseline Policy

Classical communication baselines should be implemented and reported before claiming AI improvement. If a baseline is not yet implemented, benchmark tables must mark it as `Pending` instead of inventing values.

## Dataset Policy

Synthetic data may be generated for demonstrations only when clearly labelled as synthetic. Real datasets must include source, sensor/channel description, calibration details, license, and preprocessing steps.

## Artifact Policy

Generated media should be reproducible from code and stored under the documented paths:

- `assets/`
- `docs/assets/`
- `results/videos/`
- `results/experiments/`

Large generated files should be published through releases or external archival storage rather than committed directly to the repository.

## Current Status

- Container support: implemented in this branch.
- CI checks: implemented in this branch.
- Real-world validation: pending.
- Full classical benchmark suite: pending.
- Hardware-in-the-loop experiments: pending.
