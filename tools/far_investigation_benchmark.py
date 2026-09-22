#!/usr/bin/env python3
"""Fail-closed validator/analyzer entry point for FAR Investigation Benchmark v0.1."""

from __future__ import annotations

import argparse
import base64
import datetime as dt
import hashlib
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
ROOT_RESOLVED = ROOT.resolve()
SCHEMA = ROOT / "schemas/far-research-campaign-v1.schema.json"
BENCHMARK_DIR = "research/comparisons/far-investigation-benchmark-v0.1"
PREREG = "research/comparisons/far-investigation-benchmark-v0.1.md"
ZERO64 = "0" * 64
ANALYZABLE = {"unblinded", "completed", "completed_imported_sealed"}
FROZEN_OR_LATER = {"frozen", *ANALYZABLE}

REQUIRED_FROZEN_ARTIFACTS = {
    PREREG,
    f"{BENCHMARK_DIR}/freeze-contract-v0.1.md",
    f"{BENCHMARK_DIR}/case-selection-protocol-v0.1.md",
    f"{BENCHMARK_DIR}/adjudication-rubric-v0.1.md",
    f"{BENCHMARK_DIR}/reference-evidence-protocol-v0.1.md",
    f"{BENCHMARK_DIR}/condition-contracts-v0.1.md",
    f"{BENCHMARK_DIR}/resource-budget-v0.1.json",
    f"{BENCHMARK_DIR}/analysis-parameters-v0.1.json",
    f"{BENCHMARK_DIR}/candidate-frame.jsonl",
    f"{BENCHMARK_DIR}/cases.jsonl",
    f"{BENCHMARK_DIR}/replacement-frame.jsonl",
    f"{BENCHMARK_DIR}/case-selection-config.json",
    f"{BENCHMARK_DIR}/case-selection-declarations.json",
    f"{BENCHMARK_DIR}/condition-prompts.json",
    f"{BENCHMARK_DIR}/execution-schedule.json",
    f"{BENCHMARK_DIR}/reference-search-config.json",
    f"{BENCHMARK_DIR}/reference-evidence-manifest.json",
    f"{BENCHMARK_DIR}/environment-lock.json",
    f"{BENCHMARK_DIR}/mutation-config.json",
}

REQUIRED_SOURCE_PATHS = {
    "tools/far_investigation_benchmark.py",
    "frameworks/FAR/workflow.md",
    "schemas/far-research-campaign-v1.schema.json",
}

FROZEN_CONFIG_JSON = {
    f"{BENCHMARK_DIR}/resource-budget-v0.1.json",
    f"{BENCHMARK_DIR}/analysis-parameters-v0.1.json",
    f"{BENCHMARK_DIR}/case-selection-config.json",
    f"{BENCHMARK_DIR}/case-selection-declarations.json",
    f"{BENCHMARK_DIR}/condition-prompts.json",
    f"{BENCHMARK_DIR}/execution-schedule.json",
    f"{BENCHMARK_DIR}/reference-search-config.json",
    f"{BENCHMARK_DIR}/reference-evidence-manifest.json",
    f"{BENCHMARK_DIR}/environment-lock.json",
    f"{BENCHMARK_DIR}/mutation-config.json",
}

UNFROZEN_MARKERS = ("TO_BE_", "PLACEHOLDER")
UNFROZEN_EXACT = {"UNASSIGNED", "PREPARED_NOT_FROZEN"}


def load(path: pathlib.Path):
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: pathlib.Path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def safe_repo_path(raw: object):
    if not isinstance(raw, str) or not raw or "\\" in raw or "\x00" in raw:
        return None
    pure = pathlib.PurePosixPath(raw)
    if pure.is_absolute() or ".." in pure.parts or pure == pathlib.PurePosixPath("."):
        return None
    resolved = (ROOT / pure).resolve()
    try:
        resolved.relative_to(ROOT_RESOLVED)
    except ValueError:
        return None
    return resolved


