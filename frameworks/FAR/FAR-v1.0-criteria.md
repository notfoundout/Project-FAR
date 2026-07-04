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

### 3. Explicit Delegation of Technical Terms

All technical terms used by FAR shall be either:

- defined in `theory/definitions/definitions.md`;
- defined architecturally by FARA;
- or explicitly identified as FAR document roles rather than new primitives.

Status: required.

---

### 4. No New FAR Primitives

FAR shall not introduce new primitives.

FAR workflow stages are procedural roles, not primitive concepts.

Status: required.

---

### 5. FARA Dependency Preserved

FAR shall remain downstream of FARA.

FAR applies the FARA architecture during investigations but does not modify the FARA architecture.

Status: required.

---

### 6. FARO Boundary Preserved

FARO shall not begin as a stable operational layer until FAR reaches comparable stability.

FARO shall operationalize FAR rather than redefine it.

Status: required.

---

### 7. Dependency Graph Present

`dependency-graph.md` shall exist and identify the FAR document dependency order.

Status: required.

---

### 8. Design Principles Present

`design-principles.md` shall exist and identify the governing design constraints of FAR.

Status: required.

---

### 9. Methodology, Workflow, and Application Synchronized

The following documents shall be synchronized:

- `methodology.md`
- `workflow.md`
- `application.md`

They may have different roles, but they shall not conflict.

Status: required.

---

### 10. Audit Record Present

The Phase 1 canonical audit shall be recorded and preserved under `docs/audits/`.

Status: required.

---

## Completion Checklist

Before FAR v1.0 Stable is declared, verify:

- [ ] `workflow.md` is the canonical stage source.
- [ ] `methodology.md` delegates stage order to `workflow.md`.
- [ ] `application.md` delegates stage order to `workflow.md`.
- [ ] `dependency-graph.md` exists.
- [ ] `design-principles.md` exists.
- [ ] all FARA concepts used by FAR are explicitly delegated.
- [ ] no FAR document introduces new primitives.
- [ ] FARO boundary is stated.
- [ ] canonical map is updated if necessary.
- [ ] README navigation is updated.

---

## Notes

FAR v1.0 Stable should be declared only after a final consistency audit confirms that these criteria are satisfied.
