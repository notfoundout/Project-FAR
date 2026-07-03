# Mathematical Definition

## Identifier

MDEF-002

---

# Title

Evaluation Transformation

---

# Purpose

This document defines evaluation transformations, the primitive morphisms of evaluation spaces.

Evaluation transformations describe formally permitted changes between evaluations.

---

# Motivation

Reasoning rarely remains static.

Evaluations evolve through:

- refinement;
- revision;
- normalization;
- simplification;
- extension.

These changes are represented mathematically as evaluation transformations.

---

# Dependencies

- MDEF-001 — Evaluation Space

---

# Definition

An **evaluation transformation** is an admissible operation that maps one evaluation to another within the same evaluation space.

A transformation may be written as `tau: E_1 -> E_2`, where:

- `E_1` and `E_2` belong to the same evaluation space;
- `tau` satisfies every admissibility requirement imposed by FARE.

---

# Domain

The **domain** of a transformation is the evaluation upon which the transformation operates.

For `tau: E_1 -> E_2`, the domain is `E_1`.

---

# Codomain

The **codomain** of a transformation is the evaluation produced by the transformation.

For `tau: E_1 -> E_2`, the codomain is `E_2`.

---

# Identity Transformation

Every evaluation possesses an identity transformation `id_E: E -> E` that leaves the evaluation unchanged.

---

# Composition

If `tau_1: E_1 -> E_2` and `tau_2: E_2 -> E_3`, then their composition `tau_2 ∘ tau_1: E_1 -> E_3` is an evaluation transformation whenever the composed operation is admissible.

---

# Invertibility

A transformation `tau` is **invertible** if there exists another admissible transformation `tau^-1` such that:

- `tau^-1 ∘ tau = id`;
- `tau ∘ tau^-1 = id`.

Not every admissible transformation is invertible.

---

# Classes of Transformations

Possible transformation classes include:

- refinement;
- revision;
- normalization;
- simplification;
- decomposition;
- composition;
- extension.

Additional classes may be introduced through future investigations.

---

# Structural Properties

This definition does not assume that transformations:

- preserve equivalence;
- preserve distance;
- preserve support;
- preserve dependency;
- preserve canonical form;
- possess a cost.

Such properties must be established independently.

---

# Equality

Two transformations are equal if they possess identical:

- domains;
- codomains;
- transformation behavior.

---

# Relationship to Evaluation Space

Evaluation transformations define the connections between evaluations within an evaluation space.

Together:

- evaluations;
- transformations;

form the foundational mathematical structure upon which the geometry of FARE is constructed.

---

# Notes

Evaluation transformations are primitive mathematical objects.

Whether they preserve meaning, equivalence, support, distance, or any other property is determined by additional mathematical definitions rather than by this definition itself.

Future work may classify transformations into families according to the properties they preserve.
