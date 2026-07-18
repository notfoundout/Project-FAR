# PBTS-001 Independent Replication Package v1.0

## Status

Frozen prospective replication package for `PBTS-001-REP-001`.

This package defines how independent replication may be conducted. It contains no participant registrations, submissions, scores, adjudications, or replication results. The scoped FARA representation-theorem gate remains closed.

## Purpose

Replicate the frozen PBTS-001 preservation-basis evaluation through genuinely separate evaluation or implementation paths, without changing PB-001, PBTS-001, IRD-001, or the reasoning-domain specification after exposure.

The replication asks whether independently constructed paths reproduce the scoped discrimination, ablation, coverage, hidden-recovery, and addition-search findings reported internally in RUN-001. It also tests whether P8 should remain an ordinary preservation coordinate, become a cross-cutting evidential qualifier, become a separate evidence contract, require revision, or remain unresolved.

## Evidence classification

The primary evidence class is `replication`.

The target replication layer is R3 independent technical replication. Each completed submission must be classified at the strongest justified layer:

- R1 when the same team and path are repeated;
- R2 when isolated implementations are produced by the same person, agent, or organization;
- R3 only when a separate person or organization independently executes the frozen package without generated artifacts or unpublished repair knowledge;
- R4 only when an adversarially independent group also controls objections, cases, or adjudication;
- R5 only after materially different contexts or designs are included.

No submission is upgraded merely because it uses a different prompt, process label, software file, or isolated runtime.

## Frozen protected inputs

The participant-facing package is restricted to the following protected inputs and package artifacts. The Git blob identifiers are frozen in the replication registry.

1. `docs/research/reasoning-domain-specification-v1.0.md`
2. `docs/research/independent-reasoning-definition-v1.0.md`
3. `docs/research/preservation-basis-investigation-v1.0.md`
4. `theory/evaluation/preservation-basis-registry.json`
5. `docs/research/pb001-preservation-basis-test-suite-v1.0.md`
6. `theory/evaluation/pb001-test-suite-registry.json`
7. this replication protocol;
8. the response schema;
9. the unrelated calibration exercise.

Material alteration of any protected input creates a new replication-package version. An erratum may correct only a demonstrably outcome-invariant transcription or packaging error and must be registered before affected submissions are accepted.

## Excluded prior-result artifacts

The participant-facing bundle must exclude:

- `docs/research/pb001-execution-run-001-report.md`;
- `theory/evaluation/pb001-execution-run-001-records.json`;
- `theory/evaluation/pb001-execution-run-001-summary.json`;
- derivative summaries of RUN-001 judgments;
- unpublished explanations of why an internal judgment was assigned;
- any prepared consensus answer key for PBTS-001.

The repository is public, so technical prevention of all prior access is impossible. Each replicator must therefore declare exposure truthfully. A submission made after access to RUN-001 results remains preserved but is classified as unblinded and cannot satisfy the R3 gate for this package.

## Replication units

Three independently constructed primary paths are required. Each path receives an opaque identifier: `REP-A`, `REP-B`, or `REP-C`. Identity and provenance are stored in a coordinator-controlled registration record and are not used during scoring.

A primary path may be:

- an independent formal evaluator;
- an independent implementation of the frozen evaluation contracts;
- an independent team combining implementation and adjudication, provided internal roles are declared;
- an adversarial evaluator satisfying stronger R4 conditions.

Multiple paths created by one person, one assistant context, or one organization count as R2 at most, regardless of isolation.

## Eligibility

Every primary replicator must:

1. be able to read formal specifications and state-transition or related process models;
2. complete the unrelated calibration exercise before receiving PBTS-001 materials;
3. have had no role in authoring IRD-001, PB-001, PBTS-001, or RUN-001;
4. declare organizational, funding, supervisory, authorship, and collaboration relationships relevant to independence;
5. declare prior exposure to Project FAR and specifically to RUN-001 results;
6. agree not to communicate with other replicators before submission freeze;
7. agree to preserve unfavorable, partial, unknown, and rejected records;
8. disclose all tools, models, code, assistants, and external materials used.

The minimum passing calibration result is five of six items with no failure on the observation-versus-inference item. Calibration checks specification-reading competence; it is not evidence about PB-001.

## Independence gate

A primary submission counts toward the R3 gate only when all of the following are true:

- the replicator is a distinct person or organization from Project FAR authorship and RUN-001 execution;
- no material assistance was received from another registered replicator;
- no access to RUN-001 result artifacts or derivative judgments occurred before submission freeze;
- no generated mapping, scoring artifact, or unpublished repair knowledge was supplied;
- the evaluation or implementation was constructed from the frozen participant-facing package;
- all tooling and assistance are disclosed;
- the independence auditor accepts the declaration without unresolved conflict.

The package requires three valid primary submissions and at least two distinct organizational affiliations, unless an auditor documents that unaffiliated replicators are operationally independent. Failed independence checks do not delete a submission; they downgrade its evidential layer.

## Role separation

The replication distinguishes:

1. package coordinator;
2. replicator or implementation author;
3. calibration scorer;
4. independence auditor;
5. adjudicator;
6. deterministic aggregation operator;
7. red-team reviewer.

No person may serve simultaneously as a primary replicator and final adjudicator of that replicator's disputed records. The coordinator may validate schema and completeness but may not repair substantive answers.

## Calibration

The calibration exercise is defined in `docs/research/pbts001-independent-replication-calibration-v1.0.md` and is unrelated to PB-001 labels and RUN-001 cases.

