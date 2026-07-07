# OpenUWOC-AI

OpenUWOC-AI is an open-source research framework for Artificial Intelligence-powered Underwater Wireless Optical Communications (UWOC).

The project aims to provide researchers, students, and engineers with a modular, extensible, and reproducible platform for developing, simulating, and evaluating next-generation UWOC systems.

## Vision

OpenUWOC-AI is designed to support high-quality academic research and future publications in IEEE journals and conferences. It focuses on the intersection of underwater optical wireless communications, artificial intelligence, digital twins, and intelligent network optimization.

## Core Capabilities

- Underwater optical wireless channel simulation
- Configurable underwater environment models
- AI-ready APIs for learning-based communication optimization
- Digital twin abstractions for UWOC systems
- Optimization modules for beam alignment, power control, routing, and resource allocation
- Reproducible experiments with configuration files and logging
- Visualization utilities for research-grade figures

## Initial Research Directions

- AI-driven UWOC channel modeling and prediction
- Generative AI for synthetic underwater channel datasets
- Reinforcement learning for adaptive modulation and power control
- Graph neural networks for underwater network optimization
- Digital twin-assisted link adaptation and transfer learning
- Energy-efficient and secure UWOC system design

## Project Structure

```text
OpenUWOC-AI/
├── docs/                  # Architecture, roadmap, and research notes
├── examples/              # Runnable examples
├── experiments/           # Reproducible experiment configurations
├── notebooks/             # Exploratory research notebooks
├── src/openuwoc_ai/       # Main Python package
├── tests/                 # Unit tests
├── pyproject.toml         # Python packaging and tool configuration
└── README.md
```

## Quick Start

```bash
git clone https://github.com/panagiotagrosdouli/OpenUWOC-AI.git
cd OpenUWOC-AI
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e .[dev]
pytest
```

## Minimal Example

```python
from openuwoc_ai.channels import UnderwaterOpticalChannel
from openuwoc_ai.environments import WaterEnvironment

water = WaterEnvironment.preset("coastal")
channel = UnderwaterOpticalChannel(environment=water)

result = channel.link_budget(distance_m=20.0, transmit_power_w=1.0)
print(result.received_power_w)
```

## Status

This repository is at the initial framework-design stage. The first milestone is to implement a validated baseline UWOC channel model, environment presets, reproducible experiments, and basic AI-ready interfaces.

## Citation

If you use this project in academic work, please cite the repository. A formal `CITATION.cff` file will be maintained as the project matures.

## License

This project is released under the MIT License.
