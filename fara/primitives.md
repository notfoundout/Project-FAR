# Candidate Primitives

## Introduction

A central objective of FARA is to identify the smallest collection of concepts required to represent every structured, explicit, auditable reasoning process within its stated scope.

Every proposed primitive is repeatedly subjected to attempted elimination.

A primitive remains only if it cannot be derived from simpler assumptions without reducing expressive power.

The following primitives represent the current state of the research.

---

# Primitive 1 — Representational Structure

## Definition

A representational structure specifies the class of distinguishable representations available within a reasoning system.

Representations may take many forms, including:

- symbolic expressions,
- graphs,
- logical formulas,
- typed objects,
- mathematical structures,
- or equivalent formal representations.

FARA does not privilege any particular representation.

The only requirement is that representations be explicit and distinguishable.

---

## Motivation

Without distinguishable representations:

- nothing can be compared,
- nothing can be transformed,
- nothing can be audited.

Every reasoning framework examined to date possesses some representational structure.

---

## Current Status

Candidate primitive.

No successful reduction has yet been identified.

---

# Primitive 2 — Interpretation

## Definition

Interpretation assigns meaning to representations.

Representations without interpretation remain syntactic objects.

Interpretation connects representations to whatever they are intended to denote.

---

## Motivation

Two identical symbolic structures may possess different meanings.

Meaning therefore cannot generally be derived from syntax alone.

---

## Current Status

Candidate primitive.

No successful reduction has yet been identified.

---

# Primitive 3 — Investigation Question

## Definition

The investigation question specifies the objective of the reasoning process.

It determines:

- relevance,
- explanatory target,
- termination conditions,
- and evaluation criteria.

---

## Motivation

Without an investigation question, there is no principled distinction between relevant and irrelevant reasoning.

Every explicit investigation is directed toward some objective.

---

## Current Status

Candidate primitive.

Repeated elimination attempts have not succeeded.

---

# Primitive 4 — Reasoning Calculus

## Definition

A reasoning calculus specifies the rules governing evaluation, transformation, or inference within a reasoning process.

Examples include:

- deductive logic,
- Bayesian inference,
- optimization procedures,
- legal reasoning,
- scientific methodologies.

FARA remains neutral with respect to the particular calculus employed.

---

## Motivation

The same reasoning state may admit different conclusions under different reasoning calculi.

Accordingly, the reasoning calculus cannot presently be derived from the remaining primitives.

---

## Current Status

Candidate primitive.

No successful reduction has yet been demonstrated.

---

# Independence

At present, no proof exists that these four primitives are mutually independent.

Likewise, no successful derivation of any primitive from the remaining three has been established.

Accordingly, the current architecture should be regarded as provisional.

The primary objective of future work is either:

- to prove the independence of the remaining primitives,

or

- to reduce the architecture further through successful elimination.

---

# Research Principle

Every surviving primitive should be regarded as temporary.

A primitive remains only until either:

1. a valid reduction is discovered,

or

2. an independence proof demonstrates that no such reduction exists.
