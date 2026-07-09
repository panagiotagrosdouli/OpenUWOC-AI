# OpenUWOC-AI

[![Python](https://img.shields.io/badge/python-3.10%2B-blue)](pyproject.toml)
[![Tests](https://img.shields.io/badge/tests-pytest-informational)](tests/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-simulation--only-orange)](docs/REPRODUCIBILITY.md)

**OpenUWOC-AI is a research-grade, simulation-first framework for studying how AI can improve the robustness, reliability, and adaptability of underwater optical wireless communication (UWOC).**

> Central research question: **How can AI improve UWOC under absorption, scattering, turbulence, misalignment, and noise?**

This repository is designed to look and behave like software accompanying a serious IEEE OCEANS / ICC / Globecom / IEEE Access / ICRA / IROS / RA-L research project, while remaining scientifically honest: no fabricated results, no unverified state-of-the-art claims, and clear separation between implemented, prototype, and planned work.

## Motivation

UWOC can support high-rate short-range links for marine robotics, autonomous underwater vehicles, diver systems, and underwater sensor networks. The physical channel is challenging because seawater causes wavelength-dependent absorption, scattering, turbulence-induced irradiance fluctuation, pointing loss from platform motion, ambient light noise, shot noise, and receiver thermal noise.

AI may help when the channel is nonlinear, time-varying, partially observed, or difficult to model analytically. However, AI receivers must be compared against classical baselines and evaluated under reproducible assumptions.

## System architecture

```text
bits -> modulation -> optical channel -> receiver -> metrics
                         |              |
                         |              +-> neural equalizer / BER predictor prototypes
                         +-> absorption + scattering + turbulence + pointing + noise

simulator states + observed states -> Digital Twin -> calibration residuals / AI hooks
sampled scenarios -> synthetic dataset generator -> CSV + metadata -> AI training pipeline
```

## UWOC channel model

The baseline channel uses intensity modulation/direct detection:

```math
y_k = h_k P_t[k] + P_{amb} + n_{shot,k} + n_{th,k}
```

with

```math
h_k = \exp[-(a(\lambda)+b(\lambda))d] h_p(k) h_t(k).
```

See [`docs/MATHEMATICAL_FORMULATION.md`](docs/MATHEMATICAL_FORMULATION.md) for notation, assumptions, and limitations.

## AI receiver pipeline

```text
received samples -> feature/window extraction -> neural equalizer -> bit probabilities
                                  |               |
                                  |               +-> thresholded decisions
                                  +-> BER predictor / adaptive policy state
```

The AI components are currently **prototypes**. They are implemented to enable reproducible experiments, not to claim superiority.

## Installation

```bash
git clone https://github.com/panagiotagrosdouli/OpenUWOC-AI.git
cd OpenUWOC-AI
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
```

For PyTorch prototypes:

```bash
pip install -e .[ai]
```

## Quick start

```python
from openuwoc_ai.channel.models import ChannelConfig, UnderwaterOpticalChannel, WaterType
from openuwoc_ai.modulation.ook import bits_to_ook, random_bits, threshold_detect
from openuwoc_ai.evaluation.metrics import bit_error_rate

bits = random_bits(1000, seed=7)
tx = bits_to_ook(bits, optical_power_w=1.0)
channel = UnderwaterOpticalChannel(ChannelConfig(water_type=WaterType.COASTAL, distance_m=10.0))
rx = channel.propagate(tx)
estimated = threshold_detect(rx)
print(bit_error_rate(bits, estimated))
```

## Run a reproducible experiment

```bash
python scripts/run_experiment.py configs/coastal_ook_baseline.yaml --output results/coastal_ook_baseline.csv
```

## Generate an AI-ready synthetic dataset

```bash
python scripts/generate_synthetic_dataset.py \
  configs/synthetic_dataset_baseline.yaml \
  --csv results/datasets/synthetic_channel_states.csv \
  --metadata results/datasets/synthetic_channel_states.metadata.json
```

The dataset generator samples water type, distance, transmit power, wavelength, pointing offset, turbulence, and noise, then records simulator-derived BER/SNR labels. See [`docs/SYNTHETIC_DATASETS.md`](docs/SYNTHETIC_DATASETS.md).

## Digital Twin workflow

The Digital Twin layer stores UWOC state variables, synchronizes simulated and observed states, computes calibration residuals, and exposes predictive hooks for future AI models. See [`docs/DIGITAL_TWIN.md`](docs/DIGITAL_TWIN.md).

## Generate the demo GIF

```bash
python scripts/make_demo_gif.py
```

Outputs:

- `assets/demo.gif`
- `results/videos/demo.mp4` when ffmpeg is available

The animation is generated from code and is illustrative, not measured experimental evidence.

## Implemented / Prototype / Planned

| Area | Status | Notes |
|---|---:|---|
| Beer-Lambert attenuation | Implemented | Uses `c=a+b` water profiles |
| Water profiles | Implemented | Clear ocean, coastal, turbid harbor simulation presets |
| Pointing error | Implemented | Gaussian pointing-loss scaffold |
| Turbulence | Prototype | Unit-mean lognormal scaffold |
| Thermal / shot noise | Implemented | Gaussian thermal noise and shot-noise approximation |
| OOK modulation | Implemented | Symbol mapping and threshold detector |
| BER/SER/SNR metrics | Implemented | Includes Wilson confidence intervals |
| YAML experiments | Implemented | Deterministic seeds |
| Synthetic dataset generator | Implemented | Writes CSV plus metadata JSON for AI prototyping |
| Digital Twin state/synchronization | Implemented | State model, residuals, hooks, transfer spec |
| Neural equalizer | Prototype | Small PyTorch MLP |
| BER predictor | Prototype | Small PyTorch MLP |
| BPSK/QPSK/M-QAM/OFDM | Planned | API to be added |
| Matched filter / linear equalizer | Planned | Required classical baselines |
| Real experimental data | Planned | No real dataset currently committed |
| Adaptive modulation policy | Planned | Current demo uses a rule-based proxy only |

## Metrics

- Bit error rate (BER)
- Symbol error rate (SER)
- Approximate SNR
- Wilson confidence interval
- Robustness under water type, distance, noise, turbidity, and pointing perturbations
- Synthetic dataset schema reproducibility
- Digital Twin residuals between simulated and observed states

## Limitations

- Current results are simulation-only.
- Water coefficients are presets and must be calibrated before physical claims.
- Turbulence and multipath models are scaffolds.
- Neural models are prototypes and are not benchmarked against all classical baselines yet.
- The synthetic dataset generator produces simulator labels, not measured underwater data.
- The Digital Twin layer is an abstraction for calibration workflows, not a validated deployment system.
- No state-of-the-art claim is made.

## Roadmap

See [`docs/ROADMAP.md`](docs/ROADMAP.md).

## Future MSc/PhD extensions

- Tank-based UWOC dataset acquisition and calibration.
- Robust neural equalization across unseen water types.
- Joint channel estimation and adaptive modulation.
- Physics-informed neural receivers.
- AUV/ROV optical link adaptation under motion-induced pointing error.
- Sim-to-real transfer for underwater communication links.

## Citation

See [`CITATION.cff`](CITATION.cff). Until a paper is published, cite this repository as simulation software and avoid implying peer-reviewed experimental validation.

## License

MIT License. See [`LICENSE`](LICENSE).
