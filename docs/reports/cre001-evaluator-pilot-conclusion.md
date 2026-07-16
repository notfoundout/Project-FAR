# CRE-001 Evaluator Pilot Conclusion

Status: Decision recorded.
Date: 2026-07-15.
Scope: CRE-001 evaluator-based pilot workstream.

## Decision

Conclude the evaluator-correction workstream initiated by the first Claude CRE-001 pilot and supersede its planned next action with development of a deterministic CRE-001 verifier.

The preserved v1 pilot remains an immutable, noncanonical historical artifact. It is not reverted, promoted, adjudicated, or counted as experimental evidence.

No additional Claude correction round is required for this pilot.

## Reason

The pilot exposed a recursive process:

1. an evaluator generated a mapping;
2. a reviewer identified mapping, preservation, and complexity defects;
3. the evaluator corrected those defects;
4. the correction introduced new normalization and audit questions;
5. another review and correction round became necessary.

This process does not provide an objective stopping condition. It also combines mapping with evaluator self-assessment and leaves important quantities dependent on judgment, including:

- semantic-clause duplication;
- derived-construct normalization;
- construct indispensability;
- preservation grading;
- treatment of scenario ambiguities.

The core CRE-001 claim is better framed as a formal comparison problem: does a structured candidate representation preserve the states, enabled transitions, updates, history, termination behavior, dependencies, prohibitions, and observable outputs of a formal reference scenario?

## Superseding direction

Build a narrow deterministic CRE-001 verifier with four initial artifacts:

1. a machine-readable reference scenario;
2. a machine-readable candidate mapping format;
3. an executor that generates canonical reachable behavior;
4. a comparator that reports mismatches and shortest counterexample traces.

The first verifier should check:

- proposition and rule coverage;
- initial-state equality;
- transition guard equality;
- update equality;
- rule-status modification behavior;
- ordered append-only history;
- terminal-state behavior;
- prohibited-state and prohibited-transition reachability;
- required-output recoverability;
- the acceptance-after-modification branch;
- explicitly registered ambiguity policies.

Complexity values should be derived from canonical machine-readable structures where possible rather than trusted from evaluator self-reports.

## What remains valid from the pilot

The pilot remains useful because it documents concrete failure modes that the verifier must address:

- incorrect internal clause references;
- inconsistent atomic-clause counting;
- disputed derived-construct indispensability;
- ambiguity around prohibited-transition occurrence;
- ambiguity around unterminated outputs;
- repeatability ambiguity for `T_disable_reject`;
- omission of a reachable modification-then-accept branch;
- overstated preservation conclusions.

These findings become verifier requirements and fixtures, not additional evaluator prompts.

## Nonclaims

This decision does not establish:

- sufficiency of the assigned vocabulary;
- necessity or minimality of any primitive set;
- comparative superiority over another vocabulary;
- reproducibility across evaluators;
- universality of Project FAR.

It changes the method used to seek evidence. It does not change the evidentiary status of CRE-001.

## Next implementation task

Create a focused implementation PR for the deterministic CRE-001 verifier with tested valid and invalid fixtures. The verifier should fail with machine-readable diagnostics and a shortest counterexample whenever the candidate model diverges from the reference model.
