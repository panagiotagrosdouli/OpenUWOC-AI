# Baseline UWOC Channel Validation

This workflow supports Milestone 1: validate the first publication-quality baseline UWOC channel model.

## Current model

The repository models intensity modulation / direct detection with deterministic Beer-Lambert attenuation:

```math
h(d, \lambda) = \exp[-(a(\lambda) + b(\lambda))d] h_p h_t
```

where `a` is absorption, `b` is scattering, `h_p` is pointing loss, and `h_t` is a turbulence proxy.

## Command

```bash
python scripts/validate_baseline_channel.py --output results/baseline_channel_sweep.csv
```

The script sweeps distance for all repository water presets and writes:

- water type;
- nominal wavelength;
- absorption, scattering, and attenuation coefficients;
- Beer-Lambert gain;
- deterministic gain;
- simulated SNR;
- simulated BER and bit errors.

## Publication-quality discipline

The produced CSV is a reproducible simulation artifact. It can support plots and sanity-check tables, but it is not a measured UWOC benchmark.

Before physical claims are made, the following evidence is required:

1. measured absorption/scattering values for the actual water environment;
2. receiver field-of-view and beam-divergence assumptions;
3. calibrated pointing-error model;
4. measured or justified noise parameters;
5. reproduction commands and committed result artifacts.

## Status

Implemented:

- deterministic channel attenuation sweep;
- wavelength, absorption, scattering, attenuation, SNR, and BER outputs;
- publication-style CSV artifact generation.

Still planned:

- measured coefficient calibration;
- distance-dependent figures committed from script output;
- comparison against external experimental datasets;
- multipath and turbulence validation beyond the current scaffold.
