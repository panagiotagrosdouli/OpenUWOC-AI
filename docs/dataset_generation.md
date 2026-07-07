# Dataset Generation

OpenUWOC-AI provides a first synthetic dataset generator for baseline UWOC link-budget experiments.

## Purpose

The generator creates tabular data for early AI experiments such as channel prediction, link adaptation, and benchmark comparisons.

## Generated Fields

- environment
- distance_m
- transmit_power_w
- absorption_coefficient
- scattering_coefficient
- attenuation_coefficient
- beam_divergence_rad
- receiver_aperture_m
- attenuation_loss
- geometric_loss
- received_power_w
- signal_to_noise_ratio

## Usage

```bash
python examples/generate_dataset.py
```

The example writes a CSV dataset to the experiments output folder.

## Scientific Note

The current generator is a baseline software component. The next research step is to validate the coefficients and extend the model with wavelength dependence, turbulence, pointing error, mobility, and measured-data calibration.
