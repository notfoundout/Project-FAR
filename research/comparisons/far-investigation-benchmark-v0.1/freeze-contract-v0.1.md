# FAR Investigation Benchmark — Freeze Contract v0.1

Status: PREPARED / normative for transition from `prepared` to `frozen`  
Parent: `research/comparisons/far-investigation-benchmark-v0.1.md`

## Purpose

A campaign may enter `frozen` status only when every choice that can affect case selection, execution, scoring, or confirmatory analysis is represented by an immutable artifact and bound by SHA-256 in the campaign manifest. A status edit by itself never constitutes a freeze.

The pre-S1 hardening amendment is normative and is itself part of the frozen bundle. The validator must reject any frozen campaign whose artifacts contradict the amendment or the reconciled protocol files.

## Required static protocol artifacts

The campaign `artifacts` array must bind the current bytes of:

- `research/comparisons/far-investigation-benchmark-v0.1.md`;
- `research/comparisons/far-investigation-benchmark-v0.1/hardening-amendment-v0.1.md`;
- `research/comparisons/far-investigation-benchmark-v0.1/freeze-contract-v0.1.md`;
- `research/comparisons/far-investigation-benchmark-v0.1/case-selection-protocol-v0.1.md`;
- `research/comparisons/far-investigation-benchmark-v0.1/adjudication-rubric-v0.1.md`;
- `research/comparisons/far-investigation-benchmark-v0.1/reference-evidence-protocol-v0.1.md`;
- `research/comparisons/far-investigation-benchmark-v0.1/condition-contracts-v0.1.md`;
- `research/comparisons/far-investigation-benchmark-v0.1/resource-budget-v0.1.json`;
- `research/comparisons/far-investigation-benchmark-v0.1/analysis-parameters-v0.1.json`.

Every required static artifact must have `verify_current_path = true`, a nonzero SHA-256, and a byte-for-byte hash match.

## Required generated pre-execution artifacts

The following files must exist, be listed in `artifacts`, use `verify_current_path = true`, and match their recorded SHA-256 before the first condition run:

- `candidate-frame.jsonl` — complete discovery ledger, including rejected candidates, claim-family memberships, and canonical representatives;
- `cases.jsonl` — exactly 60 final case records, exactly 10 for each canonical textual stratum ID;
- `replacement-frame.jsonl` — at least 10 ordered unused canonical claim-family representatives per stratum;
- `case-selection-config.json` — discovery queries, source classes, source cutoff, retrieval configuration, seed, normalization rules, claim-clustering rule, and selection-key test vector;
- `case-selection-declarations.json` — exactly two selector declarations plus one clustering-adjudicator declaration, with distinct IDs/identities and substantive independence/exposure/conflict declarations;
- `condition-prompts.json` — exact prompt bytes for F/B0/B1/B2 encoded as base64 plus per-surface SHA-256 and deterministic case-prompt rendering rule;
- `execution-schedule.json` — all 240 case-condition runs in the exact globally hashed order with stable run IDs, schedule keys, indices, and cache nonces;
- `adjudication-schedule.json` — deterministic 240-packet presentation schedule for each of the two unitizers and two primary scorers;
- `reference-search-config.json` — reference-panel query templates, retrieval configuration, source cutoff, search/tool-call budget, source-chain limits, and researcher declarations;
- `reference-evidence-manifest.json` — one locked entry per final case, with a positive material-evidence denominator and hashes of the per-case reference-evidence records;
- `environment-lock.json` — immutable model/provider identifier or strongest available snapshot/fingerprint, provider settings, tool versions, retrieval settings, dependency/runtime versions, retry policy, and the provider-documented cache/session-isolation mechanism;
- `mutation-config.json` — exact mutation families, generator/version identity, seed or deterministic construction rule, and sealing procedure;
- `far-treatment-source-manifest.json` — every transitive methodology/schema/architecture source that defines condition F and is required by the benchmark validator.

