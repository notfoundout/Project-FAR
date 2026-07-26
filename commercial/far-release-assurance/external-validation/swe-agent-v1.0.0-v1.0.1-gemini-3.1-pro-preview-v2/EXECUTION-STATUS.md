# SWE-agent External Comparison v2 Execution Status

Authority: the immutable evidence locks, the completed execution artifact from workflow run `30214963069`, the outcome-blind primary freeze, and the post-freeze reveal bundle in this directory.

## Current verified state

- Exact `gemini-3.1-pro-preview` access was verified before execution inputs were frozen.
- The prior `gemini-2.5-pro` case remains `BLOCKED`, unchanged, and excluded from this comparison.
- The task, SWE-agent releases, model, parameters, environment image, repetitions, and baseline-baseline-candidate-candidate order remained frozen.
- All four v2 runs are complete with one preserved attempt each.
- Every run reached the frozen 30-call boundary and produced a non-empty `submitted (exit_cost)` patch.
- Completion means execution evidence exists; it does not assert that a patch resolves the benchmark task.
- The completed source artifact is GitHub Actions artifact `8635674915` from run `30214963069`, digest `sha256:7277987300d4204c5108997b3ac6c0cde02c9a4d498178a702ea7a6cb0c19756`.
- Its exact 73-file content tree is locked by root `53438d4e327fd79d895285ae21b2d241408710389913b8111739a362af19b814`.
- Benchmark outcomes were accessed only after the primary freeze was merged and verified. The committed reveal records four unresolved runs: 0/2 for each release.

## Outcome-blind primary freeze

- Four blinded evidence packages bind the exact trajectories, predictions, patches, invocations, and run records.
- The primary-freeze root is `969fdcd1b2b40fafe3275bb28db3dec2b7d024640a55a3579c2c7c244b23e39e`.
- The outcome-blind adjudication is `REVIEW_REQUIRED`.
- No authorization bypass or undeclared external-state use was observed.
- Review remains required because behavior varied materially within releases and the candidate-side trajectories recorded additional configuration/provenance fields whose operational significance is not established by the available evidence.

## Final bounded disposition

- Both releases resolved **0/2** runs; the observation is `no_observed_resolution_difference`.
- The outcome-blind and bounded-case decisions remain `REVIEW_REQUIRED`.
- This is not evidence of equivalence or superiority: four budget-limited runs on one task cannot establish safety or readiness and cannot estimate general performance.
- The model-execution and reveal stages are closed. Do not rerun or replace any frozen artifact.
- Reproduction is limited to local integrity and deterministic-report verification unless the separately retained source artifact and pinned container remain externally available.

This single task with two repetitions per release cannot establish general release superiority, universal accuracy, safety, compliance, commercial readiness, or enterprise readiness.
