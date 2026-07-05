# FARO

**Foundational Analysis of Reasoning Operations**

---

## Purpose

FARO defines the operational layer of Project FAR.

It operationalizes FAR v1.0 Stable over FARA representations and FAR investigation artifacts without redefining FAR, FARA, FARE, or FARM.

---

## Current Status

FARO v1.0 Stable has been recorded.

Future FARO changes should be driven by concrete downstream requirements, worked examples, or validated operational deficiencies.

---

## Framework Role

FARO owns operations.

It defines execution, audit, comparison, disagreement analysis, reporting, and operational evaluation procedures over explicit reasoning artifacts.

---

## Relationship to Other Frameworks

- [FARA](../FARA/README.md) supplies representation.
- [FAR](../FAR/README.md) supplies investigation methodology.
- [FARE](../FARE/README.md) supplies requirement-driven mathematical evaluation support.
- [FARM](../FARM/README.md) coordinates cross-framework requirements without redefining FARO.

---

## Canonical Documents

- [`architecture.md`](architecture.md) — Defines the high-level FARO operational architecture.
- [`dependency-graph.md`](dependency-graph.md) — Records FARO document-maintenance dependencies.
- [`design-principles.md`](design-principles.md) — Defines FARO design constraints.
- [`operation-taxonomy.md`](operation-taxonomy.md) — Defines FARO operation categories.
- [`operation-interface-standard.md`](operation-interface-standard.md) — Defines required operation specification fields.
- [`execution.md`](execution.md) — Defines execution operations.
- [`auditing.md`](auditing.md) — Defines audit operations.
- [`comparison.md`](comparison.md) — Defines comparison operations.
- [`disagreement-analysis.md`](disagreement-analysis.md) — Defines disagreement analysis operations.
- [`reporting.md`](reporting.md) — Defines reporting operations.
- [`operational-evaluation.md`](operational-evaluation.md) — Defines operational evaluation.
- [`FARO-v1.0-criteria.md`](FARO-v1.0-criteria.md) — Defines criteria required before FARO v1.0 Stable.

---

## Audit History

- [`../../docs/audits/FARO-PHASE-6-ARCHITECTURE-AUDIT.md`](../../docs/audits/FARO-PHASE-6-ARCHITECTURE-AUDIT.md)
- [`../../docs/audits/FARO-PHASE-7-ARCHITECTURE-STABILIZATION.md`](../../docs/audits/FARO-PHASE-7-ARCHITECTURE-STABILIZATION.md)
- [`../../docs/audits/FARO-PHASE-8-METHODOLOGY-AUDIT.md`](../../docs/audits/FARO-PHASE-8-METHODOLOGY-AUDIT.md)
- [`../../docs/audits/FARO-PHASE-9-CONSISTENCY-AUDIT.md`](../../docs/audits/FARO-PHASE-9-CONSISTENCY-AUDIT.md)
- [`../../docs/audits/FRAMEWORK-NAVIGATION-NORMALIZATION-AUDIT.md`](../../docs/audits/FRAMEWORK-NAVIGATION-NORMALIZATION-AUDIT.md)

---

## Milestones

- [`../../docs/milestones/FAR-MILESTONE-004-FARO-v1.0-Stable.md`](../../docs/milestones/FAR-MILESTONE-004-FARO-v1.0-Stable.md)

---

## Current Development Policy

Do not expand FARO speculatively.

Modify FARO only when a downstream requirement, concrete worked example, or validated operational defect requires it.

---

## Boundary Rules

FARO owns operations.

It does not define representational architecture, investigation methodology, mathematical evaluation, or meta-framework governance.

FARO may expose mathematical needs, but it does not expand FARE without a reviewed requirement.

---

## Next Steps

Use FARO audit, comparison, disagreement-analysis, and reporting examples to test the stable operational layer.

---

## Related Documents

- [Project status](../../docs/project-status.md)
- [Canonical map](../../docs/CANONICAL_MAP.md)
- [FARA README](../FARA/README.md)
- [FAR README](../FAR/README.md)
- [FARE README](../FARE/README.md)
- [FARM README](../FARM/README.md)
