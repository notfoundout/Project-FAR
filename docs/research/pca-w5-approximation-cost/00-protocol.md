# PCA-W5 Approximation-and-Cost Protocol v1.0

Status: **QUERY PROTOCOL FROZEN BEFORE EXTERNAL SEARCH**

Program: `POST-CLOSURE-001`

Workstream: `PCA-W5-APPROXIMATION-AND-COST`

Governing theory: `PROJECT-FAR-CORE-THEORY-1.1`

Canonical base commit: `e31ab40df0d0c75d3edfe3884681e3596dd65abd`

Canonical base tree: `078b91999ebe21bb77c777f2cace62c23e5415da`

Branch: `research/pca-w5-approximation-cost`

Freeze time: `2026-08-30T18:04:48Z`

## Objective

Determine, from independently motivated mathematical and scientific literature before FAR mapping, what must be declared for approximate adequacy and cost-relative minimality to be well-defined and checkable. Then determine the weakest governed Project FAR representation that can express those semantics without silently changing exact `far-ir/2.0` or promoting any domain-specific choice to a universal metric, loss, tolerance, aggregation rule, or cost order.

W5 is downstream of the closed exact core. It may define approximation and implementation-comparison methods; it may not reopen the core unless a reproducible contradiction to a stated theorem, proof step, or formal premise is found.

## Entry boundary

The W4 records remain exact finite-explicit certificates. They are not approximate certificates, cost optima, minimal repairs, or evidence of a universal approximation contract.

The existing `far-ir/2.0` approximation object is declaration scaffolding only: its status remains `DECLARED_ONLY`/`Unknown` and `w5_semantics_established` remains false. W5 must not silently reinterpret those fields as operational semantics. Any operational successor must be explicitly versioned or otherwise governed without changing the meaning of existing v2 records.

## Staged-access rule

### Stage A — native discovery

Use only the frozen queries below. Search terminology is intentionally native to the external research families and does not use Project FAR, FARA, FARO, `far-ir`, observational quotient, or Project FAR's preferred schema roles.

External discovery may identify definitions, theorems, counterexamples, impossibility results, alternative formalisms, and source terminology. Discovery output is not evidence until the underlying source is verified.

### Stage B — native concept/source freeze

Before controlled FAR mapping, freeze:

1. primary or authoritative source identities;
2. native definitions and their exact scope;
3. required mathematical objects and assumptions;
4. aggregation rules and probability/reference measures where applicable;
5. tolerance or acceptance relations;
6. cost/objective structures and their order properties;
7. existence, uniqueness, nonuniqueness, and incomparability conditions;
8. negative results and counterexamples;
9. rejected candidate sources and tool failures.

The frozen native record must distinguish what a source states from Project FAR's interpretation of it.

### Stage C — controlled FAR mapping

Only after the Stage-B freeze may W5 ask how the native structures map into Project FAR. The mapping must determine, rather than assume:

- whether a metric is required or a more general loss/discrepancy suffices;
- whether adequacy is pointwise, worst-case, expected, distribution-weighted, vector-valued, or otherwise aggregated;
- what a tolerance means and what relation compares loss to it;
- whether randomized decoders/channels are required;
- whether a single objective, preorder, partial order, or Pareto relation is required for cost;
- what conditions support existence of minimal elements;
- what additional conditions, if any, support a unique least element;
- when zero approximate loss does or does not recover exact sufficiency;
- whether operational semantics can be a backward-compatible successor to `far-ir/2.0` or require a stronger version boundary.

No source family may be forced into another family's native semantics merely to obtain a single architecture.

### Stage D — formal/computational checks

Construct finite-explicit witnesses and adversarial controls that test at least:

- dependence on the chosen loss or distortion;
- dependence on the aggregation/reference distribution;
- dependence on tolerance;
- nonseparating zero-loss cases;
- cost-preorder incomparability;
- nonunique minimal candidates;
- scalarization/preference dependence where applicable;
- exact/approximate boundary cases;
- failure when required declarations are omitted.

Use independent computation where useful. A finite computation certifies only the encoded finite claim.

### Stage E — hostile audit and promotion

Re-run canonical repository validation, mutation tests, provenance/hash checks, and review findings. Promote W5 only if the exact completed scope is internally consistent and all failures/nonclaims are retained.

## Frozen native query set

### Statistical experiments and decision risk

- `W5-Q-DE-01`: `comparison of statistical experiments deficiency distance decision risk approximate sufficiency`
- `W5-Q-DE-02`: `Le Cam deficiency randomization criterion bounded loss decision problems`
- `W5-Q-DE-03`: `approximate sufficient statistics excess risk decision theory`

