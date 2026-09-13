# Contract Discovery Protocol

## Status

Accepted methodology correction.

## Purpose

This protocol governs the transition from under-specified input to the explicit comparison contracts required by FAR.

Its purpose is to prevent an investigator, model, or tool from silently selecting a result-determining parse, interpretation, scope, frame, target class, or comparison objective before evaluation.

It does not establish facts about an application domain. It governs how candidate parses, interpretations, assumptions, exclusions, materiality decisions, and contracts are discovered, recorded, frozen, and handed to the existing contract-relative evaluation machinery.

## Trigger

Run this protocol unless the supplied artifact is itself an explicit machine-readable downstream comparison contract accepted by the applicable contract schema and semantic validator.

A missing parameter remains `Unknown` until supported. It shall not be filled from convention, model prior, unstated preference, or remembered context.

Intake bypass requires the investigation to record the supplied contract artifact's exact format/version, content hash, and successful applicable validation result. A prose claim that the input is complete, already defines the contract, or makes intake unnecessary is not sufficient. If the supplied artifact fails downstream contract validation or leaves a result-determining parameter outside the artifact, this protocol applies.

A validated supplied contract need not have speculative alternative meanings manufactured without evidence of material ambiguity.

## Core Rule

No material parse, interpretation, assumption, exclusion, materiality classification, or contract parameter may enter or leave the evaluated family silently.

A difference is material when substituting it can change a required behavior, admissible case, evaluation outcome, scope boundary, or terminal verdict.

The governed machine-readable intake is strict JSON. Transport parsing and programmatic validation must not admit Python-only values, duplicate object keys, or non-finite numeric extensions that cannot be represented unambiguously in the governed JSON artifact.

## Required Intake Record

The governed intake record uses `far-intake/1.0` and records:

- the exact raw input and SHA-256;
- every retained claim parse and any explicit parse exclusions;
- every term, its materiality classification, the basis for that classification, and the effect if misclassified;
- the bounded source-search protocol and evidence cutoff;
- source identity, scope, retrieval time, and declared content hash;
- source-supported interpretations;
- explicit synthesis and inference steps;
- interpretation and compatibility exclusions with auditable bases;
- explicit assumptions and the consequence if each is false;
- the complete bounded contract family;
- provenance for every leaf parameter in every candidate downstream contract;
- a freeze identity binding the exact intake state before evaluation;
- only after freeze, hash-bound per-contract evaluations.

The JSON data-model gate runs before the JSON Schema. The JSON Schema then governs document shape, and the semantic validator enforces provenance, coverage, chronology, hash binding, freeze order, and aggregation rules.

## Discovery Procedure

### 1. Preserve the input

Record the supplied input as text and bind it by SHA-256.

Do not substitute a paraphrase for the recorded input.

Cryptographic immutability begins at freeze. A single draft manifest cannot prove its own prior draft history; therefore any pre-freeze edits must remain reviewable through the surrounding version-control or investigation record when historical reconstruction matters.

### 2. Enumerate materially distinct parses

Record each materially distinct parse required to represent the input.

A parse inferred beyond the surface form requires an explicit derivation.

Do not collapse parses merely because one is more familiar or convenient.

A discovered parse may be removed from the active family only through an explicit parse-exclusion record. At least one parse must remain active at freeze.

### 3. Identify material terms and bind the classification

A term is material when a supported change in its interpretation can change the contract or outcome.

Terms that cannot affect the result may be marked non-material, but the material/non-material decision is itself result-relevant and must remain auditable. Every term therefore records:

- `material`;
- `materiality_basis` as `SOURCE`, `RAW_INPUT`, or `INFERENCE`;
- source references when the basis is `SOURCE`;
- an explicit derivation when the basis is `RAW_INPUT` or `INFERENCE`;
- `effect_if_misclassified`.

Every material term in an active parse must retain at least one active interpretation before freeze.

### 4. Search before interpretation selection

Run a recorded, bounded source search directed at materially distinct parses and interpretations.

Each registered query records:

- the query text;
- its target ambiguity;
- the source scope;
- the material term identifiers it targets;
- the claim-parse identifiers it targets.