def _json_key(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def _resolve_ref(root_schema, ref):
    if not isinstance(ref, str) or not ref.startswith("#/"):
        return None
    node = root_schema
    for part in ref[2:].split("/"):
        part = part.replace("~1", "/").replace("~0", "~")
        if not isinstance(node, dict) or part not in node:
            return None
        node = node[part]
    return node


def _type_matches(value, expected):
    if expected == "object":
        return isinstance(value, dict)
    if expected == "array":
        return isinstance(value, list)
    if expected == "string":
        return isinstance(value, str)
    if expected == "boolean":
        return isinstance(value, bool)
    if expected == "null":
        return value is None
    if expected == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    return False


def schema_errors(instance, schema, root_schema=None, path="$", *, quiet=False):
    """Validate the JSON-Schema subset used by far-research-campaign-v1.schema.json.

    The repository deliberately avoids a runtime dependency on a third-party JSON-Schema
    package, so this routine implements only the keywords present in the governed schema.
    Unknown schema keywords are ignored as annotations only when they do not affect validation.
    """
    root_schema = schema if root_schema is None else root_schema
    errors = []

    if "$ref" in schema:
        target = _resolve_ref(root_schema, schema["$ref"])
        if target is None:
            return [f"schema {path}: unresolved $ref {schema['$ref']!r}"]
        return schema_errors(instance, target, root_schema, path, quiet=quiet)

    if "oneOf" in schema:
        branches = [schema_errors(instance, sub, root_schema, path, quiet=True) for sub in schema["oneOf"]]
        matches = sum(not branch for branch in branches)
        if matches != 1:
            errors.append(f"schema {path}: expected exactly one oneOf branch, got {matches}")
            return errors

    if "const" in schema and instance != schema["const"]:
        errors.append(f"schema {path}: value must equal {schema['const']!r}")
    if "enum" in schema and instance not in schema["enum"]:
        errors.append(f"schema {path}: value is not in enum")

    expected_type = schema.get("type")
    if expected_type is not None and not _type_matches(instance, expected_type):
        errors.append(f"schema {path}: expected {expected_type}")
        return errors

    if isinstance(instance, str):
        if "minLength" in schema and len(instance) < schema["minLength"]:
            errors.append(f"schema {path}: string shorter than minLength")
        if "pattern" in schema and re.search(schema["pattern"], instance) is None:
            errors.append(f"schema {path}: string does not match pattern")

    if isinstance(instance, list):
        if "minItems" in schema and len(instance) < schema["minItems"]:
            errors.append(f"schema {path}: array shorter than minItems")
        if schema.get("uniqueItems"):
            keys = [_json_key(v) for v in instance]
            if len(keys) != len(set(keys)):
                errors.append(f"schema {path}: array items must be unique")
        item_schema = schema.get("items")
        if isinstance(item_schema, dict):
            for i, value in enumerate(instance):
                errors.extend(schema_errors(value, item_schema, root_schema, f"{path}[{i}]", quiet=quiet))

    if isinstance(instance, dict):
        required = schema.get("required", [])
        for key in required:
            if key not in instance:
                errors.append(f"schema {path}: missing required property {key!r}")
        properties = schema.get("properties", {})
        additional = schema.get("additionalProperties", True)
        for key, value in instance.items():
            child_path = f"{path}.{key}"
            if key in properties:
                errors.extend(schema_errors(value, properties[key], root_schema, child_path, quiet=quiet))
            elif additional is False:
                errors.append(f"schema {path}: additional property {key!r} is not allowed")
            elif isinstance(additional, dict):
                errors.extend(schema_errors(value, additional, root_schema, child_path, quiet=quiet))

    return errors


def find_unfrozen(value, path="$"):
    findings = []
    if isinstance(value, str):
        if value in UNFROZEN_EXACT or any(marker in value for marker in UNFROZEN_MARKERS) or value.endswith("_NOT_FROZEN"):
            findings.append(path)
    elif isinstance(value, dict):
        for key, child in value.items():
            findings.extend(find_unfrozen(child, f"{path}.{key}"))
    elif isinstance(value, list):
        for i, child in enumerate(value):
            findings.extend(find_unfrozen(child, f"{path}[{i}]"))
    return findings


def _parse_time(value):
    if not isinstance(value, str) or not value:
        return None
    try:
        parsed = dt.datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    if parsed.tzinfo is None:
        return None
    return parsed


def _artifact_map(records, label, errors):
    result = {}
    for i, record in enumerate(records if isinstance(records, list) else []):
        if not isinstance(record, dict):
            continue
        raw = record.get("path")
        if raw in result:
            errors.append(f"{label}: duplicate path {raw}")
        result[raw] = record
        fp = safe_repo_path(raw)
        if fp is None:
            errors.append(f"{label}[{i}]: unsafe repository path {raw!r}")
    return result


def _verify_records(records, label, status, errors):
    for i, record in enumerate(records if isinstance(records, list) else []):
        if not isinstance(record, dict):
            continue
        raw = record.get("path")
        digest = record.get("sha256")
        fp = safe_repo_path(raw)
        if fp is None:
            continue
        verify = record.get("verify_current_path") is True
        if verify and not fp.exists():
            errors.append(f"{label}[{i}]: path missing: {raw}")
            continue
        if status in FROZEN_OR_LATER and digest == ZERO64:
            errors.append(f"{label}[{i}]: frozen-or-later record retains zero hash sentinel: {raw}")
        if verify and fp.exists() and isinstance(digest, str) and digest != ZERO64 and digest != sha256(fp):
            errors.append(f"{label}[{i}]: hash mismatch: {raw}")


def _require_verified_paths(path_map, required, label, errors):
    for path in sorted(required):
        record = path_map.get(path)
        if record is None:
            errors.append(f"frozen-or-later manifest missing required {label}: {path}")
            continue
        if record.get("verify_current_path") is not True:
            errors.append(f"required {label} must set verify_current_path=true: {path}")
        if record.get("sha256") == ZERO64:
            errors.append(f"required {label} retains zero hash sentinel: {path}")


def _load_required_json(rel_path, errors):
    fp = safe_repo_path(rel_path)
    if fp is None or not fp.exists():
        return None
    try:
        return load(fp)
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"invalid JSON freeze artifact {rel_path}: {exc}")
        return None


