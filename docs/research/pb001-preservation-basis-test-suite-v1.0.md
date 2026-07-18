# PB-001 Preservation-Basis Test Suite v1.0

## Status

Frozen prospective test suite. This artifact defines tests but contains no executed scores and establishes no preservation claim.

## Purpose

Test whether PB-001's eight axes are sufficient, independently discriminating, nonredundant, and architecture-neutral across the frozen reasoning domain and IRD-001.

The suite must be interpreted before any FARA representation theorem is attempted.

## Frozen inputs

- `docs/research/reasoning-domain-specification-v1.0.md`
- `docs/research/independent-reasoning-definition-v1.0.md`
- `docs/research/preservation-basis-investigation-v1.0.md`
- `theory/evaluation/preservation-basis-registry.json`

No input may be edited after exposure to suite results without a new version and supersession record.

## Evaluation unit

A test case contains:

- stable case identifier and version;
- source-system pair or ablation target;
- independently stated source distinction;
- intended target axis or missing-axis hypothesis;
- all non-target axes intended to remain fixed where feasible;
- observability stratum;
- admissible evidence;
- prohibited repairs;
- expected discriminating result;
- ambiguity and failure conditions.

A test does not pass merely because labels differ. The distinction must have an observable or formally specified effect relevant to IRD-001.

## Scoring

Each axis is scored `pass`, `partial`, `fail`, or `unknown`.

`Unknown` is unordered. It is not weaker than Partial or stronger than Fail.

A paired test supports discrimination only when the target difference is preserved without reconstructing it through metadata, an interpreter, evaluator judgment, runtime behavior, hidden state, or candidate-specific repair.

## Family A — Paired-axis discrimination

Exactly eight primary pairs are frozen.

### PA-01 — Configuration

Two systems retain the same commitments, stake, grounds, transition behavior, consequences, history length, and evidence grade, but differ in whether two operationally distinct state components remain distinguishable.

Target: P1.

Failure exposed: state/configuration collapse.

### PA-02 — Commitment

Two systems share configuration shape and transitions but differ in which alternative is accepted, rejected, suspended, or assigned confidence.

Target: P2.

Failure exposed: commitment-state collapse.

### PA-03 — Stake and alternatives

The same apparent conclusion is reached under different questions or live alternative sets, changing what the conclusion resolves.

Target: P3.

Failure exposed: context-free conclusion equivalence.

### PA-04 — Grounds and justification

The same commitment follows from different grounds, one admissible and one inadmissible or one causal and one merely correlational.

Target: P4.

Failure exposed: dependency or justification collapse.

### PA-05 — Admissibility and dynamics

Two systems share states and outputs but differ in which transitions are permitted, including a rule revision that changes later possible moves.

Target: P5.

Failure exposed: extensional output equivalence masking operational difference.

### PA-06 — Consequence

Two episodes end in textually identical statements but differ in downstream policy, action, entitlement, burden, confidence, or permitted inference.

Target: P6.

Failure exposed: consequence-free semantic equivalence.

### PA-07 — History and path

Two systems reach the same current configuration and commitment through histories that create different dependencies, permissions, provenance, or revision obligations.

Target: P7.

Failure exposed: endpoint-only representation.

### PA-08 — Evidential correspondence

Two records contain identical visible traces, but one is only self-reported and the other is linked by instrumentation or proof to the producing process.

Target: P8.

Failure exposed: unsupported upgrade from E0/E1 to E2.

## Family B — Axis ablations

For each P1-P8, construct an otherwise unchanged evaluator contract with that axis removed.

An ablation result must be classified as:

- `loss_detected`: at least one frozen distinction becomes unscoreable or falsely equivalent;
- `recoverable_with_counted_commitment`: recovery is possible only by adding explicit machinery counted under the cost model;
- `hidden_reintroduction`: recovery occurs through an uncounted alias or mechanism;
- `no_observed_loss`: no loss appears in the frozen suite;
- `unknown`: evidence is insufficient.

`No observed loss` does not establish redundancy. It triggers additional adversarial search.

## Family C — Domain coverage

