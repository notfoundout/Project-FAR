# SWE-agent External Comparison Execution Status

Authority: GitHub issue #365 and the frozen files in this directory.

## Current verified state

- The task, two SWE-agent releases, model, repetitions, agent configuration, SWE-bench harness revision, and environment image are frozen.
- The environment image is pinned by immutable GHCR digest.
- Preflight and deterministic four-run planning are implemented.
- A sequential, resume-safe execution controller is implemented.
- Exact configuration compatibility is verified for SWE-agent v1.0.0 and v1.0.1 without a model call.
- The case-specific regression suite, both repository-health workflows, SWE-agent smoke matrix, formal validation, specification export, Lean mechanization, unified validation shadow, and validator assurance were green before this branch was created.

## Active PR scope

This branch completes the remaining executable case boundary:

1. verify the live `execute` workflow restores and validates state without advancing the wrong run;
2. ensure one dispatch can execute no more than one frozen run;
3. preserve raw trajectories, process output, invocation metadata, state transitions, and file hashes;
4. add outcome-blind FAR package compilation contracts;
5. add blinded comparison and primary-freeze contracts;
6. add a separate post-freeze outcome-reveal boundary;
7. add reproducibility and failure-preservation documentation.

## Non-negotiable gates

- No benchmark outcome may be accessed before the primary comparison freeze verifies.
- No model, task, release, environment digest, configuration, repetition count, or run ordering may be substituted.
- No execution change may merge with a failing required check.
- No direct commit to `main`; all changes in this scope must pass through this PR.
- A single external case cannot support a general superiority, independent validation, commercial-readiness, or enterprise-readiness claim.

## Merge condition

This branch is mergeable only after every required PR check is green and the diff demonstrates that the execution, evidence compilation, freeze, and reveal boundaries fail closed under mutation and interrupted-run tests.
