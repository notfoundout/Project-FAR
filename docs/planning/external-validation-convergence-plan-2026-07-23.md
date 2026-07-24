# External Validation Convergence Plan

Date: 2026-07-23
Status: active execution order

## Objective

Run an ordinary external SWE-agent trajectory through existing FAR product machinery without duplicating the existing release-assurance, decision-integrity, trace, report, or storage systems.

## Ordered work

### EV-C1 — Integrate the minimum reusable commercial core

Port from `research/execute-pte-w1-independent-review` onto current `main` in bounded, reviewable tranches.

Required before Candidate 001:

1. release/decision package models and deterministic loaders;
2. four-state adjudication and evidence findings;
3. reasoning regression or baseline/candidate comparison;
4. deterministic report and evidence manifest generation;
5. only the trace-normalization interfaces required by the external adapter.

Deferred until after Candidate 001:

- HTTP services;
- OIDC/JWKS;
- OTLP export;
- Kubernetes;
- distributed storage contracts;
- production backup and recovery layers;
- advanced tenant operations.

### EV-C2 — Recreate Candidate 001 on current `main`

Create a new branch from the then-current `main` and restore:

- `README.md`;
- `acquisition-chain.md`;
- `preregistration-procedure.md`;
- raw artifact manifest;
- source hashes;
- scope and nonclaim boundaries.

Candidate 001 remains nondecisive because its outcome label was exposed.

### EV-C3 — Implement the SWE-agent adapter

The adapter must:

1. read the ordinary trajectory without requiring FAR instrumentation;
2. preserve event order and raw source locations;
3. emit a generic normalized event representation;
4. map only defensible fields into existing FAR contracts;
5. attach a provenance class to every mapped field;
6. preserve missing and unverifiable states;
7. reject claims of semantic completeness.

### EV-C4 — Execute Candidate 001

Required outputs:

- raw artifact hash manifest;
- normalized trace;
- FAR package;
- claim assessment;
- evidence report;
- evidence manifest;
- deterministic rerun hashes;
- runtime metrics;
- human-effort ledger;
- unsupported-field inventory.

### EV-C5 — Execute blind Candidate 002

Before outcome access:

1. select the candidate using permitted metadata only;
2. acquire and hash task and trace inputs while isolating outcome artifacts;
3. commit `freeze.md` and `freeze.sha256`;
4. record commitments, operationalizations, alternatives, evidence requirements, scoring, Unknown conditions, and nonclaims;
5. run the same adapter and comparison pipeline;
6. compare FAR findings with benchmark-visible results.

## Acceptance gates

### Gate A — Repository convergence

Pass when the minimum commercial core runs from current `main` without dependence on the diverged research branch.

### Gate B — External compatibility

Pass when Candidate 001 produces a deterministic source-linked report without invented fields.

### Gate C — Blind incremental value

Pass only if Candidate 002 shows a preregistered, useful FAR finding not already supplied by the benchmark outcome or competent baseline tests.

A negative or Unknown result is valid and must remain recorded.

## Governing constraint

No additional product infrastructure or universality strengthening should displace EV-C1 through EV-C5.
