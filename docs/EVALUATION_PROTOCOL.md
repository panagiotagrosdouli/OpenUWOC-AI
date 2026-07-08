# Evaluation Protocol

## Baselines

1. Classical OOK threshold detector: implemented.
2. Matched filter: planned.
3. Linear equalizer: planned.
4. Neural equalizer: prototype.
5. Oracle channel estimator: planned scaffold.

## Required reporting

Every experiment should report:

- water profile and coefficient assumptions;
- distance, transmit power, pointing offset, and noise parameters;
- number of transmitted bits/symbols;
- random seed;
- BER or SER;
- confidence interval;
- whether the result is simulation-only or measured.

## Prohibited reporting

Do not claim state-of-the-art, experimental validation, or field performance unless a reproducible benchmark and dataset are committed. Do not compare against papers unless the implementation, assumptions, and channel conditions are compatible.
