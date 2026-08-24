# FARA

**Foundational Architecture of Reasoning Analysis**

---

## Purpose

FARA defines Project FAR's selected representation-target layer. It supplies a finite explicit auditable v1 engineering schema; it is not a universal source ontology.

It specifies the architectural objects used to represent structured, explicit, and auditable reasoning.

Formal shared definitions are maintained in [`../../theory/definitions/definitions.md`](../../theory/definitions/definitions.md).

---

## Current Status

FARA is treated as the stable representational architecture layer of Project FAR.

`FARA-FORMAL-KERNEL-001` is Accepted within Project FAR v1.0 finite explicit auditable representational architecture. The canonical target for that scope is the [identity-bearing many-sorted relational kernel](formal-kernel.md). Its seven named concepts are schema/contract roles rather than global primitives, and Ω is a derived materialized view. This selection does not establish global uniqueness, universality, minimality, completeness, or external-investigator independence.

Future FARA changes should be driven by concrete downstream requirements, worked examples, validated representational deficiencies, or the accepted discovery lifecycle.

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
- [`formal-kernel.md`](formal-kernel.md) — Defines the accepted identity-bearing many-sorted relational formal kernel within the registered v1.0 scope.
- [`dependency-graph.md`](dependency-graph.md) — Records FARA document-maintenance dependencies.
- [`design-principles.md`](design-principles.md) — Records governing design constraints for FARA.
- [`document-map.md`](document-map.md) — Maps FARA documents and their roles.
- [`primitives.md`](primitives.md) — Records the seven FARA schema roles at the historical path.
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

The formal-kernel authority is recorded by:

- [`../../docs/governance/fara-formal-kernel-acceptance-v1.0.md`](../../docs/governance/fara-formal-kernel-acceptance-v1.0.md)
- [`../../docs/governance/fara-formal-kernel-promotion-v1.0.md`](../../docs/governance/fara-formal-kernel-promotion-v1.0.md)

---

## Milestones

FARA is treated as the stable representational layer in the post-v1.0 framework stack. No separate FARA milestone file is currently present.

---

## Current Development Policy

Do not expand FARA speculatively.

Modify FARA only when a downstream requirement, concrete worked example, validated representational defect, or accepted and promoted discovery requires it.

---

## Boundary Rules

FARA owns representational architecture.

It does not define investigation methodology, operational procedures, mathematical evaluation, or meta-framework governance.

The canonical formal kernel is a representation architecture. It does not make typed-hypergraph paths or algebraic operation composition primitive FARA commitments.

---

## Next Steps

Use declared contracts and factorization/collision tests to evaluate mappings into the kernel. Preserve every added tag, interpreter, sidecar, and audit-only distinction as charged machinery.

---

## Related Documents

- [Project status](../../docs/project-status.md)
- [Canonical map](../../docs/CANONICAL_MAP.md)
- [FAR README](../FAR/README.md)
- [FARO README](../FARO/README.md)
- [FARE README](../FARE/README.md)
- [FARM README](../FARM/README.md)

## Epistemic boundary

“Stable” is a maintenance status, not proof that FARA is universal, globally minimal, necessary, or lossless. The seven named concepts are schema roles, not global primitives; FAR methods and FARO operations are downstream and are not FARA axioms. `FARA-FORMAL-KERNEL-001` is Accepted only at its registered scope. See the [framework-boundary specification](../../docs/governance/framework-boundaries.md) and [limitations register](../../docs/governance/limitations-register.md).

## Contract-relative adequacy

A mapping into FARA is sufficient only for a declared comparison contract and only when behavior factors through the mapping. The kernel may retain more distinctions than the contract's observational quotient for auditability; that is an explicit engineering choice, not a minimality theorem.
