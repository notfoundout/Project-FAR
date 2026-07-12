# Project FAR

[![Release](https://img.shields.io/github/v/release/notfoundout/Project-FAR?include_prereleases&label=release)](https://github.com/notfoundout/Project-FAR/releases/tag/v0.3.1)
[![Verify Theory](https://github.com/notfoundout/Project-FAR/actions/workflows/verify-theory.yml/badge.svg)](https://github.com/notfoundout/Project-FAR/actions/workflows/verify-theory.yml)

Project FAR is a foundational framework for representing, analyzing, and comparing structured, explicit, and auditable reasoning.

This root README is the canonical Project FAR command center: the single entry point for repository status, health, evidence, planning, and navigation. Only the generated dashboard block below is automatically regenerated; content outside the block is manually maintained.

<!-- BEGIN GENERATED PROJECT FAR DASHBOARD -->

## Repository Status

- Current release: [docs/releases/project-far-v0.3.1.md](docs/releases/project-far-v0.3.1.md)
- Current project phase: v0.4 external validation preparation
- Repository health status: PASS ([health checks](docs/maintenance/repository-health-checks.md))
- Planner status: CURRENT ([planner](tools/self_advancement_plan.py))
- Last dashboard generation time: 2026-07-08T16:26:56+00:00

## Repository Alerts

| Alert | Status | Source |
|---|---:|---|
| Critical Issues | 0 | [docs/reports/research-gap-report.md](docs/reports/research-gap-report.md) |
| High Priority Issues | 1 | [docs/reports/research-gap-report.md](docs/reports/research-gap-report.md) |
| Repository Health | PASS | [docs/maintenance/repository-health-checks.md](docs/maintenance/repository-health-checks.md) |
| Planner Status | CURRENT | [docs/planning/next-actions.md](docs/planning/next-actions.md) |
| CI Status | Manual workflows available | [.github/workflows/repository-health.yml](.github/workflows/repository-health.yml) |
| Release Readiness | AVAILABLE | [docs/reports/release-readiness-report.md](docs/reports/release-readiness-report.md) |

## Evidence Snapshot

| Metric | Current | Source |
|---|---:|---|
| Internal reasoning systems | 23 | [theory/evaluation/evidence-registry.yaml](theory/evaluation/evidence-registry.yaml) |
| External reasoning systems | 20 | [theory/evaluation/external-validation-registry.yaml](theory/evaluation/external-validation-registry.yaml) |
| Adversarial fixtures | 14 | [theory/falsification/adversarial-test-suite.yaml](theory/falsification/adversarial-test-suite.yaml) |
| Counterexample fixtures | 1 | [tests](tests) |
| Candidate primitive failures | 0 | [theory/falsification/primitive-pressure-registry.yaml](theory/falsification/primitive-pressure-registry.yaml) |
| Conservative extensions | 33 | [theory/falsification/primitive-pressure-registry.yaml](theory/falsification/primitive-pressure-registry.yaml) |
| Fits FAR | 12 | [theory/evaluation/evidence-registry.yaml](theory/evaluation/evidence-registry.yaml) |
| Unresolved cases | 12 | [docs/reports/project-status-generated.md](docs/reports/project-status-generated.md) |

## Progress Summary

Trend data is not yet available because no prior generated snapshot is stored.

| Metric | Current | Previous | Change |
|---|---:|---:|---:|
| Internal reasoning systems | 23 | not available | not available |
| External reasoning systems | 20 | not available | not available |
| Conservative extensions | 33 | not available | not available |
| Candidate primitive failures | 0 | not available | not available |
| Open gaps | 93 | not available | not available |

## Top Priority Tasks

### TASK-045: Review unresolved primitive pressure at `Reasoning Calculus`
- Source gap: [GAP-045](docs/reports/research-gap-report.md#gap-045)
- Affected files:
  - `Reasoning Calculus`
- Suggested branch: `codex/review-unresolved-primitive-pressure-gap-045`
- Suggested PR title: `Review unresolved primitive pressure (GAP-045)`

### TASK-001: Review unresolved case at `PS-001`
- Source gap: [GAP-001](docs/reports/research-gap-report.md#gap-001)
- Affected files:
  - `PS-001`
- Suggested branch: `codex/review-unresolved-case-gap-001`
- Suggested PR title: `Review unresolved case (GAP-001)`

### TASK-002: Review provisional system at `PS-001`
- Source gap: [GAP-002](docs/reports/research-gap-report.md#gap-002)
- Affected files:
  - `PS-001`
- Suggested branch: `codex/review-provisional-system-gap-002`
- Suggested PR title: `Review provisional system (GAP-002)`

### TASK-003: Review unresolved case at `PS-002`
- Source gap: [GAP-003](docs/reports/research-gap-report.md#gap-003)
- Affected files:
  - `PS-002`
- Suggested branch: `codex/review-unresolved-case-gap-003`
- Suggested PR title: `Review unresolved case (GAP-003)`

### TASK-004: Review provisional system at `PS-002`
- Source gap: [GAP-004](docs/reports/research-gap-report.md#gap-004)
- Affected files:
  - `PS-002`
- Suggested branch: `codex/review-provisional-system-gap-004`
- Suggested PR title: `Review provisional system (GAP-004)`

## Research Gap Summary

| Severity | Count | Source |
|---|---:|---|
| Critical | 0 | [docs/reports/research-gap-report.md](docs/reports/research-gap-report.md) |
| High | 1 | [docs/reports/research-gap-report.md](docs/reports/research-gap-report.md) |
| Medium | 55 | [docs/reports/research-gap-report.md](docs/reports/research-gap-report.md) |
| Low | 37 | [docs/reports/research-gap-report.md](docs/reports/research-gap-report.md) |

## Repository Navigation

- [Project Status](docs/reports/project-status-generated.md)
- [Research Gap Report](docs/reports/research-gap-report.md)
- [Next Actions](docs/planning/next-actions.md)
- [Dashboard Metrics](docs/planning/dashboard-metrics.md)
- [External Validation](docs/reports/external-validation-report.md)
- [Primitive Sufficiency](docs/reports/primitive-sufficiency-report.md)
- [Evidence Registry](theory/evaluation/evidence-registry.yaml)
- [External Validation Registry](theory/evaluation/external-validation-registry.yaml)
- [Primitive Pressure Registry](theory/falsification/primitive-pressure-registry.yaml)
- [Adversarial Test Suite](theory/falsification/adversarial-test-suite.yaml)
- [Releases](docs/releases)
- [Maintenance](docs/maintenance)
- [Planning](docs/planning/README.md)
- [Repository Index](docs/planning/repository-index.md)
- [Dependency Report](docs/reports/dependency-report.md)
- [Theory Impact Report](docs/reports/theory-impact-report.md)
- [Dependency Graph JSON](docs/reports/dependency-graph.json)
- [Dependency Graph Mermaid](docs/reports/dependency-graph.mmd)
- [Dependency Registry](theory/dependencies/dependency-registry.yaml)
- [Dependency Schema](theory/dependencies/dependency-schema.yaml)

## Current Roadmap

- Current phase: v0.4 external validation preparation
- Completed work: Repository Health; Self-Advancement Planner; README Command Center; External Validation
- In-progress work: Repository Automation
- Planned work: Theory Dependency Graph; Knowledge Graph; Evidence Dashboard; Theory Impact Analyzer; Semantic Consistency Auditor

## Command Center

### Local Commands

```bash
make dashboard
make health-fast
make health
make docs-check
make plan
```

### GitHub Actions

- Repository Health: [repository-health.yml](.github/workflows/repository-health.yml)
- Regenerate Dashboard: [regenerate-dashboard.yml](.github/workflows/regenerate-dashboard.yml)
- Release Readiness: [release-readiness.yml](.github/workflows/release-readiness.yml)
- Repository Maintenance: [repository-maintenance.yml](.github/workflows/repository-maintenance.yml)

## Typical Workflow

1. `make health-fast`
2. `make dashboard`
3. Open README
4. Choose top task
5. Open source gap
6. Open affected files
7. Copy generated Codex prompt
8. Implement
9. Run health
10. Merge

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
