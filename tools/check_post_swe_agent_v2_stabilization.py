#!/usr/bin/env python3
"""Fail-closed checks for the completed SWE-agent v2 case and its claim boundary."""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CASE_REL = Path("commercial/far-release-assurance/external-validation/swe-agent-v1.0.0-v1.0.1-gemini-3.1-pro-preview-v2")
CASE = ROOT / CASE_REL
REQUIRED_AUTHORITIES = (
    "README.md", "docs/ARCHITECTURE.md", "docs/project-status.md",
    "docs/glossary/canonical-vocabulary-index.md", "docs/DECISION_LOG.md",
    "docs/validation/README.md", "docs/governance/limitations-register.md",
    "docs/governance/unresolved-questions-register.md", "docs/ROADMAP.md",
)
FROZEN_PREFIXES = (f"{CASE_REL}/primary-freeze/", f"{CASE_REL}/post-freeze-reveal/")
# Exact historical source blobs are authenticated evidence snapshots, not live docs.
# Their relative links intentionally target the historical tree and their bytes may not be
# rewritten merely to satisfy current-tree navigation checks.
FROZEN_LINK_EVIDENCE_ROOTS = (
    (ROOT / "research/theory-dependency-audit/frozen-source-v1.0").resolve(),
)


def fail(message: str) -> None:
    raise SystemExit(f"post-swe-agent-v2: {message}")


def read(path: str | Path) -> str:
    target = ROOT / path
    if not target.is_file():
        fail(f"missing required file: {path}")
    return target.read_text(encoding="utf-8")


def data(path: str | Path):
    try:
        return json.loads(read(path))
    except json.JSONDecodeError as exc:
        fail(f"malformed JSON in {path}: {exc}")


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_authorities_and_architecture() -> None:
    for path in REQUIRED_AUTHORITIES:
        read(path)
    architecture = read("docs/ARCHITECTURE.md")
    ordered = ("Layer 1 — Foundations", "Layer 2 — Shared Theory", "Layer 3 — FARA", "Layer 4 — FAR", "Layer 5 — FARO")
    positions = [architecture.find(item) for item in ordered]
    if any(pos < 0 for pos in positions) or positions != sorted(positions):
        fail("canonical dependency order is missing or cyclic")
    prohibited = ("FARA depends on FAR", "FARA depends on FARO", "FAR depends on FARO", "theory depends on methodology")
    if any(value.lower() in architecture.lower() for value in prohibited):
        fail("canonical dependency direction is violated")
    canonical_map = read("docs/CANONICAL_MAP.md")
    for label in ("Project Status", "Canonical Terminology", "Decision Log", "Validation Evidence", "Current Limitations", "Open Problems", "Roadmap"):
        if canonical_map.count(f"| {label} |") != 1:
            fail(f"canonical map must declare exactly one {label} authority")


def _is_frozen_link_evidence(path: Path) -> bool:
    resolved = path.resolve()
    return any(resolved == root or root in resolved.parents for root in FROZEN_LINK_EVIDENCE_ROOTS)


def check_markdown_links() -> None:
    pattern = re.compile(r"(?<!!)\[[^\]]*\]\(([^)]+)\)")
    for path in sorted(ROOT.rglob("*.md")):
        if ".git" in path.parts or _is_frozen_link_evidence(path):
            continue
        for raw in pattern.findall(path.read_text(encoding="utf-8")):
            target = raw.split(maxsplit=1)[0].strip("<>")
            if not target or target.startswith(("#", "http://", "https://", "mailto:")):
                continue
            target = target.split("#", 1)[0]
            if target and not (path.parent / target).resolve().exists():
                fail(f"broken Markdown link: {path.relative_to(ROOT)} -> {target}")


