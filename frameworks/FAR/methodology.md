# FAR Methodology

## Purpose

This document defines the methodology of the Foundational Analysis of Reasoning (FAR).

FAR provides a structured process for conducting investigations within the architectural framework established by FARA.

It defines how the architectural components are applied during an investigation.

This document describes methodological principles.

The canonical ordered stage sequence is maintained in:

`workflow.md`

---

## Objective

The objective of FAR is to conduct investigations that are:

- structured;
- explicit;
- auditable;
- reconstructible.

The methodology is independent of any particular reasoning calculus or application domain.

---

## Methodological Role

FAR does not define the architecture of reasoning.

FAR applies the architecture supplied by FARA.

FAR does not introduce new primitives.

FAR workflow stages are procedural roles used to organize investigation activity.

---

## Workflow Delegation

A FAR investigation proceeds according to the canonical workflow defined in:

`workflow.md`

This document does not maintain an independent stage list.

Any change to the FAR stage sequence shall be made in `workflow.md` and then reflected in dependent documents.

---

## Delegated Architectural Concepts

The following concepts are defined by FARA and repository-wide canonical definitions:

- reasoning state;
- reasoning state representation;
- transition signature;
- Admissibility Structure (Ω);
- resolution rule;
- resolution execution;
- resolution.

FAR specifies how these concepts are used during an investigation.

FAR does not redefine them.

---

## Principles

Every FAR investigation should satisfy the following principles.

### Explicitness

Every assumption, representation, transformation, and conclusion should be explicitly represented.

---

### Auditability

The complete investigation should be reconstructible from its recorded reasoning states and transition signatures.

---

### Neutrality

The methodology does not prescribe which reasoning calculus should be used.

Different investigations may employ different reasoning calculi.

---

### Reproducibility

Equivalent investigators following the same methodology should be capable of reproducing equivalent investigations.

---

### Iterative Revisability

A FAR investigation may return to earlier workflow stages whenever new representations, revised interpretations, modified criteria, or additional reasoning require further analysis.

---

## Relationship to FARA

FARA defines the architectural components used during an investigation.

FAR defines the methodology for applying those components.

The methodology depends upon the architecture but does not modify it.

---

## Relationship to FARO

FARO should operationalize stable FAR methodology.

FARO should not redefine FAR methodology, alter FAR workflow stages, or introduce replacement primitives.

---

## Current Status

The FAR methodology remains under Phase 1 canonical stabilization.

Current work includes:

- synchronization of workflow, methodology, and application documents;
- explicit delegation to canonical definitions and FARA;
- and preparation for FAR v1.0 Stable.
