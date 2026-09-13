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

The accepted instance domain is strict JSON. CLI parsing rejects duplicate object keys and the non-standard `NaN`, `Infinity`, and `-Infinity` tokens. Programmatic callers are checked recursively before schema validation: objects must be Python `dict` values with string keys, arrays must be Python `list` values, and scalars must be exactly JSON-native string, integer, finite float, boolean, or null values. Python-only containers, custom scalar subclasses, non-string object keys, and non-finite floats are rejected before they can reach schema semantics or canonical hashing.

The published JSON Schema is normative for document shape after that JSON-domain gate. The semantic validator applies the schema and stops semantic interpretation of a schema-invalid document.

Strings and object keys must encode as UTF-8; unpaired surrogates are rejected. Cyclic programmatic containers and nesting beyond the runtime's supported depth produce validation errors. Freeze validates shape before reading fields. Validation, freeze, aggregation, and the installed CLI share this boundary without import-time rebinding, so reloading the public module does not change validation behavior.

The repository's constrained local JSON Schema engine implements the structural keywords used by this format, including Draft 2020-12 numeric type semantics, regex-search semantics for `pattern`, array/object cardinality and uniqueness, and schema-valued `additionalProperties`. In particular, mathematically integral finite JSON numbers such as `1.0` satisfy `type: integer`, while booleans do not. Optional format assertions remain outside the local validator's decidable enforcement boundary unless separately checked semantically.

Semantic checks then enforce cross-reference validity, provenance, complete bounded family coverage, chronology, hash binding, terminal saturation coverage, and aggregation.

This order prevents the implementation from accepting records the published schema rejects within the supported schema subset and prevents Python-only values from creating a larger programmatic instance domain than the JSON format itself.

## 3. Preserved raw input

`raw_input.text` preserves the supplied proposition or investigation input. `raw_input.sha256` is SHA-256 of its UTF-8 bytes.

Changing a frozen raw input invalidates the intake freeze. A single draft manifest does not cryptographically preserve its own earlier draft history; version control or an external investigation log is required when pre-freeze edit history must be reconstructed.

## 4. Discovery object

The `discovery` object contains:

- claim parses and explicit claim-parse exclusions;
- terms and provenance-bearing materiality classifications;
- source records;
- interpretations;
- interpretation exclusions;
- compatibility exclusions;
- assumptions;
- the bounded search protocol;
- contract candidates and leaf-level contract-parameter provenance.

The semantic validator checks identifiers and references across these tables.

## 5. Materiality provenance

Every term records whether it is material and why that classification is permitted to affect the contract family.

The fields are:

- `material`;
- `materiality_basis` (`SOURCE`, `RAW_INPUT`, or `INFERENCE`);
- `materiality_source_ids`;
- `materiality_derivation`;
- `effect_if_misclassified`.

`SOURCE` requires source provenance. `RAW_INPUT` and `INFERENCE` require an explicit derivation. This prevents an untracked `material: false` choice from silently deleting a result-relevant ambiguity.

## 6. Interpretation provenance

Interpretations have one of three origins:

- `SOURCE_EXPLICIT`;
- `SOURCE_SYNTHESIS`;
- `INFERENCE`.

Source-explicit and source-synthesis rows require source references. Synthesis and inference rows require a written derivation.

The format therefore distinguishes source content from constructed or inferred content instead of flattening them into one field.

## 7. Exclusion provenance

Claim-parse, interpretation, and compatibility exclusions cannot rest on an analyst-written reason alone.

Every exclusion has an auditable basis:

- `SOURCE` — requires non-empty source references;
- `RAW_INPUT` — requires an explicit derivation from the preserved input;
- `INFERENCE` — requires an explicit reasoning derivation.

Interpretation and parse exclusions preserve the excluded item in the manifest. Deleting an item is not equivalent to recording its exclusion.

## 8. Search and saturation record

Each search query records its text, target, source scope, material term identifiers, and claim-parse identifiers.

At freeze readiness:

- every active material term has query coverage;
- every active claim parse has query coverage;
- every registered query appears in saturation execution provenance;
- every registered source appears in saturation provenance;
- saturation round numbers are unique and strictly increasing, and their timestamps are nondecreasing in that order (equivalent instants across timezones are allowed);
- an observation cannot predate a source it claims to include;
- source retrievals and saturation observations must be no later than the evidence cutoff;
- the final saturation observation records no new material parse or material interpretation; and
- that same final zero-new observation must itself enumerate every registered query and every registered source.

Earlier rounds may establish discovery history, but their cumulative coverage cannot substitute for the complete terminal recheck. A search therefore cannot terminate merely because a subset of the registry produced no new material result while another registered query or source was last considered only in an earlier round.