No generated freeze artifact may contain an unresolved sentinel such as `TO_BE_*`, `UNASSIGNED`, `PLACEHOLDER`, or a `*_NOT_FROZEN` status.

## Required source bindings

The campaign `source_manifest` must be nonempty and must bind the exact current bytes of:

- `tools/far_investigation_benchmark.py`;
- `schemas/far-research-campaign-v1.schema.json`;
- every treatment-defining source required by `far-treatment-source-manifest.json` and by the validator's mandatory treatment-source set.

At minimum that treatment set includes the canonical FAR workflow, contract-discovery protocol, methodology-audit protocol, intake schema, and all FARA architecture documents enumerated by the validator. Any additional executable harness, renderer, unitizer, mutation generator, packet normalizer, schedule generator, or analysis implementation used by the campaign must also be added to `source_manifest` before freeze.

Every frozen source record uses `verify_current_path = true`, a nonzero SHA-256, and a byte-for-byte hash match. A frozen record cannot opt out of verification.

## Case record contract

Every final case record must contain at least:

- `case_id`;
- `candidate_id`;
- canonical textual `stratum_id`;
- `claim_cluster_id`;
- verbatim/raw and frozen normalized claim text fields;
- normalized source identity;
- `source_context` sufficient only for disambiguation;
- exact rendered case prompt;
- lowercase SHA-256 of the UTF-8 case-prompt bytes;
- deterministic `selection_key`;
- discovery provenance and eligibility/contamination disposition.

The final corpus contains exactly 60 unique case IDs, candidate IDs, and claim-cluster IDs, exactly 10 cases in each canonical stratum. A selected case must trace to exactly one eligible uncontaminated canonical representative in `candidate-frame.jsonl` and must be disjoint by candidate ID and claim-cluster ID from every reserve.

## Condition prompt contract

`condition-prompts.json` stores the exact bytes supplied by the benchmark harness. Each system, developer, and user-template surface is represented as base64 plus SHA-256. An absent surface is represented explicitly as `null`. The user template contains one literal `{{CASE_PROMPT}}` marker. Rendering consists only of replacing that marker with the exact UTF-8 case-prompt bytes from `cases.jsonl`; no other normalization, nonce insertion, or rewriting is permitted.

## Reference-evidence freeze

Reference evidence is constructed and locked before any condition run. The panel remains firewalled from condition prompts beyond the shared case prompt and from all condition outputs. If the frozen bounded search yields zero valid material reference items for a provisional selected case, that case is replaced by the next reserve in the same stratum before execution and the replacement is processed under the same search protocol.

`reference-evidence-manifest.json` must cover exactly the 60 final cases, each with a strictly positive M2 denominator. Reference-item inclusion, materiality, validity, and denominator membership are fixed before S1. After S1 begins, reference items cannot be deleted, merged, split, reweighted, or newly added for confirmatory M2. A discovered defect is an integrity deviation handled by the preregistered missingness/disposition rules.

## Execution schedule freeze

`execution-schedule.json` contains exactly one run for every 60×4 case-condition pair and exactly 240 runs total. For each pair, `schedule_key` is lowercase hexadecimal `SHA256(UTF8("20260922|schedule|" + case_id + "|" + condition))`. Sorting all 240 rows by that key defines `execution_index = 1..240`.

Every run has a unique stable `run_id`. If `environment-lock.json` uses the `non_model_visible_nonce` isolation mode, the run's cache nonce is exactly `SHA256(UTF8("FAR-INVESTIGATION-BENCHMARK-0.1|cache|" + run_id))` and is transported only through the frozen non-model-visible provider channel. Reordering, inserting, deleting, or model-visibly injecting nonce bytes is invalid.

## Adjudication schedule freeze

`adjudication-schedule.json` is generated only after the final 60 case IDs, complete execution schedule, and evaluator identities are frozen, but before any scoring output exists.

