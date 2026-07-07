#!/usr/bin/env python3
import re
from pathlib import Path
from common_health import ROOT, rel
errors=[]; warnings=[]
readme=ROOT/'README.md'
text=readme.read_text(encoding='utf-8', errors='replace') if readme.exists() else ''
release_docs=sorted([p for p in (ROOT/'docs/releases').glob('project-far-v*.md') if re.match(r'project-far-v\d+\.\d+\.\d+\.md$', p.name)], key=lambda p: [int(x) for x in re.findall(r'\d+', p.name)])
if not (ROOT/'docs/releases/project-far-v0.3.0.md').exists(): errors.append('missing docs/releases/project-far-v0.3.0.md')
if not (ROOT/'docs/releases/github-release-v0.3.0.md').exists(): errors.append('missing docs/releases/github-release-v0.3.0.md')
if release_docs:
    newest=release_docs[-1]
    tag=re.search(r'v\d+\.\d+\.\d+', newest.name).group(0)
    latest_section=re.search(r'(?is)(latest release|current release|release)[^\n]*(?:\n.{0,200}){0,8}', text)
    latest_text=latest_section.group(0) if latest_section else text[:2000]
    if tag not in latest_text:
        errors.append(f'README latest release section does not reference newest release {tag}')
    if 'v0.2.0' in latest_text and tag != 'v0.2.0':
        errors.append('README latest release text appears to describe v0.2.0 as latest')
    for m in re.finditer(r'\]\(([^)]*(?:docs/releases/[^)]*|/releases/tag/[^)]*))\)', text):
        target=m.group(1)
        if target.startswith('docs/releases/') and not (ROOT/target.split('#')[0]).exists(): errors.append(f'README release link missing: {target}')
        if '/releases/tag/' in target and tag not in target: warnings.append(f'README historical release tag link: {target}')
    for p in (ROOT/'docs/releases').glob('*.md'):
        t=p.read_text(encoding='utf-8', errors='replace')
        if p.name != newest.name and re.search(r'latest release[^\n]*v0\.2\.0', t, re.I) and tag != 'v0.2.0':
            warnings.append(f'ambiguous historical latest wording in {rel(p)}')
else:
    errors.append('no docs/releases/project-far-v*.md release docs found')
for e in errors: print('FAIL', e)
for w in warnings: print('WARN', w)
if errors: raise SystemExit(1)
print('Release consistency OK')
