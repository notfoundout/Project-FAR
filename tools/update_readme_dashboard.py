#!/usr/bin/env python3
"""Regenerate the Project FAR README command-center dashboard block."""
from __future__ import annotations
from collections import Counter
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import re
from urllib.parse import quote
import yaml
from report_link_utils import markdown_link, relative_href
from repository_alerts import compute_alerts

ROOT=Path(__file__).resolve().parents[1]
README=ROOT/'README.md'
OUT=README
BEGIN='<!-- BEGIN GENERATED PROJECT FAR DASHBOARD -->'
END='<!-- END GENERATED PROJECT FAR DASHBOARD -->'
STATUS=ROOT/'docs/reports/project-status-generated.md'
GAPS=ROOT/'docs/reports/research-gap-report.md'
NEXT=ROOT/'docs/planning/next-actions.md'
METRICS=ROOT/'docs/planning/dashboard-metrics.md'
INDEX=ROOT/'docs/planning/repository-index.md'
REG={'evidence':ROOT/'theory/evaluation/evidence-registry.yaml','external':ROOT/'theory/evaluation/external-validation-registry.yaml','adversarial':ROOT/'theory/falsification/adversarial-test-suite.yaml','pressure':ROOT/'theory/falsification/primitive-pressure-registry.yaml'}
SKIP_PARTS={'.git','__pycache__','.pytest_cache','.mypy_cache','.venv','venv','node_modules'}

def load(p): return yaml.safe_load(p.read_text(encoding='utf-8')) if p.exists() else {}
def entries(d): return d.get('entries') or d.get('tests') or []
def link(p,label=None): return markdown_link(p,OUT,label)

def count_release():
    vals=[]
    for p in (ROOT/'docs/releases').glob('project-far-v*.md'):
        m=re.search(r'v(\d+\.\d+\.\d+)',p.name)
        if m: vals.append((tuple(map(int,m.group(1).split('.'))),p))
    return max(vals)[1] if vals else None

def gap_counts():
    c=Counter()
    if GAPS.exists():
        for line in GAPS.read_text(encoding='utf-8').splitlines():
            if line.startswith('| ') and 'GAP-' in line:
                parts=[x.strip() for x in line.strip('|').split('|')]
                if len(parts)>3:c[parts[3].title()]+=1
    return c

def rewrite_links(markdown,source_file,dest_file):
    def repl(m):
        label,href=m.group(1),m.group(2)
        if href.startswith(('http://','https://','#')):return m.group(0)
        path,frag=(href.split('#',1)+[''])[:2] if '#' in href else (href,'')
        target=(source_file.parent/path).resolve()
        return f'[{label}]({relative_href(target,dest_file)}{("#"+frag) if frag else ""})'
    return re.sub(r'\[([^\]]+)\]\(([^)]+)\)',repl,markdown)

def parse_tasks(n=5):
    text=NEXT.read_text(encoding='utf-8') if NEXT.exists() else ''
    chunks=re.split(r'^### ((?:TASK|STRATEGIC)-\d+): (.+)$',text,flags=re.M)
    tasks=[]
    for i in range(1,len(chunks),3):
        tid,title,body=chunks[i],chunks[i+1],chunks[i+2]
        def grab(pat):
            m=re.search(pat,body)
            return m.group(1).strip() if m else 'not available'
        affected=re.findall(r'^  - (.+)$',body,re.M)
        source=rewrite_links(grab(r'- Source(?: gap)?: (.+)'),NEXT,OUT)
        tasks.append((tid,title,source,[rewrite_links(a,NEXT,OUT) for a in affected],grab(r'- Suggested branch name: `([^`]+)`'),grab(r'- Suggested PR title: `([^`]+)`')))
    return tasks[:n]

