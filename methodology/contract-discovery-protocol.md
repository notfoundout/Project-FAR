# Contract Discovery Protocol

## Status

Accepted methodology correction.

## Purpose

This protocol governs the transition from under-specified input to the explicit comparison contracts required by FAR.

Its purpose is to prevent an investigator, model, or tool from silently selecting a result-determining interpretation, scope, frame, target class, or comparison objective before evaluation.

It does not establish facts about an application domain. It governs how candidate interpretations and contracts are discovered, recorded, frozen, and handed to the existing contract-relative evaluation machinery.

## Trigger

Run this protocol whenever the supplied input does not already determine every comparison parameter needed by the governing FAR claim type.

A missing parameter shall remain `Unknown` until supported. It shall not be filled from convention, model prior, unstated preference, or remembered context.

If the supplied input already contains a complete contract, record that fact and its provenance; do not manufacture alternative meanings without evidence of material ambiguity.

## Core Rule

No material interpretation may enter or leave the evaluated contract family silently.

A material interpretation is one whose substitution can change a required behavior, admissible case, evaluation outcome, scope boundary, or terminal verdict.

## Required Intake Record

The governed intake record uses `far-intake/1.0` and records:

- the exact raw input and its SHA-256;
- every retained claim parse;
- every material term;
- the bounded source search protocol and evidence cutoff;
- source identity, scope, retrieval time, and content hash;
- source-supported interpretations;
- explicit synthesis or inference steps;
- interpretation exclusions and their reasons;
- explicit assumptions and the consequence if each assumption is false;
- compatibility exclusions between otherwise active interpretations;
- the resulting contract family;
- the freeze hash binding all discovery inputs;
- only after freeze, per-contract evaluations.

The schema records shape. The semantic validator enforces provenance, coverage, hash binding, freeze order, and aggregation rules.

## Discovery Procedure

### 1. Preserve the input

Record the supplied input byte-for-byte as text and bind it by SHA-256.

Do not replace the input with a paraphrase.

### 2. Enumerate materially distinct parses

Record each materially distinct parse required to represent the input.

A parse inferred beyond the surface form must carry an explicit derivation.

Do not collapse parses merely because one is more familiar or convenient.

### 3. Identify material terms

A term is material when a supported change in its interpretation can change the contract or outcome.

Terms that cannot affect the result may be marked non-material. That classification remains auditable and revisable.

### 4. Search before interpretation selection

Run a recorded, bounded source search directed at materially distinct interpretations.

For each search record:

- the query;
- the target ambiguity;
- the source scope;
- the evidence cutoff;
- the stopping rule;
- saturation observations;
- known limitations.

Bounded saturation does not establish open-world semantic completeness. It establishes only that the recorded search stopped under the recorded rule.

### 5. Bind interpretations to provenance

Each interpretation must be classified as:

- `SOURCE_EXPLICIT` — directly stated by identified source material;
- `SOURCE_SYNTHESIS` — constructed from identified source material, with the synthesis written out;
- `INFERENCE` — introduced by reasoning, with the derivation written out.

Source-explicit and source-synthesis interpretations require source references. Synthesis and inference require an explicit derivation.

### 6. Preserve exclusions

An interpretation discovered during intake may be excluded only by an explicit exclusion record.

Allowed reason classes are:

- duplicate;
- wrong domain;
- anachronistic;
- unsupported;
- incompatible with the frozen scope;
- other, with a written reason.

The excluded interpretation remains in the manifest. Deletion is not an exclusion record.

### 7. Record assumptions

Every known result-relevant assumption must be listed with:

- its statement;
- whether it is explicit or `Unknown`;
- supporting sources, if any;
- what changes if it is false.

The protocol does not claim that a finite record proves the absence of all possible hidden assumptions. It makes detected assumptions reviewable and makes silent completion non-conforming.

### 8. Generate the complete bounded contract family

For each retained claim parse, take the Cartesian product of active interpretations for every material term.

Every admissible combination must correspond to exactly one contract candidate.

A combination may be removed only through an explicit compatibility exclusion with a reason and provenance.

This requirement prevents cherry-picking one supported interpretation while silently omitting another.

### 9. Freeze before evaluation

No contract outcome may be recorded while the intake manifest is `DRAFT`.

A frozen manifest binds the exact raw input plus the complete discovery object by canonical SHA-256. Any change to parses, terms, sources, interpretations, exclusions, assumptions, search protocol, or contract candidates invalidates the freeze.

Each contract candidate independently binds its downstream contract object by SHA-256.

### 10. Evaluate exact frozen candidates

Evaluation occurs only after freeze.

Each result must reference the frozen contract identifier and exact contract hash. Evaluation time must not predate the freeze.

The downstream evaluator remains responsible for the existing `far-ir/2.0` or successor contract checks.

### 11. Aggregate mechanically

Once every frozen contract candidate has an evaluation, the aggregate is determined without analyst discretion:

| Frozen per-contract outcomes | Aggregate |
|---|---|
| all `PROVED` | `INVARIANTLY_PROVED` |
| all `REFUTED` | `INVARIANTLY_REFUTED` |
| at least one `PROVED` and at least one `REFUTED` | `CONTRACT_SENSITIVE` |
| any other complete mixture | `UNDERDETERMINED` |
| any frozen candidate missing an evaluation | `INCOMPLETE` |
| intake validation failure | `INVALID` |

The aggregate rule must not be changed after outcomes are known.

## Failure Conditions

The intake is non-conforming if any of the following occurs:

- raw input is altered without a new intake identity;
- a material interpretation lacks required provenance;
- synthesis or inference is presented as source-explicit;
- a discovered interpretation disappears without an exclusion record;
- an admissible interpretation combination is omitted from the contract family;
- evaluation begins before freeze;
- evaluation refers to a contract whose hash differs from the frozen candidate;
- a frozen discovery object is modified without invalidating the freeze;
- a terminal aggregate is selected by judgment instead of the fixed aggregation rule.

## Boundary

This protocol reduces untracked analyst freedom. It does not prove that a bounded search found every meaning, every source, or every assumption in an open domain.

Claims of source completeness, semantic completeness, authority, or domain adequacy require their own evidence and scope.

The protocol is methodology. It does not alter the current core theory or the semantics of `far-ir/2.0`.
