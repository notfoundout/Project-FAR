## Admissibility Structure (Ω)

## Purpose

This document defines the Admissibility Structure (Ω) within the Foundational Architecture of Reasoning Analysis (FARA).

The Admissibility Structure represents the classification of candidates according to a reasoning calculus within the context of an investigation.

It does not perform reasoning or determine how candidates are generated.

---

## Definition

The **Admissibility Structure**, denoted **Ω**, classifies the candidates admitted for consideration within an investigation according to the applicable reasoning calculus.

The canonical definition of the Admissibility Structure is maintained in:

`theory/definitions/definitions.md`

---

## Objective

The purpose of the Admissibility Structure is to explicitly record the admissibility status of every candidate considered during an investigation.

It provides a representation of admissibility rather than a procedure for determining admissibility.

---

## Dependencies

The Admissibility Structure depends upon:

- an investigation,
- a reasoning calculus,
- a reasoning state,
- the candidates admitted for consideration.

Changes to any of these components may produce a different Admissibility Structure.

---

## Admissibility

Admissibility is determined solely by the applicable reasoning calculus operating within the investigation.

The Admissibility Structure records those determinations.

It does not define the reasoning calculus or perform its operations.

---

## Resolution

The Admissibility Structure does not itself produce a resolution.

A resolution is obtained by applying the applicable resolution rule to the classified candidates.

Different investigations may employ different resolution rules.

---

## Properties

An Admissibility Structure should satisfy the following properties.

### Explicitness

Every candidate admitted for consideration possesses an explicitly represented admissibility status.

---

### Traceability

Every admissibility classification can be traced to the reasoning process that produced it.

---

### Calculus Dependence

Different reasoning calculi may classify the same candidates differently.

---

### Investigation Dependence

Different investigations may admit different candidates or employ different criteria, producing different Admissibility Structures.

---

## Relationship to Other Components

The Admissibility Structure depends upon the architectural components defined elsewhere within FARA.

The formal definitions of those components are maintained in:

`theory/definitions/definitions.md`

Detailed descriptions are provided in:

- `reasoning-states.md`
- `transition-signatures.md`

---

## Research Status

Current research investigates:

- the formal properties of the Admissibility Structure,
- admissibility equivalence,
- admissibility preservation,
- completeness,
- minimality,
- and representation theorems. 
