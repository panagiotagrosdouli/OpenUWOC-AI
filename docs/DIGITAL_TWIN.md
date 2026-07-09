# UWOC Digital Twin Workflow

This document defines the first Digital Twin abstraction for OpenUWOC-AI.
It is designed for reproducible simulation-to-observation studies, not for claiming a validated underwater deployment.

## State variables

The canonical state is `DigitalTwinState` and contains:

- time stamp;
- water type;
- link distance;
- transmit optical power;
- wavelength;
- absorption, scattering, and attenuation coefficients;
- pointing offset;
- turbulence proxy;
- thermal-noise proxy;
- optional SNR and BER observations.

## Synchronization

`UWOCStateSynchronizer` aligns observed states with simulated states by nearest timestamp within a configurable tolerance.
The output is a list of `SimulatedObservedPair` objects.
Each pair can compute observed-minus-simulated residuals for calibration audits.

## Predictive hooks

`UWOCSystemTwin` supports named prediction hooks:

```python
from openuwoc_ai.digital_twin import UWOCSystemTwin

twin = UWOCSystemTwin(initial_state)
twin.register_prediction_hook("ber_predictor", lambda state: {"ber_hat": 0.01})
predictions = twin.predict()
```

Hooks can later wrap neural BER predictors, adaptive modulation policies, or uncertainty estimators.
They are deliberately typed as small functions so that non-AI baselines and AI prototypes can share the same interface.

## Transfer-learning experiments

`TransferExperimentSpec` records source and target water domains, feature fields, and target fields.
This is enough to define controlled experiments such as:

- train on clear-ocean simulation and adapt to coastal simulation;
- train on coastal simulation and evaluate on turbid-harbor simulation;
- compare physics-only calibration against learned residual correction.

## Scientific status

Implemented:

- state definition;
- timestamp-based state synchronization;
- residual computation;
- predictive hook interface;
- transfer-experiment specification.

Prototype / planned:

- learned residual correction;
- online calibration from measured tank data;
- adaptive modulation controller;
- sim-to-real validation.

No real underwater experimental claim should be made until measured logs, calibration metadata, and reproduction scripts are committed.
