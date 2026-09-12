# FAR Contract-Discovery Intake Correction v1.0

Status: **Accepted internal methodology correction**

Date: 2026-09-12

## Question

Can the current FAR workflow receive under-specified input and reach a non-`Unknown` comparison without an investigator first choosing result-determining contract parameters outside the governed method?

## Execution

Current authority was traced through the root agent instructions, research execution charter, project status, canonical map, FAR workflow, FAR methodology, FAR investigation validation, `far-ir/2.0` specification, contract schema, and mechanization CLI.

## Observation

The canonical workflow requires a frozen claim and comparison contract. `far-ir/2.0` requires explicit source domain, required behavior, representation, observation contexts, admitted transformations, interpretation profile, target/model class, and frame. The mechanization validates already-constructed records.

No canonical procedure governed how an under-specified input becomes that contract. Therefore a non-`Unknown` application could depend on an externally supplied interpretation or contract choice that was not itself subjected to the same provenance, ambiguity, freeze, and no-silent-pruning discipline.

## Discovery

The missing methodological object is a governed pre-contract intake record. The correction is necessary only at the boundary between raw input and the existing contract-relative machinery.

The correction must preserve the core theory and existing `far-ir/2.0` semantics while making material interpretation selection auditable.

## Falsification attempts

The correction was tested against the following failure modes:

- source-derived interpretation with no source provenance;
- inferred interpretation with no derivation;
- silent omission of one active interpretation combination;
- explicit compatibility exclusion of a combination;
- post-freeze discovery tampering;
- evaluation before freeze;
- evaluation bound to the wrong contract hash;
- evaluation timestamp preceding freeze;
- incomplete evaluation of the frozen family;
- analyst-free aggregation across invariant, conflicting, and unresolved outcomes.

The negative cases are rejected and the positive cases pass in the registered unit tests.

## Replication

`tests/test_far_intake_v1.py` reconstructs the bounded semantics using only generic entities and contracts. It contains no application-specific taxonomy or expected domain verdict.

The test suite verifies deterministic hash binding, Cartesian family coverage, explicit exclusions, evaluation ordering, and fixed aggregation.

## Acceptance

Accepted at this exact scope:

1. Under-specified input requires a governed intake before non-`Unknown` contract-relative evaluation.
2. Material interpretations must be explicit and provenance-classified.
3. Exclusions must remain recorded rather than being silently deleted.
4. The bounded contract family must cover every active material interpretation combination unless an explicit compatibility exclusion removes that exact combination.
5. Discovery inputs must be frozen before evaluation.
6. Per-contract evaluations must bind the frozen candidate hash.
7. Cross-contract aggregation is mechanical.

## Promotion

The accepted correction is promoted through:

- [`../../methodology/contract-discovery-protocol.md`](../../methodology/contract-discovery-protocol.md);
- [`../specification/far-intake-1.0.md`](../specification/far-intake-1.0.md);
- [`../../schemas/far-intake-v1.schema.json`](../../schemas/far-intake-v1.schema.json);
- [`../../mechanization/far_mechanization/intake_v1.py`](../../mechanization/far_mechanization/intake_v1.py);
- [`../../tests/test_far_intake_v1.py`](../../tests/test_far_intake_v1.py);
- the FAR workflow and investigation-validation gates.

## Nonclaims

This correction does not establish:

- that any bounded search is semantically complete in an open domain;
- that recorded sources are factually correct or authoritative merely because they are hashed;
- that every hidden assumption can be mechanically detected;
- that every Cartesian combination is meaningful outside the recorded scope;
- that `far-intake/1.0` is a universal or minimal intake architecture;
- external validation, novelty, priority, empirical utility, or commercial value.

It changes no core-theory claim status and does not reinterpret `far-ir/2.0` or `far-ir/2.1`.
