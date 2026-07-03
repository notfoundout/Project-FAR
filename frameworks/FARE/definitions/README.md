# FARE Canonical Definitions

## Purpose

This directory contains the canonical definitions used throughout the Formal Architecture of Reasoning Evaluation.

These documents establish the official meaning of every foundational term appearing within FARE.

Unless explicitly stated otherwise, all investigations, proofs, graphs, architectures, and future extensions shall use these definitions.

---

# Definition Hierarchy

The definition system is organized from the most foundational concepts to the most specialized.

```text
Evaluation Definitions
        │
        ▼
Assessment Definitions
        │
        ▼
Relationship Definitions
        │
        ▼
Graph Definitions
```

Higher-level definitions may depend upon lower-level definitions.

Lower-level definitions shall never depend upon higher-level definitions.

---

# Canonical Definition Rule

Every formal concept shall possess exactly one canonical definition.

Canonical definitions shall not be duplicated elsewhere within FARE.

Documents requiring a definition shall reference the canonical definition rather than redefining the concept.

---

# Definition Requirements

Every definition shall satisfy the following requirements.

- Introduce exactly one concept.
- Be non-circular.
- Depend only upon previously established concepts.
- Contain only necessary conditions.
- Contain all necessary conditions.
- Remain stable throughout the framework.

---

# Definition Categories

## Evaluation

Defines the evaluation process.

Document

- evaluation-definitions.md

---

## Assessment

Defines the products of evaluation.

Document

- assessment-definitions.md

---

## Relationships

Defines interactions between assessments.

Document

- relationship-definitions.md

---

## Graph Theory

Defines the structural representation of assessment systems.

Document

- graph-definitions.md

---

# Definition Dependencies

```text
Evaluation

↓

Assessment

↓

Relationships

↓

Graphs
```

Dependency direction shall always follow this ordering.

---

# Definition Governance

Definitions shall be modified only when:

- inconsistency is identified;
- redundancy is removed;
- precision is improved;
- architectural changes require revision.

Definitions shall not change merely to accommodate individual investigations or proofs.

Instead, investigations and proofs shall be updated to remain consistent with canonical definitions.

---

# Relationship to Other Documents

Investigations discover concepts.

Definitions formalize concepts.

Proofs establish consequences of definitions.

Audits verify consistency among all three.

---

# Notes

The documents within this directory constitute the semantic foundation of FARE.

Every future extension of the framework shall preserve compatibility with these canonical definitions unless an explicit architectural revision supersedes them.