# FAR governed intake 1.0 specification

Status: **governed methodology support format**

Format identifier: `far-intake/1.0`

Schema: [`../../schemas/far-intake-v1.schema.json`](../../schemas/far-intake-v1.schema.json)

Semantic validator: [`../../mechanization/far_mechanization/intake_v1.py`](../../mechanization/far_mechanization/intake_v1.py)

Governing method: [`../../methodology/contract-discovery-protocol.md`](../../methodology/contract-discovery-protocol.md)

## 1. Version boundary

`far-intake/1.0` is a pre-contract intake format. It does not replace, extend, or reinterpret `far-ir/2.0` or `far-ir/2.1`.

Its job is to make result-determining choices explicit before an exact comparison contract is evaluated.

## 2. Preserved raw input

`raw_input.text` preserves the supplied proposition or investigation input. `raw_input.sha256` is SHA-256 of its UTF-8 bytes.

Changing the raw input requires a new hash and invalidates any freeze derived from the prior input.

## 3. Discovery object

The `discovery` object contains:

- claim parses;
- material terms;
- source records;
- interpretations;
- interpretation exclusions;
- compatibility exclusions;
- assumptions;
- the bounded search protocol;
- contract candidates.

The semantic validator checks identifiers and references across these tables.

## 4. Provenance classes

Interpretations have one of three origins:

- `SOURCE_EXPLICIT`;
- `SOURCE_SYNTHESIS`;
- `INFERENCE`.

Source-explicit and source-synthesis rows require source references. Synthesis and inference rows require a written derivation.

The format therefore distinguishes source content from constructed or inferred content instead of flattening them into one field.

## 5. No-silent-pruning rule

For each claim parse, the validator determines the material terms and the active interpretations of each term.

It computes the Cartesian product of those interpretation sets. Every product element must appear as exactly one contract candidate unless the exact combination is present in `compatibility_exclusions`.

Interpretation exclusions do not delete interpretations. They preserve the rejected row plus reason and provenance.

## 6. Contract binding

Each candidate contains:

- a claim-parse identifier;
- the exact term-to-interpretation assignments;
- a downstream contract object;
- SHA-256 of canonical JSON for that contract object.

The intake validator does not claim that the downstream contract is valid `far-ir/2.0`; the appropriate downstream semantic verifier remains authoritative for that question.

## 7. Freeze

A manifest can be `DRAFT` or `FROZEN`.

Freezing requires a complete intake and no pre-existing evaluations. The freeze stores:

- the freeze timestamp;
- SHA-256 of canonical JSON for the exact `raw_input` plus the complete `discovery` object.

Any result-determining discovery change therefore invalidates the freeze hash.

## 8. Evaluation order

Evaluations are prohibited before freeze.

Each evaluation binds:

- the contract identifier;
- the candidate contract hash;
- a typed outcome;
- an evaluation timestamp;
- evidence references.

The evaluation timestamp must not predate the freeze.

## 9. Mechanical aggregation

The validator exposes a fixed aggregate over the complete frozen contract family:

- all `PROVED` -> `INVARIANTLY_PROVED`;
- all `REFUTED` -> `INVARIANTLY_REFUTED`;
- at least one `PROVED` and one `REFUTED` -> `CONTRACT_SENSITIVE`;
- any other complete combination -> `UNDERDETERMINED`;
- missing contract evaluation -> `INCOMPLETE`;
- semantic validation failure -> `INVALID`.

No ranking, weighting, majority vote, or preferred interpretation is introduced by this format.

## 10. CLI

The package exposes `far-intake`:

```bash
far-intake init "<raw input>" --id INTAKE-001 --write intake.json
far-intake validate intake.json --ready
far-intake freeze intake.json --write intake.frozen.json
far-intake aggregate intake.evaluated.json
```

`init` deliberately creates a draft with no inferred meanings. Interpretation discovery remains an evidence-producing research activity governed by the protocol.

## 11. Boundary

A valid frozen intake proves only that the recorded bounded discovery state is explicit, provenance-linked, complete relative to its active interpretation tables, contract-family complete under the recorded compatibility exclusions, and hash-bound before evaluation.

It does not prove open-world source completeness, semantic completeness, factual correctness of sources, external independence, or downstream contract adequacy.
