from __future__ import annotations

import numpy as np


EPS = 1e-12


def safe_normalize(x: np.ndarray, eps: float = EPS) -> np.ndarray:
    """
    Normalize a non-negative vector into a probability distribution.

    Parameters
    ----------
    x:
        Input vector.
    eps:
        Numerical stability constant.

    Returns
    -------
    np.ndarray
        Probability vector summing to 1.

    Raises
    ------
    ValueError
        If vector contains negative values or has zero total mass.
    """
    x = np.asarray(x, dtype=float)

    if np.any(x < 0):
        raise ValueError("Probabilities or weights must be non-negative.")

    total = float(np.sum(x))

    if total <= eps:
        raise ValueError("Cannot normalize vector with near-zero total mass.")

    return x / total


def entropy(p: np.ndarray, eps: float = EPS) -> float:
    """
    Shannon entropy H(p) = -sum p log p.
    """
    p = safe_normalize(p, eps)
    return float(-np.sum(p * np.log(p + eps)))


def kl_divergence(p: np.ndarray, q: np.ndarray, eps: float = EPS) -> float:
    """
    KL divergence D_KL(p || q).
    """
    p = safe_normalize(p, eps)
    q = safe_normalize(q, eps)
    return float(np.sum(p * np.log((p + eps) / (q + eps))))


def cross_entropy(p: np.ndarray, q: np.ndarray, eps: float = EPS) -> float:
    """
    Cross entropy H(p, q) = -sum p log q.
    """
    p = safe_normalize(p, eps)
    q = safe_normalize(q, eps)
    return float(-np.sum(p * np.log(q + eps)))


def surprisal(probability: float, eps: float = EPS) -> float:
    """
    Surprisal of an event: -log p.
    """
    if probability < 0 or probability > 1:
        raise ValueError("Probability must be in [0, 1].")
    return float(-np.log(max(probability, eps)))


def variational_free_energy(
    posterior: np.ndarray,
    prior: np.ndarray,
    likelihood: np.ndarray,
    eps: float = EPS,
) -> float:
    """
    Simplified discrete variational free energy:

        F = E_Q[-log P(o|s)] + D_KL(Q(s)||P(s))

    Parameters
    ----------
    posterior:
        Q(s)
    prior:
        P(s)
    likelihood:
        P(o|s)

    Returns
    -------
    float
        Variational free energy.
    """
    q = safe_normalize(posterior, eps)
    p = safe_normalize(prior, eps)

    likelihood = np.asarray(likelihood, dtype=float)

    if np.any(likelihood < 0):
        raise ValueError("Likelihood must be non-negative.")

    accuracy_cost = float(-np.sum(q * np.log(likelihood + eps)))
    complexity = kl_divergence(q, p, eps)

    return accuracy_cost + complexity


def normalized_predictive_gain(
    model_loss: float,
    baseline_loss: float,
    eps: float = EPS,
) -> float:
    """
    Normalized Predictive Gain:

        NPG = (baseline_loss - model_loss) / (baseline_loss + eps)

    Positive means the model improves over baseline.
    Zero means no improvement.
    Negative means worse than baseline.
    """
    if baseline_loss < 0 or model_loss < 0:
        raise ValueError("Loss values must be non-negative.")

    return float((baseline_loss - model_loss) / (baseline_loss + eps))


def mean_pairwise_kl(distributions: list[np.ndarray], eps: float = EPS) -> float:
    """
    Mean pairwise KL divergence across a set of distributions.

    Useful as a simple collective incoherence metric.
    """
    if len(distributions) < 2:
        return 0.0

    values = []

    for i in range(len(distributions)):
        for j in range(i + 1, len(distributions)):
            values.append(kl_divergence(distributions[i], distributions[j], eps))

    return float(np.mean(values))
