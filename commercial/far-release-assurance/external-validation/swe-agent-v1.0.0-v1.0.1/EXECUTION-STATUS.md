# SWE-agent External Comparison Execution Status

Authority: GitHub issue #365, the frozen files in this directory, and the newest required checks on the exact repository head under review.

## Current verified state

- The task, two SWE-agent releases, model, repetitions, agent configuration, SWE-bench harness revision, and environment image are frozen.
- The environment image is pinned by immutable GHCR digest.
- Preflight, deterministic four-run planning, one-run-at-a-time execution, outcome-blind evidence compilation, primary freeze verification, and separate outcome reveal are implemented.
- Exact configuration compatibility is exercised for SWE-agent v1.0.0 and v1.0.1 without a model call.
- The first live run reached the real model-execution path but did not produce an accepted completion. Preserved internal evidence reported `exit_error`, the prediction was empty, and provider quota exhaustion was present.
- That run must remain the active frozen slot as `failed_retryable`; it must not be treated as complete or allow the matrix to advance.
- No four-run execution matrix, primary comparison freeze, outcome reveal, or bounded external case report is complete.

## Required next execution behavior

1. Restore the newest execution artifact for this case.
2. Revalidate every run marked `complete` against its preserved outer return code, internal status file, target-instance prediction, and patch content.
3. Write an auditable correction artifact when preserved evidence disproves completion.
4. Block progression on any terminal failure.
5. Archive prior-attempt artifacts before retrying a retryable slot so stale status or prediction files cannot contaminate the new attempt.
6. Execute at most one frozen slot per confirmed workflow dispatch.
7. Preserve the outcome-blind boundary until the primary comparison has been hash-frozen and independently verified.

## Non-negotiable gates

- No benchmark outcome may be accessed before the primary comparison freeze verifies.
- No model, task, release, environment digest, configuration, repetition count, or run ordering may be substituted.
- No execution or repository repair may merge unless the newest run of every required check on the exact final head is successful.
- Older successful runs do not override newer failures, cancellations, timeouts, or pending checks.
- No direct commit to `main`; changes in this scope pass through a pull request.
- A single external case cannot support a general superiority, independent-validation, commercial-readiness, or enterprise-readiness claim.

## Completion condition

This case remains incomplete until all four internally validated runs exist, the outcome-blind evidence packages and primary comparison are frozen and independently verified, outcomes are revealed only afterward, and the bounded case report is published without generalization.
