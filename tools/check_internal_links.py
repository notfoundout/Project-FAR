#!/usr/bin/env python3
from pathlib import Path
import re
from urllib.parse import unquote
from common_health import ROOT, iter_files, markdown_links, is_ignored_link, strip_anchor, rel, HEADING_RE

CHECK_EXTS = {'.md','.png','.svg','.pdf','.tex','.yaml','.yml','.json'}
HTML_ANCHOR_RE = re.compile(r'<a\s+(?:[^>]*\s+)?(?:id|name)=["\']?([^"\'\s>]+)', re.I)
ADVISORY_LINE_ANCHOR_SOURCES = {
    (ROOT / 'docs/reports/research-gap-report.md').resolve(),
}
# Authenticated historical bytes are evidence snapshots, not live documentation. Their
# relative links intentionally refer to the historical tree and must not be repaired or
# followed against the current tree; byte identity is enforced by the audit source locks.
FROZEN_EVIDENCE_ROOTS = {
    (ROOT / 'research/theory-dependency-audit/frozen-source-v1.0').resolve(),
}

def slugify(text: str) -> str:
    text = re.sub(r'[`*_~\[\]()]+', '', text.strip().lower())
    text = re.sub(r'[^a-z0-9 -]', '', text)
    return re.sub(r'\s+', '-', text).strip('-')

def anchors_for(path: Path):
    anchors=set()
    if path.suffix.lower() != '.md' or not path.exists():
        return anchors
    text=path.read_text(encoding='utf-8', errors='replace')
    for line in text.splitlines():
        m=HEADING_RE.match(line)
        if m: anchors.add(slugify(m.group(2)))
        anchors.update(a.lower() for a in HTML_ANCHOR_RE.findall(line))
    return anchors

def anchor_part(target: str) -> str:
    return unquote(target.split('#',1)[1].split('?',1)[0]) if '#' in target else ''

def is_frozen_evidence(path: Path) -> bool:
    resolved = path.resolve()
    return any(resolved == root or root in resolved.parents for root in FROZEN_EVIDENCE_ROOTS)

errors=[]
warnings=[]
for path in iter_files({'.md','.yaml','.yml'}):
    if is_frozen_evidence(path):
        continue
    text = path.read_text(encoding='utf-8', errors='replace')
    for line, target, is_img, _alt in markdown_links(text):
        if is_ignored_link(target):
            continue
        clean = unquote(strip_anchor(target))
        if not clean:
            continue
        resolved = (path.parent / clean).resolve()
        should_check = Path(clean).suffix.lower() in CHECK_EXTS or clean.endswith('/') or '/' in clean or is_img
        if should_check and not resolved.exists():
            errors.append((path,line,target,f'missing {rel(resolved)}'))
            continue
        anchor=anchor_part(target)
        if anchor and resolved.exists() and resolved.suffix.lower() == '.md':
            if re.fullmatch(r'L\d+', anchor):
                line_no=int(anchor[1:])
                total=len(resolved.read_text(encoding='utf-8', errors='replace').splitlines())
                if line_no < 1 or line_no > total:
                    item=(path,line,target,f'line anchor outside 1..{total}')
                    if path.resolve() in ADVISORY_LINE_ANCHOR_SOURCES:
                        # The research-gap report is a generated advisory snapshot. Its
                        # observed line number is provenance, not a stable document
                        # identity. The generator now emits path-only hrefs for these
                        # observations; tolerate pre-regeneration line drift while still
                        # requiring the target file itself to exist. All other Markdown
                        # line anchors remain fail-closed.
                        warnings.append(item)
                    else:
                        errors.append(item)
            elif anchor.lower() not in anchors_for(resolved):
                errors.append((path,line,target,'missing anchor'))
if warnings:
    print('Advisory generated-line drift:')
    for p,l,t,msg in warnings:
        print(f'WARN {rel(p)}:{l}: {t} -> {msg}')
if errors:
    print('Broken internal links:')
    for p,l,t,msg in errors:
        print(f'{rel(p)}:{l}: {t} -> {msg}')
    raise SystemExit(1)
print('Internal links OK')
