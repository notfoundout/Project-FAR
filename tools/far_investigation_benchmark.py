#!/usr/bin/env python3
"""Fail-closed validator/analyzer entry point for FAR Investigation Benchmark v0.1."""

from __future__ import annotations

import argparse
import base64
import csv
import datetime as dt
import hashlib
import json
import math
import pathlib
import re
import sys
from collections import Counter

ROOT = pathlib.Path(__file__).resolve().parents[1]
ROOT_RESOLVED = ROOT.resolve()
SCHEMA = ROOT / "schemas/far-research-campaign-v1.schema.json"
BENCHMARK_DIR = "research/comparisons/far-investigation-benchmark-v0.1"
PREREG = "research/comparisons/far-investigation-benchmark-v0.1.md"
CAMPAIGN_ID = "FAR-INVESTIGATION-BENCHMARK-0.1"
ZERO64 = "0" * 64
ANALYZABLE = {"unblinded", "completed", "completed_imported_sealed"}
FROZEN_OR_LATER = {"frozen", *ANALYZABLE}
COMPLETED = {"completed", "completed_imported_sealed"}
CONDITIONS = ("F", "B0", "B1", "B2")
STRATA = (
    "public_policy_law",
    "health_biomedical",
    "economics_quant_social",
    "science_technology",
    "historical",
    "media_viral_public_factual",
)
EVALUATOR_LANES = Counter(
    {
        "primary_scorer": 2,
        "scoring_adjudicator": 1,
        "unitizer": 2,
        "unitization_adjudicator": 1,
    }
)
FINAL_STATUSES = {
    "SURVIVES_TESTED_SCOPE",
    "NOT_SUPPORTED_AT_TESTED_SCOPE",
    "FALSIFIED_AT_TESTED_SCOPE",
    "INDETERMINATE",
}
AMENDMENT = f"{BENCHMARK_DIR}/hardening-amendment-v0.1.md"
TREATMENT_MANIFEST = f"{BENCHMARK_DIR}/far-treatment-source-manifest.json"

TREATMENT_SOURCE_PATHS = {
    "frameworks/FAR/workflow.md",
    "methodology/contract-discovery-protocol.md",
    "methodology/methodology-audit-protocol.md",
    "schemas/far-intake-v1.schema.json",
    "frameworks/FARA/README.md",
    "frameworks/FARA/admissibility-structure.md",
    "frameworks/FARA/architecture.md",
    "frameworks/FARA/dependency-graph.md",
    "frameworks/FARA/design-principles.md",
    "frameworks/FARA/document-map.md",
    "frameworks/FARA/formal-kernel.md",
    "frameworks/FARA/ontology.md",
    "frameworks/FARA/primitives.md",
    "frameworks/FARA/reasoning-states.md",
    "frameworks/FARA/semantics.md",
    "frameworks/FARA/transition-signatures.md",
}

REQUIRED_FROZEN_ARTIFACTS = {
    PREREG,
    AMENDMENT,
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
    f"{BENCHMARK_DIR}/adjudication-schedule.json",
    f"{BENCHMARK_DIR}/reference-search-config.json",
    f"{BENCHMARK_DIR}/reference-evidence-manifest.json",
    f"{BENCHMARK_DIR}/environment-lock.json",
    f"{BENCHMARK_DIR}/mutation-config.json",
    TREATMENT_MANIFEST,
}

REQUIRED_SOURCE_PATHS = {
    "tools/far_investigation_benchmark.py",
    "schemas/far-research-campaign-v1.schema.json",
    *TREATMENT_SOURCE_PATHS,
}

PREUNBLIND_OUTPUTS = {
    f"{BENCHMARK_DIR}/canonical-unitization.jsonl",
    f"{BENCHMARK_DIR}/ratings.raw.jsonl",
    f"{BENCHMARK_DIR}/ratings.adjudicated.jsonl",
    f"{BENCHMARK_DIR}/blinding-guesses.jsonl",
    f"{BENCHMARK_DIR}/score-lock.json",
    f"{BENCHMARK_DIR}/metrics.csv",
}
COMPLETION_OUTPUTS = {
    f"{BENCHMARK_DIR}/run-manifest.json",
    f"{BENCHMARK_DIR}/analysis.json",
    f"{BENCHMARK_DIR}/report.md",
    f"{BENCHMARK_DIR}/checksums.sha256",
}
FROZEN_CONFIG_JSON = {
    f"{BENCHMARK_DIR}/resource-budget-v0.1.json",
    f"{BENCHMARK_DIR}/analysis-parameters-v0.1.json",
    f"{BENCHMARK_DIR}/case-selection-config.json",
    f"{BENCHMARK_DIR}/case-selection-declarations.json",
    f"{BENCHMARK_DIR}/condition-prompts.json",
    f"{BENCHMARK_DIR}/execution-schedule.json",
    f"{BENCHMARK_DIR}/adjudication-schedule.json",
    f"{BENCHMARK_DIR}/reference-search-config.json",
    f"{BENCHMARK_DIR}/reference-evidence-manifest.json",
    f"{BENCHMARK_DIR}/environment-lock.json",
    f"{BENCHMARK_DIR}/mutation-config.json",
    TREATMENT_MANIFEST,
}
UNFROZEN_MARKERS = ("TO_BE_", "PLACEHOLDER")
UNFROZEN_EXACT = {"UNASSIGNED", "PREPARED_NOT_FROZEN"}
HEX64 = re.compile(r"^[0-9a-f]{64}$")


