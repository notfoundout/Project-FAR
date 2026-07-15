#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import yaml
ROOT=Path(__file__).resolve().parents[1]
def main():
    errors=[]
    for p in sorted((ROOT/'.github/workflows').glob('*.yml')):
        data=yaml.safe_load(p.read_text())
        if not isinstance(data,dict): errors.append(f'{p}: not mapping'); continue
        for job_name,job in (data.get('jobs') or {}).items():
            if 'timeout-minutes' not in job: errors.append(f'{p.relative_to(ROOT)} job {job_name} missing timeout-minutes')
    if errors:
        print('CI WORKFLOW CHECK FAILED'); print('\n'.join('- '+e for e in errors)); return 1
    print('CI workflows OK'); return 0
if __name__=='__main__': raise SystemExit(main())
