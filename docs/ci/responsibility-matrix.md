# CI Responsibility Matrix

| Workflow | Trigger | Responsibility | Local equivalent | Timeout policy |
|---|---|---|---|---|
| `repo-health.yml` | pull request and push to `main` | Canonical read-only PR health verification. | `python tools/repo_health_check.py --fast` | Job timeout: 30 minutes; per-subprocess timeout defaults to `PROJECT_FAR_HEALTH_TIMEOUT` or 120 seconds. |
| `repository-health.yml` | manual dispatch | Canonical full read-only verification. | `python tools/repo_health_check.py --full` | Job timeout: 60 minutes; same per-subprocess policy. |
| `regenerate-dashboard.yml` | manual dispatch | Generated dashboard/report update workflow. Not a PR verification authority. | `make dashboard` | Job timeout: 30 minutes. |
| `release-readiness.yml` | manual dispatch | Release-readiness report generation and artifact upload. | `python tools/release_readiness_report.py` after full health. | Job timeout: 60 minutes. |
| `project-planning.yml` | manual dispatch | Advisory planning generation. | `python tools/self_advancement_plan.py` | Job timeout: 30 minutes. |
| `repository-maintenance.yml` | manual dispatch | Manual maintenance summary and generated report support. | maintenance commands in workflow | Job timeout: 60 minutes. |

Definitions of repository health must live in `tools/repo_health_check.py`; workflows must not independently encode divergent health command lists.
