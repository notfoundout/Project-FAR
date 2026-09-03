# PCA-W6 Empirical Audit Utility — Preregistration v1.0

Status: **FROZEN BEFORE EXECUTION**

Program: `POST-CLOSURE-001`

Workstream: `PCA-W6-EMPIRICAL-AUDIT-UTILITY`

Protocol base: `main@2cecf2e21cc27208f606dcd38337af4369e66af2`

## Question

On the six already-frozen W4 repaired finite-explicit comparison contracts, does the Project FAR semantic audit detect a deliberately injected material representational collision that remains valid at the JSON-Schema level, while leaving the unmodified repaired controls unflagged?

This is a bounded controlled artifact experiment. It is not a human-subject study, field deployment, external-investigator evaluation, or claim that FAR reduces real-world disagreement.

## Registered corpus

The corpus is fixed by `research/results/pca-w4-domain-contracts/manifest.json` at the protocol base. The six `variant = repaired` records are the primary negative controls. Their six paired `variant = lossy` records are a preregistered secondary positive-control replication set.

No W6 result may add or remove W4 records after seeing W6 outcomes.

## Conditions

### B0 — schema-only baseline

Validate document shape against `schemas/far-contract-v2.schema.json`. B0 flags an item only when the schema rejects it. B0 intentionally does not recompute factorization or collisions.

This baseline represents minimal syntactic conformance, not unaided human review. No conclusion about human reviewers may be drawn from B0.

### A1 — FAR semantic audit

Run `mechanization.far_mechanization.contract_v2.validate_contract` and interpret its checked typed evidence. A repaired control is accepted only when semantic validation succeeds. A native lossy control counts as detected material loss only when semantic validation succeeds and the record carries checked `REFUTED` collision evidence. An injected mutant counts as detected when semantic validation fails after the registered collision injection.

### O1 — independent collision oracle

Independently scan only `contract.required_behavior.table` and `contract.representation.table`, using canonical JSON equality. O1 reports material collision iff two distinct registered cases share a representation value while their required behaviors differ. O1 does not call the FAR semantic verifier and does not read the report outcome or evidence.

## Registered mutation

For each repaired record, deep-copy the record and replace the second case's representation value with the first case's representation value. Do not modify required behavior, report outcome, evidence, source domain, or any other semantic field. Recompute only `freeze.contract_sha256` so the mutation remains hash-consistent.

Precondition: the two registered cases have different required-behavior values. If this precondition fails for any domain, execution is `BLOCKED` rather than silently changing the mutation.

The mutation is material by construction under the frozen exact contract: two cases requiring different behavior become representation-indistinguishable.

## Primary endpoint

Primary paired corpus: six unmodified repaired controls (negative) plus six registered collision mutants (positive).

The bounded loss-detection claim is promoted to `PROVED` only if all of the following hold:

1. all 12 primary items remain schema-valid;
2. all six unmodified repaired controls pass A1;
3. all six mutants fail A1;
4. O1 reports no collision for all six unmodified repaired controls;
5. O1 reports a material collision for all six mutants;
6. A1's loss/no-loss classification agrees with O1 on all 12 primary items.

Any false negative or false positive refutes the registered all-items claim. Infrastructure failure that prevents classification yields `BLOCKED`. Ambiguous evidence yields `UNDERDETERMINED`.

## Secondary endpoint

For the six frozen native W4 lossy controls:

- schema validation must succeed;
- FAR semantic validation must succeed as a valid checked `REFUTED` collision record;
- O1 must independently locate a material collision.

Failure of a native positive control does not get rewritten as a W6 success; it is reported exactly and triggers review of the relevant W4 dependency.

## Disagreement endpoint

Machine implementation agreement between A1 and O1 is recorded descriptively. Human reviewer disagreement is **not tested** and remains `UNDERDETERMINED`. No model-model, tool-tool, or implementation agreement may be relabeled human agreement.

## Analysis

Report exact counts, sensitivity, specificity, false-negative count, false-positive count, and A1/O1 agreement. Because the corpus is project-authored, finite, exhaustively registered, and not a probability sample, do not use p-values, confidence intervals, or population-generalization language.

Primary sensitivity denominator: six injected mutants.

Primary specificity denominator: six unmodified repaired controls.

Secondary native-loss detection denominator: six frozen lossy records.

## Falsifiers

The bounded W6 loss-detection result is not `PROVED` if any of these occur:

- a collision mutant is rejected by schema-only validation;
- a collision mutant passes the FAR semantic audit;
- an unmodified repaired control fails the FAR semantic audit;
- O1 disagrees with the registered mutation truth;
- A1 and O1 disagree on primary loss classification;
- the W4 manifest or registered source records do not match their frozen hashes;
- the executed algorithm differs from this protocol without an explicit deviation record.

## Independence, exposure, and scope

Project FAR authors the protocol, mutation, corpus selection, implementation, and adjudication. Therefore the result is internal bounded empirical evidence only.

This workstream may establish only that the registered semantic audit detects the registered material collision on this frozen corpus. It cannot establish external effectiveness, usefulness to human reviewers, reduced disagreement, domain completeness, unbiased contract selection, superiority over alternative audit systems, population error rates, empirical benefit in deployment, novelty, or any change to deductive theorem status.

## Required outputs

Execution must produce:

- a deterministic machine-readable result record;
- an independent oracle comparison;
- mutation and negative-control tests;
- a campaign checker that fails closed on corpus or result drift;
- an exact artifact manifest;
- a deviation log, including an explicit `none` value when no deviation occurred;
- a terminal W6 status record distinguishing bounded loss detection from untested human disagreement and external utility.
