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

Status: verified by Phase 4 consistency audit.

---

### 2. No Duplicated Stage Definitions

The nine-stage workflow shall not be independently defined across multiple FAR documents.

`methodology.md` and `application.md` shall refer to `workflow.md` for the canonical stage sequence.

Status: verified by Phase 4 consistency audit.

---

### 3. Candidate Generation Placement

Candidate generation shall remain part of Stage 6 — Perform Reasoning.

Candidate admissibility shall be classified in Stage 7 through the Admissibility Structure (Ω).

Candidate generation is not a separate universal FAR workflow stage.

Status: verified by Phase 4 consistency audit.

---

### 4. Optional Stage Policy

FAR shall permit stages to be marked `Not applicable` only when the investigation record explicitly states why the stage is not applicable.

No workflow stage shall be silently omitted.

Status: verified by Phase 4 consistency audit.

---

### 5. Revision Record Policy

FAR shall require revision records when an investigation revisits an earlier stage.

A revision record should identify the stage revisited, the reason for revision, the artifact changed, and the effect on later stages.

Status: verified by Phase 4 consistency audit.

---

### 6. Closure Policy

FAR shall define investigation closure statuses.

At minimum, FAR shall distinguish resolved, provisionally resolved, unresolved, suspended, incomplete, and invalid investigations.

Status: verified by Phase 4 consistency audit.

---

### 7. Artifact-Based Reconstructibility

FAR shall define reproducibility in terms of artifact-based reconstructibility.

It shall not rely on assumptions about identical investigators or identical psychological states.

Status: verified by Phase 4 consistency audit.

---

### 8. Edge-Case Handling

FAR shall explicitly handle edge cases including no admissible candidates, multiple admissible candidates, changing interpretations, changing reasoning calculi, open-ended investigations, and conflicting resolutions.

Status: verified by Phase 4 consistency audit.

---

### 9. Explicit Delegation of Technical Terms

All technical terms used by FAR shall be either:

- defined in `theory/definitions/definitions.md`;
- defined architecturally by FARA;
- or explicitly identified as FAR document roles rather than new primitives.

Status: verified by Phase 4 consistency audit.

---

### 10. No New FAR Primitives

FAR shall not introduce new primitives.

FAR workflow stages are procedural roles, not primitive concepts.

Status: verified by Phase 4 consistency audit.

---

### 11. FARA Dependency Preserved

FAR shall remain downstream of FARA.

FAR applies the FARA architecture during investigations but does not modify the FARA architecture.

Status: verified by Phase 4 consistency audit.

---

### 12. FARO Boundary Preserved

`faro-boundary.md` shall exist and identify permitted and prohibited FARO responsibilities.

FARO shall not begin as a stable operational layer until FAR reaches comparable stability.

FARO shall operationalize FAR rather than redefine it.

Status: verified by Phase 4 consistency audit.

---

### 13. Dependency Graph Present and Clarified

`dependency-graph.md` shall exist and identify the FAR document dependency order.

The dependency graph shall state that the ordering is document-maintenance order, not conceptual priority.

Status: verified by Phase 4 consistency audit.

---

### 14. Design Principles Present

`design-principles.md` shall exist and identify the governing design constraints of FAR.

Status: verified by Phase 4 consistency audit.

---

### 15. Example Standard Present

`example-standard.md` shall exist and define the minimum required structure for canonical FAR examples.

Status: verified by Phase 4 consistency audit.

---

### 16. Investigation Validation Present

`investigation-validation.md` shall exist and define the minimum methodological validation checklist for completed FAR investigations.

Status: verified by Phase 4 consistency audit.

---

### 17. Methodology, Workflow, and Application Synchronized

The following documents shall be synchronized:

- `methodology.md`
- `workflow.md`
- `application.md`

They may have different roles, but they shall not conflict.

Status: verified by Phase 4 consistency audit.

---

### 18. Audit Records Present

The Phase 1 canonical audit, Phase 2 structural audit, Phase 3 methodology audit, and Phase 4 consistency audit shall be recorded and preserved under `docs/audits/`.

Status: verified by Phase 4 consistency audit.

---

## Completion Checklist

Before FAR v1.0 Stable is declared, verify:

- [x] `workflow.md` is the canonical stage source.
- [x] candidate generation is treated as part of Stage 6.
- [x] candidate admissibility classification is treated as part of Stage 7.
- [x] optional-stage policy is present.
- [x] revision-record policy is present.
- [x] closure policy is present.
- [x] reproducibility is framed as artifact-based reconstructibility.
- [x] edge-case handling is present.
- [x] `methodology.md` delegates stage order to `workflow.md`.
- [x] `application.md` delegates stage order to `workflow.md`.
- [x] `dependency-graph.md` exists.
- [x] dependency graph order is identified as document-maintenance order.
- [x] `design-principles.md` exists.
- [x] `faro-boundary.md` exists.
- [x] `example-standard.md` exists.
- [x] `investigation-validation.md` exists.
- [x] all FARA concepts used by FAR are explicitly delegated.
- [x] no FAR document introduces new primitives.
- [x] FARO boundary is stated.
- [x] canonical map is updated if necessary.
- [x] README navigation is updated.
- [x] final methodology audit is complete.
- [x] final consistency audit is complete.

---

## Notes

The Phase 4 consistency audit found no remaining blocker to FAR v1.0 Stable.

FAR v1.0 should be declared through a dedicated milestone PR after the Phase 4 audit changes are merged.
