#!/usr/bin/env python3
"""Generate advisory next actions from generated status and gap reports."""
from __future__ import annotations
from pathlib import Path
import re
from report_link_utils import existing_file, markdown_link, relative_href

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs/planning/next-actions.md'
GAP=ROOT/'docs/reports/research-gap-report.md'
STATUS=ROOT/'docs/reports/project-status-generated.md'
SEV={'critical':0,'high':1,'medium':2,'low':3}
GAP_ID_RE=re.compile(r'(GAP-\d{3})')
LINK_RE=re.compile(r'\[([^\]]+)\]\(([^)]+)\)')

def parse_gaps():
    rows=[]
    if not GAP.exists(): return rows
    for line in GAP.read_text(encoding='utf-8').splitlines():
        if not line.startswith('| ') or 'GAP-' not in line: continue
        parts=[p.strip() for p in line.strip('|').split('|')]
        if len(parts)>=5:
            m=GAP_ID_RE.search(parts[0])
            if m: rows.append(dict(id=m.group(1), type=parts[1], loc=parts[2], sev=parts[3], action=parts[4]))
    return rows

def source_gap_link(gap_id):
    return f"[{gap_id}]({relative_href(GAP, OUT)}#gap-{gap_id.split('-')[1].lower()})"

def affected_links(loc):
    m=LINK_RE.search(loc)
    if m:
        label=m.group(1).split(':L')[0]
        target=(GAP.parent / m.group(2).split('#',1)[0]).resolve()
        return [markdown_link(target, OUT, label)]
    clean=loc.strip('`')
    if existing_file(clean):
        return [markdown_link(clean, OUT)]
    return [f'`{clean}`']

def task_from_gap(g):
    slug=re.sub(r'[^a-z0-9]+','-',g['type'].lower()).strip('-')[:40]
    clean_title=re.sub(r'<[^>]+>','',g['loc'])
    return {
      'id': 'TASK-'+g['id'].split('-')[-1], 'gap': g['id'], 'priority': g['sev'],
      'title': f"Review {g['type']} at {clean_title}", 'why': g['action'],
      'affected': affected_links(g['loc']), 'outcome': 'Human-reviewed resolution plan or advisory documentation update; no automatic theory change.',
      'risk': 'high' if g['sev'] in ('critical','high') else 'medium' if g['sev']=='medium' else 'low',
      'branch': f"maintenance/review-{slug}-{g['id'].lower()}",
      'pr': f"Review {g['type']} ({g['id']})"
    }

def strategic_tasks():
    return [
        {'id':'TASK-001','gap':'GAP-001','priority':'high','title':'Freeze independent formal semantics for each official vocabulary','why':'CRE-001 established deterministic compatibility through compiler-local vocabulary interpretations, but formally licensed vocabulary semantics remain not established.','affected':[markdown_link(ROOT / 'theory/evaluation/comparative-representation/experiments/CRE-001/vocabularies/vocabulary-A.md', OUT), markdown_link(ROOT / 'theory/evaluation/comparative-representation/experiments/CRE-001/vocabularies/vocabulary-B.md', OUT), markdown_link(ROOT / 'theory/evaluation/comparative-representation/experiments/CRE-001/vocabularies/vocabulary-C.md', OUT)],'outcome':'Independently frozen semantics plan or artifact set that does not strengthen CRE-001 conclusions without evidence.','risk':'high','branch':'research/freeze-vocabulary-semantics','pr':'Freeze official vocabulary semantics'},
        {'id':'TASK-002','gap':'GAP-002','priority':'high','title':'Design and preregister CRE-002','why':'A prospective follow-up is required before independent comparative evidence can be analyzed beyond the deterministic CRE-001 implementation.','affected':[markdown_link(ROOT / 'theory/evaluation/comparative-representation', OUT), markdown_link(ROOT / 'docs/ROADMAP.md', OUT)],'outcome':'Preregistered CRE-002 design preserving all CRE-001 limitations.','risk':'high','branch':'research/preregister-cre-002','pr':'Design and preregister CRE-002'},
        {'id':'TASK-003','gap':'GAP-003','priority':'high','title':'Execute CRE-002 prospectively','why':'Prospective execution is needed to collect evidence not already fixed by deterministic CRE-001 artifacts.','affected':[markdown_link(ROOT / 'theory/evaluation/comparative-representation', OUT)],'outcome':'Prospective CRE-002 execution records under the frozen preregistered protocol.','risk':'high','branch':'research/execute-cre-002','pr':'Execute CRE-002 prospectively'},
        {'id':'TASK-004','gap':'GAP-004','priority':'medium','title':'Analyze prospective CRE-002 evidence','why':'Prospective records must be analyzed before any new comparative conclusion is considered.','affected':[markdown_link(ROOT / 'docs/reports', OUT), markdown_link(ROOT / 'theory/evaluation/comparative-representation', OUT)],'outcome':'Cautious analysis that states supported and unsupported conclusions.','risk':'medium','branch':'research/analyze-cre-002-evidence','pr':'Analyze prospective CRE-002 evidence'},
        {'id':'TASK-005','gap':'GAP-005','priority':'medium','title':'Plan independent replication','why':'Deterministic CRE-001 repository integration is not independent replication.','affected':[markdown_link(ROOT / 'docs/methodology/adversarial-evaluation.md', OUT), markdown_link(ROOT / 'docs/governance/central-research-program.md', OUT)],'outcome':'Replication plan with isolation, provenance, and limitation language.','risk':'medium','branch':'research/plan-independent-replication','pr':'Plan independent replication'},
    ]

