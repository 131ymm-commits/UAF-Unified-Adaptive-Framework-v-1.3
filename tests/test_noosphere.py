from uaf.noosphere import (
    tokenize,
    entropy,
    kl_divergence,
    surprisal,
    normalized_predictive_gain,
    uaf_score,
    BeliefState,
    NoosphereEngine,
)


def test_tokenize_removes_stop_words():
    tokens = tokenize("the brain generates predictions about sensory input")
    assert "the" not in tokens
    assert "about" not in tokens
    assert "brain" in tokens
    assert "predictions" in tokens


def test_entropy_uniform_is_maximum():
    uniform = {"a": 0.5, "b": 0.5}
    skewed = {"a": 0.9, "b": 0.1}
    assert entropy(uniform) > entropy(skewed)


def test_kl_zero_for_identical():
    p = {"a": 0.6, "b": 0.4}
    assert kl_divergence(p, p) < 1e-9


def test_surprisal_lower_for_common_token():
    assert surprisal("prediction", {"prediction": 0.8, "entropy": 0.2}) < \
           surprisal("entropy", {"prediction": 0.8, "entropy": 0.2})


def test_npg_positive_when_model_is_better():
    npg = normalized_predictive_gain(model_surprisal=1.0, baseline_surprisal=3.0)
    assert npg > 0


def test_npg_negative_when_model_is_worse():
    npg = normalized_predictive_gain(model_surprisal=4.0, baseline_surprisal=3.0)
    assert npg < 0


def test_uaf_score_in_range():
    for npg_val in [-5.0, -1.0, 0.0, 1.0, 5.0]:
        score = uaf_score(npg_val)
        assert -3.0 <= score <= 3.0


def test_belief_state_updates():
    belief = BeliefState()
    assert belief.is_empty()
    belief.update(["prediction", "entropy", "prediction"])
    assert not belief.is_empty()
    assert belief.counts["prediction"] == 2


def test_engine_integrates_new_knowledge():
    engine = NoosphereEngine()
    result = engine.evaluate(
        "Predictive coding minimizes free energy through hierarchical inference.",
        label="test_doc"
    )
    assert result["integrated"] is True
    assert result["npg"] >= 0


def test_engine_flags_redundant():
    engine = NoosphereEngine()

    text = "Prediction minimizes surprise through hierarchical inference models."
    engine.evaluate(text, label="first")
    engine.evaluate(text, label="second")
    result = engine.evaluate(text, label="third")

    assert result["npg"] < engine.evaluate(
        "Quantum spin topology manifold belief state representation.",
        label="new"
    )["npg"]


def test_engine_report_structure():
    engine = NoosphereEngine()
    engine.evaluate("The noosphere maximizes collective predictive gain.")
    report = engine.report()

    assert "documents_seen" in report
    assert "collective_free_energy" in report
    assert "average_npg" in report
    assert "belief_vocab_size" in report
