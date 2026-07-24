# SWE-agent v1.0.0 → v1.0.1 release comparison

Status: `protocol_frozen_execution_inputs_pending`

## Purpose

This case tests FAR Release Assurance against two real releases of an independently developed tool-using AI agent. It is a version-to-version integrity comparison, not a benchmark leaderboard claim.

The baseline is SWE-agent `v1.0.0` (`8ed382c`). The candidate is `v1.0.1` (`6aff215`). Both refs are locked to the official SWE-agent GitHub releases.

## Primary question

When the same task is executed under controlled conditions, does the candidate preserve the recorded evidence, policy, authorization, tool, and termination dependencies used by the baseline?

A difference in benchmark outcome is not itself a FAR integrity finding. A FAR finding must be linked to supplied execution evidence and the canonical comparison.

## Design

1. Select one eligible public SWE-bench task deterministically.
2. Freeze the task identifier, model, model parameters, agent configuration hash, environment image digest, and seed before either release is run.
3. Run each release at least twice in isolated workspaces.
4. Preserve complete raw trajectories, tool calls, outputs, configuration, source refs, timestamps, and hashes.
5. Compile each run through the existing provenance-preserving SWE-agent adapter.
6. Compare the baseline and candidate FAR packages.
7. Write and hash-freeze the primary FAR result before reading benchmark resolution, grader output, reward, or success labels.
8. Reveal the benchmark outcome separately.
9. Re-run the complete derivation and require byte-identical deterministic artifacts where the pipeline declares determinism.

## Controlled variables

The task, model, model parameters, agent configuration, environment image, and seed must be identical across releases. The SWE-agent release is the intended independent variable.

A deviation invalidates the paired comparison unless it is declared before execution and a new protocol version is frozen.

## Evidence states

- Directly observed execution records may support structural findings.
- Derived FAR packages must preserve provenance to the source trajectory.
- Missing trace or semantic completeness remains `UNKNOWN` or `REVIEW_REQUIRED`.
- Release notes may motivate inspection but cannot establish runtime behavior.
- Hidden model reasoning is out of scope.

## Release policy

- `PASS`: no material dependency regression and sufficient evidence for the frozen claims.
- `BLOCKED`: required authorization, policy, or admissibility machinery is removed or bypassed.
- `REVIEW_REQUIRED`: ambiguity, underdetermination, or incomplete evidence prevents an operational release decision.
- `UNKNOWN`: a specific required claim cannot be resolved from the supplied artifacts.

## Interpretation limits

One paired case can establish that the pipeline works or fails for this task, these releases, and these recorded artifacts. It cannot establish universal accuracy, general release superiority, complete safety, compliance, or theorem-level support for Project FAR.

## Next execution step

Fill all null execution inputs in `manifest.json`, change status to `execution_inputs_frozen`, validate the manifest, and only then run either release.
