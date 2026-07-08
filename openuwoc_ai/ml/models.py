"""Prototype neural receivers and predictors for AI-assisted UWOC.

These models are intentionally small PyTorch scaffolds. They are implemented so
experiments can be reproduced, but they are not claimed to outperform classical
baselines without benchmark evidence.
"""

from __future__ import annotations

try:
    import torch
    from torch import nn
except ImportError:  # pragma: no cover - optional dependency path
    torch = None
    nn = None


if nn is not None:

    class NeuralEqualizer(nn.Module):
        """Simple MLP equalizer for scalar received samples or short windows."""

        def __init__(self, input_dim: int = 1, hidden_dim: int = 32):
            super().__init__()
            self.network = nn.Sequential(
                nn.Linear(input_dim, hidden_dim),
                nn.ReLU(),
                nn.Linear(hidden_dim, hidden_dim),
                nn.ReLU(),
                nn.Linear(hidden_dim, 1),
                nn.Sigmoid(),
            )

        def forward(self, samples: "torch.Tensor") -> "torch.Tensor":
            """Return bit probabilities for received samples."""
            return self.network(samples)


    class BerPredictor(nn.Module):
        """Small regression network for simulation-derived BER prediction."""

        def __init__(self, feature_dim: int = 5, hidden_dim: int = 32):
            super().__init__()
            self.network = nn.Sequential(
                nn.Linear(feature_dim, hidden_dim),
                nn.ReLU(),
                nn.Linear(hidden_dim, hidden_dim),
                nn.ReLU(),
                nn.Linear(hidden_dim, 1),
                nn.Sigmoid(),
            )

        def forward(self, features: "torch.Tensor") -> "torch.Tensor":
            """Return predicted BER in [0, 1]."""
            return self.network(features)

else:

    class NeuralEqualizer:  # type: ignore[no-redef]
        """Placeholder raised when PyTorch is not installed."""

        def __init__(self, *_: object, **__: object) -> None:
            raise ImportError("Install openuwoc-ai[ai] to use NeuralEqualizer")


    class BerPredictor:  # type: ignore[no-redef]
        """Placeholder raised when PyTorch is not installed."""

        def __init__(self, *_: object, **__: object) -> None:
            raise ImportError("Install openuwoc-ai[ai] to use BerPredictor")
