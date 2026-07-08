# System Architecture

```text
bits -> modulation -> optical channel -> receiver -> metrics
                         |              |
                         |              +-> AI equalizer prototype
                         +-> absorption, scattering, turbulence, pointing, noise
```

## Package map

- `openuwoc_ai/channel`: absorption, scattering, attenuation, pointing error, turbulence, and noise.
- `openuwoc_ai/modulation`: OOK and future modulation families.
- `openuwoc_ai/simulation`: transmitter-channel-receiver experiments.
- `openuwoc_ai/ml`: neural equalizer and BER predictor prototypes.
- `openuwoc_ai/evaluation`: BER, SER, SNR, confidence intervals, and robustness metrics.
- `openuwoc_ai/visualization`: publication-oriented plots and waveform exports.

## Engineering rationale

Core logic lives in importable Python modules. Scripts are thin entry points. Experiments are configuration-driven with deterministic seeds so that figures and result tables can be regenerated.
