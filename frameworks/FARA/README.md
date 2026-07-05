# FARA

**Foundational Architecture of Reasoning Analysis**

---

## Purpose

FARA defines the representational architecture layer of Project FAR.

It specifies the architectural objects used to represent structured, explicit, and auditable reasoning.

Formal shared definitions are maintained in [`../../theory/definitions/definitions.md`](../../theory/definitions/definitions.md).

---

## Current Status

FARA is treated as the stable representational architecture layer of Project FAR.

Future FARA changes should be driven by concrete downstream requirements, worked examples, or validated representational deficiencies.

---

## Framework Role

FARA owns representation.

It defines the architectural objects that FAR applies methodologically, FARO operationalizes, FARE may evaluate, and FARM coordinates around.

---

## Relationship to Other Frameworks

- [FAR](../FAR/README.md) uses FARA architecture during investigations.
- [FARO](../FARO/README.md) operates over FAR investigation artifacts and FARA representations.
- [FARE](../FARE/README.md) provides requirement-driven mathematical evaluation support.
- [FARM](../FARM/README.md) coordinates cross-framework requirements without redefining FARA.

---

## Canonical Documents

- [`architecture.md`](architecture.md) — Defines the FARA architecture.
- [`dependency-graph.md`](dependency-graph.md) — Records FARA document-maintenance dependencies.
- [`design-principles.md`](design-principles.md) — Records governing design constraints for FARA.
- [`document-map.md`](document-map.md) — Maps FARA documents and their roles.
- [`primitives.md`](primitives.md) — Identifies candidate primitive concepts.
- [`ontology.md`](ontology.md) — Defines the FARA ontology.
- [`semantics.md`](semantics.md) — Defines the semantic component of FARA.
- [`reasoning-states.md`](reasoning-states.md) — Defines reasoning states.
- [`transition-signatures.md`](transition-signatures.md) — Defines transitions between reasoning states.
- [`admissibility-structure.md`](admissibility-structure.md) — Defines the Admissibility Structure.

---

## Audit History

FARA is covered by the repository-wide stabilization and navigation audits:

- [`../../docs/audits/PROJECT-FAR-POST-V1-REPOSITORY-AUDIT.md`](../../docs/audits/PROJECT-FAR-POST-V1-REPOSITORY-AUDIT.md)
- [`../../docs/audits/FRAMEWORK-NAVIGATION-NORMALIZATION-AUDIT.md`](../../docs/audits/FRAMEWORK-NAVIGATION-NORMALIZATION-AUDIT.md)

---

## Milestones

FARA is treated as the stable representational layer in the post-v1.0 framework stack. No separate FARA milestone file is currently present.

---

## Current Development Policy

Do not expand FARA speculatively.

Modify FARA only when a downstream requirement, concrete worked example, or validated representational defect requires it.

---

## Boundary Rules

FARA owns representational architecture.

It does not define investigation methodology, operational procedures, mathematical evaluation, or meta-framework governance.

---

## Next Steps

Use worked examples to test whether the current representational architecture is sufficient.

---

## Related Documents

- [Project status](../../docs/project-status.md)
- [Canonical map](../../docs/CANONICAL_MAP.md)
- [FAR README](../FAR/README.md)
- [FARO README](../FARO/README.md)
- [FARE README](../FARE/README.md)
- [FARM README](../FARM/README.md)