Calibration must be completed and frozen before participant-facing PBTS materials are released. The raw response, score, scorer identity, date, and any retest must be preserved. One retest using a separately ordered item form is allowed. Failure after retest makes the person ineligible as a primary replicator but does not prohibit a separately declared implementation-support role.

## Participant-facing execution

Each primary replicator must independently complete:

- all eight paired-axis discrimination cases;
- all eight axis ablations;
- D1-D16 domain coverage review;
- all ten mandatory IRD countermodels;
- all registered hidden-recovery checks;
- all ten adversarial addition-search hypotheses;
- the dedicated P8 classification task;
- deviation, tool-use, exposure, and nonclaim declarations.

The response schema fixes allowed values and required justifications. Blank, malformed, late, exposed, or materially assisted submissions are preserved with rejection or downgrade reasons.

## P8 classification task

Without access to RUN-001 judgments, every replicator must select and justify one of:

- `ordinary_preservation_coordinate`;
- `cross_cutting_evidential_qualifier`;
- `separate_evidence_contract`;
- `axis_revision_required`;
- `unresolved`.

The replicator must state:

- what source distinction P8 protects;
- whether it can vary independently of P1-P7;
- whether removing it causes representational loss, claim overreach, or only evidence-classification loss;
- how the answer changes representation-theorem obligations;
- what counterexample would change the classification.

Consensus is not required. Material disagreement keeps the P8-dependent theorem obligation unresolved.

## Append-only submission controls

Responses are append-only after submission. A correction creates a new version linked to the prior response and must state whether it is clerical or substantive.

The coordinator records:

- submission identifier and digest;
- received timestamp;
- package version;
- calibration status;
- exposure and independence declarations;
- tool and assistance disclosure;
- validation errors;
- acceptance, rejection, or downgrade status;
- all later adjudication events.

No original response is overwritten or deleted.

## Embargo and exposure control

All primary submissions remain mutually inaccessible until all three are frozen or a preregistered deadline expires. Replicators may not see another submission, coordinator notes, preliminary aggregates, or RUN-001 comparisons before freeze.

The coordinator must not provide hints based on emerging agreement. Questions are answered only through package-wide written clarifications delivered identically to every active replicator and preserved in an errata log.

## Adjudication

Schema-valid replicator judgments are not changed to manufacture consensus. Adjudication may classify:

- protocol compliance;
- whether a stated recovery mechanism is counted or hidden;
- whether an answer addresses the frozen distinction;
- whether a deviation is material;
- whether independence is established;
- whether evidence supports the chosen replication layer.

Substantive disagreement remains in the distribution. The adjudicator may mark a response `invalid` only with a cited frozen rule and preserved rationale.

## Deterministic aggregation

Aggregation operates only after submission freeze.

For each P1-P8 paired test, report the full distribution of `pass`, `partial`, `fail`, and `unknown` across valid primary submissions.

- Existential independent discrimination is present when at least one valid R3 path produces `pass` or justified `partial` without hidden recovery.
- Reproducible independent discrimination requires all three valid R3 paths to produce `pass` or justified `partial`, with no `fail` and no unresolved hidden recovery.
- Any `unknown` prevents a 3/3 reproducible claim for that item.

For each ablation:

- `loss_detected`, `recoverable_with_counted_commitment`, and `hidden_reintroduction` count as evidence that removal was not demonstrated lossless;
- `no_observed_loss` or `unknown` keeps nonredundancy unresolved and triggers targeted follow-up;
- no finite ablation result proves global necessity.

A candidate new general axis from any valid primary path closes the advance gate pending independent adjudication and PB revision analysis. Domain-specific distinctions are retained but do not automatically create a general axis.

## Replication comparison with RUN-001

RUN-001 remains hidden until all primary submissions are frozen. Comparison then reports:

- exact agreement and disagreement by pair, ablation, countermodel, and addition hypothesis;
- whether RUN-001 was more favorable, less favorable, or simply different;
- whether disagreements track observability, interpretation, implementation, or authoring assumptions;
- whether P3, P6, or P8 concerns replicate independently;
- whether any internal result appears dependent on proponent framing.

RUN-001 is not used as the answer key.

## Advance gate

The representation-theorem gate remains closed until a later results artifact establishes all of the following:

- three valid primary submissions are complete;
- calibration and independence records are complete;
- each submission used unchanged protected inputs;
- all PBTS-001 families are completed or explicitly unresolved;
- full distributions and rejected records are registered;
- hidden-recovery adjudication is complete;
- no candidate new general axis remains unresolved;
- no required IRD, domain, PB, or suite revision remains unresolved;
- P8's theorem role is resolved or represented through explicit alternative theorem obligations;
- the maximum justified replication layer is recorded;
- nonclaims and unfavorable results are published.

Package freeze alone satisfies none of these gates.

## Allowed outcomes

- R3 scoped replication support;
- R2 implementation-path robustness only;
- partial replication;
- nonreplication of one or more axes;
- axis redundancy or revision pressure;
- required new general axis;
- class-specific bases;
- P8 reclassification;
- IRD, domain, PB, or suite revision required;
- independence failure;
- observability-blocked result;
- insufficient evidence.

## Nonclaims

This package does not establish:

- that independent replicators have been registered;
- that PBTS-001 has been independently executed;
- PB-001 sufficiency, necessity, independence, minimality, or completeness;
- resolution of P8;
- FARA compliance;
- a representation theorem;
- universality, global minimality, superiority, or comparative economy.

## Next required artifact

Register qualified independent replicators and freeze `PBTS-001-REP-001-RUN-001` assignments, calibration records, exposure declarations, and append-only submission channels without adding any replication result.