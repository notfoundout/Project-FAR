# SWE-agent v3 FAR augmentation study

Status: **Research — design only**  
Program ID: `FAR-SWE-V3-001`  
Execution authorized: **No**

This directory registers a new causal experiment. It does not repair, continue, or pool the historical SWE-agent v2 comparison.

The experiment asks whether a frozen Project FAR treatment capsule improves software-engineering task performance when the model, task, repository, tools, environment, budgets, and evaluation are otherwise identical. The confirmatory design uses three mandatory arms:

1. `baseline`: the ordinary agent configuration;
2. `placebo`: an inert capsule matched to the FAR capsule for size, structure, read order, and interaction burden;
3. `far`: the frozen FAR treatment capsule.

Project FAR itself is prohibited as a benchmark task repository. Confirmatory tasks must be external and source-identity sealed before execution. The treatment capsule must not contain task identities, repository-specific facts, gold patches, hidden tests, outcomes, or extra model/tool access.

The historical v2 result remains immutable and separate: one task, two repetitions per SWE-agent release, four budget-limited failures, and no observed resolution difference. Its runs are not prior observations for v3 and may not be pooled.

## Current boundary

This package freezes the causal question, arm structure, estimands, outcome contract, evidence requirements, capsule constraints, exact bootstrap procedure and bootstrap seed, task-manifest schema including required strata, critical-harm threshold contract, and fail-closed execution gate. It does not select the confirmatory tasks, choose a model endpoint, build the FAR capsule, build the placebo, set the final run budget, freeze assignment/counterbalancing randomization, or authorize a pilot or confirmatory run.

All model calls and benchmark execution are currently blocked. A sacrificial pilot may only be separately authorized after every pre-pilot gate in `execution-gate-v1.0.json` is true, including `critical_harm_thresholds_frozen_and_verified`; confirmatory execution additionally requires the completed-and-excluded pilot gate and every remaining confirmatory gate. No such authorization currently exists.

The bootstrap seed is already prospectively frozen by `bootstrap-seed-commitment-contract-v1.0.json`. It is a direct committed value and does not depend on mutable capsule, task, or execution-gate identities. This is distinct from the still-unfrozen assignment/counterbalancing randomization seed.

`historical-authority-v1.0.json` roots the two exact historical snapshots needed to interpret the v1.1 failure/arithmetic amendment. Those snapshots are immutable historical evidence, not current design authority, and verification does not require repository history beyond the reviewed checkout.

## Integrity model

The reviewed Git commit/tree is the immutable current root. Every governed current design artifact plus the self-contained historical authority is indexed exactly once by `design-manifest-v1.0.json`. The manifest records committed Git blob identity and byte count; semantic verifiers enforce contract invariants without copying mutable current blob IDs into verifier constants. Verifier source is deliberately excluded from the governed-artifact manifest to avoid recursive self-hashing and remains ordinary reviewed code at the exact PR head.

## Verification

```bash
python research/external-validation/swe-agent-v3/verify_design.py
python research/external-validation/swe-agent-v3/verify_amendment_v1_1.py
python research/external-validation/swe-agent-v3/verify_review_closure.py
python -m unittest discover -s tests -p 'test_swe_agent_v3*.py' -v
python -m py_compile \
  research/external-validation/swe-agent-v3/verify_integrity.py \
  research/external-validation/swe-agent-v3/verify_design.py \
  research/external-validation/swe-agent-v3/verify_review_closure.py \
  research/external-validation/swe-agent-v3/verify_amendment_v1_1.py \
  tests/test_swe_agent_v3*.py
```
