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
            'title':'Resolve the formal role of P8',
            'why':'THM-TARGET-001 and FAITHFUL-REP-001 freeze all three P8 clauses, but THM-CORE-REP-001 remains blocked until coordinate, side_condition, or split is selected and justified.',
            'affected':[
                markdown_link(ROOT / 'docs/research/faithful-representation-specification-v1.0.md', OUT),
                markdown_link(ROOT / 'docs/research/thm-target-001-v1.0.md', OUT),
                markdown_link(ROOT / 'docs/research/preservation-basis-investigation-v1.0.md', OUT),
                markdown_link(ROOT / 'docs/research/pb001-execution-run-001-report.md', OUT),
                markdown_link(ROOT / 'theory/evaluation/thm-target-001.json', OUT),
            ],
            'outcome':'A versioned theorem-facing P8 decision selecting one frozen mode, recording theorem and application effects, and leaving every representation claim unproved.',
            'risk':'high','branch':'research/resolve-p8-theorem-role','pr':'Resolve P8 theorem role'
        },
        {
            'id':'STRATEGIC-002','priority':'high',
            'title':'Build the S_core construction and obstruction ledger',
            'why':'After P8 is selected, every finite-core source feature needs either a uniform FARA construction lemma or a registered obstruction before the theorem can be attempted.',
            'affected':[
                markdown_link(ROOT / 'docs/research/faithful-representation-specification-v1.0.md', OUT),
                markdown_link(ROOT / 'docs/research/thm-target-001-v1.0.md', OUT),
                markdown_link(ROOT / 'docs/research/independent-reasoning-definition-v1.0.md', OUT),
                markdown_link(ROOT / 'docs/planning/deduction-first-proof-roadmap.md', OUT),
            ],
            'outcome':'A dependency-ordered lemma ledger for S_core covering configuration, commitments, alternatives, grounds, dynamics, consequences, history, self-modification, uncertainty, and composition.',
            'risk':'high','branch':'research/build-s-core-lemma-ledger','pr':'Build S_core construction and obstruction ledger'
        },
        {
            'id':'STRATEGIC-003','priority':'high',
            'title':'Prove formal negative-control lemmas',
            'why':'FAITHFUL-REP-001 assigns NC-01 through NC-10 to exact failure predicates, but those expected failures must be proved rather than inferred from the definitions.',
            'affected':[
                markdown_link(ROOT / 'docs/research/faithful-representation-specification-v1.0.md', OUT),
                markdown_link(ROOT / 'docs/methodology/negative-control-suite-v1.0.md', OUT),
                markdown_link(ROOT / 'theory/falsification', OUT),
                markdown_link(ROOT / 'docs/planning/deduction-first-proof-roadmap.md', OUT),
            ],
            'outcome':'A formal control-lemma family giving each mandatory negative control a source-valid construction and a derivation of its registered faithfulness failure.',
            'risk':'high','branch':'research/prove-faithful-negative-controls','pr':'Prove faithful-representation negative-control lemmas'
        },
        {
            'id':'STRATEGIC-004','priority':'medium',
            'title':'Develop the first uniform S_core constructor',
            'why':'The common-schema and representation theorems require one effective source-isomorphism-equivariant constructor, not a collection of hand-built mappings.',
            'affected':[
                markdown_link(ROOT / 'docs/research/faithful-representation-specification-v1.0.md', OUT),
                markdown_link(ROOT / 'docs/research/thm-target-001-v1.0.md', OUT),
                markdown_link(ROOT / 'frameworks/FARA/architecture.md', OUT),
                markdown_link(ROOT / 'theory/evaluation/thm-target-001-premise-ledger.json', OUT),
            ],
            'outcome':'A constructor definition and witness schema for the ordinary finite core, with all helper machinery declared and no theorem claim until its obligations are proved.',
            'risk':'high','branch':'research/build-s-core-constructor','pr':'Develop uniform S_core constructor'
        },
        {
            'id':'STRATEGIC-005','priority':'medium',
            'title':'Prepare proof mechanization architecture',
            'why':'Machine checking will require a declared trusted base, formal encodings of S_core, A_FARA, FAITHFUL-REP-001, the selected P8 mode, theorem dependencies, and admitted-obligation policy.',
            'affected':[
                markdown_link(ROOT / 'mechanization', OUT),
                markdown_link(ROOT / 'docs/research/faithful-representation-specification-v1.0.md', OUT),
                markdown_link(ROOT / 'docs/research/thm-target-001-v1.0.md', OUT),
                markdown_link(ROOT / 'docs/planning/deduction-first-proof-roadmap.md', OUT),
            ],
            'outcome':'A proof-assistant selection and encoding plan that does not claim machine verification before theorem lemmas and dependencies are proved.',
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
    lines=['# Next Actions','', '## Navigation','', *nav_links(OUT), '', 'Generated by `python tools/generate_next_tasks.py` under the deduction-first strategic priority. THM-TARGET-001 and FAITHFUL-REP-001 are frozen; research gaps remain available in the gap report but do not automatically enter the active central queue. These recommendations do not authorize unregistered theory changes.','', '## Ranked Next Actions','']
    for t in tasks:
        lines += [f"### {t['id']}: {t['title']}",'','- Source: deduction-first strategic priority',f"- Priority: {t['priority']}",f"- Why it matters: {t['why']}",'- Affected files:',*[f"  - {a}" for a in t['affected']],f"- Expected outcome: {t['outcome']}",f"- Risk level: {t['risk']}",f"- Suggested branch name: `{t['branch']}`",f"- Suggested PR title: `{t['pr']}`",'']
    lines += ['## Maintainer Task Briefs','']
    for t in tasks:
        allowed=', '.join(t['affected'])
        lines += [f"### Task brief for {t['id']}",'','```markdown',f"Create branch `{t['branch']}`.",'',f"Scope: {t['title']}.",'Source: deduction-first strategic priority.',f"Primary files: {allowed}.",'Preserve THM-TARGET-001, FAITHFUL-REP-001, all frozen evidence, failures, unknowns, and nonclaims. A material source-scope, target-structure, faithful-predicate, theorem-family, or P8-content change requires a versioned revision.','Do not claim a theorem, universality, necessity, minimality, mechanized verification, or independent validation unless the corresponding research gate contains evidence.','Validation commands:','- `make research-check`','- `make health-fast`',f"PR title: `{t['pr']}`",'Stop condition: stop when the scoped artifact is complete or when a formal obstruction requires a separately registered revision.','```','']
    lines += ['', '## Navigation', '', *nav_links(OUT)]
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text('\n'.join(lines)+'\n',encoding='utf-8')
    print(f"{OUT.relative_to(ROOT)} tasks={len(tasks)}")
    return 0


if __name__=='__main__': raise SystemExit(main())