Every D1-D16 target class must be covered by at least two cases:

- one ordinary or representative case;
- one pressure, unfavorable, opaque, self-modifying, distributed, continuous, adversarial, or boundary-adjacent case.

Coverage records must identify:

- target class;
- variation axes exercised;
- observability stratum;
- PB-001 axes materially at issue;
- source provenance;
- candidate-author involvement;
- unresolved limitations.

Coverage count alone is not adequacy evidence.

## Family D — IRD-001 countermodel coverage

The suite must include all ten mandatory countermodels:

1. arbitrary labeled transition;
2. output-equivalent lookup;
3. post hoc narrative;
4. hidden operator;
5. pure optimizer;
6. trivial universal encoding;
7. distributed reasoning;
8. self-revision;
9. continuous embodied control;
10. conflicting normative reasons.

For invalid or boundary countermodels, the suite must test whether PB-001 prevents a representation from manufacturing preservation that the observation contract does not support.

For positive pressure cases such as distributed reasoning, self-revision, continuous embodied control, and conflicting normative reasons, the suite must test whether PB-001 can preserve the relevant distinctions without forcing symbolic, centralized, discrete, or fixed-rule structure.

## Family E — Hidden-recovery audit

Every apparent preservation must be audited for recovery through:

- aliases or renamed primitives;
- unrestricted metadata;
- compiler-generated hidden state;
- verifier assumptions;
- runtime interpreters;
- evaluator repair;
- external operator knowledge;
- uncounted exception policies;
- trace information unavailable at the declared observability stratum.

A functionally equivalent reconstruction counts as reintroduction regardless of terminology.

## Family F — Adversarial addition search

Search for distinctions relevant to IRD-001 that can vary while P1-P8 remain apparently equal.

At minimum test hypotheses involving:

- resource and computational bounds;
- agency, authorship, and responsibility;
- uncertainty calibration;
- social authority and institutional role;
- spatial or environmental embedding;
- representational granularity;
- type creation and ontology change;
- counterfactual or causal intervention structure;
- privacy and public/private commitment separation;
- termination, liveness, and open-endedness.

A discovered distinction is classified as:

- already subsumed by one or more axes;
- a required clarification of an axis;
- a candidate new axis;
- domain-specific rather than general;
- irrelevant to faithful reasoning representation;
- unresolved.

No new axis may be added after execution without PB-002 or a later version.

## Execution design

The suite is executed in a separate PR after this freeze.

Execution must:

1. preserve every response and rejected record;
2. use at least three independently constructed mappings or evaluations where construction is required;
3. report full distributions rather than only favorable aggregates;
4. separate existential support from reproducible support;
5. retain Unknown without forced ordering;
6. apply full-cost and anti-reintroduction rules;
7. disclose candidate-author and evaluator independence;
8. avoid modifying PB-001 after exposure;
9. classify failures as axis, suite, IRD, observation, mapping, or evidence failures;
10. publish unfavorable and unresolved outcomes.

## Decision rules

PB-001 may advance to scoped representation-theorem work only if:

- every P1-P8 axis has at least one valid discriminating pair;
- every axis ablation produces loss, counted recovery, or remains explicitly unresolved after adversarial search;
- D1-D16 coverage requirements are complete;
- all mandatory countermodels are covered;
- hidden-recovery audits are complete;
- no discovered missing distinction remains classified as a required general axis;
- no contradiction requires changing IRD-001 or the frozen domain;
- results and nonclaims are registered.

Failure of this gate requires PB revision, domain restriction, IRD revision, class-specific bases, or an unresolved result. It may not be bypassed by beginning a favorable FARA theorem.

## Allowed outcomes

- PB-001 receives scoped empirical or formal support;
- one or more axes are redundant;
- one or more axes require revision;
- a new general axis is required;
- different domain classes require different bases;
- no finite basis is adequate;
- IRD-001 requires revision;
- observability prevents resolution;
- evidence remains insufficient.

## Nonclaims

Freezing this suite does not establish PB-001 sufficiency, necessity, independence, minimality, completeness, FARA compliance, a representation theorem, universality, superiority, or independent replication.
