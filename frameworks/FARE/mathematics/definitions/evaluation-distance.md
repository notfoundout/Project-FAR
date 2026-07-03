# Mathematical Definition

## Identifier

MDEF-004

---

# Title

Evaluation Distance

---

# Purpose

This document defines evaluation distance within an evaluation space.

Evaluation distance quantifies separation between evaluations using admissible transformation paths and a specified transformation cost model.

---

# Motivation

Evaluation paths establish connectivity.

Distance measures how far apart evaluations are relative to admissible transformations.

Distance serves as the basis for geodesics, neighborhoods, convergence, optimization, and evaluation geometry.

---

# Dependencies

- MDEF-001 — Evaluation Space
- MDEF-002 — Evaluation Transformation
- MDEF-003 — Evaluation Path

---

# Transformation Cost Model

A **transformation cost model** assigns a non-negative cost to every admissible evaluation transformation under consideration.

For every admissible transformation `tau`, `Cost(tau) >= 0`.

The identity transformation has cost `0`.

Transformation costs may depend upon structural modification, dependency modification, support modification, information modification, or other formally defined criteria.

---

# Path Cost

The **cost** of an evaluation path is the sum of the costs of its constituent transformations.

For `P = (tau_1, tau_2, ..., tau_n)`, `Cost(P) = Cost(tau_1) + Cost(tau_2) + ... + Cost(tau_n)`.

The empty path has cost `0`.

---

# Definition

Let `E_1` and `E_2` be evaluations belonging to the same evaluation space.

The **evaluation distance** `d(E_1, E_2)` is defined relative to a specified transformation cost model.

If at least one admissible evaluation path exists from `E_1` to `E_2`, then `d(E_1, E_2)` is the infimum of `Cost(P)` over all admissible paths `P` from `E_1` to `E_2`.

If no admissible path exists from `E_1` to `E_2`, then `d(E_1, E_2) = infinity`.

---

# Infimum Rather Than Minimum

The distance is defined using an infimum rather than a minimum because a minimum-cost path may fail to exist.

A path realizes the distance only when its cost equals the infimum.

---

# Zero Distance

An evaluation possesses zero distance from itself because the empty path and identity transformation have cost `0`.

Whether distinct evaluations may possess zero distance depends upon the adopted transformation cost model and any applicable notion of evaluation equivalence.

---

# Symmetry

Evaluation distance is not assumed to be symmetric.

Whether `d(E_1, E_2) = d(E_2, E_1)` holds depends upon the transformation system and cost model.

---

# Triangle Property

This definition does not assume the triangle inequality.

Whether evaluation distance forms a metric, pseudometric, quasimetric, or another structure remains an open mathematical question.

---

# Structural Properties

This definition guarantees only:

- non-negative distance;
- zero self-distance;
- infinite distance when no admissible path exists;
- infimum-based path-cost interpretation when paths exist.

No additional metric properties are assumed.

---

# Relationship to Geodesics

Evaluation distance specifies the infimum of attainable transformation costs.

Evaluation geodesics are paths that realize that infimum.

A geodesic may fail to exist even when the distance is finite.

---

# Relationship to Evaluation Space

Evaluation distance provides the first quantitative structure on an evaluation space.

It enables shortest-path analysis, neighborhoods, convergence, optimization, and geometric analysis.

---

# Future Investigations

Future investigations should determine:

- whether evaluation distance is a metric;
- whether multiple useful distance functions exist;
- how transformation costs should be assigned;
- whether canonical cost models exist;
- conditions under which distance infima are realized by paths.

---

# Notes

This definition intentionally avoids assuming any existing notion of mathematical distance.

Instead, evaluation distance is defined from admissible transformations and a transformation cost model.

Any stronger mathematical properties must be established by later investigation rather than assumed here.
