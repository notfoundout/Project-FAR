#!/usr/bin/env python3
"""Fail closed on unsupported investigation PASS declarations."""
from __future__ import annotations

import argparse
import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
EXECUTIONS = ROOT / "research/validation/executions"
PASS_RESULTS = {"pass", "passed"}
COMPLETE_STATES = {"complete", "completed"}


def validate_manifest(path: Path, root: Path = ROOT) -> list[str]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    errors: list[str] = []
    investigation = data.get("investigation", path.stem)
    result = str(data.get("result", "")).lower()
    required = data.get("required_steps", [])
    upstream = data.get("upstream_dependencies", [])

    for step in required:
        state = str(step.get("status", "")).lower()
        evidence = step.get("evidence", [])
        if state in COMPLETE_STATES and not evidence:
            errors.append(f"{investigation}: complete step {step.get('id')} has no evidence")
        for item in evidence:
            artifact = root / item["path"]
            if not artifact.is_file():
                errors.append(f"{investigation}: missing evidence artifact {item['path']}")

    if result in PASS_RESULTS:
        incomplete = [str(step.get("id")) for step in required if str(step.get("status", "")).lower() not in COMPLETE_STATES]
        if incomplete:
            errors.append(f"{investigation}: PASS with incomplete required steps: {', '.join(incomplete)}")
        missing_evidence = [str(step.get("id")) for step in required if not step.get("evidence")]
        if missing_evidence:
            errors.append(f"{investigation}: PASS with required steps lacking evidence: {', '.join(missing_evidence)}")
        unresolved = [str(dep.get("id")) for dep in upstream if str(dep.get("status", "")).lower() not in PASS_RESULTS | COMPLETE_STATES]
        if unresolved:
            errors.append(f"{investigation}: PASS with unresolved upstream dependencies: {', '.join(unresolved)}")
    return errors


def validate_declared_results(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    manifests = {}
    for path in sorted((root / "research/validation/executions").glob("*.execution.yaml")):
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        manifests[data["investigation"]] = str(data.get("result", "")).lower()
    for path in sorted((root / "research/validation/investigations").glob("VI-*.md")):
        text = path.read_text(encoding="utf-8")
        ident_match = re.search(r"## Investigation ID\s+\n\s*(VI-\d+)", text)
        if not ident_match:
            continue
        ident = ident_match.group(1)
        if re.search(r"(?:Result:\s*\*\*|Result:\s*|Scoped Result:\s*\*\*)PASS\b", text, re.IGNORECASE):
            if ident not in manifests:
                errors.append(f"{ident}: PASS declared without an execution manifest")
            elif manifests[ident] not in PASS_RESULTS:
                errors.append(f"{ident}: document declares PASS but manifest result is {manifests[ident]}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.parse_args()
    paths = sorted(EXECUTIONS.glob("*.execution.yaml"))
    errors = [error for path in paths for error in validate_manifest(path)]
    errors.extend(validate_declared_results())
    if errors:
        print("Investigation execution validation: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"Investigation execution validation: PASS ({len(paths)} manifests checked)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
