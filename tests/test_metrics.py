import numpy as np

from uaf.metrics import (
    entropy,
    kl_divergence,
    surprisal,
    variational_free_energy,
    normalized_predictive_gain,
    mean_pairwise_kl,
)


def test_entropy_uniform_greater_than_delta():
    uniform = np.array([0.5, 0.5])
    delta = np.array([1.0, 0.0])

    assert entropy(uniform) > entropy(delta)


def test_kl_zero_for_same_distribution():
    p = np.array([0.2, 0.8])

    assert kl_divergence(p, p) < 1e-9


def test_surprisal_lower_for_likely_event():
    assert surprisal(0.9) < surprisal(0.1)


def test_variational_free_energy_nonnegative_like():
    posterior = np.array([0.7, 0.3])
    prior = np.array([0.5, 0.5])
    likelihood = np.array([0.9, 0.2])

    f = variational_free_energy(posterior, prior, likelihood)

    assert f >= 0


def test_npg_positive_when_model_better():
    assert normalized_predictive_gain(model_loss=0.2, baseline_loss=0.5) > 0


def test_mean_pairwise_kl_zero_for_identical():
    distributions = [
        np.array([0.4, 0.6]),
        np.array([0.4, 0.6]),
        np.array([0.4, 0.6]),
    ]

    assert mean_pairwise_kl(distributions) < 1e-9
