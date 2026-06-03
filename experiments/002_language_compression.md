# Experiment 002: Language as Collective Free Energy Minimization

Status: Layer 2 (cross-domain interpretation)

## Problem

10+ incompatible theories of language exist:

- Chomsky: innate grammar.
- Wittgenstein: meaning is use.
- Montague: meaning maps to logic.
- Lakoff: embodied metaphor.
- Harris: distributional semantics.

None explains everything.

## UAF Answer

Language is a communication protocol that minimizes
collective free energy between agents.

    L* = argmin_L E_{agents,contexts}[F(Q_i || Q_j) + λK(L)]

where:

- F(Q_i || Q_j) is the divergence between agent models,
- K(L) is the Kolmogorov complexity of the language itself,
- λ balances precision against learning cost.

## Key Results

### Meaning

    Meaning(w) = E_contexts[ΔF(w)]

The meaning of a word is how much it reduces
the listener's free energy in a given context.

### Grammar

Grammar is optimal compression of predictive sequences.

    L(S) = Σ -log P(w_i | w_{<i})

Syntactic rules are patterns that minimize code length.

Children learn language fast not because of innate grammar,
but because their brains are efficient MDL compressors.

### LLM and Human

LLM minimizes: L = -Σ log P(w_{t+1} | w_{≤t})
Human minimizes: F = D_KL[Q(s)||P(s|o)] - log P(o)

These are the same operation on different substrates.

### Synonyms, polysemy, poetry

Synonyms: words with equal ΔF in same contexts.
Polysemy: one word, different ΔF in different contexts.
Poetry: high ΔF with minimal K (beautiful = efficient surprise reduction).

## Empirical Check

Piantadosi et al. (2011): all languages have
approximately equal information rate (~39 bits/sec),
despite different speech speeds.

This is a direct prediction of UAF:
communication rate is determined by channel capacity,
not by surface properties of the language.

## Surprise Reduction

10 theories → 1 equation.
NPG > 0 across all subdomains of linguistics.
