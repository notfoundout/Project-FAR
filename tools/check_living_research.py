#!/usr/bin/env python3
"""Validate FAR-LIVING-RESEARCH-001 without network access."""
from __future__ import annotations

import argparse
import re
from pathlib import Path

from run_living_research import (
    AUTHORITY_BOUNDARY,
    CANDIDATE_DIR,
    CONFIG_PATH,
    DASHBOARD_PATH,
    RQ_PATH,
    RUN_DIR,
    STATE_PATH,
    THREAT_PATH,
    _candidate_id,
    _read_json,
    _sha256_text,
    validate_bindings,
)

ALLOWED_RUN_STATUSES = {"SUCCESS", "PARTIAL_SOURCE_FAILURE"}


def check(root: Path) -> list[str]:
    errors: list[str] = []
    try:
        config = _read_json(root / CONFIG_PATH)
        questions = validate_bindings(config, _read_json(root / RQ_PATH), _read_json(root / THREAT_PATH))
    except Exception as exc:
        return [f"configuration: {type(exc).__name__}: {exc}"]
    target_config = {target["target_id"]: target for target in config["targets"]}
    try:
        state = _read_json(root / STATE_PATH)
    except Exception as exc:
        return [f"state: {type(exc).__name__}: {exc}"]
    if state.get("program_id") != "FAR-LIVING-RESEARCH-001":
        errors.append("state program_id mismatch")
    if state.get("last_run_status") not in ALLOWED_RUN_STATUSES | {"NEVER_RUN"}:
        errors.append("state last_run_status invalid")

    candidate_paths = sorted((root / CANDIDATE_DIR).glob("*.json")) if (root / CANDIDATE_DIR).exists() else []
    for path in candidate_paths:
        try:
            record = _read_json(path)
        except Exception as exc:
            errors.append(f"{path}: unreadable candidate: {exc}")
            continue
        cid = record.get("candidate_id")
        source = record.get("source")
        source_key = source.get("source_key") if isinstance(source, dict) else None
        if not isinstance(cid, str) or not re.fullmatch(r"FAR-LIT-[0-9A-F]{16}", cid):
            errors.append(f"{path}: invalid candidate_id")
            continue
        if path.name != f"{cid}.json":
            errors.append(f"{path}: filename/candidate_id mismatch")
        if not isinstance(source_key, str) or _candidate_id(source_key) != cid:
            errors.append(f"{path}: source identity hash mismatch")
        if record.get("authority") != "Research":
            errors.append(f"{path}: candidate authority must be Research")
        boundary = record.get("epistemic_boundary")
        if not isinstance(boundary, dict) or boundary.get("statement") != AUTHORITY_BOUNDARY:
            errors.append(f"{path}: authority boundary missing or changed")
        else:
            for field in ("may_change_claim_status", "may_establish_novelty", "may_execute_efr", "may_count_as_external_independence"):
                if boundary.get(field) is not False:
                    errors.append(f"{path}: {field} must be false")
        discovery = record.get("discovery")
        bindings = discovery.get("query_bindings", []) if isinstance(discovery, dict) else []
        if not isinstance(bindings, list) or not bindings:
            errors.append(f"{path}: candidate has no query binding")
            continue
        seen: set[tuple[str, str]] = set()
        for binding in bindings:
            if not isinstance(binding, dict):
                errors.append(f"{path}: malformed query binding")
                continue
            target_id, query = binding.get("target_id"), binding.get("query")
            key = (str(target_id), str(query))
            if key in seen:
                errors.append(f"{path}: duplicate query binding {key}")
            seen.add(key)
            if target_id not in target_config or target_id not in questions:
                errors.append(f"{path}: unknown target {target_id!r}")
                continue
            target = target_config[target_id]
            if query not in target["queries"]:
                errors.append(f"{path}: query is not registered for {target_id}")
            if binding.get("candidate_relation") != target["candidate_relation"]:
                errors.append(f"{path}: candidate relation drift for {target_id}")
            expected_hash = _sha256_text(str(questions[target_id].get("exact_question", "")))
            if binding.get("governed_question_sha256") != expected_hash:
                errors.append(f"{path}: governed question hash drift for {target_id}")
    if state.get("total_unique_candidates") != len(candidate_paths):
        errors.append("state total_unique_candidates does not match candidate files")

    run_paths = sorted((root / RUN_DIR).glob("*.json")) if (root / RUN_DIR).exists() else []
    for path in run_paths:
        try:
            run = _read_json(path)
        except Exception as exc:
            errors.append(f"{path}: unreadable run report: {exc}")
            continue
        if run.get("program_id") != "FAR-LIVING-RESEARCH-001" or run.get("authority") != "Research":
            errors.append(f"{path}: run authority/program mismatch")
        if run.get("authority_boundary") != AUTHORITY_BOUNDARY:
            errors.append(f"{path}: run authority boundary drift")
        summary, failures = run.get("summary"), run.get("failures")
        if not isinstance(summary, dict) or summary.get("status") not in ALLOWED_RUN_STATUSES:
            errors.append(f"{path}: invalid run summary/status")
            continue
        if not isinstance(failures, list):
            errors.append(f"{path}: failures must be an array")
            continue
        if summary["status"] == "SUCCESS":
            if failures or summary.get("queries_failed") != 0 or summary.get("cursor_advanced") is not True:
                errors.append(f"{path}: successful run has inconsistent failure/cursor state")
        elif not failures or summary.get("queries_failed", 0) < 1 or summary.get("cursor_advanced") is not False:
            errors.append(f"{path}: partial failure must preserve failures and freeze cursor")

    dashboard = root / DASHBOARD_PATH
    if not dashboard.exists():
        errors.append(f"missing generated dashboard: {DASHBOARD_PATH}")
    else:
        text = dashboard.read_text(encoding="utf-8")
        for needle in ("Generated Research view; never theory or evidence authority", AUTHORITY_BOUNDARY, f"Unique candidate records: **{len(candidate_paths)}**"):
            if needle not in text:
                errors.append(f"dashboard missing expected text: {needle}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Project FAR living-research state")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    root = args.root.resolve()
    errors = check(root)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    candidates = len(list((root / CANDIDATE_DIR).glob("*.json"))) if (root / CANDIDATE_DIR).exists() else 0
    runs = len(list((root / RUN_DIR).glob("*.json"))) if (root / RUN_DIR).exists() else 0
    print(f"living research validation passed: {candidates} candidates, {runs} run reports")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
