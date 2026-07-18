# PBTS-001 RUN-001 Execution and Interpretation Report

## Status

Executed internal methodological study against the frozen PBTS-001 v1.0 suite.

This report records scoped internal evidence only. It is not independent replication and does not open the FARA representation-theorem gate.

## Frozen inputs

RUN-001 used the following artifacts without changing them after exposure:

- `docs/research/pb001-preservation-basis-test-suite-v1.0.md`;
- `theory/evaluation/pb001-test-suite-registry.json`;
- `docs/research/preservation-basis-investigation-v1.0.md`;
- `theory/evaluation/preservation-basis-registry.json`;
- `docs/research/independent-reasoning-definition-v1.0.md`;
- `docs/research/reasoning-domain-specification-v1.0.md`.

The execution records pin the available blob hashes for the suite and preservation-basis registries.

## Execution design

Three evaluation methods were applied:

1. **EV-A — Literal contract:** used only distinctions explicitly stated in the frozen source, observation, pair, and axis contracts.
2. **EV-B — Adversarial collapse:** attempted to collapse the target distinction while holding other axes fixed and recorded the first material false equivalence.
3. **EV-C — Observability and reintroduction:** tested whether preservation depended on hidden state, metadata, evaluator repair, runtime interpretation, or information unavailable at the declared observation stratum.

These are separately specified methods, not independent evaluators. All were authored in one assistant context. RUN-001 therefore establishes only internal methodological robustness.

## Preserved records

The execution preserves:

- 24 paired-axis responses;
- 24 ablation responses;
- 32 D1-D16 coverage records;
- 10 mandatory countermodel results;
- 8 rejected hidden-recovery attempts;
- 10 adversarial addition-search classifications;
- 4 rejected or invalid records.

Rejected records remain visible and do not disappear from the aggregate.

## Paired-axis results

| Axis | Pass | Partial | Fail | Unknown | RUN-001 interpretation |
|---|---:|---:|---:|---:|---|
| P1 Configuration | 2 | 1 | 0 | 0 | Valid at white-box scope; lower observability may block component identity. |
| P2 Commitment | 3 | 0 | 0 | 0 | Clear discrimination among acceptance, rejection, suspension, and confidence states. |
| P3 Stake and alternatives | 2 | 1 | 0 | 0 | Distinct, but exact isolation from commitment and consequence is imperfect. |
| P4 Grounds and justification | 3 | 0 | 0 | 0 | Clear discrimination among admissible, inadmissible, causal, correlational, and authority grounds. |
| P5 Admissibility and dynamics | 3 | 0 | 0 | 0 | Equal outputs do not preserve future permitted transitions or rule revision. |
| P6 Consequence | 2 | 1 | 0 | 0 | Action and institutional effects discriminate, though some cases can be encoded as counted commitment changes. |
| P7 History and path | 3 | 0 | 0 | 0 | Equal endpoints do not preserve provenance, path-dependent permissions, or revision duties. |
| P8 Evidential correspondence | 2 | 0 | 0 | 1 | Required to prevent unsupported evidence upgrades, but its status as an axis rather than a mandatory qualifier remains unresolved. |

Every axis has at least one valid internal discriminating pair. That is existential internal support, not independent reproducible support.

## Ablation results

Removing P1, P2, P4, P5, or P7 produced direct loss in all three methods.

Removing P3, P6, or P8 produced either direct loss or recovery only through explicit counted machinery:

- P3 required a question or contrast-set commitment;
- P6 required explicit downstream-state or policy machinery;
- P8 required an evidence-grade or correspondence qualifier.

No axis was removed without observed loss or counted recovery. RUN-001 therefore found no internally demonstrated redundant axis.

This is not a proof of necessity. The suite is finite, constructed, and internally evaluated.

## Domain coverage

All sixteen domain classes received:

- one ordinary or representative case;
- one pressure or boundary-adjacent case.

The 32-case inventory spans O0 through O3 observability and includes symbolic, probabilistic, causal, scientific, legal, analogical, planning, learning, language-model, agentic, human, collective, embodied, reflective, and adversarial cases.

Ten cases retain explicit unknowns because their observation contracts do not support stronger internal-process claims. These include creative analogy, representation change, opaque language-model behavior, asynchronous agents, human tacit reasoning, institutional reasoning, continuous embodied control, and deceptive traces.

