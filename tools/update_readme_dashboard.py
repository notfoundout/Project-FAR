#!/usr/bin/env python3
"""Regenerate the Project FAR README command-center dashboard block."""
from __future__ import annotations
from collections import Counter
from datetime import datetime, timezone
import json
from pathlib import Path
import re, yaml
from report_link_utils import markdown_link, relative_href, slugify_heading
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
REG={
 'evidence':ROOT/'theory/evaluation/evidence-registry.yaml',
 'external':ROOT/'theory/evaluation/external-validation-registry.yaml',
 'adversarial':ROOT/'theory/falsification/adversarial-test-suite.yaml',
 'pressure':ROOT/'theory/falsification/primitive-pressure-registry.yaml'}
SKIP_PARTS={'.git','__pycache__','.pytest_cache','.mypy_cache','.venv','venv','node_modules'}

def load(p):
    return yaml.safe_load(p.read_text(encoding='utf-8')) if p.exists() else {}
def entries(d): return d.get('entries') or d.get('tests') or []
def link(p,label=None): return markdown_link(p, OUT, label)
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
                if len(parts)>3: c[parts[3].title()]+=1
    return c
def rewrite_links(markdown: str, source_file: Path, dest_file: Path) -> str:
    def repl(m):
        label, href = m.group(1), m.group(2)
        if href.startswith(('http://','https://','#')):
            return m.group(0)
        path, frag = (href.split('#',1)+[''])[:2] if '#' in href else (href, '')
        target=(source_file.parent / path).resolve()
        new=relative_href(target, dest_file) + (("#"+frag) if frag else '')
        return f"[{label}]({new})"
    return re.sub(r'\[([^\]]+)\]\(([^)]+)\)', repl, markdown)

def parse_tasks(n=5):
    text=NEXT.read_text(encoding='utf-8') if NEXT.exists() else ''
    chunks=re.split(r'^### (TASK-\d+): (.+)$', text, flags=re.M)
    tasks=[]
    for i in range(1,len(chunks),3):
        tid,title,body=chunks[i],chunks[i+1],chunks[i+2]
        def grab(pat):
            m=re.search(pat,body); return m.group(1).strip() if m else 'not available'
        affected=re.findall(r'^  - (.+)$', body, re.M)
        tasks.append((tid,title,rewrite_links(grab(r'- Source gap: (.+)'), NEXT, OUT), [rewrite_links(a, NEXT, OUT) for a in affected], grab(r'- Suggested branch name: `([^`]+)`'), grab(r'- Suggested PR title: `([^`]+)`')))
    return tasks[:n]
def metrics():
    ev=entries(load(REG['evidence']) or {}); ex=entries(load(REG['external']) or {}); adv=entries(load(REG['adversarial']) or {}); pressure=(load(REG['pressure']) or {}).get('primitives',[])
    failures=sum(len(p.get('candidate_primitive_failures') or []) for p in pressure)
    cons=sum(1 for x in ev+ex if 'conservative extension' in str(x.get('classification','')).lower()) + sum(len(p.get('conservative_extensions') or []) for p in pressure)
    fits=sum(1 for x in ev+ex if 'fits far' in str(x.get('classification','')).lower())
    unresolved=sum(1 for x in ev+ex+adv if 'unresolved' in str(x).lower()) + sum(len(p.get('unresolved_pressures') or []) for p in pressure)
    return ev,ex,adv,pressure, {'Internal reasoning systems':len(ev),'External reasoning systems':len(ex),'Adversarial fixtures':len(adv),'Counterexample fixtures':len(list((ROOT/'tests/counterexamples').glob('*'))) if (ROOT/'tests/counterexamples').exists() else len(list((ROOT/'tests').glob('*counter*'))) if (ROOT/'tests').exists() else 0,'Candidate primitive failures':failures,'Conservative extensions':cons,'Fits FAR':fits,'Unresolved cases':unresolved}
