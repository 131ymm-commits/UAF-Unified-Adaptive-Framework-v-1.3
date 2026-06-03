# Formal Core

This file contains the minimum mathematical kernel of UAF.

---

## 1. State space

Each level \(k\) has a state space:

\[
\mathcal{X}_k
\]

and observations:

\[
\mathcal{O}_k
\]

A model is a probability distribution:

\[
Q_k(s_k)
\]

with generative structure:

\[
P_k(o_k, s_k)
=
P_k(o_k\mid s_k)P_k(s_k)
\]

---

## 2. Surprise

\[
\mathcal{S}_k(o)
=
-\ln P_k(o)
\]

---

## 3. Variational free energy

\[
\mathcal{F}_k[Q_k]
=
\mathbb{E}_{Q_k(s)}
[
\ln Q_k(s)
-
\ln P_k(o,s)
]
\]

Decomposition:

\[
\mathcal{F}_k
=
\underbrace{
\mathbb{E}_{Q_k}[-\ln P_k(o\mid s)]
}_{\text{inaccuracy}}
+
\underbrace{
D_{\mathrm{KL}}(Q_k(s)\|P_k(s))
}_{\text{complexity}}
\]

---

## 4. Multi-level objective

\[
\mathcal{F}_{total}
=
\sum_k
\mathcal{F}_k
+
\sum_k
\lambda_k
D_{\mathrm{KL}}
(
\Pi_{k\to k+1}Q_k
\|
Q_{k+1}
)
+
\sum_k
\gamma_k\mathcal{T}_k
\]

where:

- \(\Pi_{k\to k+1}\) is a representation map,
- \(\mathcal{T}_k\) is topological complexity,
- \(\lambda_k,\gamma_k\) are coupling weights.

---

## 5. Topological complexity

A possible topological penalty:

\[
\mathcal{T}_k
=
\sum_i
\sum_{\gamma\in H_i}
\epsilon(\gamma)
\]

where:

\[
\epsilon(\gamma)
=
t_{\mathrm{death}}(\gamma)
-
t_{\mathrm{birth}}(\gamma)
\]

This connects UAF to persistent homology.

---

## 6. Active inference

Expected free energy:

\[
G(\pi)
=
D_{\mathrm{KL}}
(
Q(\tilde{o}\mid\pi)
\|
\tilde{P}(\tilde{o})
)
+
\mathbb{E}_{Q(\tilde{s}\mid\pi)}
H[P(\tilde{o}\mid \tilde{s})]
\]

Policy:

\[
\pi^*
=
\arg\min_\pi G(\pi)
\]

---

## 7. Predictive gain

Given model \(M\), baseline \(B\), data \(D\):

\[
\mathrm{NPG}
=
\frac{L(B,D)-L(M,D)}{L(B,D)+\epsilon}
\]

Possible losses:

- negative log-likelihood,
- Brier score,
- cross-entropy,
- MDL description length.

---

## 8. Attractor truth

Let \(Q(t)\) evolve by:

\[
\dot{Q}
=
-\nabla_Q \mathcal{F}
+
\eta(t)
\]

A truth-attractor is:

\[
\mathcal{A}
=
\{Q:
\dot{Q}\approx 0,
\;
Q \text{ stable under perturbation}
\}
\]

Truth is not merely a proposition.  
Truth is stable predictive compression.
