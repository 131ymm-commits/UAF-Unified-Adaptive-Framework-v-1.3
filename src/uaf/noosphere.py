"""
UAF Noosphere Engine
====================
A living system that maximizes Normalized Predictive Gain (NPG)
by filtering incoming knowledge through the lens of collective free energy.

No external APIs required.
No pretend output.
Pure UAF mechanics.

Run:
    python -m uaf.noosphere
"""

from __future__ import annotations

import math
import re
import json
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional


# ---------------------------------------------------------------------------
# Core: vocabulary and belief state
# ---------------------------------------------------------------------------

STOP_WORDS = {
    "the", "a", "an", "is", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "do", "does", "did", "will", "would", "could",
    "should", "may", "might", "shall", "can", "need", "dare", "ought",
    "used", "to", "of", "in", "for", "on", "with", "at", "by", "from",
    "as", "into", "through", "during", "before", "after", "above", "below",
    "between", "each", "but", "or", "and", "not", "no", "so", "if", "it",
    "its", "this", "that", "these", "those", "i", "we", "you", "he", "she",
    "they", "what", "which", "who", "whom", "when", "where", "why", "how",
}

EPS = 1e-12


def tokenize(text: str) -> list[str]:
    """
    Minimal tokenizer.
    Lowercases, splits on non-alphabetic characters,
    removes stop words and short tokens.
    """
    tokens = re.findall(r"[a-zA-Z]+", text.lower())
    return [t for t in tokens if t not in STOP_WORDS and len(t) > 3]


def counts_to_distribution(counts: Counter, vocab: set[str]) -> dict[str, float]:
    """
    Convert token counts to a probability distribution over a vocabulary.
    Adds Laplace smoothing (alpha=1) for unseen tokens.
    """
    total = sum(counts.values()) + len(vocab)
    return {
        token: (counts.get(token, 0) + 1) / total
        for token in vocab
    }


# ---------------------------------------------------------------------------
# Core metrics
# ---------------------------------------------------------------------------

def entropy(distribution: dict[str, float]) -> float:
    """Shannon entropy H(p) = -sum p log p."""
    return -sum(
        p * math.log(p + EPS)
        for p in distribution.values()
        if p > 0
    )


def kl_divergence(p: dict[str, float], q: dict[str, float]) -> float:
    """
    KL divergence D_KL(p || q).
    p is the new distribution, q is the prior.
    """
    result = 0.0
    for token, p_val in p.items():
        q_val = q.get(token, EPS)
        if p_val > 0:
            result += p_val * math.log((p_val + EPS) / (q_val + EPS))
    return max(result, 0.0)


def surprisal(token: str, distribution: dict[str, float]) -> float:
    """Surprisal of a token: -log P(token)."""
    p = distribution.get(token, EPS)
    return -math.log(p + EPS)


def average_surprisal(tokens: list[str], distribution: dict[str, float]) -> float:
    """Average surprisal of a list of tokens under a distribution."""
    if not tokens:
        return 0.0
    return sum(surprisal(t, distribution) for t in tokens) / len(tokens)


def normalized_predictive_gain(
    model_surprisal: float,
    baseline_surprisal: float,
) -> float:
    """
    NPG = (baseline - model) / (baseline + eps)

    Positive: model reduces surprise better than baseline.
    Zero: no improvement.
    Negative: model is worse than baseline.
    """
    return (baseline_surprisal - model_surprisal) / (baseline_surprisal + EPS)


def uaf_score(npg: float) -> float:
    """
    Map NPG to UAF scale [-3, +3] via tanh.
    """
    return 3.0 * math.tanh(npg / 2.0)


# ---------------------------------------------------------------------------
# Belief State
# ---------------------------------------------------------------------------

@dataclass
class BeliefState:
    """
    The noosphere's current model of the world.

    Represented as a probability distribution over a vocabulary,
    built from accumulated knowledge tokens.
    """
    counts: Counter = field(default_factory=Counter)
    vocab: set[str] = field(default_factory=set)
    total_documents: int = 0

    def update(self, tokens: list[str]) -> None:
        """Absorb new tokens into the belief state."""
        self.counts.update(tokens)
        self.vocab.update(tokens)
        self.total_documents += 1

    def distribution(self) -> dict[str, float]:
        """Return probability distribution with Laplace smoothing."""
        return counts_to_distribution(self.counts, self.vocab)

    def entropy(self) -> float:
        return entropy(self.distribution())

    def is_empty(self) -> bool:
        return self.total_documents == 0


