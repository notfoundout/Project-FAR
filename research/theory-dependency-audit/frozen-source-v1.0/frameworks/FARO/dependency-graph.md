# FARO Dependency Graph

## Purpose

This document records FARO document-maintenance dependencies.

It does not define conceptual priority and does not introduce new framework primitives.

---

## Maintenance Order

```text
theory/definitions/definitions.md
  -> frameworks/FARA/
  -> frameworks/FAR/
  -> frameworks/FARO/architecture.md
  -> frameworks/FARO/design-principles.md
  -> frameworks/FARO/operation-taxonomy.md
  -> frameworks/FARO/operation-interface-standard.md
  -> frameworks/FARO/{execution,auditing,comparison,disagreement-analysis,reporting,operational-evaluation}.md
  -> frameworks/FARO/FARO-v1.0-criteria.md
```

---

## Dependency Roles

### FARA

Supplies representational architecture.

### FAR

Supplies stable investigation methodology, validation requirements, workflow stages, closure status, revision policy, and artifact standards.

### FARO Architecture

Defines the operational layer and its major sublayers.

### Design Principles

Govern how FARO operations must preserve FAR, FARA, and FARE boundaries.

### Operation Taxonomy

Defines the recognized categories of FARO operations.

### Operation Interface Standard

Defines the required structure for individual operation specifications.

### Operation Category Documents

Define execution, auditing, comparison, disagreement analysis, reporting, and operational evaluation.

### FARO v1.0 Criteria

Defines the criteria required before FARO v1.0 Stable.

---

## Boundary Constraints

- FARO shall not redefine FARA architecture.
- FARO shall not redefine FAR methodology.
- FARO shall not expand FARE mathematics without a specific requirement.
- FARO shall not use operation-specific convenience as a reason to change canonical methodology.
