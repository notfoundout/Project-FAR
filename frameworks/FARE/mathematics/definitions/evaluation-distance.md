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

Let

$begin:math:display$
E\_1\,E\_2
$end:math:display$

be evaluations belonging to the same evaluation space.

The **evaluation distance**

$begin:math:display$
d\(E\_1\,E\_2\)
$end:math:display$

is a function assigning a non-negative quantity to the pair

$begin:math:display$
\(E\_1\,E\_2\)\.
$end:math:display$

The precise value depends upon the adopted transformation cost model.

---

# Transformation Cost

Every admissible evaluation transformation possesses a non-negative cost.

Transformation costs may depend upon:

- structural modification;
- dependency modification;
- support modification;
- information modification;

or other formally defined criteria.

---

# Path Cost

The cost of an evaluation path is the sum of the costs of its constituent transformations.

If

$begin:math:display$
P\=\(\\tau\_1\,\\tau\_2\,\\ldots\,\\tau\_n\)\,
$end:math:display$

then

$begin:math:display$
Cost\(P\)
\=
\\sum\_\{i\=1\}\^\{n\}
Cost\(\\tau\_i\)\.
$end:math:display$

---

# Evaluation Distance

If at least one evaluation path exists between

$begin:math:display$
E\_1
$end:math:display$

and

$begin:math:display$
E\_2\,
$end:math:display$

their evaluation distance is the minimum cost among all admissible paths connecting them.

Formally,

$begin:math:display$
d\(E\_1\,E\_2\)
\=
\\min
\\\{
Cost\(P\)
\:
P
\\text\{ connects \}
E\_1
\\text\{ to \}
E\_2
\\\}\.
$end:math:display$

If no path exists,

$begin:math:display$
d\(E\_1\,E\_2\)
\=
\\infty\.
$end:math:display$

---

# Zero Distance

An evaluation possesses zero distance from itself.

Whether distinct evaluations may possess zero distance depends upon the adopted notion of evaluation equivalence.

---

# Symmetry

Evaluation distance is **not assumed** to be symmetric.

Whether

$begin:math:display$
d\(E\_1\,E\_2\)
\=
d\(E\_2\,E\_1\)
$end:math:display$

holds depends upon the transformation system.

---

# Triangle Property

This definition does not assume the triangle inequality.

Whether evaluation distance forms a metric, pseudometric, quasimetric, or another structure remains an open mathematical question.

---

# Structural Properties

This definition guarantees only:

- non-negative distance;
- zero self-distance;
- minimal-path interpretation when paths exist.

No additional metric properties are assumed.

---

# Relationship to Evaluation Space

Evaluation distance provides the first quantitative structure on an evaluation space.

It enables:

- shortest paths;
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
- whether canonical cost models exist.

---

# Notes

This definition intentionally avoids assuming any existing notion of mathematical distance.

Instead, evaluation distance is defined from the admissible transformations of FARE itself.

Any stronger mathematical properties must be established by later investigation rather than assumed here.