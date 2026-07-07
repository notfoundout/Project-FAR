#!/usr/bin/env python3
import argparse
from collections import deque
from pathlib import Path
from common_health import ROOT, markdown_links, is_ignored_link, strip_anchor, rel, iter_files
parser=argparse.ArgumentParser(); parser.add_argument('--strict', action='store_true'); args=parser.parse_args()
roots=[ROOT/'README.md',ROOT/'docs/CANONICAL_MAP.md',ROOT/'docs/OVERVIEW.md',ROOT/'docs/project-status.md']
roots += list((ROOT/'frameworks').glob('*/README.md')) if (ROOT/'frameworks').exists() else []
roots += list((ROOT/'docs/releases').glob('*.md')) if (ROOT/'docs/releases').exists() else []
roots += list((ROOT/'docs').glob('**/*report*.md')) if (ROOT/'docs').exists() else []
scan_roots=['docs','theory','frameworks','foundations','methodology','research','papers']
all_docs={p.resolve() for p in iter_files({'.md'}, scan_roots) if 'archive' not in p.parts and 'orphan-ok' not in p.read_text(encoding='utf-8', errors='replace')}
seen=set(); q=deque([p.resolve() for p in roots if p.exists()])
while q:
    p=q.popleft()
    if p in seen or not p.exists() or p.suffix.lower()!='.md': continue
    seen.add(p)
    text=p.read_text(encoding='utf-8', errors='replace')
    for _,target,_,_ in markdown_links(text):
        if is_ignored_link(target): continue
        clean=strip_anchor(target)
        if not clean: continue
        r=(p.parent/clean).resolve()
        if r.is_dir(): r=r/'README.md'
        if r.exists() and r.suffix.lower()=='.md' and r not in seen: q.append(r)
orphans=sorted(all_docs-seen)
for p in orphans: print(f'WARN orphaned doc: {rel(p)}')
if args.strict:
    strict=[p for p in orphans if 'archive' not in p.parts]
    if strict: raise SystemExit(1)
print('Orphaned doc check completed')
