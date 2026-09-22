# FAR Investigation Benchmark v0.1 — Preregistration

Status: Research / preregistration only  
Date: 2026-09-22  
Claim impact: none until execution, replication, adjudication, and any separately governed acceptance/promotion

## 1. Objective

Test the currently open empirical question that matters for Project FAR's commercial positioning:

> On bounded real-world disputed-claim investigations, does a FAR-governed workflow improve investigation quality relative to matched non-FAR research workflows?

This benchmark does **not** test whether FAR is universally superior, whether FAR is novel, or whether FAR is commercially valuable. It tests specified observable differences under a frozen corpus, frozen scoring rules, and matched resource constraints.

## 2. Primary hypothesis

For a preregistered corpus of real-world disputed claims, FAR will reduce unsupported inference while preserving or improving evidence coverage relative to matched baseline workflows.

The primary endpoint is the paired difference in unsupported-inference rate. Evidence coverage is a co-primary endpoint. The preregistered hypothesis survives only if both co-primary gates pass; this is not a universal or overall ranking of systems.

## 3. Systems under comparison

### FAR condition

A workflow that must preserve, at minimum:

1. exact raw input and provenance;
2. atomic claim decomposition and claim typing;
3. materially distinct interpretations and explicit exclusions;
4. source/evidence provenance;
5. support, contradiction, and unresolved-evidence links;
6. explicit assumptions and dependencies;
7. competing hypotheses or alternative explanations when materially applicable;
8. inference-step audit;
9. uncertainty and Unknown outcomes;
10. falsification conditions;
11. replayable investigation record.

Condition F must execute the canonical Project FAR workflow and its governed contract-discovery/factorization machinery as specified in `condition-contracts-v0.1.md`. This preregistration creates no new theory authority.

### Baseline B0 — direct answer

The same underlying model receives the raw investigation prompt and returns its best researched answer with citations, without FAR-specific protocol instructions.

### Baseline B1 — generic deep research

The same underlying model receives a neutral instruction to research the claim thoroughly, seek counterevidence, cite sources, and explain its conclusion. It receives no FAR terminology, schemas, or artifacts.

### Baseline B2 — structured fact-check

The same underlying model receives a conventional fact-checking workflow: identify factual claims, search supporting and contradicting evidence, assess sources, and issue a bounded conclusion. It receives no FAR-specific machinery.

## 4. Resource matching

For each case and system:

- identical immutable model identifier or provider snapshot where technically available;
- identical retrieval/tool access;
- identical source cutoff and source-version admissibility rule;
- identical maximum wall-clock budget;
- identical maximum model-output-token ceiling;
- identical retrieval/tool-call ceiling;
- identical retry allowance;
- identical output-size ceiling;
- no cross-condition reuse of hidden reasoning or intermediate artifacts.

If the provider exposes only a rolling model alias, that limitation and any available provider fingerprint must be frozen in `environment-lock.json`. A detectable model/tool/configuration drift outside the frozen tolerance is an integrity mismatch rather than an unrecorded substitution.

Any resource mismatch is recorded and handled only under the frozen mismatch rule. No outcome-aware resource exclusion is permitted.

## 5. Corpus

Target: 60 cases.

The final corpus is frozen before system execution and stratified across exactly six domains, with 10 cases per domain:

- public policy / law;
- health or biomedical claims;
- economics / quantitative social claims;
- science / technology;
- historical claims;
- media / viral or public factual claims.

### Inclusion criteria

Each case must:

- contain at least one externally checkable factual proposition;
- permit more than a trivial single-source lookup;
- have enough public evidence for a competent investigator to make progress;
- contain at least one plausible opportunity for evidence omission, interpretation error, or inference error;
- avoid requiring private or inaccessible evidence for the primary adjudication;
- yield at least one valid material reference-evidence item under the frozen reference-search protocol before S1.

### Exclusion criteria

Exclude cases whose correct resolution depends primarily on:

- private evidence unavailable to all conditions;
- subjective taste or pure normative preference;
- prediction of future events;
- a single arithmetic or dictionary lookup;
- a claim already present in Project FAR development examples or used to tune the protocol.

The case selector records prompts and admissibility metadata but does not prepare gold conclusions. Selection, reserve replacement, case IDs, and exact normalization are governed by `case-selection-protocol-v0.1.md` and `freeze-contract-v0.1.md`.

## 6. Independence and blinding

