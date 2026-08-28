#!/usr/bin/env python3
"""Generate advisory tasks for POST-CLOSURE-001."""
from __future__ import annotations

import posixpath
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs/planning/next-actions.md"
OUT_REPO_PATH = "docs/planning/next-actions.md"
PROGRAM = "docs/governance/post-closure-assurance-and-application-program-v1.0.md"
THEORY = "theory/theorems/Project-FAR-Theory-Closure-v1.1.md"
HISTORICAL_THEORY = "theory/theorems/Project-FAR-Theory-Closure-v1.0.md"
CORE_ID = "PROJECT-FAR-CORE-THEORY-1.1"

TASKS = [
    {
        "id": "STRATEGIC-010",
        "workstream": "PCA-W1-INDEPENDENT-REVIEW",
        "priority": "high",
        "title": "Review the corrected core independently",
        "why": "The corrected core is accepted internal deductive work but has no genuinely independent premise-by-premise review.",
        "outcome": "An immutable review record that confirms, narrows, refutes, or leaves each obligation OPEN without changing its wording by convention.",
        "branch": "research/pca-w1-core-v1.1-independent-review",
        "pr": "Execute PCA-W1 independent review of core theory v1.1",
        "review_target": CORE_ID,
        "required_provenance": "disclose reviewer prior exposure, conflicts, tools, assumptions, checked obligations, unresolved objections, and source corpus.",
    },
    {
        "id": "STRATEGIC-011",
        "workstream": "PCA-W2-PROOF-ASSISTANT-FORMALIZATION",
        "priority": "queued",
        "title": "Formalize the corrected factorization core",
        "why": "The core has explicit narrative proofs but no single proof-assistant-checked artifact.",
        "outcome": "A checked formalization or an exact obstruction report with external assumptions exposed.",
        "branch": "research/pca-w2-core-formalization",
        "pr": "Formalize Project FAR core theorems",
    },
    {
        "id": "STRATEGIC-012",
        "workstream": "PCA-W3-CONTRACT-SCHEMA",
        "priority": "queued",
        "title": "Implement the contract schema",
        "why": "`far-ir/1.0` cannot natively certify contracts, decoders, collisions, quotients, profiles, frames, or cost orders.",
        "outcome": "A new versioned schema, deterministic implementation, migration boundary, and conformance suite.",
        "branch": "feat/pca-w3-contract-schema",
        "pr": "Implement contract-relative FAR IR",
    },
    {
        "id": "STRATEGIC-013",
        "workstream": "PCA-W4-DOMAIN-CONTRACTS",
        "priority": "queued",
        "title": "Develop domain comparison contracts",
        "why": "The core theorem does not select tests, outcome types, or normative objectives for a domain.",
        "outcome": "Independently motivated, versioned contracts with explicit nonclaims and collision tests.",
        "branch": "research/pca-w4-domain-contracts",
        "pr": "Develop scoped domain contracts",
    },
    {
        "id": "STRATEGIC-014",
        "workstream": "PCA-W5-APPROXIMATION-AND-COST",
        "priority": "queued",
        "title": "Specify approximation and cost orders",
        "why": "Exact information minimality does not choose metrics, decision losses, tolerances, runtime, storage, or explanatory cost.",
        "outcome": "Scoped approximate adequacy and cost-minimality specifications without a universal optimum claim.",
        "branch": "research/pca-w5-approximation-cost",
        "pr": "Specify approximate and cost-relative adequacy",
    },
    {
        "id": "STRATEGIC-015",
        "workstream": "PCA-W6-EMPIRICAL-AUDIT-UTILITY",
        "priority": "external-dependency",
        "title": "Test audit utility",
        "why": "No preregistered external study shows that contract/factorization auditing catches material loss or reduces disagreement.",
        "outcome": "Bounded empirical evidence with negative results, protocol deviations, and independence disclosed.",
        "branch": "research/pca-w6-audit-utility",
        "pr": "Prepare PCA-W6 audit-utility study",
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
        f"- Post-Closure Program: {repository_link(PROGRAM)}",
        f"- Historical Bounded Status: {repository_link('docs/reports/project-status-generated.md')}",
        f"- Next Actions: {repository_link(OUT_REPO_PATH)}",
    ]


def main() -> int:
    assert TASKS[0]["workstream"] == "PCA-W1-INDEPENDENT-REVIEW"
    assert TASKS[0]["review_target"] == CORE_ID
    assert len({item["id"] for item in TASKS}) == len(TASKS)
    assert len({item["workstream"] for item in TASKS}) == len(TASKS)

    lines = [
        "# Next Actions",
        "",
        "## Navigation",
        "",
        *nav_links(),
        "",
        "Generated from the registered post-closure program.",
        "",
        "Program: `POST-CLOSURE-001`.",
        "",
        f"Current review target: `{CORE_ID}`.",
        "",
        "The core theory is closed after the governed v1.1 correction. These tasks change assurance, implementation, applicability, or utility; they do not reopen the core without a genuine contradiction.",
        "",
        "The hostile W1 audit that found the v1.1 defects is internal/non-independent evidence. It does not satisfy `PCA-W1-INDEPENDENT-REVIEW`.",
        "",
        "Canonical next workstream: `PCA-W1-INDEPENDENT-REVIEW`.",
        "",
        "## Ranked Next Actions",
        "",
    ]
    for task in TASKS:
        lines += [
            f"### {task['id']}: {task['title']}",
            "",
            f"- Registered workstream: `{task['workstream']}`",
        ]
        if task.get("review_target"):
            lines.append(f"- Review target: `{task['review_target']}`")
        lines += [
            f"- Source: {repository_link(PROGRAM)}",
            f"- Priority: {task['priority']}",
            f"- Why it matters: {task['why']}",
        ]
        if task.get("required_provenance"):
            lines.append(f"- Required provenance: {task['required_provenance']}")
        lines += [
            f"- Expected outcome: {task['outcome']}",
            f"- Suggested branch name: `{task['branch']}`",
            f"- Suggested PR title: `{task['pr']}`",
            "",
        ]
    lines += [
        "## Maintainer Boundaries",
        "",
        "- Read `AGENTS.md` and the Research Execution Charter before execution.",
        "- Preserve historical v1.0 bytes/hash and the corrected v1.1 authority.",
        "- Preserve the v1.1 FAR-CORE-004 minimality/sufficiency distinction and FAR-CORE-010 exact-theory/frame-residue distinction.",
        "- Reopen the core only for a reproducible contradiction to a premise, proof step, theorem, or derivation.",
        "- Keep determinate absence, failure, inapplicability, unresolvedness, and epistemic Unknown distinct when the contract does.",
        "- Do not infer mathematical proof from CI, schema conformance, finite panels, or successful encoding.",
        "",
        "Validation commands:",
        "",
        "- `python tools/check_project_far_theory_closure.py`",
        "- `make semantic-check`",
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
