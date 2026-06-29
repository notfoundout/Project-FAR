# Ontology

## Purpose

This document defines the ontological structure of the Foundational Architecture of Reasoning Analysis (FARA).

It distinguishes the primitive concepts of the architecture from concepts derived from them.

Unless explicitly stated otherwise, the terminology used here follows the canonical definitions provided in `theory/definitions.md`.

---

# Primitive Concepts

The current formulation of FARA recognizes the following candidate primitive concepts.

- Investigation
- Representation
- Representational Structure
- Interpretation
- Reasoning Calculus

These concepts are presently regarded as irreducible within the framework.

Whether this collection is both minimal and sufficient remains an active research question.

---

# Derived Concepts

The following concepts are currently regarded as derived from the primitive concepts.

- Reasoning State
- Transition Signature
- Candidate
- Admissibility Structure (Ω)
- Resolution Rule
- Resolution

Additional derived concepts include, but are not limited to:

- Evidence
- Observation
- Hypothesis
- Proof
- Argument
- Explanation
- Model
- Theory
- Prediction
- Counterexample

Every derived concept should ultimately be definable in terms of the primitive concepts.

---

# Primitive and Derived Concepts

Primitive concepts provide the architectural foundation of FARA.

Derived concepts are defined in terms of primitive concepts and other previously established derived concepts.

The objective is to maintain the smallest collection of primitive concepts capable of representing every reasoning process within the intended scope of Project FAR.

---

# Research Status

The ontology remains provisional.

Current research investigates:

- Whether additional primitive concepts are required.
- Whether any current primitive can be reduced.
- Whether the current primitive collection is minimal.
- Whether the architecture is universal within its stated scope.

See:

`research/open-questions.md`

---

# Design Principle

Project FAR prefers reduction over expansion.

A concept should be regarded as primitive only after reasonable attempts to derive it from simpler concepts have failed.

Accordingly, every candidate primitive remains subject to revision as the formal theory develops.
