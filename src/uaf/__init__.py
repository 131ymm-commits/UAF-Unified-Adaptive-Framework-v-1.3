"""
UAF — Unified Adaptive Framework.

Minimal computational primitives:
- surprisal
- entropy
- KL divergence
- variational free energy
- normalized predictive gain
- consensus divergence
"""

from .metrics import (
    safe_normalize,
    entropy,
    kl_divergence,
    surprisal,
    cross_entropy,
    variational_free_energy,
    normalized_predictive_gain,
    mean_pairwise_kl,
)
