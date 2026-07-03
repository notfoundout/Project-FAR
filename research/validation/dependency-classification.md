# Dependency Classification

## Purpose

Determine the kinds of dependency that may exist between concepts within Project FAR.

The objective is to ensure that the foundational dependency graph distinguishes different forms of dependence rather than representing every relationship with a single undifferentiated edge.

---

# Motivation

Previous investigations established a candidate dependency graph connecting the foundational concepts of Project FAR.

However, every edge currently represents only "depends upon."

This investigation determines whether multiple classes of dependency are required.

---

# Central Question

Do all dependencies represent the same relationship?

---

# Candidate Dependency Type 1

Logical Dependency.

Definition:

Concept B cannot be coherently stated without Concept A.

Example:

Comparison cannot occur unless distinguishable entities exist.

Status:

Supported.

---

# Candidate Dependency Type 2

Definitional Dependency.

Definition:

Concept B is defined using Concept A.

Example:

Evaluation may be defined using comparison.

Status:

Supported.

---

# Candidate Dependency Type 3

Ontological Dependency.

Definition:

The existence of Concept B presupposes the existence of Concept A.

Example:

Relations presuppose relata.

Status:

Supported.

---

# Candidate Dependency Type 4

Methodological Dependency.

Definition:

A methodology presupposes another methodological concept.

Example:

Investigation presupposes reasoning.

Status:

Supported.

---

# Candidate Dependency Type 5

Operational Dependency.

Definition:

Execution of Concept B requires Concept A.

Example:

Investigation progression requires operations.

Status:

Supported.

---

# Analysis

Different dependencies answer different questions.

Logical dependency concerns coherence.

Definitional dependency concerns meaning.

Ontological dependency concerns existence.

Methodological dependency concerns investigative structure.

Operational dependency concerns execution.

Treating every dependency as identical obscures important distinctions.

---

# Example

The statement:

Evaluation depends upon comparison.

May simultaneously express:

- a definitional dependency;
- a logical dependency.

The statement:

Investigation depends upon operation.

May express:

- an operational dependency;
- a methodological dependency.

The dependency types are therefore independent of the concepts themselves.

---

# Consequences

The Project FAR dependency graph should distinguish dependency classes.

Each edge should explicitly identify the type of dependency it represents.

This allows individual dependency claims to be independently investigated and validated.

---

# Proposed Notation

L → Logical Dependency

D → Definitional Dependency

O → Ontological Dependency

M → Methodological Dependency

P → Operational Dependency

Multiple dependency types may connect the same pair of concepts.

---

# Decision Criteria

A dependency graph is considered complete only if every edge specifies its dependency class.

---

# Provisional Conclusion

Current evidence supports introducing explicit dependency classes into the foundational architecture of Project FAR.

A single undifferentiated dependency relation is insufficient.

---

# Remaining Questions

Future investigations should determine:

- whether additional dependency classes exist;
- whether dependency classes themselves possess hierarchical relationships;
- whether dependency classes admit formal axiomatization.

---

# Current Status

The investigation remains active.

Dependency classification is provisionally accepted pending further validation.