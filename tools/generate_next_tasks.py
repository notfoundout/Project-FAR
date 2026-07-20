#!/usr/bin/env python3
"""Generate the active deduction-first strategic task queue."""
from __future__ import annotations
from pathlib import Path
from report_link_utils import markdown_link

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'docs/planning/next-actions.md'
STATUS=ROOT/'docs/reports/project-status-generated.md'
GAP=ROOT/'docs/reports/research-gap-report.md'


def strategic_tasks():
    return [
        {
            'id':'STRATEGIC-001','priority':'high',
            'title':'Freeze THM-TARGET-001 and premise ledger',
            'why':'The central question cannot be proved or refuted until its source class, target structure, theorem family, assumptions, preservation obligations, P8 alternatives, failure conditions, and nonclaims are fixed.',
            'affected':[
                markdown_link(ROOT / 'docs/governance/deduction-first-research-standard.md', OUT),
                markdown_link(ROOT / 'docs/planning/deduction-first-proof-roadmap.md', OUT),
                markdown_link(ROOT / 'docs/research/independent-reasoning-definition-v1.0.md', OUT),
                markdown_link(ROOT / 'docs/research/preservation-basis-investigation-v1.0.md', OUT),
            ],
            'outcome':'A versioned THM-TARGET-001 artifact that states separate scoped existence, faithful-representation, necessity, minimality, equivalence, and impossibility obligations without claiming a proof.',
            'risk':'high','branch':'research/freeze-thm-target-001','pr':'Freeze THM-TARGET-001 theorem target and premise ledger'
        },
        {
            'id':'STRATEGIC-002','priority':'high',
            'title':'Formalize faithful representation and nontriviality',
            'why':'A representation theorem is vacuous unless the representation relation formally excludes label-only mappings, lookup tables, hidden interpreters, metadata smuggling, dependency collapse, history erasure, and evaluator repair.',
            'affected':[
                markdown_link(ROOT / 'docs/planning/deduction-first-proof-roadmap.md', OUT),
                markdown_link(ROOT / 'docs/research/preservation-basis-investigation-v1.0.md', OUT),
                markdown_link(ROOT / 'docs/methodology/negative-control-suite-v1.0.md', OUT),
            ],
            'outcome':'A frozen faithful-representation specification with explicit source and target objects, preservation clauses, conditional obligations, and formal nontriviality exclusions.',
            'risk':'high','branch':'research/formalize-faithful-representation','pr':'Formalize faithful representation and nontriviality'
        },
        {
            'id':'STRATEGIC-003','priority':'high',
            'title':'Resolve the formal role of P8',
            'why':'P8 remains unresolved as an ordinary preservation coordinate versus a cross-cutting evidential condition. A completed theorem cannot leave that distinction informal.',
            'affected':[
                markdown_link(ROOT / 'docs/research/preservation-basis-investigation-v1.0.md', OUT),
                markdown_link(ROOT / 'docs/research/pb001-execution-run-001-report.md', OUT),
                markdown_link(ROOT / 'docs/planning/deduction-first-proof-roadmap.md', OUT),
            ],
            'outcome':'A theorem-facing classification of P8 as a coordinate, theorem side condition, separate correspondence theorem, revision requirement, or explicit unresolved blocker.',
            'risk':'high','branch':'research/resolve-p8-theorem-role','pr':'Resolve P8 theorem role'
        },
        {
            'id':'STRATEGIC-004','priority':'medium',
            'title':'Develop construction and obstruction lemmas',
            'why':'The theorem program must build mappings for the ordinary finite core while simultaneously searching for self-modification, nonmonotonic, probabilistic, distributed, semantic-change, hidden-state, and open-ended countermodels.',
            'affected':[
                markdown_link(ROOT / 'docs/research/reasoning-domain-specification-v1.0.md', OUT),
                markdown_link(ROOT / 'docs/research/independent-reasoning-definition-v1.0.md', OUT),
                markdown_link(ROOT / 'docs/planning/deduction-first-proof-roadmap.md', OUT),
            ],
            'outcome':'A dependency-ordered lemma ledger in which every admitted source feature has a construction lemma or a registered obstruction.',
            'risk':'high','branch':'research/build-representation-lemmas','pr':'Develop representation construction and obstruction lemmas'
        },
        {
            'id':'STRATEGIC-005','priority':'medium',
            'title':'Prepare proof mechanization architecture',
            'why':'Machine checking will require a declared trusted base, formal encodings of the source and target classes, explicit axioms, theorem dependencies, and a policy for admitted obligations.',
            'affected':[
                markdown_link(ROOT / 'mechanization', OUT),
                markdown_link(ROOT / 'docs/governance/deduction-first-research-standard.md', OUT),
                markdown_link(ROOT / 'docs/planning/deduction-first-proof-roadmap.md', OUT),
            ],
            'outcome':'A proof-assistant selection and encoding plan that does not claim machine verification before the theorem statement and semantics are frozen.',
            'risk':'medium','branch':'research/plan-proof-mechanization','pr':'Plan deduction-first proof mechanization'
        },
    ]


def nav_links(out_path: Path) -> list[str]:
    return [
        f"- README Command Center: {markdown_link(ROOT / 'README.md', out_path)}",
        f"- Project Status: {markdown_link(STATUS, out_path)}",
        f"- Research Gaps: {markdown_link(GAP, out_path)}",
        f"- Next Actions: {markdown_link(OUT, out_path)}",
    ]


def main():
    tasks=strategic_tasks()
    ids=[t['id'] for t in tasks]
    if len(ids)!=len(set(ids)):
        raise ValueError('generated task identifiers must be unique')
    lines=['# Next Actions','', '## Navigation','', *nav_links(OUT), '', 'Generated by `python tools/generate_next_tasks.py` under the deduction-first strategic priority. Research gaps remain available in the gap report but do not automatically enter the active central queue. These recommendations do not authorize unregistered theory changes.','', '## Ranked Next Actions','']
    for t in tasks:
        lines += [f"### {t['id']}: {t['title']}",'','- Source: deduction-first strategic priority',f"- Priority: {t['priority']}",f"- Why it matters: {t['why']}",'- Affected files:',*[f"  - {a}" for a in t['affected']],f"- Expected outcome: {t['outcome']}",f"- Risk level: {t['risk']}",f"- Suggested branch name: `{t['branch']}`",f"- Suggested PR title: `{t['pr']}`",'']
    lines += ['## Maintainer Task Briefs','']
    for t in tasks:
        allowed=', '.join(t['affected'])
        lines += [f"### Task brief for {t['id']}",'','```markdown',f"Create branch `{t['branch']}`.",'',f"Scope: {t['title']}.",'Source: deduction-first strategic priority.',f"Primary files: {allowed}.",'Preserve all frozen evidence, failures, unknowns, and nonclaims. Do not silently modify Foundation, accepted primitives, axioms, or prior results. Any substantive theory change requires the registered versioned revision process.','Do not claim a theorem, universality, necessity, minimality, mechanized verification, or independent validation unless the corresponding research gate contains evidence.','Validation commands:','- `make research-check`','- `make health-fast`',f"PR title: `{t['pr']}`",'Stop condition: stop when the scoped artifact is complete or when a formal obstruction requires a separately registered revision.','```','']
    lines += ['', '## Navigation', '', *nav_links(OUT)]
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print(f"{OUT.relative_to(ROOT)} tasks={len(tasks)}")
    return 0


if __name__=='__main__': raise SystemExit(main())
