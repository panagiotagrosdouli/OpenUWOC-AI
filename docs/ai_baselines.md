# AI Baselines

OpenUWOC-AI starts with simple, transparent AI baselines before introducing deep learning models.

## Channel Prediction

The first implemented model is `LinearChannelPredictor`, an ordinary least-squares regressor for predicting UWOC link metrics from synthetic simulator data.

## Why Start With a Linear Baseline?

A simple baseline is scientifically useful because it provides:

- a reproducible point of comparison
- interpretable behavior
- fast execution in CI
- a benchmark that future neural models should outperform

## Current Prediction Target

The initial example predicts:

```text
received_power_w
```

from features such as:

```text
distance_m
transmit_power_w
attenuation_coefficient
beam_divergence_rad
receiver_aperture_m
```

## Usage

```bash
python examples/train_channel_predictor.py
```

## Future Extensions

- neural channel predictors
- transformer-based sequence predictors
- generative channel models
- reinforcement learning for link adaptation
- uncertainty-aware prediction
- transfer learning across water environments