class ValidationError(ValueError):
    pass


def _reject_constant(value: str):
    raise ValidationError(f"non-finite JSON numeric literal forbidden: {value}")


def loads_strict(text: str):
    return json.loads(text, parse_constant=_reject_constant)


def load(path: pathlib.Path):
    return loads_strict(path.read_text(encoding="utf-8"))


def sha256(path: pathlib.Path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_text(text: str):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


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
        return (
            isinstance(value, (int, float))
            and not isinstance(value, bool)
            and (not isinstance(value, float) or math.isfinite(value))
        )
    return False


def schema_errors(instance, schema, root_schema=None, path="$", *, quiet=False):
    """Validate only the JSON-Schema keywords used by the governed campaign schema."""
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
            return [f"schema {path}: expected exactly one oneOf branch, got {matches}"]
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
        if isinstance(schema.get("items"), dict):
            for i, value in enumerate(instance):
                errors.extend(schema_errors(value, schema["items"], root_schema, f"{path}[{i}]", quiet=quiet))
    if isinstance(instance, dict):
        for key in schema.get("required", []):
            if key not in instance:
                errors.append(f"schema {path}: missing required property {key!r}")
        properties = schema.get("properties", {})
        additional = schema.get("additionalProperties", True)
        for key, value in instance.items():
            child = f"{path}.{key}"
            if key in properties:
                errors.extend(schema_errors(value, properties[key], root_schema, child, quiet=quiet))
            elif additional is False:
                errors.append(f"schema {path}: additional property {key!r} is not allowed")
            elif isinstance(additional, dict):
                errors.extend(schema_errors(value, additional, root_schema, child, quiet=quiet))
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
    return parsed if parsed.tzinfo is not None else None


def _finite_positive(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value) and value > 0


def _artifact_map(records, label, errors):
    result = {}
    for i, record in enumerate(records if isinstance(records, list) else []):
        if not isinstance(record, dict):
            continue
        raw = record.get("path")
        if raw in result:
            errors.append(f"{label}: duplicate path {raw}")
        result[raw] = record
        if safe_repo_path(raw) is None:
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
        if status in FROZEN_OR_LATER and not verify:
            errors.append(f"{label}[{i}]: frozen-or-later record must set verify_current_path=true: {raw}")
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
        errors.append(f"required JSON freeze artifact missing: {rel_path}")
        return None
    try:
        return load(fp)
    except (OSError, json.JSONDecodeError, ValidationError) as exc:
        errors.append(f"invalid JSON freeze artifact {rel_path}: {exc}")
        return None


def _load_required_jsonl(rel_path, errors):
    fp = safe_repo_path(rel_path)
    if fp is None or not fp.exists():
        errors.append(f"required JSONL freeze artifact missing: {rel_path}")
        return None
    rows = []
    try:
        for lineno, line in enumerate(fp.read_text(encoding="utf-8").splitlines(), 1):
            if not line.strip():
                continue
            row = loads_strict(line)
            if not isinstance(row, dict):
                errors.append(f"{rel_path}:{lineno}: JSONL row must be an object")
            else:
                rows.append(row)
    except (OSError, json.JSONDecodeError, ValidationError) as exc:
        errors.append(f"invalid JSONL freeze artifact {rel_path}: {exc}")
        return None
    if not rows:
        errors.append(f"{rel_path}: must contain at least one row")
    return rows


def _validate_resource_budget(data, errors):
    if not isinstance(data, dict):
        errors.append("resource-budget-v0.1.json must be an object")
        return
    if data.get("status") != "FROZEN":
        errors.append("resource-budget-v0.1.json status must be FROZEN before campaign freeze")
    budgets = data.get("budgets")
    if not isinstance(budgets, dict):
        errors.append("resource-budget-v0.1.json budgets must be an object")
        return
    for key in ("wall_clock_seconds", "model_output_token_ceiling", "retrieval_tool_call_ceiling", "output_size_ceiling"):
        if not _finite_positive(budgets.get(key)):
            errors.append(f"resource budget {key} must be a finite positive number")
    retry = budgets.get("retry_rounds")
    if not isinstance(retry, int) or isinstance(retry, bool) or retry < 0:
        errors.append("resource budget retry_rounds must be a nonnegative integer")
    for key in ("model_family", "model_version", "source_cutoff"):
        if not isinstance(budgets.get(key), str) or not budgets.get(key).strip():
            errors.append(f"resource budget {key} must be a nonempty string")
    tools = budgets.get("retrieval_tools")
    if not isinstance(tools, list) or not tools or any(not isinstance(v, str) or not v.strip() for v in tools):
        errors.append("resource budget retrieval_tools must be a nonempty string array")
    exclusion = str(data.get("confirmatory_exclusion_rule", "")).lower()
    if "ceiling" not in exclusion or "not" not in exclusion or "exogenous" not in exclusion:
        errors.append("resource budget exclusion rule must state that ceiling hits are not exclusions and only exogenous failures are nonratable")


def _validate_analysis_parameters(data, errors):
    if not isinstance(data, dict):
        errors.append("analysis-parameters-v0.1.json must be an object")
        return
    expected = {
        "case_count": 60,
        "domains": 6,
        "cases_per_domain": 10,
        "confirmatory_baselines": ["B0", "B1", "B2"],
    }
    for key, value in expected.items():
        if data.get(key) != value:
            errors.append(f"analysis parameters {key} must equal {value!r}")
    m2 = data.get("m2")
    if not isinstance(m2, dict):
        errors.append("analysis parameters m2 must be an object")
    else:
        if m2.get("bootstrap_resamples") != 10000 or m2.get("seed") != 20260922:
            errors.append("M2 bootstrap must freeze 10000 resamples and seed 20260922")
        fam = m2.get("directional_falsification_familywise")
        if not isinstance(fam, dict):
            errors.append("M2 must define directional_falsification_familywise")
        else:
            q = fam.get("one_sided_upper_confidence")
            if not isinstance(q, (int, float)) or isinstance(q, bool) or not math.isclose(q, 1 - 0.05 / 3, rel_tol=0, abs_tol=1e-15):
                errors.append("M2 familywise falsification confidence must equal 1 - 0.05/3")
            if fam.get("zero_based_index_n10000") != 9833:
                errors.append("M2 familywise falsification upper index must be 9833 for N=10000")
            if fam.get("strictly_less_than") != -0.05:
                errors.append("M2 familywise falsification threshold must equal -0.05")


def _validate_condition_prompts(data, errors):
    if not isinstance(data, dict):
        errors.append("condition-prompts.json must be an object")
        return
    if data.get("status") != "FROZEN":
        errors.append("condition-prompts.json status must be FROZEN")
    conditions = data.get("conditions")
    if not isinstance(conditions, dict) or set(conditions) != set(CONDITIONS):
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
            if value.get("sha256") != hashlib.sha256(raw).hexdigest():
                errors.append(f"condition-prompts.json {condition}.{surface} hash mismatch")
            if surface == "user_template" and raw.count(b"{{CASE_PROMPT}}") != 1:
                errors.append(f"condition-prompts.json {condition}.user_template must contain exactly one {{CASE_PROMPT}} marker")


def _validate_case_selection_declarations(data, errors):
    if not isinstance(data, dict) or data.get("status") != "FROZEN":
        errors.append("case-selection-declarations.json must be a FROZEN object")
        return
    selectors = data.get("selectors")
    adjudicator = data.get("clustering_adjudicator")
    if not isinstance(selectors, list) or len(selectors) != 2 or not isinstance(adjudicator, dict):
        errors.append("case selection requires exactly two selectors and one clustering_adjudicator")
        return
    declarations = [*selectors, adjudicator]
    ids, identities = [], []
    for item in declarations:
        if not isinstance(item, dict):
            errors.append("case-selection declaration entries must be objects")
            continue
        for field in ("id", "identity", "provider", "independence", "conflicts", "role"):
            if not isinstance(item.get(field), str) or not item[field].strip() or find_unfrozen(item[field]):
                errors.append(f"case-selection declaration requires substantive {field}")
        ids.append(item.get("id"))
        identities.append(item.get("identity"))
    if len(set(ids)) != 3 or len(set(identities)) != 3:
        errors.append("case selectors and clustering adjudicator must have distinct IDs and identities")
    if [s.get("role") for s in selectors].count("selector") != 2 or adjudicator.get("role") != "clustering_adjudicator":
        errors.append("case-selection declaration roles must be two selector and one clustering_adjudicator")


def _validate_case_bundle(candidates, cases, reserves, errors):
    if not candidates:
        errors.append("candidate-frame.jsonl must not be empty")
    if not cases:
        errors.append("cases.jsonl must not be empty")
    if not reserves:
        errors.append("replacement-frame.jsonl must not be empty")
    if not candidates or not cases or not reserves:
        return
    by_id = {}
    eligible_reps = {s: [] for s in STRATA}
    for row in candidates:
        cid = row.get("candidate_id")
        if not isinstance(cid, str) or not cid or cid in by_id:
            errors.append("candidate-frame.jsonl candidate_id values must be unique nonempty strings")
            continue
        by_id[cid] = row
        stratum = row.get("stratum_id")
        if stratum not in STRATA:
            errors.append(f"candidate {cid}: invalid stratum_id")
            continue
        rank = row.get("retrieval_rank")
        if not isinstance(rank, int) or isinstance(rank, bool) or rank < 1:
            errors.append(f"candidate {cid}: retrieval_rank must be a positive integer")
        for key in ("claim_text", "normalized_claim_text", "normalized_source_identity"):
            if not isinstance(row.get(key), str) or not row[key].strip():
                errors.append(f"candidate {cid}: {key} must be nonempty")
        cluster = row.get("claim_cluster_id")
        if not isinstance(cluster, str) or not HEX64.fullmatch(cluster):
            errors.append(f"candidate {cid}: claim_cluster_id must be lowercase SHA-256")
        if row.get("cluster_representative") is True and row.get("eligible") is True and row.get("contaminated") is False and row.get("contamination_checked") is True:
            eligible_reps[stratum].append(row)

    for stratum, rows in eligible_reps.items():
        seen = set()
        for row in rows:
            cluster = row.get("claim_cluster_id")
            if cluster in seen:
                errors.append(f"candidate frame: duplicate eligible representative claim cluster in {stratum}: {cluster}")
            seen.add(cluster)
        if len(rows) < 20:
            errors.append(f"candidate frame: {stratum} requires at least 20 eligible uncontaminated cluster representatives")

    if len(cases) != 60:
        errors.append(f"cases.jsonl must contain exactly 60 cases, got {len(cases)}")
    case_ids, selected_candidates, selected_clusters = set(), set(), set()
    stratum_counts = Counter()
    for row in cases:
        case_id = row.get("case_id")
        candidate_id = row.get("candidate_id")
        cluster = row.get("claim_cluster_id")
        stratum = row.get("stratum_id")
        if not isinstance(case_id, str) or not case_id or case_id in case_ids:
            errors.append("cases.jsonl case_id values must be unique nonempty strings")
        case_ids.add(case_id)
        if candidate_id in selected_candidates:
            errors.append(f"cases.jsonl duplicate candidate_id: {candidate_id}")
        selected_candidates.add(candidate_id)
        if cluster in selected_clusters:
            errors.append(f"cases.jsonl duplicate claim_cluster_id: {cluster}")
        selected_clusters.add(cluster)
        stratum_counts[stratum] += 1
        candidate = by_id.get(candidate_id)
        if candidate is None:
            errors.append(f"case {case_id}: candidate_id not present in candidate frame")
        else:
            for key in ("stratum_id", "claim_cluster_id"):
                if row.get(key) != candidate.get(key):
                    errors.append(f"case {case_id}: {key} does not match candidate frame")
            if not (
                candidate.get("eligible") is True
                and candidate.get("cluster_representative") is True
                and candidate.get("contamination_checked") is True
                and candidate.get("contaminated") is False
            ):
                errors.append(f"case {case_id}: selected candidate is not eligible uncontaminated cluster representative")
        prompt = row.get("prompt")
        if not isinstance(prompt, str) or not prompt.strip():
            errors.append(f"case {case_id}: prompt must be nonempty")
        elif row.get("prompt_sha256") != sha256_text(prompt):
            errors.append(f"case {case_id}: prompt_sha256 mismatch")
    for stratum in STRATA:
        if stratum_counts[stratum] != 10:
            errors.append(f"cases.jsonl requires exactly 10 cases in {stratum}, got {stratum_counts[stratum]}")

    reserve_counts = Counter()
    reserve_candidates, reserve_clusters = set(), set()
    for row in reserves:
        cid = row.get("candidate_id")
        cluster = row.get("claim_cluster_id")
        stratum = row.get("stratum_id")
        reserve_counts[stratum] += 1
        if cid in selected_candidates or cid in reserve_candidates:
            errors.append(f"replacement-frame.jsonl candidate overlap/duplicate: {cid}")
        reserve_candidates.add(cid)
        if cluster in selected_clusters or cluster in reserve_clusters:
            errors.append(f"replacement-frame.jsonl claim-cluster overlap/duplicate: {cluster}")
        reserve_clusters.add(cluster)
        candidate = by_id.get(cid)
        if candidate is None or candidate.get("claim_cluster_id") != cluster or candidate.get("stratum_id") != stratum:
            errors.append(f"reserve candidate {cid}: does not match candidate frame")
        elif not (
            candidate.get("eligible") is True
            and candidate.get("cluster_representative") is True
            and candidate.get("contamination_checked") is True
            and candidate.get("contaminated") is False
        ):
            errors.append(f"reserve candidate {cid}: not eligible uncontaminated cluster representative")
    for stratum in STRATA:
        if reserve_counts[stratum] < 10:
            errors.append(f"replacement-frame.jsonl requires at least 10 reserves in {stratum}")


def _validate_schedule(data, case_ids, errors):
    if not isinstance(data, dict) or data.get("status") != "FROZEN":
        errors.append("execution-schedule.json must be a FROZEN object")
        return
    runs = data.get("runs")
    if not isinstance(runs, list) or len(runs) != 240:
        errors.append("execution-schedule.json must contain exactly 240 runs")
        return
    seen_pairs, run_ids, indices = set(), set(), set()
    sortable = []
    for run in runs:
        if not isinstance(run, dict):
            errors.append("execution schedule run must be an object")
            continue
        case_id, condition, run_id = run.get("case_id"), run.get("condition"), run.get("run_id")
        idx = run.get("execution_index")
        pair = (case_id, condition)
        if case_id not in case_ids or condition not in CONDITIONS:
            errors.append(f"execution schedule contains invalid case/condition: {pair}")
        if pair in seen_pairs:
            errors.append(f"execution schedule duplicate case-condition: {pair}")
        seen_pairs.add(pair)
        if not isinstance(run_id, str) or not run_id or run_id in run_ids:
            errors.append("execution schedule run_id values must be unique nonempty strings")
        run_ids.add(run_id)
        if not isinstance(idx, int) or isinstance(idx, bool) or idx < 1 or idx > 240 or idx in indices:
            errors.append("execution schedule execution_index values must be unique integers 1..240")
        indices.add(idx)
        expected_nonce = sha256_text(f"{CAMPAIGN_ID}|cache|{run_id}") if isinstance(run_id, str) else None
        if run.get("cache_nonce") != expected_nonce:
            errors.append(f"execution schedule cache nonce mismatch for run {run_id}")
        sort_key = sha256_text(f"20260922|schedule|{case_id}|{condition}")
        if run.get("schedule_key") != sort_key:
            errors.append(f"execution schedule schedule_key mismatch for run {run_id}")
        sortable.append((sort_key, case_id, condition, idx))
    expected_pairs = {(case_id, c) for case_id in case_ids for c in CONDITIONS}
    if seen_pairs != expected_pairs:
        errors.append("execution schedule is not the complete 60×4 Cartesian product")
    if indices != set(range(1, 241)):
        errors.append("execution schedule indices must equal exactly 1..240")
    for expected_idx, item in enumerate(sorted(sortable) if len(sortable) == 240 else [], 1):
        if item[3] != expected_idx:
            errors.append("execution schedule order does not match frozen deterministic schedule_key sort")
            break


def _validate_adjudication_schedule(data, case_ids, execution_schedule, evaluators, errors):
    """Reproduce the frozen, evaluator-specific packet presentation schedules."""
    if not isinstance(data, dict) or set(data) != {"status", "schedules"} or data.get("status") != "FROZEN":
        errors.append("adjudication-schedule.json must be a FROZEN object with exactly status and schedules")
        return
    schedules = data.get("schedules")
    if not isinstance(schedules, list) or len(schedules) != 4:
        errors.append("adjudication-schedule.json must contain exactly four evaluator schedules")
        return
    if not isinstance(execution_schedule, dict) or not isinstance(execution_schedule.get("runs"), list):
        errors.append("adjudication schedule requires a valid execution-schedule.json")
        return
    run_by_pair = {
        (run.get("case_id"), run.get("condition")): run.get("run_id")
        for run in execution_schedule["runs"]
        if isinstance(run, dict)
    }
    expected_evaluators = {
        evaluator.get("id"): evaluator.get("lane")
        for evaluator in evaluators or []
        if isinstance(evaluator, dict) and evaluator.get("lane") in {"unitizer", "primary_scorer"}
    }
    seen_evaluators = set()
    assignment_fields = {
        "presentation_index", "round", "round_position", "case_id", "condition", "run_id",
        "condition_label_visible", "fresh_context", "other_case_versions_visible",
        "other_evaluator_outputs_visible",
    }
    for schedule in schedules:
        if not isinstance(schedule, dict) or set(schedule) != {"evaluator_id", "lane", "assignments"}:
            errors.append("each adjudication evaluator schedule must contain exactly evaluator_id, lane, and assignments")
            continue
        evaluator_id, lane = schedule.get("evaluator_id"), schedule.get("lane")
        if evaluator_id in seen_evaluators:
            errors.append(f"duplicate adjudication evaluator schedule: {evaluator_id}")
        seen_evaluators.add(evaluator_id)
        if expected_evaluators.get(evaluator_id) != lane:
            errors.append(f"adjudication schedule evaluator/lane mismatch: {evaluator_id}")
        assignments = schedule.get("assignments")
        if not isinstance(assignments, list) or len(assignments) != 240:
            errors.append(f"adjudication schedule for {evaluator_id} must contain exactly 240 assignments")
            continue
        base_order = sorted(case_ids, key=lambda cid: sha256_text(f"20260922|adjudication-case-order|{evaluator_id}|{cid}"))
        expected = []
        for round_index in range(4):
            for round_position, case_id in enumerate(base_order, 1):
                condition = CONDITIONS[(round_index + (round_position - 1) % 4) % 4]
                expected.append((round_index + 1, round_position, case_id, condition, run_by_pair.get((case_id, condition))))
        for presentation_index, (assignment, values) in enumerate(zip(assignments, expected), 1):
            if not isinstance(assignment, dict) or set(assignment) != assignment_fields:
                errors.append(f"adjudication assignment {evaluator_id}/{presentation_index} has invalid fields")
                continue
            round_number, round_position, case_id, condition, run_id = values
            actual = (
                assignment.get("presentation_index"), assignment.get("round"), assignment.get("round_position"),
                assignment.get("case_id"), assignment.get("condition"), assignment.get("run_id"),
            )
            required = (presentation_index, round_number, round_position, case_id, condition, run_id)
            if actual != required:
                errors.append(f"adjudication assignment {evaluator_id}/{presentation_index} does not match frozen order/run binding")
            if assignment.get("condition_label_visible") is not False:
                errors.append(f"adjudication assignment {evaluator_id}/{presentation_index} must be condition-blinded")
            if assignment.get("fresh_context") is not True:
                errors.append(f"adjudication assignment {evaluator_id}/{presentation_index} must use a fresh context")
            if assignment.get("other_case_versions_visible") is not False:
                errors.append(f"adjudication assignment {evaluator_id}/{presentation_index} exposes another case version")
            if assignment.get("other_evaluator_outputs_visible") is not False:
                errors.append(f"adjudication assignment {evaluator_id}/{presentation_index} exposes another evaluator output")
    if seen_evaluators != set(expected_evaluators) or len(expected_evaluators) != 4:
        errors.append("adjudication schedules must exactly cover the two unitizers and two primary scorers")


def _validate_reference_manifest(data, case_ids, errors):
    if not isinstance(data, dict) or data.get("status") != "FROZEN":
        errors.append("reference-evidence-manifest.json must be a FROZEN object")
        return
    rows = data.get("cases")
    if not isinstance(rows, list) or len(rows) != 60:
        errors.append("reference-evidence-manifest.json must contain exactly 60 case records")
        return
    seen = set()
    for row in rows:
        if not isinstance(row, dict):
            errors.append("reference evidence case record must be an object")
            continue
        cid = row.get("case_id")
        if cid in seen:
            errors.append(f"reference evidence duplicate case_id: {cid}")
        seen.add(cid)
        denom = row.get("m2_denominator")
        if not isinstance(denom, int) or isinstance(denom, bool) or denom < 1:
            errors.append(f"reference evidence case {cid}: m2_denominator must be a positive integer")
        items = row.get("items")
        if not isinstance(items, list) or len(items) != denom:
            errors.append(f"reference evidence case {cid}: items length must equal m2_denominator")
    if seen != set(case_ids):
        errors.append("reference-evidence-manifest case IDs must exactly match cases.jsonl")


def _validate_environment_lock(data, errors):
    if not isinstance(data, dict) or data.get("status") != "FROZEN":
        errors.append("environment-lock.json must be a FROZEN object")
        return
    for key in ("provider", "model_identifier", "tool_configuration"):
        if not data.get(key):
            errors.append(f"environment-lock.json requires {key}")
    cache = data.get("cache_isolation")
    if not isinstance(cache, dict):
        errors.append("environment-lock.json requires cache_isolation")
        return
    mode = cache.get("mode")
    if mode not in {"provider_isolated_context", "non_model_visible_nonce"}:
        errors.append("cache isolation mode must be provider_isolated_context or non_model_visible_nonce")
    if cache.get("model_visible") is not False or cache.get("counts_toward_model_token_budget") is not False:
        errors.append("cache isolation must be non-model-visible and excluded from model-visible token budget")
    if not isinstance(cache.get("channel"), str) or not cache["channel"].strip():
        errors.append("cache isolation requires a nonempty channel")
    if not isinstance(cache.get("documentation"), str) or not cache["documentation"].strip():
        errors.append("cache isolation requires provider/tool documentation")
    if mode == "non_model_visible_nonce":
        if cache.get("nonce_algorithm") != 'SHA256(UTF8("FAR-INVESTIGATION-BENCHMARK-0.1|cache|" + run_id))':
            errors.append("cache nonce algorithm does not match frozen rule")


def _validate_mutation_config(data, errors):
    if not isinstance(data, dict) or data.get("status") != "FROZEN":
        errors.append("mutation-config.json must be a FROZEN object")
        return
    mutations = data.get("mutations")
    if not isinstance(mutations, list) or len(mutations) != 6:
        errors.append("mutation-config.json must freeze exactly six mutation families")
        return
    ids = [m.get("id") if isinstance(m, dict) else None for m in mutations]
    if any(not isinstance(v, str) or not v for v in ids) or len(set(ids)) != 6:
        errors.append("mutation-config.json mutation IDs must be six unique nonempty strings")


def _validate_treatment_manifest(data, errors):
    if not isinstance(data, dict) or data.get("status") != "FROZEN":
        errors.append("far-treatment-source-manifest.json must be a FROZEN object")
        return
    records = data.get("sources")
    if not isinstance(records, list):
        errors.append("far-treatment-source-manifest.json sources must be an array")
        return
    seen = {}
    for rec in records:
        if not isinstance(rec, dict):
            errors.append("treatment source record must be an object")
            continue
        path = rec.get("path")
        if path in seen:
            errors.append(f"duplicate treatment source path: {path}")
        seen[path] = rec
        fp = safe_repo_path(path)
        if fp is None or not fp.exists():
            errors.append(f"treatment source missing/unsafe: {path}")
            continue
        if rec.get("verify_current_path") is not True:
            errors.append(f"treatment source must verify current path: {path}")
        digest = rec.get("sha256")
        if not isinstance(digest, str) or not HEX64.fullmatch(digest) or digest == ZERO64 or digest != sha256(fp):
            errors.append(f"treatment source hash mismatch/invalid: {path}")
    missing = TREATMENT_SOURCE_PATHS - set(seen)
    if missing:
        errors.append(f"treatment source manifest missing mandatory transitive sources: {sorted(missing)}")


def _validate_evaluators(evaluators, errors):
    if not isinstance(evaluators, list):
        return
    lanes = Counter()
    ids, identities = [], []
    for e in evaluators:
        if not isinstance(e, dict):
            continue
        lanes[e.get("lane")] += 1
        ids.append(e.get("id"))
        identities.append(e.get("identity"))
        for key in ("id", "identity", "provider", "prior_exposure", "conflicts", "lane"):
            value = e.get(key)
            if not isinstance(value, str) or not value.strip() or find_unfrozen(value):
                errors.append(f"frozen evaluator requires substantive {key}")
        provider = str(e.get("provider", "")).lower()
        if "project-far" in provider or "project far" in provider:
            errors.append(f"confirmatory evaluator {e.get('id')} cannot be project-authored")
    if lanes != EVALUATOR_LANES:
        errors.append(f"frozen evaluator lanes must equal {dict(EVALUATOR_LANES)}; got {dict(lanes)}")
    if len(ids) != 6 or len(set(ids)) != 6 or len(set(identities)) != 6:
        errors.append("frozen benchmark requires six distinct evaluator IDs and identities")


def _validate_case_selection_config(data, errors):
    if not isinstance(data, dict) or data.get("status") != "FROZEN":
        errors.append("case-selection-config.json must be a FROZEN object")
        return
    if data.get("seed") != 20260922 or data.get("result_limit_per_query") != 50:
        errors.append("case-selection-config must freeze seed=20260922 and result_limit_per_query=50")
    if data.get("minimum_reserves_per_stratum") != 10:
        errors.append("case-selection-config minimum_reserves_per_stratum must equal 10")
    strata = data.get("strata")
    if not isinstance(strata, list) or set(strata) != set(STRATA) or len(strata) != 6:
        errors.append("case-selection-config strata must equal the six canonical strata")
    for key in ("normalization_rule", "claim_clustering_rule", "selection_rule", "contamination_rule"):
        if not isinstance(data.get(key), str) or not data[key].strip():
            errors.append(f"case-selection-config requires {key}")


def _validate_frozen_semantics(evaluators, errors):
    paths = {p: _load_required_json(p, errors) for p in sorted(FROZEN_CONFIG_JSON)}
    for path, data in paths.items():
        if data is not None:
            findings = find_unfrozen(data)
            if findings:
                errors.append(f"freeze artifact {path} contains unresolved sentinel(s): {findings[:5]}")

    candidates = _load_required_jsonl(f"{BENCHMARK_DIR}/candidate-frame.jsonl", errors)
    cases = _load_required_jsonl(f"{BENCHMARK_DIR}/cases.jsonl", errors)
    reserves = _load_required_jsonl(f"{BENCHMARK_DIR}/replacement-frame.jsonl", errors)

    _validate_resource_budget(paths.get(f"{BENCHMARK_DIR}/resource-budget-v0.1.json"), errors)
    _validate_analysis_parameters(paths.get(f"{BENCHMARK_DIR}/analysis-parameters-v0.1.json"), errors)
    _validate_condition_prompts(paths.get(f"{BENCHMARK_DIR}/condition-prompts.json"), errors)
    _validate_case_selection_config(paths.get(f"{BENCHMARK_DIR}/case-selection-config.json"), errors)
    _validate_case_selection_declarations(paths.get(f"{BENCHMARK_DIR}/case-selection-declarations.json"), errors)
    _validate_environment_lock(paths.get(f"{BENCHMARK_DIR}/environment-lock.json"), errors)
    _validate_mutation_config(paths.get(f"{BENCHMARK_DIR}/mutation-config.json"), errors)
    _validate_treatment_manifest(paths.get(TREATMENT_MANIFEST), errors)

    if candidates is not None and cases is not None and reserves is not None:
        _validate_case_bundle(candidates, cases, reserves, errors)
    case_ids = {r.get("case_id") for r in cases or [] if isinstance(r.get("case_id"), str)}
    if len(case_ids) == 60:
        execution_schedule = paths.get(f"{BENCHMARK_DIR}/execution-schedule.json")
        _validate_schedule(execution_schedule, case_ids, errors)
        _validate_adjudication_schedule(
            paths.get(f"{BENCHMARK_DIR}/adjudication-schedule.json"),
            case_ids,
            execution_schedule,
            evaluators,
            errors,
        )
        _validate_reference_manifest(paths.get(f"{BENCHMARK_DIR}/reference-evidence-manifest.json"), case_ids, errors)

    ref_cfg = paths.get(f"{BENCHMARK_DIR}/reference-search-config.json")
    if not isinstance(ref_cfg, dict) or ref_cfg.get("status") != "FROZEN":
        errors.append("reference-search-config.json must be a FROZEN object")


def _validate_score_lock(unblinding_time, artifact_map, errors):
    _require_verified_paths(artifact_map, PREUNBLIND_OUTPUTS, "pre-unblinding artifact", errors)
    lock_path = safe_repo_path(f"{BENCHMARK_DIR}/score-lock.json")
    if lock_path is None or not lock_path.exists():
        return
    try:
        lock = load(lock_path)
    except (OSError, json.JSONDecodeError, ValidationError) as exc:
        errors.append(f"score-lock.json invalid: {exc}")
        return
    if not isinstance(lock, dict) or lock.get("status") != "LOCKED":
        errors.append("score-lock.json status must be LOCKED")
        return
    locked_at = _parse_time(lock.get("locked_at"))
    if locked_at is None:
        errors.append("score-lock.json locked_at must be offset-aware ISO-8601")
    elif unblinding_time is not None and locked_at > unblinding_time:
        errors.append("score-lock.json locked_at cannot follow unblinding_time")
    bindings = lock.get("bindings")
    expected = PREUNBLIND_OUTPUTS - {f"{BENCHMARK_DIR}/score-lock.json"}
    if not isinstance(bindings, dict) or set(bindings) != expected:
        errors.append("score-lock.json bindings must exactly cover canonical unitization, ratings, blinding guesses, and metrics")
    else:
        for path, digest in bindings.items():
            fp = safe_repo_path(path)
            if fp is None or not fp.exists() or digest != sha256(fp):
                errors.append(f"score-lock binding hash mismatch: {path}")


def _validate_blinding_guesses(evaluators, final_status, errors):
    guesses = _load_required_jsonl(f"{BENCHMARK_DIR}/blinding-guesses.jsonl", errors)
    schedule = _load_required_json(f"{BENCHMARK_DIR}/execution-schedule.json", errors)
    if not guesses or not isinstance(schedule, dict):
        return
    cond_by_run = {r.get("run_id"): r.get("condition") for r in schedule.get("runs", []) if isinstance(r, dict)}
    scorers = [e.get("id") for e in evaluators if isinstance(e, dict) and e.get("lane") == "primary_scorer"]
    expected = {(sid, rid) for sid in scorers for rid in cond_by_run}
    seen = set()
    stats = {sid: {"total": 0, "correct": 0, "f_total": 0, "f_correct": 0} for sid in scorers}
    for row in guesses:
        key = (row.get("evaluator_id"), row.get("run_id"))
        if key in seen:
            errors.append(f"duplicate blinding guess: {key}")
        seen.add(key)
        if key not in expected:
            errors.append(f"unexpected blinding guess: {key}")
            continue
        guess = row.get("guess")
        if guess not in {*CONDITIONS, "UNKNOWN"}:
            errors.append(f"invalid blinding guess {guess!r}")
            continue
        actual = cond_by_run[key[1]]
        s = stats[key[0]]
        s["total"] += 1
        s["correct"] += int(guess == actual)
        if actual == "F":
            s["f_total"] += 1
            s["f_correct"] += int(guess == "F")
    if seen != expected:
        errors.append("blinding-guesses.jsonl must contain exactly two primary-scorer guesses for every run")
    failed = False
    for s in stats.values():
        if s["f_total"] == 60 and s["f_correct"] >= 30:
            failed = True
        if s["total"] == 240 and s["correct"] / 240 >= 0.40:
            failed = True
    if failed and final_status not in {None, "NOT_EXECUTED", "INDETERMINATE"}:
        errors.append("blinding diagnostic failed; final disposition must be INDETERMINATE")


def _validate_completed(manifest, artifact_map, errors):
    _require_verified_paths(artifact_map, COMPLETION_OUTPUTS, "completion artifact", errors)
    final = manifest.get("final_adjudication")
    if not isinstance(final, dict):
        errors.append("completed campaign requires final_adjudication object")
        return
    if final.get("status") not in FINAL_STATUSES:
        errors.append(f"completed final_adjudication.status must be one of {sorted(FINAL_STATUSES)}")
    if not final.get("justification") or not final.get("evidence"):
        errors.append("completed final_adjudication requires nonempty justification and evidence")
    run_path = safe_repo_path(f"{BENCHMARK_DIR}/run-manifest.json")
    if run_path and run_path.exists():
        try:
            run_manifest = load(run_path)
            runs = run_manifest.get("runs") if isinstance(run_manifest, dict) else None
            if not isinstance(runs, list) or len(runs) != 240:
                errors.append("run-manifest.json must contain exactly 240 run records")
        except (OSError, json.JSONDecodeError, ValidationError) as exc:
            errors.append(f"run-manifest.json invalid: {exc}")


def validate(manifest_path: pathlib.Path):
    try:
        m = load(manifest_path)
    except (OSError, json.JSONDecodeError, ValidationError) as exc:
        print(f"ERROR: manifest cannot be loaded: {exc}", file=sys.stderr)
        return 1

    errors = []
    try:
        schema = load(SCHEMA)
    except (OSError, json.JSONDecodeError, ValidationError) as exc:
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
        findings = find_unfrozen(m)
        if findings:
            errors.append(f"frozen-or-later manifest contains unset sentinel(s): {findings[:5]}")
        freeze_time = _parse_time(m.get("times", {}).get("freeze_time") if isinstance(m.get("times"), dict) else None)
        if freeze_time is None:
            errors.append("frozen-or-later manifest requires an offset-aware ISO-8601 freeze_time")
        raw_unblind = m.get("times", {}).get("unblinding_time") if isinstance(m.get("times"), dict) else None
        if status == "frozen" and raw_unblind is not None:
            errors.append("frozen manifest must have unblinding_time=null")
        unblinding_time = None
        if status in ANALYZABLE:
            unblinding_time = _parse_time(raw_unblind)
            if unblinding_time is None:
                errors.append("unblinded/completed manifest requires an offset-aware ISO-8601 unblinding_time")
            elif freeze_time is not None and unblinding_time < freeze_time:
                errors.append("unblinding_time cannot precede freeze_time")

        _require_verified_paths(artifact_map, REQUIRED_FROZEN_ARTIFACTS, "artifact", errors)
        _require_verified_paths(source_map, REQUIRED_SOURCE_PATHS, "source binding", errors)
        _validate_evaluators(m.get("evaluators", []), errors)
        _validate_frozen_semantics(m.get("evaluators"), errors)

        if status == "frozen":
            illegal = sorted(PREUNBLIND_OUTPUTS & set(artifact_map))
            if illegal:
                errors.append(f"frozen manifest cannot already bind post-S1 scoring outputs: {illegal}")
        if status in ANALYZABLE:
            _validate_score_lock(unblinding_time, artifact_map, errors)
            _validate_blinding_guesses(m.get("evaluators", []), m.get("final_adjudication", {}).get("status"), errors)
        if status in COMPLETED:
            _validate_completed(m, artifact_map, errors)

    if errors:
        for error in errors:
            print("ERROR:", error, file=sys.stderr)
        return 1
    print(f"VALID {m.get('campaign_id', '<unknown>')} status={status}")
    return 0


def analyze(manifest_path: pathlib.Path):
    try:
        m = load(manifest_path)
    except (OSError, json.JSONDecodeError, ValidationError) as exc:
        print(f"ERROR: manifest cannot be loaded: {exc}", file=sys.stderr)
        return 1
    if validate(manifest_path):
        return 1
    if m["status"] not in ANALYZABLE:
        print("BLOCKED: analysis requires an unblinded/completed frozen campaign.", file=sys.stderr)
        return 2
    metrics = ROOT / BENCHMARK_DIR / "metrics.csv"
    if not metrics.exists():
        print("BLOCKED: metrics.csv is absent.", file=sys.stderr)
        return 2
    print("BLOCKED: statistical execution implementation is not yet frozen for this prepared campaign.", file=sys.stderr)
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
