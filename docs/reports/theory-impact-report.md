# Theory Impact Report

Results are based only on registered dependencies in `theory/dependencies/dependency-registry.yaml` and do not imply semantic dependence.

## Summary

- Dependency records: 21
- Registry nodes: 30
- Registry edges: 21
- Dependency inference: disabled; absent registry edges are never inferred.

## Registry Statistics

### Source Types

| Value | Count |
|---|---:|
| `document` | 2 |
| `proof_object` | 5 |
| `release` | 2 |
| `report` | 3 |
| `tool` | 5 |
| `workflow` | 4 |

### Target Types

| Value | Count |
|---|---:|
| `document` | 3 |
| `registry` | 2 |
| `release` | 2 |
| `report` | 5 |
| `theorem` | 5 |
| `tool` | 4 |

## Dependency Depth Histogram

| Value | Count |
|---|---:|
| `0` | 18 |
| `1` | 10 |
| `2` | 2 |

## Top 20 Highest-Impact Nodes

| Node | Affected Nodes | Max Depth |
|---|---:|---:|
| `theory/theorems/theorems.md` | 5 | 1 |
| `docs/reports/research-gap-report.md` | 4 | 2 |
| `Makefile` | 3 | 1 |
| `docs/reports/project-status-generated.md` | 3 | 2 |
| `README.md` | 1 | 1 |
| `docs/planning/dashboard-metrics.md` | 1 | 1 |
| `docs/planning/next-actions.md` | 1 | 1 |
| `docs/releases/github-release-v0.3.1.md` | 1 | 1 |
| `docs/releases/project-far-v0.3.0.md` | 1 | 1 |
| `theory/evaluation/evidence-registry.yaml` | 1 | 1 |
| `theory/falsification/adversarial-test-suite.yaml` | 1 | 1 |
| `tools/release_readiness_report.py` | 1 | 1 |
| `.github/workflows/regenerate-dashboard.yml` | 0 | 0 |
| `.github/workflows/release-readiness.yml` | 0 | 0 |
| `.github/workflows/repository-health.yml` | 0 | 0 |
| `.github/workflows/repository-maintenance.yml` | 0 | 0 |
| `docs/releases/project-far-v0.3.1.md` | 0 | 0 |
| `docs/reports/adversarial-evaluation-report.md` | 0 | 0 |
| `docs/reports/primitive-sufficiency-report.md` | 0 | 0 |
| `docs/reports/release-readiness-report.md` | 0 | 0 |

## Nodes with No Incoming Edges

- `.github/workflows/regenerate-dashboard.yml`
- `.github/workflows/release-readiness.yml`
- `.github/workflows/repository-health.yml`
- `.github/workflows/repository-maintenance.yml`
- `docs/releases/project-far-v0.3.1.md`
- `docs/reports/adversarial-evaluation-report.md`
- `docs/reports/primitive-sufficiency-report.md`
- `docs/reports/release-readiness-report.md`
- `theory/proof-objects/T-001.proof.yaml`
- `theory/proof-objects/T-002.proof.yaml`
- `theory/proof-objects/T-003.proof.yaml`
- `theory/proof-objects/T-004.proof.yaml`
- `theory/proof-objects/T-005.proof.yaml`
- `tools/dashboard_metrics.py`
- `tools/detect_research_gaps.py`
- `tools/generate_next_tasks.py`
- `tools/project_status_report.py`
- `tools/update_readme_dashboard.py`

## Nodes with No Outgoing Edges

- `Makefile`
- `docs/planning/dashboard-metrics.md`
- `docs/planning/next-actions.md`
- `docs/releases/github-release-v0.3.1.md`
- `docs/releases/project-far-v0.3.0.md`
- `docs/reports/project-status-generated.md`
- `docs/reports/research-gap-report.md`
- `theory/evaluation/evidence-registry.yaml`
- `theory/falsification/adversarial-test-suite.yaml`
- `theory/theorems/theorems.md`
- `tools/release_readiness_report.py`

## Circular Dependency Analysis

- No circular dependency chains detected.

## Broken Dependency Analysis

- No broken references detected.

## Missing Node Analysis

- No missing source or target node fields detected.

## Duplicate ID Analysis

- None detected.

## Orphan Registry Entries

Orphan registry entries are defined here as registered nodes with neither incoming nor outgoing registry edges after registry parsing.

- None detected.

## Confidence Summary

| Value | Count |
|---|---:|
| `high` | 21 |

## Status Summary

| Value | Count |
|---|---:|
| `accepted` | 18 |
| `generated` | 3 |

## Relationship Summary

| Value | Count |
|---|---:|
| `depends_on` | 5 |
| `documents` | 2 |
| `generates` | 5 |
| `references` | 5 |
| `uses` | 4 |

## Known Limitations

- The analyzer uses only explicit registry edges.
- Results do not imply semantic dependence.
- Missing registry edges mean unknown impact, not no impact.
- File existence checks validate repository paths only, not theory correctness.