# ---------------------------------------------------------------------------
# Noosphere Engine
# ---------------------------------------------------------------------------

@dataclass
class NoosphereEngine:
    """
    UAF Noosphere Engine.

    Accepts text documents and evaluates each against the current
    collective belief state using Normalized Predictive Gain.

    Documents with high NPG are integrated (they reduce surprise).
    Documents with low NPG are flagged as redundant.

    This is the living implementation of:

        F_total = sum_k F_k + lambda * sum_{i<j} D_KL(Q_i || Q_j)

    in its simplest single-agent form.
    """

    name: str = "UAF Noosphere v0.1"
    npg_threshold: float = 0.0
    lambda_consistency: float = 0.5
    belief: BeliefState = field(default_factory=BeliefState)
    history: list[dict] = field(default_factory=list)

    def evaluate(self, text: str, label: Optional[str] = None) -> dict:
        """
        Evaluate a new document against the current belief state.

        Returns a result dict containing:
        - tokens extracted,
        - surprisal before and after integration,
        - NPG,
        - UAF score,
        - integration decision.
        """
        tokens = tokenize(text)

        if not tokens:
            return {
                "label": label or "unnamed",
                "tokens": 0,
                "status": "EMPTY",
                "npg": 0.0,
                "uaf_score": 0.0,
                "integrated": False,
            }

        # Baseline: uniform distribution over current + new vocab
        new_vocab = self.belief.vocab | set(tokens)
        baseline_dist = {t: 1.0 / len(new_vocab) for t in new_vocab}
        baseline_s = average_surprisal(tokens, baseline_dist)

        # Current model surprisal
        if self.belief.is_empty():
            # No model yet: everything is new, surprisal = log(vocab_size)
            current_s = math.log(max(len(tokens), 1) + EPS)
        else:
            current_s = average_surprisal(tokens, self.belief.distribution())

        # Compute NPG
        npg = normalized_predictive_gain(current_s, baseline_s)
        score = uaf_score(npg)

        # Decision
        integrate = npg >= self.npg_threshold

        if integrate:
            # Prior before integration
            if not self.belief.is_empty():
                prior_dist = self.belief.distribution()
            else:
                prior_dist = None

            self.belief.update(tokens)

            # Complexity cost: KL from prior to posterior
            if prior_dist is not None:
                posterior_dist = self.belief.distribution()
                complexity = kl_divergence(posterior_dist, prior_dist)
            else:
                complexity = 0.0

            # Free energy after integration
            post_s = average_surprisal(tokens, self.belief.distribution())
            free_energy = post_s + self.lambda_consistency * complexity
            status = "INTEGRATED"
        else:
            complexity = 0.0
            free_energy = current_s
            status = "REDUNDANT"

        result = {
            "label": label or f"doc_{len(self.history):03d}",
            "tokens": len(tokens),
            "baseline_surprisal": round(baseline_s, 4),
            "model_surprisal": round(current_s, 4),
            "npg": round(npg, 4),
            "uaf_score": round(score, 4),
            "complexity_cost": round(complexity, 4),
            "free_energy": round(free_energy, 4),
            "belief_entropy": round(self.belief.entropy(), 4),
            "belief_vocab_size": len(self.belief.vocab),
            "status": status,
            "integrated": integrate,
        }

        self.history.append(result)
        return result

    def collective_free_energy(self) -> float:
        """
        Global estimate of collective free energy:
        average surprisal + lambda * belief entropy.
        """
        if self.belief.is_empty():
            return float("inf")

        dist = self.belief.distribution()
        avg_s = sum(
            -math.log(p + EPS) * p
            for p in dist.values()
        )
        return avg_s + self.lambda_consistency * self.belief.entropy()

    def report(self) -> dict:
        """Summary of the noosphere's current state."""
        integrated = [r for r in self.history if r["integrated"]]
        redundant = [r for r in self.history if not r["integrated"]]

        avg_npg = (
            sum(r["npg"] for r in self.history) / len(self.history)
            if self.history else 0.0
        )

        return {
            "engine": self.name,
            "documents_seen": len(self.history),
            "documents_integrated": len(integrated),
            "documents_redundant": len(redundant),
            "belief_vocab_size": len(self.belief.vocab),
            "belief_entropy": round(self.belief.entropy(), 4),
            "collective_free_energy": round(self.collective_free_energy(), 4),
            "average_npg": round(avg_npg, 4),
            "average_uaf_score": round(uaf_score(avg_npg), 4),
        }

    def save(self, path: str) -> None:
        """Save history to JSON."""
        data = {
            "report": self.report(),
            "history": self.history,
            "belief_counts": dict(self.belief.counts.most_common(100)),
        }
        Path(path).write_text(
            json.dumps(data, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

    def load_counts(self, path: str) -> None:
        """Load previously saved belief counts."""
        data = json.loads(Path(path).read_text(encoding="utf-8"))
        counts = data.get("belief_counts", {})
        self.belief.counts = Counter(counts)
        self.belief.vocab = set(counts.keys())
        self.belief.total_documents = data["report"]["documents_integrated"]


# ---------------------------------------------------------------------------
# Demo: run the noosphere on UAF-related texts
# ---------------------------------------------------------------------------

DEMO_DOCUMENTS = [
    (
        "Predictive coding is a theory of brain function in which the brain "
        "constantly generates and updates predictions about sensory input. "
        "Prediction errors propagate upward through the hierarchy.",
        "predictive_coding_intro",
    ),
    (
        "The free energy principle states that biological organisms minimize "
        "variational free energy to maintain their integrity. "
        "This involves both perception and action.",
        "free_energy_principle",
    ),
    (
        "Active inference extends predictive coding to action. "
        "Agents select policies that minimize expected free energy, "
        "balancing risk and ambiguity.",
        "active_inference",
    ),
    (
        "The brain generates predictions. Organisms minimize free energy. "
        "The brain generates predictions. Organisms minimize free energy.",
        "redundant_repetition",
    ),
    (
        "Spin is a topological invariant of the quantum prediction manifold. "
        "The belief state for spin-half lives in CP1, governed by SU2. "
        "A rotation by 2pi changes the sign of the state.",
        "spin_as_topology",
    ),
    (
        "Language minimizes collective free energy between communicating agents. "
        "Meaning is the expected reduction in surprise that a word produces "
        "in a given context. Grammar emerges from optimal compression.",
        "language_free_energy",
    ),
    (
        "A black hole is a region where the external predictive free energy "
        "diverges at the horizon. The singularity is not a physical point "
        "but a collapse of the level-one description.",
        "black_holes_uaf",
    ),
    (
        "The cosmic microwave background encodes the oldest prediction residue. "
        "Anomalies at large scales may be traces of the mathematical substrate "
        "transition into quantum fields.",
        "cmb_anomalies",
    ),
    (
        "Large language models provide the sensory-motor interface of the noosphere. "
        "They allow the global knowledge network to transition from passive storage "
        "to active predictive inference across all scales.",
        "llm_noosphere",
    ),
    (
        "Mathematics is the structural substrate of compressible invariance. "
        "A mathematical structure applies to a domain when it reduces "
        "the Kolmogorov complexity of that domain.",
        "mathematics_L_minus_1",
    ),
]


def run_demo() -> None:
    print("=" * 72)
    print("UAF NOOSPHERE ENGINE — Live Demo")
    print("Maximizing NPG: each document is evaluated for surprise reduction")
    print("=" * 72)
    print()

    engine = NoosphereEngine(
        name="UAF Noosphere v0.1",
        npg_threshold=0.0,
        lambda_consistency=0.5,
    )

    for text, label in DEMO_DOCUMENTS:
        result = engine.evaluate(text, label=label)

        status_marker = "✓ INTEGRATED" if result["integrated"] else "✗ REDUNDANT"

        print(f"[{result['label']}]")
        print(f"  Tokens          : {result['tokens']}")
        print(f"  Baseline S      : {result['baseline_surprisal']:.4f}")
        print(f"  Model S         : {result['model_surprisal']:.4f}")
        print(f"  NPG             : {result['npg']:+.4f}")
        print(f"  UAF Score       : {result['uaf_score']:+.4f}  (scale -3 to +3)")
        print(f"  Free Energy     : {result['free_energy']:.4f}")
        print(f"  Vocab Size      : {result['belief_vocab_size']}")
        print(f"  Status          : {status_marker}")
        print()

    print("=" * 72)
    print("FINAL REPORT")
    print("=" * 72)

    report = engine.report()
    for key, value in report.items():
        print(f"  {key:<35}: {value}")

    print()
    print("Top 20 concepts in collective belief:")
    top = engine.belief.counts.most_common(20)
    for token, count in top:
        bar = "█" * min(count, 40)
        print(f"  {token:<25} {count:3d}  {bar}")

    output_path = "noosphere_state.json"
    engine.save(output_path)
    print()
    print(f"State saved to: {output_path}")
    print("=" * 72)


if __name__ == "__main__":
    run_demo()
