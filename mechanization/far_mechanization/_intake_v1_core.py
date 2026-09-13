"""Governed pre-contract intake for Project FAR."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

from jsonschema import Draft202012Validator

REPO_ROOT = Path(__file__).resolve().parents[2]
SCHEMA_PATH = REPO_ROOT / "schemas" / "far-intake-v1.schema.json"
FORMAT_VERSION = "far-intake/1.0"
SOURCE_TYPES = {"PRIMARY", "SCHOLARLY", "REFERENCE", "USER_SUPPLIED", "OTHER"}
ORIGINS = {"SOURCE_EXPLICIT", "SOURCE_SYNTHESIS", "INFERENCE"}
EXCLUSION_REASONS = {
    "DUPLICATE",
    "WRONG_DOMAIN",
    "ANACHRONISTIC",
    "UNSUPPORTED",
    "INCOMPATIBLE_WITH_SCOPE",
    "OTHER",
}
EXCLUSION_BASES = {"RAW_INPUT", "SOURCE", "INFERENCE"}
PARAMETER_BASES = {"RAW_INPUT", "SOURCE", "INTERPRETATION", "ASSUMPTION", "INFERENCE"}
EVALUATION_OUTCOMES = {
    "PROVED",
    "REFUTED",
    "UNDERDETERMINED",
    "OPEN",
    "BLOCKED",
    "NOT_APPLICABLE",
    "Unknown",
}
_HEX64 = re.compile(r"^[0-9a-f]{64}$")
_ID = re.compile(r"^[A-Za-z][A-Za-z0-9_.:-]*$")


def canonical_json(value: Any) -> str:
    return json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    )


def sha256_json(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode()).hexdigest()


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode()).hexdigest()


def _checked_sha256_json(value: Any, label: str, errors: list[str]) -> str | None:
    try:
        return sha256_json(value)
    except (TypeError, ValueError):
        errors.append(f"{label} is not canonical-JSON serializable")
        return None


def _timestamp(value: Any) -> datetime | None:
    if not isinstance(value, str) or not value:
        return None
    try:
        result = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except (TypeError, ValueError):
        return None
    return result if result.tzinfo else None


def _duplicates(values: Iterable[str]) -> set[str]:
    seen: set[str] = set()
    duplicates: set[str] = set()
    for value in values:
        if value in seen:
            duplicates.add(value)
        else:
            seen.add(value)
    return duplicates


def _index(items: Any, label: str, errors: list[str]) -> dict[str, dict[str, Any]]:
    if not isinstance(items, list):
        errors.append(f"{label} must be an array")
        return {}
    result: dict[str, dict[str, Any]] = {}
    ids: list[str] = []
    for i, item in enumerate(items):
        if not isinstance(item, dict):
            errors.append(f"{label}[{i}] must be an object")
            continue
        ident = item.get("id")
        if not isinstance(ident, str) or not _ID.fullmatch(ident):
            errors.append(f"{label}[{i}].id is invalid")
            continue
        ids.append(ident)
        result[ident] = item
    for ident in sorted(_duplicates(ids)):
        errors.append(f"duplicate {label} id: {ident}")
    return result


def _json_native_errors(value: Any, path: str = "$", _ancestors: set[int] | None = None) -> list[str]:
    """Reject values that cannot exist in a strict JSON data model.

    Programmatic callers can otherwise bypass the parser and supply Python-only
    containers, non-string object keys, custom scalar subclasses, or non-finite
    floats.  Reject them before JSON Schema sees the instance so the schema and
    canonical hash operate on the same data model.
    """
    value_type = type(value)
    ancestors = set() if _ancestors is None else _ancestors
    if value_type in {dict, list}:
        if id(value) in ancestors:
            return [f"{path} is not canonical-JSON serializable: cyclic container"]
        ancestors = ancestors | {id(value)}
    if value_type is dict:
        errors: list[str] = []
        for key, child in value.items():
            if type(key) is not str:
                errors.append(
                    f"{path} has non-string object key of type {type(key).__name__}; value is not canonical-JSON serializable"
                )
                continue
            try:
                key.encode("utf-8")
            except UnicodeEncodeError:
                errors.append(f"{path} has a non-UTF-8 object key {key!r}; value is not canonical-JSON serializable")
                continue
            errors.extend(_json_native_errors(child, f"{path}/{_json_pointer_token(key)}", ancestors))
        return errors
    if value_type is list:
        errors: list[str] = []
        for index, child in enumerate(value):
            errors.extend(_json_native_errors(child, f"{path}/{index}", ancestors))
        return errors
    if value_type is str:
        try:
            value.encode("utf-8")
        except UnicodeEncodeError:
            return [f"{path} is not canonical-JSON serializable: string is not valid UTF-8"]
        return []
    if value_type is int:
        try:
            str(value)
        except ValueError:
            return [f"{path} is not canonical-JSON serializable: integer exceeds the runtime's decimal conversion limit"]
        return []
    if value is None or value_type is bool:
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
    try:
        return _validate_bounded_manifest(manifest, require_complete=require_complete)
    except RecursionError:
        return ["manifest nesting exceeds the supported validation depth"]


def _validate_bounded_manifest(manifest: Any, *, require_complete: bool | None = None) -> list[str]:
    native_errors = _json_native_errors(manifest)
    if native_errors:
        return native_errors

    errors = _validate_manifest(manifest, require_complete=require_complete)
    if errors:
        return errors

    effective_complete = manifest["freeze"]["status"] == "FROZEN" or require_complete
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
    try:
        data = json.loads(
            text,
            object_pairs_hook=_reject_duplicate_object_pairs,
            parse_constant=_reject_nonfinite_constant,
        )
        native_errors = _json_native_errors(data)
    except RecursionError as exc:
        raise ValueError("JSON nesting exceeds the supported parsing depth") from exc
    if native_errors:
        raise ValueError("; ".join(native_errors))
    return data


def _load_schema() -> dict[str, Any]:
    schema = _strict_json_loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    if not isinstance(schema, dict):
        raise ValueError("intake schema root must be an object")
    Draft202012Validator.check_schema(schema)
    return schema


def _schema_errors(manifest: Any) -> list[str]:
    try:
        validator = Draft202012Validator(_load_schema())
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        return [f"schema unavailable or invalid: {exc}"]
    errors = sorted(validator.iter_errors(manifest), key=lambda e: (tuple(str(p) for p in e.path), e.message))
    result: list[str] = []
    for error in errors:
        path = ".".join(str(p) for p in error.path) or "$"
        result.append(f"SCHEMA_CONSTRAINT_VIOLATION {path}: {error.message}")
    return result


def _validate_exclusion_basis(
    row: dict[str, Any],
    label: str,
    sources: dict[str, dict[str, Any]],
    errors: list[str],
) -> None:
    basis = row.get("basis")
    if basis not in EXCLUSION_BASES:
        errors.append(f"{label} has invalid basis")
        return
    source_ids = row.get("source_ids")
    if not isinstance(source_ids, list) or any(s not in sources for s in source_ids):
        errors.append(f"{label} has invalid source_ids")
        source_ids = []
    derivation = row.get("derivation")
    if basis == "SOURCE" and not source_ids:
        errors.append(f"{label} with SOURCE basis requires source provenance")
    if basis in {"RAW_INPUT", "INFERENCE"} and (not isinstance(derivation, str) or not derivation.strip()):
        errors.append(f"{label} with {basis} basis requires explicit derivation")


def _json_pointer_token(value: object) -> str:
    return str(value).replace("~", "~0").replace("/", "~1")


def _json_leaf_paths(value: Any, base: str = "") -> set[str]:
    """Return JSON Pointer paths for every scalar or empty-container leaf."""
    if isinstance(value, dict):
        if not value:
            return {base or "/"}
        result: set[str] = set()
        for key, child in value.items():
            result.update(_json_leaf_paths(child, f"{base}/{_json_pointer_token(key)}"))
        return result
    if isinstance(value, list):
        if not value:
            return {base or "/"}
        result: set[str] = set()
        for index, child in enumerate(value):
            result.update(_json_leaf_paths(child, f"{base}/{index}"))
        return result
    return {base or "/"}


def _validate_materiality_basis(
    term_id: str,
    term: dict[str, Any],
    sources: dict[str, dict[str, Any]],
    errors: list[str],
) -> None:
    basis = term.get("materiality_basis")
    source_ids = term.get("materiality_source_ids")
    derivation = term.get("materiality_derivation")
    if not isinstance(source_ids, list) or any(s not in sources for s in source_ids):
        errors.append(f"term {term_id} has invalid materiality_source_ids")
        source_ids = []
    if basis == "SOURCE" and not source_ids:
        errors.append(f"term {term_id} SOURCE materiality requires source provenance")
    if basis in {"RAW_INPUT", "INFERENCE"} and not (
        isinstance(derivation, str) and derivation.strip()
    ):
        errors.append(f"term {term_id} {basis} materiality requires explicit derivation")


def _validate_parameter_provenance(
    candidate_id: str,
    candidate: dict[str, Any],
    assignments: dict[str, str],
    sources: dict[str, dict[str, Any]],
    interpretations: dict[str, dict[str, Any]],
    assumptions: dict[str, dict[str, Any]],
    errors: list[str],
) -> None:
    rows = candidate.get("parameter_provenance")
    if not isinstance(rows, list):
        errors.append(f"contract candidate {candidate_id}.parameter_provenance must be an array")
        return
    declared_paths: list[str] = []
    assigned_interpretations = set(assignments.values())
    for index, row in enumerate(rows):
        if not isinstance(row, dict):
            errors.append(f"contract candidate {candidate_id}.parameter_provenance[{index}] must be an object")
            continue
        path = row.get("path")
        if isinstance(path, str):
            declared_paths.append(path)
        basis = row.get("basis")
        source_ids = row.get("source_ids")
        interpretation_ids = row.get("interpretation_ids")
        assumption_ids = row.get("assumption_ids")
        if not isinstance(source_ids, list) or any(s not in sources for s in source_ids):
            errors.append(f"contract candidate {candidate_id} provenance {path} has invalid source_ids")
            source_ids = []
        if not isinstance(interpretation_ids, list) or any(i not in interpretations for i in interpretation_ids):
            errors.append(f"contract candidate {candidate_id} provenance {path} has invalid interpretation_ids")
            interpretation_ids = []
        if not isinstance(assumption_ids, list) or any(a not in assumptions for a in assumption_ids):
            errors.append(f"contract candidate {candidate_id} provenance {path} has invalid assumption_ids")
            assumption_ids = []
        if basis == "SOURCE" and not source_ids:
            errors.append(f"contract candidate {candidate_id} provenance {path} SOURCE basis requires source provenance")
        elif basis == "INTERPRETATION":
            if not interpretation_ids:
                errors.append(f"contract candidate {candidate_id} provenance {path} INTERPRETATION basis requires interpretation_ids")
            elif any(i not in assigned_interpretations for i in interpretation_ids):
                errors.append(f"contract candidate {candidate_id} provenance {path} uses interpretation outside candidate assignments")
        elif basis == "ASSUMPTION" and not assumption_ids:
            errors.append(f"contract candidate {candidate_id} provenance {path} ASSUMPTION basis requires assumption_ids")
        if basis not in PARAMETER_BASES:
            errors.append(f"contract candidate {candidate_id} provenance {path} has invalid basis")
    for path in sorted(_duplicates(declared_paths)):
        errors.append(f"contract candidate {candidate_id} has duplicate parameter provenance path {path}")
    try:
        expected_paths = _json_leaf_paths(candidate.get("contract"))
    except (TypeError, ValueError):
        return
    declared_set = set(declared_paths)
    missing = sorted(expected_paths - declared_set)
    extra = sorted(declared_set - expected_paths)
    if missing:
        errors.append(
            f"contract candidate {candidate_id} lacks parameter provenance for: " + ", ".join(missing)
        )
    if extra:
        errors.append(
            f"contract candidate {candidate_id} has provenance for non-leaf paths: " + ", ".join(extra)
        )


def new_manifest(raw_text: str, identifier: str = "FAR-INTAKE-DRAFT") -> dict[str, Any]:
    if not raw_text:
        raise ValueError("raw_text must be non-empty")
    if not _ID.fullmatch(identifier):
        raise ValueError("identifier is invalid")
    return {
        "format_version": FORMAT_VERSION,
        "id": identifier,
        "raw_input": {"text": raw_text, "sha256": sha256_text(raw_text)},
        "discovery": {
            "claim_parses": [],
            "claim_parse_exclusions": [],
            "terms": [],
            "sources": [],
            "interpretations": [],
            "interpretation_exclusions": [],
            "compatibility_exclusions": [],
            "assumptions": [],
            "search_protocol": {
                "evidence_cutoff": None,
                "queries": [],
                "stopping_rule": None,
                "saturation_observations": [],
                "limitations": [],
            },
            "contract_candidates": [],
        },
        "freeze": {"status": "DRAFT", "frozen_at": None, "intake_sha256": None, "freeze_sha256": None},
        "evaluations": [],
    }


def _validate_manifest(manifest: Any, *, require_complete: bool | None = None) -> list[str]:
    schema_errors = _schema_errors(manifest)
    if schema_errors:
        return schema_errors

    errors: list[str] = []
    # Schema validation above guarantees the top-level shape and primitive types.
    assert isinstance(manifest, dict)
    raw = manifest["raw_input"]
    discovery = manifest["discovery"]
    freeze = manifest["freeze"]
    status = freeze["status"]
    require_complete = status == "FROZEN" or require_complete

    if raw["sha256"] != sha256_text(raw["text"]):
        errors.append("raw_input.sha256 mismatch")

    parses = _index(discovery["claim_parses"], "claim_parses", errors)
    terms = _index(discovery["terms"], "terms", errors)
    sources = _index(discovery["sources"], "sources", errors)
    interpretations = _index(discovery["interpretations"], "interpretations", errors)
    candidates = _index(discovery["contract_candidates"], "contract_candidates", errors)

    source_times: list[tuple[str, datetime]] = []
    for sid, source in sources.items():
        if source["source_type"] not in SOURCE_TYPES:
            errors.append(f"source {sid} has invalid source_type")
        if not _HEX64.fullmatch(source["sha256"]):
            errors.append(f"source {sid} requires lowercase SHA-256")
        retrieved = _timestamp(source["retrieved_at"])
        if retrieved is None:
            errors.append(f"source {sid} requires timezone-aware retrieved_at")
        else:
            source_times.append((sid, retrieved))

    per_term: dict[str, set[str]] = {term_id: set() for term_id in terms}
    for iid, row in interpretations.items():
        term_id = row["term_id"]
        if term_id not in terms:
            errors.append(f"interpretation {iid} references unknown term {term_id}")
            continue
        per_term[term_id].add(iid)
        origin = row["origin"]
        if origin not in ORIGINS:
            errors.append(f"interpretation {iid} has invalid origin")
        source_ids = row["source_ids"]
        if any(s not in sources for s in source_ids):
            errors.append(f"interpretation {iid} has invalid source_ids")
            source_ids = []
        if origin in {"SOURCE_EXPLICIT", "SOURCE_SYNTHESIS"} and not source_ids:
            errors.append(f"interpretation {iid} requires source provenance")
        if origin in {"SOURCE_SYNTHESIS", "INFERENCE"} and not (isinstance(row["derivation"], str) and row["derivation"].strip()):
            errors.append(f"interpretation {iid} requires explicit derivation")

    parse_excluded: set[str] = set()
    for i, row in enumerate(discovery["claim_parse_exclusions"]):
        pid = row["claim_parse_id"]
        label = f"claim parse exclusion {pid}"
        if pid not in parses:
            errors.append(f"claim parse exclusion references unknown parse {pid}")
        elif pid in parse_excluded:
            errors.append(f"duplicate claim parse exclusion: {pid}")
        else:
            parse_excluded.add(pid)
        if row["reason_code"] not in EXCLUSION_REASONS:
            errors.append(f"{label} has invalid reason_code")
        _validate_exclusion_basis(row, label, sources, errors)

    interp_excluded: set[str] = set()
    for i, row in enumerate(discovery["interpretation_exclusions"]):
        iid = row["interpretation_id"]
        label = f"interpretation exclusion {iid}"
        if iid not in interpretations:
            errors.append(f"interpretation exclusion references unknown interpretation {iid}")
        elif iid in interp_excluded:
            errors.append(f"duplicate interpretation exclusion: {iid}")
        else:
            interp_excluded.add(iid)
        if row["reason_code"] not in EXCLUSION_REASONS:
            errors.append(f"{label} has invalid reason_code")
        _validate_exclusion_basis(row, label, sources, errors)

    referenced_terms: set[str] = set()
    for pid, parse in parses.items():
        term_ids = parse["term_ids"]
        referenced_terms.update(term_ids)
        unknown = sorted({t for t in term_ids if t not in terms})
        if unknown:
            errors.append(f"claim parse {pid} references unknown terms: {', '.join(unknown)}")
        if parse["origin"] == "INFERENCE" and not (isinstance(parse["derivation"], str) and parse["derivation"].strip()):
            errors.append(f"claim parse {pid} requires derivation")

    for term_id, term in terms.items():
        declared = term["interpretation_ids"]
        if set(declared) != per_term[term_id]:
            errors.append(f"term {term_id}.interpretation_ids must exactly enumerate its interpretations")
        _validate_materiality_basis(term_id, term, sources, errors)
        if term["material"] and term_id not in referenced_terms:
            errors.append(f"material term {term_id} is not referenced by any claim parse")

    assumptions = _index(discovery["assumptions"], "assumptions", errors)
    for aid, row in assumptions.items():
        if any(s not in sources for s in row["source_ids"]):
            errors.append(f"assumption {aid} has invalid source_ids")

    protocol = discovery["search_protocol"]
    queries = protocol["queries"]
    qids: list[str] = []
    query_term_coverage: set[str] = set()
    query_parse_coverage: set[str] = set()
    for i, query in enumerate(queries):
        qid = query["id"]
        qids.append(qid)
        unknown_terms = sorted({tid for tid in query["term_ids"] if tid not in terms})
        unknown_parses = sorted({pid for pid in query["claim_parse_ids"] if pid not in parses})
        if unknown_terms:
            errors.append(f"search query {qid} references unknown terms: {', '.join(unknown_terms)}")
        if unknown_parses:
            errors.append(f"search query {qid} references unknown parses: {', '.join(unknown_parses)}")
        nonmaterial = sorted({tid for tid in query["term_ids"] if tid in terms and terms[tid]["material"] is not True})
        if nonmaterial:
            errors.append(f"search query {qid} targets non-material terms: {', '.join(nonmaterial)}")
        if not query["term_ids"] and not query["claim_parse_ids"]:
            errors.append(f"search query {qid} must target at least one term or claim parse")
        query_term_coverage.update(tid for tid in query["term_ids"] if tid in terms)
        query_parse_coverage.update(pid for pid in query["claim_parse_ids"] if pid in parses)
    for qid in sorted(_duplicates(qids)):
        errors.append(f"duplicate search query id: {qid}")

    active_parses = {pid: row for pid, row in parses.items() if pid not in parse_excluded}
    active_material_terms = {
        tid
        for parse in active_parses.values()
        for tid in parse["term_ids"]
        if tid in terms and terms[tid]["material"] is True
    }

    cutoff = _timestamp(protocol["evidence_cutoff"])
    saturation_times: list[tuple[int, datetime]] = []
    saturation_query_coverage: set[str] = set()
    saturation_source_coverage: set[str] = set()
    rounds: list[int] = []
    for i, row in enumerate(protocol["saturation_observations"]):
        round_number = row["round"]
        rounds.append(round_number)
        observed = _timestamp(row["observed_at"])
        if observed is None:
            errors.append(f"saturation observation round {round_number} requires timezone-aware observed_at")
        else:
            saturation_times.append((round_number, observed))
        unknown_qids = sorted({qid for qid in row["query_ids"] if qid not in set(qids)})
        if unknown_qids:
            errors.append(f"saturation observation round {round_number} references unknown queries: {', '.join(unknown_qids)}")
        saturation_query_coverage.update(qid for qid in row["query_ids"] if qid in set(qids))
        unknown_source_ids = sorted({sid for sid in row["source_ids"] if sid not in sources})
        if unknown_source_ids:
            errors.append(f"saturation observation round {round_number} references unknown sources: {', '.join(unknown_source_ids)}")
        saturation_source_coverage.update(sid for sid in row["source_ids"] if sid in sources)
        if observed is not None:
            source_time_map = dict(source_times)
            for sid in row["source_ids"]:
                retrieved = source_time_map.get(sid)
                if retrieved is not None and observed < retrieved:
                    errors.append(f"saturation observation round {round_number} predates source retrieval {sid}")
        unknown_parses = sorted({pid for pid in row["new_claim_parse_ids"] if pid not in parses})
        if unknown_parses:
            errors.append(f"saturation observation round {round_number} has invalid new_claim_parse_ids")
        unknown_iids = sorted({iid for iid in row["new_material_interpretation_ids"] if iid not in interpretations})
        if unknown_iids:
            errors.append(f"saturation observation round {round_number} has invalid new_material_interpretation_ids")
        nonmaterial_iids = sorted(
            {
                iid
                for iid in row["new_material_interpretation_ids"]
                if iid in interpretations
                and interpretations[iid]["term_id"] in terms
                and terms[interpretations[iid]["term_id"]]["material"] is not True
            }
        )
        if nonmaterial_iids:
            errors.append(f"saturation observation round {round_number} reports non-material interpretations: {', '.join(nonmaterial_iids)}")

    if rounds != sorted(rounds) or len(rounds) != len(set(rounds)):
        errors.append("saturation observation rounds must be unique and strictly increasing")
    if any(later[1] < earlier[1] for earlier, later in zip(saturation_times, saturation_times[1:])):
        errors.append("saturation observation timestamps must be nondecreasing in round order")

    if require_complete:
        if not parses:
            errors.append("freeze requires at least one claim parse")
        if not active_parses:
            errors.append("freeze requires at least one active claim parse")
        if not terms:
            errors.append("freeze requires at least one term")
        if not sources:
            errors.append("freeze requires at least one source")
        if cutoff is None:
            errors.append("freeze requires timezone-aware search_protocol.evidence_cutoff")
        if not queries:
            errors.append("freeze requires a recorded search protocol query")
        if not protocol["stopping_rule"]:
            errors.append("freeze requires search_protocol.stopping_rule")
        if not protocol["saturation_observations"]:
            errors.append("freeze requires saturation_observations")
        else:
            final = protocol["saturation_observations"][-1]
            if final["new_claim_parse_ids"] or final["new_material_interpretation_ids"]:
                errors.append("freeze requires a final saturation observation with no new claim parses or material interpretations")
        if set(qids) - saturation_query_coverage:
            missing_qids = sorted(set(qids) - saturation_query_coverage)
            errors.append("registered search queries lack saturation execution records: " + ", ".join(missing_qids))
        if set(sources) - saturation_source_coverage:
            missing_sources = sorted(set(sources) - saturation_source_coverage)
            errors.append("registered sources lack saturation provenance: " + ", ".join(missing_sources))
        missing_term_search = sorted(active_material_terms - query_term_coverage)
        if missing_term_search:
            errors.append("active material terms lack recorded search coverage: " + ", ".join(missing_term_search))
        missing_parse_search = sorted(set(active_parses) - query_parse_coverage)
        if missing_parse_search:
            errors.append("active claim parses lack recorded search coverage: " + ", ".join(missing_parse_search))
        for pid, parse in active_parses.items():
            for tid in parse["term_ids"]:
                if tid in terms and terms[tid]["material"] is True and not (per_term[tid] - interp_excluded):
                    errors.append(f"active material term {tid} in parse {pid} has no active interpretation")
        if cutoff is not None:
            for sid, retrieved in source_times:
                if retrieved > cutoff:
                    errors.append(f"source {sid} was retrieved after evidence_cutoff")
            for round_number, observed in saturation_times:
                if observed > cutoff:
                    errors.append(f"saturation observation round {round_number} occurred after evidence_cutoff")

    compat = discovery["compatibility_exclusions"]
    excluded_combos: set[tuple[str, tuple[tuple[str, str], ...]]] = set()
    for i, row in enumerate(compat):
        pid, assignments = row["claim_parse_id"], row["assignments"]
        label = f"compatibility exclusion {i}"
        if pid not in parses:
            errors.append(f"compatibility exclusion references unknown parse {pid}")
            continue
        if pid in parse_excluded:
            errors.append(f"compatibility exclusion {i} targets excluded parse {pid}")
            continue
        required = {
            tid
            for tid in parses[pid]["term_ids"]
            if tid in terms and terms[tid]["material"] is True
        }
        if set(assignments) != required:
            errors.append(f"compatibility exclusion {i} assignments must exactly cover material terms for {pid}")
        for tid, iid in assignments.items():
            if iid not in interpretations:
                errors.append(f"compatibility exclusion {i} references unknown interpretation {iid}")
            elif interpretations[iid]["term_id"] != tid:
                errors.append(f"compatibility exclusion {i} assigns {iid} to wrong term {tid}")
            elif iid in interp_excluded:
                errors.append(f"compatibility exclusion {i} redundantly uses excluded interpretation {iid}")
        key = (pid, tuple(sorted((str(k), str(v)) for k, v in assignments.items())))
        if key in excluded_combos:
            errors.append(f"duplicate compatibility exclusion for {pid}: {dict(assignments)}")
        excluded_combos.add(key)
        _validate_exclusion_basis(row, label, sources, errors)

    candidate_keys: dict[tuple[str, tuple[tuple[str, str], ...]], str] = {}
    for cid, row in candidates.items():
        pid, assignments = row["claim_parse_id"], row["assignments"]
        if pid not in parses:
            errors.append(f"contract candidate {cid} references unknown parse {pid}")
            continue
        if pid in parse_excluded:
            errors.append(f"contract candidate {cid} targets excluded parse {pid}")
            continue
        required = {
            tid
            for tid in parses[pid]["term_ids"]
            if tid in terms and terms[tid]["material"] is True
        }
        if set(assignments) != required:
            errors.append(f"contract candidate {cid} assignments must exactly cover material terms for {pid}")
        for tid, iid in assignments.items():
            if iid not in interpretations:
                errors.append(f"contract candidate {cid} references unknown interpretation {iid}")
            elif interpretations[iid]["term_id"] != tid:
                errors.append(f"contract candidate {cid} assigns {iid} to wrong term {tid}")
            elif iid in interp_excluded:
                errors.append(f"contract candidate {cid} uses excluded interpretation {iid}")
        key = (pid, tuple(sorted((str(k), str(v)) for k, v in assignments.items())))
        if key in candidate_keys:
            errors.append(f"duplicate contract candidate assignments: {cid} and {candidate_keys[key]}")
        candidate_keys[key] = cid
        contract_digest = _checked_sha256_json(row["contract"], f"contract candidate {cid}.contract", errors)
        if contract_digest is not None and row["sha256"] != contract_digest:
            errors.append(f"contract candidate {cid}.sha256 mismatch")
        _validate_parameter_provenance(
            cid, row, assignments, sources, interpretations, assumptions, errors
        )

    if require_complete and active_parses and terms and not errors:
        # Membership and uniqueness were checked above. Count the Cartesian
        # family exactly instead of materializing exponentially many missing
        # combinations from a small, incomplete manifest.
        expected_count = 0
        for pid, parse in active_parses.items():
            material = [tid for tid in parse["term_ids"] if terms[tid]["material"] is True]
            # prod([]) is 1: zero material terms has one empty assignment.
            expected_count += math.prod(len(per_term[tid] - interp_excluded) for tid in material)
        expected_count -= len(excluded_combos)
        extra = set(candidate_keys) & excluded_combos
        missing = expected_count - len(set(candidate_keys) - excluded_combos)
        if missing:
            try:
                count = str(missing)
            except ValueError:
                errors.append("contract family omits admissible interpretation combinations (count exceeds the runtime's decimal conversion limit)")
            else:
                errors.append(f"contract family omits {count} admissible interpretation combination(s)")
        if extra:
            errors.append(f"contract family contains {len(extra)} non-admissible interpretation combination(s)")

    evaluations = manifest["evaluations"]
    if evaluations and status != "FROZEN":
        errors.append("evaluations are prohibited before freeze")
    eval_ids: list[str] = []
    frozen_at = _timestamp(freeze["frozen_at"])
    for row in evaluations:
        cid = row["contract_id"]
        if cid not in candidates:
            errors.append(f"evaluation references unknown contract {cid}")
            continue
        eval_ids.append(cid)
        if row["contract_sha256"] != candidates[cid]["sha256"]:
            errors.append(f"evaluation {cid} contract hash mismatch")
        if row["freeze_sha256"] != freeze.get("freeze_sha256"):
            errors.append(f"evaluation {cid} freeze hash mismatch")
        if row["outcome"] not in EVALUATION_OUTCOMES:
            errors.append(f"evaluation {cid} has invalid outcome")
        if row["outcome"] != "Unknown" and not row["evidence_refs"]:
            errors.append(f"evaluation {cid} requires evidence_refs for non-Unknown outcome")
        if row["outcome"] == "Unknown" and not (isinstance(row.get("notes"), str) and row["notes"].strip()):
            errors.append(f"evaluation {cid} with Unknown outcome requires notes")
        evaluated_at = _timestamp(row["evaluated_at"])
        if evaluated_at is None:
            errors.append(f"evaluation {cid} requires timezone-aware evaluated_at")
        elif frozen_at is not None and evaluated_at < frozen_at:
            errors.append(f"evaluation {cid} predates freeze")
    for cid in sorted(_duplicates(eval_ids)):
        errors.append(f"duplicate evaluation for contract {cid}")

    if status == "FROZEN":
        if frozen_at is None:
            errors.append("FROZEN manifest requires timezone-aware frozen_at")
        else:
            if cutoff is not None and frozen_at < cutoff:
                errors.append("freeze time predates evidence_cutoff")
            for sid, retrieved in source_times:
                if frozen_at < retrieved:
                    errors.append(f"freeze time predates source retrieval {sid}")
            for round_number, observed in saturation_times:
                if frozen_at < observed:
                    errors.append(f"freeze time predates saturation observation round {round_number}")
        digest = freeze["intake_sha256"]
        expected_intake = _checked_sha256_json(
            {"raw_input": manifest["raw_input"], "discovery": discovery},
            "frozen intake payload",
            errors,
        )
        if not isinstance(digest, str) or not _HEX64.fullmatch(digest):
            errors.append("FROZEN manifest requires intake_sha256")
        elif expected_intake is not None and digest != expected_intake:
            errors.append("freeze intake_sha256 mismatch")
        freeze_digest = freeze.get("freeze_sha256")
        expected_freeze = None
        if isinstance(digest, str) and _HEX64.fullmatch(digest) and isinstance(freeze.get("frozen_at"), str):
            expected_freeze = _checked_sha256_json(
                {"intake_sha256": digest, "frozen_at": freeze["frozen_at"]},
                "freeze identity payload",
                errors,
            )
        if not isinstance(freeze_digest, str) or not _HEX64.fullmatch(freeze_digest):
            errors.append("FROZEN manifest requires freeze_sha256")
        elif expected_freeze is not None and freeze_digest != expected_freeze:
            errors.append("freeze freeze_sha256 mismatch")
    return errors


def freeze_manifest(manifest: dict[str, Any], *, frozen_at: str | None = None) -> dict[str, Any]:
    errors = validate_manifest(manifest, require_complete=True)
    if errors:
        raise ValueError("cannot freeze invalid manifest: " + "; ".join(errors))
    if manifest["freeze"]["status"] == "FROZEN":
        raise ValueError("manifest is already frozen")
    if manifest["evaluations"]:
        raise ValueError("cannot freeze a manifest that already contains evaluations")
    result = copy.deepcopy(manifest)
    stamp = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z") if frozen_at is None else frozen_at
    parsed_stamp = _timestamp(stamp)
    if parsed_stamp is None:
        raise ValueError("frozen_at must be timezone-aware RFC3339/ISO-8601")
    cutoff = _timestamp(result["discovery"]["search_protocol"]["evidence_cutoff"])
    if cutoff is not None and parsed_stamp < cutoff:
        raise ValueError("frozen_at cannot predate evidence_cutoff")
    for source in result["discovery"]["sources"]:
        retrieved = _timestamp(source["retrieved_at"])
        if retrieved is not None and parsed_stamp < retrieved:
            raise ValueError(f"frozen_at cannot predate source retrieval {source['id']}")
    for observation in result["discovery"]["search_protocol"]["saturation_observations"]:
        observed = _timestamp(observation["observed_at"])
        if observed is not None and parsed_stamp < observed:
            raise ValueError(f"frozen_at cannot predate saturation observation round {observation['round']}")
    intake_digest = sha256_json({"raw_input": result["raw_input"], "discovery": result["discovery"]})
    freeze_digest = sha256_json({"intake_sha256": intake_digest, "frozen_at": stamp})
    result["freeze"] = {
        "status": "FROZEN",
        "frozen_at": stamp,
        "intake_sha256": intake_digest,
        "freeze_sha256": freeze_digest,
    }
    post_errors = validate_manifest(result)
    if post_errors:
        raise ValueError("frozen manifest failed validation: " + "; ".join(post_errors))
    return result


def aggregate_manifest(manifest: dict[str, Any]) -> dict[str, Any]:
    errors = validate_manifest(manifest)
    if errors:
        return {"outcome": "INVALID", "errors": errors, "contract_outcomes": {}}
    if manifest["freeze"]["status"] != "FROZEN":
        return {"outcome": "INCOMPLETE", "errors": ["manifest is not frozen"], "contract_outcomes": {}}
    candidates = {row["id"]: row for row in manifest["discovery"]["contract_candidates"]}
    evaluations = {row["contract_id"]: row["outcome"] for row in manifest["evaluations"]}
    if set(evaluations) != set(candidates):
        missing = sorted(set(candidates) - set(evaluations))
        extra = sorted(set(evaluations) - set(candidates))
        messages = (["missing evaluations: " + ", ".join(missing)] if missing else []) + (
            ["unexpected evaluations: " + ", ".join(extra)] if extra else []
        )
        return {"outcome": "INCOMPLETE", "errors": messages, "contract_outcomes": evaluations}
    unknown_assumptions = sorted(
        row["id"] for row in manifest["discovery"]["assumptions"] if row["status"] == "Unknown"
    )
    if unknown_assumptions:
        return {
            "outcome": "UNDERDETERMINED",
            "errors": [],
            "contract_outcomes": dict(sorted(evaluations.items())),
            "unresolved_assumptions": unknown_assumptions,
        }
    outcomes = set(evaluations.values())
    if outcomes == {"PROVED"}:
        aggregate = "INVARIANTLY_PROVED"
    elif outcomes == {"REFUTED"}:
        aggregate = "INVARIANTLY_REFUTED"
    elif "PROVED" in outcomes and "REFUTED" in outcomes:
        aggregate = "CONTRACT_SENSITIVE"
    else:
        aggregate = "UNDERDETERMINED"
    return {"outcome": aggregate, "errors": [], "contract_outcomes": dict(sorted(evaluations.items()))}


def _load(path: str) -> dict[str, Any]:
    data = _strict_json_loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("manifest root must be an object")
    return data


def _dump(value: Any) -> str:
    # Escape even malformed Unicode in diagnostics so reporting an invalid input
    # cannot itself fail when written to a UTF-8 terminal.
    return json.dumps(value, indent=2, sort_keys=True, ensure_ascii=True, allow_nan=False) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="far-intake", description="Project FAR governed pre-contract intake")
    sub = parser.add_subparsers(dest="command", required=True)
    init_p = sub.add_parser("init", help="create a draft intake manifest")
    init_p.add_argument("raw_text")
    init_p.add_argument("--id", default="FAR-INTAKE-DRAFT")
    init_p.add_argument("--write")
    validate_p = sub.add_parser("validate", help="validate an intake manifest")
    validate_p.add_argument("file")
    validate_p.add_argument("--ready", action="store_true", help="require freeze-readiness")
    freeze_p = sub.add_parser("freeze", help="freeze a complete intake manifest")
    freeze_p.add_argument("file")
    freeze_p.add_argument("--write")
    freeze_p.add_argument("--frozen-at")
    aggregate_p = sub.add_parser("aggregate", help="mechanically aggregate frozen contract outcomes")
    aggregate_p.add_argument("file")
    args = parser.parse_args(argv)
    try:
        if args.command == "init":
            result = new_manifest(args.raw_text, args.id)
            text = _dump(result)
            Path(args.write).write_text(text, encoding="utf-8") if args.write else print(text, end="")
            return 0
        if args.command == "validate":
            errors = validate_manifest(_load(args.file), require_complete=args.ready or None)
            print(_dump({"valid": not errors, "errors": errors}), end="")
            return 0 if not errors else 1
        if args.command == "freeze":
            text = _dump(freeze_manifest(_load(args.file), frozen_at=args.frozen_at))
            Path(args.write).write_text(text, encoding="utf-8") if args.write else print(text, end="")
            return 0
        if args.command == "aggregate":
            result = aggregate_manifest(_load(args.file))
            print(_dump(result), end="")
            return 0 if result["outcome"] not in {"INVALID", "INCOMPLETE"} else 1
    except (OSError, json.JSONDecodeError, TypeError, ValueError) as exc:
        print(_dump({"valid": False, "errors": [str(exc)]}), end="")
        return 1
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
