# FAR Investigation Benchmark v0.1 — Pre-execution hardening amendment

Status: **NORMATIVE PRE-S1 AMENDMENT**  
Campaign: `FAR-INVESTIGATION-BENCHMARK-0.1`  
Date: 2026-09-22

No benchmark condition output had been collected when this amendment was adopted. This amendment therefore changes no observed result. It closes fail-closed and preregistration ambiguities discovered during pre-execution review.

Where this document conflicts with `far-investigation-benchmark-v0.1.md`, `case-selection-protocol-v0.1.md`, `adjudication-rubric-v0.1.md`, `condition-contracts-v0.1.md`, `freeze-contract-v0.1.md`, `resource-budget-v0.1.json`, or `analysis-parameters-v0.1.json`, this amendment controls for benchmark v0.1. The executable validator is required to enforce the machine-checkable portions below before a campaign may enter `frozen` status.

## 1. All frozen records are current-path verified

For every `source_manifest` and `artifacts` record in a `frozen`, `unblinded`, `completed`, or `completed_imported_sealed` campaign, `verify_current_path` MUST equal `true`, the path MUST exist inside the repository root, the SHA-256 MUST be nonzero, and the SHA-256 MUST equal the current file bytes. A future record cannot opt out of verification by setting the flag to false.

## 2. Frozen corpus semantics

The six canonical stratum IDs are:

- `public_policy_law`
- `health_biomedical`
- `economics_quant_social`
- `science_technology`
- `historical`
- `media_viral_public_factual`

The final corpus MUST contain exactly 60 unique cases, exactly 10 per stratum. Every selected case MUST cross-reference an eligible, uncontaminated, cluster-representative candidate in `candidate-frame.jsonl`. Selected and reserve cases MUST have unique candidate IDs and unique claim-cluster IDs.

The reserve frame MUST contain at least 10 eligible uncontaminated cluster representatives per stratum, disjoint from the selected corpus. Replacement is allowed only before S1. No post-S1 case replacement is permitted.

### Claim-family deduplication

Source-level deduplication is insufficient. Before deterministic selection, candidate claims are clustered by proposition identity.

1. Text normalization is Unicode NFKC, lowercase, then whitespace collapse.
2. A claim family represents the same material proposition: subject, predicate, object, and material time, geography, population, quantity, or other scope qualifiers. Source, publication, eventual outcome, and evidence are ignored for family identity.
3. Two independent selectors perform clustering without condition outputs. A separate clustering adjudicator resolves disagreements before selection.
4. The canonical representative of each resolved family is the minimum tuple `(retrieval_rank, normalized_source_identity, candidate_id)`.
5. `claim_cluster_id` is SHA-256 of the canonical representative's normalized claim text encoded as UTF-8.
6. Only canonical cluster representatives are eligible for final or reserve selection.

## 3. Case-selection declarations

Before freeze, `case-selection-declarations.json` MUST identify two distinct independent selectors and one distinct clustering adjudicator. Each declaration MUST include a nonempty ID, identity, provider or affiliation, independence declaration, conflict declaration, and role. Project FAR authorship or protocol-tuning exposure MUST be disclosed. The three identities MUST be distinct.

## 4. Execution schedule and cache isolation

`execution-schedule.json` MUST contain exactly 240 runs: one and only one run for every Cartesian product of the 60 final case IDs and conditions `F`, `B0`, `B1`, and `B2`. Run IDs and execution indices MUST be unique; indices MUST be exactly 1 through 240.

The schedule MUST be generated deterministically by sorting all case-condition rows by the hexadecimal SHA-256 of `UTF8("20260922|schedule|" + case_id + "|" + condition)` and then assigning execution indices 1 through 240.

Shared model-visible cache state is forbidden. Before S1 the frozen environment MUST support either:

- a provider-documented isolated/no-shared-cache context; or
- a non-model-visible provider metadata/header nonce equal to `SHA256(UTF8("FAR-INVESTIGATION-BENCHMARK-0.1|cache|" + run_id))`.

The nonce MUST NOT appear in system, developer, user, or tool-call content and MUST NOT consume the model-visible token budget. `environment-lock.json` MUST record the mechanism, channel, documentation/reference, and whether it is model-visible. If neither mechanism is available for every condition, the campaign is `BLOCKED` before S1.

## 5. Resource ceilings are outcomes, not exclusions

A run reaching a frozen wall-clock, token, tool-call, retry, or output-size ceiling remains a benchmark outcome. It MUST NOT be excluded merely because the ceiling was reached.

Only an exogenous infrastructure/configuration failure that prevents the frozen condition from being executed as specified may make the entire four-condition case nonratable. Such a failure MUST be condition-blindly classified and documented. No replacement occurs after S1.

If more than 3 of 60 cases are nonratable for such exogenous failures, the campaign disposition is `INDETERMINATE`. With 1–3 such cases, the primary complete-case analysis and the frozen best/worst-case sensitivity analysis are both reported. Sensitivity cannot rescue a failed primary gate.

All frozen numeric budgets MUST be finite real numbers (or integers where required). JSON `NaN`, `Infinity`, and `-Infinity` are invalid.

## 6. FAR treatment is transitively bound

