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


def execution_paths(root: Path = ROOT) -> list[Path]:
    return sorted((root / "research/validation/executions").glob("*.execution.yaml"))


def load_manifest_results(root: Path = ROOT) -> dict[str, str]:
    """Load canonical results without allowing later duplicate files to shadow earlier ones."""
    results: dict[str, str] = {}
    for path in execution_paths(root):
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        investigation = str(data.get("investigation", "")).strip()
        if investigation and investigation not in results:
            results[investigation] = str(data.get("result", "")).lower()
    return results


def validate_manifest_registry(root: Path = ROOT) -> list[str]:
    """Require a one-to-one mapping between investigation IDs and canonical filenames."""
    errors: list[str] = []
    seen: dict[str, Path] = {}
    for path in execution_paths(root):
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        investigation = str(data.get("investigation", "")).strip()
        expected = path.name.removesuffix(".execution.yaml")
        if not investigation:
            errors.append(f"{path.name}: missing investigation ID")
            continue
        if investigation != expected:
            errors.append(
                f"{path.name}: investigation ID {investigation} does not match canonical filename {expected}"
            )
        previous = seen.get(investigation)
        if previous is not None:
            errors.append(
                f"{investigation}: duplicate execution manifests {previous.name} and {path.name}"
            )
        else:
            seen[investigation] = path
    return errors


def resolve_repository_artifact(root: Path, declared_path: object) -> tuple[Path | None, str | None]:
    """Resolve an evidence path and reject absolute or repository-escaping locations."""
    if not isinstance(declared_path, str) or not declared_path.strip():
        return None, "<missing-path>"
    relative = Path(declared_path)
    if relative.is_absolute():
        return None, declared_path
    root_resolved = root.resolve()
    artifact = (root_resolved / relative).resolve()
    try:
        artifact.relative_to(root_resolved)
    except ValueError:
        return None, declared_path
    return artifact, None


def validate_manifest(
    path: Path,
    root: Path = ROOT,
    manifest_results: dict[str, str] | None = None,
) -> list[str]:
    data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    errors: list[str] = []
    investigation = data.get("investigation", path.stem)
    result = str(data.get("result", "")).lower()
    required = data.get("required_steps")
    upstream = data.get("upstream_dependencies", [])

    if required is None:
        required_steps: list[dict] = []
    elif isinstance(required, list):
        required_steps = required
    else:
        errors.append(f"{investigation}: required_steps must be a list")
        required_steps = []

    seen_step_ids: set[str] = set()
    for step in required_steps:
        if not isinstance(step, dict):
            errors.append(f"{investigation}: required step must be a mapping")
            continue
        step_id = str(step.get("id", "")).strip()
        if not step_id:
            errors.append(f"{investigation}: required step has missing or empty id")
        elif step_id in seen_step_ids:
            errors.append(f"{investigation}: duplicate required step id: {step_id}")
        else:
            seen_step_ids.add(step_id)
        state = str(step.get("status", "")).lower()
        evidence = step.get("evidence", [])
        if not isinstance(evidence, list):
            errors.append(f"{investigation}: step {step.get('id')} evidence must be a list")
            continue
        if state in COMPLETE_STATES and not evidence:
            errors.append(f"{investigation}: complete step {step.get('id')} has no evidence")
        for item in evidence:
            if not isinstance(item, dict):
                errors.append(f"{investigation}: step {step.get('id')} evidence entry must be a mapping")
                continue
            declared_path = item.get("path")
            artifact, invalid_path = resolve_repository_artifact(root, declared_path)
            if invalid_path is not None:
                errors.append(
                    f"{investigation}: evidence artifact must remain within repository root: {invalid_path}"
                )
            elif artifact is not None and not artifact.is_file():
                errors.append(f"{investigation}: missing evidence artifact {declared_path}")

    if result in PASS_RESULTS:
        if not isinstance(required, list) or not required_steps:
            errors.append(f"{investigation}: PASS requires a non-empty required_steps list")

        incomplete = [
            str(step.get("id"))
            for step in required_steps
            if not isinstance(step, dict)
            or str(step.get("status", "")).lower() not in COMPLETE_STATES
        ]
        if incomplete:
            errors.append(f"{investigation}: PASS with incomplete required steps: {', '.join(incomplete)}")

        missing_evidence = [
            str(step.get("id"))
            for step in required_steps
            if not isinstance(step, dict) or not step.get("evidence")
        ]
        if missing_evidence:
            errors.append(
                f"{investigation}: PASS with required steps lacking evidence: {', '.join(missing_evidence)}"
            )

        canonical_results = manifest_results if manifest_results is not None else load_manifest_results(root)
        unresolved: list[str] = []
        if not isinstance(upstream, list):
            errors.append(f"{investigation}: upstream_dependencies must be a list")
            upstream = []
        for dependency in upstream:
            if not isinstance(dependency, dict):
                unresolved.append("<invalid-dependency>")
                continue
            dependency_id = str(dependency.get("id", "")).strip()
            if not dependency_id:
                unresolved.append("<missing-id>")
                continue
            canonical_result = canonical_results.get(dependency_id)
            if canonical_result not in PASS_RESULTS:
                unresolved.append(dependency_id)
        if unresolved:
            errors.append(
                f"{investigation}: PASS with unresolved upstream dependencies: {', '.join(unresolved)}"
            )
    return errors


def validate_declared_results(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    manifests = load_manifest_results(root)
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
    paths = execution_paths()
    manifest_results = load_manifest_results()
    errors = validate_manifest_registry()
    errors.extend(
        error
        for path in paths
        for error in validate_manifest(path, manifest_results=manifest_results)
    )
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
