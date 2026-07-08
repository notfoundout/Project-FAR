# Dependency Report

Generated from [theory/dependencies/dependency-registry.yaml](../../theory/dependencies/dependency-registry.yaml) using [tools/generate_dependency_report.py](../../tools/generate_dependency_report.py).

This report is repository-infrastructure evidence only. It does not infer controversial semantic dependencies or alter accepted theory content.

## Registry Inputs

- Schema: [theory/dependencies/dependency-schema.yaml](../../theory/dependencies/dependency-schema.yaml)
- Registry: [theory/dependencies/dependency-registry.yaml](../../theory/dependencies/dependency-registry.yaml)

## Summary

- Dependency records: 21
- Registry nodes: 30
- Registry edges: 21

## Counts by Source Type

| Value | Count |
|---|---:|
| `document` | 2 |
| `proof_object` | 5 |
| `release` | 2 |
| `report` | 3 |
| `tool` | 5 |
| `workflow` | 4 |

## Counts by Target Type

| Value | Count |
|---|---:|
| `document` | 3 |
| `registry` | 2 |
| `release` | 2 |
| `report` | 5 |
| `theorem` | 5 |
| `tool` | 4 |

## Counts by Relationship

| Value | Count |
|---|---:|
| `depends_on` | 5 |
| `documents` | 2 |
| `generates` | 5 |
| `references` | 5 |
| `uses` | 4 |

## High-Confidence Dependencies

| ID | Source | Relationship | Target | Evidence |
|---|---|---|---|---|
| `DEP-0001` | [theory/proof-objects/T-001.proof.yaml](../../theory/proof-objects/T-001.proof.yaml) | `depends_on` | [theory/theorems/theorems.md](../../theory/theorems/theorems.md) | proof object filename T-001 and theorem catalog file exist in repository. |
| `DEP-0002` | [theory/proof-objects/T-002.proof.yaml](../../theory/proof-objects/T-002.proof.yaml) | `depends_on` | [theory/theorems/theorems.md](../../theory/theorems/theorems.md) | proof object filename T-002 and theorem catalog file exist in repository. |
| `DEP-0003` | [theory/proof-objects/T-003.proof.yaml](../../theory/proof-objects/T-003.proof.yaml) | `depends_on` | [theory/theorems/theorems.md](../../theory/theorems/theorems.md) | proof object filename T-003 and theorem catalog file exist in repository. |
| `DEP-0004` | [theory/proof-objects/T-004.proof.yaml](../../theory/proof-objects/T-004.proof.yaml) | `depends_on` | [theory/theorems/theorems.md](../../theory/theorems/theorems.md) | proof object filename T-004 and theorem catalog file exist in repository. |
| `DEP-0005` | [theory/proof-objects/T-005.proof.yaml](../../theory/proof-objects/T-005.proof.yaml) | `depends_on` | [theory/theorems/theorems.md](../../theory/theorems/theorems.md) | proof object filename T-005 and theorem catalog file exist in repository. |
| `DEP-0006` | [docs/reports/primitive-sufficiency-report.md](primitive-sufficiency-report.md) | `references` | [theory/evaluation/evidence-registry.yaml](../../theory/evaluation/evidence-registry.yaml) | Primitive sufficiency report summarizes evidence registry counts and classifications. |
| `DEP-0007` | [docs/reports/adversarial-evaluation-report.md](adversarial-evaluation-report.md) | `references` | [theory/falsification/adversarial-test-suite.yaml](../../theory/falsification/adversarial-test-suite.yaml) | Adversarial evaluation report summarizes adversarial test suite content. |
| `DEP-0008` | [docs/reports/release-readiness-report.md](release-readiness-report.md) | `references` | [docs/reports/research-gap-report.md](research-gap-report.md) | Release readiness report includes research-gap status and links to research-gap report. |
| `DEP-0009` | [README.md](../../README.md) | `references` | [docs/reports/project-status-generated.md](project-status-generated.md) | README Command Center links to Project Status. |
| `DEP-0010` | [README.md](../../README.md) | `references` | [docs/reports/research-gap-report.md](research-gap-report.md) | README Command Center links to Research Gap Report. |
| `DEP-0011` | [tools/project_status_report.py](../../tools/project_status_report.py) | `generates` | [docs/reports/project-status-generated.md](project-status-generated.md) | Tool defines OUT as docs/reports/project-status-generated.md. |
| `DEP-0012` | [tools/detect_research_gaps.py](../../tools/detect_research_gaps.py) | `generates` | [docs/reports/research-gap-report.md](research-gap-report.md) | Tool writes docs/reports/research-gap-report.md. |
| `DEP-0013` | [tools/generate_next_tasks.py](../../tools/generate_next_tasks.py) | `generates` | [docs/planning/next-actions.md](../planning/next-actions.md) | Tool writes docs/planning/next-actions.md. |
| `DEP-0014` | [tools/dashboard_metrics.py](../../tools/dashboard_metrics.py) | `generates` | [docs/planning/dashboard-metrics.md](../planning/dashboard-metrics.md) | Tool defines OUT as docs/planning/dashboard-metrics.md. |
| `DEP-0015` | [tools/update_readme_dashboard.py](../../tools/update_readme_dashboard.py) | `generates` | [README.md](../../README.md) | Tool defines README and updates the generated dashboard block. |
| `DEP-0016` | [.github/workflows/repository-health.yml](../../.github/workflows/repository-health.yml) | `uses` | [Makefile](../../Makefile) | Workflow invokes make health-fast. |
| `DEP-0017` | [.github/workflows/regenerate-dashboard.yml](../../.github/workflows/regenerate-dashboard.yml) | `uses` | [Makefile](../../Makefile) | Workflow invokes make dashboard. |
| `DEP-0018` | [.github/workflows/release-readiness.yml](../../.github/workflows/release-readiness.yml) | `uses` | [tools/release_readiness_report.py](../../tools/release_readiness_report.py) | Workflow invokes python tools/release_readiness_report.py. |
| `DEP-0019` | [.github/workflows/repository-maintenance.yml](../../.github/workflows/repository-maintenance.yml) | `uses` | [Makefile](../../Makefile) | Workflow invokes make health-fast and make dashboard. |
| `DEP-0020` | [docs/releases/project-far-v0.3.1.md](../releases/project-far-v0.3.1.md) | `documents` | [docs/releases/github-release-v0.3.1.md](../releases/github-release-v0.3.1.md) | v0.3.1 release document and GitHub release notes describe the same maintenance release. |
| `DEP-0021` | [docs/releases/project-far-v0.3.1.md](../releases/project-far-v0.3.1.md) | `documents` | [docs/releases/project-far-v0.3.0.md](../releases/project-far-v0.3.0.md) | v0.3.1 explicitly preserves the v0.3.0 internal-validation baseline. |

