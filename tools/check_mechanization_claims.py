#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
BANNED=['fully mechanized','general semantic inference','machine-verified formal proof']
def main():
    errors=[]
    for p in [ROOT/'README.md', ROOT/'docs/project-status.md', ROOT/'docs/reports/project-status-generated.md']:
        if not p.exists(): continue
        for i,line in enumerate(p.read_text(encoding='utf-8',errors='ignore').splitlines(),1):
            low=line.lower()
            for b in BANNED:
                if b in low and not any(q in low for q in ['unsupported', 'does not', 'not perform', 'not provide', 'remain absent', 'not machine-verified', 'machine-verified formal proofs remain absent']): errors.append(f'{p.relative_to(ROOT)}:{i}: unsupported mechanization claim: {b}')
    if errors:
        print('MECHANIZATION CLAIM CHECK FAILED'); print('\n'.join('- '+e for e in errors)); return 1
    print('Mechanization claims OK'); return 0
if __name__=='__main__': raise SystemExit(main())
