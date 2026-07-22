# EVC-W3 R4 adversarial package audit

## Scope

This audit checks whether the repository now contains a complete frozen package for `EVC-W3-R4-ADVERSARIAL-REPLICATION` without claiming that an external adversarial team has executed it.

## Findings

The package includes the parent `POST-USD-EVC-001` program, terminal synthesis, complete USD-W1 through USD-W6 evidence chain, negative and boundary evidence, formal and validation evidence, an explicit twelve-case challenge corpus, a team guide, and a machine-readable result template.

The protocol distinguishes R4 from:

- internal red-team or multi-implementation robustness;
- EVC-W1 external proof review;
- EVC-W2 R3 independent technical reimplementation;
- EVC-W4 full candidate expansion;
- EVC-W5 cross-context replication;
- EVC-W6 empirical correspondence testing.

The team may challenge the benchmark and conceptual framework rather than merely rerun the current implementation. It must attempt every registered challenge and preserve unsuccessful attacks.

## Independence and contamination controls

Eligibility requires a separate human or organization uninvolved in artifact construction. Same-controller agent runs, author simulation, preferred-verdict coaching, and selective evidence access are disqualifying.

The immutable release identifier, first-access timestamp, communication log, initial report freeze, and post-access versioning rule prevent silent repair or retrospective rewriting.

## Decision integrity

The weakest-gate rule prevents a strong verdict when a mandatory attack domain is incomplete. `scope_limited` remains distinct from `refuted`, and inability to construct a counterexample is explicitly barred from proving universality or exhaustiveness.

## Current state

The package is `frozen_unexecuted` and `frozen_unreleased`. No adversarial team has been recruited, no first access has occurred, no report exists, and no R4 verdict is claimed.

## Nonclaims

This audit does not establish package completeness independently of the validator, substantive correctness of the USD results, survival under adversarial criticism, candidate exhaustiveness, universal structure, or actual-process correspondence.
