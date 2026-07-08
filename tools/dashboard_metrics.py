#!/usr/bin/env python3
"""Generate Project FAR dashboard metrics."""
from __future__ import annotations

from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
import json
import yaml

from report_link_utils import markdown_link

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs/planning/dashboard-metrics.md'
HISTORY = ROOT / 'docs/planning/dashboard-metrics-history.json'
EVIDENCE = ROOT / 'theory/evaluation/evidence-registry.yaml'
EXTERNAL = ROOT / 'theory/evaluation/external-validation-registry.yaml'
ADVERSARIAL = ROOT / 'theory/falsification/adversarial-test-suite.yaml'
PRESSURE = ROOT / 'theory/falsification/primitive-pressure-registry.yaml'
GAPS = ROOT / 'docs/reports/research-gap-report.md'

SKIP_PARTS = {'.git', '__pycache__', '.pytest_cache', '.mypy_cache', '.venv', 'venv', 'node_modules'}


def load_yaml(path: Path) -> dict:
    if not path.exists():
        return {}
    data = yaml.safe_load(path.read_text(encoding='utf-8'))
    return data if isinstance(data, dict) else {}


def entries(data: dict) -> list:
    values = data.get('entries') or data.get('tests') or []
    return values if isinstance(values, list) else []


def iter_repo_files() -> list[Path]:
    files = []
    for path in ROOT.rglob('*'):
        if not path.is_file():
            continue
        if any(part in SKIP_PARTS for part in path.relative_to(ROOT).parts):
            continue
        if path.suffix == '.pyc':
            continue
        files.append(path)
    return files


def gap_counts() -> Counter:
    counts = Counter()
    if not GAPS.exists():
        return counts
    for line in GAPS.read_text(encoding='utf-8').splitlines():
        if not (line.startswith('| ') and 'GAP-' in line):
            continue
        parts = [part.strip() for part in line.strip('|').split('|')]
        if len(parts) > 3:
            counts[parts[3].title()] += 1
    return counts


def collect_metrics() -> list[tuple[str, int, Path | str]]:
    files = iter_repo_files()
    evidence = entries(load_yaml(EVIDENCE))
    external = entries(load_yaml(EXTERNAL))
    adversarial = entries(load_yaml(ADVERSARIAL))
    pressure = load_yaml(PRESSURE).get('primitives') or []
    candidate_failures = sum(len(p.get('candidate_primitive_failures') or []) for p in pressure if isinstance(p, dict))
    pressure_extensions = sum(len(p.get('conservative_extensions') or []) for p in pressure if isinstance(p, dict))
    conservative_extensions = pressure_extensions + sum(
        1 for item in evidence + external
        if 'conservative extension' in str(item.get('classification', '')).lower()
    )
    fits_far = sum(1 for item in evidence + external if 'fits far' in str(item.get('classification', '')).lower())
    unresolved = sum(1 for item in evidence + external + adversarial if 'unresolved' in str(item).lower())
    unresolved += sum(len(p.get('unresolved_pressures') or []) for p in pressure if isinstance(p, dict))
    gaps = gap_counts()
    return [
        ('Markdown files', sum(1 for path in files if path.suffix.lower() == '.md'), ROOT),
        ('Theory files', sum(1 for path in files if 'theory' in path.relative_to(ROOT).parts), ROOT / 'theory'),
        ('Python tools', sum(1 for path in files if path.suffix == '.py' and 'tools' in path.relative_to(ROOT).parts), ROOT / 'tools'),
        ('Reports', sum(1 for path in files if 'reports' in path.relative_to(ROOT).parts), ROOT / 'docs/reports'),
        ('Registries', sum(1 for path in files if 'registry' in path.name.lower()), ROOT / 'theory'),
        ('Proof objects', len(list((ROOT / 'theory/proof-objects').glob('T-*.proof.yaml'))), ROOT / 'theory/proof-objects'),
        ('Examples', sum(1 for path in files if 'examples' in path.relative_to(ROOT).parts), ROOT / 'examples'),
        ('Maintenance documents', sum(1 for path in files if 'maintenance' in path.relative_to(ROOT).parts), ROOT / 'docs/maintenance'),
        ('Releases', sum(1 for path in files if 'releases' in path.relative_to(ROOT).parts), ROOT / 'docs/releases'),
        ('Internal evaluations', len(evidence), EVIDENCE),
        ('External evaluations', len(external), EXTERNAL),
        ('Adversarial fixtures', len(adversarial), ADVERSARIAL),
        ('Counterexample fixtures', len(list((ROOT / 'tests/counterexamples').glob('*'))) if (ROOT / 'tests/counterexamples').exists() else len(list((ROOT / 'tests').glob('*counter*'))) if (ROOT / 'tests').exists() else 0, ROOT / 'tests'),
        ('Candidate primitive failures', candidate_failures, PRESSURE),
        ('Conservative extensions', conservative_extensions, PRESSURE),
        ('Fits FAR', fits_far, EVIDENCE),
        ('Unresolved cases', unresolved, GAPS),
        ('Unresolved gaps', sum(gaps.values()), GAPS),
        ('Documentation coverage', sum(1 for path in files if path.suffix.lower() == '.md'), ROOT / 'docs'),
        ('Health-check availability', 1 if (ROOT / 'tools/repo_health_check.py').exists() else 0, ROOT / 'tools/repo_health_check.py'),
    ]