Case selection, condition execution, reference-evidence construction, unitization, and adjudication are separated roles to the extent declared by the frozen campaign.

Reference-evidence construction is completed and locked before any condition output exists. Adjudicators receive normalized, condition-blinded investigation packets. FAR-specific field names and formatting are transformed into a common presentation layer where possible so that raters cannot infer condition merely from labels.

Two primary raters independently score every packet. Disagreements on primary metrics are resolved by a third adjudicator under the frozen rubric. Raw pre-adjudication scores are retained.

Project-authored adjudication is insufficient for an external-independence claim. Any run lacking externally independent adjudication must be labeled internal.

## 7. Primary metrics

### M1 — Unsupported-inference rate

Unit: material inferential steps.

A material inference is unsupported when the stated conclusion does not follow at the claimed strength from the cited evidence plus explicitly declared assumptions.

Score per case:

`unsupported material inference steps / all ratable material inference steps`

Lower is better. A non-missing packet with no ratable material inferential step is a scoring failure handled by the missingness rule; it is not assigned M1 = 0.

Primary gate: for every confirmatory baseline, FAR must have a negative observed mean paired difference in case-level M1 rate; the Holm-adjusted two-sided paired sign-flip permutation test on the **mean paired difference** must reject at family-wise α = 0.05; and the paired Hodges-Lehmann location estimate (FAR minus baseline) must be ≤ -0.05. The exact Hodges-Lehmann, permutation, randomization, and tie rules are frozen in Section 11 and `analysis-parameters-v0.1.json`.

### M2 — Evidence coverage

Before any condition run, a firewalled evidence-reference panel constructs and locks a bounded reference set of valid material evidence items for every final case using the frozen reference-search protocol. Every final case must have a positive M2 denominator before S1 begins.

Score per case:

`material reference evidence recovered and correctly connected / frozen valid material reference evidence`

Evidence that is merely cited but attached to the wrong proposition does not count. Exact connection rules are frozen in `adjudication-rubric-v0.1.md`.

Primary gate: FAR must be non-inferior to each confirmatory baseline under an absolute evidence-coverage margin Δ = 0.05. For each paired comparison, the frozen one-sided 95% bootstrap lower bound for mean coverage difference (FAR minus baseline) must be strictly greater than -0.05.

Both M1 and M2 gates are required for the primary hypothesis to survive.

## 8. Secondary metrics

- contradiction discovery rate;
- material alternative-hypothesis coverage;
- assumption-explicitness rate;
- source-to-claim correspondence accuracy;
- calibrated Unknown use;
- falsification-condition quality;
- provenance completeness;
- deterministic replay completeness;
- adjudicator agreement;
- elapsed time;
- model tokens;
- retrieval/tool calls;
- estimated marginal execution cost.

Secondary metrics cannot rescue failure of either primary gate.

## 9. Critical error taxonomy

Each material defect is assigned one primary class:

- C1: unsupported factual assertion;
- C2: evidence does not support cited claim;
- C3: omitted material counterevidence;
- C4: hidden assumption;
- C5: invalid or over-strength inference;
- C6: interpretation/claim-substitution error;
- C7: provenance failure;
- C8: unresolved contradiction presented as resolved;
- C9: uncertainty suppression / unjustified certainty;
- C10: materially incomplete alternative set;
- C11: unreplayable evidence or computation;
- C12: other, with mandatory written justification.

## 10. Adversarial controls

The benchmark includes sealed mutations of completed investigation packets. The exact mutation configuration and deterministic generation/sealing rule are frozen before S1; the mutations themselves are derived from completed packets only after the relevant originals exist. They must not alter the underlying case prompt.

Mutation families:

1. remove a material contradicting source;
2. swap a citation onto a proposition it does not support;
3. strengthen a conclusion beyond the evidence;
4. hide a material assumption;
5. replace a bounded uncertainty statement with unjustified certainty;
6. remove provenance needed for replay.

Detection of these mutations is evaluated separately from natural-case performance and cannot substitute for the primary real-world endpoints.

## 11. Statistical plan

