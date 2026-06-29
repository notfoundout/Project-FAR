# Failed Approaches

## Purpose

This document records approaches that were considered during the development of Project FAR but were ultimately rejected.

Recording failed approaches preserves design history, prevents repeated investigation of previously rejected ideas, and documents the reasoning behind architectural decisions.

A rejected approach may be reconsidered if new theoretical or empirical evidence justifies doing so.

---

# Approach 1

## Name

Possibility Space as an Architectural Concept

---

## Description

Represent all possible reasoning outcomes using an explicit Possibility Space.

---

## Reason for Rejection

The concept was found to be reducible to the collection of candidates admitted for consideration within an investigation.

Maintaining Possibility Space as a separate architectural concept increased complexity without increasing expressive power.

---

## Outcome

Removed from the core architecture.

---

# Approach 2

## Name

Candidate Resolution

---

## Description

Treat candidate resolutions as a primitive architectural concept.

---

## Reason for Rejection

The concept introduced an unnecessary dependency between candidates and resolutions.

Candidates exist before admissibility is determined and before any resolution is selected.

---

## Outcome

Replaced by the more general concept of Candidate.

---

# Approach 3

## Name

Distributed Definitions

---

## Description

Maintain independent definitions throughout multiple documents.

---

## Reason for Rejection

Distributed definitions created redundancy, increased maintenance effort, and risked inconsistencies.

---

## Outcome

Adopted `theory/definitions.md` as the single canonical source for formal terminology.

---

# Approach 4

## Name

Mixed Architectural and Methodological Documents

---

## Description

Allow architecture, methodology, operations, and theory to be defined within the same documents.

---

## Reason for Rejection

The resulting structure blurred responsibilities, increased duplication, and complicated dependency management.

---

## Outcome

Separated the repository into:

- FARA
- FAR
- FARO
- Theory

Each component now has a distinct responsibility.

---

# Approach 5

## Name

Introducing New Concepts Before Demonstrating Necessity

---

## Description

Expand the architecture whenever a new reasoning framework appears to require an additional concept.

---

## Reason for Rejection

This approach conflicts with the principle of minimality.

New concepts should be introduced only after demonstrating that existing concepts cannot adequately represent the required structure.

---

## Outcome

Adopted a reduction-first methodology.

Architectural expansion now requires explicit theoretical justification.

---

# Lessons Learned

Several recurring principles have emerged during the development of Project FAR.

- Prefer reduction before expansion.
- Prefer derivation before introducing new primitives.
- Maintain a single canonical definition for each concept.
- Separate architecture, methodology, operations, and theory.
- Minimize dependencies and avoid circularity.
- Introduce new concepts only when they increase expressive power.
