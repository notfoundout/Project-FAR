# FAR Investigation Benchmark — Freeze Contract v0.1

Status: PREPARED / normative for transition from `prepared` to `frozen`
Parent: `research/comparisons/far-investigation-benchmark-v0.1.md`

## Purpose

A campaign may enter `frozen` status only when every choice that can affect case selection, execution, scoring, or confirmatory analysis is represented by an immutable artifact and bound by SHA-256 in the campaign manifest. A status edit by itself never constitutes a freeze.

## Required static protocol artifacts

The campaign `artifacts` array must bind the current bytes of:

- `research/comparisons/far-investigation-benchmark-v0.1.md`;
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

- `candidate-frame.jsonl` — complete discovery ledger, including rejected candidates;
- `cases.jsonl` — exactly 60 final case records, 10 for each `S1` through `S6`;
- `replacement-frame.jsonl` — the ordered reserve frame;
- `case-selection-config.json` — discovery queries, source classes, source cutoff, retrieval configuration, seed, normalization rule identifier, and selection-key test vector;
- `case-selection-declarations.json` — selector identities, prior exposure, conflicts, and contamination-search record;
- `condition-prompts.json` — exact prompt bytes for F/B0/B1/B2 encoded as base64 plus per-surface SHA-256 and deterministic case-prompt rendering rule;
- `execution-schedule.json` — all 240 case-condition runs in the exact preregistered order with stable run IDs;
- `reference-search-config.json` — reference-panel query templates, retrieval configuration, source cutoff, search/tool-call budget, source-chain limits, and researcher declarations;
- `reference-evidence-manifest.json` — one locked entry per final case, with a positive material-evidence denominator and hashes of the per-case reference-evidence record;
- `environment-lock.json` — immutable model/provider identifier or snapshot, provider settings, tool versions, retrieval settings, dependency/runtime versions, retry policy, session-isolation policy, and any provider fingerprint available;
- `mutation-config.json` — exact mutation families, generator/version identity, seed or deterministic construction rule, and sealing procedure.

No generated freeze artifact may contain an unresolved sentinel such as `TO_BE_*`, `UNASSIGNED`, `PLACEHOLDER`, or a `*_NOT_FROZEN` status.

## Required source bindings

The `source_manifest` must be nonempty and must at minimum bind the exact current bytes of:

- `tools/far_investigation_benchmark.py`;
- `frameworks/FAR/workflow.md`;
- `schemas/far-research-campaign-v1.schema.json`.

Every source binding required by this benchmark must use `verify_current_path = true` and match its recorded SHA-256. Any additional executable harness, renderer, unitizer, mutation generator, or analysis implementation used by the campaign must also be added to `source_manifest` before freeze.

## Case record contract

Every final case record must contain at least:

- `case_id`;
- `stratum_id` (`S1` through `S6`);
- verbatim `claim_text`;
- normalized `source_identity`;
- `source_context` sufficient only for disambiguation;
- exact rendered `case_prompt`;
- lowercase SHA-256 of the UTF-8 case-prompt bytes;
- deterministic `selection_key`;
- discovery provenance and eligibility disposition.

Case IDs are assigned after deterministic selection: `S1-C01` through `S6-C10`, ordered by selection key inside each stratum. Reserve IDs use `S1-R01` etc. A final selected case must be traceable to exactly one candidate-frame entry and must not appear in the reserve frame.

## Condition prompt contract

`condition-prompts.json` stores the exact bytes supplied by the benchmark harness. Each system, developer, and user-template surface is represented as base64 plus SHA-256. An absent surface is represented explicitly as `null`. The user template contains one literal `{{CASE_PROMPT}}` marker. Rendering consists only of replacing that marker with the exact UTF-8 `case_prompt` bytes from `cases.jsonl`; no other normalization or rewriting is permitted.

## Reference-evidence freeze

Reference evidence is constructed and locked before any condition run. The panel remains firewalled from condition prompts beyond the shared case prompt and from all condition outputs. If the frozen bounded search yields zero valid material reference items for a selected case, that case is replaced by the next reserve in the same stratum before execution and the replacement is processed under the same search protocol. The final 60 cases therefore each have a positive frozen M2 denominator before S1 begins.

`reference-evidence-manifest.json` must bind every per-case reference record and denominator. After S1 begins, reference items cannot be deleted, merged, split, reweighted, or newly added for confirmatory M2. A discovered defect is an integrity deviation handled by the preregistered missingness rule.

## Execution schedule freeze

`execution-schedule.json` contains exactly four runs for every final case and exactly 240 runs total. The order for each case is the deterministic order defined in `condition-contracts-v0.1.md`. The schedule is generated and hashed before S1. Reordering, inserting, or deleting a run after any condition output exists is a protocol deviation.

## Chronology

The required order is:

1. freeze selection configuration and discovery environment;
2. construct candidate and reserve frames and select provisional cases;
3. build and lock bounded reference-evidence sets; replace only under the preregistered reserve rule;
4. freeze final `cases.jsonl`, prompt bundle, environment lock, resource budget, mutation config, execution schedule, adjudication materials, numerical analysis parameters, all hashes, and evaluator/source declarations;
5. set `freeze_time` and validate the complete frozen campaign;
6. execute S1;
7. lock raw scores before unblinding;
8. set `unblinding_time` only when S3 begins.

`unblinding_time` must be null while status is `frozen`, and must be present and no earlier than `freeze_time` for `unblinded` or completed states.

## Fail-closed rule

If any required path is absent, duplicated ambiguously, unhashed, hash-mismatched, path-unsafe, placeholder-bearing, or inconsistent with this contract, the campaign remains `prepared` or becomes `blocked`. The validator must not infer missing values or permit execution because a human intends to fill them later.
