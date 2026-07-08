#!/usr/bin/env python3
"""Generate the canonical advisory Project FAR release-readiness checklist."""
from __future__ import annotations
from pathlib import Path
import subprocess, sys
from dashboard_metrics import collect_metrics
from repository_alerts import compute_alerts, gap_counts
from report_link_utils import markdown_link

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs/reports/release-readiness-report.md'


def run(cmd: list[str]) -> tuple[int, str]:
    cp = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True)
    return cp.returncode, (cp.stdout + cp.stderr).strip()


def exists(path: str) -> str:
    return 'PASS' if (ROOT / path).exists() else 'FAIL'


def recommendation(health_rc: int, gaps) -> str:
    if health_rc != 0 or gaps.get('Critical', 0):
        return 'NOT READY'
    if gaps.get('High', 0):
        return 'READY WITH WARNINGS'
    return 'READY'


def main() -> int:
    health_rc, health_out = run([sys.executable, 'tools/repo_health_check.py', '--fast'])
    gaps = gap_counts()
    rec = recommendation(health_rc, gaps)
    metrics = collect_metrics()
    alert_rows = compute_alerts('PASS' if health_rc == 0 else 'FAIL', release_status=rec)
    metric_map = {name: value for name, value, source in metrics}
    lines = [
        '# Release Readiness Report', '',
        'This advisory report is the canonical Project FAR release checklist. It never publishes a GitHub Release and does not authorize theory changes.', '',
        '## Repository Overview', '',
        '| Metric | Current | Source |', '|---|---:|---|',
    ]
    for name, value, source in metrics:
        lines.append(f'| {name} | {value} | {markdown_link(source, OUT)} |')
    lines += ['', '## Validation Results', '', '| Area | Status | Evidence |', '|---|---|---|',
        f'| Repository Health | {"PASS" if health_rc == 0 else "FAIL"} | `make health-fast` |',
        f'| Internal Links | {exists("tools/check_internal_links.py")} | {markdown_link("tools/check_internal_links.py", OUT)} |',
        f'| Generated Reports | {exists("docs/reports/project-status-generated.md")} | {markdown_link("docs/reports/project-status-generated.md", OUT)} |',
        f'| README Synchronization | {exists("README.md")} | {markdown_link("README.md", OUT)} |',
        f'| Release Consistency | {exists("tools/check_release_consistency.py")} | {markdown_link("tools/check_release_consistency.py", OUT)} |',
        f'| Registry Validation | {exists("tools/check_registry.py")} | {markdown_link("tools/check_registry.py", OUT)} |',
        f'| Critical Research Gaps | {gaps.get("Critical", 0)} | {markdown_link("docs/reports/research-gap-report.md", OUT)} |',
        f'| Candidate Primitive Failures | {metric_map.get("Candidate primitive failures", 0)} | {markdown_link("theory/falsification/primitive-pressure-registry.yaml", OUT)} |',
        f'| Documentation Completeness | {metric_map.get("Documentation coverage", 0)} | {markdown_link("docs", OUT)} |',
        f'| Planner Freshness | {exists("docs/planning/next-actions.md")} | {markdown_link("docs/planning/next-actions.md", OUT)} |',
        '', '## Documentation Status', '',
        f'- Markdown files: {metric_map.get("Markdown files", 0)}',
        f'- Reports: {metric_map.get("Reports", 0)}',
        f'- Maintenance documents: {metric_map.get("Maintenance documents", 0)}',
        '', '## Planning Status', '',
        f'- Planner: {markdown_link("tools/self_advancement_plan.py", OUT)}',
        f'- Next actions: {markdown_link("docs/planning/next-actions.md", OUT)}',
        '', '## Outstanding Critical Issues', '', f'- Critical issues: {gaps.get("Critical", 0)}',
        '', '## Outstanding High Priority Issues', '', f'- High priority issues: {gaps.get("High", 0)}',
        '', '## Repository Alerts', '', '| Category | Status | Source |', '|---|---:|---|']
    for alert in alert_rows:
        lines.append(f"| {alert['category']} | {alert['status']} | {markdown_link(alert['source'], OUT)} |")
    lines += ['', '## Release Recommendation', '', rec, '', '## Next Required Actions', '', '- Run `make health` before any human-approved release publication.', '- Resolve critical issues before release.', '- Review high priority issues when recommendation is READY WITH WARNINGS.', '', '<details><summary>Health output excerpt</summary>', '', '```text', '\n'.join(health_out.splitlines()[-80:]), '```', '', '</details>', '']
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text('\n'.join(lines), encoding='utf-8')
    print(f'{OUT.relative_to(ROOT)} generated: {rec}')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
