# FAR

**Foundational Analysis of Reasoning**

---

## Purpose

FAR defines Project FAR's contract-relative investigation methodology. It freezes the claim and comparison contract, evaluates candidate representations by factorization or collisions, minimizes relative to declared objectives, and reports loss and Unknown. [FARA](../FARA/README.md) is one selected representation target.

When supplied input does not already determine the comparison contract, FAR first uses the governed [Contract Discovery Protocol](../../methodology/contract-discovery-protocol.md) to preserve ambiguity, provenance, assumptions, and the complete bounded contract family before evaluation.

FAR does not introduce or rely on global FARA primitives. Construct, Differentiate, and Restrict are workflow verbs; Resolve is derived rule application.

---

## Current Status

FAR v1.0 Stable has been recorded.

An accepted methodology correction now governs the previously unspecified boundary between under-specified input and the frozen comparison contracts required by the existing contract-relative machinery. The correction is additive and does not change the core theory or reinterpret `far-ir/2.0` or `far-ir/2.1`.

Future FAR changes should be driven by concrete downstream requirements, worked examples, or validated methodological deficiencies.

---

## Framework Role

FAR owns contract discovery when required, contract freezing, and investigation methodology.

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
- [`../../methodology/contract-discovery-protocol.md`](../../methodology/contract-discovery-protocol.md) — Governs pre-contract interpretation discovery and freeze-before-evaluation when input is under-specified.
- [`../../docs/specification/far-intake-1.0.md`](../../docs/specification/far-intake-1.0.md) — Specifies the machine-readable governed intake format and deterministic aggregation semantics.
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
- [`../../docs/governance/far-contract-discovery-acceptance-v1.0.md`](../../docs/governance/far-contract-discovery-acceptance-v1.0.md) — Acceptance record for the governed intake correction.

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

Candidate generation remains part of Stage 6 — Perform Reasoning. The applicable calculus classifies candidates; Stage 7 materializes those results and provenance in the derived Admissibility Structure.

Pre-contract interpretation discovery is an intake obligation, not Stage 6 candidate generation. It determines which explicit comparison contracts must be evaluated; it does not choose the investigation's substantive resolution.

---

## Next Steps

Use canonical worked investigations to test whether declared behavior factors through each representation and to expose collisions, hidden machinery, and contract sensitivity.

---

## Related Documents

- [Project status](../../docs/project-status.md)
- [Canonical map](../../docs/CANONICAL_MAP.md)
- [FARA README](../FARA/README.md)
- [FARO README](../FARO/README.md)
- [FARE README](../FARE/README.md)
- [FARM README](../FARM/README.md)

## Derivation boundary

The factorization and quotient obligations are constrained by shared theory; sequencing, selection, governance, and reporting choices remain compatible independent methodology unless a cited derivation establishes otherwise. The workflow, selections, failure reporting, claim-dimension analysis, and contract-discovery intake procedure are not logical consequences of FARA. See the [derivation-status matrix](../../docs/governance/derivation-status-matrix.md).

## Theory-conformance rule

No FAR artifact may call a representation lossless, sufficient, minimal, or representation-independent without naming the controlling contract, admitted transformations, objective/order, and certificate or boundary required by the core theory.
