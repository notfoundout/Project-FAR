# Repository Automation

Project FAR automation is advisory infrastructure. It regenerates documentation, reports, dashboard metrics, repository alerts, and release-readiness checklists without changing accepted theory.

## Architecture

Canonical automation has one implementation per operation:

- `tools/self_advancement_plan.py` is the orchestration entry point for planning and dashboard generation.
- `tools/repo_health_check.py` is the validation entry point.
- `tools/update_readme_dashboard.py` is the README command-center renderer.
- `tools/repository_alerts.py` centralizes alert computation for dashboards and future reports.
- `tools/dashboard_metrics.py` computes repository metrics and maintains trend snapshots.
- `tools/release_readiness_report.py` generates the advisory release checklist.

Future automation should call these tools through Make targets rather than duplicating logic in workflows.

## Make Targets

- `make dashboard` runs the canonical planner.
- `make plan` runs the canonical planner.
- `make health-fast` runs fast repository validation.
- `make health` runs full repository validation.
- `make docs-check` validates documentation.
- `make release-readiness` generates the release-readiness report.

## GitHub Actions

Four manual workflows are available:

- Repository Health: runs `make health-fast` and reports pass/fail, failed checks, and execution time.
- Regenerate Command Center: runs `make dashboard`, commits regenerated artifacts when possible, and opens a fallback PR if push is unavailable.
- Release Readiness: runs `make health`, `make dashboard`, and generates `docs/reports/release-readiness-report.md` without publishing a release.
- Repository Maintenance: runs health, dashboard regeneration, and release readiness as the preferred one-click maintenance operation.

## Planner

The planner regenerates README dashboard content, project status, research gap reporting, next actions, dashboard metrics, and repository index data. Add future generated infrastructure to the planner instead of creating separate orchestration scripts.

## Release Readiness

The release-readiness report is the canonical release checklist. It evaluates repository health, internal links, generated reports, README synchronization, release consistency, registry validation, critical research gaps, candidate primitive failures, documentation completeness, and planner freshness. Recommendations are advisory: `READY`, `READY WITH WARNINGS`, or `NOT READY`.

## Integration Rule

Automation may regenerate documentation, reports, dashboards, metrics, validations, and recommendations. Automation must never alter primitives, definitions, axioms, theorem statements, proof objects, parser behavior, reasoning-engine behavior, metadata schemas, or evaluation conclusions.
