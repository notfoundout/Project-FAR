# Admissibility Structure (Ω)

## Purpose

This document specifies the architectural role of the Admissibility Structure (Ω) within the Foundational Architecture of Reasoning Analysis (FARA).

The Admissibility Structure records the admissibility classifications of candidates within an investigation.

The canonical definitions of all terminology used here are maintained in:

`theory/definitions/definitions.md`

This document specifies the architectural role of Ω rather than redefining the underlying concepts.

---

## Overview

Within an investigation, candidates are evaluated according to the applicable reasoning calculus.

Admissibility is the property of satisfying the admissibility criteria established by that reasoning calculus.

An admissibility classification is the explicit assignment of admissibility status to a candidate.

The Admissibility Structure (Ω) represents those admissibility classifications.

Ω is distinct from:

- the reasoning calculus that determines admissibility;
- the admissibility criteria;
- the candidates being classified;
- the reasoning process that produces the classifications;
- the resolution rule;
- the resolution execution;
- the resulting resolution.

---

## Definition

The **Admissibility Structure**, denoted **Ω**, is the representation of the admissibility classifications of candidates within an investigation.

Ω represents and records those classifications without determining them.

Ω does not:

- perform reasoning;
- determine admissibility;
- generate candidates;
- perform candidate selection;
- produce resolutions.

---

## Dependencies

Ω exists relative to:

- an investigation;
- a set of candidates;
- an applicable reasoning calculus;
- one or more admissibility classifications.

Changes to any of these may produce a different Admissibility Structure.

---

## Admissibility

Admissibility is determined solely by the applicable reasoning calculus within an investigation.

Ω records the resulting admissibility classifications.

Ω neither defines nor executes the reasoning calculus.

---

## Candidates

A candidate is an explicitly represented object admitted for consideration within an investigation.

Candidate status does not imply admissibility.

The admissibility classifications available within Ω are determined entirely by the applicable reasoning calculus.

---

## Resolution

Ω does not itself produce a resolution.

A resolution is produced by applying a resolution rule to Ω through a resolution execution.

Different investigations may employ different resolution rules.

A resolution is distinct from:

- Ω;
- the resolution rule;
- the resolution execution;
- the candidate set prior to selection.

---

## Properties

An Admissibility Structure should satisfy the following properties.

### Explicitness

Every candidate admitted for consideration should possess either an explicit admissibility classification or an explicitly represented unresolved status.

---

### Traceability

Every admissibility classification should be traceable to:

- the candidate classified;
- the applicable investigation;
- the applicable reasoning calculus;
- the reasoning process or reasoning trace that produced the classification.

---

### Calculus Dependence

Different reasoning calculi may classify identical candidate sets differently.

Admissibility classifications are therefore always relative to the applicable reasoning calculus.

---

### Investigation Dependence

Different investigations may admit different candidates, apply different reasoning calculi, or pursue different objectives.

Accordingly, they may produce different Admissibility Structures.

---

### Auditability

An Admissibility Structure should permit reconstruction of why each candidate received its admissibility classification.

Auditability requires explicit links between classifications, reasoning traces, criteria, and supporting representations.

---

## Relationship to Reasoning States

Reasoning states provide the investigation context within which candidates and admissibility classifications exist.

Ω may be associated with one or more reasoning state representations.

Ω is not itself a reasoning state.

See:

`reasoning-states.md`

---

## Relationship to Transition Signatures

Transition signatures document transformation executions that may introduce, modify, or remove candidate representations or admissibility classifications.

They may therefore explain how Ω changes between reasoning state representations.

A transition signature is not itself Ω.

See:

`transition-signatures.md`

---

## Scope

This document specifies the architectural role of Ω within FARA.

It does not define:

- candidate;
- admissibility;
- admissibility classification;
- reasoning calculus;
- reasoning state;
- transition signature;
- resolution rule;
- resolution execution;
- resolution.

Those concepts are defined by the canonical definitions and related architectural documents.

---

## Research Status

Current research investigates:

- formal properties of Ω;
- admissibility equivalence;
- admissibility preservation across transformations;
- completeness of admissibility classification;
- minimality of admissibility representation;
- relationships between Ω and resolution rules;
- representation theorems for admissibility structures.