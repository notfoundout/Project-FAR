#!/usr/bin/env python3
"""Fail closed on unsupported investigation PASS declarations."""
from __future__ import annotations

import argparse
import hashlib
import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
EXECUTIONS = ROOT / "research/validation/executions"
PASS_RESULTS = {"pass", "passed"}
COMPLETE_STATES = {"complete", "completed"}
COVERAGE_STATES = {"covered", "not_applicable"}
MANDATORY_CLOSURE_EVIDENCE_CLASSES = (
    "direct_primary_evidence",
    "opposing_disconfirming_evidence",
    "measurement_data_quality",
    "denominator_directness_construct_alignment",
    "alternative_explanations",
    "surviving_narrower_propositions",
    "residual_uncertainty",
)
MANDATORY_CLOSURE_INVENTORIES = (
    "strongest_opposing_evidence",
    "measurement_and_classification_limits",
    "alternative_explanations",
    "surviving_narrower_propositions",
    "residual_uncertainty",
)

# These PASS records predate FAR-POST-EVIDENCE-CLOSURE-1.0. The exemption is
# bound to the exact historical Git blob; changing one byte activates the new
# closure contract rather than inheriting a mutable legacy bypass.
LEGACY_PASS_BLOBS = {
    "research/validation/executions/VI-001.execution.yaml":
        "8da94d4caa38170303b319769d36b0c4ced731e0",
}


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


def git_blob_sha(path: Path) -> str:
    raw = path.read_bytes()
    header = f"blob {len(raw)}\0".encode("ascii")
    return hashlib.sha1(header + raw).hexdigest()


def is_legacy_pass_manifest(path: Path, root: Path = ROOT) -> bool:
    try:
        relative = path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return False
    expected = LEGACY_PASS_BLOBS.get(relative)
    return expected is not None and git_blob_sha(path) == expected


