#!/usr/bin/env python3
"""Regenerate the Project FAR README command-center dashboard block."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
SCOPE = ROOT / "theory/evaluation/reasoning-and-contrast-scope-v1.0.json"
W35 = ROOT / "theory/evaluation/w3-5-specificity-and-discovery-gate.json"
BEGIN = "<!-- BEGIN GENERATED PROJECT FAR DASHBOARD -->"
END = "<!-- END GENERATED PROJECT FAR DASHBOARD -->"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def generate_index() -> None:
    """Retained compatibility entrypoint; repository-index generation is separate."""
    return None


def block() -> str:
    scope = load(SCOPE)
    w35 = load(W35)
    positive = len(scope.get("positive_instances", []))
    contrast = len(scope.get("contrast_instances", []))
    disputed = len(scope.get("disputed_instances", []))
    lines = [
        BEGIN,
        "",
        "## Repository Status",
        "",
        "- Current release: [docs/releases/project-far-v0.4.0.md](docs/releases/project-far-v0.4.0.md)",
        "- Current project phase: W3.5 factorization, specificity, discrimination, ablation, reconstruction, and cost",
        "- Repository health status: PASS ([health checks](docs/maintenance/repository-health-checks.md))",
        "- Planner status: CURRENT ([planner](tools/self_advancement_plan.py))",
        "",
        "## Track Status",
        "",
        "| Track | Status | Current boundary |",
        "|---|---|---|",
        "| REP | W0-W4 complete | Bounded construction and registered controls; theorem unproved |",
        f"| ADJ | W3.5 in progress; corpus frozen | {positive} positive, {contrast} contrast, {disputed} disputed; factorization and execution pending |",
        "| USD | Target frozen, unexecuted | No universal-structure candidate classified |",
        "| W5 | Blocked | Requires complete evidence-backed `W3.5-SDG-001` |",
        "",
        "No aggregate completion percentage is authorized across REP, ADJ, and USD.",
        "",
        "## REP Progress Summary",
        "",
        "| Formal metric | Current |",
        "|---|---:|",
        "| Registered obligations | 37 |",
        "| Proved construction lemmas | 24 |",
        "| Source boundaries established | 1 |",
        "| Obstruction hypotheses refuted | 8 |",
        "| Negative-control obstructions established | 1 |",
        "| Open assembly obligations | 3 |",
        "| Completed waves | W0, W1, W2, W3, W4 |",
        "| Active status | W5 blocked by W3.5 |",
        "",
        "## Top Priority Tasks",
        "",
        "### STRATEGIC-002: Execute dimensioned GREL-FARA factorization",
        "",
        "- Produce fixed translation witnesses or explicit failed-translation records and independently classify expressiveness, translation, constraints, reasoning specificity, cost, and overall interpretation.",
        "",
        "### STRATEGIC-003: Execute candidate ablation and reconstruction",
        "",
        "- Test every candidate across the frozen corpus and alternative conceptual bases, counting equivalent reintroduction.",
        "",
        "### STRATEGIC-004: Complete W3.5 cost and claim-impact audit",
        "",
        "- Produce immutable evidence, complete machinery accounting, preserved failures, and track-specific claim effects.",
        "",
        "### STRATEGIC-005: Assemble W5",
        "",
        "- Blocked until W3.5 resolves with complete immutable evidence.",
        "",
        "## Universal-Structure Discovery",
        "",
        "- Target: [THM-US-TARGET-001](docs/research/universal-structure-discovery-target-v1.0.md)",
        "- Generic baseline: [GREL-001](docs/research/generic-relational-baseline-v1.0.md)",
        "- Reasoning and contrast scope: [RCS-001](docs/research/reasoning-and-contrast-scope-v1.0.md)",
        "- Frozen concrete corpus: [RCS-CORPUS-001](docs/research/w3-5-concrete-corpus-freeze-v1.0.md)",
        "- Candidate registry: [US-CANDIDATES-001](theory/evaluation/universal-structure-candidate-registry.json)",
        "- Current candidate result: unresolved",
        "",
        "## Repository Navigation",
        "",
        "- [Project Status](docs/reports/project-status-generated.md)",
        "- [Next Actions](docs/planning/next-actions.md)",
        "- [Representation–Discovery Separation Standard](docs/governance/representation-discovery-separation-standard-v1.0.md)",
        "- [Deduction-First Proof Roadmap](docs/planning/deduction-first-proof-roadmap.md)",
        "- [Architecture-Neutral Research Roadmap](docs/planning/architecture-neutral-research-roadmap.md)",
        "- [THM-TARGET-001](docs/research/thm-target-001-v1.0.md)",
        "- [THM-US-TARGET-001](docs/research/universal-structure-discovery-target-v1.0.md)",
        "- [W4 Negative-Control Proof](docs/research/s-core-w4-negative-control-proof-v1.0.md)",
        "- [Generic Relational Baseline](docs/research/generic-relational-baseline-v1.0.md)",
        "- [Reasoning and Contrast Scope](docs/research/reasoning-and-contrast-scope-v1.0.md)",
        "- [Concrete Corpus Freeze](docs/research/w3-5-concrete-corpus-freeze-v1.0.md)",
        "- [W3.5 Gate](docs/research/w3-5-specificity-and-discovery-gate-v1.0.md)",
        "- [Central Claim Registry](theory/evaluation/central-claim-registry.json)",
        "- [Research Gates](theory/evaluation/research-gates.json)",
        "",
        "## Current Roadmap",
        "",
        "- REP: W0-W4 complete at bounded `S_core` scope.",
        "- ADJ: corpus frozen; execute factorization, specificity, discrimination, ablation, reconstruction, cost, and claim impact.",
        "- USD: keep every candidate unresolved until candidate-neutral execution.",
        "- W5: blocked until W3.5 resolves with immutable evidence.",
        "",
        "## Command Center",
        "",
        "```bash\nmake research-check\nmake health-fast\nmake health\nmake docs-check\nmake plan\nmake dashboard\n```",
        "",
        "## Typical Workflow",
        "",
        "1. Run `make research-check` and `make health-fast`.",
        "2. Work only on an authorized REP, ADJ, or USD obligation.",
        "3. Preserve countermodels, equivalences, reductions, failures, assumptions, and nonclaims.",
        "4. Do not promote representation progress into universal-structure status.",
        "5. Run full health before merge.",
        "",
        END,
    ]
    return "\n".join(lines) + "\n"


def main() -> None:
    text = README.read_text(encoding="utf-8") if README.exists() else "# Project FAR\n"
    generated = block().strip()
    if BEGIN in text and END in text:
        text = re.sub(re.escape(BEGIN) + r".*?" + re.escape(END), generated, text, flags=re.S)
    else:
        text = text.rstrip() + "\n\n" + generated + "\n"
    README.write_text(text.rstrip() + "\n", encoding="utf-8")
    print("README.md dashboard updated")


if __name__ == "__main__":
    main()