### Information theory and lossy representation

- `W5-Q-IT-01`: `rate distortion theory distortion measure lossy compression optimal representation`
- `W5-Q-IT-02`: `information bottleneck relevance distortion task loss representation`
- `W5-Q-IT-03`: `rate distortion multiple distortion measures nonunique optimum`

### Behavioral and model abstraction

- `W5-Q-BM-01`: `approximate bisimulation behavioral pseudometric model reduction error bounds`
- `W5-Q-BM-02`: `simulation metrics abstraction error probabilistic systems`
- `W5-Q-BM-03`: `model reduction output error norms approximation error bounds`

### Statistical learning and calibration

- `W5-Q-SL-01`: `surrogate loss calibration excess risk decision tasks`
- `W5-Q-SL-02`: `task aware representation learning sufficiency risk information`
- `W5-Q-SL-03`: `loss functions Bayes risk approximation representation`

### Multiobjective optimization and order structure

- `W5-Q-MO-01`: `multiobjective optimization Pareto preorder scalarization nonunique optimum`
- `W5-Q-MO-02`: `partial order costs resource tradeoffs Pareto minimality`
- `W5-Q-MO-03`: `multiobjective optimization preference dependence scalarization limitations`

### Computational and resource cost

- `W5-Q-RC-01`: `computational complexity time space communication tradeoff representation`
- `W5-Q-RC-02`: `description length model complexity computation tradeoff`
- `W5-Q-RC-03`: `sample complexity computational complexity statistical tradeoff`

## Discovery stack and evidence roles

- **Acumen/Talarion**: first current-state/gap brief before broader discovery; not canonical evidence by itself.
- **Consensus**: literature discovery and paper-level retrieval; underlying papers must be fetched/verified before citation.
- **SciSpace**: independent literature discovery/triage using the frozen native questions.
- **Scite**: citation-context/support/dispute/context checks for selected papers; citation labels are not proof.
- **ordinary web/primary-source search**: primary papers, official versions, standards, and current gaps.
- **Wolfram**: independent symbolic/numeric/finite verification after the native concept freeze; computational output is scoped evidence only.
- **Zotero**: intended bibliography/provenance lane. The installed Zotero skill requires a local Zotero Desktop/helper environment not exposed in this chat runtime; this limitation must be recorded rather than represented as a successful Zotero-managed library operation.
- **GitHub**: sole canonical authority for freezes, source manifests, results, tests, hashes, review adjudication, and promotion.

## Inclusion criteria

Prefer primary papers, monographs/standards by responsible authors or institutions, and authoritative technical treatments that explicitly define or prove relationships among approximation, deficiency, distortion, loss/risk, tolerance, cost, preorders, Pareto minimality, or complexity/resource tradeoffs.

A source is retained only if its identity is verifiable and its role in W5 can be stated without importing a Project FAR conclusion into the source.

## Rejection rules

Reject or quarantine:

- unverified discovery summaries;
- sources selected only because their terminology resembles FAR;
- purely empirical benchmark claims with no relevant formal semantics when used to justify a formal definition;
- citation-count or support-label arguments presented as theorem proof;
- arbitrary scalar cost weights without an independently declared preference basis;
- negative search results presented as novelty or priority proof;
- any mapping performed before the native concept/source freeze.

## Required terminal distinctions

W5 outputs must preserve at least:

- exact vs approximate adequacy;
- discrepancy/loss declaration vs metric special case;
- pointwise/worst-case vs distribution-weighted/expected aggregation;
- tolerance declaration vs achieved loss;
- adequacy vs cost comparison;
- least vs minimal vs Pareto-minimal vs incomparable;
- existence vs uniqueness;
- deterministic vs randomized transformation when relevant;
- internally authored mapping vs externally supplied framing/evaluation;
- mathematical result vs finite software certificate vs empirical evidence.

## Nonclaims

W5 does not establish, merely by successful execution:

- a universal metric, divergence, loss, tolerance, aggregation rule, or cost order;
- a universal unique cost-optimal representation;
- empirical usefulness or disagreement reduction;
- open-domain completeness;
- external-investigator independence;
- novelty or priority;
- computational tractability of the exact observational quotient;
- that zero loss recovers exact sufficiency without the required separation/aggregation assumptions;
- that a finite Pareto-minimal candidate is globally optimal outside its declared candidate set and preorder.

## Reopening rule

The core theory reopens only for a reproducible contradiction to a stated theorem, proof step, or formal premise. A new approximation convention, cost model, implementation tradeoff, or domain failure is downstream unless it satisfies that rule.
