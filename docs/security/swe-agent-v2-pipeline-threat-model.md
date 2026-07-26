# Frozen SWE-agent v2 Pipeline Threat Model

Status: **Accepted audit model; historical controls and residual risks**

## Assets and trust boundaries

Assets are preregistered inputs, provider-access attestation, execution outputs, predictions/patches, primary freeze, outcome reveal and final report. Trust boundaries include Git/GitHub, hosted runners, external package and source hosts, GHCR, the model provider, artifact storage and the SWE-bench harness.

| Threat | Existing or new control | Residual risk / disposition |
|---|---|---|
| Post-freeze mutation | SHA-256 file/tree locks, sidecar verification, completed-case workflow guard | Git history and review remain trust roots. |
| Outcome leakage | Redacted task record, forbidden-key scan, blind primary adjudication | Build infrastructure accessed outcome-bearing inputs; non-export is attested, not independently observed. |
| Mutable dependencies | Image digest and source commits are pinned | Action major tags, runner image and package acquisition were not fully content-addressed; historical limitation. |
| Circular hashing | Roots derive from canonical ordered entries and files are rehashed | Hashes prove identity, not truth or external origin. |
| Artifact/repository divergence | Source lock plus independent download/tree comparison | External artifact retention is not guaranteed. |
| Silent skip | Reveal verification now requires the reveal; stages use explicit conditions | GitHub expression semantics and platform availability remain external. |
| Outer success/internal failure | Exit 75 now propagates; artifact upload remains `always()` | Historical run conclusions still require record inspection. |
| Empty/malformed prediction | Materializer requires JSON, task identity, nonblank string, and exact patch equality | Semantic patch quality is decided only by the harness. |
| Failure misclassification | Controller distinguishes retryable/provider/quota states from completion | Provider and harness classifications depend on observable logs and may be incomplete. |
| Non-independent runs | Isolated workspaces and fixed sequential order | Shared provider/controller/time and only two repetitions prevent independence claims. |
| Race or rerun | Workflow concurrency and completed-bundle guard | Repository administrators can alter protections; historical artifact selection used “latest” before final locking. |
| Report drift | Exact deterministic JSON/Markdown comparison and bundle hashes | Timestamps prevent byte-identical regeneration without retaining the frozen reveal/report times; verification, not rewrite, is authoritative. |

## Failure policy

Missing artifacts, malformed JSON, unexpected membership, hash mismatch, absent outcomes, null/empty patches, internal nonzero status, or an unknown decision input must fail closed. Infrastructure/provider/quota failures are not benchmark task failures. `UNKNOWN`, `BLOCKED`, and `REVIEW_REQUIRED` must remain distinct.
