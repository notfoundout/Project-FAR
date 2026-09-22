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

The FAR condition must use only currently governed Project FAR mechanisms. This preregistration creates no new theory authority.

### Baseline B0 — direct answer

The same underlying model receives the raw investigation prompt and returns its best researched answer with citations, without FAR-specific protocol instructions.

### Baseline B1 — generic deep research

The same underlying model receives a neutral instruction to research the claim thoroughly, seek counterevidence, cite sources, and explain its conclusion. It receives no FAR terminology, schemas, or artifacts.

### Baseline B2 — structured fact-check

The same underlying model receives a conventional fact-checking workflow: identify factual claims, search supporting and contradicting evidence, assess sources, and issue a bounded conclusion. It receives no FAR-specific machinery.

## 4. Resource matching

For each case and system:

- identical model family and version where technically possible;
- identical retrieval/tool access;
- identical source-date cutoff;
- identical maximum wall-clock budget;
- identical maximum model-token budget within a preregistered tolerance;
- identical number of permitted retry/research rounds;
- no cross-condition reuse of hidden reasoning or intermediate artifacts.

Any resource mismatch is recorded and the affected pair is excluded from confirmatory analysis unless the preregistered tolerance permits it.

## 5. Corpus

Target: 60 cases.

The corpus is frozen before system execution and stratified across at least six domains, with 10 cases per domain:

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
- avoid requiring private or inaccessible evidence for the primary adjudication.

### Exclusion criteria

Exclude cases whose correct resolution depends primarily on:

- private evidence unavailable to all conditions;
- subjective taste or pure normative preference;
- prediction of future events;
- a single arithmetic or dictionary lookup;
- a claim already present in Project FAR development examples or used to tune the protocol.

The case selector freezes only prompts and admissibility metadata. It does not prepare gold conclusions.

## 6. Independence and blinding

Case selection, investigation execution, and adjudication are separated roles.

Adjudicators receive normalized, condition-blinded investigation packets. FAR-specific field names and formatting are transformed into a common presentation layer where possible so that raters cannot infer condition merely from labels.

At least two independent adjudicators score every case. Disagreements on primary metrics are resolved by a third adjudicator under the frozen rubric. Raw pre-adjudication scores are retained.

Project-authored adjudication is insufficient for an external-independence claim. Any run lacking externally independent adjudication must be labeled internal.

## 7. Primary metrics

### M1 — Unsupported-inference rate

Unit: material inferential steps.

A material inference is unsupported when the stated conclusion does not follow at the claimed strength from the cited evidence plus explicitly declared assumptions.

Score per case:

`unsupported material inference steps / all material inference steps`

Lower is better.

Primary gate: FAR must show a lower paired median rate than every confirmatory baseline. The confirmatory M1 family uses Holm-adjusted two-sided paired permutation tests with family-wise α = 0.05. In addition, the Hodges-Lehmann paired median-difference estimate (FAR minus baseline) must be ≤ -0.05 for every confirmatory baseline. Lower values favor FAR on this metric.

### M2 — Evidence coverage

Before adjudicators inspect system outputs, an evidence-reference panel constructs a bounded reference set of material evidence items for each case using a separately frozen search protocol.

Score per case:

`material reference evidence recovered and correctly connected / material reference evidence in bounded reference set`

Evidence that is merely cited but attached to the wrong proposition does not count.

Primary gate: FAR must be non-inferior to each confirmatory baseline under an absolute evidence-coverage margin Δ = 0.05. For each paired comparison, the lower bound of the 95% bootstrap confidence interval for mean coverage difference (FAR minus baseline) must be greater than -0.05.

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

The benchmark includes sealed mutations of completed investigation packets. Mutations are generated only after the original corpus is frozen and must not alter the underlying case prompt.

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
- Primary family: M1 comparisons plus the M2 non-inferiority gate.
- M1 confirmatory p-values use two-sided paired permutation tests with Holm correction across B0, B1, and B2 at family-wise α = 0.05.
- Exact permutation is used when computationally feasible; otherwise use 100,000 Monte Carlo permutations with seed 20260922.
- M1 effect-size floor: Hodges-Lehmann paired median-difference estimate ≤ -0.05 for every confirmatory baseline.
- M2 non-inferiority margin: absolute evidence-coverage difference Δ = 0.05; use 10,000 paired bootstrap resamples with seed 20260922 and require the 95% lower confidence bound for FAR minus each baseline to exceed -0.05.
- Report paired mean and median differences, percentile bootstrap confidence intervals, and raw per-case values in addition to confirmatory decisions.
- All exclusions are reported both before and after exclusion.
- Missing output is scored as failure on completion-dependent metrics and remains visible.
- No post-hoc subgroup becomes confirmatory.
- These numerical parameters are frozen by this preregistration. The execution manifest must reproduce them byte-for-byte before the first system run.

## 12. Leakage controls

Before execution:

- hash every case prompt;
- hash the complete corpus manifest;
- record model/version identifiers;
- record all system prompts;
- record tool/retrieval configuration;
- record source cutoff;
- record resource budgets;
- record adjudication rubric and mutation generator version.

Cases with demonstrated training/tuning leakage from Project FAR development are removed before unblinding and replaced under the frozen selection protocol.

## 13. Required artifacts

An executable campaign must produce:

- `manifest.json`;
- `cases.jsonl`;
- `conditions/` frozen prompts/configuration;
- `runs/` raw outputs and tool traces;
- `reference-evidence/` bounded evidence sets;
- `adjudication/` blinded raw ratings and adjudications;
- `mutations/` sealed adversarial controls;
- `metrics.csv`;
- `analysis.json`;
- `report.md`;
- `checksums.sha256`;
- environment and dependency lock information sufficient for replay.

Every result row must bind to case hash, condition hash, model identifier, run identifier, evidence cutoff, and output hash.

## 14. Decision rules

### SURVIVES

The primary hypothesis survives this benchmark only if:

1. FAR passes the M1 superiority gate against all confirmatory baselines;
2. FAR passes the M2 evidence-coverage non-inferiority gate;
3. no integrity failure invalidates the paired comparison;
4. adjudication independence is reported at its actual class.

### FALSIFIED AT TESTED SCOPE

If FAR fails the M1 gate or falls outside the M2 non-inferiority margin, the primary hypothesis is falsified at the tested corpus/model/resource scope.

### INDETERMINATE

Use INDETERMINATE when execution or integrity failures prevent the frozen decision rule from being applied. INDETERMINATE must not be rewritten as support.

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

This document is a Research preregistration. It authorizes no claim promotion. Before first execution, the machine-readable campaign manifest must bind the exact corpus, prompts, model/tool versions, adjudication rubric, resource limits, evidence-reference search protocol, and hashes. Section 11's numerical parameters are already frozen here and must be reproduced without alteration.

No benchmark result may be reported as confirmatory if those values were chosen after observing condition outputs.