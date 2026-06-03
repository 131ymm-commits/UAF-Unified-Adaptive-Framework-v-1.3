# Experiment 001: Spin as Topology of Prediction Manifold

Status: Layer 3 (physics reinterpretation)

## Problem

Standard explanation says spin is "intrinsic angular momentum".
But electron is a point particle. Nothing rotates.
What is spin?

## UAF Answer

Spin is a topological invariant of the prediction manifold.

The quantum belief state for spin-1/2 lives in:

    CP^1 ≅ S^2 (Bloch sphere)

Transformations are governed by SU(2), the double cover of SO(3).

Key fact: a 2π rotation changes the sign of the state.
Only 4π returns it to the original.

This is not a property of the particle.
This is a property of the space in which the particle predicts.

## Core Equations

Spin-1/2 state:

    |ψ⟩ = cos(θ/2)|↑⟩ + e^{iφ}sin(θ/2)|↓⟩

The factor θ/2 (not θ) is the topological trace of double covering.

Pauli matrices are precision-switching operators:

    σ_z measures which hypothesis dominates.
    σ_x flips belief between hypotheses.
    σ_y flips with phase shift.

Anti-commutativity {σ_i, σ_j} = 2δ_{ij} is the algebraic form
of the information bound: measuring precision on one axis
determines uncertainty on the other two.

## Consequences

### Spin-statistics theorem

Fermions (half-integer spin): antisymmetric belief exchange.
Two fermions cannot share identical belief states.
This is not a rule. It is topological impossibility:
the corresponding point does not exist in the manifold.

    |φ⟩|φ⟩ - |φ⟩|φ⟩ = 0

Bosons (integer spin): symmetric belief exchange.
Multiple bosons can share one state (Bose-Einstein condensate).

### Periodic table

The entire periodic table is a topological map
of electron belief manifold under Coulomb potential.

### g-factor

    μ = g(e/2m)S

g ≈ 2 because spinor is a double covering.
The factor 2 in g is the topological fingerprint of π₁(SU(2)) = Z₂.

### Hierarchy of matter

Tensor products of CP^1 create richer topology at each level:

    Single electron: CP^1
    Two electrons: CP^1 ⊗ CP^1 ⊂ CP^3
    Atom: ⊗_i CP^1_i / symmetry
    Molecule: tensor product + bond constraints
    Crystal: product + topological defects

Complexity accumulates through tensor products.
Spin of the electron is still "audible" in the topology of a crystal.

## Predictions

1. All matter types correspond to SU(2) representations.
   No other types exist.
2. Stability requires β₁ > 0 (nontrivial first loop).
3. Life requires spin-1/2 for electrons (antisymmetry → periodic table → chemistry).
4. ℏ is the scale at which prediction manifold topology becomes physically visible.

## Surprise Reduction

Standard: spin is "intrinsic rotation" (misleading metaphor).
UAF: spin is topology of prediction space (precise, falsifiable).

NPG > 0: removes metaphor, connects to matter classification,
explains periodic table, predicts g-factor origin.
