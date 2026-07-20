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
        "title": "Prove the W1 S_core base carriers and direct axes",
        "why": "SCORE-W0-PROOF-001 proves the source-normalization kernel. The next dependency is one target allocation schema plus direct P1, P2, P3, P4, P6, and P8-I preservation constructions or quantified obstructions.",
        "affected": [
            "docs/research/s-core-construction-obstruction-ledger-v1.0.md",
            "theory/evaluation/s-core-construction-obstruction-ledger.json",
            "frameworks/FARA/architecture.md",
            "frameworks/FARA/primitives.md",
            "docs/research/faithful-representation-specification-v1.0.md",
        ],
        "outcome": "A versioned proof-or-obstruction package resolving LEM-SC-005, LEM-SC-006, LEM-SC-007, LEM-SC-008, LEM-SC-009, LEM-SC-012, and LEM-SC-014 without hidden machinery or theorem promotion.",
        "risk": "high",
        "branch": "research/prove-s-core-w1-direct-axes",
        "pr": "Construct S_core W1 base carriers and direct axes",
    },
    {
        "id": "STRATEGIC-002",
        "priority": "high",
        "title": "Prove dynamics, history, and revision constructors",
        "why": "After W1, the finite-core theorem requires deterministic and finite-support probabilistic bisimulation, path and history reflection, nonmonotonic revision, and operational self-modification rather than labels alone.",
        "affected": [
            "docs/research/s-core-construction-obstruction-ledger-v1.0.md",
            "theory/evaluation/s-core-construction-obstruction-ledger.json",
            "docs/research/faithful-representation-specification-v1.0.md",
            "docs/research/independent-reasoning-definition-v1.0.md",
        ],
        "outcome": "Accepted W2 lemmas or quantified obstructions for LEM-SC-010, LEM-SC-011, LEM-SC-013, LEM-SC-015, and LEM-SC-016.",
        "risk": "high",
        "branch": "research/prove-s-core-w2-dynamics-history",
        "pr": "Construct S_core W2 dynamics history and revision",
    },
    {
        "id": "STRATEGIC-003",
        "priority": "high",
        "title": "Prove global witness obligations",
        "why": "Per-axis mappings do not establish faithfulness until recovery, semantic agreement, coherence, machinery accounting, uniformity, composition, and witness assembly are proved together.",
        "affected": [
            "docs/research/s-core-construction-obstruction-ledger-v1.0.md",
            "theory/evaluation/s-core-construction-obstruction-ledger.json",
            "docs/research/faithful-representation-specification-v1.0.md",
            "theory/evaluation/thm-target-001.json",
        ],
        "outcome": "Accepted W3 lemmas or quantified obstructions for LEM-SC-017 through LEM-SC-024.",
        "risk": "high",
        "branch": "research/prove-s-core-w3-global-witness",
        "pr": "Construct S_core W3 global witness obligations",
    },
    {
        "id": "STRATEGIC-004",
        "priority": "high",
        "title": "Execute the remaining obstruction and negative-control program",
        "why": "OBS-SC-001 is resolved only as a source boundary. Target construction must still survive quantified impossibility searches and NC-01 through NC-10; one failed witness is not a theorem-level obstruction.",
        "affected": [
            "docs/research/s-core-construction-obstruction-ledger-v1.0.md",
            "theory/evaluation/s-core-construction-obstruction-ledger.json",
            "docs/methodology/negative-control-suite-v1.0.md",
            "theory/falsification",
        ],
        "outcome": "Accepted obstruction, refutation, scope-boundary, or unresolved records for OBS-SC-002 through OBS-SC-010, including the formal negative-control family.",
        "risk": "high",
        "branch": "research/execute-s-core-obstructions",
        "pr": "Execute remaining S_core obstruction program",
    },
    {
        "id": "STRATEGIC-005",
        "priority": "high",
        "title": "Assemble the finite-core theorem or strongest obstruction",
        "why": "Only after all dependencies are resolved may ASM-SC-001 through ASM-SC-003 derive the common schema, arbitrary-episode witness, and strongest justified theorem-or-obstruction outcome.",
        "affected": [
            "docs/research/s-core-construction-obstruction-ledger-v1.0.md",
            "theory/evaluation/s-core-construction-obstruction-ledger.json",
            "theory/evaluation/thm-target-001.json",
            "theory/evaluation/central-claim-registry.json",
        ],
        "outcome": "A complete scoped theorem, formal countermodel, proper-subclass theorem, or explicit unresolved result with every remaining obligation named.",
        "risk": "high",
        "branch": "research/assemble-s-core-result",
        "pr": "Assemble S_core theorem or obstruction",
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
        "Generated by `python tools/generate_next_tasks.py` under the deduction-first strategic priority. THM-TARGET-001, FAITHFUL-REP-001, P8-ROLE-001, and SCORE-LEMMA-LEDGER-001 are frozen. SCORE-W0-PROOF-001 proves four source-side lemmas and establishes one source boundary; 32 obligations remain and W1 is active. Research gaps remain available in the gap report but do not automatically enter the active central queue.",
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
            f"### Task brief for {task['id']}", "", "```markdown",
            f"Create branch `{task['branch']}`.",
            f"Scope: {task['title']}.",
            "Preserve THM-TARGET-001, FAITHFUL-REP-001, P8-ROLE-001, SCORE-LEMMA-LEDGER-001, SCORE-W0-PROOF-001, all failed or unresolved obligations, and every nonclaim.",
            "Do not mark a lemma proved without a versioned proof artifact and dependency audit. Do not claim a representation theorem, universality, necessity, minimality, proof-assistant verification, actual-process correspondence, or independent validation without registered evidence.",
            "Validation commands:",
            "- `make research-check`",
            "- `make health-fast`",
            f"PR title: `{task['pr']}`",
            "```", "",
        ]
    lines += ["## Navigation", "", *nav_links()]
    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"{OUT.relative_to(ROOT)} tasks={len(TASKS)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
