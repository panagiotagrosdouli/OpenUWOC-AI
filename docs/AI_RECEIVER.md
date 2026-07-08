# AI Receiver

## Implemented/prototype software

`openuwoc_ai.ml.models` contains:

- `NeuralEqualizer`: small MLP mapping received samples/windows to bit probabilities.
- `BerPredictor`: small MLP mapping link features to BER estimates.

## Required baselines

AI receivers must be evaluated against:

- OOK threshold detection;
- matched filtering;
- linear equalization;
- channel-estimator-assisted receivers;
- oracle-channel upper bounds when appropriate.

## Limitation

The neural receiver is a prototype. The repository does not currently provide benchmark evidence that it improves BER, robustness, or generalization.
