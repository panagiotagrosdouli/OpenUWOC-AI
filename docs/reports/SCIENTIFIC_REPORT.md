# Scientific Report

## Scope

OpenUWOC-AI studies underwater optical wireless communication (UWOC) with simulation-first physical-layer models and prototype AI receivers. The repository is intended for reproducible algorithm development, not for claiming real-world performance without calibrated experimental data.

## Research Questions

1. How do absorption, scattering, turbulence, pointing error, and receiver noise affect bit-level reliability under OOK intensity modulation?
2. Which operating regimes are suitable for classical threshold detection, and which regimes motivate learned equalization or adaptive policies?
3. How can simulation assumptions be made explicit enough to support future tank or field validation?

## Implemented Contributions

- Deterministic channel simulation scaffold for water-type, distance, attenuation, pointing, turbulence, and noise perturbations.
- OOK modulation and threshold-detection baseline for transparent physical-layer evaluation.
- Metric pipeline for BER, SER, SNR-style summaries, and confidence intervals.
- Prototype AI receiver components that are explicitly marked as non-SOTA and non-validated.

## Scientific Impact

The project provides a reproducible bridge between communication theory, marine robotics, and AI-assisted receiver design. Its primary value is methodological: it gives future experiments a controlled simulator, a baseline, and documentation of assumptions before hardware validation.

## Limitations

- Results are simulation-only unless generated from future calibrated datasets.
- Turbulence, multipath, and water optical properties currently use simplified presets.
- Neural receiver prototypes require systematic comparison against classical equalizers before any performance claim.
- No real tank, sea-trial, or hardware-in-the-loop dataset is included.

## Future Research Directions

- Calibrate water coefficients using measured absorption and scattering profiles.
- Add classical baselines such as matched filtering, adaptive thresholding, linear equalization, and MLSE.
- Extend modulation support to PPM, PAM, OFDM, and higher-order constellations where physically appropriate.
- Evaluate uncertainty-aware adaptation under AUV/ROV motion-induced pointing error.
- Add sim-to-real validation once real optical link measurements are available.
