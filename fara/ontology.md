# Ontology

## Purpose

This document defines the ontological structure of the Foundational Architecture of Reasoning Analysis (FARA).

It distinguishes the primitive concepts of the architecture from concepts that are derived from them.

Unless explicitly stated otherwise, the terminology used here follows the canonical definitions provided in `theory/definitions.md`.

---

# Primitive Concepts

The following concepts are treated as primitive within the current version of FARA.

- Investigation
- Representation
- Representational Structure
- Interpretation
- Reasoning Calculus
- Reasoning State
- Transition Signature
- Candidate
- Admissibility Structure (Ω)
- Resolution Rule
- Resolution

Primitive concepts are not currently defined in terms of other architectural concepts.

Whether this collection is minimal or complete remains an open research question.

---

# Derived Concepts

The following concepts are currently regarded as derived from the primitive concepts.

Examples include:

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

Additional derived concepts may be introduced provided they can be defined using the primitive concepts.

---

# Primitive and Derived Concepts

Primitive concepts provide the architectural foundation of FARA.

Derived concepts are defined in terms of the primitive concepts and their relationships.

The objective is to maintain a minimal ontology while preserving the expressive power required to represent reasoning across multiple domains.

---

# Research Status

The current ontology is regarded as provisional.

Ongoing research seeks to determine:

- Whether any primitive concepts can be derived.
- Whether additional primitive concepts are required.
- Whether the current ontology is minimal.
- Whether the ontology is universal within the scope of Project FAR.

These questions are tracked in:

`research/open-questions.md`

---

# Design Principle

New primitive concepts should be introduced only after demonstrating that existing primitive concepts cannot adequately represent the required architectural structure.

Whenever possible, Project FAR prefers reduction over expansion.