The treatment is not defined by `frameworks/FAR/workflow.md` alone. Before S1, `far-treatment-source-manifest.json` MUST bind and current-path verify every treatment-defining source required by the benchmark validator, including the FAR workflow, the contract-discovery and methodology-audit protocols, the intake schema, and the FARA architectural documents referenced by the workflow. Changing any bound treatment source after freeze invalidates the freeze.

## 7. Canonical M1 unitization precedes scoring

M1 inferential-step boundaries are frozen before support scoring.

1. Two blinded independent `unitizer` evaluators receive normalized packets and mark material-inference boundaries and immutable unit IDs without support/evidence labels.
2. A separate `unitization_adjudicator` resolves boundary disagreements.
3. The resulting `canonical-unitization.jsonl` is locked before primary scoring.
4. Primary scorers receive the immutable unit IDs and may not split, merge, add, or delete M1 units.
5. A nonmissing packet with zero ratable material-inference units is a scoring failure/nonratable packet; it is never assigned M1 = 0.

## 8. Frozen evaluator lanes

A frozen-or-later campaign MUST identify six distinct externally independent evaluators with these exact lane counts:

- 2 × `primary_scorer`
- 1 × `scoring_adjudicator`
- 2 × `unitizer`
- 1 × `unitization_adjudicator`

All evaluator IDs and identities MUST be distinct. `prior_exposure` and `conflicts` MUST be substantive declarations, not placeholders. Any campaign that cannot satisfy this requirement may still be run as a separately versioned internal study, but it cannot claim to instantiate this confirmatory external benchmark.

## 9. Blinding diagnostic

Immediately after scoring each packet and before condition identities are revealed, each primary scorer records one guess from `F`, `B0`, `B1`, `B2`, or `UNKNOWN`.

Blinding fails if either primary scorer:

- correctly identifies condition `F` on at least 30 of the 60 `F` packets; or
- has exact four-way condition accuracy of at least 40% across all 240 packets.

`UNKNOWN` counts as incorrect. A blinding failure makes the confirmatory campaign `INDETERMINATE`. These are preregistered design thresholds, not null-hypothesis significance tests.

## 10. Reference-evidence denominator

Before S1, every final case MUST have at least one frozen valid material reference-evidence item. `reference-evidence-manifest.json` MUST cover exactly the 60 final case IDs and MUST give each case a positive M2 denominator. Zero-denominator cases cannot enter S1.

## 11. M2 familywise rules

The noninferiority survival gate remains an intersection-union gate: for each of B0, B1, and B2, the one-sided 95% lower bootstrap bound for `FAR - baseline` MUST be strictly greater than `-0.05`. Because all three component nulls must be rejected for the global survival claim, no additional multiplicity correction is required for that intersection-union pass gate.

Directional M2 falsification is familywise controlled across the three baselines. For each baseline, compute the one-sided Bonferroni upper percentile bound at confidence `1 - 0.05/3 = 0.9833333333333333`. With 10,000 sorted bootstrap statistics and the frozen zero-based rule `ceil(q*N) - 1`, the upper index is 9833. M2 is directionally falsified if any baseline's familywise upper bound is strictly less than `-0.05`.

The absolute `0.05` effect/noninferiority threshold is a preregistered design threshold. It is not claimed to be an externally validated practical-utility threshold.

## 12. Score lock and unblinding

Before `unblinded` status, the following MUST exist, be hash-bound, current-path verified, and temporally locked before `unblinding_time`:

- `canonical-unitization.jsonl`
- `ratings.raw.jsonl`
- `ratings.adjudicated.jsonl`
- `blinding-guesses.jsonl`
- `score-lock.json`
- `metrics.csv`

`score-lock.json` MUST identify the exact hashes of all scoring inputs/outputs above. Unblinding before that lock is invalid.

## 13. Completed-state gate

A `completed` or `completed_imported_sealed` campaign MUST additionally bind and verify:

- `run-manifest.json`
- `analysis.json`
- `report.md`
- `checksums.sha256`

The final adjudication status MUST be exactly one of `SURVIVES_TESTED_SCOPE`, `FALSIFIED_AT_TESTED_SCOPE`, or `INDETERMINATE`, and the final-adjudication object MUST contain nonempty `justification` and `evidence` fields. A status-only manifest without the completion artifacts is invalid.

## 14. Fail-closed semantic validation

Hash correctness is necessary but not sufficient. Before S1 the validator MUST reject semantically invalid frozen artifacts, including empty corpora, wrong stratum quotas, duplicate candidate/cluster identities, malformed reserve frames, incomplete Cartesian schedules, invalid cache nonces, nonfinite budgets, missing reference denominators, malformed declarations, unresolved placeholders, and treatment manifests that omit mandatory transitive sources.

The validator MUST reject every `source_manifest` or `artifacts` record in frozen-or-later status that is not current-path verified, even if that record is not otherwise listed as a known mandatory artifact.

## 15. Scope remains unchanged

This amendment does not create a benchmark result, establish FAR superiority, establish novelty or priority, establish commercial value, or authorize promotion of W6. It only hardens the pre-execution benchmark contract for FAR-RQ-005 / UQ-T35.