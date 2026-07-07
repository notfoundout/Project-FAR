#!/usr/bin/env python3
"""Run the Project FAR advisory self-advancement planning pipeline."""
from __future__ import annotations
from pathlib import Path
import re, subprocess, sys
ROOT=Path(__file__).resolve().parents[1]
CMDS=[['python','tools/project_status_report.py'],['python','tools/detect_research_gaps.py'],['python','tools/generate_next_tasks.py']]
GEN=[ROOT/'docs/reports/project-status-generated.md',ROOT/'docs/reports/research-gap-report.md',ROOT/'docs/planning/next-actions.md']
def run(cmd):
    r=subprocess.run(cmd,cwd=ROOT,text=True,capture_output=True)
    print(r.stdout,end='');
    if r.stderr: print(r.stderr,end='',file=sys.stderr)
    return r.returncode
def count_gaps():
    p=ROOT/'docs/reports/research-gap-report.md'
    return sum(1 for l in p.read_text(encoding='utf-8').splitlines() if l.startswith('| GAP-')) if p.exists() else 0
def tasks():
    p=ROOT/'docs/planning/next-actions.md'
    if not p.exists(): return []
    return re.findall(r'^### (TASK-\d+): (.+)$', p.read_text(encoding='utf-8'), re.M)
def main():
    for cmd in CMDS:
        rc=run(cmd)
        if rc: return rc
    missing=[str(p.relative_to(ROOT)) for p in GEN if not p.exists()]
    if missing:
        print('Missing generated files: '+', '.join(missing), file=sys.stderr); return 2
    ts=tasks()
    print('\nGenerated files:')
    for p in GEN: print(f"- {p.relative_to(ROOT)}")
    print(f"Gaps found: {count_gaps()}")
    print(f"Recommended tasks: {len(ts)}")
    print('Top 3 next actions:')
    for tid,title in ts[:3]: print(f"- {tid}: {title}")
    return 0
if __name__=='__main__': raise SystemExit(main())