These checks establish bounded procedural completion only. They do not prove open-world semantic completeness.

## 9. No-silent-pruning rule

For each active claim parse, the validator determines its material terms and each term's active interpretations.

Every element of the Cartesian product of those interpretation sets must appear as exactly one contract candidate unless that exact combination has a valid compatibility exclusion. The validator checks membership and uniqueness, then compares exact cardinalities after exclusions; it does not enumerate an exponentially large absent family merely to reject an incomplete record.

A retained parse with no material terms contributes one singleton candidate with an empty assignment object. It is not silently omitted.

At least one claim parse must remain active.

## 10. Contract binding and parameter provenance

Each candidate contains:

- a claim-parse identifier;
- the exact material term-to-interpretation assignments;
- a downstream contract object;
- SHA-256 of canonical JSON for that contract object;
- `parameter_provenance` covering every scalar or empty-container leaf in the downstream contract.

Each provenance row identifies the leaf by JSON Pointer and classifies its basis as `RAW_INPUT`, `SOURCE`, `INTERPRETATION`, `ASSUMPTION`, or `INFERENCE`. It records the applicable source, interpretation, and assumption identifiers plus an explicit derivation/trace statement. Interpretation-based provenance may reference only interpretations selected by that candidate.

The validator rejects duplicate provenance paths, missing leaf paths, provenance for non-leaf paths, unknown references, and interpretation references outside the candidate assignment map.

The intake validator does not claim that the downstream contract is valid `far-ir/2.0`; the appropriate downstream semantic verifier remains authoritative for that question. Non-JSON-native or non-canonical-JSON contract values are rejected rather than causing an uncaught exception.

## 11. Freeze identity and chronology

A manifest can be `DRAFT` or `FROZEN`.

Frozen records always require complete intake validation; passing `require_complete=False` cannot disable that requirement. An explicitly supplied invalid freeze timestamp is rejected rather than silently replaced by the current time.

Freezing requires a complete intake and no pre-existing evaluations. Freeze time may not predate:

- the evidence cutoff;
- any registered source retrieval;
- any saturation observation.

The freeze stores:

- `intake_sha256` — SHA-256 of canonical JSON for the exact `raw_input` plus complete `discovery` object;
- `freeze_sha256` — SHA-256 of canonical JSON for `{intake_sha256, frozen_at}`.

Changing any frozen discovery input, including materiality or parameter-provenance records, or changing the freeze timestamp invalidates the corresponding hash.

## 12. Evaluation order and evidence

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

## 13. Mechanical aggregation

The validator exposes a fixed aggregate over the complete frozen contract family:

- any frozen result-relevant assumption still `Unknown` -> `UNDERDETERMINED`;
- all `PROVED` -> `INVARIANTLY_PROVED`;
- all `REFUTED` -> `INVARIANTLY_REFUTED`;
- at least one `PROVED` and one `REFUTED` -> `CONTRACT_SENSITIVE`;
- any other complete combination -> `UNDERDETERMINED`;
- missing contract evaluation -> `INCOMPLETE`;
- validation failure -> `INVALID`.

No ranking, weighting, majority vote, or preferred interpretation is introduced by this format.

## 14. CLI and packaging

The package exposes `far-intake` alongside the existing `far` and `far-evidence` console entrypoints:

```bash
far-intake init "<raw input>" --id INTAKE-001 --write intake.json
far-intake validate intake.json --ready
far-intake freeze intake.json --write intake.frozen.json
far-intake aggregate intake.evaluated.json
```

The CLI accepts strict JSON rather than Python's permissive JSON extensions: duplicate object keys and non-finite numeric tokens are errors, not silently normalized inputs.

Non-editable wheels include the runtime and schema. Relocation coverage both imports the extracted wheel with site initialization disabled and installs it into a fresh virtual environment to execute the generated `far-intake` script through draft, readiness, freeze, evaluation aggregation, and tamper rejection.

`init` deliberately creates a draft with no inferred meanings. Interpretation discovery remains an evidence-producing research activity governed by the protocol.

## 15. Boundary

A valid frozen intake establishes only that the recorded bounded discovery state is explicit, provenance-linked, complete relative to its active tables and exclusions, terminally rechecked across the registered query/source set, chronologically ordered, and cryptographically bound before evaluation.

It does not establish:

- open-world source, parse, interpretation, assumption, or contract-parameter completeness;
- factual correctness or authority of a source merely because its locator and declared hash are recorded;
- independent retrieval of external source bytes;
- a uniquely unbiased or universally acceptable contract (`LIM-038` remains open);
- downstream contract adequacy;
- external independence, novelty, priority, empirical utility, or commercial value.
