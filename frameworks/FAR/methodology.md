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

Every assumption, representation, transformation, candidate, admissibility classification, resolution rule, and conclusion should be explicitly represented when relevant.

Silent omission weakens the investigation record.

---

### Auditability

The complete investigation should be reconstructible from its recorded reasoning states, transition signatures, revision records, validation status, and closure status.

---

### Neutrality

The methodology does not prescribe which reasoning calculus should be used.

Different investigations may employ different reasoning calculi.

FAR does not require a specific logic, mathematical system, epistemology, scientific domain, legal standard, historical method, or AI architecture.

---

### Reconstructibility

A FAR investigation is reproducible to the extent that another investigator can reconstruct the reasoning process from the recorded artifacts under the stated interpretation and reasoning calculus.

FAR does not require that independent investigators reach identical psychological states or identical judgments.

It requires enough explicit structure for the investigation to be reconstructed, audited, and compared.

---

### Iterative Revisability

A FAR investigation may return to earlier workflow stages whenever new representations, revised interpretations, modified criteria, or additional reasoning require further analysis.

Every such revision should record the stage revisited, the reason for revision, the artifact changed, and the effect on later stages.

---

### Closure Discipline

A FAR investigation should not simply stop without status.

Closure should be recorded as resolved, provisionally resolved, unresolved, suspended, incomplete, or invalid.

Closure status is methodological rather than truth-guaranteeing.

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

The FAR methodology remains under Phase 3 methodology audit.

Current work includes:

- verifying methodological neutrality;
- strengthening revision and closure policies;
- ensuring artifact-based reconstructibility;
- and preparing for Phase 4 consistency audit.
