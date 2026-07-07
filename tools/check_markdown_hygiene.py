#!/usr/bin/env python3
import re
from collections import defaultdict
from common_health import iter_files, rel, HEADING_RE
errors=[]; warnings=[]
for path in iter_files({'.md'}):
    lines=path.read_text(encoding='utf-8', errors='replace').splitlines()
    fence=None; headings=defaultdict(list); table_counts=[]
    for i,line in enumerate(lines,1):
        if line.strip().startswith('```'): fence = None if fence else i
        m=HEADING_RE.match(line)
        if m: headings[re.sub(r'[^a-z0-9 -]','',m.group(2).lower()).replace(' ','-')].append(i)
        if re.search(r'\[[^\]]*\]\(\s*\)', line): errors.append((path,i,'empty Markdown link'))
        if re.search(r'!\[\s*\]\(', line): warnings.append((path,i,'image link without alt text'))
        if '|' in line and not line.lstrip().startswith('```'):
            cells=line.strip().strip('|').count('|')+1
            if cells>1: table_counts.append((i,cells,line))
    if fence: errors.append((path,fence,'unclosed code fence'))
    for slug,locs in headings.items():
        if slug and len(locs)>1: warnings.append((path,locs[1],f'duplicate heading anchor: {slug}'))
    # conservative table check: consecutive pipe rows must match counts
    block=[]
    for i,c,_ in table_counts+[(10**9,0,'')]:
        if block and i != block[-1][0]+1:
            counts={x[1] for x in block}
            if len(block)>=2 and len(counts)>1:
                errors.append((path,block[0][0],'malformed Markdown table with inconsistent column counts'))
            block=[]
        if i<10**9: block.append((i,c))
for p,l,msg in errors: print(f'FAIL {rel(p)}:{l}: {msg}')
for p,l,msg in warnings: print(f'WARN {rel(p)}:{l}: {msg}')
if errors: raise SystemExit(1)
print('Markdown hygiene OK')
