# FAR Epistemic Assurance Contracts 1.0

Status: Accepted additive specification

## Purpose

These contracts preserve distinctions required by general-purpose evidence and argument verification without modifying existing FAR reasoning contracts.

## Contracts

### Source lineage

`far-source-lineage/1.0` records whether a source is independent, originating, copied, syndicated, quoted, derived, mixed, or unknown. `root_lineage_ids` represent independent origin lineages rather than visible source count.

An `origin` or `independent` record has no upstream source and establishes exactly one root lineage. Additional roots require declared upstream derivation (`mixed_derivation` when appropriate); they cannot be introduced by a base record.

Semantic validation rejects self-dependence, cycles, unresolved upstream references inside a checked set, and forged root-lineage inheritance.

### Temporal state

`far-temporal-state/1.0` separates:

- `valid_time`: when a represented state applies to the subject;
- `known_time`: when that state is known/recorded by FAR.

Retraction, correction, supersession, and withdrawal are state changes, not retroactive deletion of prior knowledge state.

### Abstention

`far-abstention/1.0` records a deliberate decision not to adjudicate. It requires a reason, blocking assurance dimensions, rationale, and explicit conditions for reopening.

Abstention is not support, contradiction, or evidence of absence.

### Audit assurance

`far-audit-assurance/1.0` requires a completed audit to state the status of:

- source integrity;
- interpretation fidelity;
- search coverage;
- evidence adjudication;
- inference adjudication;
- reproducibility;
- hostile-source isolation.

An `assured` audit cannot contain unknown/failed required checks or unresolved defeaters. A `bounded` audit must expose its boundary.
Direct semantic validation rejects absent or unrecognized `overall_status` values, even if a caller has not separately run JSON Schema validation.

## Security boundary

`methodology/hostile-source-boundary.md` makes source material untrusted data. Content under audit cannot alter control policy merely by containing instructions.

## Assurance boundary

These contracts improve auditability of the process. They do not certify external-world truth.
