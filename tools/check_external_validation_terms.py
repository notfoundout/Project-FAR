#!/usr/bin/env python3
from __future__ import annotations
import re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def main():
    errors=[]
    for p in [ROOT/'README.md', ROOT/'docs/project-status.md', ROOT/'docs/reports/project-status-generated.md']:
        if not p.exists(): continue
        for i,line in enumerate(p.read_text(encoding='utf-8',errors='ignore').splitlines(),1):
            low=line.lower()
            if 'independent validation' in low and not any(q in low for q in ['not independent', 'requires', 'future', 'distinct']):
                errors.append(f'{p.relative_to(ROOT)}:{i}: unqualified independent validation claim')
    if errors:
        print('EXTERNAL VALIDATION TERMINOLOGY CHECK FAILED'); print('\n'.join('- '+e for e in errors)); return 1
    print('External-validation terminology OK'); return 0
if __name__=='__main__': raise SystemExit(main())
