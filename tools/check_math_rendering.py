#!/usr/bin/env python3
import re
from pathlib import Path
from common_health import iter_files, markdown_links, is_ignored_link, strip_anchor, rel
errors=[]; warnings=[]
for path in iter_files({'.md'}):
    lines=path.read_text(encoding='utf-8', errors='replace').splitlines()
    dollar=None; bracket=None; fence=None
    for i,line in enumerate(lines,1):
        s=line.strip()
        if s.startswith('```') and re.match(r'^```\s*(math|tex|latex)\s*$', s, re.I):
            fence = None if fence else i; continue
        if fence and s.startswith('```'): fence=None; continue
        if s == '$$': dollar = None if dollar else i
        if r'\[' in line: bracket = i if bracket is None else bracket
        if r'\]' in line and bracket is not None: bracket=None
        if line.count('$') == 1 and re.search(r'(^|\s)\$\S', line) and not re.search(r'\$\d', line):
            warnings.append((path,i,'possible unmatched inline math delimiter','Use paired $...$ or escape literal dollars.'))
        for ln,target,is_img,alt in markdown_links(line):
            if is_img and any(k in (alt+' '+target).lower() for k in ['math','equation','latex','tex']):
                if not is_ignored_link(target):
                    clean=strip_anchor(target); resolved=(path.parent/clean).resolve()
                    if clean and not resolved.exists(): errors.append((path,i,'broken math-display image link',f'Fix or remove {target}.'))
    if dollar: errors.append((path,dollar,'unclosed $$ display math block','Add closing $$ on its own line.'))
    if bracket: errors.append((path,bracket,r'unclosed \[ display math block',r'Add matching \].'))
    if fence: errors.append((path,fence,'unclosed fenced math block','Add closing ``` fence.'))
for p,l,msg,fix in errors: print(f'FAIL {rel(p)}:{l}: {msg}. Suggested fix: {fix}')
for p,l,msg,fix in warnings: print(f'WARN {rel(p)}:{l}: {msg}. Suggested fix: {fix}')
if errors: raise SystemExit(1)
print('Math rendering checks OK')
