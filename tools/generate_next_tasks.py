#!/usr/bin/env python3
"""Generate advisory tasks for the registered post-terminal evaluation program."""
from __future__ import annotations

import posixpath
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs/planning/next-actions.md"
OUT_REPO_PATH = "docs/planning/next-actions.md"
STATUS = "docs/project-status.md"
HISTORICAL_STATUS = "docs/reports/project-status-generated.md"
GAP = "docs/reports/research-gap-report.md"
PROGRAM = "docs/governance/post-terminal-public-evaluation-program-v1.0.md"

TASKS = [
    {
        "id": "STRATEGIC-006",
        "workstream": "PTE-W1-INDEPENDENT-REVIEW",
        "priority": "high",
        "title": "Prepare independent terminal-theorem proof review",
        "why": "`POST-TERM-EVAL-001` names independent proof review as the next post-terminal workstream. The review package must expose the exact theorem, frozen premises, dependency audit, mechanization boundary, nonclaims, reviewer prior exposure, conflicts, tools, checked obligations, and unresolved concerns without allowing project-authored adjudication to masquerade as independence.",
        "affected": [
            "docs/governance/post-terminal-public-evaluation-program-v1.0.md",
            "docs/research/upp-w15-terminal-theorem-v1.0.md",
            "docs/audits/upp-w15-terminal-theorem-audit.md",
        ],
        "outcome": "A review-ready immutable package and disclosure contract that permits an independent reviewer to accept, reject, narrow, or leave obligations Unknown without changing the theorem by review convention.",
        "risk": "high",
        "branch": "research/pte-w1-independent-review",
        "pr": "Prepare PTE-W1 independent proof review package",
    },
    {
        "id": "STRATEGIC-007",
        "workstream": "PTE-W2-KERNEL-RECONSTRUCTION",
        "priority": "queued",
        "title": "Attempt end-to-end kernel-checked reconstruction",
        "why": "The terminal semantic composition is executable and audited but is not one kernel-checked proof object. The registered objective is a complete proof-assistant reconstruction or an explicit obstruction report, with every external assumption identified rather than silently trusted.",
        "affected": [
            "docs/governance/post-terminal-public-evaluation-program-v1.0.md",
            "docs/research/upp-w15-terminal-theorem-v1.0.md",
            "docs/audits/upp-w15-terminal-theorem-audit.md",
            "docs/governance/theorem-proof-status-register.md",
        ],
        "outcome": "Either one end-to-end kernel-checked representation of the terminal composition or a reproducible obstruction record that narrows exactly what remains outside the proof kernel.",
        "risk": "high",
        "branch": "research/pte-w2-kernel-reconstruction",
        "pr": "Attempt PTE-W2 kernel reconstruction",
    },
    {
        "id": "STRATEGIC-008",
        "workstream": "PTE-W3-COUNTERMODEL-SEARCH",
        "priority": "queued",
        "title": "Run adversarial countermodel and scope challenge",
        "why": "Post-terminal evaluation must actively attack class membership, admissibility, faithfulness, machinery closure, equivalence, component necessity, construction sufficiency, independence, maximality, and terminal composition. Failed attacks are evidence; unresolved attacks remain Unknown.",
        "affected": [
            "docs/governance/post-terminal-public-evaluation-program-v1.0.md",
            "docs/governance/limitations-register.md",
            "docs/governance/open-problems-register.md",
            "docs/governance/counterexample-register.md",
        ],
        "outcome": "A prospectively scoped challenge record preserving successful countermodels, failed challenges, unresolved cases, and exact claim impact without treating survival as unrestricted confirmation.",
        "risk": "high",
        "branch": "research/pte-w3-countermodel-search",
        "pr": "Execute PTE-W3 countermodel challenge",
    },
    {
        "id": "STRATEGIC-009",
        "workstream": "PTE-W4-EMPIRICAL-REPLICATION",
        "priority": "external-dependency",
        "title": "Prepare independent bounded replication",
        "why": "The registered replication channel requires genuinely independent execution under a frozen protocol. Project-authored or same-implementation-path runs cannot be relabeled as independent and cannot establish the deductive theorem by themselves.",
        "affected": [
            "docs/governance/post-terminal-public-evaluation-program-v1.0.md",
            "docs/doctrine/isolation-classification.md",
            "docs/validation/README.md",
        ],
        "outcome": "A bounded replication package whose protocol, evaluator independence, provenance, deviations, negative results, and claim boundary are fixed before outcome interpretation.",
        "risk": "high",
        "branch": "research/pte-w4-independent-replication",
        "pr": "Prepare PTE-W4 independent replication package",
    },
]


