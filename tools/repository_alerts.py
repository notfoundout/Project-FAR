#!/usr/bin/env python3
"""Reusable repository alert computation for Project FAR automation."""
from __future__ import annotations
from collections import Counter
from pathlib import Path
import subprocess, sys

ROOT = Path(__file__).resolve().parents[1]
GAPS = ROOT / 'docs/reports/research-gap-report.md'
RELEASE_REPORT = ROOT / 'docs/reports/release-readiness-report.md'
NEXT = ROOT / 'docs/planning/next-actions.md'


def gap_counts() -> Counter:
    counts = Counter()
    if not GAPS.exists():
        return counts
    for line in GAPS.read_text(encoding='utf-8').splitlines():
        if line.startswith('| ') and 'GAP-' in line:
            parts = [p.strip() for p in line.strip('|').split('|')]
            if len(parts) > 3:
                counts[parts[3].title()] += 1
    return counts


def git_changed(path: Path | None = None) -> bool:
    cmd = ['git', 'status', '--porcelain']
    if path is not None:
        cmd += ['--', str(path.relative_to(ROOT) if path.is_absolute() else path)]
    result = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True)
    return bool(result.stdout.strip())


def compute_alerts(health_status: str = 'UNKNOWN', ci_status: str = 'Manual workflows available', release_status: str | None = None) -> list[dict[str, str | int]]:
    gaps = gap_counts()
    planner_status = 'CURRENT' if NEXT.exists() else 'MISSING'
    if release_status is None:
        release_status = 'AVAILABLE' if RELEASE_REPORT.exists() else 'NOT GENERATED'
    alerts = [
        {'category': 'Critical Issues', 'status': gaps.get('Critical', 0), 'source': GAPS},
        {'category': 'High Priority Issues', 'status': gaps.get('High', 0), 'source': GAPS},
        {'category': 'Repository Health', 'status': health_status, 'source': ROOT / 'docs/maintenance/repository-health-checks.md'},
        {'category': 'Planner Status', 'status': planner_status, 'source': NEXT},
        {'category': 'CI Status', 'status': ci_status, 'source': ROOT / '.github/workflows/repository-health.yml'},
        {'category': 'Release Readiness', 'status': release_status, 'source': RELEASE_REPORT},
    ]
    return alerts


def main() -> int:
    for alert in compute_alerts():
        print(f"{alert['category']}: {alert['status']} ({alert['source']})")
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
