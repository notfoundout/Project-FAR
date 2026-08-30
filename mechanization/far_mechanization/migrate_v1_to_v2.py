"""Loss-explicit migration from far-ir/1.0 to far-ir/2.0.

The legacy document is first validated against its unchanged v1 schema. Because v1 does not
encode a comparison contract, migration never invents beta, r, decoder, quotient, model class,
interpretation profile, or frame semantics. Those W3 fields are materialized as explicit Unknown
values and the original primitive payload is preserved under legacy_document.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping, Sequence

from jsonschema import Draft202012Validator

from .contract_v2 import REPO_ROOT, validate_contract

V1_SCHEMA_PATH = REPO_ROOT / "schemas" / "far-document.schema.json"


def _canonical(value: object) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def validate_v1(document: object) -> tuple[str, ...]:
    schema = json.loads(V1_SCHEMA_PATH.read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema)
    return tuple(error.message for error in sorted(validator.iter_errors(document), key=lambda e: (tuple(e.path), e.message)))


def migrate(document: Mapping[str, Any], *, source_path: str = "legacy-document", created_at: str | None = None) -> dict[str, Any]:
    errors = validate_v1(document)
    if errors:
        raise ValueError("invalid far-ir/1.0 document: " + "; ".join(errors))
    if document.get("format_version") != "far-ir/1.0":
        raise ValueError("migration accepts far-ir/1.0 only")
    timestamp = created_at or datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    legacy_id = str(document["id"])
    unknown = "Not represented by far-ir/1.0; must be supplied and frozen explicitly before any non-Unknown W3 conclusion."
    migrated: dict[str, Any] = {
        "format_version": "far-ir/2.0",
        "id": f"{legacy_id}.w3",
        "contract": {
            "id": f"{legacy_id}.contract",
            "contract_version": "2.0-migrated-unfrozen",
            "mode": "Unknown",
            "source_domain": {"status": "Unknown", "kind": "Unknown", "description": unknown, "cases": []},
            "required_behavior": {"status": "Unknown", "description": unknown, "table": []},
            "representation": {"status": "Unknown", "description": unknown, "table": []},
            "observation_contexts": [{"id": "legacy.context.unknown", "description": unknown, "status": "Unknown"}],
            "admitted_transformations": [],
            "interpretation_profile": {"id": "legacy.interpretation.unknown", "description": unknown, "status": "Unknown"},
            "target_model_class": {"id": "legacy.target.unknown", "description": unknown, "status": "Unknown"},
            "frame": {"id": "legacy.frame.unknown", "description": unknown, "status": "Unknown"}
        },
        "report": {
            "outcome": "Unknown",
            "evidence": {"kind": "unknown", "reason": unknown},
            "failure_report": ["far-ir/1.0 contains no complete W3 comparison contract; semantic completion is required before factorization, collision, or quotient certification."]
        },
        "provenance": {
            "producer": "Project FAR far-ir/1.0 -> far-ir/2.0 loss-explicit migrator",
            "created_at": timestamp,
            "sources": [{"path": source_path, "sha256": hashlib.sha256(_canonical(document)).hexdigest()}],
            "notes": "Source hash is SHA-256 of canonical JSON primitive data, independent of source JSON/YAML formatting."
        },
        "freeze": {"status": "DRAFT", "frozen_at": None, "contract_sha256": None, "notes": "Migration cannot freeze semantics absent from v1."},
        "legacy_document": json.loads(json.dumps(document))
    }
    result = validate_contract(migrated)
    if not result.success:
        raise AssertionError("migrator produced invalid v2 document: " + "; ".join(f"{d.code}: {d.message}" for d in result.diagnostics))
    return migrated


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m mechanization.far_mechanization.migrate_v1_to_v2")
    parser.add_argument("input")
    parser.add_argument("output")
    parser.add_argument("--created-at", help="Deterministic RFC3339 timestamp for reproducible fixtures")
    args = parser.parse_args(argv)
    source = Path(args.input)
    try:
        primitive = json.loads(source.read_text(encoding="utf-8"))
        if not isinstance(primitive, dict):
            raise ValueError("root must be an object")
        result = migrate(primitive, source_path=str(source), created_at=args.created_at)
    except (OSError, json.JSONDecodeError, ValueError, AssertionError) as exc:
        print(f"FAIL: {exc}")
        return 1
    Path(args.output).write_text(json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
