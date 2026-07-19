#!/usr/bin/env python3
"""Run the Project FAR advisory self-advancement planning pipeline."""
from __future__ import annotations
from pathlib import Path
import re, subprocess, sys
ROOT=Path(__file__).resolve().parents[1]
CMDS=[['python','tools/project_status_report.py'],['python','tools/detect_research_gaps.py'],['python','tools/generate_next_tasks.py'],['python','tools/generate_dependency_report.py'],['python','tools/generate_dependency_graph.py'],['python','tools/theory_impact_analyzer.py'],['python','tools/dashboard_metrics.py'],['python','tools/update_readme_dashboard.py']]
OPTIONAL_HEALTH=['python','tools/repo_health_check.py','--fast']
GEN=[ROOT/'README.md',ROOT/'docs/planning/dashboard-metrics.md',ROOT/'docs/planning/repository-index.md',ROOT/'docs/reports/project-status-generated.md',ROOT/'docs/reports/research-gap-report.md',ROOT/'docs/planning/next-actions.md',ROOT/'docs/reports/dependency-report.md',ROOT/'docs/reports/dependency-graph.json',ROOT/'docs/reports/dependency-graph.mmd',ROOT/'docs/reports/theory-impact-report.md']
def run(cmd):
    r=subprocess.run(cmd,cwd=ROOT,text=True,capture_output=True)
    print(r.stdout,end='');
    if r.stderr: print(r.stderr,end='',file=sys.stderr)
    return r.returncode
def count_gaps():
    p=ROOT/'docs/reports/research-gap-report.md'
    return sum(1 for l in p.read_text(encoding='utf-8').splitlines() if l.startswith('| ') and 'GAP-' in l) if p.exists() else 0
def tasks():
    p=ROOT/'docs/planning/next-actions.md'
    if not p.exists(): return []
    return re.findall(r'^### ((?:TASK|STRATEGIC)-\d+): (.+)$', p.read_text(encoding='utf-8'), re.M)
def main():
    for cmd in CMDS:
        rc=run(cmd)
        if rc: return rc
    missing=[str(p.relative_to(ROOT)) for p in GEN if not p.exists()]
    if missing:
        print('Missing generated files: '+', '.join(missing), file=sys.stderr); return 2
    ts=tasks()
    health_rc=run(OPTIONAL_HEALTH)
    print('\nPROJECT FAR AUTOMATION COMPLETE\n')
    print('Generated')
    for p in GEN: print(f"- {p.relative_to(ROOT)}")
    print('\nRepository Health')
    print('PASS' if health_rc == 0 else 'FAIL')
    print(f"\nGaps found: {count_gaps()}")
    print(f"Recommended tasks: {len(ts)}")
    print('\nNext Recommended Action')
    if ts:
        print(f"{ts[0][0]}: {ts[0][1]}")
    else:
        print('None generated')
    print('\nTop 3 next actions:')
    for tid,title in ts[:3]: print(f"- {tid}: {title}")
    print('\nOpen: README.md')
    return health_rc
if __name__=='__main__': raise SystemExit(main())
