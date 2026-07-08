"""PyTorch neural equalizer scaffold for UWOC receivers.

This module is implemented as an optional component. It does not report any
performance claims; it only defines a small neural receiver architecture that
can be trained in future experiments.
"""

from __future__ import annotations

try:
    import torch
    from torch import nn
except ImportError:  # pragma: no cover
    torch = None
    nn = None


class TorchAvailabilityError(ImportError):
    """Raised when PyTorch-dependent modules are used without PyTorch."""


if nn is not None:

    class NeuralEqualizer(nn.Module):
        """Small MLP equalizer for scalar received UWOC samples.

        The model maps one or more received features to a bit logit. It is a
        prototype receiver, not a validated state-of-the-art architecture.
        """

        def __init__(self, input_dim: int = 1, hidden_dim: int = 32) -> None:
            super().__init__()
            self.network = nn.Sequential(
                nn.Linear(input_dim, hidden_dim),
                nn.ReLU(),
                nn.Linear(hidden_dim, hidden_dim),
                nn.ReLU(),
                nn.Linear(hidden_dim, 1),
            )

        def forward(self, inputs: "torch.Tensor") -> "torch.Tensor":
            """Return logits for binary OOK symbol decisions."""
            return self.network(inputs)

else:

    class NeuralEqualizer:  # type: ignore[no-redef]
        """Placeholder used when PyTorch is unavailable."""

        def __init__(self, *_args: object, **_kwargs: object) -> None:
            raise TorchAvailabilityError("Install PyTorch with `pip install -e .[ai]`.")
