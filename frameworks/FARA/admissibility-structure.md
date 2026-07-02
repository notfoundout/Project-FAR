# Admissibility Structure (Ω)

## Purpose

This document specifies the role of the Admissibility Structure (Ω) within the Foundational Architecture of Reasoning Analysis (FARA).

The Admissibility Structure records admissibility classifications of candidates within an investigation.

The canonical definitions of all terminology used here are maintained in:

`theory/definitions/definitions.md`

This document specifies the architectural role of Ω rather than redefining the underlying concepts.

---

## Overview

Within an investigation, candidates may be classified according to the applicable reasoning calculus.

Admissibility is the property of satisfying the criteria established by that reasoning calculus.

An admissibility classification is the explicit assignment of admissibility status to a candidate.

The Admissibility Structure (Ω) represents those classifications.

Ω is distinct from:

- the reasoning calculus that determines admissibility;
- the admissibility criteria;
- the candidates being classified;
- the reasoning process that produces classifications;
- the resolution rule;
- the resolution execution;
- the resolution produced.

---

## Definition

The **Admissibility Structure**, denoted **Ω**, is the representation of the admissibility classifications of candidates within an investigation.

Ω records admissibility classifications.

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
- explicitly specified admissibility criteria;
- one or more admissibility classifications.

Changes to any of these may produce a different Admissibility Structure.

---

## Admissibility

Admissibility is determined by the applicable reasoning calculus within an investigation.

Ω records the resulting admissibility classifications.

Ω does not define the reasoning calculus.

Ω does not execute the reasoning calculus.

Ω does not determine whether a candidate is admissible.

---

## Candidates

A candidate is an explicitly represented object admitted for consideration within an investigation.

Candidate status does not imply admissibility.

A candidate may be:

- admissible;
- inadmissible;
- undecided;
- conditionally admissible;
- classified according to another explicitly specified admissibility status.

The admissibility statuses available within Ω depend on the applicable reasoning calculus and investigation.

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

Every candidate admitted for consideration should possess an explicitly represented admissibility classification or explicitly recorded unresolved status.

---

### Traceability

Every admissibility classification should be traceable to:

- the candidate classified;
- the applicable investigation;
- the applicable reasoning calculus;
- the criteria used;
- the reasoning process or reasoning trace that produced the classification.

---

### Calculus Dependence

Different reasoning calculi may classify the same candidates differently.

Admissibility classifications are therefore always relative to the applicable reasoning calculus.

---

### Investigation Dependence

Different investigations may admit different candidates, employ different criteria, or use different reasoning calculi.

Accordingly, they may produce different Admissibility Structures.

---

### Auditability

An Admissibility Structure should support reconstruction of why each candidate received its admissibility classification.

Auditability requires explicit links between classifications, criteria, reasoning traces, and source representations.

---

## Relationship to Reasoning States

Reasoning states provide the investigation context in which candidates and classifications are represented.

Ω may be associated with one or more reasoning state representations.

Ω is not itself a reasoning state.

See:

`reasoning-states.md`

---

## Relationship to Transition Signatures

Transition signatures may document transformation executions that introduce, modify, or remove candidate representations or admissibility classifications.

A transition signature may therefore explain how Ω changed between reasoning state representations.

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
