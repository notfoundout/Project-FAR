# Mathematical Definition

## Identifier

MDEF-010

---

# Title

Evaluation Invariant

---

# Purpose

This document defines evaluation invariants within an evaluation space.

Evaluation invariants identify properties or quantities that remain unchanged under specified admissible evaluation transformations.

They provide the mathematical foundation for classification, equivalence analysis, preservation results, and structural comparison.

---

# Motivation

Evaluation transformations may alter evaluations while preserving some features.

Determining which features remain unchanged is essential for understanding the structure of evaluation spaces.

Invariants provide stable information across transformation behavior.

---

# Dependencies

- MDEF-001 — Evaluation Space
- MDEF-002 — Evaluation Transformation

---

# Definition

Let `E` be an evaluation space and let `C` be a specified class of admissible evaluation transformations in `E`.

An **evaluation invariant** relative to `C` is a property, value, or assignment `I` such that for every transformation `tau: E_1 -> E_2` belonging to `C`, `I(E_1) = I(E_2)` whenever both sides are defined.

---

# Invariant Domain

The **invariant domain** of an evaluation invariant is the collection of evaluations for which the invariant is defined.

This definition does not require every invariant to be defined on every evaluation.

---

# Transformation Class

The transformation class specifies which admissible transformations must preserve the invariant.

Changing the transformation class may change whether a property is invariant.

---

# Preserved Quantity

A **preserved quantity** is a value assigned to evaluations that remains unchanged under the specified transformation class.

Not every invariant must be numeric.

---

# Preserved Property

A **preserved property** is a predicate on evaluations whose truth value remains unchanged under the specified transformation class.

---

# Invariant Equivalence

Two evaluations are **invariant-equivalent** with respect to an invariant if the invariant assigns them the same value or property status.

Invariant equivalence need not coincide with evaluation equivalence.

---

# Complete Invariant

An invariant is **complete** for a specified comparison problem if equality of the invariant is sufficient to resolve that comparison problem.

Completeness is not assumed by this definition.

---

# Structural Properties

This definition does not assume:

- existence of nontrivial invariants;
- uniqueness;
- completeness;
- computability;
- preservation under every transformation;
- correspondence with evaluation equivalence.

Each property requires independent mathematical investigation.

---

# Relationship to Evaluation Transformations

Evaluation invariants are defined relative to admissible transformation behavior.

A property may be invariant under one class of transformations and fail to be invariant under another.

---

# Mathematical Role

Evaluation invariants provide the foundation for:

- classification of evaluations;
- preservation theorems;
- equivalence analysis;
- obstruction arguments;
- structural comparison of evaluation spaces.

---

# Future Investigations

Future investigations should determine:

- whether nontrivial evaluation invariants exist;
- which invariants are complete for important comparison problems;
- how invariants interact with distance, convergence, and completion;
- whether canonical invariants exist;
- whether invariants can be computed for finite evaluation spaces.

---

# Notes

This definition introduces invariance only relative to a specified transformation class.

It intentionally avoids assuming that any particular feature is preserved by all admissible transformations.

Future work may identify fundamental invariants of FARE evaluation spaces.
