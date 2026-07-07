#!/usr/bin/env python3
from pathlib import Path
from common_health import ROOT, iter_files, markdown_links, is_ignored_link, strip_anchor, rel

CHECK_EXTS = {'.md','.png','.svg','.pdf','.tex','.yaml','.yml','.json'}
errors=[]
for path in iter_files({'.md','.yaml','.yml'}):
    text = path.read_text(encoding='utf-8', errors='replace')
    for line, target, is_img, _alt in markdown_links(text):
        if is_ignored_link(target):
            continue
        clean = strip_anchor(target)
        if not clean:
            continue
        resolved = (path.parent / clean).resolve()
        if Path(clean).suffix.lower() in CHECK_EXTS or clean.endswith('/') or '/' in clean or is_img:
            if not resolved.exists():
                errors.append((path,line,target,resolved))
if errors:
    print('Broken internal links:')
    for p,l,t,r in errors:
        print(f'{rel(p)}:{l}: {t} -> missing {rel(r)}')
    raise SystemExit(1)
print('Internal links OK')
