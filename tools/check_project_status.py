#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main():
    errors=[]
    status_files=[p for p in (ROOT/'docs').glob('*status*.md')]
    by={}
    for p in status_files: by.setdefault(p.name.lower(),[]).append(p)
    for group in by.values():
        if len(group)>1: errors.append('case-insensitive status path collision: '+', '.join(str(p.relative_to(ROOT)) for p in group))
    if not (ROOT/'docs/project-status.md').exists(): errors.append('missing canonical docs/project-status.md')
    if (ROOT/'docs/PROJECT_STATUS.md').exists(): errors.append('legacy docs/PROJECT_STATUS.md still exists')
    for p in ROOT.rglob('*.md'):
        if '.git' in p.parts: continue
        txt=p.read_text(encoding='utf-8',errors='ignore')
        if 'PROJECT_STATUS.md' in txt: errors.append(f'legacy PROJECT_STATUS.md link in {p.relative_to(ROOT)}')
    if errors:
        print('PROJECT STATUS CHECK FAILED'); print('\n'.join('- '+e for e in errors)); return 1
    print('Project status authority OK'); return 0
if __name__=='__main__': raise SystemExit(main())
