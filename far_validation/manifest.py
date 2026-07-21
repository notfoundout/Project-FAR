from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from .model import CheckDefinition, Manifest

SUPPORTED_SCHEMA_VERSIONS = {"1.0"}


class ManifestError(ValueError):
    pass


def _tuple_strings(value: Any, field_name: str) -> tuple[str, ...]:
    if value is None:
        return ()
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        raise ManifestError(f"{field_name} must be a list of strings")
    return tuple(value)


def load_manifest(path: Path) -> Manifest:
    try:
        raw_bytes = path.read_bytes()
    except OSError as exc:
        raise ManifestError(f"cannot read manifest {path}: {exc}") from exc
    try:
        payload = json.loads(raw_bytes)
    except json.JSONDecodeError as exc:
        raise ManifestError(f"invalid JSON manifest {path}: {exc}") from exc
    if not isinstance(payload, dict):
        raise ManifestError("manifest root must be an object")

    schema_version = payload.get("schema_version")
    if schema_version not in SUPPORTED_SCHEMA_VERSIONS:
        raise ManifestError(
            f"unsupported manifest schema_version {schema_version!r}; supported={sorted(SUPPORTED_SCHEMA_VERSIONS)}"
        )

    raw_profiles = payload.get("profiles")
    if not isinstance(raw_profiles, dict) or not raw_profiles:
        raise ManifestError("profiles must be a nonempty object")
    profiles: dict[str, tuple[str, ...]] = {}
    for name, values in raw_profiles.items():
        if not isinstance(name, str) or not name:
            raise ManifestError("profile names must be nonempty strings")
        profiles[name] = _tuple_strings(values, f"profiles.{name}")

    raw_checks = payload.get("checks")
    if not isinstance(raw_checks, list) or not raw_checks:
        raise ManifestError("checks must be a nonempty list")

    checks: dict[str, CheckDefinition] = {}
    for index, raw in enumerate(raw_checks):
        if not isinstance(raw, dict):
            raise ManifestError(f"checks[{index}] must be an object")
        check_id = raw.get("id")
        title = raw.get("title")
        if not isinstance(check_id, str) or not check_id:
            raise ManifestError(f"checks[{index}].id must be a nonempty string")
        if check_id in checks:
            raise ManifestError(f"duplicate check id: {check_id}")
        if not isinstance(title, str) or not title:
            raise ManifestError(f"checks[{index}].title must be a nonempty string")
        command = _tuple_strings(raw.get("command", []), f"checks[{index}].command")
        builtin = raw.get("builtin")
        if builtin is not None and not isinstance(builtin, str):
            raise ManifestError(f"checks[{index}].builtin must be a string or null")
        if not command and not builtin:
            raise ManifestError(f"check {check_id} must define command or builtin")
        if command and builtin:
            raise ManifestError(f"check {check_id} cannot define both command and builtin")

        definition = CheckDefinition(
            check_id=check_id,
            title=title,
            command=command,
            builtin=builtin,
            track=str(raw.get("track", "repository")),
            category=str(raw.get("category", "validation")),
            severity=str(raw.get("severity", "required")),
            profiles=_tuple_strings(raw.get("profiles", []), f"checks[{index}].profiles"),
            depends_on=_tuple_strings(raw.get("depends_on", []), f"checks[{index}].depends_on"),
            inputs=_tuple_strings(raw.get("inputs", []), f"checks[{index}].inputs"),
            outputs=_tuple_strings(raw.get("outputs", []), f"checks[{index}].outputs"),
            timeout_seconds=int(raw.get("timeout_seconds", 300)),
            cacheable=bool(raw.get("cacheable", True)),
            deterministic=bool(raw.get("deterministic", True)),
            sandbox_copy=bool(raw.get("sandbox_copy", False)),
            expect_no_changes=bool(raw.get("expect_no_changes", False)),
            trace_dependencies=bool(raw.get("trace_dependencies", True)),
            allow_network=bool(raw.get("allow_network", False)),
            protected=bool(raw.get("protected", False)),
            failure_code=str(raw.get("failure_code", "FAR-VAL-TEST-001")),
            description=str(raw.get("description", "")),
        )
        if definition.timeout_seconds <= 0:
            raise ManifestError(f"check {check_id} timeout_seconds must be positive")
        if definition.allow_network and definition.deterministic:
            raise ManifestError(f"deterministic check {check_id} may not allow network access")
        checks[check_id] = definition

    protected_checks = _tuple_strings(payload.get("protected_checks", []), "protected_checks")
    global_paths = _tuple_strings(payload.get("global_invalidation_paths", []), "global_invalidation_paths")
    manifest = Manifest(
        schema_version=schema_version,
        profiles=profiles,
        protected_checks=protected_checks,
        global_invalidation_paths=global_paths,
        checks=checks,
        manifest_path=path,
        manifest_hash=hashlib.sha256(raw_bytes).hexdigest(),
    )
    validate_manifest(manifest)
    return manifest


def validate_manifest(manifest: Manifest) -> None:
    check_ids = set(manifest.checks)
    for profile, entries in manifest.profiles.items():
        unknown = sorted(set(entries) - check_ids)
        if unknown:
            raise ManifestError(f"profile {profile} references unknown checks: {unknown}")
    for check in manifest.checks.values():
        unknown = sorted(set(check.depends_on) - check_ids)
        if unknown:
            raise ManifestError(f"check {check.check_id} has unknown dependencies: {unknown}")
        unknown_profiles = sorted(set(check.profiles) - set(manifest.profiles))
        if unknown_profiles:
            raise ManifestError(f"check {check.check_id} references unknown profiles: {unknown_profiles}")
    missing_protected = sorted(set(manifest.protected_checks) - check_ids)
    if missing_protected:
        raise ManifestError(f"protected checks missing: {missing_protected}")
    for protected_id in manifest.protected_checks:
        check = manifest.checks[protected_id]
        if not check.protected:
            raise ManifestError(f"protected check {protected_id} is not marked protected")
        for required_profile in ("pr-fast", "pr-full", "full", "release"):
            if required_profile in manifest.profiles and protected_id not in manifest.profiles[required_profile]:
                raise ManifestError(f"protected check {protected_id} missing from {required_profile}")
    _validate_acyclic(manifest)


def _validate_acyclic(manifest: Manifest) -> None:
    state: dict[str, int] = {}
    path: list[str] = []

    def visit(check_id: str) -> None:
        marker = state.get(check_id, 0)
        if marker == 2:
            return
        if marker == 1:
            try:
                start = path.index(check_id)
            except ValueError:
                start = 0
            cycle = path[start:] + [check_id]
            raise ManifestError("dependency cycle: " + " -> ".join(cycle))
        state[check_id] = 1
        path.append(check_id)
        for dependency in manifest.checks[check_id].depends_on:
            visit(dependency)
        path.pop()
        state[check_id] = 2

    for check_id in manifest.checks:
        visit(check_id)
