# FAR Compare and Adjudication Interface v1.0

Status: proposed stable interface in PR #369. Authority: issue #368.

## Purpose

This interface performs two operations that must remain separate:

1. `compare` mechanically compares two bounded FAR evidence packages.
2. `adjudicate` records a human, policy, or domain decision about every comparison finding.

Neither operation is a truth oracle. Comparison reports structure and differences. Adjudication records a decision, its rationale, supporting references, limitations, and dissent.

## Commands

```bash
far-evidence validate-package package.json --output-file canonical-package.json
far-evidence compare left.json right.json --output-file comparison.json
far-evidence adjudicate comparison.json adjudication-input.json --output-file adjudication.json
```

The equivalent module invocation is:

```bash
python -m mechanization.far_mechanization.compare_adjudication ...
```

All successful output is canonical UTF-8 JSON with sorted object keys, deterministic set-like arrays, a trailing newline, and content-derived identifiers. Validation failures return exit code `2` and write an explanation to stderr.

## Evidence package contract

Schema: `far-evidence-package/1.0`.

Each package contains:

- a stable `package_id` and `subject_id`;
- one or more uniquely identified claims;
- a claim status from the closed v1.0 vocabulary;
- explicit support references, assumptions, contradiction references, and boundaries;
- optional scalar-only metadata.

The closed claim-status vocabulary is:

- `observed`
- `derived`
- `inferred`
- `declared`
- `unknown`
- `contradicted`
- `unverifiable`

Unknown fields, duplicate identifiers, duplicate set-like values, nested metadata, unsupported statuses, and contradiction references to absent claims fail closed.

## Mechanical comparison contract

Schema: `far-evidence-comparison/1.0`.

The comparison records canonical SHA-256 hashes of the left and right packages. Orientation is preserved: reversing the packages produces a different comparison ID. Each claim ID produces exactly one finding classified as:

- `agreement`
- `contradiction`
- `left_only`
- `right_only`
- `unresolved`

The finding includes both bounded claim records where present and exact differences in support, assumptions, and boundaries. The comparison does not select a winner or convert a claim into truth.

## Adjudication contract

Schema: `far-evidence-adjudication/1.0`.

An adjudication must bind to the canonical comparison SHA-256 and explicitly decide every finding. Permitted dispositions are:

- `accept_left`
- `accept_right`
- `combine`
- `unresolved`
- `out_of_scope`

Each decision requires rationale, support references, and limitations. Dissent is preserved as a first-class list. Missing findings, duplicate decisions, unknown findings, stale comparison hashes, forged content IDs, unsupported dispositions, and extra fields fail closed.

## Stable identifiers and serialization

Package hashes are computed after package normalization. Comparison and finding IDs are derived from the schema version, oriented package hashes, and claim ID. Adjudication IDs are derived from the canonical adjudication content excluding the ID field itself.

The v1.0 serialization contract is part of artifact identity. A producer must not add timestamps, random identifiers, implicit defaults, or environment-dependent ordering to canonical artifacts.

## Versioning rules

Changes that alter required fields, permitted vocabularies, comparison classification, hash material, canonical ordering, ID derivation, or validation behavior require a new major schema version.

Backward-compatible documentation corrections and additional non-authoritative examples do not change the schema version. A future version must not silently reinterpret v1.0 artifacts; migration must be explicit and produce a new artifact with a new schema identifier.

## Claim boundary

Passing this interface proves only that the artifacts conform to the frozen v1.0 contract and that the recorded hashes and references are internally consistent. It does not prove factual correctness, domain adequacy, fairness, policy legitimacy, certification, external validation, or commercial readiness.


## Core-theory conformance note

This evidence interface compares declared package contents; it is not the full comparison contract of `PROJECT-FAR-CORE-THEORY-1.0`. A representation-sufficiency claim additionally requires cases, tests/contexts, typed outcomes, observation semantics, a representation mapping, and either a decoder/factorization certificate or a collision witness. Evidence-package agreement cannot substitute for that proof.
