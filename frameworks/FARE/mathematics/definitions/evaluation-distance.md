# Mathematical Definition

## Identifier

MDEF-004

---

# Title

Evaluation Distance

---

# Purpose

This document defines evaluation distance within an evaluation space.

Evaluation distance quantifies the separation between evaluations in terms of admissible transformation paths.

It provides the foundation for the geometry of evaluation spaces.

---

# Motivation

Evaluation paths establish connectivity.

Distance measures how far apart evaluations are.

Distance serves as the basis for:

- geodesics;
- neighborhoods;
- convergence;
- optimization;
- evaluation geometry.

---

# Dependencies

- MDEF-001 — Evaluation Space
- MDEF-002 — Evaluation Transformation
- MDEF-003 — Evaluation Path

---

# Definition

Let `E_1` and `E_2` be evaluations belonging to the same evaluation space.

The **evaluation distance** `d(E_1, E_2)` is a function assigning a non-negative quantity or `infinity` to the ordered pair `(E_1, E_2)`.

The precise value depends upon the adopted transformation cost model.

---

# Transformation Cost

Every admissible evaluation transformation possesses a non-negative cost.

The identity transformation has cost `0`.

Transformation costs may depend upon:

- structural modification;
- dependency modification;
- support modification;
- information modification;

or other formally defined criteria.

---

# Path Cost

The cost of an evaluation path is the sum of the costs of its constituent transformations.

If `P = (tau_1, tau_2, ..., tau_n)`, then `Cost(P) = sum_{i=1}^n Cost(tau_i)`.

The empty path has cost `0`.

---

# Evaluation Distance

If at least one evaluation path exists from `E_1` to `E_2`, their evaluation distance is the infimum of the costs of all admissible paths from `E_1` to `E_2`.

Formally, `d(E_1, E_2) = inf { Cost(P) : P is an admissible path from E_1 to E_2 }`.

If no path exists, `d(E_1, E_2) = infinity`.

A minimum-cost path may or may not exist.

---

# Zero Distance

An evaluation possesses zero distance from itself because the identity path has cost `0`.

Whether distinct evaluations may possess zero distance depends upon the adopted notion of evaluation equivalence.

---

# Symmetry

Evaluation distance is **not assumed** to be symmetric.

Whether `d(E_1, E_2) = d(E_2, E_1)` holds depends upon the transformation system.

---

# Triangle Property

This definition does not assume the triangle inequality.

Whether evaluation distance forms a metric, pseudometric, quasimetric, or another structure remains an open mathematical question.

---

# Structural Properties

This definition guarantees only:

- non-negative transformation costs;
- identity transformation cost `0`;
- path costs given by sums of transformation costs;
- distance defined by the infimum of admissible path costs;
- infinite distance when no admissible path exists.

No additional metric properties are assumed.

---

# Relationship to Evaluation Space

Evaluation distance provides the first quantitative structure on an evaluation space.

It enables:

- shortest-path investigations;
- geodesics as paths realizing distance infima;
- neighborhoods;
- convergence;
- optimization;
- geometric analysis.

---

# Future Investigations

Future investigations should determine:

- whether evaluation distance is a metric;
- whether multiple useful distance functions exist;
- how transformation costs should be assigned;
- whether canonical cost models exist;
- when distance infima are realized by admissible paths.

---

# Notes

This definition intentionally avoids assuming any existing notion of mathematical distance.

Instead, evaluation distance is defined from the admissible transformations of FARE itself.

Any stronger mathematical properties must be established by later investigation rather than assumed here.
