# PCA-W6 Execution and Results

Status: **ACCEPTED BOUNDED INTERNAL CONTROL RESULT**

Protocol freeze: `3813b9e3eb49562bd8b9f4d3179c3d9536831de6`

Protocol base: `main@2cecf2e21cc27208f606dcd38337af4369e66af2`

## Execution

The frozen protocol was executed against the six repaired W4 finite-explicit contracts and their six paired lossy W4 controls. For each repaired record, the registered mutation replaced the second case's representation value with the first case's representation value while preserving the distinct required behavior and recomputing only the frozen contract hash.

The first CI execution exposed implementation defects in the W6 test harness before any result was accepted: Python boolean literals had been written with JSON spelling, and an independence test inspected its own explanatory docstring. Those defects were corrected without changing the frozen corpus, mutation, endpoint, baseline, oracle, success criteria, or interpretation boundaries.

The next controlled test execution passed all six W6 tests. It recomputed the recorded deterministic result exactly and confirmed the registered mutation remained JSON-Schema-valid while producing `FACTORIZATION_FAILURE` under the FAR semantic audit. A subsequent standalone-checker invocation exposed a repository-path import defect (`jsonschema` unavailable when the script was executed directly); the checker was corrected to place the repository root on `sys.path` before loading the vendored validator. This was an execution-harness repair only and did not alter the frozen experiment.

These implementation corrections are recorded here as execution history. The machine result's `deviations` field remains empty because no preregistered scientific condition, endpoint, corpus, mutation, or analysis rule changed.

The final repository-wide merge-gate audit found two additional assurance defects after the scientific result had stabilized: the terminal CRE-001 regression had not been rebound in the W4 supporting-artifact manifest, and the expanded W6 exact-artifact set had not been regenerated into the W6 manifest. The same audit found incomplete propagation into the canonical map and current claim, proof-status, limitation, and open-problem registers, plus a temporary branch-mutating remediation workflow. Finalization refreshed the governed hashes, expanded W6 coverage to every changed evidence/dependency/propagation surface, completed those indexes, removed the temporary workflow, and added a regression rejecting its return. None of these assurance repairs changed the frozen W4 records, W6 corpus, mutation, endpoints, algorithm, result record, or claim boundary.

## Primary result

Primary corpus: six clean repaired negative controls plus six injected material-collision mutants.

| Condition | True positives | False negatives | True negatives | False positives | Sensitivity | Specificity |
|---|---:|---:|---:|---:|---:|---:|
| Schema-only baseline | 0 | 6 | 6 | 0 | 0/6 | 6/6 |
| FAR semantic audit | 6 | 0 | 6 | 0 | 6/6 | 6/6 |

All twelve primary records remained schema-valid. All six unmodified repaired controls passed the FAR semantic audit. All six registered mutants failed the FAR semantic audit with `FACTORIZATION_FAILURE`. The independent table-only collision oracle classified all six clean controls as no material collision and all six mutants as material collisions. FAR audit/oracle agreement was `12/12`.

Registered primary all-items claim: **PROVED at this frozen finite controlled-artifact scope.**

## Secondary positive controls

All six frozen W4 native lossy records remained schema-valid, were accepted by the FAR semantic verifier as valid checked `REFUTED` collision records, and were independently identified by the table-only oracle as material collisions.

Native lossy controls detected: `6/6`.

Registered secondary control claim: **PROVED.**

## Observation

A syntactic shape check alone did not detect any of the registered semantic collisions. The explicit semantic audit did detect every registered collision without flagging any clean repaired control in this corpus. The result demonstrates that the semantic constraints exercised here add detection power over schema-only shape validation for this exact defect class and corpus.

This is not evidence that every FAR audit detects every material loss. The mutation directly targets the finite factorization condition that the semantic verifier was built to check.

## Discovery

The bounded operational result supports a narrower statement than the broad wording sometimes associated with “audit utility”:

> For the six frozen two-case W4 repaired controls, the registered FAR finite-explicit semantic audit detects the preregistered representation-collision mutation while schema-only validation does not, with no false positives on the six clean controls.

Nothing in this execution identifies a human cognitive mechanism or establishes that reviewers disagree less when using FAR.

## Replication and acceptance

Replication is internal but implementation-diverse at the collision predicate: the FAR verifier and the independent oracle use separate code paths, and the oracle does not call the verifier or inspect report/evidence labels. The frozen native W4 lossy controls provide an additional positive-control replication set.

This does **not** constitute external independent replication. Project FAR selected the corpus, designed the mutation, implemented both machine lanes, and adjudicated the result.

## Terminal disposition

- bounded registered material-loss detection: `PROVED`
- human disagreement reduction: `UNDERDETERMINED`
- external real-world audit utility: `OPEN`
- impact on `PROJECT-FAR-CORE-THEORY-1.1`: `NONE`

PCA-W6 is complete at its registered bounded internal controlled-artifact deliverable. External effectiveness and human-review utility remain downstream empirical obligations and must not be inferred from this result.
