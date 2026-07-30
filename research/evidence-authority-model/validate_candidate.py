#!/usr/bin/env python3
"""Schema-aware extension for FAR-EVIDENCE-AUTHORITY-MODEL-001.

The reviewed v1 entrypoint remains in ``validator_entrypoint_v1.py``. This
entrypoint applies the explicit Research candidate discovery extension for
self-registering proof records whose canonical identifier is ``id`` rather
than ``proof_id``.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import pathlib
from typing import Any

import yaml

HERE = pathlib.Path(__file__).resolve().parent
V1_PATH = HERE / "validator_entrypoint_v1.py"
DISCOVERY_SCHEMA_PATH = HERE / "candidate/proof-discovery-schema-v1.0.json"
_spec = importlib.util.spec_from_file_location("evidence_authority_validator_v1", V1_PATH)
v1 = importlib.util.module_from_spec(_spec)
assert _spec.loader is not None
_spec.loader.exec_module(v1)
core = v1.core

CANONICAL_ID_PROOF_PATHWAY = "canonical_id_proof_records"
_original_discover_proof_paths = core.discover_proof_paths
_original_validate_candidate = v1.validate_candidate
_original_execute_negative_controls = v1.execute_negative_controls


def _load_discovery_schema() -> dict[str, Any]:
    return json.loads(DISCOVERY_SCHEMA_PATH.read_text(encoding="utf-8"))


def _canonical_id_rule() -> dict[str, Any]:
    schema = _load_discovery_schema()
    for rule in schema.get("rules", []):
        if rule.get("rule_id") == "canonical_id_proof_record":
            return rule
    return {}


def _validate_discovery_schema() -> list[str]:
    schema = _load_discovery_schema()
    errors: list[str] = []
    if schema.get("status") != "Research" or schema.get("active") is not False:
        errors.append("proof_discovery_schema_not_inactive_research")
    if schema.get("pathway") != "self_registering_records":
        errors.append("proof_discovery_schema_pathway_mismatch")
    rule = _canonical_id_rule()
    required = {
        "identifier_field": "id",
        "file_extension": ".json",
        "filename_must_contain": "proof",
        "negative_control": "disable_canonical_id_proof_record_schema",
    }
    for field, expected in required.items():
        if rule.get(field) != expected:
            errors.append(f"proof_discovery_schema_field_mismatch:{field}")
    roots = rule.get("roots")
    if not isinstance(roots, list) or not roots:
        errors.append("proof_discovery_schema_roots_missing")
    sentinels = rule.get("required_sentinels")
    if not isinstance(sentinels, list) or not sentinels:
        errors.append("proof_discovery_schema_sentinels_missing")
    return errors


def _is_canonical_id_proof_record(source: str, payload: Any) -> bool:
    """Recognize records according to the declared candidate schema extension."""
    rule = _canonical_id_rule()
    identifier_field = rule.get("identifier_field")
    if not isinstance(payload, dict) or not isinstance(payload.get(identifier_field), str):
        return False
    roots = tuple(item for item in rule.get("roots", []) if isinstance(item, str))
    extension = rule.get("file_extension")
    token = str(rule.get("filename_must_contain", "")).lower()
    path = pathlib.PurePosixPath(source)
    return (
        bool(roots)
        and source.startswith(roots)
        and path.suffix == extension
        and bool(token)
        and token in path.name.lower()
    )


def discover_proof_paths(
    frozen: Any,
    disabled: set[str] | None = None,
) -> tuple[dict[str, set[str]], set[str], dict[str, str]]:
    disabled = set(disabled or set())
    inventory, executed, discovery_inputs = _original_discover_proof_paths(
        frozen, disabled
    )
    if (
        CANONICAL_ID_PROOF_PATHWAY in disabled
        or "self_registering_records" in disabled
    ):
        return inventory, executed, discovery_inputs

    found = False
    for source in frozen.structured_metadata_paths():
        if not source.endswith(".json"):
            continue
        try:
            payload = frozen.load_json(source)
        except (json.JSONDecodeError, yaml.YAMLError, UnicodeDecodeError):
            continue
        if _is_canonical_id_proof_record(source, payload):
            inventory[source].add("self_registering_records")
            found = True
    if found:
        executed.add("self_registering_records")
    return inventory, executed, discovery_inputs


def validate_candidate(*args: Any, **kwargs: Any) -> dict[str, Any]:
    result = _original_validate_candidate(*args, **kwargs)
    result["errors"].extend(_validate_discovery_schema())
    for sentinel in _canonical_id_rule().get("required_sentinels", []):
        if sentinel not in result.get("proof_inventory", {}):
            result["errors"].append(f"missing_canonical_id_proof_record:{sentinel}")
    result["valid"] = not result["errors"]
    return result


def execute_negative_controls(frozen: Any) -> list[dict[str, Any]]:
    controls = _original_execute_negative_controls(frozen)
    result = validate_candidate(
        frozen,
        disabled_pathways={CANONICAL_ID_PROOF_PATHWAY},
        enforce_research_only_placement=False,
    )
    expected = "missing_canonical_id_proof_record:"
    observed = [error for error in result["errors"] if error.startswith(expected)]
    controls.append(
        {
            "control_id": "disable_canonical_id_proof_record_schema",
            "expected_failure": expected,
            "observed_failures": observed,
            "detected": bool(observed) and not result["valid"],
        }
    )
    return controls


core.discover_proof_paths = discover_proof_paths
core.validate_candidate = validate_candidate
core.execute_negative_controls = execute_negative_controls


def run_full_validation(*, enforce_research_only_placement: bool = True) -> dict[str, Any]:
    result = core.run_full_validation(
        enforce_research_only_placement=enforce_research_only_placement
    )
    result["schema_version"] = "1.5"
    result["evidence_digest"] = core.canonical_digest(
        {key: value for key, value in result.items() if key != "evidence_digest"}
    )
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=pathlib.Path)
    parser.add_argument("--allow-canonical-staging", action="store_true")
    args = parser.parse_args()
    result = run_full_validation(
        enforce_research_only_placement=not args.allow_canonical_staging
    )
    rendered = json.dumps(result, indent=2, sort_keys=True)
    if args.output:
        args.output.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)
    return 0 if result["overall"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