It must contain exactly one 240-run presentation list for each of the two `unitizer` evaluators and two `primary_scorer` evaluators. The list for an evaluator is reproduced exactly from `adjudication-rubric-v0.1.md`: evaluator-specific SHA-256 base case order, four 60-packet rounds, condition rotation by base position modulo four, exact presentation indices, and exact run-ID linkage to `execution-schedule.json`. Every evaluator therefore sees each condition exactly 60 times, 15 times per round, and each case's four versions exactly 60 presentation positions apart. The four presentation-isolation flags specified by the rubric must all be frozen as `true`; missing or additional fields, evaluators, or assignments are invalid.

The schedule is condition-blinded at presentation time and cannot be changed after any unitization or scoring output exists.

## Evaluator freeze

The frozen campaign manifest contains exactly six distinct evaluator IDs and identities with exact lane counts:

- 2 × `unitizer`;
- 1 × `unitization_adjudicator`;
- 2 × `primary_scorer`;
- 1 × `scoring_adjudicator`.

Provider/affiliation, prior-exposure, conflict, and lane declarations must be substantive and non-placeholder. Project-authored adjudication does not instantiate this confirmatory external benchmark.

## Chronology

The required order is:

1. freeze selection configuration and discovery environment;
2. construct candidate frame, resolve claim families, and select provisional final/reserve representatives;
3. build and lock bounded reference-evidence sets; replace only under the preregistered reserve rule;
4. freeze final `cases.jsonl`, prompt bundle, environment lock, resource budget, mutation config, execution schedule, adjudication schedule, evaluator declarations, treatment/source bindings, adjudication materials, numerical analysis parameters, and all hashes;
5. set `freeze_time` and validate the complete frozen campaign;
6. execute S1 according to the frozen execution schedule;
7. complete and lock canonical unitization, raw ratings, adjudicated ratings, blinding guesses, and metrics;
8. create `score-lock.json` binding those exact bytes and record `locked_at`;
9. set `unblinding_time` only after the score lock exists and no earlier than `freeze_time`;
10. run the frozen unblinded analysis and produce completion artifacts.

`unblinding_time` must be null while status is `frozen`, and must be present, offset-aware, and no earlier than `freeze_time` for `unblinded`, `completed`, or `completed_imported_sealed` states. `score-lock.json.locked_at` must be no later than `unblinding_time`.

## Pre-unblinding score-lock artifacts

Before condition identities are revealed, the campaign must bind and current-path verify:

- `canonical-unitization.jsonl`;
- `ratings.raw.jsonl`;
- `ratings.adjudicated.jsonl`;
- `blinding-guesses.jsonl`;
- `metrics.csv`;
- `score-lock.json`.

`score-lock.json` must bind the hashes of every other pre-unblinding scoring artifact. A campaign cannot enter an analyzable status without this lock.

## Completed-state artifacts

A `completed` or `completed_imported_sealed` campaign additionally binds and verifies:

- `run-manifest.json` with exactly 240 run records;
- `analysis.json`;
- `report.md`;
- `checksums.sha256`.

Its `final_adjudication.status` must be one of `SURVIVES_TESTED_SCOPE`, `NOT_SUPPORTED_AT_TESTED_SCOPE`, `FALSIFIED_AT_TESTED_SCOPE`, or `INDETERMINATE`, with nonempty justification and evidence fields. A completed status without completed evidence is invalid.

## Fail-closed rule

If any required path is absent, duplicated ambiguously, unhashed, hash-mismatched, path-unsafe, placeholder-bearing, nonfinite where numeric finiteness is required, semantically inconsistent with its contract, or inconsistent with the frozen chronology, the campaign remains `prepared` or becomes `blocked`.

Hash correctness is necessary but not sufficient. The validator must semantically reject, at minimum, empty or wrongly stratified corpora, duplicate claim families, malformed reserve frames, incomplete execution or adjudication schedules, invalid cache isolation/nonces, nonfinite resource ceilings, missing reference denominators, malformed selector/evaluator declarations, incomplete treatment-source closure, and invalid completed states. The validator must not infer missing values or permit execution because a human intends to fill them later.
