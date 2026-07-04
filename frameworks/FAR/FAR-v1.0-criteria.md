# FAR v1.0 Stability Criteria

## Purpose

This document defines the criteria required before the Foundational Analysis of Reasoning (FAR) may be declared v1.0 Stable.

It is a governance and audit document.

It does not introduce new definitions.

---

## Stability Standard

FAR v1.0 Stable means that FAR is suitable to serve as the canonical methodology layer of Project FAR.

It does not mean FAR is final, unrevisable, universal, or proven minimal.

---

## Required Criteria

### 1. Canonical Workflow Source

`workflow.md` shall be the canonical source for the FAR investigation stage sequence.

Other documents may summarize the workflow but shall not maintain independent stage definitions.

Status: required.

---

### 2. No Duplicated Stage Definitions

The nine-stage workflow shall not be independently defined across multiple FAR documents.

`methodology.md` and `application.md` shall refer to `workflow.md` for the canonical stage sequence.

Status: required.

---

### 3. Candidate Generation Placement

Candidate generation shall remain part of Stage 6 — Perform Reasoning.

Candidate admissibility shall be classified in Stage 7 through the Admissibility Structure (Ω).

Candidate generation is not a separate universal FAR workflow stage.

Status: required.

---

### 4. Explicit Delegation of Technical Terms

All technical terms used by FAR shall be either:

- defined in `theory/definitions/definitions.md`;
- defined architecturally by FARA;
- or explicitly identified as FAR document roles rather than new primitives.

Status: required.

---

### 5. No New FAR Primitives

FAR shall not introduce new primitives.

FAR workflow stages are procedural roles, not primitive concepts.

Status: required.

---

### 6. FARA Dependency Preserved

FAR shall remain downstream of FARA.

FAR applies the FARA architecture during investigations but does not modify the FARA architecture.

Status: required.

---

### 7. FARO Boundary Preserved

`faro-boundary.md` shall exist and identify permitted and prohibited FARO responsibilities.

FARO shall not begin as a stable operational layer until FAR reaches comparable stability.

FARO shall operationalize FAR rather than redefine it.

Status: required.

---

### 8. Dependency Graph Present and Clarified

`dependency-graph.md` shall exist and identify the FAR document dependency order.

The dependency graph shall state that the ordering is document-maintenance order, not conceptual priority.

Status: required.

---

### 9. Design Principles Present

`design-principles.md` shall exist and identify the governing design constraints of FAR.

Status: required.

---

### 10. Example Standard Present

`example-standard.md` shall exist and define the minimum required structure for canonical FAR examples.

Status: required.

---

### 11. Investigation Validation Present

`investigation-validation.md` shall exist and define the minimum methodological validation checklist for completed FAR investigations.

Status: required.

---

### 12. Methodology, Workflow, and Application Synchronized

The following documents shall be synchronized:

- `methodology.md`
- `workflow.md`
- `application.md`

They may have different roles, but they shall not conflict.

Status: required.

---

### 13. Audit Records Present

The Phase 1 canonical audit and Phase 2 structural audit shall be recorded and preserved under `docs/audits/`.

Status: required.

---

## Completion Checklist

Before FAR v1.0 Stable is declared, verify:

- [ ] `workflow.md` is the canonical stage source.
- [ ] candidate generation is treated as part of Stage 6.
- [ ] candidate admissibility classification is treated as part of Stage 7.
- [ ] `methodology.md` delegates stage order to `workflow.md`.
- [ ] `application.md` delegates stage order to `workflow.md`.
- [ ] `dependency-graph.md` exists.
- [ ] dependency graph order is identified as document-maintenance order.
- [ ] `design-principles.md` exists.
- [ ] `faro-boundary.md` exists.
- [ ] `example-standard.md` exists.
- [ ] `investigation-validation.md` exists.
- [ ] all FARA concepts used by FAR are explicitly delegated.
- [ ] no FAR document introduces new primitives.
- [ ] FARO boundary is stated.
- [ ] canonical map is updated if necessary.
- [ ] README navigation is updated.
- [ ] final methodology audit is complete.
- [ ] final consistency audit is complete.

---

## Notes

FAR v1.0 Stable should be declared only after final methodology and consistency audits confirm that these criteria are satisfied.
