# FAR Dependency Graph

## Purpose

This document records the dependency structure among the core documents and concepts of the Foundational Analysis of Reasoning (FAR).

It is a maintenance artifact intended to prevent circular definitions, duplicated stage definitions, and methodological drift.

This document does not introduce new definitions.

---

## Document Dependency Order

The FAR document dependency order is:

```text
theory/definitions/definitions.md
  -> frameworks/FARA/
  -> frameworks/FAR/workflow.md
  -> frameworks/FAR/methodology.md
  -> frameworks/FAR/application.md
```

This order is a document-maintenance order.

It does not assert philosophical priority, conceptual fundamentality, or chronological rigidity.

`workflow.md` appears before `methodology.md` because it is the canonical source for stage order. `methodology.md` governs the principles for using that workflow.

Navigation and maintenance documents depend on the whole FAR set:

```text
frameworks/FAR/README.md
frameworks/FAR/dependency-graph.md
frameworks/FAR/design-principles.md
frameworks/FAR/FAR-v1.0-criteria.md
frameworks/FAR/faro-boundary.md
frameworks/FAR/example-standard.md
frameworks/FAR/investigation-validation.md
```

---

## Dependency Roles

### Canonical Definitions

Repository-wide technical terminology is defined in:

`theory/definitions/definitions.md`

FAR documents use these definitions rather than redefining them.

---

### FARA

FARA provides the architecture used by FAR.

FAR depends on FARA for concepts such as:

- reasoning states;
- transition signatures;
- admissibility structure;
- resolution rules;
- resolution executions;
- resolutions.

FAR applies these architectural concepts methodologically.

It does not modify their definitions.

---

### Workflow

`workflow.md` is the canonical source for the ordered FAR investigation stages.

Other FAR documents may summarize the workflow, but they should not maintain independent stage definitions.

Candidate generation belongs within Stage 6 — Perform Reasoning.

Stage 7 evaluates and records candidate admissibility through the Admissibility Structure (Ω).

---

### Methodology

`methodology.md` defines the principles governing use of the FAR workflow.

It explains how investigations should remain explicit, auditable, reconstructible, neutral, and reproducible.

It depends on `workflow.md` for the canonical stage sequence.

---

### Application

`application.md` describes how FAR is applied across domains.

It depends on `workflow.md` for stage structure and on `methodology.md` for methodological principles.

---

## Concept Dependency Flow

The core methodological dependency flow is:

```text
Investigation
  -> Representational Structure
  -> Interpretation
  -> Reasoning Calculus
  -> Reasoning State
  -> Transition Signature
  -> Candidate Generation
  -> Admissibility Structure (Ω)
  -> Resolution Rule
  -> Resolution
```

This flow describes methodological dependence, not strict chronological irreversibility.

Candidate generation is included within reasoning activity rather than elevated to a separate universal stage.

FAR investigations may iterate and revisit earlier stages.

---

## Dependency Constraints

The following constraints must be preserved:

- FAR shall not redefine terms canonically defined in `theory/definitions/definitions.md`.
- FAR shall not redefine architectural concepts defined by FARA.
- FAR shall not introduce new primitives.
- FAR shall not collapse reasoning states with reasoning state representations.
- FAR shall not collapse transition signatures with transformation executions.
- FAR shall not collapse admissibility with the Admissibility Structure (Ω).
- FAR shall not collapse resolution rules, resolution executions, and resolutions.
- FARO shall not be developed as an operational layer until FAR is stable.

---

## Maintenance Policy

This dependency graph should be updated whenever:

- a FAR document is added, removed, or re-scoped;
- the canonical workflow changes;
- FAR's dependency on FARA changes;
- a relevant canonical definition changes;
- a methodological stage is added, removed, or renamed.

Dependency updates should be justified by artifact audits, framework revisions, or explicit architectural review.
