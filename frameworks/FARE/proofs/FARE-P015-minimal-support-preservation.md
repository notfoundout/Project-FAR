# FARE Proof

## Identifier

FARE-P015

---

# Title

Minimal Support Preservation

---

## Status

Accepted

---

# Objective

Demonstrate that a minimal support set remains minimal under transformations that preserve all support relationships among its members.

---

# Definitions Used

- Support
- Support Set
- Minimal Support Set
- Support Preservation
- Graph Transformation

Canonical terminology is defined in:

- `frameworks/FARE/theory/support-theory.md`
- `frameworks/FARE/definitions/graph-definitions.md`

---

# Dependencies

- Support Theory
- Graph Definitions
- FARE-P005 — Minimal Supporting Sets

---

# Theorem

Let **M** be a minimal support set for an assessment **A**.

If a graph transformation preserves every support relationship involving the members of **M**, then **M** remains a minimal support set for **A** after the transformation.

---

# Proof

Let **M** be a minimal support set supporting assessment **A**.

Assume a graph transformation preserves every support relationship involving the members of **M**.

Since every support relationship is preserved, **M** continues to support **A** after the transformation.

Assume **M** is no longer minimal.

Then there exists a proper subset **M′** of **M** that is sufficient to support **A** after the transformation.

Because the transformation preserved every support relationship within **M**, the same subset **M′** would also have supported **A** before the transformation.

This contradicts the assumption that **M** was minimal before the transformation.

Therefore no proper subset of **M** becomes sufficient after the transformation.

Hence **M** remains a minimal support set.

**Q.E.D.**

---

# Corollary 1

Support-preserving graph transformations cannot introduce redundant members into an existing minimal support set.

---

# Corollary 2

Minimality depends upon changes to support relationships rather than arbitrary graph modifications.

---

# Consequences

Support-preserving transformations may be applied without recomputing minimal support sets.

Graph optimization algorithms may safely transform assessment graphs while preserving support semantics.

Support analysis remains stable under semantics-preserving transformations.

---

# Notes

This theorem applies only to transformations that preserve support relationships.

It does not apply to transformations that add, remove, or modify support edges.

Those cases require recomputation of minimal support sets.