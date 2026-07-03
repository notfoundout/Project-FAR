# Relationship Definitions

## Purpose

This document defines the canonical assessment relationships used throughout the Formal Architecture of Reasoning Evaluation.

Unless explicitly stated otherwise, every relationship appearing elsewhere in FARE refers to the definitions given here.

---

# Definition 1 — Assessment Relationship

An **assessment relationship** is a formally defined association between two or more assessments.

Relationships describe how assessments are connected without modifying the assessments themselves.

---

# Definition 2 — Dependency

An assessment **depends** upon another assessment if the latter is required for its construction, justification, evaluation, or interpretation.

Removing a required dependency alters the evaluability of the dependent assessment.

Dependency is directional.

---

# Definition 3 — Support

An assessment **supports** another assessment if it contributes positively to the justification or confidence of that assessment.

Support does not necessarily imply dependency.

Supporting assessments may strengthen an assessment without being required for it.

Support is directional.

---

# Definition 4 — Conflict

Two assessments are in **conflict** if they cannot both be accepted simultaneously under the same evaluation conditions without producing evaluative incompatibility.

Conflict is symmetric.

Conflict alone does not determine which assessment should be preferred.

---

# Definition 5 — Refinement

An assessment **refines** another assessment if it preserves its evaluative content while increasing precision, completeness, clarity, or explanatory power.

Refinement preserves assessment identity while producing a more informative assessment.

Refinement is directional.

---

# Definition 6 — Relationship Direction

A relationship is **directional** if reversing its endpoints changes its meaning.

Examples include:

- Dependency
- Support
- Refinement

Conflict is not directional.

---

# Definition 7 — Relationship Type

A **relationship type** identifies the semantic role of a relationship independently of its graphical representation.

Relationship types determine how connected assessments interact during evaluation.

---

# Definition 8 — Relationship Composition

A **relationship composition** is the combination of two or more assessment relationships to produce a derived relationship.

Relationship composition is valid only when explicitly defined by FARE.

---

# Definition 9 — Relationship Consistency

A collection of assessment relationships is **relationship consistent** if the relationships do not violate the formal semantics of their respective relationship types.

Relationship consistency concerns relationships themselves rather than the truth or correctness of the connected assessments.

---

# Definition 10 — Relationship Graph

A **relationship graph** is the subgraph of an assessment graph induced by one or more specified relationship types.

Examples include:

- dependency graphs;
- support graphs;
- conflict graphs;
- refinement graphs.

---

# Notes

These definitions establish the canonical relationship vocabulary used throughout FARE.

Investigations, graph representations, proofs, and future extensions shall reference these definitions unless explicitly stated otherwise.

Relationship definitions specify semantic meaning.

Graph definitions specify structural representation.

The two are intentionally distinct.