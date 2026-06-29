# Ω

## Purpose

This document defines Ω, the admissibility structure of FARA.

Ω represents the admissibility status of candidate resolutions for a particular investigation.

It is the primary object through which FARA evaluates the outcomes of structured reasoning.

---

## Definition

Given:

- a reasoning state,
- an investigation,
- an interpretation,
- and a reasoning calculus,

Ω represents the admissibility structure induced by those components.

The formal definition of Ω is maintained in:

`theory/definitions.md`

---

## Candidate Resolutions

Every investigation admits a collection of candidate resolutions.

The complete collection of candidates constitutes the possibility space for that investigation.

Ω classifies those candidates according to their admissibility.

---

## Admissibility

Admissibility is determined by the reasoning calculus operating upon the current reasoning state.

Ω does not perform reasoning.

It represents the result of reasoning.

---

## Properties

An admissibility structure should satisfy the following properties.

### Explicitness

Every admissibility classification is explicitly represented.

---

### Traceability

Every admissibility determination is supported by an explicit chain of reasoning.

---

### Calculus Dependence

Different reasoning calculi may induce different admissibility structures over the same investigation.

---

### Investigation Dependence

Different investigations may induce different admissibility structures over the same representations.

---

## Relationship to Other Components

Ω depends upon:

- the reasoning state,
- the investigation,
- the interpretation,
- and the reasoning calculus.

Changes to any of these components may produce a different admissibility structure.

---

## Research Status

Current research investigates:

- the formal structure of Ω,
- irreducibility,
- admissibility equivalence,
- completeness,
- representation theorems,
- and the relationship between Ω and candidate resolutions.
