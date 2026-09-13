"""Public hardened FAR intake facade.

The semantic core is kept in ``_intake_v1_core``.  This facade owns input-boundary
hardening that must run before schema or semantic interpretation: exact JSON-native
Python types, strict JSON parsing, and terminal saturation recheck completeness.
"""
from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

from . import _intake_v1_core as _core

# Preserve the public surface of the original module.  Private helpers are exposed
# below only where this facade intentionally replaces them.
for _name in dir(_core):
    if not _name.startswith("_"):
        globals()[_name] = getattr(_core, _name)

_core_validate_manifest = _core.validate_manifest


def _json_pointer_token(value: str) -> str:
    return value.replace("~", "~0").replace("/", "~1")


def _json_native_errors(value: Any, path: str = "$") -> list[str]:
    """Reject values that cannot exist in a strict JSON data model.

    Programmatic callers can otherwise bypass the parser and supply Python-only
    containers, non-string object keys, custom scalar subclasses, or non-finite
    floats.  Reject them before JSON Schema sees the instance so the schema and
    canonical hash operate on the same data model.
    """
    value_type = type(value)
    if value_type is dict:
        errors: list[str] = []
        for key, child in value.items():
            if type(key) is not str:
                errors.append(
                    f"{path} has non-string object key {key!r}; value is not canonical-JSON serializable"
                )
                continue
            errors.extend(_json_native_errors(child, f"{path}/{_json_pointer_token(key)}"))
        return errors
    if value_type is list:
        errors: list[str] = []
        for index, child in enumerate(value):
            errors.extend(_json_native_errors(child, f"{path}/{index}"))
        return errors
    if value is None or value_type in {str, int, bool}:
        return []
    if value_type is float:
        if math.isfinite(value):
            return []
        return [f"{path} is not canonical-JSON serializable: non-finite number"]
    return [
        f"{path} is not canonical-JSON serializable: unsupported Python type {value_type.__name__}"
    ]


def _terminal_saturation_errors(
    protocol: dict[str, Any],
    registered_query_ids: set[str],
    registered_source_ids: set[str],
) -> list[str]:
    """Require the terminating zero-new round itself to recheck the full registry."""
    observations = protocol.get("saturation_observations")
    if not isinstance(observations, list) or not observations:
        return []
    final = observations[-1]
    if not isinstance(final, dict):
        return []
    final_query_ids = set(final.get("query_ids", []))
    final_source_ids = set(final.get("source_ids", []))
    errors: list[str] = []
    missing_queries = sorted(registered_query_ids - final_query_ids)
    if missing_queries:
        errors.append(
            "final saturation observation does not recheck registered queries: "
            + ", ".join(missing_queries)
        )
    missing_sources = sorted(registered_source_ids - final_source_ids)
    if missing_sources:
        errors.append(
            "final saturation observation does not recheck registered sources: "
            + ", ".join(missing_sources)
        )
    return errors


def validate_manifest(manifest: Any, *, require_complete: bool | None = None) -> list[str]:
    native_errors = _json_native_errors(manifest)
    if native_errors:
        return native_errors

    errors = _core_validate_manifest(manifest, require_complete=require_complete)
    if errors:
        return errors

    effective_complete = require_complete
    if effective_complete is None:
        effective_complete = manifest["freeze"]["status"] == "FROZEN"
    if effective_complete:
        protocol = manifest["discovery"]["search_protocol"]
        registered_query_ids = {row["id"] for row in protocol["queries"]}
        registered_source_ids = {row["id"] for row in manifest["discovery"]["sources"]}
        errors.extend(
            _terminal_saturation_errors(protocol, registered_query_ids, registered_source_ids)
        )
    return errors


def _reject_duplicate_object_pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON object key: {key}")
        result[key] = value
    return result


def _reject_nonfinite_constant(value: str) -> None:
    raise ValueError(f"non-finite JSON number is not permitted: {value}")


def _strict_json_loads(text: str) -> Any:
    data = json.loads(
        text,
        object_pairs_hook=_reject_duplicate_object_pairs,
        parse_constant=_reject_nonfinite_constant,
    )
    native_errors = _json_native_errors(data)
    if native_errors:
        raise ValueError("; ".join(native_errors))
    return data


def _load_schema() -> dict[str, Any]:
    schema = _strict_json_loads(_core.SCHEMA_PATH.read_text(encoding="utf-8"))
    if not isinstance(schema, dict):
        raise ValueError("intake schema root must be an object")
    _core.Draft202012Validator.check_schema(schema)
    return schema


def _load(path: str) -> dict[str, Any]:
    data = _strict_json_loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("manifest root must be an object")
    return data


# The core functions resolve these globals at call time.  Bind them to the hardened
# facade so freeze, aggregation, schema loading, and the CLI cannot bypass it.
_core.validate_manifest = validate_manifest
_core._load_schema = _load_schema
_core._load = _load

freeze_manifest = _core.freeze_manifest
aggregate_manifest = _core.aggregate_manifest
main = _core.main


if __name__ == "__main__":
    raise SystemExit(main())