def _nonempty_text(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _validate_evidence_refs(
    investigation: str,
    label: str,
    evidence: object,
    root: Path,
    errors: list[str],
) -> None:
    if not isinstance(evidence, list) or not evidence:
        errors.append(f"{investigation}: {label} requires a non-empty evidence list")
        return
    for item in evidence:
        if not isinstance(item, dict):
            errors.append(f"{investigation}: {label} evidence entry must be a mapping")
            continue
        declared_path = item.get("path")
        artifact, invalid_path = resolve_repository_artifact(root, declared_path)
        if invalid_path is not None:
            errors.append(
                f"{investigation}: {label} evidence artifact must remain within repository root: {invalid_path}"
            )
        elif artifact is not None and not artifact.is_file():
            errors.append(f"{investigation}: {label} missing evidence artifact {declared_path}")
        if not _nonempty_text(item.get("locator")):
            errors.append(f"{investigation}: {label} evidence requires a non-empty locator")


def _validate_inventory(
    investigation: str,
    name: str,
    value: object,
    errors: list[str],
) -> None:
    if not isinstance(value, dict):
        errors.append(f"{investigation}: closure.{name} must be a mapping")
        return
    findings = value.get("findings")
    if not isinstance(findings, list):
        errors.append(f"{investigation}: closure.{name}.findings must be a list")
        return
    if not findings and not _nonempty_text(value.get("none_found_basis")):
        errors.append(
            f"{investigation}: closure.{name} is empty without a non-empty none_found_basis"
        )
    for finding in findings:
        if not _nonempty_text(finding):
            errors.append(f"{investigation}: closure.{name}.findings entries must be non-empty strings")


def validate_closure_contract(
    data: dict,
    path: Path,
    root: Path = ROOT,
) -> list[str]:
    """Require bounded post-evidence closure before a non-legacy PASS may be declared."""
    investigation = str(data.get("investigation", path.stem)).strip() or path.stem
    errors: list[str] = []
    closure = data.get("closure")
    if not isinstance(closure, dict):
        return [f"{investigation}: PASS requires a closure mapping under FAR-POST-EVIDENCE-CLOSURE-1.0"]

    if str(closure.get("status", "")).strip().lower() != "resolved":
        errors.append(f"{investigation}: PASS requires closure.status resolved")

    logical = closure.get("logical_disposition")
    if not isinstance(logical, dict):
        errors.append(f"{investigation}: closure.logical_disposition must be a mapping")
    else:
        if not _nonempty_text(logical.get("outcome")):
            errors.append(f"{investigation}: closure.logical_disposition.outcome is required")
        _validate_evidence_refs(
            investigation,
            "closure.logical_disposition",
            logical.get("evidence"),
            root,
            errors,
        )

    search_frame = closure.get("search_frame")
    if not isinstance(search_frame, dict):
        errors.append(f"{investigation}: closure.search_frame must be a mapping")
    else:
        for field in ("scope", "stopping_rule", "evidence_cutoff"):
            if not _nonempty_text(search_frame.get(field)):
                errors.append(f"{investigation}: closure.search_frame.{field} is required")
        spaces = search_frame.get("sources_or_spaces")
        if not isinstance(spaces, list) or not spaces or any(not _nonempty_text(item) for item in spaces):
            errors.append(
                f"{investigation}: closure.search_frame.sources_or_spaces must be a non-empty list of strings"
            )

    evidence_classes = closure.get("evidence_classes")
    if not isinstance(evidence_classes, dict):
        errors.append(f"{investigation}: closure.evidence_classes must be a mapping")
    else:
        for class_id in MANDATORY_CLOSURE_EVIDENCE_CLASSES:
            entry = evidence_classes.get(class_id)
            if not isinstance(entry, dict):
                errors.append(f"{investigation}: closure.evidence_classes.{class_id} is required")
                continue
            state = str(entry.get("status", "")).strip().lower()
            if state not in COVERAGE_STATES:
                errors.append(
                    f"{investigation}: closure.evidence_classes.{class_id}.status must be covered or not_applicable"
                )
                continue
            if state == "covered":
                _validate_evidence_refs(
                    investigation,
                    f"closure.evidence_classes.{class_id}",
                    entry.get("evidence"),
                    root,
                    errors,
                )
            elif not _nonempty_text(entry.get("reason")):
                errors.append(
                    f"{investigation}: closure.evidence_classes.{class_id} not_applicable requires a reason"
                )

    for inventory in MANDATORY_CLOSURE_INVENTORIES:
        _validate_inventory(investigation, inventory, closure.get(inventory), errors)

    interpretive = closure.get("interpretive_closure")
    if not isinstance(interpretive, dict):
        errors.append(f"{investigation}: closure.interpretive_closure must be a mapping")
    else:
        if str(interpretive.get("status", "")).strip().lower() != "complete":
            errors.append(f"{investigation}: closure.interpretive_closure.status must be complete")
        _validate_evidence_refs(
            investigation,
            "closure.interpretive_closure",
            interpretive.get("evidence"),
            root,
            errors,
        )

    saturation = closure.get("terminal_saturation")
    if not isinstance(saturation, dict):
        errors.append(f"{investigation}: closure.terminal_saturation must be a mapping")
    else:
        if str(saturation.get("status", "")).strip().lower() != "complete":
            errors.append(f"{investigation}: closure.terminal_saturation.status must be complete")
        new_findings = saturation.get("new_material_findings")
        if isinstance(new_findings, bool) or not isinstance(new_findings, int) or new_findings != 0:
            errors.append(
                f"{investigation}: closure.terminal_saturation.new_material_findings must be integer 0"
            )
        _validate_evidence_refs(
            investigation,
            "closure.terminal_saturation",
            saturation.get("evidence"),
            root,
            errors,
        )

    return errors


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
        raw_step_id = step.get("id")
        if not isinstance(raw_step_id, str) or not raw_step_id.strip():
            errors.append(f"{investigation}: required step has missing, empty, or non-string id")
        else:
            step_id = raw_step_id.strip()
            if step_id in seen_step_ids:
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

        if not is_legacy_pass_manifest(path, root):
            errors.extend(validate_closure_contract(data, path, root))
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
