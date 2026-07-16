# Project FAR

[![Release](https://img.shields.io/github/v/release/notfoundout/Project-FAR?include_prereleases&label=release)](https://github.com/notfoundout/Project-FAR/releases/tag/v0.4.0)
[![Verify Theory](https://github.com/notfoundout/Project-FAR/actions/workflows/repo-health.yml/badge.svg)](https://github.com/notfoundout/Project-FAR/actions/workflows/repo-health.yml)

Project FAR is a foundational framework for representing, analyzing, and comparing structured, explicit, and auditable reasoning.

This root README is the canonical Project FAR command center: the single entry point for repository status, health, evidence, planning, and navigation. Only the generated dashboard block below is automatically regenerated; content outside the block is manually maintained.

## Central Research Program

Project FAR's primary objective is to determine whether every reasoning process necessarily instantiates a common underlying structure and, if so, whether that structure is universal and minimal.

The project does not assume that a universal structure exists, nor that FAR is that structure. The Foundation, theory, mechanization, validation work, and future implementations are instruments for evaluating the question rather than presupposing its answer.

**[Read the Central Research Program](docs/governance/central-research-program.md)**

<!-- BEGIN GENERATED PROJECT FAR DASHBOARD -->

## Repository Status

- Current release: [docs/releases/project-far-v0.4.0.md](docs/releases/project-far-v0.4.0.md)
- Current project phase: post-CRE-001 prospective semantics baseline; CRE-002 preparation
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

### STRATEGIC-001: Plan independent replication of CRE-002-EXT-001
- Source: strategic roadmap priority
- Affected files:
  - [docs/methodology/adversarial-evaluation.md](docs/methodology/adversarial-evaluation.md)
  - [docs/governance/central-research-program.md](docs/governance/central-research-program.md)
  - [docs/reports/cre002-ext001-evidence-analysis.md](docs/reports/cre002-ext001-evidence-analysis.md)
- Suggested branch: `research/plan-cre002-ext001-independent-replication`
- Suggested PR title: `Plan independent CRE-002-EXT-001 replication`

### STRATEGIC-002: Design a boundary-focused CRE-003
- Source: strategic roadmap priority
- Affected files:
  - [theory/evaluation/comparative-representation](theory/evaluation/comparative-representation)
  - [docs/ROADMAP.md](docs/ROADMAP.md)
  - [docs/reports/cre002-ext001-evidence-analysis.md](docs/reports/cre002-ext001-evidence-analysis.md)
- Suggested branch: `research/design-cre003-boundary-test`
- Suggested PR title: `Design CRE-003 boundary test`

### STRATEGIC-003: Audit comparative representation cost
- Source: strategic roadmap priority
- Affected files:
  - [docs/reports/cre002-ext001-evidence-analysis.md](docs/reports/cre002-ext001-evidence-analysis.md)
  - [theory/evaluation/comparative-representation](theory/evaluation/comparative-representation)
- Suggested branch: `research/audit-comparative-representation-cost`
- Suggested PR title: `Audit comparative representation cost`

### STRATEGIC-004: Preserve semantic and result drift locks
- Source: strategic roadmap priority
- Affected files:
  - [theory/evaluation/comparative-representation/semantics/vocabulary-semantics-baseline-1.1.json](theory/evaluation/comparative-representation/semantics/vocabulary-semantics-baseline-1.1.json)
  - [theory/evaluation/comparative-representation/experiments/CRE-002-EXT-001](theory/evaluation/comparative-representation/experiments/CRE-002-EXT-001)
- Suggested branch: `maintenance/monitor-cre002-ext001-drift`
- Suggested PR title: `Monitor CRE-002-EXT-001 drift`

### STRATEGIC-005: Prepare the next evidence release
- Source: strategic roadmap priority
- Affected files:
  - [docs/releases](docs/releases)
  - [docs/project-status.md](docs/project-status.md)
  - [docs/reports/cre002-ext001-evidence-analysis.md](docs/reports/cre002-ext001-evidence-analysis.md)
- Suggested branch: `release/prepare-post-cre002-evidence-release`
- Suggested PR title: `Prepare post-CRE-002 evidence release`

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

- Current phase: post-CRE-001 prospective semantics baseline; CRE-002 preparation
- Completed work: Repository Health; Self-Advancement Planner; README Command Center; External Validation; CRP v1.0 registration; deterministic CRE-001 implementation; vocabulary-native compilation; executable lowering; deterministic verification; replayable lowering traces; mutation testing; adversarial compiler audit; repository integration
- In-progress work: CRE-002 preregistration design using Vocabulary Semantics Baseline 1.0 prospectively
- Planned work: prospective CRE-002 execution; prospective evidence analysis; independent replication; semantic drift monitoring; Theory Dependency Graph; Knowledge Graph; Evidence Dashboard; Theory Impact Analyzer; Semantic Consistency Auditor

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
5. Open source reference
6. Open affected files
7. Copy generated task brief
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