- Unit of analysis: case.
- Comparisons: paired by case.
- Confirmatory baselines: B0, B1, B2.
- Primary M1 family: three FAR-versus-baseline comparisons with Holm family-wise control at α = 0.05. M2 is a required co-primary non-inferiority gate against every confirmatory baseline; all M1 and M2 requirements must pass for SURVIVES.
- For each baseline, define case-level M1 paired differences `d_i = M1_FAR,i - M1_baseline,i` over the complete paired cases sorted by `case_id`. The M1 test statistic is the arithmetic mean of the `d_i` values.
- Under the paired sign-flip null, independently multiply each nonzero `d_i` by +1 or -1; zero differences remain zero. Enumerate every sign assignment when the number of nonzero pairs is ≤ 20. Otherwise generate exactly 100,000 deterministic sign vectors. For draw `r >= 1`, case `case_id`, and baseline ID, the sign is +1 when the low-order bit of `SHA256(UTF8("20260922|M1|" + baseline + "|" + decimal(r) + "|" + case_id))` is 0, otherwise -1.
- The exact two-sided permutation p-value is the fraction of all sign assignments whose absolute statistic is at least the absolute observed statistic. The Monte Carlo p-value is `(1 + extreme_draws) / (1 + 100000)` under the same extreme rule.
- Apply Holm's step-down correction to the three M1 raw p-values. Raw p-value ties are ordered B0, then B1, then B2 for deterministic reporting; the tie order does not change the Holm thresholds.
- The paired Hodges-Lehmann estimator is the median of all Walsh averages `(d_i + d_j) / 2` for `i <= j`. If the count of Walsh averages is even, the median is the arithmetic mean of the two central sorted values. The M1 effect-size requirement is Hodges-Lehmann ≤ -0.05 for every baseline, with observed mean `d_i < 0` for every baseline.
- For M2, define complete-case paired differences `q_i = M2_FAR,i - M2_baseline,i`, sorted by `case_id`. Each bootstrap draw resamples `n` paired case indices with replacement and computes the arithmetic mean. For draw `r >= 1` and sample position `p = 1..n`, use index `integer(SHA256(UTF8("20260922|M2|" + baseline + "|" + decimal(r) + "|" + decimal(p))), 16) mod n` into the sorted complete-pair list. Generate exactly 10,000 bootstrap statistics.
- Sort the 10,000 M2 bootstrap statistics ascending. The frozen one-sided 95% lower bound is element `ceil(0.05*N)` under 1-based indexing; the frozen one-sided 95% upper bound is element `ceil(0.95*N)`; `N = 10000`. Non-inferiority requires the lower bound > -0.05 for every baseline. Directional M2 falsification requires an upper bound < -0.05 for at least one baseline.
- Report paired mean and median differences, the frozen Hodges-Lehmann estimate, raw and Holm-adjusted M1 p-values, frozen M2 bounds, raw per-case values, and all exclusions/missingness.
- A wholly missing condition output receives M1 = 1 and M2 = 0 for that case. Packet corruption, inaccessible evidence, or failure to produce a ratable M1 unit makes the entire case non-ratable for that affected metric across all conditions. Condition-specific deletion is forbidden.
- If more than 3 of 60 cases are non-ratable for either primary metric, status is INDETERMINATE. At 3 or fewer, run the confirmatory analysis on complete pairs and the frozen sensitivity analysis: for each non-ratable case, M1 worst-case for FAR is FAR=1/baseline=0 and best-case is FAR=0/baseline=1; M2 worst-case is FAR=0/baseline=1 and best-case is FAR=1/baseline=0.
- SURVIVES requires the complete-pair gates to pass **and** the worst-case-for-FAR sensitivity analysis to preserve every M1 and M2 primary gate. If complete-pair gates pass but worst-case sensitivity reverses any gate, status is INDETERMINATE. Sensitivity analysis cannot rescue a failed complete-pair gate.
- No post-hoc subgroup becomes confirmatory.
- These numerical and algorithmic parameters are frozen by this preregistration and `analysis-parameters-v0.1.json`. Any change requires a new benchmark version before execution.

## 12. Leakage and source-cutoff controls

Before S1:

- hash every case prompt;
- hash the complete corpus and reserve manifests;
- record immutable model/version identifiers or the strongest available provider fingerprint;
- record exact system/developer/user prompt bytes;
- record tool/retrieval configuration;
- record source cutoff and source-version admissibility rule;
- record resource budgets;
- record adjudication rubric and mutation generator/configuration;
- record the complete reference-evidence manifest;
- record the exact 240-run execution schedule and session-isolation policy.

Cases with demonstrated Project FAR development/tuning leakage are excluded before final freeze and replaced under the deterministic reserve protocol. After S1 begins, the confirmatory corpus cannot be changed.

