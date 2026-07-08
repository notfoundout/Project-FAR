#!/usr/bin/env python3
"""Detect advisory research gaps without changing Project FAR theory."""
from __future__ import annotations
from pathlib import Path
import re, yaml
from collections import Counter
from report_link_utils import existing_file, markdown_line_link

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs/reports/research-gap-report.md'
REG=[ROOT/'theory/evaluation/evidence-registry.yaml',ROOT/'theory/evaluation/external-validation-registry.yaml',ROOT/'theory/falsification/adversarial-test-suite.yaml',ROOT/'theory/falsification/primitive-pressure-registry.yaml']
REPORT_DIRS=[ROOT/'docs',ROOT/'theory']

def load(p):
    with p.open(encoding='utf-8') as f: return yaml.safe_load(f) or {}
def ent(d): return d.get('entries') or d.get('tests') or []
def add(gaps, typ, loc, sev, action, line=None):
    gaps.append({'type':typ,'location':loc,'severity':sev,'action':action,'line':line})
def linked_location(g):
    loc=str(g['location'])
    if existing_file(loc):
        return markdown_line_link(loc, OUT, g.get('line'))
    return f'`{loc}`'
def norm(s): return str(s or '').lower()

def main():
    data={str(p):load(p) for p in REG}; gaps=[]
    evidence=ent(data[str(REG[0])]); external=ent(data[str(REG[1])]); adv=ent(data[str(REG[2])]); pressure=data[str(REG[3])].get('primitives',[])
    for e in evidence+external:
        ident=e.get('id','unknown')
        if 'unresolved' in norm(e.get('registry_resolution')) or 'unresolved' in norm(e.get('analysis_status')):
            add(gaps,'unresolved case',ident,'medium','Review the case and decide whether it remains unresolved, is outside scope, or needs a conservative-extension report.')
        if 'provisional' in norm(e.get('confidence')) or 'provisional' in norm(e.get('review_status')):
            add(gaps,'provisional system',ident,'medium','Perform human review and update confidence only if evidence warrants it.')
        if 'candidate primitive' in norm(e.get('classification')):
            add(gaps,'candidate primitive failure',ident,'critical','Human review required before any primitive-level conclusion or theory change.')
        rep=e.get('report')
        if rep and not (ROOT/rep).exists(): add(gaps,'missing analysis report',rep,'high','Create or correct the referenced analysis report after human approval.')
    for a in adv:
        ident=a.get('id','unknown')
        if 'unresolved' in norm(a.get('current_status')): add(gaps,'unresolved case',ident,'medium','Review adversarial test status and document next validation step.')
        if 'candidate primitive' in norm(a.get('current_status')): add(gaps,'candidate primitive failure',ident,'critical','Escalate to human theory review; do not modify primitives automatically.')
    for p in pressure:
        prim=p.get('primitive','unknown')
        if p.get('candidate_primitive_failures'): add(gaps,'candidate primitive failure',prim,'critical','Human theory review required for recorded candidate primitive failures.')
        if p.get('unresolved_pressures'): add(gaps,'unresolved primitive pressure',prim,'high','Analyze unresolved pressure before promoting stronger sufficiency claims.')
        if int(p.get('number_of_tests_stressing_it') or 0) < 2: add(gaps,'low primitive coverage',prim,'medium','Add human-approved adversarial coverage for this primitive.')
    domains=Counter(e.get('domain','unspecified') for e in external)
    for domain,count in domains.items():
        if count < 2: add(gaps,'underrepresented external-validation domain',domain,'medium','Consider adding at least one additional external validation system for this domain.')
    for status,count in Counter(e.get('classification','') for e in evidence+external).items():
        if 'conservative extension' in norm(status) and count>=3: add(gaps,'conservative-extension cluster',status,'medium','Review cluster for recurring policy needs without assuming primitive failure.')
    reports=set(str(p.relative_to(ROOT)) for p in sorted((ROOT/'theory/evaluation/external-systems').glob('*.md')))
    registered=set(e.get('report') for e in external if e.get('report'))
    for r in sorted(reports-registered): add(gaps,'missing registry entry for report',r,'medium','Decide whether this report should be entered in the external validation registry.')
    for p in [ROOT/'README.md', ROOT/'docs/reports/project-far-v0.3.0-synthesis.md', ROOT/'docs/project-status.md']:
        if p.exists():
            for lineno, line in enumerate(p.read_text(encoding='utf-8').splitlines(), 1):
                if 'latest' in line.lower() and re.search(r'v0\.[0-3]\.', line):
                    add(gaps,'stale latest-release reference',str(p.relative_to(ROOT)),'high','Review release wording against current release baseline.', lineno)
                    break
    pat=re.compile(r'\b(TODO|TBD|unresolved|future work)\b', re.I)
    for base in REPORT_DIRS:
        for p in sorted(base.rglob('*.md')):
            rel=str(p.relative_to(ROOT))
            if rel in {'docs/reports/project-status-generated.md','docs/reports/research-gap-report.md','docs/planning/next-actions.md'}:
                continue
            text=p.read_text(encoding='utf-8', errors='ignore')
            match_line=next((i for i,line in enumerate(text.splitlines(),1) if pat.search(line)), None)
            if match_line: add(gaps,'TODO/future-work note',rel,'low','Review note and decide whether it blocks validation.', match_line)
    lines=['# Research Gap Report','', 'Generated by `python tools/detect_research_gaps.py`. Findings are advisory and require human review.','', '| Gap ID | Type | Location | Severity | Recommended Action |','|---|---|---|---|---|']
    for i,g in enumerate(gaps,1): lines.append(f"| <a id=\"gap-{i:03d}\"></a>GAP-{i:03d} | {g['type']} | {linked_location(g)} | {g['severity']} | {g['action']} |")
    OUT.parent.mkdir(parents=True, exist_ok=True); OUT.write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print(f"{OUT.relative_to(ROOT)} gaps={len(gaps)}")
    return 0
if __name__=='__main__': raise SystemExit(main())