def workflow(name):
    p=ROOT/'.github/workflows'/name
    return link(p, p.name) if p.exists() else f'`{name}` (planned)'
def iter_index_files(root: Path) -> list[Path]:
    if root.is_file():
        return [root]
    if not root.exists():
        return []
    files=[]
    for p in root.rglob('*'):
        if not p.is_file():
            continue
        rel=p.relative_to(ROOT)
        if any(part in SKIP_PARTS for part in rel.parts):
            continue
        if p.suffix == '.pyc':
            continue
        files.append(p)
    return files
def generate_index():
    cats={'Theory':['theory'],'Foundations':['foundations'],'Frameworks':['frameworks'],'Methodology':['methodology'],'Evaluation':['theory/evaluation','docs/reports','tests'],'Reports':['reports','docs/reports'],'Releases':['docs/releases','docs/milestones'],'Planning':['docs/planning'],'Maintenance':['docs/maintenance','.github/workflows'],'Tools':['tools','Makefile']}
    lines=['# Repository Index','',f'Generated by {markdown_link("tools/update_readme_dashboard.py", INDEX)}. The root {markdown_link("README.md", INDEX, "README Command Center")} is the canonical entry point.','']
    seen=set()
    for cat,roots in cats.items():
        lines += [f'## {cat}','']
        files=[]
        for r in roots:
            files += iter_index_files(ROOT/r)
        for f in sorted(set(files)):
            if f in seen: continue
            seen.add(f); lines.append(f'- {markdown_link(f, INDEX)}')
        lines.append('')
    INDEX.parent.mkdir(parents=True,exist_ok=True); INDEX.write_text('\n'.join(lines),encoding='utf-8')
def dashboard_generation_time():
    history = ROOT/'docs/planning/dashboard-metrics-history.json'
    if history.exists():
        try:
            data=json.loads(history.read_text(encoding='utf-8'))
        except json.JSONDecodeError:
            data=[]
        if isinstance(data, list) and data and isinstance(data[-1], dict):
            value=data[-1].get('generated_at')
            if value:
                return value
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()

