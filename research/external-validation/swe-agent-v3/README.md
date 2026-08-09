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

This package freezes the causal question, arm structure, estimands, outcome contract, evidence requirements, capsule constraints, exact bootstrap procedure and bootstrap seed, task-manifest and sealed-identity-ledger contracts, required task strata, repository-prohibition contract, critical-harm threshold contract, failure/arithmetic contract, and fail-closed execution gate. It does not select the confirmatory tasks, instantiate the sealed identity ledger, choose a model endpoint, build the FAR capsule, build the placebo, set the final run budget, freeze assignment/counterbalancing randomization, or authorize a pilot or confirmatory run.

All model calls and benchmark execution are currently blocked. A sacrificial pilot may only be separately authorized after every pre-pilot gate in `execution-gate-v1.0.json` is true, including `critical_harm_thresholds_frozen_and_verified`; confirmatory execution additionally requires the completed-and-excluded pilot gate and every remaining confirmatory gate. No such authorization currently exists.

The bootstrap seed is already prospectively frozen by `bootstrap-seed-commitment-contract-v1.0.json`. It is a direct committed value and does not depend on mutable capsule, task-manifest, sealed-identity-ledger, or execution-gate identities. This is distinct from the still-unfrozen assignment/counterbalancing randomization seed.

The future frozen task manifest contains blinded task/repository labels, a unique task-bundle root, and prospective strata. A separate sealed identity ledger governed by `task-manifest-contract-v1.0.json` must bind every manifest position one-to-one to the authoritative GitHub repository ID, canonical audit URL, exact repository commit, task-payload digest/byte count, matching strata, GitHub fork-source repository ID or null, and treatment-material audit result. Before any pilot or confirmatory execution, an independent identity auditor must recompute every task root; enforce the minimum 24 tasks, at least five provider-stable repositories, and the 20% per-repository cap; enforce one canonical URL and one blind repository ID per authoritative provider/ID pair; reject repository ID `1283452680` (`notfoundout/Project-FAR`); reject any GitHub fork whose `source.id` is `1283452680`; reject any candidate commit whose retained audit finds Project FAR treatment material; and verify coverage of all five required strata. The exact task-manifest and sealed-ledger bytes and Git blob identities plus the repository-prohibition audit report root must be committed before execution. The ledger remains sealed from the executing agent and capsule authors.

`critical-harm-thresholds-v1.0.json` prospectively fixes zero-tolerance harm rules plus exact rational FAR-minus-placebo regression-introduction and invalid-run rate thresholds. The zero-tolerance rules use explicit frozen-slot numerators and denominators and cannot be waived by dilution. Regression introduction is determined from the same frozen regression tests passing in the pristine control and failing against the submitted workspace; no causal-attribution override, operator waiver, or post-hoc exclusion is permitted.

`failure-arithmetic-amendment-v1.1.json` is now a standalone current prospective contract for replacement/terminal-reason classification and exact arithmetic. Its validity does not depend on historical snapshot provenance. `historical-authority-v1.0.json` preserves archival context only, explicitly does not self-prove that its snapshots occurred at its claimed historical commit, and is not part of the live authority chain.

A true gate alone can never authorize a run. Every pilot or confirmatory launch also requires a separately committed prospective launch record containing every identity in `launch_record_required_bindings`, including the frozen design commit/manifest, task manifest, sealed identity ledger, repository-prohibition audit report root, seed commitment, harm contract, treatment/placebo roots, model, prompts/configuration, environment/dependencies, budgets/stopping rules, assignment seed, grader, evidence-store configuration, protection reference, and manual authorization record.

## Integrity model

The reviewed Git commit/tree is the immutable current-byte authority. Every governed current design artifact plus archival context is indexed exactly once by `design-manifest-v1.0.json`, whose entries contain only governed paths. The manifest does not duplicate current blob identities, byte counts, hashes, or semantic digests; semantic verifiers enforce complete type-exact contract invariants while current bytes are bound solely by the reviewed Git tree. Verifier source is deliberately excluded from the governed-artifact manifest to avoid recursive self-hashing and remains ordinary reviewed code at the exact PR head.

The archival snapshot record is intentionally weaker than live authority: it proves only that the current archive bytes match the archive record’s blob IDs. Establishing that those bytes existed at a claimed historical Git commit requires independent external Git/history provenance. Current experiment validity does not depend on that proof.

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
