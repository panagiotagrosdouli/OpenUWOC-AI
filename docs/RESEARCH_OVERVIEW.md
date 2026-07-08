# Research Overview

OpenUWOC-AI is organized around AI-assisted underwater optical wireless communication (UWOC) for marine robotic and autonomous underwater systems.

## Motivation

UWOC links can provide high-rate short-range communication, but reliability degrades under absorption, scattering, water turbidity, turbulence, pointing error, ambient light, shot noise, and thermal noise. Classical receivers remain essential baselines, while AI methods may help when the channel is nonlinear, partially observed, and time-varying.

## Implemented

- Beer-Lambert attenuation with absorption/scattering presets.
- Gaussian pointing-error loss scaffold.
- Lognormal turbulence scaffold.
- Thermal and shot-noise simulation utilities.
- OOK modulation and threshold detection.
- End-to-end deterministic-seed OOK link simulation.
- BER, SER, SNR, and Wilson confidence intervals.
- YAML experiment runner.
- Plotting utilities.
- Prototype neural equalizer and BER predictor classes.

## Prototype

- Neural equalization using small PyTorch MLPs.
- BER prediction from simulated link features.
- Demo animation with confidence and adaptive-decision proxies.

## Planned

- Measured-water calibration and real tank/sea datasets.
- Validated turbulence and multipath impulse-response models.
- BPSK/QPSK/M-QAM/OFDM implementations.
- Matched-filter, linear-equalizer, and oracle-estimator baselines.
- Adaptive modulation and coding policies.
- Marine-robotics integration experiments.

## Scientific limitations

The repository currently provides simulation software. It does not claim state-of-the-art performance, experimental validation, or superiority of AI receivers. Any future claim must be backed by code, reproducible configuration, datasets, and statistically reported metrics.
