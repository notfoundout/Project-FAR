# FARO

## Purpose

FARO (Foundational Analysis of Reasoning Operations) defines the operational layer of Project FAR.

FARO operationalizes FAR v1.0 Stable without redefining FAR, FARA, or FARE.

---

## Current Status

FARO has completed Phase 9 consistency audit and is eligible for a dedicated FARO v1.0 Stable milestone PR.

FARO is not formally v1.0 Stable until that milestone is recorded.

---

## Canonical Documents

- `architecture.md` — Defines the high-level FARO operational architecture.
- `dependency-graph.md` — Records FARO document-maintenance dependencies.
- `design-principles.md` — Defines FARO design constraints.
- `operation-taxonomy.md` — Defines FARO operation categories.
- `operation-interface-standard.md` — Defines required operation specification fields.
- `execution.md` — Defines execution operations.
- `auditing.md` — Defines audit operations.
- `comparison.md` — Defines comparison operations.
- `disagreement-analysis.md` — Defines disagreement analysis operations.
- `reporting.md` — Defines reporting operations.
- `operational-evaluation.md` — Defines operational evaluation.
- `FARO-v1.0-criteria.md` — Defines criteria required before FARO v1.0 Stable.

---

## Boundary Rules

FARO may operationalize FAR.

FARO shall not redefine FAR methodology.

FARO may operate over FARA representations.

FARO shall not redefine FARA architecture.

FARO may expose FARE mathematical needs.

FARO shall not expand FARE without a specific requirement and formal review.

---

## Operation Categories

FARO recognizes six primary operation categories:

- Execution;
- Audit;
- Comparison;
- Disagreement Analysis;
- Reporting;
- Operational Evaluation.

The canonical taxonomy is maintained in `operation-taxonomy.md`.

---

## Relationship to Project FAR

```text
FARA -> FAR v1.0 Stable -> FARO
```

FARA supplies representation.

FAR supplies methodology.

FARO supplies operation.

---

## Notes

FARO v1.0 Stable should be recorded through a dedicated milestone after the Phase 9 consistency audit is reviewed and merged.
