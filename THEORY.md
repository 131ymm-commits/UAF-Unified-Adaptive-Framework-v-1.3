# UAF Theory

## 1. Core intuition

UAF begins from a simple observation:

Stable systems behave as if they maintain boundaries, update states, and reduce prediction error.

This does not mean every system is conscious.  
It means every stable system has a structure that can be described as a predictive constraint.

A thermostat, a cell, a brain, a language, and a scientific community are not the same thing.  
But each can be modeled as a system that maintains coherence by reducing expected surprise.

---

## 2. Basic unit

A UAF-system is defined as:

\[
S_k = (Q_k, P_k, B_k, \Delta_k, U_k)
\]

where:

- \(Q_k\): current belief/state distribution,
- \(P_k\): generative model or prior,
- \(B_k\): boundary of the system,
- \(\Delta_k\): prediction horizon,
- \(U_k\): update operator.

The basic cycle is:

\[
Q_k(t)
\xrightarrow{\text{predict}}
\hat{o}_{t+\Delta}
\xrightarrow{\text{observe}}
o_{t+\Delta}
\xrightarrow{\text{error}}
\mathcal{S}_k
\xrightarrow{\text{update}}
Q_k(t+\Delta)
\]

---

## 3. Surprise

\[
\mathcal{S}_k(t)
=
-\ln P_k(o_t\mid Q_k)
\]

Surprise is not emotion.  
It is negative log-likelihood.

---

## 4. Free energy

Variational free energy:

\[
\mathcal{F}[Q]
=
\mathbb{E}_{Q(s)}
[\ln Q(s)-\ln P(o,s)]
\]

Equivalently:

\[
\mathcal{F}[Q]
=
D_{\mathrm{KL}}(Q(s)\|P(s\mid o))
-
\ln P(o)
\]

Therefore:

\[
\mathcal{F}[Q] \ge -\ln P(o)
\]

Free energy is an upper bound on surprise.

---

## 5. Active inference

Agents can reduce surprise in two ways:

1. update beliefs to match observations,
2. act to make future observations match beliefs/preferences.

Expected free energy:

\[
G(\pi)
=
D_{\mathrm{KL}}(Q(\tilde{o}\mid\pi)\|\tilde{P}(\tilde{o}))
+
\mathbb{E}_{Q(\tilde{s}\mid\pi)}
H[P(\tilde{o}\mid \tilde{s})]
\]

Policy selection:

\[
\pi^*
=
\arg\min_\pi G(\pi)
\]

---

## 6. Hierarchy

A higher level receives lower-level errors as signals.

\[
\mathrm{input}_{k+1}
=
\mathcal{S}_k
\]

A lower level receives higher-level predictions as priors.

\[
Q_k
\leftarrow
Q_k
\;\text{constrained by}\;
P_{k+1}
\]

Thus hierarchy is not a ladder of substances.  
It is a ladder of prediction horizons.

---

## 7. Truth

Truth is not only correspondence.  
Truth is stable predictive compression.

A model \(M\) is better than baseline \(B\) on data \(D\) if:

\[
L(M,D) < L(B,D)
\]

Normalized predictive gain:

\[
\mathrm{NPG}(M;D,B)
=
\frac{L(B,D)-L(M,D)}{L(B,D)+\epsilon}
\]

A true theory is one that remains in an attractor of positive NPG under perturbation.

---

## 8. Knowledge compression

UAF is itself judged by the same criterion:

\[
\mathrm{NPG}_{UAF} > 0
\]

If it does not reduce explanatory cost, it fails.
