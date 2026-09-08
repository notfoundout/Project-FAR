#!/usr/bin/env python3
"""Unattended, fail-closed literature discovery for Project FAR.

This tool discovers *candidate* research records only. It never changes theorem,
claim, evidence, EFR, novelty, or acceptance status. Source failures and rejected
results are preserved in per-run reports so absence is never inferred from failure.
"""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import os
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Callable, Iterable

CONFIG_PATH = Path("research/living/config-v1.0.json")
STATE_PATH = Path("research/living/state-v1.0.json")
RQ_PATH = Path("research/registry/research-questions-v1.0.json")
THREAT_PATH = Path("research/registry/epistemic-threats-v1.0.json")
CANDIDATE_DIR = Path("research/living/inbox/candidates")
RUN_DIR = Path("research/living/runs")
DASHBOARD_PATH = Path("docs/research/living-research-status.md")

AUTHORITY_BOUNDARY = (
    "Research candidate only. Discovery or triage does not establish support, dispute, "
    "novelty, priority, external validity, utility, independence, theorem status, EFR result, "
    "or any other Project FAR claim/evidence disposition."
)
_TAG_RE = re.compile(r"<[^>]+>")
_SPACE_RE = re.compile(r"\s+")


class LivingResearchError(RuntimeError):
    """Configuration or invariant failure; never a negative search result."""


@dataclass(frozen=True)
class QueryResult:
    items: list[dict[str, Any]]
    request: dict[str, Any]


def _read_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise LivingResearchError(f"expected JSON object: {path}")
    return value


def _write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")


