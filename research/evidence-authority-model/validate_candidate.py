#!/usr/bin/env python3
"""Schema-aware extension for FAR-EVIDENCE-AUTHORITY-MODEL-001.

The reviewed v1 entrypoint remains in ``validator_entrypoint_v1.py``. This
entrypoint adds independent discovery for self-registering proof records whose
canonical identifier field is ``id`` rather than ``proof_id``.
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
_spec = importlib.util.spec_from_file_location("evidence_authority_validator_v1", V1_PATH)
v1 = importlib.util.module_from_spec(_spec)
assert _spec.loader is not None
_spec.loader.exec_module(v1)
core = v1.core

CANONICAL_ID_PROOF_PATHWAY = "canonical_id_proof_records"
CANONICAL_ID_PROOF_SENTINEL = "theory/evaluation/fara-operator-w2-proof-v1.0.json"
_original_discover_proof_paths = core.discover_proof_paths
_original_validate_candidate = v1.validate_candidate
_original_execute_negative_controls = v1.execute_negative_controls


def _is_canonical_id_proof_record(source: str, payload: Any) -> bool:
    """Recognize repository proof records that self-register through ``id``."""
    if not isinstance(payload, dict) or not isinstance(payload.get("id"), str):
        return False
    path = pathlib.PurePosixPath(source)
    return (
        source.startswith(("theory/evaluation/", "theory/terminal/", "foundations/"))
        and path.suffix == ".json"
        and "proof" in path.name.lower()
    )


def discover_proof_paths(
    frozen: Any,
    disabled: set[str] | None = None,
) -> tuple[dict[str, set[str]], set[str], dict[str, str]]:
    disabled = set(disabled or set())
    inventory, executed, discovery_inputs = _original_discover_proof_paths(
        frozen, disabled
    )
    if CANONICAL_ID_PROOF_PATHWAY in disabled:
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
    if CANONICAL_ID_PROOF_SENTINEL not in result.get("proof_inventory", {}):
        result["errors"].append(
            f"missing_canonical_id_proof_record:{CANONICAL_ID_PROOF_SENTINEL}"
        )
    result["valid"] = not result["errors"]
    return result


def execute_negative_controls(frozen: Any) -> list[dict[str, Any]]:
    controls = _original_execute_negative_controls(frozen)
    result = validate_candidate(
        frozen,
        disabled_pathways={CANONICAL_ID_PROOF_PATHWAY},
        enforce_research_only_placement=False,
    )
    expected = f"missing_canonical_id_proof_record:{CANONICAL_ID_PROOF_SENTINEL}"
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
    result["schema_version"] = "1.4"
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
