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
        {'id':'STRATEGIC-001','gap':None,'priority':'high','title':'Plan independent replication of CRE-002-EXT-001','why':'CRE-002-EXT-001 is a positive prospective bounded result, but all encodings, compilers, lowerers, and verifiers remain repository-authored. Independent replication is now the primary evidential bottleneck.','affected':[markdown_link(ROOT / 'docs/methodology/adversarial-evaluation.md', OUT), markdown_link(ROOT / 'docs/governance/central-research-program.md', OUT), markdown_link(ROOT / 'docs/reports/cre002-ext001-evidence-analysis.md', OUT)],'outcome':'A preregistered replication plan with independent encoders or compiler implementations, isolation rules, provenance requirements, frozen acceptance criteria, and explicit nonclaims.','risk':'high','branch':'research/plan-cre002-ext001-independent-replication','pr':'Plan independent CRE-002-EXT-001 replication'},
        {'id':'STRATEGIC-002','gap':None,'priority':'high','title':'Design a boundary-focused CRE-003','why':'The extension passed only a bounded registered scenario with five derived constructs. A new prospective experiment should target capabilities and failure modes outside that exact grammar without reusing the same acceptance path.','affected':[markdown_link(ROOT / 'theory/evaluation/comparative-representation', OUT), markdown_link(ROOT / 'docs/ROADMAP.md', OUT), markdown_link(ROOT / 'docs/reports/cre002-ext001-evidence-analysis.md', OUT)],'outcome':'A boundary-focused preregistration that attempts to falsify adequacy outside CRE-002-EXT-001 while preserving the current result unchanged.','risk':'high','branch':'research/design-cre003-boundary-test','pr':'Design CRE-003 boundary test'},
        {'id':'STRATEGIC-003','gap':None,'priority':'medium','title':'Audit comparative representation cost','why':'CRE-002-EXT-001 showed behavioral completion for all three vocabularies but did not measure complexity, derived-machinery burden, or encoding cost, so it supports no ranking.','affected':[markdown_link(ROOT / 'docs/reports/cre002-ext001-evidence-analysis.md', OUT), markdown_link(ROOT / 'theory/evaluation/comparative-representation', OUT)],'outcome':'A preregistered cost model separating primitive count, derived constructs, semantic clauses, lowering rules, trace size, and implementation assumptions without converting cost into unsupported superiority claims.','risk':'medium','branch':'research/audit-comparative-representation-cost','pr':'Audit comparative representation cost'},
        {'id':'STRATEGIC-004','gap':None,'priority':'medium','title':'Preserve semantic and result drift locks','why':'Baseline 1.1, the original CRE-002 result, the CRE-002-EXT-001 scientific package, and its generated result must remain historically distinct and reproducible.','affected':[markdown_link(ROOT / 'theory/evaluation/comparative-representation/semantics/vocabulary-semantics-baseline-1.1.json', OUT), markdown_link(ROOT / 'theory/evaluation/comparative-representation/experiments/CRE-002-EXT-001', OUT)],'outcome':'Regression checks continue to detect semantic, checksum, chronology, generated-result, and claim-boundary drift.','risk':'medium','branch':'maintenance/monitor-cre002-ext001-drift','pr':'Monitor CRE-002-EXT-001 drift'},
        {'id':'STRATEGIC-005','gap':None,'priority':'medium','title':'Prepare the next evidence release','why':'The current v0.4.0 release predates the prospective CRE-002 and CRE-002-EXT-001 evidence sequence. A later release should package the evidence without strengthening theory claims.','affected':[markdown_link(ROOT / 'docs/releases', OUT), markdown_link(ROOT / 'docs/project-status.md', OUT), markdown_link(ROOT / 'docs/reports/cre002-ext001-evidence-analysis.md', OUT)],'outcome':'A release-readiness plan that records CRE-002 and CRE-002-EXT-001 chronology, supported conclusions, limitations, and independent-replication requirements.','risk':'medium','branch':'release/prepare-post-cre002-evidence-release','pr':'Prepare post-CRE-002 evidence release'},
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
        tasks=[{'id':'STRATEGIC-999','gap':None,'priority':'low','title':'Review generated status report','why':'Keep advisory planning current.','affected':[markdown_link(STATUS, OUT)],'outcome':'Human confirms planner output remains aligned with evidence.','risk':'low','branch':'maintenance/review-generated-status','pr':'Review generated Project FAR status'}]
    ids=[t['id'] for t in tasks]
    if len(ids)!=len(set(ids)):
        raise ValueError('generated task identifiers must be unique')
    lines=['# Next Actions','', '## Navigation','', *nav_links(OUT), '', f'Generated by `python tools/generate_next_tasks.py` from {markdown_link(STATUS, OUT)} and {markdown_link(GAP, OUT)}. These recommendations are advisory only and do not authorize theory changes.','', '## Ranked Next Actions','']
    for t in tasks:
        source=(f"- Source gap: {source_gap_link(t['gap'])}" if t.get('gap') else '- Source: strategic roadmap priority')
        lines += [f"### {t['id']}: {t['title']}",'',source,f"- Priority: {t['priority']}",f"- Why it matters: {t['why']}","- Affected files:",*[f"  - {a}" for a in t['affected']],f"- Expected outcome: {t['outcome']}",f"- Risk level: {t['risk']}",f"- Suggested branch name: `{t['branch']}`",f"- Suggested PR title: `{t['pr']}`",'']
    lines += ['## Maintainer Task Briefs','']
    for t in tasks[:5]:
        allowed=', '.join(t['affected'])
        source=(f"Source gap: {source_gap_link(t['gap'])}" if t.get('gap') else 'Source: strategic roadmap priority')
        lines += [f"### Task brief for {t['id']}",'','```markdown',f"Create branch `{t['branch']}`.",'',f"Scope: {t['title']}. This is advisory planning or documentation only.",source,f"Allowed files: {allowed}, generated reports, and planning documentation directly needed for this review.",'Forbidden files: primitives, definitions, axioms, theorem statements, proof objects, parser behavior, reasoning-engine behavior, metadata schemas, and evaluation conclusions.','Validation commands:','- `python tools/self_advancement_plan.py`','- `python tools/repo_health_check.py --fast` if available',f"PR title: {t['pr']}",'Stop condition: stop before any theory change; request human review if the work would alter accepted theory or conclusions.','```','']
    lines += ['', '## Navigation', '', *nav_links(OUT)]
    OUT.parent.mkdir(parents=True, exist_ok=True); OUT.write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print(f"{OUT.relative_to(ROOT)} tasks={len(tasks)}")
    return 0
if __name__=='__main__': raise SystemExit(main())
