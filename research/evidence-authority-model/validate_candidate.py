#!/usr/bin/env python3
"""Schema-aware extension for FAR-EVIDENCE-AUTHORITY-MODEL-001.

The reviewed v1 entrypoint remains in ``validator_entrypoint_v1.py``. This
entrypoint applies the explicit Research candidate discovery extensions for
canonical ``id`` proof records and hash-locked artifact-map keys. It also
derives numeric priority direction from the candidate model rather than a
private validator default.
"""
from __future__ import annotations

import argparse
import json
import pathlib
from typing import Any, Iterable

import yaml

HERE = pathlib.Path(__file__).resolve().parent
V1_PATH = HERE / "validator_entrypoint_v1.py"
DISCOVERY_SCHEMA_PATH = HERE / "candidate/proof-discovery-schema-v1.0.json"
_spec = __import__("importlib.util").util.spec_from_file_location(
    "evidence_authority_validator_v1", V1_PATH
)
v1 = __import__("importlib.util").util.module_from_spec(_spec)
assert _spec.loader is not None
_spec.loader.exec_module(v1)
core = v1.core

CANONICAL_ID_PROOF_PATHWAY = "canonical_id_proof_records"
ARTIFACT_MAP_KEY_PATHWAY = "artifact_map_key_paths"
LOWER_PRIORITY_DECLARATION = "lower numeric rank means higher authority"
HIGHER_PRIORITY_DECLARATION = "higher numeric rank means higher authority"
_original_discover_proof_paths = core.discover_proof_paths
_original_validate_candidate = v1.validate_candidate
_original_execute_negative_controls = v1.execute_negative_controls


def _load_discovery_schema() -> dict[str, Any]:
    return json.loads(DISCOVERY_SCHEMA_PATH.read_text(encoding="utf-8"))


def _rule(rule_id: str) -> dict[str, Any]:
    schema = _load_discovery_schema()
    for rule in schema.get("rules", []):
        if rule.get("rule_id") == rule_id:
            return rule
    return {}


def _canonical_id_rule() -> dict[str, Any]:
    return _rule("canonical_id_proof_record")


def _artifact_map_key_rule() -> dict[str, Any]:
    return _rule("hash_locked_artifact_map_keys")


def _validate_discovery_schema() -> list[str]:
    schema = _load_discovery_schema()
    errors: list[str] = []
    if schema.get("status") != "Research" or schema.get("active") is not False:
        errors.append("proof_discovery_schema_not_inactive_research")
    if schema.get("pathway") != "schema_aware_proof_discovery":
        errors.append("proof_discovery_schema_pathway_mismatch")

    canonical_rule = _canonical_id_rule()
    canonical_required = {
        "identifier_field": "id",
        "file_extension": ".json",
        "filename_must_contain": "proof",
        "negative_control": "disable_canonical_id_proof_record_schema",
    }
    for field, expected in canonical_required.items():
        if canonical_rule.get(field) != expected:
            errors.append(f"proof_discovery_schema_field_mismatch:{field}")
    if not isinstance(canonical_rule.get("roots"), list) or not canonical_rule["roots"]:
        errors.append("proof_discovery_schema_roots_missing")
    if not isinstance(canonical_rule.get("required_sentinels"), list) or not canonical_rule[
        "required_sentinels"
    ]:
        errors.append("proof_discovery_schema_sentinels_missing")

    map_rule = _artifact_map_key_rule()
    map_required = {
        "source_file_extension": ".json",
        "registered_key_extension": ".json",
        "negative_control": "disable_hash_locked_artifact_map_key_schema",
    }
    for field, expected in map_required.items():
        if map_rule.get(field) != expected:
            errors.append(f"artifact_map_key_schema_field_mismatch:{field}")
    for field in ("mapping_fields", "roots", "required_sentinels"):
        value = map_rule.get(field)
        if not isinstance(value, list) or not value:
            errors.append(f"artifact_map_key_schema_{field}_missing")
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


def _artifact_map_keys(value: Any, mapping_fields: set[str]) -> Iterable[str]:
    if isinstance(value, dict):
        for key, child in value.items():
            if key in mapping_fields and isinstance(child, dict):
                for registered_path in child:
                    if isinstance(registered_path, str):
                        yield registered_path
            yield from _artifact_map_keys(child, mapping_fields)
    elif isinstance(value, list):
        for child in value:
            yield from _artifact_map_keys(child, mapping_fields)


def _source_matches_artifact_map_rule(source: str) -> bool:
    rule = _artifact_map_key_rule()
    roots = tuple(item for item in rule.get("roots", []) if isinstance(item, str))
    extension = rule.get("source_file_extension")
    return bool(roots) and source.startswith(roots) and source.endswith(str(extension))


