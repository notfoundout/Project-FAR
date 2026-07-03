# FARE Proof

## Identifier

FARE-P018

---

# Title

Support Propagation Limits

---

## Status

Accepted

---

# Objective

Demonstrate that support propagation is constrained by dependency structure and evaluation conditions.

---

# Definitions Used

- Assessment
- Dependency
- Support
- Evaluation Condition
- Support Set

Canonical terminology is defined in:

- `frameworks/FARE/definitions/evaluation-definitions.md`
- `frameworks/FARE/definitions/relationship-definitions.md`
- `frameworks/FARE/theory/support-theory.md`

---

# Dependencies

- Evaluation Definitions
- Relationship Definitions
- Support Theory
- FARE-P017 — Dependency Support Propagation

---

# Theorem

Support propagates through dependency relationships only while the dependency remains valid under the relevant evaluation conditions.

---

# Proof

Assume assessment **A** depends upon assessment **B**.

Assume **B** receives support from assessment **C**.

By FARE-P017, the support provided by **C** contributes indirectly to the support of **A**.

Now suppose the dependency between **A** and **B** is removed or becomes invalid under the applicable evaluation conditions.

Since **A** no longer depends upon **B**, the justification contributed through **B** is no longer required for evaluating **A**.

Therefore the indirect support previously supplied by **C** no longer propagates to **A** through that dependency.

Likewise, if the evaluation conditions change such that the dependency is no longer valid, propagation ceases.

Therefore support propagation is constrained by valid dependency relationships under the applicable evaluation conditions.

**Q.E.D.**

---

# Corollary 1

Support propagation is conditional rather than absolute.

---

# Corollary 2

Changes to dependency relationships may alter propagated support without changing direct support.

---

# Corollary 3

Support graphs should be recomputed whenever dependency relationships change.

---

# Consequences

Support propagation depends upon the current dependency graph.

Changes to evaluation conditions may invalidate previously propagated support.

Support analysis must account for dependency validity throughout an investigation.

---

# Notes

This theorem establishes a necessary condition for support propagation.

It does not establish sufficient conditions for overall assessment acceptance.

Acceptance remains a separate concept within FARE.