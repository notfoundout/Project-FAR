# FAR

**Foundational Analysis of Reasoning**

---

## Purpose

FAR defines the investigation methodology layer of Project FAR.

It provides a structured method for conducting reasoning investigations using the representational architecture defined by [FARA](../FARA/README.md).

FAR does not introduce new FARA primitives.

---

## Current Status

FAR v1.0 Stable has been recorded.

Future FAR changes should be driven by concrete downstream requirements, worked examples, or validated methodological deficiencies.

---

## Framework Role

FAR owns investigation methodology.

It defines how reasoning investigations are conducted, recorded, validated, revised, and closed.

---

## Relationship to Other Frameworks

- [FARA](../FARA/README.md) supplies representational architecture.
- [FARO](../FARO/README.md) operationalizes FAR investigations.
- [FARE](../FARE/README.md) provides requirement-driven mathematical evaluation support.
- [FARM](../FARM/README.md) coordinates cross-framework requirements without redefining FAR.

---

## Canonical Documents

- [`workflow.md`](workflow.md) — Canonical source for the stages of a FAR investigation.
- [`methodology.md`](methodology.md) — Defines methodological principles governing FAR investigations.
- [`application.md`](application.md) — Describes how FAR is applied across domains.
- [`dependency-graph.md`](dependency-graph.md) — Records FAR document and concept dependency order.
- [`design-principles.md`](design-principles.md) — Records governing design principles for FAR.
- [`faro-boundary.md`](faro-boundary.md) — Defines the boundary between FAR and FARO.
- [`example-standard.md`](example-standard.md) — Defines the required structure for canonical FAR examples.
- [`investigation-validation.md`](investigation-validation.md) — Defines validation checks for completed FAR investigations.
- [`FAR-v1.0-criteria.md`](FAR-v1.0-criteria.md) — Defines criteria required before FAR v1.0 Stable.

---

## Audit History

- [`../../docs/audits/FAR-PHASE-1-CANONICAL-AUDIT.md`](../../docs/audits/FAR-PHASE-1-CANONICAL-AUDIT.md)
- [`../../docs/audits/FAR-PHASE-2-STRUCTURAL-AUDIT.md`](../../docs/audits/FAR-PHASE-2-STRUCTURAL-AUDIT.md)
- [`../../docs/audits/FAR-PHASE-3-METHODOLOGY-AUDIT.md`](../../docs/audits/FAR-PHASE-3-METHODOLOGY-AUDIT.md)
- [`../../docs/audits/FAR-PHASE-4-CONSISTENCY-AUDIT.md`](../../docs/audits/FAR-PHASE-4-CONSISTENCY-AUDIT.md)
- [`../../docs/audits/FRAMEWORK-NAVIGATION-NORMALIZATION-AUDIT.md`](../../docs/audits/FRAMEWORK-NAVIGATION-NORMALIZATION-AUDIT.md)

---

## Milestones

- [`../../docs/milestones/FAR-MILESTONE-002-FAR-v1.0-Stable.md`](../../docs/milestones/FAR-MILESTONE-002-FAR-v1.0-Stable.md)

---

## Current Development Policy

Do not expand FAR speculatively.

Modify FAR only when a downstream requirement, concrete worked example, or validated methodological defect requires it.

---

## Boundary Rules

FAR owns investigation methodology.

It does not define representational architecture, operational procedures, mathematical evaluation, or meta-framework governance.

Candidate generation remains part of Stage 6 — Perform Reasoning. Candidate admissibility classification occurs in Stage 7 through the Admissibility Structure.

---

## Next Steps

Use canonical worked investigations to test whether the stable FAR methodology is sufficient.

---

## Related Documents

- [Project status](../../docs/project-status.md)
- [Canonical map](../../docs/CANONICAL_MAP.md)
- [FARA README](../FARA/README.md)
- [FARO README](../FARO/README.md)
- [FARE README](../FARE/README.md)
- [FARM README](../FARM/README.md)
