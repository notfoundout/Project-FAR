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

This package freezes only the causal question, arm structure, estimands, outcome contract, evidence requirements, capsule constraints, prospective corrections, and fail-closed execution gates. It does not authorize a model call, pilot, benchmark run, confirmatory run, grading, outcome reveal, release, or accepted-theory change.

`failure-arithmetic-amendment-v1.1.json` controls its two registered subjects. `review-closure-amendment-v1.2.json` prospectively controls only the bootstrap-seed authority correction, stratum-auditable task-manifest extension, critical-harm thresholds and launch prerequisites, and shallow-checkout historical-authority consumption described in `AMENDMENT-v1.2.md`. The original historical authority bytes are preserved under `historical-base-83c951/` and are manifest-rooted immutable snapshots, not new evidence.

The frozen bootstrap seed remains bound to its originally committed derivation-input identities; later launch-preparation changes cannot rewrite it. Future instantiated confirmatory task manifests must record one of the five preregistered strata per task and prove all required strata are represented before execution. Critical-harm thresholds are prospectively fixed and fail closed on missing required harm evidence.

All model calls and benchmark execution are currently blocked. A sacrificial pilot may only be separately authorized after every pre-pilot gate and every v1.2 pilot prerequisite are true; confirmatory execution additionally requires the completed-and-excluded pilot gate, frozen required-strata coverage, harm-evidence retention, and every remaining confirmatory gate. No such authorization currently exists.

## Integrity model

Every governed data, narrative, prospective-amendment, seed-commitment, and immutable historical-authority snapshot artifact is exact-locked in `design-manifest-v1.0.json`. The verifier checks each committed Git blob and the corresponding worktree bytes, then evaluates the critical semantic contracts. Verifier source is deliberately excluded from the governed-artifact manifest to avoid recursive self-hashing; it remains ordinary reviewed code at the exact PR head.

The historical snapshots make primary verification self-contained in a depth-1 checkout. The required verification path does not depend on fetching historical Git objects or proving an unrelated ancestry relation.

## Verification

```bash
python research/external-validation/swe-agent-v3/verify_design.py
python research/external-validation/swe-agent-v3/verify_review_closure_v1_2.py
python -m unittest discover -s tests -p 'test_swe_agent_v3*.py' -v
python -m py_compile \
  research/external-validation/swe-agent-v3/verify_integrity.py \
  research/external-validation/swe-agent-v3/verify_design.py \
  research/external-validation/swe-agent-v3/verify_review_closure.py \
  research/external-validation/swe-agent-v3/verify_review_closure_v1_2.py \
  tests/test_swe_agent_v3*.py
```
