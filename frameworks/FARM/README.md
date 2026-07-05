# FARM

**Foundational Analysis of Reasoning Meta-framework**

---

## Purpose

FARM defines the meta-framework coordination layer of Project FAR.

It handles post-v1.0 integration across stable framework layers while remaining narrow and non-duplicative.

It shall not redefine FARA, FAR, FARO, or FARE.

---

## Current Status

FARM v1.0 Stable has been recorded.

Future FARM changes should be driven by concrete downstream requirements, worked examples, or validated cross-framework coordination deficiencies.

---

## Framework Role

FARM owns meta-framework coordination.

It routes requirements, classifies defects, governs stable-layer change control, and records cross-framework integration decisions.

---

## Relationship to Other Frameworks

- [FARA](../FARA/README.md) owns representational architecture.
- [FAR](../FAR/README.md) owns investigation methodology.
- [FARO](../FARO/README.md) owns operations.
- [FARE](../FARE/README.md) owns mathematics and formal evaluation support.

FARM coordinates around those layers but does not redefine them.

---

## Canonical Documents

- [`architecture.md`](architecture.md) — Defines FARM's meta-framework role.
- [`dependency-graph.md`](dependency-graph.md) — Records FARM document-maintenance dependencies.
- [`design-principles.md`](design-principles.md) — Defines FARM design constraints.
- [`requirement-routing.md`](requirement-routing.md) — Defines routing of downstream requirements.
- [`defect-classification.md`](defect-classification.md) — Defines defect classes and statuses.
- [`change-control.md`](change-control.md) — Defines gates for stable-layer changes.
- [`integration-record.md`](integration-record.md) — Defines cross-framework integration records.
- [`FARM-v1.0-criteria.md`](FARM-v1.0-criteria.md) — Defines criteria required before FARM v1.0 Stable.

---

## Audit History

- [`../../docs/audits/FARM-PHASE-1-ARCHITECTURE-AUDIT.md`](../../docs/audits/FARM-PHASE-1-ARCHITECTURE-AUDIT.md)
- [`../../docs/audits/FARM-PHASE-2-ARCHITECTURE-STABILIZATION.md`](../../docs/audits/FARM-PHASE-2-ARCHITECTURE-STABILIZATION.md)
- [`../../docs/audits/FARM-PHASE-3-METHODOLOGY-AUDIT.md`](../../docs/audits/FARM-PHASE-3-METHODOLOGY-AUDIT.md)
- [`../../docs/audits/FARM-PHASE-4-CONSISTENCY-AUDIT.md`](../../docs/audits/FARM-PHASE-4-CONSISTENCY-AUDIT.md)
- [`../../docs/audits/FRAMEWORK-NAVIGATION-NORMALIZATION-AUDIT.md`](../../docs/audits/FRAMEWORK-NAVIGATION-NORMALIZATION-AUDIT.md)

---

## Milestones

- [`../../docs/milestones/FARM-v1.0-Stable.md`](../../docs/milestones/FARM-v1.0-Stable.md)

---

## Current Development Policy

Do not expand FARM speculatively.

Modify FARM only when a downstream requirement, concrete worked example, or validated cross-framework coordination defect requires it.

---

## Boundary Rules

FARM owns meta-framework coordination.

It does not define representational architecture, investigation methodology, operational procedures, or mathematical evaluation.

FARM may route a requirement to another framework, but routing does not authorize modification.

---

## Next Steps

Use worked examples to generate real integration records and test whether FARM routing, defect classification, and change control are sufficient.

---

## Related Documents

- [Project status](../../docs/project-status.md)
- [Canonical map](../../docs/CANONICAL_MAP.md)
- [FARA README](../FARA/README.md)
- [FAR README](../FAR/README.md)
- [FARO README](../FARO/README.md)
- [FARE README](../FARE/README.md)