For mutable web sources, only content demonstrably existing by the frozen source cutoff is admissible. Materially updated living pages require an archived/versioned snapshot at or before the cutoff.

## 13. Required artifacts and freeze

The normative transition from `prepared` to `frozen` is defined by `research/comparisons/far-investigation-benchmark-v0.1/freeze-contract-v0.1.md` and enforced by `tools/far_investigation_benchmark.py`.

At minimum, the frozen campaign binds:

- the preregistration and all static benchmark protocols/configuration;
- the complete candidate frame, final 60-case corpus, and ordered reserves;
- exact condition prompt bytes;
- the 240-run execution schedule;
- reference-search configuration and the locked positive-denominator reference-evidence manifest;
- model/provider/tool/environment lock and resource ceilings;
- adjudicator/evaluator declarations;
- mutation configuration;
- benchmark validator plus canonical FAR workflow/schema source bindings;
- SHA-256 for every bound artifact and source.

Execution outputs then add `runs/`, blinded adjudication records, mutations, `metrics.csv`, `analysis.json`, `report.md`, checksums, and sufficient environment/dependency information for replay.

Every result row must bind to case hash, condition hash, model identifier, run identifier, evidence cutoff, and output hash.

## 14. Decision rules

### SURVIVES

The primary hypothesis survives this benchmark only if:

1. FAR passes the M1 superiority gate against all confirmatory baselines;
2. FAR passes the M2 evidence-coverage non-inferiority gate against all confirmatory baselines;
3. the worst-case-for-FAR sensitivity analysis preserves every primary gate when 1–3 cases are non-ratable;
4. no integrity failure invalidates the paired comparison;
5. adjudication independence is reported at its actual class.

### NOT SUPPORTED AT TESTED SCOPE

If either confirmatory gate is not passed, but the data do not meet a separately preregistered directional falsification criterion, report the primary hypothesis as **NOT SUPPORTED AT TESTED SCOPE**. Failure to reject or failure to establish non-inferiority is not itself falsification.

### FALSIFIED AT TESTED SCOPE

Reserve **FALSIFIED AT TESTED SCOPE** for an affirmative directional contradiction: against at least one confirmatory baseline, the observed M1 mean paired difference is > 0, the frozen Hodges-Lehmann estimate is ≥ +0.05, and the corresponding Holm-adjusted two-sided M1 test is significant at family-wise α = 0.05; or the frozen one-sided 95% M2 upper bound for FAR minus that baseline is < -0.05. Report the exact baseline(s) and tested scope.

### INDETERMINATE

Use INDETERMINATE when execution, integrity, or missingness prevents the frozen rule from supporting or contradicting the hypothesis, including primary-metric non-ratability above 3/60 or a complete-pair SURVIVES result that fails the frozen worst-case sensitivity requirement. INDETERMINATE must not be rewritten as support or falsification.

## 15. Prohibited promotions

This benchmark, even if successful, does not by itself establish:

- universal superiority;
- mathematical or foundational novelty;
- priority;
- enterprise reliability;
- commercial product-market fit;
- open-domain completeness;
- causal attribution of every observed gain to a specific FAR component.

A successful internal run establishes only bounded internal comparative evidence. External claims require independent replication under separately governed evidence.

## 16. Commercial interpretation

The benchmark is intentionally aimed at the current commercial bottleneck: whether FAR's integrated investigation protocol produces measurable gains over ordinary answer generation, generic deep research, and conventional structured fact-checking.

Formal proof engines, retrieval systems, frontier models, provenance systems, and evidence-receipt systems are treated as replaceable components where resource matching permits. The tested object is the investigation protocol and its auditable evidence-to-conclusion structure, not ownership of commodity proof or retrieval capability.

## 17. Execution gate

This document is a Research preregistration. It authorizes no claim promotion. Before the first condition run, the campaign must satisfy `freeze-contract-v0.1.md` and pass the fail-closed validator as `status = frozen`. That requires the exact final corpus and reserves, locked reference evidence, prompt bytes, model/tool/environment snapshot, resource limits, execution schedule, adjudicator declarations, mutation configuration, source bindings, and all required hashes.

A status edit without the complete validated freeze bundle does not authorize execution. No benchmark result may be reported as confirmatory if any confirmatory parameter or required freeze artifact was chosen or altered after condition outputs existed.