Coverage completeness means the registered cells were populated. It does not mean the cases are statistically representative or that PB-001 is adequate for every system in each class.

## Mandatory countermodels

Seven countermodels produced clear expected discrimination:

- arbitrary labeled transition;
- output-equivalent lookup;
- post hoc narrative;
- hidden operator;
- trivial universal encoding;
- distributed reasoning;
- self-revision;
- conflicting normative reasons.

Two received partial outcomes:

- pure optimization remains boundary-sensitive because sufficiently instrumented alternative-sensitive optimization may satisfy IRD-001;
- continuous embodied control remains partly underdetermined because operational segmentation at O2 may be nonunique.

These are preserved as pressure points rather than converted into favorable results.

## Hidden-recovery audit

Eight attempted recoveries were rejected:

- compiler-generated hidden configuration;
- commitment metadata;
- evaluator-supplied stakes;
- external knowledge of grounds;
- runtime interpretation of admissibility;
- uncounted consequence policies;
- history stored outside the scored representation;
- unsupported correspondence assumptions.

No accepted result relies on an uncounted hidden recovery in RUN-001.

## Adversarial addition search

No required new general axis was identified in the ten frozen hypotheses.

Five hypotheses were classified as already subsumed:

- uncertainty calibration;
- institutional authority;
- ontology change;
- causal intervention structure;
- public/private commitment separation.

Four require clarification within existing axes:

- resource and computational bounds under P5/P6;
- environmental embedding under P1/P5/P7;
- representational granularity under P1/P8;
- termination and liveness under P5/P7.

Agency, authorship, and responsibility were classified as domain-specific rather than constitutive of every reasoning episode.

No axis was added. Any later addition requires PB-002 or another explicit version.

## Rejected records

RUN-001 preserves four rejected records:

1. a P3 pair that also changed P6 without declaring the overlap;
2. a P5 ablation recovery using an uncounted runtime interpreter;
3. an opaque language-model case incorrectly labeled O2 rather than O0;
4. a pure-optimizer judgment forced into a binary classification despite insufficient instrumentation.

These rejections materially constrain the favorable interpretation.

## Decision

The substantive PBTS-001 conditions received scoped internal support:

- every P1-P8 axis has a valid internal pair;
- every ablation showed loss or counted recovery;
- D1-D16 inventory coverage is complete;
- all mandatory countermodels were exercised;
- hidden-recovery auditing is complete;
- no required new general axis was found;
- no contradiction currently requires changing IRD-001 or the frozen domain;
- results and nonclaims are registered.

However, PBTS-001 also required at least three independently constructed evaluations where construction was required. RUN-001 contains three methods, but they were created in one context. Treating them as independent would repeat the implementation-independence error corrected by PR #210.

Therefore:

> PB-001 receives scoped internal methodological support, while the representation-theorem gate remains closed pending independently implemented or externally evaluated replication.

## P8 issue

P8 behaved differently from the other axes.

P1-P7 primarily describe distinctions in a reasoning process or its effects. P8 describes the warrant for asserting that a representation corresponds to that process.

RUN-001 confirms that removing P8 permits unsupported evidence upgrades, but it does not settle whether P8 should remain:

- an ordinary coordinate in the preservation vector;
- a mandatory qualifier applied to every coordinate;
- or a separate meta-level evidence contract.

Independent replication should be instructed to test this exact issue rather than silently resolving it.

## Current claim boundary

RUN-001 supports only this claim:

> Within the frozen PBTS-001 constructions and one internally authored three-method evaluation, each PB-001 axis discriminated at least one registered distinction, no axis ablation was lossless without counted recovery, and no additional general axis was required by the frozen addition search.

RUN-001 does not establish:

- PB-001 sufficiency across the full frozen domain;
- necessity, independence, minimality, or completeness;
- representative domain coverage;
- external or independent replication;
- FARA compliance;
- a FARA representation theorem;
- universality, superiority, or comparative economy.

## Next required work

Execute the frozen PBTS-001 package through independently implemented or externally evaluated paths.

The next package must:

- preserve the exact PB-001 and PBTS-001 versions;
- give evaluators no access to RUN-001 judgments before submission;
- preserve all disagreements and unknowns;
- test whether P8 is a coordinate or meta-level qualifier;
- report provenance and independence level explicitly;
- keep the representation-theorem gate closed unless the independence requirement is genuinely satisfied.