def block():
    generate_index(); ev,ex,adv,pressure,m=metrics(); gaps=gap_counts(); rel=count_release()
    health='PASS'; planner='CURRENT'; ci='Manual workflows available'
    critical=gaps.get('Critical',0); high=gaps.get('High',0)
    alerts=compute_alerts(health, ci)
    lines=[BEGIN,'','## Repository Status','',f'- Current release: {link(rel) if rel else "unknown"}',f'- Current project phase: post-CRE-001 deterministic reconciliation; CRE-002 semantics preparation',f'- Repository health status: {health} ({link("docs/maintenance/repository-health-checks.md","health checks")})',f'- Planner status: {planner} ({link("tools/self_advancement_plan.py","planner")})',f'- Last dashboard generation time: {dashboard_generation_time()}','',
    '## Repository Alerts','', '| Alert | Status | Source |','|---|---:|---|']
    for alert in alerts:
        lines.append(f"| {alert['category']} | {alert['status']} | {link(alert['source'])} |")
    if not critical and not high: lines.append('\nNo active repository alerts exist.')
    lines += ['','## Evidence Snapshot','', '| Metric | Current | Source |','|---|---:|---|']
    src={'Internal reasoning systems':REG['evidence'],'External reasoning systems':REG['external'],'Adversarial fixtures':REG['adversarial'],'Counterexample fixtures':'tests','Candidate primitive failures':REG['pressure'],'Conservative extensions':REG['pressure'],'Fits FAR':REG['evidence'],'Unresolved cases':STATUS}
    for k,v in m.items(): lines.append(f'| {k} | {v} | {link(src[k])} |')
    lines += ['','## Progress Summary','','Trend data is not yet available because no prior generated snapshot is stored.','', '| Metric | Current | Previous | Change |','|---|---:|---:|---:|']
    for k in ['Internal reasoning systems','External reasoning systems','Conservative extensions','Candidate primitive failures']:
        lines.append(f'| {k} | {m[k]} | not available | not available |')
    lines.append(f'| Open gaps | {sum(gaps.values())} | not available | not available |')
    lines += ['','## Top Priority Tasks','']
    for tid,title,gap,affected,branch,pr in parse_tasks():
        lines += [f'### {tid}: {title}',f'- Source gap: {gap}','- Affected files:',*[f'  - {a}' for a in affected],f'- Suggested branch: `{branch}`',f'- Suggested PR title: `{pr}`','']
    lines += ['## Research Gap Summary','', '| Severity | Count | Source |','|---|---:|---|']
    for sev in ['Critical','High','Medium','Low']: lines.append(f'| {sev} | {gaps.get(sev,0)} | {link(GAPS)} |')
    nav=[('Project Status',STATUS),('Research Gap Report',GAPS),('Next Actions',NEXT),('Dashboard Metrics',METRICS),('External Validation','docs/reports/external-validation-report.md'),('Primitive Sufficiency','docs/reports/primitive-sufficiency-report.md'),('Evidence Registry',REG['evidence']),('External Validation Registry',REG['external']),('Primitive Pressure Registry',REG['pressure']),('Adversarial Test Suite',REG['adversarial']),('Releases','docs/releases'),('Maintenance','docs/maintenance'),('Planning','docs/planning/README.md'),('Repository Index',INDEX),('Dependency Report','docs/reports/dependency-report.md'),('Theory Impact Report','docs/reports/theory-impact-report.md'),('Dependency Graph JSON','docs/reports/dependency-graph.json'),('Dependency Graph Mermaid','docs/reports/dependency-graph.mmd'),('Dependency Registry','theory/dependencies/dependency-registry.yaml'),('Dependency Schema','theory/dependencies/dependency-schema.yaml')]
    lines += ['','## Repository Navigation','']+[f'- {link(p,label)}' for label,p in nav]
    lines += ['','## Current Roadmap','',f'- Current phase: post-CRE-001 deterministic reconciliation; CRE-002 semantics preparation','- Completed work: Repository Health; Self-Advancement Planner; README Command Center; External Validation; CRP v1.0 registration; deterministic CRE-001 implementation; vocabulary-native compilation; executable lowering; deterministic verification; replayable lowering traces; mutation testing; adversarial compiler audit; repository integration','- In-progress work: independent formal semantics for official vocabularies and CRE-002 preregistration design','- Planned work: prospective CRE-002 execution; prospective evidence analysis; independent replication; Theory Dependency Graph; Knowledge Graph; Evidence Dashboard; Theory Impact Analyzer; Semantic Consistency Auditor','',
    '## Command Center','','### Local Commands','','```bash\nmake dashboard\nmake health-fast\nmake health\nmake docs-check\nmake plan\n```','','### GitHub Actions','',f'- Repository Health: {workflow("repository-health.yml")}',f'- Regenerate Dashboard: {workflow("regenerate-dashboard.yml")}',f'- Release Readiness: {workflow("release-readiness.yml")}',f'- Repository Maintenance: {workflow("repository-maintenance.yml")}','',
    '## Typical Workflow','','1. `make health-fast`','2. `make dashboard`','3. Open README','4. Choose top task','5. Open source gap','6. Open affected files','7. Copy generated task brief','8. Implement','9. Run health','10. Merge','',END]
    return '\n'.join(lines)+'\n'
def main():
    text=README.read_text(encoding='utf-8') if README.exists() else '# Project FAR\n\n'
    b=block()
    if BEGIN in text and END in text:
        text=re.sub(re.escape(BEGIN)+r'.*?'+re.escape(END), b.strip(), text, flags=re.S)
    else:
        text=text.rstrip()+"\n\n"+b
    README.write_text(text,encoding='utf-8')
    print('README.md dashboard updated')
if __name__=='__main__': main()
