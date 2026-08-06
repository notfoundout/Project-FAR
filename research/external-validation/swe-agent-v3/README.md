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

This package freezes only the causal question, arm structure, estimands, outcome contract, evidence requirements, capsule constraints, and fail-closed execution gate. It does not select tasks, choose a model, build the FAR capsule, build the placebo, set the final run budget, generate randomization, or authorize a pilot or confirmatory run.

All model calls and benchmark execution remain blocked until every gate in `execution-gate-v1.0.json` is satisfied and separately authorized after the theory version is frozen.

## Verification

```bash
python research/external-validation/swe-agent-v3/verify_design.py
python -m unittest tests.test_swe_agent_v3_design -v
```