Every active material term and active claim parse must have recorded search coverage.

The search protocol additionally records:

- the evidence cutoff;
- the stopping rule;
- saturation observations;
- known limitations.

Each saturation observation records its time, executed query identifiers, sources considered, and newly found material parses or interpretations. Registered queries and registered sources must appear in saturation provenance.

Termination requires a final saturation observation that both (a) reports no new material parse or material interpretation and (b) itself enumerates every registered query and every registered source. Cumulative coverage from older rounds is insufficient: a query or source last considered only in a prior round has not been rechecked under the terminal zero-new pass and cannot support a saturation stop.

Bounded saturation does not establish open-world semantic completeness. It establishes only that the complete recorded query/source registry was rechecked in the terminal bounded pass and stopped under the recorded rule.

### 5. Bind interpretations to provenance

Each interpretation is classified as:

- `SOURCE_EXPLICIT` — directly stated by identified source material;
- `SOURCE_SYNTHESIS` — constructed from identified source material, with the synthesis written out;
- `INFERENCE` — introduced by reasoning, with the derivation written out.

Source-explicit and source-synthesis interpretations require source references. Synthesis and inference require explicit derivation.

### 6. Preserve exclusions with an auditable basis

A discovered parse, interpretation, or interpretation combination may be excluded only by an explicit exclusion record.

Interpretation and parse exclusions retain the excluded item in the manifest. Deletion is not an exclusion record.

Allowed exclusion reason classes are:

- duplicate;
- wrong domain;
- anachronistic;
- unsupported;
- incompatible with the frozen scope;
- other, with a written reason.

Every exclusion also records one of these bases:

- `SOURCE` — requires non-empty source provenance;
- `RAW_INPUT` — requires an explicit derivation from the preserved input;
- `INFERENCE` — requires an explicit reasoning derivation.

An analyst-written reason by itself cannot prune a result-determining interpretation or contract combination.

### 7. Record assumptions

Every known result-relevant assumption must be listed with:

- its statement;
- status `EXPLICIT` or `Unknown`;
- supporting sources, if any;
- what changes if it is false.

The protocol does not claim that a finite record proves the absence of all possible hidden assumptions. It makes detected assumptions reviewable and makes silent completion non-conforming.

If any frozen result-relevant assumption remains `Unknown`, the cross-contract aggregate cannot be promoted to an invariant proved or refuted verdict; it remains `UNDERDETERMINED` even if all candidate evaluations happen to agree.

### 8. Generate the complete bounded contract family

For each active claim parse, take the Cartesian product of active interpretations for every material term.

Every admissible combination must correspond to exactly one contract candidate.

A retained parse with zero material terms still contributes exactly one candidate with an empty assignment map. This is the singleton Cartesian product, not an omitted parse.

A combination may be removed only through an explicit compatibility exclusion satisfying the exclusion-basis rules above.

This requirement prevents cherry-picking one supported interpretation or parse while silently omitting another.

### 9. Bind every candidate contract parameter to provenance

Completeness of the interpretation assignments is not sufficient if an analyst can silently add result-determining fields inside the downstream contract object.

Every scalar or empty-container leaf in each candidate contract therefore requires exactly one `parameter_provenance` record naming its JSON Pointer path and one of these bases:

- `RAW_INPUT` — the value is derived from the preserved input;
- `SOURCE` — the value is supported by identified source records;
- `INTERPRETATION` — the value is supported by interpretations selected in that candidate's assignment map;
- `ASSUMPTION` — the value is supported by an explicitly declared assumption;
- `INFERENCE` — the value is introduced by an explicit derivation.

Source-, interpretation-, and assumption-based rows must reference the corresponding existing records. Interpretation references may not reach outside the candidate's selected assignments. Every provenance row carries an explicit derivation/trace statement, and no provenance row may point to a non-leaf or duplicate path.

This is a traceability requirement. It does not establish that the resulting downstream contract is substantively adequate; `far-ir/2.0` or its successor remains authoritative for downstream contract conformance.

