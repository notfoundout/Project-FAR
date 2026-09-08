#!/usr/bin/env python3
"""Network-free invariant checker for Project FAR living-repository infrastructure."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from tools.run_living_research import (
    AUTHORITY_BOUNDARY,
    CLAIM_PATH,
    CONFIG_PATH,
    CANDIDATE_DIR,
    RQ_PATH,
    STATE_PATH,
    THREAT_PATH,
    claim_index,
    read_json,
    validate_bindings,
)
from tools.reconcile_living_repo import SURFACES_PATH

ROOT = Path(".")
LIFECYCLE_PATH = Path("research/living/lifecycle-v1.0.json")
REPOSITORY_STATE_PATH = Path("research/living/repository-state-v1.0.json")
DASHBOARD_PATH = Path("docs/research/living-research-status.md")
REPOSITORY_STATUS_PATH = Path("docs/research/living-repository-status.md")
RUN_DIR = Path("research/living/runs")


class CheckError(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise CheckError(message)


def question_map(registry: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {q["id"]: q for q in registry.get("questions", []) if isinstance(q, dict) and isinstance(q.get("id"), str)}


def validate_config() -> tuple[dict[str, Any], dict[str, dict[str, Any]], list[str]]:
    config = read_json(ROOT / CONFIG_PATH)
    rq = read_json(ROOT / RQ_PATH)
    threats = read_json(ROOT / THREAT_PATH)
    claims = read_json(ROOT / CLAIM_PATH)
    validate_bindings(config, rq, threats, claims)
    require(config.get("schedule_intent") == "every_30_minutes", "schedule_intent drift")
    sources = config.get("sources", {})
    require(sources.get("crossref", {}).get("endpoint") == "https://api.crossref.org/works", "Crossref endpoint drift")
    require(sources.get("openalex", {}).get("endpoint") == "https://api.openalex.org/works", "OpenAlex endpoint drift")
    require(sources.get("openlibrary", {}).get("endpoint") == "https://openlibrary.org/search.json", "Open Library endpoint drift")
    require(int(sources["openlibrary"].get("interval_runs", 0)) >= 4, "Open Library lane must remain low volume")
    require(int(config["historical_backfill"].get("min_year", 9999)) <= 1600, "historical backfill no longer reaches early modern sources")
    return config, question_map(rq), list(claim_index(claims))


def validate_lifecycle() -> None:
    lifecycle = read_json(ROOT / LIFECYCLE_PATH)
    require(lifecycle.get("authority") == "Research", "lifecycle authority drift")
    require(lifecycle.get("authority_boundary") == AUTHORITY_BOUNDARY, "lifecycle boundary drift")
    stages = lifecycle.get("stages")
    require(isinstance(stages, list) and len(stages) >= 7, "lifecycle stages missing")
    ids = [s.get("id") for s in stages if isinstance(s, dict)]
    require(ids[0] == "DISCOVERED" and ids[-1] == "CANONICAL", "lifecycle endpoint drift")
    for stage in stages[1:]:
        require(stage.get("automation_may_enter") is False, f"automation cannot self-promote into {stage.get('id')}")


def validate_surfaces() -> None:
    surfaces = read_json(ROOT / SURFACES_PATH)
    require(surfaces.get("authority") == "Research", "surface registry authority drift")
    require(surfaces.get("authority_boundary") == AUTHORITY_BOUNDARY, "surface boundary drift")
    rows = surfaces.get("surfaces")
    require(isinstance(rows, list) and len(rows) >= 15, "insufficient canonical surface coverage")
    paths = [row.get("path") for row in rows if isinstance(row, dict)]
    require(len(paths) == len(set(paths)), "duplicate canonical surface")
    required = {
        "docs/project-status.md",
        "docs/governance/limitations-register.md",
        "docs/governance/open-problems-register.md",
        "theory/terminal/project-far-core-theory-v1.1.json",
        "theory/evaluation/far-core-assurance-v1.0.json",
        "research/registry/research-questions-v1.0.json",
    }
    require(required.issubset(set(paths)), "required living surfaces missing")
    for path in paths:
        require(isinstance(path, str) and (ROOT / path).is_file(), f"missing tracked surface: {path}")


def validate_state(config: dict[str, Any]) -> None:
    state = read_json(ROOT / STATE_PATH)
    require(state.get("program_id") == "FAR-LIVING-RESEARCH-001", "state program drift")
    require(isinstance(state.get("run_count"), int) and state["run_count"] >= 0, "invalid run_count")
    historical = state.get("historical")
    require(isinstance(historical, dict), "historical state missing")
    require(isinstance(historical.get("query_index"), int), "historical query index invalid")
    require(isinstance(historical.get("window_end_year"), int), "historical year cursor invalid")
    require(isinstance(historical.get("complete"), bool), "historical complete flag invalid")
    ol = state.get("openlibrary")
    require(isinstance(ol, dict) and int(ol.get("page", 0)) >= 1, "Open Library state invalid")
    require(state.get("last_run_status") in {"NEVER_RUN", "SUCCESS", "PARTIAL_SOURCE_FAILURE"}, "invalid last_run_status")


def validate_candidates(config: dict[str, Any], questions: dict[str, dict[str, Any]], claim_ids: list[str]) -> int:
    count = 0
    target_by_id = {t["target_id"]: t for t in config["targets"]}
    historical_ids = {q["id"] for q in config["historical_backfill"]["queries"]} | {q["id"] for q in config["historical_backfill"].get("book_queries", [])}
    for path in sorted((ROOT / CANDIDATE_DIR).glob("FAR-LIT-*.json")):
        count += 1
        record = read_json(path)
        cid = record.get("candidate_id")
        require(isinstance(cid, str) and re.fullmatch(r"FAR-LIT-[0-9A-F]{16}", cid) is not None, f"{path}: invalid id")
        require(path.name == f"{cid}.json", f"{path}: filename/id mismatch")
        require(record.get("authority") == "Research", f"{cid}: authority drift")
        require(record.get("authority_boundary") == AUTHORITY_BOUNDARY, f"{cid}: boundary drift")
        require(record.get("source_key"), f"{cid}: source_key missing")
        sources = record.get("sources")
        require(isinstance(sources, list) and sources, f"{cid}: sources missing")
        providers = {s.get("provider") for s in sources if isinstance(s, dict)}
        require(providers <= {"Crossref", "OpenAlex", "Open Library"}, f"{cid}: unknown provider")
        lifecycle = record.get("lifecycle")
        require(isinstance(lifecycle, dict) and lifecycle.get("stage") == "DISCOVERED", f"{cid}: automation stage escalation")
        for flag in ("may_change_claim_status", "may_establish_novelty", "may_execute_efr", "may_count_as_external_independence"):
            require(lifecycle.get(flag) is False, f"{cid}: forbidden permission {flag}")
        potential = record.get("potential_claim_ids")
        require(isinstance(potential, list) and all(x in claim_ids for x in potential), f"{cid}: invalid potential claim mapping")
        binds = record.get("discovery", {}).get("query_bindings", [])
        require(isinstance(binds, list) and binds, f"{cid}: query bindings missing")
        seen_keys = set()
        for binding in binds:
            require(isinstance(binding, dict), f"{cid}: malformed binding")
            target_id = binding.get("target_id")
            require(target_id in questions, f"{cid}: unknown target binding")
            mode = binding.get("mode")
            require(mode in {"incremental", "historical_backfill"}, f"{cid}: invalid binding mode")
            if mode == "incremental":
                target = target_by_id.get(target_id)
                require(target is not None and binding.get("query") in target["queries"], f"{cid}: unregistered incremental query")
            else:
                require(binding.get("historical_query_id") in historical_ids, f"{cid}: unregistered historical query")
            key = (binding.get("provider"), target_id, binding.get("query"), binding.get("historical_query_id"))
            require(key not in seen_keys, f"{cid}: duplicate binding")
            seen_keys.add(key)
    return count


def validate_runs() -> None:
    for path in sorted((ROOT / RUN_DIR).glob("*.json")):
        run = read_json(path)
        require(run.get("authority") == "Research", f"{path}: authority drift")
        require(run.get("authority_boundary") == AUTHORITY_BOUNDARY, f"{path}: boundary drift")
        status = run.get("status")
        require(status in {"SUCCESS", "PARTIAL_SOURCE_FAILURE"}, f"{path}: invalid status")
        failures = run.get("failures")
        require(isinstance(failures, list), f"{path}: failures not array")
        if status == "SUCCESS":
            require(not failures, f"{path}: SUCCESS contains failures")
            require(run.get("cursor_advanced") is True, f"{path}: SUCCESS did not advance incremental cursor")
        else:
            require(failures, f"{path}: partial failure missing failure records")


def validate_generated(candidate_count: int) -> None:
    if REPOSITORY_STATE_PATH.exists():
        repo = read_json(REPOSITORY_STATE_PATH)
        require(repo.get("program_id") == "FAR-LIVING-REPOSITORY-001", "repository state program drift")
        require(repo.get("authority") == "Research", "repository state authority drift")
        require(repo.get("authority_boundary") == AUTHORITY_BOUNDARY, "repository state boundary drift")
        require(len(repo.get("claims", [])) == 14, "repository reconciliation must contain 14 claims")
        require(repo.get("candidate_counts", {}).get("candidates") == candidate_count, "repository candidate count mismatch")
        for item in repo.get("core_claim_review_queue", []):
            require(item.get("epistemic_status") == "METADATA_SIGNAL_ONLY", "review queue overclaim")
            require(item.get("stage") == "REVIEW_REQUIRED", "review queue stage drift")
    for path in (DASHBOARD_PATH, REPOSITORY_STATUS_PATH):
        if path.exists():
            text = path.read_text(encoding="utf-8")
            require(AUTHORITY_BOUNDARY in text, f"{path}: missing authority boundary")


def main() -> int:
    config, questions, claims = validate_config()
    validate_lifecycle()
    validate_surfaces()
    validate_state(config)
    count = validate_candidates(config, questions, claims)
    validate_runs()
    validate_generated(count)
    print(f"living repository invariants: PASS ({count} candidates)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
