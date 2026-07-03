# Support Theory

## Status

Draft

---

# Purpose

Support Theory formalizes how assessments contribute to the justification of other assessments.

The objective is to establish a precise mathematical foundation for support relationships, support sets, and support-based reasoning.

---

# Scope

Support Theory defines:

- support;
- support sets;
- sufficient support;
- necessary support;
- minimal support;
- support closure;
- support preservation.

These concepts provide the foundation for later support proofs.

---

# Primitive Relationship

Support is a primitive assessment relationship.

The remaining concepts defined within this document are derived from Support.

---

# Definition 1 — Supporting Assessment

A **supporting assessment** is an assessment that supports another assessment.

---

# Definition 2 — Support Set

A **support set** is a collection of supporting assessments associated with a particular assessment.

A support set may contain one or more assessments.

---

# Definition 3 — Sufficient Support

A support set is **sufficient** if the supported assessment remains supported whenever every assessment within the support set is accepted.

Adding additional supporting assessments cannot invalidate sufficiency.

---

# Definition 4 — Necessary Support

A supporting assessment is **necessary** if removing it from every sufficient support set causes the supported assessment to lose sufficient support.

Necessary support is therefore indispensable.

---

# Definition 5 — Unnecessary Support

A supporting assessment is **unnecessary** if at least one sufficient support set remains sufficient after its removal.

---

# Definition 6 — Minimal Support Set

A **minimal support set** is a sufficient support set in which no supporting assessment may be removed without destroying sufficiency.

Every member of a minimal support set is therefore necessary relative to that set.

---

# Definition 7 — Support Closure

The **support closure** of an assessment is the smallest set containing:

- the assessment;
- every assessment supporting it;
- every assessment supporting those assessments;

and so on until no additional supporting assessments are introduced.

---

# Definition 8 — Independent Support Sets

Two support sets are **independent** if neither depends upon any assessment contained within the other.

---

# Definition 9 — Redundant Support

Support is **redundant** whenever multiple independent sufficient support sets exist for the same assessment.

---

# Definition 10 — Support Preservation

Support is **preserved** if every sufficient support set remains sufficient after a permitted transformation of the assessment graph.

---

# Fundamental Properties

Support satisfies the following properties.

- Support is directional.
- Support does not imply dependency.
- Dependency does not imply support.
- Support sets may overlap.
- Minimal support sets are not necessarily unique.
- Necessary support is relative to a specified support set unless explicitly stated otherwise.

---

# Relationship to Other Theories

Support Theory depends upon:

- Evaluation Theory
- Assessment Theory
- Relationship Theory
- Graph Theory

Support Theory enables:

- Minimal Supporting Sets
- Support Closure
- Support Preservation
- Redundant Support
- Reliability proofs

---

# Notes

Completion of Support Theory enables restoration of FARE-P005 and future support-based proofs.

Until Support Theory is finalized, all proofs depending upon sufficient support, necessary support, or minimal support remain provisional.