def discover_proof_paths(
    frozen: Any,
    disabled: set[str] | None = None,
) -> tuple[dict[str, set[str]], set[str], dict[str, str]]:
    disabled = set(disabled or set())
    inventory, executed, discovery_inputs = _original_discover_proof_paths(
        frozen, disabled
    )

    canonical_enabled = (
        CANONICAL_ID_PROOF_PATHWAY not in disabled
        and "self_registering_records" not in disabled
    )
    artifact_map_enabled = ARTIFACT_MAP_KEY_PATHWAY not in disabled
    canonical_found = False
    artifact_map_found = False
    mapping_fields = {
        item
        for item in _artifact_map_key_rule().get("mapping_fields", [])
        if isinstance(item, str)
    }
    registered_extension = str(
        _artifact_map_key_rule().get("registered_key_extension", "")
    )

    for source in frozen.structured_metadata_paths():
        if not source.endswith(".json"):
            continue
        try:
            payload = frozen.load_json(source)
        except (json.JSONDecodeError, yaml.YAMLError, UnicodeDecodeError):
            continue

        if canonical_enabled and _is_canonical_id_proof_record(source, payload):
            inventory[source].add("self_registering_records")
            canonical_found = True

        if artifact_map_enabled and _source_matches_artifact_map_rule(source):
            for registered_path in _artifact_map_keys(payload, mapping_fields):
                if (
                    core.syntactic_repo_path(registered_path)
                    and pathlib.PurePosixPath(registered_path).suffix
                    == registered_extension
                ):
                    inventory[registered_path].add("artifact_map_keys")
                    artifact_map_found = True

    if canonical_found:
        executed.add("self_registering_records")
    if artifact_map_found:
        executed.add("artifact_map_keys")
    return inventory, executed, discovery_inputs


def _declared_priority_order(model_text: str) -> tuple[str, list[str]]:
    lower_text = model_text.lower()
    lower_declared = LOWER_PRIORITY_DECLARATION in lower_text
    higher_declared = HIGHER_PRIORITY_DECLARATION in lower_text
    if lower_declared and not higher_declared:
        return "lower_is_higher", []
    if higher_declared and not lower_declared:
        return "higher_is_higher", []
    if lower_declared and higher_declared:
        return "lower_is_higher", ["priority_order_declaration_ambiguous"]
    return "lower_is_higher", ["priority_order_declaration_missing"]


def validate_candidate(*args: Any, **kwargs: Any) -> dict[str, Any]:
    model_text = kwargs.get("model_text")
    if model_text is None:
        model_text = core.MODEL_PATH.read_text(encoding="utf-8")
    declared_order, declaration_errors = _declared_priority_order(model_text)
    result = _original_validate_candidate(
        *args,
        numeric_priority_order=declared_order,
        **kwargs,
    )
    result["errors"].extend(declaration_errors)
    result["errors"].extend(_validate_discovery_schema())

    for sentinel in _canonical_id_rule().get("required_sentinels", []):
        if sentinel not in result.get("proof_inventory", {}):
            result["errors"].append(f"missing_canonical_id_proof_record:{sentinel}")
    for sentinel in _artifact_map_key_rule().get("required_sentinels", []):
        if sentinel not in result.get("proof_inventory", {}):
            result["errors"].append(f"missing_hash_locked_artifact_map_key:{sentinel}")

    probe = result.get("unequal_priority_probe", {})
    if probe.get("numeric_priority_order") != declared_order:
        result["errors"].append("priority_probe_contract_order_mismatch")
    result["declared_numeric_priority_order"] = declared_order
    result["valid"] = not result["errors"]
    return result


def _record_control(
    controls: list[dict[str, Any]],
    control_id: str,
    result: dict[str, Any],
    expected_prefix: str,
) -> None:
    observed = [error for error in result["errors"] if error.startswith(expected_prefix)]
    controls.append(
        {
            "control_id": control_id,
            "expected_failure": expected_prefix,
            "observed_failures": observed,
            "detected": bool(observed) and not result["valid"],
        }
    )


def execute_negative_controls(frozen: Any) -> list[dict[str, Any]]:
    controls = [
        item
        for item in _original_execute_negative_controls(frozen)
        if item.get("control_id") != "reverse_numeric_priority_order"
    ]

    result = validate_candidate(
        frozen,
        disabled_pathways={CANONICAL_ID_PROOF_PATHWAY},
        enforce_research_only_placement=False,
    )
    _record_control(
        controls,
        "disable_canonical_id_proof_record_schema",
        result,
        "missing_canonical_id_proof_record:",
    )

    result = validate_candidate(
        frozen,
        disabled_pathways={ARTIFACT_MAP_KEY_PATHWAY},
        enforce_research_only_placement=False,
    )
    _record_control(
        controls,
        "disable_hash_locked_artifact_map_key_schema",
        result,
        "missing_hash_locked_artifact_map_key:",
    )

    model_text = core.MODEL_PATH.read_text(encoding="utf-8")
    reversed_model = model_text.replace(
        "Lower numeric rank means higher authority.",
        "Higher numeric rank means higher authority.",
    ).replace(
        "lower rank is always higher authority",
        "higher rank is always higher authority",
    )
    result = validate_candidate(
        frozen,
        model_text=reversed_model,
        enforce_research_only_placement=False,
    )
    _record_control(
        controls,
        "reverse_declared_numeric_priority_order",
        result,
        "priority_probe_wrong_winner:Denied",
    )
    return controls


core.discover_proof_paths = discover_proof_paths
core.validate_candidate = validate_candidate
core.execute_negative_controls = execute_negative_controls


def run_full_validation(*, enforce_research_only_placement: bool = True) -> dict[str, Any]:
    result = core.run_full_validation(
        enforce_research_only_placement=enforce_research_only_placement
    )
    result["schema_version"] = "1.6"
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
