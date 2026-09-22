#!/usr/bin/env python3
"""Fail closed if FAR evidence-closure requirements drift out of canonical surfaces."""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT_ID = "FAR-EVIDENCE-CLOSURE-1.0"
REQUIREMENT_IDS = tuple(f"EC-{index:02d}" for index in range(1, 12))
REPLICATION_PATH = Path("research/validation/evidence/far-evidence-closure-replication-v1.0.md")

SURFACES = {
    "workflow": Path("frameworks/FAR/workflow.md"),
    "methodology": Path("frameworks/FAR/methodology.md"),
    "validation": Path("frameworks/FAR/investigation-validation.md"),
    "methodology_audit": Path("methodology/methodology-audit-protocol.md"),
    "methodology_index": Path("methodology/README.md"),
    "clean_room_auditor": Path(".claude/skills/far-clean-room-auditor/SKILL.md"),
    "discovery_engine": Path(".claude/skills/far-discovery-engine/SKILL.md"),
    "research_orchestrator": Path(".claude/skills/far-research-orchestrator/SKILL.md"),
    "research_quality_gate": Path(".claude/skills/far-research-quality-gate/SKILL.md"),
    "execution_validator": Path("tools/check_investigation_execution.py"),
    "acceptance": Path("docs/governance/far-evidence-closure-acceptance-v1.0.md"),
    "replication": REPLICATION_PATH,
    "canonical_map": Path("docs/CANONICAL_MAP.md"),
}

WORKFLOW_ANCHORS = (
    "claim-level logical disposition",
    "terminal bounded saturation pass",
    "strongest support",
    "strongest counterevidence",
    "denominator",
    "measurement",
    "alternative explanations",
    "narrower",
    "residual uncertainty",
    "NOT APPLICABLE",
    "methodology audit",
)

VALIDATION_ANCHORS = (
    "claim-level logical disposition",
    "evidence/search classes",
    "denominator",
    "measurement",
    "strongest support",
    "strongest counterevidence",
    "alternative explanations",
    "narrower",
    "residual uncertainty",
    "terminal bounded saturation pass",
    "methodology audit",
)

CANONICAL_MAP_ANCHORS = (
    "FAR Evidence-Closure Contract",
    "FAR Evidence-Closure Acceptance",
    "far-evidence-closure-acceptance-v1.0.md",
)

ACCEPTANCE_LIFECYCLE_ANCHORS = (
    "## Question",
    "## Execution",
    "## Observation",
    "## Discovery",
    "## Replication",
    "## Acceptance",
    "## Promotion",
    REPLICATION_PATH.as_posix(),
)

AUDIT_PASSING_POLARITY = (
    "did the investigation continue until `FAR-EVIDENCE-CLOSURE-1.0` was satisfied"
)


def _read(root: Path, relative: Path, errors: list[str]) -> str:
    path = root / relative
    if not path.is_file():
        errors.append(f"missing required evidence-closure surface: {relative.as_posix()}")
        return ""
    text = path.read_text(encoding="utf-8")
    if not text.strip():
        errors.append(f"empty required evidence-closure surface: {relative.as_posix()}")
    return text


def validate(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    texts = {name: _read(root, path, errors) for name, path in SURFACES.items()}

    for name, text in texts.items():
        if CONTRACT_ID not in text:
            errors.append(f"{SURFACES[name].as_posix()}: missing {CONTRACT_ID} reference")

    workflow = texts.get("workflow", "")
    validation = texts.get("validation", "")
    for requirement_id in REQUIREMENT_IDS:
        if requirement_id not in workflow:
            errors.append(f"workflow missing closure requirement {requirement_id}")
        if requirement_id not in validation:
            errors.append(f"investigation validation missing closure requirement {requirement_id}")

    for anchor in WORKFLOW_ANCHORS:
        if anchor.casefold() not in workflow.casefold():
            errors.append(f"workflow missing evidence-closure anchor: {anchor}")

    for anchor in VALIDATION_ANCHORS:
        if anchor.casefold() not in validation.casefold():
            errors.append(f"investigation validation missing evidence-closure anchor: {anchor}")

    if "A decisive claim-level disposition does not by itself authorize investigation closure." not in workflow:
        errors.append("workflow does not explicitly prohibit disposition-to-closure collapse")

    if "A decisive atomic verdict is not evidence that the closure gate passed." not in validation:
        errors.append("investigation validation does not explicitly reject atomic-verdict self-certification")

    canonical_map = texts.get("canonical_map", "")
    for anchor in CANONICAL_MAP_ANCHORS:
        if anchor not in canonical_map:
            errors.append(f"canonical map missing evidence-closure authority anchor: {anchor}")

    acceptance = texts.get("acceptance", "")
    positions: list[int] = []
    for anchor in ACCEPTANCE_LIFECYCLE_ANCHORS:
        position = acceptance.find(anchor)
        if position < 0:
            errors.append(f"evidence-closure acceptance missing lifecycle anchor: {anchor}")
        positions.append(position)
    found_positions = [position for position in positions if position >= 0]
    if len(found_positions) == len(positions) and found_positions != sorted(found_positions):
        errors.append("evidence-closure acceptance lifecycle stages are out of order")

    methodology_audit = texts.get("methodology_audit", "")
    if AUDIT_PASSING_POLARITY.casefold() not in methodology_audit.casefold():
        errors.append("methodology audit does not encode affirmative passing polarity for post-decisive continuation")
    if (
        "Did a decisive witness, counterexample, proof, or authoritative record cause the investigation to stop before"
        in methodology_audit
    ):
        errors.append("methodology audit retains the inverted premature-stopping closure question")

    return errors


def main() -> int:
    errors = validate()
    if errors:
        print("FAR evidence-closure validation: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    print(
        "FAR evidence-closure validation: PASS "
        f"({len(SURFACES)} surfaces; {len(REQUIREMENT_IDS)} closure requirements)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