def nav_links(out_path: Path) -> list[str]:
    return [
        f"- README Command Center: {markdown_link(ROOT / 'README.md', out_path)}",
        f"- Project Status: {markdown_link(ROOT / 'docs/reports/project-status-generated.md', out_path)}",
        f"- Research Gaps: {markdown_link(ROOT / 'docs/reports/research-gap-report.md', out_path)}",
        f"- Next Actions: {markdown_link(ROOT / 'docs/planning/next-actions.md', out_path)}",
    ]


def main():
    gaps=parse_gaps(); gaps.sort(key=lambda g:(SEV.get(g['sev'],9), g['id']))
    tasks=strategic_tasks() + [task_from_gap(g) for g in gaps[:15]]
    if not tasks:
        tasks=[{'id':'TASK-999','gap':'GAP-001','priority':'low','title':'Review generated status report','why':'Keep advisory planning current.','affected':[markdown_link(STATUS, OUT)],'outcome':'Human confirms planner output remains aligned with evidence.','risk':'low','branch':'maintenance/review-generated-status','pr':'Review generated Project FAR status'}]
    lines=['# Next Actions','', '## Navigation','', *nav_links(OUT), '', f'Generated by `python tools/generate_next_tasks.py` from {markdown_link(STATUS, OUT)} and {markdown_link(GAP, OUT)}. These recommendations are advisory only and do not authorize theory changes.','', '## Ranked Next Actions','']
    for t in tasks:
        lines += [f"### {t['id']}: {t['title']}",'',f"- Source gap: {source_gap_link(t['gap'])}",f"- Priority: {t['priority']}",f"- Why it matters: {t['why']}","- Affected files:",*[f"  - {a}" for a in t['affected']],f"- Expected outcome: {t['outcome']}",f"- Risk level: {t['risk']}",f"- Suggested branch name: `{t['branch']}`",f"- Suggested PR title: `{t['pr']}`",'']
    lines += ['## Maintainer Task Briefs','']
    for t in tasks[:5]:
        allowed=', '.join(t['affected'])
        lines += [f"### Task brief for {t['id']}",'','```markdown',f"Create branch `{t['branch']}`.",'',f"Scope: {t['title']}. This is advisory planning or documentation only.",f"Source gap: {source_gap_link(t['gap'])}",f"Allowed files: {allowed}, generated reports, and planning documentation directly needed for this review.",'Forbidden files: primitives, definitions, axioms, theorem statements, proof objects, parser behavior, reasoning-engine behavior, metadata schemas, and evaluation conclusions.','Validation commands:','- `python tools/self_advancement_plan.py`','- `python tools/repo_health_check.py --fast` if available',f"PR title: {t['pr']}",'Stop condition: stop before any theory change; request human review if the work would alter accepted theory or conclusions.','```','']
    lines += ['', '## Navigation', '', *nav_links(OUT)]
    OUT.parent.mkdir(parents=True, exist_ok=True); OUT.write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print(f"{OUT.relative_to(ROOT)} tasks={len(tasks)}")
    return 0
if __name__=='__main__': raise SystemExit(main())
