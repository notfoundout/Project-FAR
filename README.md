# Project FAR

[![Release](https://img.shields.io/github/v/release/notfoundout/Project-FAR?include_prereleases&label=release)](https://github.com/notfoundout/Project-FAR/releases/tag/v0.4.0)
[![Verify Theory](https://github.com/notfoundout/Project-FAR/actions/workflows/repo-health.yml/badge.svg)](https://github.com/notfoundout/Project-FAR/actions/workflows/repo-health.yml)

Project FAR is a foundational framework for representing, analyzing, and comparing structured, explicit, and auditable reasoning.

This root README is the canonical command center for repository status, health, evidence, planning, and navigation.

## Central Research Program

Project FAR's primary objective is to determine whether every reasoning process necessarily instantiates a common underlying structure and, if so, whether that structure is universal and minimal.

The project does not assume that a universal structure exists or that FAR is that structure.

**[Read the Central Research Program](docs/governance/central-research-program.md)**

## Current Research State

The project is deduction-first. [`THM-TARGET-001`](docs/research/thm-target-001-v1.0.md), premise ledger v1.4, [`FAITHFUL-REP-001`](docs/research/faithful-representation-specification-v1.0.md), [`P8-ROLE-001`](docs/research/p8-theorem-role-decision-v1.0.md), and [`SCORE-LEMMA-LEDGER-001`](docs/research/s-core-construction-obstruction-ledger-v1.0.md) remain frozen.

[`SCORE-W0-PROOF-001`](docs/research/s-core-w0-normalization-proof-v1.0.md) and [`SCORE-W1-PROOF-001`](docs/research/s-core-w1-direct-axis-proof-v1.0.md) establish 11 construction lemmas, one source boundary, and two refuted direct-axis obstruction hypotheses. Twenty-three obligations remain. W2 dynamics, history, revision, and self-modification are active.

W1 proves finite direct-axis strong embeddings. It does not prove target-only recovery, complete `Pres_i` predicates, `Faithful_split`, a representation theorem, universality, necessity, or minimality.

Run `make research-check` to validate the theorem target, semantics, P8 split, lemma ledger, W0/W1 proof packages, executable corroboration, gates, and conservative claim boundaries.

<!-- BEGIN GENERATED PROJECT FAR DASHBOARD -->

## Repository Status

- Current release: [docs/releases/project-far-v0.4.0.md](docs/releases/project-far-v0.4.0.md)
- Current project phase: S_core W2 dynamics history revision and self-modification
- Repository health status: PASS ([health checks](docs/maintenance/repository-health-checks.md))
- Planner status: CURRENT ([planner](tools/self_advancement_plan.py))
- Last dashboard generation time: 2026-07-16T08:17:16+00:00

## Repository Alerts

| Alert | Status | Source |
|---|---:|---|
| Critical Issues | 0 | [docs/reports/research-gap-report.md](docs/reports/research-gap-report.md) |
| High Priority Issues | 1 | [docs/reports/research-gap-report.md](docs/reports/research-gap-report.md) |
| Repository Health | PASS | [docs/maintenance/repository-health-checks.md](docs/maintenance/repository-health-checks.md) |
| Planner Status | CURRENT | [docs/planning/next-actions.md](docs/planning/next-actions.md) |
| CI Status | Push, pull-request, and manual workflows available | [.github/workflows/repository-health.yml](.github/workflows/repository-health.yml) |
| Release Readiness | AVAILABLE | [docs/reports/release-readiness-report.md](docs/reports/release-readiness-report.md) |

## Evidence Snapshot

| Metric | Current | Source |
|---|---:|---|
| Internal reasoning systems | 23 | [theory/evaluation/evidence-registry.yaml](theory/evaluation/evidence-registry.yaml) |
| External reasoning systems | 29 | [theory/evaluation/external-validation-registry.yaml](theory/evaluation/external-validation-registry.yaml) |
| Adversarial fixtures | 14 | [theory/falsification/adversarial-test-suite.yaml](theory/falsification/adversarial-test-suite.yaml) |
| Counterexample fixtures | 1 | [tests](tests) |
| Candidate primitive failures | 0 | [theory/falsification/primitive-pressure-registry.yaml](theory/falsification/primitive-pressure-registry.yaml) |
| Conservative extensions | 35 | [theory/falsification/primitive-pressure-registry.yaml](theory/falsification/primitive-pressure-registry.yaml) |
| Fits FAR | 14 | [theory/evaluation/evidence-registry.yaml](theory/evaluation/evidence-registry.yaml) |
| Unresolved cases | 17 | [docs/reports/project-status-generated.md](docs/reports/project-status-generated.md) |

## Progress Summary

| Formal metric | Current |
|---|---:|
| Registered obligations | 37 |
| Proved construction lemmas | 11 |
| Source boundaries established | 1 |
| Obstruction hypotheses refuted | 2 |
| Open obligations | 23 |
| Completed waves | W0, W1 |
| Active wave | W2 |

## Top Priority Tasks

### STRATEGIC-001: Prove the W2 S_core dynamics history and revision package
- Source: deduction-first strategic priority
- Affected files:
  - [docs/research/s-core-construction-obstruction-ledger-v1.0.md](docs/research/s-core-construction-obstruction-ledger-v1.0.md)
  - [theory/evaluation/s-core-construction-obstruction-ledger.json](theory/evaluation/s-core-construction-obstruction-ledger.json)
  - [docs/research/faithful-representation-specification-v1.0.md](docs/research/faithful-representation-specification-v1.0.md)
  - [docs/research/independent-reasoning-definition-v1.0.md](docs/research/independent-reasoning-definition-v1.0.md)
- Suggested branch: `research/prove-s-core-w2-dynamics-history`
- Suggested PR title: `Prove S_core W2 dynamics history and revision`

### STRATEGIC-002: Prove the W3 global witness obligations
- Source: deduction-first strategic priority
- Affected files:
  - [docs/research/s-core-construction-obstruction-ledger-v1.0.md](docs/research/s-core-construction-obstruction-ledger-v1.0.md)
  - [theory/evaluation/s-core-construction-obstruction-ledger.json](theory/evaluation/s-core-construction-obstruction-ledger.json)
  - [docs/research/faithful-representation-specification-v1.0.md](docs/research/faithful-representation-specification-v1.0.md)
  - [theory/evaluation/thm-target-001.json](theory/evaluation/thm-target-001.json)
- Suggested branch: `research/prove-s-core-w3-global-witness`
- Suggested PR title: `Prove S_core W3 global witness obligations`

### STRATEGIC-003: Execute the remaining obstruction and negative-control program
- Source: deduction-first strategic priority
- Suggested branch: `research/execute-s-core-obstructions`
- Suggested PR title: `Execute remaining S_core obstruction program`

### STRATEGIC-004: Assemble the finite-core theorem or strongest obstruction
- Source: deduction-first strategic priority
- Suggested branch: `research/assemble-s-core-result`
- Suggested PR title: `Assemble S_core theorem or obstruction`

## Research Gap Summary

| Severity | Count | Source |
|---|---:|---|
| Critical | 0 | [docs/reports/research-gap-report.md](docs/reports/research-gap-report.md) |
| High | 1 | [docs/reports/research-gap-report.md](docs/reports/research-gap-report.md) |
| Medium | 67 | [docs/reports/research-gap-report.md](docs/reports/research-gap-report.md) |
| Low | 94 | [docs/reports/research-gap-report.md](docs/reports/research-gap-report.md) |

## Repository Navigation

- [Project Status](docs/reports/project-status-generated.md)
- [Research Gap Report](docs/reports/research-gap-report.md)
- [Next Actions](docs/planning/next-actions.md)
- [Dashboard Metrics](docs/planning/dashboard-metrics.md)
- [Deduction-First Standard](docs/governance/deduction-first-research-standard.md)
- [Proof Roadmap](docs/planning/deduction-first-proof-roadmap.md)
- [THM-TARGET-001](docs/research/thm-target-001-v1.0.md)
- [Faithful Representation](docs/research/faithful-representation-specification-v1.0.md)
- [P8 Role Decision](docs/research/p8-theorem-role-decision-v1.0.md)
- [S_core Lemma Ledger](docs/research/s-core-construction-obstruction-ledger-v1.0.md)
- [S_core Lemma Registry](theory/evaluation/s-core-construction-obstruction-ledger.json)
- [S_core W0 Proof](docs/research/s-core-w0-normalization-proof-v1.0.md)
- [S_core W0 Proof Registry](theory/evaluation/s-core-w0-normalization-proof.json)
- [S_core W1 Proof](docs/research/s-core-w1-direct-axis-proof-v1.0.md)
- [S_core W1 Proof Registry](theory/evaluation/s-core-w1-direct-axis-proof.json)
- [Evidence Registry](theory/evaluation/evidence-registry.yaml)
- [External Validation Registry](theory/evaluation/external-validation-registry.yaml)
- [Primitive Pressure Registry](theory/falsification/primitive-pressure-registry.yaml)
- [Adversarial Test Suite](theory/falsification/adversarial-test-suite.yaml)
- [Repository Index](docs/planning/repository-index.md)

## Current Roadmap

- Current phase: S_core W2 dynamics history revision and self-modification
- Completed foundation: domain; IRD-001; PB-001; PBTS-001; theorem target; premise ledger v1.4; faithful semantics; P8 split; W0; W1
- In progress: `LEM-SC-010`, `011`, `013`, `015`, and `016`, with `OBS-SC-004` and `OBS-SC-005`
- Planned: W3 global witness; remaining W4 obstructions; W5 assembly; S_IRD extension; lower bounds; minimality; mechanization; independent review
- Parallel: PBTS replication, comparative evaluation, boundary discovery, and application validation

## Command Center

```bash
make research-check
make health-fast
make health
make docs-check
make plan
make dashboard
```

## Typical Workflow

1. Run `make research-check` and `make health-fast`.
2. Open the lemma ledger and latest proof package.
3. Select the earliest open obligation with resolved dependencies.
4. Freeze assumptions, statement, countermodels, failure conditions, and nonclaims.
5. Prove, refute, or establish the strongest justified obstruction.
6. Preserve failures and unresolved obligations.
7. Run full health before merge.

<!-- END GENERATED PROJECT FAR DASHBOARD -->

## Certification and Architecture Navigation

- Repository certification governance: [docs/governance/repository-certification-standard.md](docs/governance/repository-certification-standard.md).
- Repository certification inventory baseline: [docs/audits/repository-certification-inventory-audit.md](docs/audits/repository-certification-inventory-audit.md).
- Semantic certification and terminology baseline: [docs/audits/semantic-certification-report.md](docs/audits/semantic-certification-report.md).
- Canonical vocabulary index: [docs/glossary/canonical-vocabulary-index.md](docs/glossary/canonical-vocabulary-index.md).
- Repository architecture certification and report-root policy: [docs/audits/repository-architecture-certification-report.md](docs/audits/repository-architecture-certification-report.md).
- Repository Certification Index: [docs/certification/README.md](docs/certification/README.md).
- Repository Domain Registry: [docs/architecture/repository-domain-registry.md](docs/architecture/repository-domain-registry.md).
- Documentation standardization report: [docs/audits/documentation-standardization-report.md](docs/audits/documentation-standardization-report.md).
- Repository compliance enforcement report: [docs/audits/repository-compliance-enforcement-report.md](docs/audits/repository-compliance-enforcement-report.md).
- Independent repository certification audit: [docs/audits/independent-repository-certification-audit.md](docs/audits/independent-repository-certification-audit.md).
- Repository certification status: [docs/certification/repository-certification-status.md](docs/certification/repository-certification-status.md).

## Mechanization MVP

Phase 3 mechanization provides an executable MVP for the `far-ir/1.0` interchange format. It includes a canonical Python IR, JSON/YAML parsing, deterministic normalization and serialization, graph construction and dependency validation, structured diagnostics, a CLI, and a versioned conformance suite.

```bash
python -m pip install -r requirements.txt
python -m pip install -e .
far version
far validate examples/mechanization/minimal-investigation.json
far normalize examples/mechanization/minimal-investigation.json
far graph examples/mechanization/minimal-investigation.json
python -m mechanization.far_mechanization.conformance
```

The MVP intentionally defers proof verification, automated reasoning, operation execution, REST APIs, persistent storage, web interfaces, plugin systems, production hardening, and independent external implementation.
