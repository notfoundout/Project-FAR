#!/usr/bin/env python3
"""Scan high-risk maturity phrases and flag clear unqualified overstatements."""
from __future__ import annotations
import re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
TERMS=re.compile(r'\b(machine-verified|machine verified|production-ready|fully mechanized|independent validation)\b',re.I)
QUAL=re.compile(
    r'\b(not |unsupported|requires|future|unknown|unexecuted|separate|distinguishes|not independent|no current|checks and challenges|strengthens confidence)\b',
    re.I,
)
def main():
    findings=[]
    for base in ['README.md','docs','theory']:
        root=ROOT/base
        paths=[root] if root.is_file() else sorted(root.rglob('*.md'))
        for p in paths:
            rel=p.relative_to(ROOT).as_posix()
            for i,line in enumerate(p.read_text(encoding='utf-8',errors='ignore').splitlines(),1):
                if TERMS.search(line) and not QUAL.search(line):
                    if rel.startswith('docs/doctrine/') or rel.startswith('docs/reports/p') or rel.startswith('docs/reports/t') or rel in {'docs/reports/external-validation-terminology-review.md','docs/reports/theorem-substance-and-assurance-review.md'}:
                        continue
                    findings.append(f'{rel}:{i}: {line.strip()[:160]}')
    if findings:
        print('CLAIMS AUDIT FOUND UNQUALIFIED HIGH-RISK CLAIMS')
        for f in findings[:80]: print('- '+f)
        return 1
    print('Claims audit OK'); return 0
if __name__=='__main__': raise SystemExit(main())
