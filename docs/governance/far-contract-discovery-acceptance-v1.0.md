# FAR Contract-Discovery Intake Correction v1.0

Status: **Accepted internal methodology correction**

Date: 2026-09-12

## Question

Can the current FAR workflow receive under-specified input and reach a non-`Unknown` comparison without an investigator first choosing result-determining contract parameters outside the governed method?

## Execution

Current authority was traced through the root agent instructions, research execution charter, project status, canonical map, FAR workflow, FAR methodology, FAR investigation validation, `far-ir/2.0` specification, contract schema, and mechanization CLI.

The proposed correction was then subjected to adversarial implementation review, schema/semantic consistency checks, hostile mutations, chronology attacks, provenance-pruning attacks, freeze tampering, evaluation substitution, aggregation boundary tests, and package-entrypoint verification.

## Observation

The canonical workflow required a frozen claim and comparison contract. `far-ir/2.0` required explicit source domain, required behavior, representation, observation contexts, admitted transformations, interpretation profile, target/model class, and frame. The existing mechanization validated already-constructed records.

No canonical procedure governed how an under-specified input became that contract. Therefore a non-`Unknown` application could depend on an externally supplied parse, interpretation, or contract choice that was not itself subjected to the same provenance, ambiguity, freeze, and no-silent-pruning discipline.

## Discovery

The missing methodological object is a governed pre-contract intake record. The correction is required only at the boundary between incomplete input and the existing contract-relative machinery.

The correction must preserve the core theory and existing `far-ir/2.0`/`far-ir/2.1` semantics while making material parse and interpretation selection auditable.

## Falsification and hostile audit

The implementation was tested against, and now rejects or correctly bounds, at least the following failure modes:

- schema-invalid records reaching semantic validation or freeze;
- malformed nested values causing uncaught semantic-validator exceptions;
- source-derived interpretation without provenance;
- synthesis or inference without derivation;
- silent omission of an active interpretation combination;
- compatibility pruning with an analyst-written reason but no auditable basis;
- source-based exclusion without source provenance;
- raw-input or inference-based exclusion without derivation;
- silent omission of a materially distinct claim parse;
- exclusion of every claim parse;
- omission of the singleton candidate for a retained zero-material parse;
- active material term with no active interpretation;
- active material term or active parse with no recorded search coverage;
- registered query absent from saturation execution provenance;
- registered source absent from saturation provenance;
- saturation observation predating a source it claims to include;
- duplicate or unordered saturation rounds;
- final saturation round still discovering material alternatives;
- source retrieval or saturation after the evidence cutoff;
- freeze timestamp predating discovery evidence;
- post-freeze raw-input or discovery tampering;
- freeze-timestamp substitution;
- evaluation before freeze;
- evaluation bound to the wrong candidate contract hash;
- evaluation bound to the wrong freeze identity;
- non-`Unknown` evaluation without evidence reference;
- `Unknown` evaluation without explanatory note;
- incomplete evaluation of the frozen contract family;
- invariant promotion despite a frozen result-relevant `Unknown` assumption;
- non-JSON contract values causing failure-open behavior;
- package metadata declaring `far-intake` while the build backend omits the entrypoint;
- structural type mutations across major manifest objects.

The generic regression suite passes **33/33** tests. Python compilation and JSON-schema parsing also pass on the exact staged implementation.

## Replication

`tests/test_far_intake_v1.py` reconstructs the bounded semantics using only generic entities, relations, sources, interpretations, and contracts. It contains no application-specific taxonomy or expected domain verdict.

The suite verifies schema-first validation, provenance and derivation rules, complete parse/interpretation-family coverage, explicit exclusions, search and saturation bookkeeping, chronology, deterministic hash binding, evaluation ordering/evidence, unresolved-assumption handling, fixed aggregation, fail-closed malformed-input behavior, and console-entrypoint packaging.

## Acceptance

Accepted at this exact scope:

1. Under-specified input requires a governed intake before non-`Unknown` contract-relative evaluation.
2. Materially distinct parses and interpretations must remain explicit or be removed only through auditable exclusion records.
3. Source-based exclusions require source provenance; raw-input and inference-based exclusions require explicit derivations.
4. Every active material term and active parse must be covered by the recorded bounded search protocol.
5. Registered search queries and sources must be represented in timestamped saturation provenance, ending in a no-new-material-alternative observation before freeze.
6. The bounded contract family must cover every active material interpretation combination; a zero-material retained parse contributes one empty-assignment candidate.
7. Discovery evidence must temporally precede freeze, and discovery inputs plus freeze time must be cryptographically bound before evaluation.
8. Per-contract evaluations must bind both the frozen candidate hash and exact freeze identity and carry explicit evidence or an `Unknown` explanation.
9. A frozen result-relevant `Unknown` assumption blocks invariant terminal promotion.
10. Cross-contract aggregation is mechanical.
11. The published schema and semantic validator are jointly enforced; neither silently supersedes the other.

## Promotion

The accepted correction is promoted through:

- [`../../methodology/contract-discovery-protocol.md`](../../methodology/contract-discovery-protocol.md);
- [`../specification/far-intake-1.0.md`](../specification/far-intake-1.0.md);
- [`../../schemas/far-intake-v1.schema.json`](../../schemas/far-intake-v1.schema.json);
- [`../../mechanization/far_mechanization/intake_v1.py`](../../mechanization/far_mechanization/intake_v1.py);
- [`../../tests/test_far_intake_v1.py`](../../tests/test_far_intake_v1.py);
- the package console-entrypoint metadata;
- the FAR workflow, methodology, application, dependency, design, and investigation-validation surfaces.

## Nonclaims and permanent limits

This correction does not establish:

- that a bounded search is semantically or source-complete in an open domain;
- that every hidden assumption can be mechanically detected;
- that recorded source bytes have been independently retrieved merely because a locator and declared hash are stored;
- that recorded sources are factually correct or authoritative;
- that a single draft manifest proves its own pre-freeze edit history;
- that every Cartesian combination is meaningful outside the recorded scope;
- that `far-intake/1.0` is a universal, necessary, or minimal intake architecture;
- downstream `far-ir/2.x` contract adequacy merely from intake conformance;
- external validation, novelty, priority, empirical utility, or commercial value.

It changes no core-theory claim status and does not reinterpret `far-ir/2.0` or `far-ir/2.1`.