def _utc_iso(value: datetime) -> str:
    return value.astimezone(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def _parse_utc(value: str) -> datetime:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise LivingResearchError(f"timestamp must include timezone: {value}")
    return parsed.astimezone(timezone.utc)


def _sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _clean_text(value: Any, limit: int = 4000) -> str:
    if value is None:
        return ""
    if isinstance(value, list):
        value = " ".join(str(part) for part in value if part is not None)
    text = html.unescape(_TAG_RE.sub(" ", str(value)))
    return _SPACE_RE.sub(" ", text).strip()[:limit]


def _first(item: dict[str, Any], key: str) -> str:
    value = item.get(key)
    return _clean_text(value[0]) if isinstance(value, list) and value else _clean_text(value)


def _source_key(item: dict[str, Any]) -> str:
    doi = _clean_text(item.get("DOI"), 500).lower()
    if doi:
        return f"doi:{doi}"
    stable = {
        "title": _first(item, "title").lower(),
        "publisher": _clean_text(item.get("publisher"), 500).lower(),
        "type": _clean_text(item.get("type"), 100).lower(),
        "published": item.get("published") or item.get("issued") or {},
    }
    encoded = json.dumps(stable, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return f"crossref-fallback:{_sha256_text(encoded)}"


def _candidate_id(source_key: str) -> str:
    return "FAR-LIT-" + _sha256_text(source_key)[:16].upper()


def _item_search_text(item: dict[str, Any]) -> str:
    fields = [item.get(key) for key in ("title", "subtitle", "abstract", "subject", "container-title", "publisher")]
    return " ".join(_clean_text(field).lower() for field in fields if field)


def _signal_hits(item: dict[str, Any], terms: Iterable[str]) -> list[str]:
    haystack = _item_search_text(item)
    hits = [term for term in terms if (normalized := _clean_text(term, 200).lower()) and normalized in haystack]
    return sorted(set(hits), key=str.lower)


def _attention_hits(item: dict[str, Any], terms: Iterable[str]) -> list[str]:
    haystack = _item_search_text(item)
    return sorted({term for term in terms if term.lower() in haystack}, key=str.lower)


def _authors(item: dict[str, Any], limit: int = 25) -> list[str]:
    raw = item.get("author")
    if not isinstance(raw, list):
        return []
    result: list[str] = []
    for author in raw[:limit]:
        if not isinstance(author, dict):
            continue
        name = " ".join(part for part in (_clean_text(author.get("given"), 200), _clean_text(author.get("family"), 200)) if part)
        if name:
            result.append(name)
    return result


def _published_date(item: dict[str, Any]) -> str | None:
    for key in ("published-online", "published-print", "published", "issued", "created"):
        value = item.get(key)
        if not isinstance(value, dict):
            continue
        parts = value.get("date-parts")
        if not isinstance(parts, list) or not parts or not isinstance(parts[0], list) or not parts[0]:
            continue
        try:
            nums = parts[0]
            year = int(nums[0])
            month = int(nums[1]) if len(nums) > 1 else 1
            day = int(nums[2]) if len(nums) > 2 else 1
            return f"{year:04d}-{month:02d}-{day:02d}"
        except (TypeError, ValueError):
            continue
    return None


def _indexed_timestamp(item: dict[str, Any]) -> str | None:
    indexed = item.get("indexed")
    value = indexed.get("date-time") if isinstance(indexed, dict) else None
    return value if isinstance(value, str) else None


def _candidate_source(item: dict[str, Any]) -> dict[str, Any]:
    return {
        "provider": "Crossref REST API",
        "source_key": _source_key(item),
        "doi": _clean_text(item.get("DOI"), 500) or None,
        "url": _clean_text(item.get("URL"), 2000) or None,
        "title": _first(item, "title"),
        "authors": _authors(item),
        "container_title": _first(item, "container-title") or None,
        "publisher": _clean_text(item.get("publisher"), 500) or None,
        "work_type": _clean_text(item.get("type"), 100) or None,
        "published_date": _published_date(item),
        "indexed_timestamp": _indexed_timestamp(item),
    }


def _question_index(registry: dict[str, Any]) -> dict[str, dict[str, Any]]:
    questions = registry.get("questions")
    if not isinstance(questions, list):
        raise LivingResearchError("research-question registry missing questions array")
    result: dict[str, dict[str, Any]] = {}
    for question in questions:
        if not isinstance(question, dict) or not isinstance(question.get("id"), str):
            raise LivingResearchError("malformed research-question registry entry")
        if question["id"] in result:
            raise LivingResearchError(f"duplicate research question: {question['id']}")
        result[question["id"]] = question
    return result


def _threat_ids(registry: dict[str, Any]) -> set[str]:
    threats = registry.get("threats")
    if not isinstance(threats, list):
        raise LivingResearchError("epistemic-threat registry missing threats array")
    result: set[str] = set()
    for threat in threats:
        if not isinstance(threat, dict) or not isinstance(threat.get("id"), str):
            raise LivingResearchError("malformed epistemic-threat registry entry")
        result.add(threat["id"])
    return result


def validate_bindings(config: dict[str, Any], rq_registry: dict[str, Any], threat_registry: dict[str, Any]) -> dict[str, dict[str, Any]]:
    if config.get("program_id") != "FAR-LIVING-RESEARCH-001":
        raise LivingResearchError("unexpected living-research program_id")
    if config.get("authority_boundary") != AUTHORITY_BOUNDARY:
        raise LivingResearchError("authority boundary drift")
    questions = _question_index(rq_registry)
    threats = _threat_ids(threat_registry)
    guards = config.get("threat_guards")
    if not isinstance(guards, list) or not guards:
        raise LivingResearchError("threat_guards must be a nonempty array")
    missing_guards = sorted(set(guards) - threats)
    if missing_guards:
        raise LivingResearchError(f"unknown threat guard(s): {', '.join(missing_guards)}")
    targets = config.get("targets")
    if not isinstance(targets, list) or not targets:
        raise LivingResearchError("targets must be a nonempty array")
    seen: set[str] = set()
    for target in targets:
        if not isinstance(target, dict):
            raise LivingResearchError("target must be an object")
        target_id = target.get("target_id")
        if not isinstance(target_id, str) or target_id not in questions:
            raise LivingResearchError(f"unknown target_id: {target_id!r}")
        if target_id in seen:
            raise LivingResearchError(f"duplicate target_id: {target_id}")
        seen.add(target_id)
        allowed = target.get("allowed_dispositions")
        if not isinstance(allowed, list) or not allowed:
            raise LivingResearchError(f"{target_id}: allowed_dispositions must be nonempty")
        disposition = questions[target_id].get("current_disposition")
        if disposition not in allowed:
            raise LivingResearchError(f"{target_id}: current disposition {disposition!r} is not watched; update config deliberately")
        queries = target.get("queries")
        if not isinstance(queries, list) or not queries or not all(isinstance(q, str) and q.strip() for q in queries):
            raise LivingResearchError(f"{target_id}: queries must be nonempty strings")
        terms = target.get("signal_terms")
        if not isinstance(terms, list) or not terms or not all(isinstance(t, str) and t.strip() for t in terms):
            raise LivingResearchError(f"{target_id}: signal_terms must be nonempty strings")
        if not isinstance(target.get("candidate_relation"), str):
            raise LivingResearchError(f"{target_id}: candidate_relation is required")
    return questions


def _default_transport(url: str, headers: dict[str, str], timeout: int) -> dict[str, Any]:
    request = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(request, timeout=timeout) as response:
        data = response.read()
    decoded = json.loads(data.decode("utf-8"))
    if not isinstance(decoded, dict):
        raise LivingResearchError("Crossref response was not a JSON object")
    return decoded


def crossref_query(query: str, start_date: str, end_date: str, source: dict[str, Any], *, transport: Callable[[str, dict[str, str], int], dict[str, Any]] = _default_transport, sleep_fn: Callable[[float], None] = time.sleep) -> QueryResult:
    endpoint = source.get("endpoint")
    if endpoint != "https://api.crossref.org/works":
        raise LivingResearchError("Crossref endpoint drift")
    rows = int(source.get("rows_per_query", 8))
    timeout = int(source.get("timeout_seconds", 30))
    retries = int(source.get("max_retries", 3))
    params = {
        "query.bibliographic": query,
        "filter": f"from-index-date:{start_date},until-index-date:{end_date}",
        "rows": str(rows),
        "sort": "indexed",
        "order": "desc",
    }
    mailto = os.environ.get("CROSSREF_MAILTO", "").strip()
    if mailto:
        params["mailto"] = mailto
    url = endpoint + "?" + urllib.parse.urlencode(params)
    headers = {"Accept": "application/json", "User-Agent": str(source.get("user_agent", "Project-FAR-Living-Research/1.0"))}
    last_error: Exception | None = None
    for attempt in range(retries + 1):
        try:
            payload = transport(url, headers, timeout)
            message = payload.get("message")
            if not isinstance(message, dict):
                raise LivingResearchError("Crossref response missing message object")
            items = message.get("items")
            if not isinstance(items, list):
                raise LivingResearchError("Crossref response missing items array")
            clean_items = [item for item in items if isinstance(item, dict)]
            return QueryResult(items=clean_items, request={"provider": "Crossref REST API", "endpoint": endpoint, "parameters": params, "rows_returned": len(clean_items)})
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, json.JSONDecodeError, LivingResearchError) as exc:
            last_error = exc
            if attempt >= retries:
                break
            sleep_fn(min(2**attempt, 8))
    assert last_error is not None
    raise last_error


def _load_state(root: Path) -> dict[str, Any]:
    path = root / STATE_PATH
    if not path.exists():
        return {"schema_version": "1.0", "program_id": "FAR-LIVING-RESEARCH-001", "source_cursor_utc": None, "last_run_id": None, "last_run_status": "NEVER_RUN", "total_unique_candidates": 0, "updated_utc": None}
    state = _read_json(path)
    if state.get("program_id") != "FAR-LIVING-RESEARCH-001":
        raise LivingResearchError("state program_id drift")
    return state


def _candidate_path(root: Path, candidate_id: str) -> Path:
    if not re.fullmatch(r"FAR-LIT-[0-9A-F]{16}", candidate_id):
        raise LivingResearchError(f"unsafe candidate id: {candidate_id}")
    return root / CANDIDATE_DIR / f"{candidate_id}.json"


def _merge_binding(record: dict[str, Any], binding: dict[str, Any], now_iso: str) -> None:
    discovery = record.setdefault("discovery", {})
    if not isinstance(discovery, dict):
        raise LivingResearchError("candidate discovery field must be object")
    bindings = discovery.setdefault("query_bindings", [])
    if not isinstance(bindings, list):
        raise LivingResearchError("candidate query_bindings must be array")
    key = (binding["target_id"], binding["query"])
    existing = {(item.get("target_id"), item.get("query")) for item in bindings if isinstance(item, dict)}
    if key not in existing:
        bindings.append(binding)
        bindings.sort(key=lambda item: (item.get("target_id", ""), item.get("query", "")))
    discovery["last_seen_utc"] = now_iso


def _new_candidate(item: dict[str, Any], candidate_id: str, binding: dict[str, Any], now_iso: str, attention: list[str]) -> dict[str, Any]:
    return {
        "schema_version": "1.0",
        "record_type": "CANDIDATE_LITERATURE",
        "authority": "Research",
        "candidate_id": candidate_id,
        "source": _candidate_source(item),
        "discovery": {"first_seen_utc": now_iso, "last_seen_utc": now_iso, "query_bindings": [binding]},
        "triage": {"status": "UNREVIEWED_CANDIDATE", "attention_terms": attention, "attention": "HIGH" if attention else "NORMAL"},
        "epistemic_boundary": {
            "statement": AUTHORITY_BOUNDARY,
            "may_change_claim_status": False,
            "may_establish_novelty": False,
            "may_execute_efr": False,
            "may_count_as_external_independence": False,
        },
    }


def _make_binding(target: dict[str, Any], question: dict[str, Any], query: str, hits: list[str]) -> dict[str, Any]:
    return {
        "target_id": target["target_id"],
        "candidate_relation": target["candidate_relation"],
        "query": query,
        "signal_terms_hit": hits,
        "governed_question_sha256": _sha256_text(str(question.get("exact_question", ""))),
    }


def _window(state: dict[str, Any], now: datetime, source: dict[str, Any]) -> tuple[datetime, datetime]:
    cursor = state.get("source_cursor_utc")
    start = _parse_utc(cursor) - timedelta(days=int(source.get("overlap_days", 2))) if isinstance(cursor, str) and cursor else now - timedelta(days=int(source.get("initial_lookback_days", 14)))
    return start, now


def _run_id(now: datetime) -> str:
    suffix = re.sub(r"[^A-Za-z0-9_.-]", "-", os.environ.get("GITHUB_RUN_ID", "local"))[:80]
    return now.strftime("%Y%m%dT%H%M%SZ") + "-" + suffix


def render_dashboard(root: Path, state: dict[str, Any]) -> None:
    candidates = sorted((root / CANDIDATE_DIR).glob("FAR-LIT-*.json")) if (root / CANDIDATE_DIR).exists() else []
    high = 0
    targets: dict[str, int] = {}
    for path in candidates:
        record = _read_json(path)
        if record.get("triage", {}).get("attention") == "HIGH":
            high += 1
        bindings = record.get("discovery", {}).get("query_bindings", [])
        if isinstance(bindings, list):
            for binding in bindings:
                if isinstance(binding, dict) and isinstance(binding.get("target_id"), str):
                    targets[binding["target_id"]] = targets.get(binding["target_id"], 0) + 1
    lines = [
        "# Living research status", "", "Status: **Generated Research view; never theory or evidence authority**", "",
        "This page is generated from `research/living/`. Candidate literature remains unreviewed until a separate governed review promotes a relationship. Search absence, model agreement, and automated triage change no Project FAR claim status.", "",
        f"- Last run: `{state.get('last_run_id') or 'never'}`", f"- Last run status: `{state.get('last_run_status') or 'unknown'}`", f"- Source cursor: `{state.get('source_cursor_utc') or 'not established'}`",
        f"- Unique candidate records: **{len(candidates)}**", f"- High-attention candidates: **{high}**", "", "## Candidates by governed research question", "",
    ]
    lines.extend((f"- `{target_id}`: {count}" for target_id, count in sorted(targets.items())) if targets else ["No candidates recorded yet."])
    lines.extend(["", "## Authority boundary", "", AUTHORITY_BOUNDARY, "", "Source failures and result-level rejection reasons are preserved under `research/living/runs/`.", ""])
    path = root / DASHBOARD_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def run_once(root: Path, *, now: datetime | None = None, transport: Callable[[str, dict[str, str], int], dict[str, Any]] = _default_transport, sleep_fn: Callable[[float], None] = time.sleep) -> dict[str, Any]:
    supplied_now = now is not None
    now = (now or datetime.now(timezone.utc)).astimezone(timezone.utc).replace(microsecond=0)
    now_iso = _utc_iso(now)
    config = _read_json(root / CONFIG_PATH)
    questions = validate_bindings(config, _read_json(root / RQ_PATH), _read_json(root / THREAT_PATH))
    state = _load_state(root)
    source = config.get("source")
    if not isinstance(source, dict):
        raise LivingResearchError("source config missing")
    start, end = _window(state, now, source)
    start_date, end_date = start.date().isoformat(), end.date().isoformat()
    run_id = _run_id(now)
    report: dict[str, Any] = {
        "schema_version": "1.0", "program_id": "FAR-LIVING-RESEARCH-001", "run_id": run_id, "authority": "Research", "authority_boundary": AUTHORITY_BOUNDARY,
        "started_utc": now_iso, "source_window": {"from_index_date": start_date, "until_index_date": end_date, "overlap_days": int(source.get("overlap_days", 2))},
        "queries": [], "failures": [], "summary": {},
    }
    seen_in_run: set[tuple[str, str, str]] = set()
    accepted_new = accepted_seen = rejected = 0
    all_queries_succeeded = True
    attention_terms = config.get("attention_terms", [])
    if not isinstance(attention_terms, list):
        raise LivingResearchError("attention_terms must be an array")

    for target in config["targets"]:
        question = questions[target["target_id"]]
        min_hits = int(target.get("min_signal_hits", 1))
        cap = int(target.get("max_candidates_per_query", 3))
        for query in target["queries"]:
            qreport: dict[str, Any] = {"target_id": target["target_id"], "candidate_relation": target["candidate_relation"], "query": query, "governed_question_sha256": _sha256_text(str(question.get("exact_question", ""))), "request": None, "results": []}
            try:
                result = crossref_query(query, start_date, end_date, source, transport=transport, sleep_fn=sleep_fn)
                qreport["request"] = result.request
            except Exception as exc:
                all_queries_succeeded = False
                failure = {"target_id": target["target_id"], "query": query, "error_type": type(exc).__name__, "error": _clean_text(str(exc), 1000)}
                report["failures"].append(failure)
                qreport["failure"] = failure
                report["queries"].append(qreport)
                continue
            accepted_for_query = 0
            for rank, item in enumerate(result.items, start=1):
                source_key = _source_key(item)
                cid = _candidate_id(source_key)
                hits = _signal_hits(item, target["signal_terms"])
                decision, reason = "REJECTED", "NO_SIGNAL_TERM"
                if len(hits) >= min_hits and accepted_for_query < cap:
                    dedup_key = (cid, target["target_id"], query)
                    if dedup_key in seen_in_run:
                        decision, reason = "ACCEPTED_DUPLICATE_IN_RUN", "DUPLICATE_SOURCE_BINDING"
                    else:
                        seen_in_run.add(dedup_key)
                        accepted_for_query += 1
                        binding = _make_binding(target, question, query, hits)
                        path = _candidate_path(root, cid)
                        if path.exists():
                            record = _read_json(path)
                            if record.get("candidate_id") != cid or record.get("source", {}).get("source_key") != source_key:
                                raise LivingResearchError(f"candidate identity collision: {cid}")
                            _merge_binding(record, binding, now_iso)
                            _write_json(path, record)
                            accepted_seen += 1
                            decision, reason = "ACCEPTED_SEEN", "MATCHED_AND_DEDUPED"
                        else:
                            _write_json(path, _new_candidate(item, cid, binding, now_iso, _attention_hits(item, attention_terms)))
                            accepted_new += 1
                            decision, reason = "ACCEPTED_NEW", "MATCHED_SIGNAL_TERMS"
                elif len(hits) >= min_hits:
                    rejected += 1
                    reason = "QUERY_ACCEPTANCE_CAP"
                else:
                    rejected += 1
                qreport["results"].append({"rank": rank, "candidate_id": cid, "source_key": source_key, "title": _first(item, "title")[:500], "decision": decision, "reason": reason, "signal_terms_hit": hits})
            report["queries"].append(qreport)

    status = "SUCCESS" if all_queries_succeeded else "PARTIAL_SOURCE_FAILURE"
    state.update({"last_run_id": run_id, "last_run_status": status, "updated_utc": now_iso})
    if all_queries_succeeded:
        state["source_cursor_utc"] = now_iso
    count = len(list((root / CANDIDATE_DIR).glob("FAR-LIT-*.json"))) if (root / CANDIDATE_DIR).exists() else 0
    state["total_unique_candidates"] = count
    report["summary"] = {"status": status, "queries_total": len(report["queries"]), "queries_failed": len(report["failures"]), "accepted_new": accepted_new, "accepted_seen": accepted_seen, "rejected_results": rejected, "unique_candidates_after_run": count, "cursor_advanced": all_queries_succeeded}
    report["finished_utc"] = now_iso if supplied_now else _utc_iso(datetime.now(timezone.utc))
    _write_json(root / RUN_DIR / f"{run_id}.json", report)
    _write_json(root / STATE_PATH, state)
    render_dashboard(root, state)
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the Project FAR unattended research discovery loop")
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--now", help="Override UTC time for deterministic testing, e.g. 2026-09-08T02:00:00Z")
    args = parser.parse_args()
    report = run_once(args.root.resolve(), now=_parse_utc(args.now) if args.now else None)
    print(json.dumps(report["summary"], indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