def _validate_resource_budget(data, errors):
    if not isinstance(data, dict):
        return
    if data.get("status") != "FROZEN":
        errors.append("resource-budget-v0.1.json status must be FROZEN before campaign freeze")
    budgets = data.get("budgets")
    if not isinstance(budgets, dict):
        errors.append("resource-budget-v0.1.json budgets must be an object")
        return
    positive = ("wall_clock_seconds", "model_output_token_ceiling", "retrieval_tool_call_ceiling", "output_size_ceiling")
    for key in positive:
        value = budgets.get(key)
        if not isinstance(value, (int, float)) or isinstance(value, bool) or value <= 0:
            errors.append(f"resource budget {key} must be a positive number")
    retry = budgets.get("retry_rounds")
    if not isinstance(retry, int) or isinstance(retry, bool) or retry < 0:
        errors.append("resource budget retry_rounds must be a nonnegative integer")
    for key in ("model_family", "model_version", "source_cutoff"):
        if not isinstance(budgets.get(key), str) or not budgets.get(key):
            errors.append(f"resource budget {key} must be a nonempty string")
    tools = budgets.get("retrieval_tools")
    if not isinstance(tools, list) or not tools or any(not isinstance(v, str) or not v for v in tools):
        errors.append("resource budget retrieval_tools must be a nonempty string array")


def _validate_condition_prompts(data, errors):
    if not isinstance(data, dict):
        return
    conditions = data.get("conditions")
    if not isinstance(conditions, dict) or set(conditions) != {"F", "B0", "B1", "B2"}:
        errors.append("condition-prompts.json must define exactly F, B0, B1, and B2")
        return
    for condition, bundle in conditions.items():
        if not isinstance(bundle, dict):
            errors.append(f"condition-prompts.json {condition} bundle must be an object")
            continue
        for surface in ("system", "developer", "user_template"):
            value = bundle.get(surface)
            if value is None:
                if surface == "user_template":
                    errors.append(f"condition-prompts.json {condition}.user_template cannot be null")
                continue
            if not isinstance(value, dict) or set(value) != {"base64", "sha256"}:
                errors.append(f"condition-prompts.json {condition}.{surface} must contain base64 and sha256")
                continue
            try:
                raw = base64.b64decode(value["base64"], validate=True)
            except Exception:
                errors.append(f"condition-prompts.json {condition}.{surface} has invalid base64")
                continue
            digest = hashlib.sha256(raw).hexdigest()
            if value.get("sha256") != digest:
                errors.append(f"condition-prompts.json {condition}.{surface} hash mismatch")
            if surface == "user_template" and raw.count(b"{{CASE_PROMPT}}") != 1:
                errors.append(f"condition-prompts.json {condition}.user_template must contain exactly one {{CASE_PROMPT}} marker")


def _validate_frozen_configs(errors):
    loaded = {}
    for path in sorted(FROZEN_CONFIG_JSON):
        data = _load_required_json(path, errors)
        if data is None:
            continue
        loaded[path] = data
        findings = find_unfrozen(data)
        if findings:
            errors.append(f"freeze artifact {path} contains unresolved sentinel(s): {findings[:5]}")
    budget_path = f"{BENCHMARK_DIR}/resource-budget-v0.1.json"
    if budget_path in loaded:
        _validate_resource_budget(loaded[budget_path], errors)
    prompts_path = f"{BENCHMARK_DIR}/condition-prompts.json"
    if prompts_path in loaded:
        _validate_condition_prompts(loaded[prompts_path], errors)


