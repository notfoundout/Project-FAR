# Project FAR Repository Convergence Audit

Date: 2026-07-23
Status: execution baseline

## Decision

Project FAR does not need a wholesale repository rewrite before external validation. It needs a bounded convergence pass that establishes one authoritative map, resolves branch divergence, and reuses existing product machinery.

The next product milestone is not a new evidence engine. It is an external correspondence adapter that converts an ordinary SWE-agent trajectory into the existing FAR decision, regression, manifest, and report contracts without inventing unavailable information.

## Verified repository state

- `main` is the canonical default branch.
- The documented remote branch `validation/trace-candidate-001` is not currently present.
- `research/execute-pte-w1-independent-review` and `main` have diverged.
- The research branch is 70 commits ahead of the merge base and 79 commits behind current `main`.
- The research branch contains two substantial commercial packages absent from current `main`:
  - `commercial/far-release-assurance/`
  - `commercial/far-decision-integrity/`
- It also contains CI, deployment, evidence-store, trace-ingestion, instrumentation, authorization, security, operations, OIDC, OTLP, and distributed-runtime work.

## Architectural diagnosis

The repository has an integration problem, not a blank-slate capability problem.

The commercial branch already contains most of the internal pipeline:

1. disclosed package ingestion;
2. deterministic normalization and hashing;
3. claim and dependency adjudication;
4. baseline-versus-candidate comparison;
5. reasoning regression;
6. trace ingestion for FAR-instrumented telemetry;
7. deterministic reports and evidence manifests;
8. evidence persistence and service infrastructure.

The missing boundary is ordinary external telemetry. Current trace ingestion expects producers to emit FAR semantic-convention attributes. SWE-agent trajectories do not satisfy that contract by default.

## Required convergence sequence

### C1 — Preserve framework boundaries

Do not merge or rename FAR, FARA, FARE, FARM, and FARO into product names.

- FAR: investigation methodology.
- FARA: representational architecture.
- FARE: formal and mathematical evaluation support.
- FARM: cross-framework coordination and change control.
- FARO: operationalization.

These are stable framework roles. Product packages should implement or consume them, not replace them.

### C2 — Make `main` authoritative

Do not merge the diverged 70-commit research branch wholesale.

Create a clean commercial convergence series from current `main`:

1. identify commercial-only commits and files;
2. replay or port them in dependency order;
3. exclude stale research-branch mutations;
4. run the current `main` health suite after each bounded tranche;
5. retain explicit claim boundaries from the original commercial work.

Recommended tranche order:

1. FAR Release Assurance core;
2. FAR Decision Integrity core;
3. external trace ingestion and instrumentation;
4. reports and evidence manifests;
5. persistence and service layer;
6. security and operational infrastructure;
7. distributed contracts last.

### C3 — Restore external-validation work on a clean branch

Recreate external validation from current `main` only after the minimum reusable commercial core is integrated.

The branch should contain:

- acquisition-chain records;
- raw artifact hashes;
- candidate-specific freeze artifacts;
- a SWE-agent adapter;
- provenance classification;
- a reproducible report bundle;
- measured runtime and human effort.

### C4 — Build only the missing adapter

Target pipeline:

```text
ordinary SWE-agent trajectory
  -> source adapter
  -> provenance-aware normalized events
  -> existing FAR decision/release package
  -> existing adjudication/regression machinery
  -> existing report and manifest
```

The adapter must classify every mapped field as one of:

- observed;
- mechanically derived;
- human-declared;
- inferred;
- contradicted;
- missing;
- unverifiable.

Absence from a trace must not be interpreted as non-occurrence unless trace completeness is independently established.

## Non-actions

Do not perform these before the external trace run:

- another general graph model;
- another evidence-status vocabulary;
- another report format;
- more distributed infrastructure;
- mass file moves for cosmetic cleanliness;
- speculative changes to FAR, FARA, FARE, FARM, or FARO;
- direct expansion of `far-ir/1.0` without a demonstrated external requirement.

## Exit criteria

Repository convergence is complete when:

1. `main` contains the minimum commercial core required for external validation;
2. every active package has an owner layer and canonical path;
3. the old framework roles remain explicit;
4. no validation work depends on the diverged research branch;
5. one command can transform Candidate 001 into a deterministic source-linked evidence report;
6. Candidate 002 can be frozen and executed blindly.