## Provisional Dependencies

| ID | Source | Relationship | Target | Evidence |
|---|---|---|---|---|
| None |  |  |  |  |

## Needs-Review Dependencies

| ID | Source | Relationship | Target | Evidence |
|---|---|---|---|---|
| None |  |  |  |  |

## Orphan-Like Nodes Detected from Registry Only

Orphan-like means a registered node currently has only incoming or only outgoing registry edges. This is not a repository-wide orphaned-file finding.

- [.github/workflows/regenerate-dashboard.yml](../../.github/workflows/regenerate-dashboard.yml)
- [.github/workflows/release-readiness.yml](../../.github/workflows/release-readiness.yml)
- [.github/workflows/repository-health.yml](../../.github/workflows/repository-health.yml)
- [.github/workflows/repository-maintenance.yml](../../.github/workflows/repository-maintenance.yml)
- [Makefile](../../Makefile)
- [docs/planning/dashboard-metrics.md](../planning/dashboard-metrics.md)
- [docs/planning/next-actions.md](../planning/next-actions.md)
- [docs/releases/github-release-v0.3.1.md](../releases/github-release-v0.3.1.md)
- [docs/releases/project-far-v0.3.0.md](../releases/project-far-v0.3.0.md)
- [docs/releases/project-far-v0.3.1.md](../releases/project-far-v0.3.1.md)
- [docs/reports/adversarial-evaluation-report.md](adversarial-evaluation-report.md)
- [docs/reports/primitive-sufficiency-report.md](primitive-sufficiency-report.md)
- [docs/reports/project-status-generated.md](project-status-generated.md)
- [docs/reports/release-readiness-report.md](release-readiness-report.md)
- [docs/reports/research-gap-report.md](research-gap-report.md)
- [theory/evaluation/evidence-registry.yaml](../../theory/evaluation/evidence-registry.yaml)
- [theory/falsification/adversarial-test-suite.yaml](../../theory/falsification/adversarial-test-suite.yaml)
- [theory/proof-objects/T-001.proof.yaml](../../theory/proof-objects/T-001.proof.yaml)
- [theory/proof-objects/T-002.proof.yaml](../../theory/proof-objects/T-002.proof.yaml)
- [theory/proof-objects/T-003.proof.yaml](../../theory/proof-objects/T-003.proof.yaml)
- [theory/proof-objects/T-004.proof.yaml](../../theory/proof-objects/T-004.proof.yaml)
- [theory/proof-objects/T-005.proof.yaml](../../theory/proof-objects/T-005.proof.yaml)
- [theory/theorems/theorems.md](../../theory/theorems/theorems.md)
- [tools/dashboard_metrics.py](../../tools/dashboard_metrics.py)
- [tools/detect_research_gaps.py](../../tools/detect_research_gaps.py)
- [tools/generate_next_tasks.py](../../tools/generate_next_tasks.py)
- [tools/project_status_report.py](../../tools/project_status_report.py)
- [tools/release_readiness_report.py](../../tools/release_readiness_report.py)
- [tools/update_readme_dashboard.py](../../tools/update_readme_dashboard.py)

## Top Referenced Targets

| Target | Incoming Records |
|---|---:|
| [theory/theorems/theorems.md](../../theory/theorems/theorems.md) | 5 |
| [docs/reports/research-gap-report.md](research-gap-report.md) | 3 |
| [Makefile](../../Makefile) | 3 |
| [docs/reports/project-status-generated.md](project-status-generated.md) | 2 |
| [theory/evaluation/evidence-registry.yaml](../../theory/evaluation/evidence-registry.yaml) | 1 |
| [theory/falsification/adversarial-test-suite.yaml](../../theory/falsification/adversarial-test-suite.yaml) | 1 |
| [docs/planning/next-actions.md](../planning/next-actions.md) | 1 |
| [docs/planning/dashboard-metrics.md](../planning/dashboard-metrics.md) | 1 |
| [README.md](../../README.md) | 1 |
| [tools/release_readiness_report.py](../../tools/release_readiness_report.py) | 1 |

## Known Limitations

- The registry is intentionally seeded from explicit repository structure only.
- Absence of a dependency record does not imply absence of a real dependency.
- Relationship labels are infrastructure classifications, not final semantic conclusions.
- Generated graph outputs are derived from registry records and inherit registry incompleteness.
- Future v0.4 tooling must distinguish accepted evidence from provisional or needs-review records.
