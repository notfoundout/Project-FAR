#!/usr/bin/env python3
"""Generate the terminal advisory queue for completed POST-CLOSURE-001."""
from __future__ import annotations

import json
import posixpath
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs/planning/next-actions.md"
OUT_REPO_PATH = "docs/planning/next-actions.md"
PROGRAM_MD = "docs/governance/post-closure-assurance-and-application-program-v1.0.md"
PROGRAM_JSON = ROOT / "theory/evaluation/post-closure-assurance-and-application-program-v1.0.json"
THEORY = "theory/theorems/Project-FAR-Theory-Closure-v1.1.md"
HISTORICAL_THEORY = "theory/theorems/Project-FAR-Theory-Closure-v1.0.md"
CORE_ID = "PROJECT-FAR-CORE-THEORY-1.1"
PROGRAM_ID = "POST-CLOSURE-001"

COMPLETED_TASKS = [
    {
        "id": "STRATEGIC-012",
        "title": "Develop domain comparison contracts",
        "workstream": "PCA-W4-DOMAIN-CONTRACTS",
        "priority": "complete",
        "outcome": "Six source-motivated native contracts, twelve `far-ir/2.0` records, six checked collisions, and six checked scoped repairs with explicit nonclaims.",
    },
    {
        "id": "STRATEGIC-013",
        "title": "Specify approximation and cost orders",
        "workstream": "PCA-W5-APPROXIMATION-AND-COST",
        "priority": "complete",
        "outcome": "Checked finite-explicit `far-ir/2.1` approximation and product-cost semantics without a universal optimum claim.",
    },
    {
        "id": "STRATEGIC-014",
        "title": "Test audit utility",
        "workstream": "PCA-W6-EMPIRICAL-AUDIT-UTILITY",
        "priority": "complete at bounded internal controlled-artifact scope",
        "outcome": "Preregistered six-domain control found schema-only mutation detection `0/6`, FAR semantic mutation detection `6/6`, clean-control acceptance `6/6`, FAR/oracle agreement `12/12`, and native lossy-control confirmation `6/6`.",
        "boundary": "human disagreement reduction remains `UNDERDETERMINED`; external real-world utility remains `OPEN`.",
    },
]


def repository_link(path: str) -> str:
    href = posixpath.relpath(path, posixpath.dirname(OUT_REPO_PATH))
    return f"[{path}]({href})"


def nav_links() -> list[str]:
    return [
        f"- README Command Center: {repository_link('README.md')}",
        f"- Current Project Status: {repository_link('docs/project-status.md')}",
        f"- Core Theory: {repository_link(THEORY)}",
        f"- Historical v1.0 Core: {repository_link(HISTORICAL_THEORY)}",
        f"- Post-Closure Program: {repository_link(PROGRAM_MD)}",
        f"- Historical Bounded Status: {repository_link('docs/reports/project-status-generated.md')}",
        f"- Next Actions: {repository_link(OUT_REPO_PATH)}",
    ]


def validate_terminal_program() -> None:
    program = json.loads(PROGRAM_JSON.read_text(encoding="utf-8"))
    if program.get("program_id") != PROGRAM_ID:
        raise SystemExit("post-closure program identity drifted")
    if program.get("status") != "complete_registered_workstreams":
        raise SystemExit("post-closure program is not terminal")
    states = {item.get("id"): item.get("state") for item in program.get("workstreams", [])}
    for task in COMPLETED_TASKS:
        if states.get(task["workstream"]) != "complete":
            raise SystemExit(f"{task['workstream']} is not complete")
    if program.get("next_action", {}).get("workstream") is not None:
        raise SystemExit("terminal post-closure program unexpectedly registers a successor")
    if "OP-28" not in str(program.get("next_action", {}).get("obligation", "")):
        raise SystemExit("terminal post-closure program lost the external OP-28 obligation")


def main() -> int:
    validate_terminal_program()
    lines = [
        "# Next Actions",
        "",
        "## Navigation",
        "",
        *nav_links(),
        "",
        "Generated from the registered post-closure program.",
        "",
        "Program: `POST-CLOSURE-001` — complete at its six registered workstream scopes.",
        "",
        f"Current governing theory: `{CORE_ID}`.",
        "",
        "The core theory is closed after the governed v1.1 correction. The sealed W1 independent review, W2 proof-assistant formalization, W3 contract schema, W4 domain contracts, W5 approximation/cost semantics, and W6 bounded internal audit-utility control are complete at their exact governed scopes.",
        "",
        "There is **no registered next `POST-CLOSURE-001` workstream**. External/human audit-effectiveness evidence remains an open downstream obligation under OP-28 and requires separate governance before execution; it is not silently named W7.",
        "",
        "## Ranked Next Actions",
        "",
    ]
    for task in COMPLETED_TASKS:
        lines.extend(
            [
                f"### {task['id']}: {task['title']}",
                "",
                f"- Registered workstream: `{task['workstream']}`",
                f"- Priority: {task['priority']}",
                f"- Outcome: {task['outcome']}",
            ]
        )
        if "boundary" in task:
            lines.append(f"- Boundary: {task['boundary']}")
        lines.append("")
    lines.extend(
        [
            "### OPEN-EXTERNAL-OP-28: Independently test human/external audit effectiveness",
            "",
            "- Registered post-closure workstream: none",
            "- Authority: OP-28 in the open-problems register",
            "- Priority: open / external-dependency",
            "- Why it matters: W6 establishes only a project-authored machine controlled-artifact result. It does not show that human reviewers catch more consequential loss, disagree less, work faster, or make better real-world decisions.",
            "- Required before execution: a separately governed protocol defining participant population or external evaluator, comparator, blinded/randomized procedure where appropriate, outcome measures, analysis plan, independence disclosure, data governance/ethics requirements, falsifiers, and promotion boundaries.",
            "- Prohibited shortcut: do not relabel W6's schema baseline, machine oracle, or internal replication as human or external evidence.",
            "",
            "## Maintainer Boundaries",
            "",
            "- Read `AGENTS.md` and the Research Execution Charter before execution.",
            "- Preserve historical v1.0 bytes/hash and the corrected v1.1 authority.",
            "- Preserve the v1.1 FAR-CORE-004 minimality/sufficiency distinction and FAR-CORE-010 exact-theory/frame-residue distinction.",
            "- Reopen the core only for a reproducible contradiction to a premise, proof step, theorem, or derivation.",
            "- Keep determinate absence, failure, inapplicability, unresolvedness, and epistemic Unknown distinct when the contract does.",
            "- Do not infer mathematical proof from CI, schema conformance, finite panels, successful encoding, or W6 controlled-artifact performance.",
            "",
            "Validation commands:",
            "",
            "- `python tools/check_project_far_theory_closure.py`",
            "- `make pca-w6-check`",
            "- `make semantic-check`",
            "- `make docs-check`",
            "- `make health-fast`",
        ]
    )
    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"{OUT.relative_to(ROOT)} terminal_tasks={len(COMPLETED_TASKS)} external_obligations=1")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
