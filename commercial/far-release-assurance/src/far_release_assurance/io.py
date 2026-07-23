"""Deterministic JSON ingestion and canonical export for FAR release packages."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Mapping

from .model import EvidenceStatus, MachineryItem, ReasoningEvent, ReleasePackage

SCHEMA_VERSION = "far-release-package/0.1"


class ReleasePackageError(ValueError):
    """Raised when an input package is malformed or semantically invalid."""


def _require_mapping(value: object, field: str) -> Mapping[str, Any]:
    if not isinstance(value, dict):
        raise ReleasePackageError(f"{field} must be an object")
    return value


def _require_text(value: object, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ReleasePackageError(f"{field} must be a non-empty string")
    return value


def _text_tuple(value: object, field: str) -> tuple[str, ...]:
    if value is None:
        return ()
    if not isinstance(value, list) or any(not isinstance(item, str) or not item for item in value):
        raise ReleasePackageError(f"{field} must be an array of non-empty strings")
    return tuple(value)


def _optional_bool(value: object, field: str) -> bool | None:
    if value is None:
        return None
    if not isinstance(value, bool):
        raise ReleasePackageError(f"{field} must be boolean or null")
    return value


def _status(value: object, field: str) -> EvidenceStatus:
    try:
        return EvidenceStatus(_require_text(value, field))
    except ValueError as exc:
        raise ReleasePackageError(f"{field} has unsupported evidence status: {value!r}") from exc


def package_from_dict(payload: Mapping[str, Any]) -> ReleasePackage:
    if payload.get("schema_version") != SCHEMA_VERSION:
        raise ReleasePackageError(f"schema_version must equal {SCHEMA_VERSION}")

    machinery_payload = payload.get("machinery")
    events_payload = payload.get("events")
    if not isinstance(machinery_payload, list):
        raise ReleasePackageError("machinery must be an array")
    if not isinstance(events_payload, list):
        raise ReleasePackageError("events must be an array")

    machinery: list[MachineryItem] = []
    for index, raw in enumerate(machinery_payload):
        item = _require_mapping(raw, f"machinery[{index}]")
        attributes = item.get("attributes", {})
        if not isinstance(attributes, dict):
            raise ReleasePackageError(f"machinery[{index}].attributes must be an object")
        machinery.append(
            MachineryItem(
                machinery_id=_require_text(item.get("machinery_id"), f"machinery[{index}].machinery_id"),
                kind=_require_text(item.get("kind"), f"machinery[{index}].kind"),
                name=_require_text(item.get("name"), f"machinery[{index}].name"),
                version=item.get("version") if isinstance(item.get("version"), str) else None,
                digest=item.get("digest") if isinstance(item.get("digest"), str) else None,
                required_dependencies=_text_tuple(item.get("required_dependencies", []), f"machinery[{index}].required_dependencies"),
                evidence_status=_status(item.get("evidence_status", EvidenceStatus.UNKNOWN.value), f"machinery[{index}].evidence_status"),
                declared=item.get("declared", True) if isinstance(item.get("declared", True), bool) else True,
                effective=_optional_bool(item.get("effective"), f"machinery[{index}].effective"),
                valid=_optional_bool(item.get("valid"), f"machinery[{index}].valid"),
                mutable=item.get("mutable", False) if isinstance(item.get("mutable", False), bool) else False,
                external=item.get("external", False) if isinstance(item.get("external", False), bool) else False,
                attributes=attributes,
            )
        )

    events: list[ReasoningEvent] = []
    for index, raw in enumerate(events_payload):
        event = _require_mapping(raw, f"events[{index}]")
        identity_context = event.get("identity_context", {})
        attributes = event.get("attributes", {})
        if not isinstance(identity_context, dict) or any(not isinstance(k, str) or not isinstance(v, str) for k, v in identity_context.items()):
            raise ReleasePackageError(f"events[{index}].identity_context must map strings to strings")
        if not isinstance(attributes, dict):
            raise ReleasePackageError(f"events[{index}].attributes must be an object")
        sequence = event.get("sequence")
        if not isinstance(sequence, int) or sequence < 0:
            raise ReleasePackageError(f"events[{index}].sequence must be a non-negative integer")
        events.append(
            ReasoningEvent(
                event_id=_require_text(event.get("event_id"), f"events[{index}].event_id"),
                run_id=_require_text(event.get("run_id"), f"events[{index}].run_id"),
                release_id=_require_text(event.get("release_id"), f"events[{index}].release_id"),
                sequence=sequence,
                event_type=_require_text(event.get("event_type"), f"events[{index}].event_type"),
                subject_id=_require_text(event.get("subject_id"), f"events[{index}].subject_id"),
                object_ids=_text_tuple(event.get("object_ids", []), f"events[{index}].object_ids"),
                evidence_refs=_text_tuple(event.get("evidence_refs", []), f"events[{index}].evidence_refs"),
                dependency_refs=_text_tuple(event.get("dependency_refs", []), f"events[{index}].dependency_refs"),
                machinery_refs=_text_tuple(event.get("machinery_refs", []), f"events[{index}].machinery_refs"),
                identity_context=identity_context,
                status=_status(event.get("status", EvidenceStatus.UNKNOWN.value), f"events[{index}].status"),
                source_ref=event.get("source_ref") if isinstance(event.get("source_ref"), str) else None,
                attributes=attributes,
            )
        )

    package = ReleasePackage(
        release_id=_require_text(payload.get("release_id"), "release_id"),
        source_commit=_require_text(payload.get("source_commit"), "source_commit"),
        machinery=tuple(machinery),
        events=tuple(events),
        decision_roots=_text_tuple(payload.get("decision_roots", []), "decision_roots"),
        release_roots=_text_tuple(payload.get("release_roots", []), "release_roots"),
        replay_completeness=payload.get("replay_completeness") if isinstance(payload.get("replay_completeness"), (int, float)) else None,
        output_metrics=payload.get("output_metrics", {}) if isinstance(payload.get("output_metrics", {}), dict) else {},
    )
    _validate_semantics(package)
    return package


def _validate_semantics(package: ReleasePackage) -> None:
    if package.replay_completeness is not None and not 0.0 <= package.replay_completeness <= 1.0:
        raise ReleasePackageError("replay_completeness must be between 0 and 1")
    if any(event.release_id != package.release_id for event in package.events):
        raise ReleasePackageError("every event release_id must match package release_id")
    event_ids = [event.event_id for event in package.events]
    if len(event_ids) != len(set(event_ids)):
        raise ReleasePackageError("event_id values must be unique")
    sequences = [event.sequence for event in package.events]
    if sequences != sorted(sequences) or len(sequences) != len(set(sequences)):
        raise ReleasePackageError("event sequence values must be unique and ordered")
    machinery_ids = {item.machinery_id for item in package.machinery}
    for event in package.events:
        missing = sorted(set(event.machinery_refs) - machinery_ids)
        if missing:
            raise ReleasePackageError(f"event {event.event_id} references missing machinery: {', '.join(missing)}")


def package_to_dict(package: ReleasePackage) -> dict[str, Any]:
    def machinery_dict(item: MachineryItem) -> dict[str, Any]:
        return {
            "machinery_id": item.machinery_id,
            "kind": item.kind,
            "name": item.name,
            "version": item.version,
            "digest": item.digest,
            "required_dependencies": list(item.required_dependencies),
            "evidence_status": item.evidence_status.value,
            "declared": item.declared,
            "effective": item.effective,
            "valid": item.valid,
            "mutable": item.mutable,
            "external": item.external,
            "attributes": dict(item.attributes),
        }

    def event_dict(event: ReasoningEvent) -> dict[str, Any]:
        return {
            "event_id": event.event_id,
            "run_id": event.run_id,
            "release_id": event.release_id,
            "sequence": event.sequence,
            "event_type": event.event_type,
            "subject_id": event.subject_id,
            "object_ids": list(event.object_ids),
            "evidence_refs": list(event.evidence_refs),
            "dependency_refs": list(event.dependency_refs),
            "machinery_refs": list(event.machinery_refs),
            "identity_context": dict(event.identity_context),
            "status": event.status.value,
            "source_ref": event.source_ref,
            "attributes": dict(event.attributes),
        }

    return {
        "schema_version": SCHEMA_VERSION,
        "release_id": package.release_id,
        "source_commit": package.source_commit,
        "machinery": [machinery_dict(item) for item in sorted(package.machinery, key=lambda item: item.machinery_id)],
        "events": [event_dict(event) for event in sorted(package.events, key=lambda event: (event.sequence, event.event_id))],
        "decision_roots": sorted(package.decision_roots),
        "release_roots": sorted(package.release_roots),
        "replay_completeness": package.replay_completeness,
        "output_metrics": dict(sorted(package.output_metrics.items())),
    }


def canonical_json(package: ReleasePackage) -> str:
    return json.dumps(package_to_dict(package), sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n"


def package_digest(package: ReleasePackage) -> str:
    return hashlib.sha256(canonical_json(package).encode("utf-8")).hexdigest()


def load_package(path: str | Path) -> ReleasePackage:
    try:
        payload = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ReleasePackageError(f"cannot read release package: {exc}") from exc
    return package_from_dict(_require_mapping(payload, "document"))


def write_package(package: ReleasePackage, path: str | Path) -> None:
    Path(path).write_text(canonical_json(package), encoding="utf-8")
