# Project FAR

[![Release](https://img.shields.io/github/v/release/notfoundout/Project-FAR?include_prereleases&label=release)](https://github.com/notfoundout/Project-FAR/releases/tag/v0.4.0)
[![Verify Theory](https://github.com/notfoundout/Project-FAR/actions/workflows/repo-health.yml/badge.svg)](https://github.com/notfoundout/Project-FAR/actions/workflows/repo-health.yml)

Project FAR is a foundational framework for representing, analyzing, and comparing structured, explicit, and auditable reasoning.

This root README is the canonical Project FAR command center: the single entry point for repository status, health, evidence, planning, and navigation. Only the generated dashboard block below is automatically regenerated; content outside the block is manually maintained.

## Central Research Program

Project FAR's primary objective is to determine whether every reasoning process necessarily instantiates a common underlying structure and, if so, whether that structure is universal and minimal.

The project does not assume that a universal structure exists, nor that FAR is that structure. The Foundation, theory, mechanization, validation work, and future implementations are instruments for evaluating the question rather than presupposing its answer.

**[Read the Central Research Program](docs/governance/central-research-program.md)**

## Current Research Reset

The project is now deduction-first. The [Deduction-First Research Standard](docs/governance/deduction-first-research-standard.md), [Central Research Program](docs/governance/central-research-program.md), [Research Priority Reset](docs/governance/research-priority-reset.md), and machine-readable [Research Gate Registry](theory/evaluation/research-gates.json) make formal definition, proof, countermodel, lower-bound, equivalence, and impossibility work the primary path to the central answer.

[`THM-TARGET-001` v1.0](docs/research/thm-target-001-v1.0.md), premise ledger v1.1, and [`FAITHFUL-REP-001` v1.0](docs/research/faithful-representation-specification-v1.0.md) are frozen. The active objective is the P8 theorem-role decision: select and justify `coordinate`, `side_condition`, or `split` before beginning finite-core representation-proof construction.

PBTS-001 replication, comparative experiments, and external validation remain parallel supporting tracks for detecting ambiguity, defects, counterexamples, implementation dependence, and human-comprehension failures. They do not serve as prerequisites for constructing a proof.

Run `make research-check` to validate the theorem target, faithful-representation definition, deduction-first dependency structure, and conservative claim boundaries.

<!-- BEGIN GENERATED PROJECT FAR DASHBOARD -->

## Repository Status

- Current release: [docs/releases/project-far-v0.4.0.md](docs/releases/project-far-v0.4.0.md)
- Current project phase: P8 theorem-role decision
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

Trend data is not yet available because no prior generated snapshot is stored.

| Metric | Current | Previous | Change |
|---|---:|---:|---:|
| Internal reasoning systems | 23 | not available | not available |
| External reasoning systems | 29 | not available | not available |
| Conservative extensions | 35 | not available | not available |
| Candidate primitive failures | 0 | not available | not available |
| Open gaps | 162 | not available | not available |

## Top Priority Tasks

### STRATEGIC-001: Resolve the formal role of P8
- Source: deduction-first strategic priority
- Affected files:
  - [docs/research/faithful-representation-specification-v1.0.md](docs/research/faithful-representation-specification-v1.0.md)
  - [docs/research/thm-target-001-v1.0.md](docs/research/thm-target-001-v1.0.md)
  - [docs/research/preservation-basis-investigation-v1.0.md](docs/research/preservation-basis-investigation-v1.0.md)
  - [docs/research/pb001-execution-run-001-report.md](docs/research/pb001-execution-run-001-report.md)
  - [theory/evaluation/thm-target-001.json](theory/evaluation/thm-target-001.json)
- Suggested branch: `research/resolve-p8-theorem-role`
- Suggested PR title: `Resolve P8 theorem role`

### STRATEGIC-002: Build the S_core construction and obstruction ledger
- Source: deduction-first strategic priority
- Affected files:
  - [docs/research/faithful-representation-specification-v1.0.md](docs/research/faithful-representation-specification-v1.0.md)
  - [docs/research/thm-target-001-v1.0.md](docs/research/thm-target-001-v1.0.md)
  - [docs/research/independent-reasoning-definition-v1.0.md](docs/research/independent-reasoning-definition-v1.0.md)
  - [docs/planning/deduction-first-proof-roadmap.md](docs/planning/deduction-first-proof-roadmap.md)
- Suggested branch: `research/build-s-core-lemma-ledger`
- Suggested PR title: `Build S_core construction and obstruction ledger`

### STRATEGIC-003: Prove formal negative-control lemmas
- Source: deduction-first strategic priority
- Affected files:
  - [docs/research/faithful-representation-specification-v1.0.md](docs/research/faithful-representation-specification-v1.0.md)
  - [docs/methodology/negative-control-suite-v1.0.md](docs/methodology/negative-control-suite-v1.0.md)
  - [theory/falsification](theory/falsification)
  - [docs/planning/deduction-first-proof-roadmap.md](docs/planning/deduction-first-proof-roadmap.md)
- Suggested branch: `research/prove-faithful-negative-controls`
- Suggested PR title: `Prove faithful-representation negative-control lemmas`

### STRATEGIC-004: Develop the first uniform S_core constructor
- Source: deduction-first strategic priority
- Affected files:
  - [docs/research/faithful-representation-specification-v1.0.md](docs/research/faithful-representation-specification-v1.0.md)
  - [docs/research/thm-target-001-v1.0.md](docs/research/thm-target-001-v1.0.md)
  - [frameworks/FARA/architecture.md](frameworks/FARA/architecture.md)
  - [theory/evaluation/thm-target-001-premise-ledger.json](theory/evaluation/thm-target-001-premise-ledger.json)
- Suggested branch: `research/build-s-core-constructor`
- Suggested PR title: `Develop uniform S_core constructor`

### STRATEGIC-005: Prepare proof mechanization architecture
- Source: deduction-first strategic priority
- Affected files:
  - [mechanization](mechanization)
  - [docs/research/faithful-representation-specification-v1.0.md](docs/research/faithful-representation-specification-v1.0.md)
  - [docs/research/thm-target-001-v1.0.md](docs/research/thm-target-001-v1.0.md)
  - [docs/planning/deduction-first-proof-roadmap.md](docs/planning/deduction-first-proof-roadmap.md)
- Suggested branch: `research/plan-proof-mechanization`
- Suggested PR title: `Plan deduction-first proof mechanization`

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
- [Faithful Representation Registry](theory/evaluation/faithful-representation-specification-v1.0.json)
- [Evidence Registry](theory/evaluation/evidence-registry.yaml)
- [External Validation Registry](theory/evaluation/external-validation-registry.yaml)
- [Primitive Pressure Registry](theory/falsification/primitive-pressure-registry.yaml)
- [Adversarial Test Suite](theory/falsification/adversarial-test-suite.yaml)
- [Releases](docs/releases)
- [Maintenance](docs/maintenance)
- [Planning](docs/planning/README.md)
- [Repository Index](docs/planning/repository-index.md)

## Current Roadmap

- Current phase: P8 theorem-role decision
- Completed foundation for the active phase: architecture-neutral domain; IRD-001; PB-001; PBTS-001; deduction-first governance; THM-TARGET-001; premise ledger v1.1; FAITHFUL-REP-001
- In-progress work: select and justify coordinate, side_condition, or split for P8
- Planned work: S_core construction and obstruction ledger; formal negative-control lemmas; uniform constructor; finite-core theorem or refutation; extension analysis; lower bounds; minimality; mechanization; independent review
- Parallel supporting work: PBTS-001 independent replication, comparative evaluation, boundary discovery, and application validation

## Command Center

### Local Commands

```bash
make research-check
make health-fast
make health
make docs-check
make plan
make dashboard
```

### GitHub Actions

- Repository Health: [repository-health.yml](.github/workflows/repository-health.yml)
- Regenerate Dashboard: [regenerate-dashboard.yml](.github/workflows/regenerate-dashboard.yml)
- Release Readiness: [release-readiness.yml](.github/workflows/release-readiness.yml)
- Repository Maintenance: [repository-maintenance.yml](.github/workflows/repository-maintenance.yml)

## Typical Workflow

1. `make research-check`
2. `make health-fast`
3. Open THM-TARGET-001 and FAITHFUL-REP-001
4. Resolve the highest unsatisfied theorem obligation
5. Freeze assumptions, failure conditions, and nonclaims
6. Prove, refute, or register the obstruction
7. Preserve failures and unresolved obligations
8. Run health
9. Merge

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

Install dependencies and the local package:

```bash
python -m pip install -r requirements.txt
python -m pip install -e .
```

Minimal CLI workflow:

```bash
far version
far validate examples/mechanization/minimal-investigation.json
far normalize examples/mechanization/minimal-investigation.json
far graph examples/mechanization/minimal-investigation.json
python -m mechanization.far_mechanization.conformance
```

The MVP intentionally defers proof verification, automated reasoning, operation execution, REST APIs, persistent storage, web interfaces, plugin systems, production hardening, and independent external implementation.
