#!/usr/bin/env python3
"""Generate the active deduction-first strategic task queue."""
from __future__ import annotations
from pathlib import Path
from report_link_utils import markdown_link

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs/planning/next-actions.md"
STATUS = ROOT / "docs/reports/project-status-generated.md"
GAP = ROOT / "docs/reports/research-gap-report.md"

TASKS = [
    {
        "id": "STRATEGIC-001",
        "priority": "high",
        "title": "Build the S_core construction and obstruction ledger",
        "why": "THM-TARGET-001, FAITHFUL-REP-001, and P8-DEC-001 are frozen. Every finite-core source feature now needs either a uniform FARA construction obligation or a registered obstruction before the theorem can be attempted.",
        "affected": [
            "docs/research/faithful-representation-specification-v1.0.md",
            "docs/research/p8-theorem-role-decision-v1.0.md",
            "docs/research/thm-target-001-v1.0.md",
            "docs/research/independent-reasoning-definition-v1.0.md",
            "docs/planning/deduction-first-proof-roadmap.md",
        ],
        "outcome": "A dependency-ordered lemma ledger for S_core covering configuration, commitments, alternatives, grounds, dynamics, consequences, history, internal evidential status, self-modification, uncertainty, distribution, and composition.",
        "risk": "high",
        "branch": "research/build-s-core-lemma-ledger",
        "pr": "Build S_core construction and obstruction ledger",
    },
    {
        "id": "STRATEGIC-002",
        "priority": "high",
        "title": "Prove faithful-representation negative-control lemmas",
        "why": "FAITHFUL-REP-001 assigns NC-01 through NC-10 to exact failure predicates, but the expected failures remain proof obligations rather than established results.",
        "affected": [
            "docs/research/faithful-representation-specification-v1.0.md",
            "docs/methodology/negative-control-suite-v1.0.md",
            "theory/falsification",
            "docs/planning/deduction-first-proof-roadmap.md",
        ],
        "outcome": "A formal lemma family giving each mandatory negative control a source-valid construction and a derivation of its registered faithfulness failure.",
        "risk": "high",
        "branch": "research/prove-faithful-negative-controls",
        "pr": "Prove faithful-representation negative-control lemmas",
    },
    {
        "id": "STRATEGIC-003",
        "priority": "high",
        "title": "Develop the first uniform S_core constructor",
        "why": "The common-schema and faithful-representation theorems require one effective source-isomorphism-equivariant constructor, not unrelated hand-built mappings.",
        "affected": [
            "docs/research/faithful-representation-specification-v1.0.md",
            "docs/research/p8-theorem-role-decision-v1.0.md",
            "docs/research/thm-target-001-v1.0.md",
            "frameworks/FARA/architecture.md",
            "theory/evaluation/thm-target-001-premise-ledger.json",
        ],
        "outcome": "A constructor definition and witness schema for the ordinary finite core, with every helper operation and internal evidential-status mapping declared and counted.",
        "risk": "high",
        "branch": "research/build-s-core-constructor",
        "pr": "Develop uniform S_core constructor",
    },
    {
        "id": "STRATEGIC-004",
        "priority": "medium",
        "title": "Register S_core countermodel fixtures",
        "why": "Construction work must be attacked concurrently with source-valid cases targeting uniformity, dynamics, dependency, history, provenance, composition, and hidden-interpreter assumptions.",
        "affected": [
            "docs/research/faithful-representation-specification-v1.0.md",
            "docs/research/p8-theorem-role-decision-v1.0.md",
            "docs/methodology/negative-control-suite-v1.0.md",
            "theory/falsification",
        ],
        "outcome": "A registered fixture family classified as S_core countermodels, impossibility witnesses, representation failures, controls, or scope-boundary cases.",
        "risk": "high",
        "branch": "research/register-s-core-countermodels",
        "pr": "Register S_core countermodel fixtures",
    },
    {
        "id": "STRATEGIC-005",
        "priority": "medium",
        "title": "Prepare proof mechanization architecture",
        "why": "Machine checking requires a declared trusted base, formal encodings of S_core, A_FARA, FAITHFUL-REP-001, the split P8 obligations, theorem dependencies, and an admitted-obligation policy.",
        "affected": [
            "mechanization",
            "docs/research/faithful-representation-specification-v1.0.md",
            "docs/research/p8-theorem-role-decision-v1.0.md",
            "docs/research/thm-target-001-v1.0.md",
            "docs/planning/deduction-first-proof-roadmap.md",
        ],
        "outcome": "A proof-assistant selection and encoding plan preserving the separation between Faithful_split and Corr_8E without making a machine-verification claim.",
        "risk": "medium",
        "branch": "research/plan-proof-mechanization",
        "pr": "Plan deduction-first proof mechanization",
    },
]


def nav_links() -> list[str]:
    return [
        f"- README Command Center: {markdown_link(ROOT / 'README.md', OUT)}",
        f"- Project Status: {markdown_link(STATUS, OUT)}",
        f"- Research Gaps: {markdown_link(GAP, OUT)}",
        f"- Next Actions: {markdown_link(OUT, OUT)}",
    ]


def main() -> int:
    ids = [task["id"] for task in TASKS]
    if len(ids) != len(set(ids)):
        raise ValueError("generated task identifiers must be unique")
    lines = [
        "# Next Actions", "", "## Navigation", "", *nav_links(), "",
        "Generated by `python tools/generate_next_tasks.py` under the deduction-first strategic priority. THM-TARGET-001, FAITHFUL-REP-001, and P8-DEC-001 are frozen; research gaps remain available in the gap report but do not automatically enter the active central queue. These recommendations do not authorize unregistered theory changes.",
        "", "## Ranked Next Actions", "",
    ]
    for task in TASKS:
        affected = [markdown_link(ROOT / path, OUT) for path in task["affected"]]
        lines += [
            f"### {task['id']}: {task['title']}", "",
            "- Source: deduction-first strategic priority",
            f"- Priority: {task['priority']}",
            f"- Why it matters: {task['why']}",
            "- Affected files:",
            *[f"  - {item}" for item in affected],
            f"- Expected outcome: {task['outcome']}",
            f"- Risk level: {task['risk']}",
            f"- Suggested branch name: `{task['branch']}`",
            f"- Suggested PR title: `{task['pr']}`",
            "",
        ]
    lines += ["## Maintainer Task Briefs", ""]
    for task in TASKS:
        lines += [
            f"### Task brief for {task['id']}", "",
            "```markdown",
            f"Create branch `{task['branch']}`.",
            f"Scope: {task['title']}.",
            "Preserve THM-TARGET-001, FAITHFUL-REP-001, P8-DEC-001, all frozen evidence, failures, unknowns, and nonclaims.",
            "Do not claim a theorem, universality, necessity, minimality, mechanized verification, actual-process correspondence, or independent validation without registered evidence.",
            "Validation commands:",
            "- `make research-check`",
            "- `make health-fast`",
            f"PR title: `{task['pr']}`",
            "```",
            "",
        ]
    lines += ["## Navigation", "", *nav_links()]
    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"{OUT.relative_to(ROOT)} tasks={len(TASKS)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