### 10. Freeze after discovery and before evaluation

No contract outcome may be recorded while the intake manifest is `DRAFT`.

Freeze time must be no earlier than the evidence cutoff, all recorded source retrieval times, and all saturation-observation times.

A frozen manifest records:

- `intake_sha256` — SHA-256 of canonical JSON for the exact `raw_input` plus complete `discovery` object;
- `freeze_sha256` — SHA-256 of canonical JSON binding `intake_sha256` to the exact freeze timestamp.

Any change to raw input, parses, exclusions, terms, materiality records, sources, interpretations, assumptions, search protocol, contract candidates, contract-parameter provenance, or freeze timestamp invalidates the corresponding binding.

Each contract candidate independently binds its downstream contract object by SHA-256.

### 11. Evaluate exact frozen candidates

Evaluation occurs only after freeze.

Each evaluation must reference:

- the frozen contract identifier;
- the exact candidate contract hash;
- the exact `freeze_sha256`;
- a typed outcome;
- a post-freeze evaluation timestamp.

Every non-`Unknown` outcome requires at least one evidence reference. An `Unknown` outcome requires an explanatory note.

The downstream evaluator remains responsible for the existing `far-ir/2.0` or successor contract checks.

### 12. Aggregate mechanically

Once every frozen contract candidate has an evaluation, the aggregate is determined without analyst discretion:

| Frozen per-contract state | Aggregate |
|---|---|
| any result-relevant assumption remains `Unknown` | `UNDERDETERMINED` |
| all `PROVED` | `INVARIANTLY_PROVED` |
| all `REFUTED` | `INVARIANTLY_REFUTED` |
| at least one `PROVED` and at least one `REFUTED` | `CONTRACT_SENSITIVE` |
| any other complete mixture | `UNDERDETERMINED` |
| any frozen candidate missing an evaluation | `INCOMPLETE` |
| intake validation failure | `INVALID` |

The aggregate rule must not be changed after outcomes are known.

## Failure Conditions

The intake is non-conforming if any of the following occurs:

- intake is bypassed without an exact supplied machine-readable contract artifact, recorded format/version and content hash, and successful applicable downstream validation;
- the input tree contains values outside the strict JSON data model, or CLI JSON contains duplicate object keys or non-finite numeric extensions;
- the document violates the published schema;
- a material parse disappears without an exclusion record;
- a material interpretation lacks required provenance or derivation;
- a materiality classification lacks its required auditable basis or effect-if-misclassified record;
- an exclusion lacks an auditable source/raw-input/inference basis;
- an active parse or material term lacks registered search coverage;
- registered queries or sources are absent from saturation provenance;
- the final zero-new saturation observation fails to recheck every registered query and every registered source;
- freeze is declared before recorded discovery evidence is complete;
- an admissible interpretation combination is omitted from the contract family;
- a zero-material retained parse has no singleton contract;
- a candidate downstream contract contains an untraced leaf parameter or provenance outside that candidate's selected records;
- evaluation begins before freeze;
- evaluation refers to a different candidate or freeze hash;
- a non-`Unknown` evaluation carries no evidence reference;
- an `Unknown` evaluation carries no explanation;
- a frozen intake or freeze timestamp is modified without invalidating its hash;
- an unresolved `Unknown` assumption is ignored during aggregation;
- a terminal aggregate is selected by judgment instead of the fixed rule.

## Boundary

This protocol reduces untracked analyst freedom. It does not prove that a bounded search found every meaning, source, parse, assumption, or possible contract parameter in an open domain.

A source record preserves a locator and declared content hash; the intake validator does not independently retrieve external bytes to prove that the declared hash matches the remote source. Retrieval and independent source verification remain provenance/replication obligations.

Claims of source completeness, semantic completeness, authority, factual correctness, normative contract selection, or domain adequacy require their own evidence and scope. In particular, this protocol does not close `LIM-038`: it makes bounded contract construction auditable but does not prove a uniquely unbiased or universally acceptable contract.

The protocol is methodology. It does not alter the current core theory or the semantics of `far-ir/2.0` or `far-ir/2.1`.