def check_evidence() -> None:
    primary = data(CASE_REL / "primary-freeze/primary-freeze.json")
    for entry in primary.get("artifacts", []):
        path = CASE / "primary-freeze" / entry["path"]
        if not path.is_file() or sha(path) != entry["sha256"] or path.stat().st_size != entry["size_bytes"]:
            fail(f"primary-freeze member mismatch: {entry.get('path')}")
    sidecar = read(CASE_REL / "primary-freeze/primary-freeze.sha256").strip()
    if sidecar != sha(CASE / "primary-freeze/primary-freeze.json"):
        fail("primary-freeze sidecar mismatch")

    reveal = data(CASE_REL / "post-freeze-reveal/outcome-reveal.json")
    outcomes = reveal.get("outcomes")
    expected_runs = {"v1.0.0-r1", "v1.0.0-r2", "v1.0.1-r1", "v1.0.1-r2"}
    if not isinstance(outcomes, dict) or set(outcomes) != expected_runs:
        fail("reveal must contain the exact four preregistered runs")
    for run_id, outcome in outcomes.items():
        if outcome.get("resolved") is not False or outcome.get("report", {}).get("resolved") is not False:
            fail(f"unexpected or malformed bounded outcome: {run_id}")
    counts = {release: sum(v["resolved"] for v in outcomes.values() if v["release"] == release) for release in ("v1.0.0", "v1.0.1")}
    if counts != {"v1.0.0": 0, "v1.0.1": 0} or reveal.get("resolved_counts") != counts:
        fail("resolved counts do not derive to 0/2 and 0/2")
    report = data(CASE_REL / "post-freeze-reveal/final-comparison-report.json")
    adjudication = data(CASE_REL / "primary-freeze/outcome-blind-adjudication.json")
    if reveal.get("observed_resolution_result") != "no_observed_resolution_difference":
        fail("observed resolution result mismatch")
    if adjudication.get("overall_decision") != "REVIEW_REQUIRED" or report.get("bounded_case_decision") != "REVIEW_REQUIRED":
        fail("REVIEW_REQUIRED decision mismatch")
    if report.get("outcome_reveal_sha256") != sha(CASE / "post-freeze-reveal/outcome-reveal.json"):
        fail("final report is not bound to reveal")


def check_claims_and_workflows() -> None:
    required = ("0/2", "no_observed_resolution_difference", "REVIEW_REQUIRED", "equivalence", "superiority", "safety", "readiness", "general performance")
    for path in ("README.md", "docs/project-status.md", str(CASE_REL / "EXECUTION-STATUS.md")):
        lowered = read(path).lower()
        for phrase in required:
            if phrase.lower() not in lowered:
                fail(f"{path} omits bounded status/limitation language: {phrase}")
    execution = read(".github/workflows/far-swe-agent-execution-v2.yml")
    postprocess = read(".github/workflows/far-swe-agent-v2-postprocess.yml")
    for name, workflow in (("execution", execution), ("postprocess", postprocess)):
        if "timeout-minutes:" not in workflow:
            fail(f"{name} workflow has no timeout")
    retry_block = re.search(r'if \[ "\$RC" -eq 75 \]; then(?P<body>.*?)fi', execution, re.DOTALL)
    if retry_block is None or "exit 75" not in retry_block.group("body") or "exit 0" in retry_block.group("body"):
        fail("retryable internal failure is not propagated")
    if "Refuse mutation of the completed frozen case" not in execution:
        fail("completed execution case is mutable")
    if "test -f post-freeze-reveal/outcome-reveal.json" not in postprocess:
        fail("final report verification can silently skip")
    pipeline = read(CASE_REL / "evidence_pipeline_v2.py")
    for contract in ("not isinstance(model_patch, str)", "not model_patch.strip()", "model_patch != patch", "Malformed SWE-bench report", "Incomplete evaluation evidence"):
        if contract not in pipeline:
            fail(f"prediction/evaluation fail-closed contract missing: {contract}")


def main() -> int:
    check_authorities_and_architecture()
    check_markdown_links()
    check_evidence()
    check_claims_and_workflows()
    print(json.dumps({"successful": True, "case": CASE_REL.as_posix(), "resolved_counts": {"v1.0.0": 0, "v1.0.1": 0}, "decision": "REVIEW_REQUIRED"}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