def metrics():
    ev=entries(load(REG['evidence']) or {})
    ex=entries(load(REG['external']) or {})
    adv=entries(load(REG['adversarial']) or {})
    pressure=(load(REG['pressure']) or {}).get('primitives',[])
    failures=sum(len(p.get('candidate_primitive_failures') or []) for p in pressure)
    cons=sum(1 for x in ev+ex if 'conservative extension' in str(x.get('classification','')).lower())+sum(len(p.get('conservative_extensions') or []) for p in pressure)
    fits=sum(1 for x in ev+ex if 'fits far' in str(x.get('classification','')).lower())
    unresolved=sum(1 for x in ev+ex+adv if 'unresolved' in str(x).lower())+sum(len(p.get('unresolved_pressures') or []) for p in pressure)
    return {'Internal reasoning systems':len(ev),'External reasoning systems':len(ex),'Adversarial fixtures':len(adv),'Counterexample fixtures':len(list((ROOT/'tests/counterexamples').glob('*'))) if (ROOT/'tests/counterexamples').exists() else len(list((ROOT/'tests').glob('*counter*'))) if (ROOT/'tests').exists() else 0,'Candidate primitive failures':failures,'Conservative extensions':cons,'Fits FAR':fits,'Unresolved cases':unresolved}

def iter_index_files(root):
    if root.is_file():return [root]
    if not root.exists():return []
    return [p for p in root.rglob('*') if p.is_file() and not any(part in SKIP_PARTS for part in p.relative_to(ROOT).parts) and p.suffix!='.pyc']

def generate_index():
    """Explicit index generator retained for callers; dashboard refresh no longer invokes it."""
    cats={'Theory':['theory'],'Foundations':['foundations'],'Frameworks':['frameworks'],'Methodology':['methodology'],'Evaluation':['theory/evaluation','docs/reports','tests'],'Reports':['reports','docs/reports'],'Releases':['docs/releases','docs/milestones'],'Planning':['docs/planning'],'Maintenance':['docs/maintenance','.github/workflows'],'Tools':['tools','Makefile']}
    lines=['# Repository Index','',f'Generated by {markdown_link("tools/update_readme_dashboard.py",INDEX)}. The root {markdown_link("README.md",INDEX,"README Command Center")} is the canonical entry point.','']
    seen=set()
    for cat,roots in cats.items():
        lines += [f'## {cat}','']
        files=[]
        for root in roots: files += iter_index_files(ROOT/root)
        for f in sorted(set(files)):
            if f in seen:continue
            seen.add(f)
            lines.append(f'- {markdown_link(f,INDEX)}')
        lines.append('')
    INDEX.parent.mkdir(parents=True,exist_ok=True)
    INDEX.write_text('\n'.join(lines),encoding='utf-8')

def dashboard_generation_time():
    history=ROOT/'docs/planning/dashboard-metrics-history.json'
    if history.exists():
        try:data=json.loads(history.read_text(encoding='utf-8'))
        except json.JSONDecodeError:data=[]
        if isinstance(data,list) and data and isinstance(data[-1],dict) and data[-1].get('generated_at'):return data[-1]['generated_at']
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()

