# SWE-agent External Comparison Execution Status

Authority: GitHub issue #365, the frozen files in this directory, preserved execution artifacts, and the newest required checks on the exact repository head under review.

## Current verified state

- The task, two SWE-agent releases, model, repetitions, agent configuration, SWE-bench harness revision, and environment image are frozen.
- The environment image is pinned by immutable GHCR digest.
- Preflight, deterministic four-run planning, one-run-at-a-time execution, outcome-blind evidence compilation, primary freeze verification, and separate outcome reveal are implemented.
- Exact configuration compatibility is exercised for SWE-agent v1.0.0 and v1.0.1 without a model call.
- `v1.0.0-r1` has three preserved attempts and no accepted completion.
- Attempts 1 and 2 reached the provider but returned quota exhaustion with an empty prediction.
- Attempt 3 used the replacement credential and returned HTTP 404 `NOT_FOUND`: `gemini-2.5-pro` was reported as unavailable to new users. It produced no patch.
- Attempt 3 was initially recorded as `failed_retryable` because the legacy classifier matched the benign configuration field `startup_timeout` as if it were a provider timeout. Preserved evidence requires `provider_model_unavailable` / `failed_terminal` instead.
- `v1.0.0-r2`, `v1.0.1-r1`, and `v1.0.1-r2` remain untouched and pending.
- No four-run execution matrix, primary comparison freeze, outcome reveal, or bounded external case report is complete.

## Required next behavior

1. Restore the newest execution artifact for this case.
2. Reclassify attempt 3 from `retryable_provider_error` to terminal `provider_model_unavailable` while preserving every prior attempt and correction record.
3. Do not rerun the same credential. The provider explicitly rejected the frozen model for that API project.
4. Do not advance to a later frozen slot.
5. Resume the existing frozen case only through an auditable correction that proves an API project can access the exact frozen model before another attempt is authorized.
6. If exact-model access cannot be obtained, preserve this case as blocked and create a new preregistered case version with a currently available replacement model. Do not silently substitute a model inside this frozen case.
7. Preserve the outcome-blind boundary until a complete primary comparison has been hash-frozen and independently verified.

## Non-negotiable gates

- No benchmark outcome may be accessed before the primary comparison freeze verifies.
- No model, task, release, environment digest, configuration, repetition count, or run ordering may be substituted inside this frozen case.
- No execution or repository repair may merge unless the newest run of every required check on the exact final head is successful.
- Older successful runs do not override newer failures, cancellations, timeouts, or pending checks.
- No direct commit to `main`; changes in this scope pass through a pull request.
- A single external case cannot support a general superiority, independent-validation, commercial-readiness, or enterprise-readiness claim.

## Completion condition

This case remains incomplete until all four internally validated runs exist, the outcome-blind evidence packages and primary comparison are frozen and independently verified, outcomes are revealed only afterward, and the bounded case report is published without generalization.
