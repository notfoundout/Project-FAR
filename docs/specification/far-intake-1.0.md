# FAR governed intake 1.0 specification

Status: **governed methodology support format**

Format identifier: `far-intake/1.0`

Schema: [`../../schemas/far-intake-v1.schema.json`](../../schemas/far-intake-v1.schema.json)

Semantic validator: [`../../mechanization/far_mechanization/intake_v1.py`](../../mechanization/far_mechanization/intake_v1.py)

Governing method: [`../../methodology/contract-discovery-protocol.md`](../../methodology/contract-discovery-protocol.md)

## 1. Version boundary

`far-intake/1.0` is a pre-contract intake format. It does not replace, extend, or reinterpret `far-ir/2.0` or `far-ir/2.1`.

Its job is to make result-determining choices explicit before a comparison contract is evaluated.

## 2. Validation order

The published JSON Schema is normative for document shape. The semantic validator applies the schema first and stops semantic interpretation of a schema-invalid document.

Semantic checks then enforce cross-reference validity, provenance, complete bounded family coverage, chronology, hash binding, and aggregation.

This order prevents the implementation from accepting records the published schema rejects.

## 3. Preserved raw input

`raw_input.text` preserves the supplied proposition or investigation input. `raw_input.sha256` is SHA-256 of its UTF-8 bytes.

Changing a frozen raw input invalidates the intake freeze. A single draft manifest does not cryptographically preserve its own earlier draft history; version control or an external investigation log is required when pre-freeze edit history must be reconstructed.

## 4. Discovery object

The `discovery` object contains:

- claim parses and explicit claim-parse exclusions;
- terms and their materiality classification;
- source records;
- interpretations;
- interpretation exclusions;
- compatibility exclusions;
- assumptions;
- the bounded search protocol;
- contract candidates.

The semantic validator checks identifiers and references across these tables.

## 5. Interpretation provenance

Interpretations have one of three origins:

- `SOURCE_EXPLICIT`;
- `SOURCE_SYNTHESIS`;
- `INFERENCE`.

Source-explicit and source-synthesis rows require source references. Synthesis and inference rows require a written derivation.

The format therefore distinguishes source content from constructed or inferred content instead of flattening them into one field.

## 6. Exclusion provenance

Claim-parse, interpretation, and compatibility exclusions cannot rest on an analyst-written reason alone.

Every exclusion has an auditable basis:

- `SOURCE` — requires non-empty source references;
- `RAW_INPUT` — requires an explicit derivation from the preserved input;
- `INFERENCE` — requires an explicit reasoning derivation.

Interpretation and parse exclusions preserve the excluded item in the manifest. Deleting an item is not equivalent to recording its exclusion.

## 7. Search and saturation record

Each search query records its text, target, source scope, material term identifiers, and claim-parse identifiers.

At freeze readiness:

- every active material term has query coverage;
- every active claim parse has query coverage;
- every registered query appears in saturation execution provenance;
- every registered source appears in saturation provenance;
- saturation observations are timestamped and ordered;
- an observation cannot predate a source it claims to include;
- source retrievals and saturation observations must be no later than the evidence cutoff;
- the final saturation observation records no new material parse or material interpretation.

These checks establish bounded procedural completion only. They do not prove open-world semantic completeness.

## 8. No-silent-pruning rule

For each active claim parse, the validator determines its material terms and each term's active interpretations.

It computes the Cartesian product of those interpretation sets. Every product element must appear as exactly one contract candidate unless that exact combination has a valid compatibility exclusion.

A retained parse with no material terms contributes one singleton candidate with an empty assignment object. It is not silently omitted.

At least one claim parse must remain active.

## 9. Contract binding

Each candidate contains:

- a claim-parse identifier;
- the exact material term-to-interpretation assignments;
- a downstream contract object;
- SHA-256 of canonical JSON for that contract object.

The intake validator does not claim that the downstream contract is valid `far-ir/2.0`; the appropriate downstream semantic verifier remains authoritative for that question.

Non-canonical-JSON contract values are rejected rather than causing an uncaught exception.

## 10. Freeze identity and chronology

A manifest can be `DRAFT` or `FROZEN`.

Freezing requires a complete intake and no pre-existing evaluations. Freeze time may not predate:

- the evidence cutoff;
- any registered source retrieval;
- any saturation observation.

The freeze stores:

- `intake_sha256` — SHA-256 of canonical JSON for the exact `raw_input` plus complete `discovery` object;
- `freeze_sha256` — SHA-256 of canonical JSON for `{intake_sha256, frozen_at}`.

Changing any frozen discovery input or changing the freeze timestamp invalidates the corresponding hash.

## 11. Evaluation order and evidence

Evaluations are prohibited before freeze.

Each evaluation binds:

- the contract identifier;
- the candidate contract hash;
- the exact `freeze_sha256`;
- a typed outcome;
- an evaluation timestamp;
- evidence references;
- an explanatory note when the outcome is `Unknown`.

The evaluation timestamp must not predate the freeze. Every non-`Unknown` outcome requires at least one evidence reference.

## 12. Mechanical aggregation

The validator exposes a fixed aggregate over the complete frozen contract family:

- any frozen result-relevant assumption still `Unknown` -> `UNDERDETERMINED`;
- all `PROVED` -> `INVARIANTLY_PROVED`;
- all `REFUTED` -> `INVARIANTLY_REFUTED`;
- at least one `PROVED` and one `REFUTED` -> `CONTRACT_SENSITIVE`;
- any other complete combination -> `UNDERDETERMINED`;
- missing contract evaluation -> `INCOMPLETE`;
- validation failure -> `INVALID`.

No ranking, weighting, majority vote, or preferred interpretation is introduced by this format.

## 13. CLI and packaging

The package exposes `far-intake` alongside the existing `far` and `far-evidence` console entrypoints:

```bash
far-intake init "<raw input>" --id INTAKE-001 --write intake.json
far-intake validate intake.json --ready
far-intake freeze intake.json --write intake.frozen.json
far-intake aggregate intake.evaluated.json
```

`init` deliberately creates a draft with no inferred meanings. Interpretation discovery remains an evidence-producing research activity governed by the protocol.

## 14. Boundary

A valid frozen intake establishes only that the recorded bounded discovery state is explicit, provenance-linked, complete relative to its active tables and exclusions, chronologically ordered, and cryptographically bound before evaluation.

It does not establish:

- open-world source, parse, interpretation, or assumption completeness;
- factual correctness or authority of a source merely because its locator and declared hash are recorded;
- independent retrieval of external source bytes;
- downstream contract adequacy;
- external independence, novelty, priority, empirical utility, or commercial value.
