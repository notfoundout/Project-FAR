# FARO Design Principles

## Purpose

This document defines design principles for FARO.

It does not introduce new primitives.

---

## Principle 1 — Operationalize, Do Not Redefine

FARO operationalizes FAR v1.0 Stable.

It shall not redefine FAR methodology.

---

## Principle 2 — Preserve FARA Architecture

FARO operates over FARA representations.

It shall not redefine FARA architectural objects.

---

## Principle 3 — Operate on Explicit Artifacts

Every FARO operation must operate on explicit inputs and produce explicit outputs.

Implicit reasoning, hidden criteria, and undocumented assumptions are not acceptable operational artifacts.

---

## Principle 4 — Keep Evaluation FAR-Grounded

FARO evaluation criteria must be grounded in FAR methodology or explicit operation criteria.

FARO shall not treat operational evaluation as truth determination.

---

## Principle 5 — Define Failure Modes

Every operation should define how it can fail, return incomplete results, or report insufficient input.

---

## Principle 6 — Preserve FARE Freeze Policy

FARO may expose mathematical needs.

FARO shall not expand FARE unless a specific requirement is documented and reviewed.

---

## Principle 7 — Traceability

Every FARO operation should trace to:

- a FAR artifact requirement;
- a FARA representation;
- a FARO operation category;
- or an explicit operational objective.

---

## Principle 8 — No Silent Mutation

FARO operations may inspect, transform, compare, or report on artifacts only when their effects are explicit.

No operation should silently alter the meaning of an investigation record.