def repository_link(path: str) -> str:
    """Return a repository-relative Markdown link without reading the target file."""
    href = posixpath.relpath(path, posixpath.dirname(OUT_REPO_PATH))
    return f"[{path}]({href})"


def nav_links() -> list[str]:
    return [
        f"- README Command Center: {repository_link('README.md')}",
        f"- Current Project Status: {repository_link(STATUS)}",
        f"- Post-Terminal Program: {repository_link(PROGRAM)}",
        f"- Historical Bounded Status: {repository_link(HISTORICAL_STATUS)}",
        f"- Research Gaps: {repository_link(GAP)}",
        f"- Next Actions: {repository_link(OUT_REPO_PATH)}",
    ]


def main() -> int:
    ids = [task["id"] for task in TASKS]
    workstreams = [task["workstream"] for task in TASKS]
    assert len(ids) == len(set(ids))
    assert len(workstreams) == len(set(workstreams))
    assert workstreams[0] == "PTE-W1-INDEPENDENT-REVIEW"

    lines = [
        "# Next Actions",
        "",
        "## Navigation",
        "",
        *nav_links(),
        "",
        "Generated by `python tools/generate_next_tasks.py` from the registered post-terminal evaluation program.",
        "",
        "Program: `POST-TERM-EVAL-001`.",
        "",
        "The `POST-TUE-UPP-001` deductive queue is closed. There is no `UPP-W16`. These tasks evaluate the existing terminal result; they do not authorize a stronger theorem, broader target class, weaker premise set, or silent evidence-status upgrade.",
        "",
        "Canonical next workstream: `PTE-W1-INDEPENDENT-REVIEW`.",
        "",
        "## Ranked Next Actions",
        "",
    ]

    for task in TASKS:
        affected = [repository_link(path) for path in task["affected"]]
        lines += [
            f"### {task['id']}: {task['title']}",
            "",
            f"- Registered workstream: `{task['workstream']}`",
            f"- Source: {repository_link(PROGRAM)}",
            f"- Priority: {task['priority']}",
            f"- Why it matters: {task['why']}",
            "- Affected authority/evidence surfaces:",
            *[f"  - {item}" for item in affected],
            f"- Expected outcome: {task['outcome']}",
            f"- Risk level: {task['risk']}",
            f"- Suggested branch name: `{task['branch']}`",
            f"- Suggested PR title: `{task['pr']}`",
            "",
        ]

    lines += [
        "## Maintainer Boundaries",
        "",
        "- Read `AGENTS.md` and the Research Execution Charter before execution.",
        "- `PTE-W1-INDEPENDENT-REVIEW` is the canonical next workstream; later workstreams are listed because the registered program defines them, not because all are ready for immediate execution.",
        "- Preserve the terminal theorem exactly while evaluating it. A confirmed defect requires claim-impact handling, scope reduction, revision, or retraction through governance.",
        "- Preserve failed challenges, failed reconstructions, negative results, ambiguity, protocol deviations, and `Unknown`.",
        "- Do not classify internal or same-path replication as independent.",
        "- Do not begin a stronger deductive program without separate prospective registration.",
        "",
        "Validation commands:",
        "",
        "- `make research-check`",
        "- `make docs-check`",
        "- `make health-fast`",
        "",
        "## Navigation",
        "",
        *nav_links(),
    ]

    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"{OUT.relative_to(ROOT)} tasks={len(TASKS)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