def validate(manifest_path: pathlib.Path):
    try:
        m = load(manifest_path)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: manifest cannot be loaded: {exc}", file=sys.stderr)
        return 1

    errors = []
    try:
        schema = load(SCHEMA)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: governed campaign schema cannot be loaded: {exc}", file=sys.stderr)
        return 1
    errors.extend(schema_errors(m, schema))

    status = m.get("status")
    artifacts = m.get("artifacts", [])
    sources = m.get("source_manifest", [])
    artifact_map = _artifact_map(artifacts, "artifacts", errors)
    source_map = _artifact_map(sources, "source_manifest", errors)
    _verify_records(artifacts, "artifacts", status, errors)
    _verify_records(sources, "source_manifest", status, errors)

    protocol = m.get("protocol", {}) if isinstance(m.get("protocol"), dict) else {}
    protocol_path = protocol.get("path")
    ppath = safe_repo_path(protocol_path)
    if protocol_path and ppath is None:
        errors.append("protocol path is unsafe")
    elif protocol_path and not ppath.exists():
        errors.append(f"protocol path missing: {protocol_path}")
    elif protocol_path and status in FROZEN_OR_LATER:
        if protocol.get("sha256") in {"", ZERO64}:
            errors.append("frozen-or-later manifest requires a real protocol hash")
        elif protocol.get("sha256") != sha256(ppath):
            errors.append("protocol hash mismatch")

    if status in FROZEN_OR_LATER:
        manifest_findings = find_unfrozen(m)
        if manifest_findings:
            errors.append(f"frozen-or-later manifest contains unset sentinel(s): {manifest_findings[:5]}")

        freeze_time = _parse_time(m.get("times", {}).get("freeze_time") if isinstance(m.get("times"), dict) else None)
        if freeze_time is None:
            errors.append("frozen-or-later manifest requires an offset-aware ISO-8601 freeze_time")
        unblinding_raw = m.get("times", {}).get("unblinding_time") if isinstance(m.get("times"), dict) else None
        if status == "frozen" and unblinding_raw is not None:
            errors.append("frozen manifest must have unblinding_time=null")
        if status in ANALYZABLE:
            unblinding_time = _parse_time(unblinding_raw)
            if unblinding_time is None:
                errors.append("unblinded/completed manifest requires an offset-aware ISO-8601 unblinding_time")
            elif freeze_time is not None and unblinding_time < freeze_time:
                errors.append("unblinding_time cannot precede freeze_time")

        if len(sources) == 0:
            errors.append("frozen-or-later manifest requires a non-empty source_manifest")
        evaluators = m.get("evaluators", []) if isinstance(m.get("evaluators"), list) else []
        ids = [e.get("id") for e in evaluators if isinstance(e, dict)]
        if len(evaluators) < 3 or len(set(ids)) < 3:
            errors.append("frozen-or-later manifest requires at least three distinct adjudicator/evaluator identities")

        _require_verified_paths(artifact_map, REQUIRED_FROZEN_ARTIFACTS, "artifact", errors)
        _require_verified_paths(source_map, REQUIRED_SOURCE_PATHS, "source binding", errors)
        _validate_frozen_configs(errors)

    if errors:
        for error in errors:
            print("ERROR:", error, file=sys.stderr)
        return 1
    print(f"VALID {m.get('campaign_id', '<unknown>')} status={status}")
    return 0


def analyze(manifest_path: pathlib.Path):
    try:
        m = load(manifest_path)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: manifest cannot be loaded: {exc}", file=sys.stderr)
        return 1
    if validate(manifest_path):
        return 1
    if m["status"] not in ANALYZABLE:
        print("BLOCKED: analysis requires an unblinded/completed frozen campaign.", file=sys.stderr)
        return 2
    metrics = manifest_path.parent / "metrics.csv"
    if not metrics.exists():
        print("BLOCKED: metrics.csv is absent.", file=sys.stderr)
        return 2
    print("Analysis execution is intentionally unavailable until the frozen metric implementation is added and reviewed.")
    return 2


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd", required=True)
    for name in ("validate", "analyze"):
        p = sub.add_parser(name)
        p.add_argument("--manifest", required=True, type=pathlib.Path)
    args = parser.parse_args()
    path = args.manifest if args.manifest.is_absolute() else ROOT / args.manifest
    return validate(path) if args.cmd == "validate" else analyze(path)


if __name__ == "__main__":
    raise SystemExit(main())