def load_history() -> list[dict]:
    if not HISTORY.exists():
        return []
    try:
        data = json.loads(HISTORY.read_text(encoding='utf-8'))
    except json.JSONDecodeError:
        return []
    return data if isinstance(data, list) else []


def write_history(snapshot: dict[str, int]) -> None:
    history = load_history()
    history.append({'generated_at': datetime.now(timezone.utc).replace(microsecond=0).isoformat(), 'metrics': snapshot})
    HISTORY.write_text(json.dumps(history[-25:], indent=2) + '\n', encoding='utf-8')


def previous_snapshot(history: list[dict]) -> dict[str, int] | None:
    if not history:
        return None
    metrics = history[-1].get('metrics')
    return metrics if isinstance(metrics, dict) else None


def change(current: int, previous: int | None) -> str:
    if previous is None:
        return 'not initialized'
    delta = current - previous
    return f'{delta:+d}'

def main() -> int:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    collected = collect_metrics()
    snapshot = {name: value for name, value, source in collected}
    previous = previous_snapshot(load_history())
    write_history(snapshot)
    lines = [
        '# Dashboard Metrics',
        '',
        f'Navigation: {markdown_link("README.md", OUT, "README Command Center")} | {markdown_link("docs/reports/project-status-generated.md", OUT, "Project Status")} | {markdown_link("docs/reports/research-gap-report.md", OUT, "Research Gaps")} | {markdown_link("docs/planning/next-actions.md", OUT, "Next Actions")}',
        '',
        '| Metric | Current | Previous | Change | Source |',
        '|---|---:|---:|---:|---|',
    ]
    for name, value, source in collected:
        prev = None if previous is None else previous.get(name)
        prev_display = 'not initialized' if prev is None else prev
        lines.append(f'| {name} | {value} | {prev_display} | {change(value, prev)} | {markdown_link(source, OUT)} |')
    lines += [
        '',
        ('Trend tracking has not yet been initialized.' if previous is None else f'Trend tracking compares the current snapshot with {HISTORY.name}.'),
        '',
        f'Navigation: {markdown_link("README.md", OUT, "README Command Center")} | {markdown_link("docs/reports/project-status-generated.md", OUT, "Project Status")} | {markdown_link("docs/reports/research-gap-report.md", OUT, "Research Gaps")} | {markdown_link("docs/planning/next-actions.md", OUT, "Next Actions")}',
        '',
    ]
    OUT.write_text('\n'.join(lines), encoding='utf-8')
    print(f'{OUT.relative_to(ROOT)} metrics generated')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