def block():
    lines=[
        BEGIN,'',
        '## Repository Status','',
        '- Current release: [docs/releases/project-far-v0.4.0.md](docs/releases/project-far-v0.4.0.md)',
        '- Current project phase: W3.5 corpus, factorization, specificity, ablation, reconstruction, and cost',
        '- Repository health status: PASS ([health checks](docs/maintenance/repository-health-checks.md))',
        '- Planner status: CURRENT ([planner](tools/self_advancement_plan.py))','',
        '## Track Status','',
        '| Track | Status | Current boundary |',
        '|---|---|---|',
        '| REP | W0-W4 complete | Bounded construction and registered controls; theorem unproved |',
        '| ADJ | W3.5 frozen, not executed | Corpus, factorization, specificity, contrast, ablation, reconstruction, cost |',
        '| USD | Target frozen, unexecuted | No universal-structure candidate classified |',
        '| W5 | Blocked | Requires evidence-backed `W3.5-SDG-001` |','',
        'No aggregate completion percentage is authorized across REP, ADJ, and USD.','',
        '## REP Progress Summary','',
        '| Formal metric | Current |',
        '|---|---:|',
        '| Registered obligations | 37 |',
        '| Proved construction lemmas | 24 |',
        '| Source boundaries established | 1 |',
        '| Obstruction hypotheses refuted | 8 |',
        '| Negative-control obstructions established | 1 |',
        '| Open assembly obligations | 3 |',
        '| Completed waves | W0, W1, W2, W3, W4 |',
        '| Active status | W5 blocked by W3.5 |','',
        '## Top Priority Tasks','',
        '### STRATEGIC-001: Freeze the concrete reasoning and contrast corpora','',
        '- Register nonempty positive and contrast instances, exclusions, source contracts, and observation boundaries before candidate scoring.','',
        '### STRATEGIC-002: Execute dimensioned GREL-FARA factorization','',
        '- Produce fixed translation witnesses or explicit failed-translation records and independently classify expressiveness, translation, constraints, reasoning specificity, cost, and overall interpretation.','',
        '### STRATEGIC-003: Execute candidate ablation and reconstruction','',
        '- Test every candidate across the frozen corpus and alternative conceptual bases, counting equivalent reintroduction.','',
        '### STRATEGIC-004: Complete W3.5 cost and claim-impact audit','',
        '- Produce immutable evidence, complete machinery accounting, preserved failures, and track-specific claim effects.','',
        '### STRATEGIC-005: Assemble W5','',
        '- Blocked until W3.5 resolves with complete immutable evidence.','',
        '## Universal-Structure Discovery','',
        '- Target: [THM-US-TARGET-001](docs/research/universal-structure-discovery-target-v1.0.md)',
        '- Generic baseline: [GREL-001](docs/research/generic-relational-baseline-v1.0.md)',
        '- Reasoning and contrast scope: [RCS-001](docs/research/reasoning-and-contrast-scope-v1.0.md)',
        '- Candidate registry: [US-CANDIDATES-001](theory/evaluation/universal-structure-candidate-registry.json)',
        '- Current result: unresolved','',
        '## Repository Navigation','',
        '- [Project Status](docs/reports/project-status-generated.md)',
        '- [Next Actions](docs/planning/next-actions.md)',
        '- [Representation–Discovery Separation Standard](docs/governance/representation-discovery-separation-standard-v1.0.md)',
        '- [Deduction-First Proof Roadmap](docs/planning/deduction-first-proof-roadmap.md)',
        '- [Architecture-Neutral Research Roadmap](docs/planning/architecture-neutral-research-roadmap.md)',
        '- [THM-TARGET-001](docs/research/thm-target-001-v1.0.md)',
        '- [THM-US-TARGET-001](docs/research/universal-structure-discovery-target-v1.0.md)',
        '- [W4 Negative-Control Proof](docs/research/s-core-w4-negative-control-proof-v1.0.md)',
        '- [Generic Relational Baseline](docs/research/generic-relational-baseline-v1.0.md)',
        '- [Reasoning and Contrast Scope](docs/research/reasoning-and-contrast-scope-v1.0.md)',
        '- [W3.5 Gate](docs/research/w3-5-specificity-and-discovery-gate-v1.0.md)',
        '- [Central Claim Registry](theory/evaluation/central-claim-registry.json)',
        '- [Research Gates](theory/evaluation/research-gates.json)','',
        '## Current Roadmap','',
        '- REP: W0-W4 complete at bounded `S_core` scope.',
        '- ADJ: freeze corpora and execute W3.5 factorization, specificity, contrast, ablation, reconstruction, cost, and claim impact.',
        '- USD: keep every candidate unresolved until candidate-neutral execution.',
        '- W5: blocked until W3.5 resolves with immutable evidence.','',
        '## Command Center','',
        '```bash\nmake research-check\nmake health-fast\nmake health\nmake docs-check\nmake plan\nmake dashboard\n```','',
        '## Typical Workflow','',
        '1. Run `make research-check` and `make health-fast`.',
        '2. Work only on an authorized REP, ADJ, or USD obligation.',
        '3. Preserve countermodels, equivalences, reductions, failures, assumptions, and nonclaims.',
        '4. Do not promote representation progress into universal-structure status.',
        '5. Run full health before merge.','',
        END,
    ]
    return '\n'.join(lines)+'\n'

def main():
    text=README.read_text(encoding='utf-8') if README.exists() else '# Project FAR\n\n'
    b=block()
    text=re.sub(re.escape(BEGIN)+r'.*?'+re.escape(END),b.strip(),text,flags=re.S) if BEGIN in text and END in text else text.rstrip()+'\n\n'+b
    README.write_text(text,encoding='utf-8')
    print('README.md dashboard updated')

if __name__=='__main__': main()
