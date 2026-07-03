# Assessment Definitions

## Purpose

This document defines the core assessment terminology used throughout the Formal Architecture of Reasoning Evaluation.

Unless explicitly stated otherwise, every assessment-related term appearing elsewhere in FARE refers to the definitions given here.

---

# Definition 1 — Assessment

An **assessment** is an explicit evaluative representation produced during an evaluation.

An assessment represents the result of applying one or more evaluation criteria to one or more evaluation objects under specified evaluation conditions.

---

# Definition 2 — Assessment Property

An **assessment property** is a formally defined characteristic of an individual assessment.

Assessment properties describe the assessment itself rather than its relationships to other assessments.

Examples include:

- validity;
- justification;
- admissibility;
- completeness;
- robustness;
- consistency;
- confidence.

---

# Definition 3 — Assessment Relationship

An **assessment relationship** is a formally defined relationship between two or more assessments.

Assessment relationships describe how assessments interact without modifying the assessments themselves.

Examples include:

- dependency;
- support;
- conflict;
- refinement.

---

# Definition 4 — Assessment Lifecycle

An **assessment lifecycle** is the sequence of states and transitions through which an assessment evolves during an investigation.

Lifecycle concepts include:

- status;
- history;
- versioning;
- state transitions.

---

# Definition 5 — Assessment Identity

The **identity** of an assessment is the property by which that assessment remains distinguishable from every other assessment.

Identity persists independently of lifecycle state.

---

# Definition 6 — Assessment Version

An **assessment version** is a specific state of an assessment following a substantive modification while preserving assessment identity.

Multiple versions may belong to the same assessment.

---

# Definition 7 — Assessment History

An **assessment history** is the ordered record of lifecycle events affecting an assessment throughout its existence.

History records evolution without altering assessment identity.

---

# Definition 8 — Assessment Status

An **assessment status** is the current lifecycle state of an assessment.

Status represents the present condition of an assessment rather than its historical evolution.

---

# Definition 9 — Assessment System

An **assessment system** is a collection of assessments together with the formally defined relationships that exist among them.

Assessment systems are represented structurally by assessment graphs.

---

# Notes

These definitions establish the canonical assessment vocabulary used throughout FARE.

Relationship theory, lifecycle theory, graph theory, and proofs shall reference these definitions unless explicitly stated otherwise.