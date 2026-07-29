# Theory/Dependency Authority Audit Question v1.0

Status: **Research**

Investigation: `FAR-THEORY-DEPENDENCY-AUDIT-001`

Base commit: `5e8f27b617632a76e76760779dcbb24dedbb6786`

## Objective justification

The accepted repository contains an unresolved authority ambiguity:

- `theory/definitions/definitions.md` declares repository-wide canonical definition authority;
- `frameworks/FARA/primitives.md` classifies seven terms as FARA candidate primitives while directing canonical definitions back to shared theory;
- `docs/governance/semantic-consistency.json` assigns one undifferentiated `owner` field and does not register all seven candidate primitives;
- FAR and FARO depend on FARA artifacts, while accepted boundary and derivation records reject treating downstream procedures as necessary consequences of FARA.

The ambiguity is objectively relevant because the next experiment protocol must know which commitments are theory, FARA architecture, FAR methodology, FARO operations, protocol choices, or governance decisions. Leaving that distinction implicit risks circular dependency, false derivation, and invalid promotion.

## Research question

Do the accepted artifacts at the frozen base require:

1. separate authority relations for canonical definition, candidate-primitive classification, formal representation, methodology, operations, protocol design, and governance; and
2. classification of FARA→FAR and FARA/FAR→FARO dependencies as artifact/workflow contracts rather than logical derivations?

## Candidate hypotheses

### H0 — Undifferentiated authority is sufficient

One owner per term and one untyped dependency arrow can represent the accepted repository without loss or contradiction.

### H1 — Split authority is required

Canonical definition authority and FARA candidate-primitive classification are distinct relations; formalization, methodology, operations, protocol design, and governance require separate owners.

### H2-D — Downstream procedures are derived

FAR methodology and FARO operations are logical consequences of FARA or its scoped formal kernel.

### H2-C — Downstream dependencies are contracts

FAR and FARO consume and preserve upstream artifacts and declared workflow context, but their procedures remain independently selected unless an accepted derivation proves otherwise.

## Decision rules

- Reject H0 if accepted sources assign canonical definition and candidate classification to different canonical locations or if a single owner field omits a required authority relation.
- Support H1 only if the split is directly recoverable from accepted source text without adding new intellectual content.
- Reject H2-D if accepted boundary or derivation authority explicitly denies the relevant theorem/necessity claim and no accepted proof artifact establishes it.
- Support H2-C only if accepted dependency documents state that downstream layers use, apply, consume, preserve, or operate over upstream artifacts while retaining independent procedural ownership.
- Preserve `Unknown` where the accepted sources do not determine a relation.

## Frozen lifecycle state

| Stage | Status |
|---|---|
| Question | complete |
| Execution | pending |
| Observation | pending |
| Discovery | pending |
| Replication | pending |
| Acceptance | prohibited |
| Promotion | prohibited |
| Repository Change | prohibited |

## Nonclaims

This question does not establish a new authority model, alter any canonical file, classify any dependency, authorize experiment preregistration or execution, or strengthen `FARA-FORMAL-KERNEL-001`.
