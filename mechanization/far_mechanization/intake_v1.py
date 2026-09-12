"""Governed pre-contract intake for Project FAR."""
from __future__ import annotations

import argparse
import copy
import hashlib
import itertools
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

FORMAT_VERSION = "far-intake/1.0"
SOURCE_TYPES = {"PRIMARY", "SCHOLARLY", "REFERENCE", "USER_SUPPLIED", "OTHER"}
ORIGINS = {"SOURCE_EXPLICIT", "SOURCE_SYNTHESIS", "INFERENCE"}
EXCLUSION_REASONS = {"DUPLICATE", "WRONG_DOMAIN", "ANACHRONISTIC", "UNSUPPORTED", "INCOMPATIBLE_WITH_SCOPE", "OTHER"}
EVALUATION_OUTCOMES = {"PROVED", "REFUTED", "UNDERDETERMINED", "OPEN", "BLOCKED", "NOT_APPLICABLE", "Unknown"}
_HEX64 = re.compile(r"^[0-9a-f]{64}$")
_ID = re.compile(r"^[A-Za-z][A-Za-z0-9_.:-]*$")


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def sha256_json(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode()).hexdigest()


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode()).hexdigest()


def _timestamp(value: Any) -> datetime | None:
    if not isinstance(value, str) or not value:
        return None
    try:
        result = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
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
            "claim_parses": [], "terms": [], "sources": [], "interpretations": [],
            "interpretation_exclusions": [], "compatibility_exclusions": [], "assumptions": [],
            "search_protocol": {"evidence_cutoff": None, "queries": [], "stopping_rule": None, "saturation_observations": [], "limitations": []},
            "contract_candidates": [],
        },
        "freeze": {"status": "DRAFT", "frozen_at": None, "intake_sha256": None},
        "evaluations": [],
    }


def validate_manifest(manifest: Any, *, require_complete: bool | None = None) -> list[str]:
    errors: list[str] = []
    if not isinstance(manifest, dict):
        return ["manifest must be an object"]
    if manifest.get("format_version") != FORMAT_VERSION:
        errors.append(f"format_version must be {FORMAT_VERSION}")
    if not isinstance(manifest.get("id"), str) or not _ID.fullmatch(manifest["id"]):
        errors.append("id is invalid")

    raw = manifest.get("raw_input")
    if not isinstance(raw, dict):
        errors.append("raw_input must be an object")
    elif not isinstance(raw.get("text"), str) or not raw["text"]:
        errors.append("raw_input.text must be non-empty")
    elif raw.get("sha256") != sha256_text(raw["text"]):
        errors.append("raw_input.sha256 mismatch")

    discovery = manifest.get("discovery")
    if not isinstance(discovery, dict):
        return errors + ["discovery must be an object"]
    freeze = manifest.get("freeze")
    if not isinstance(freeze, dict):
        errors.append("freeze must be an object")
        freeze = {}
    status = freeze.get("status")
    if status not in {"DRAFT", "FROZEN"}:
        errors.append("freeze.status must be DRAFT or FROZEN")
    if require_complete is None:
        require_complete = status == "FROZEN"

    parses = _index(discovery.get("claim_parses", []), "claim_parses", errors)
    terms = _index(discovery.get("terms", []), "terms", errors)
    sources = _index(discovery.get("sources", []), "sources", errors)
    interpretations = _index(discovery.get("interpretations", []), "interpretations", errors)
    candidates = _index(discovery.get("contract_candidates", []), "contract_candidates", errors)

    for sid, source in sources.items():
        if source.get("source_type") not in SOURCE_TYPES:
            errors.append(f"source {sid} has invalid source_type")
        if not isinstance(source.get("locator"), str) or not source["locator"]:
            errors.append(f"source {sid} requires locator")
        if not isinstance(source.get("sha256"), str) or not _HEX64.fullmatch(source["sha256"]):
            errors.append(f"source {sid} requires lowercase SHA-256")
        if _timestamp(source.get("retrieved_at")) is None:
            errors.append(f"source {sid} requires timezone-aware retrieved_at")
        if not isinstance(source.get("scope"), str) or not source["scope"]:
            errors.append(f"source {sid} requires scope")

    per_term: dict[str, set[str]] = {term_id: set() for term_id in terms}
    for iid, row in interpretations.items():
        term_id = row.get("term_id")
        if term_id not in terms:
            errors.append(f"interpretation {iid} references unknown term {term_id}")
            continue
        per_term[term_id].add(iid)
        if not isinstance(row.get("statement"), str) or not row["statement"]:
            errors.append(f"interpretation {iid} requires statement")
        origin = row.get("origin")
        if origin not in ORIGINS:
            errors.append(f"interpretation {iid} has invalid origin")
        source_ids = row.get("source_ids")
        if not isinstance(source_ids, list) or any(s not in sources for s in source_ids):
            errors.append(f"interpretation {iid} has invalid source_ids")
            source_ids = []
        if origin in {"SOURCE_EXPLICIT", "SOURCE_SYNTHESIS"} and not source_ids:
            errors.append(f"interpretation {iid} requires source provenance")
        if origin in {"SOURCE_SYNTHESIS", "INFERENCE"} and (not isinstance(row.get("derivation"), str) or not row["derivation"]):
            errors.append(f"interpretation {iid} requires explicit derivation")
        if not isinstance(row.get("scope"), str) or not row["scope"]:
            errors.append(f"interpretation {iid} requires scope")

    excluded: set[str] = set()
    exclusions = discovery.get("interpretation_exclusions", [])
    if not isinstance(exclusions, list):
        errors.append("interpretation_exclusions must be an array")
        exclusions = []
    for i, row in enumerate(exclusions):
        if not isinstance(row, dict):
            errors.append(f"interpretation_exclusions[{i}] must be an object")
            continue
        iid = row.get("interpretation_id")
        if iid not in interpretations:
            errors.append(f"interpretation exclusion references unknown interpretation {iid}")
        elif iid in excluded:
            errors.append(f"duplicate interpretation exclusion: {iid}")
        else:
            excluded.add(iid)
        if row.get("reason_code") not in EXCLUSION_REASONS:
            errors.append(f"interpretation exclusion {iid} has invalid reason_code")
        if not isinstance(row.get("reason"), str) or not row["reason"]:
            errors.append(f"interpretation exclusion {iid} requires reason")
        if not isinstance(row.get("source_ids", []), list) or any(s not in sources for s in row.get("source_ids", [])):
            errors.append(f"interpretation exclusion {iid} has invalid source_ids")

    for term_id, term in terms.items():
        declared = term.get("interpretation_ids")
        if not isinstance(declared, list) or set(declared) != per_term[term_id]:
            errors.append(f"term {term_id}.interpretation_ids must exactly enumerate its interpretations")
        if not isinstance(term.get("surface"), str) or not term["surface"]:
            errors.append(f"term {term_id} requires surface")
        if not isinstance(term.get("material"), bool):
            errors.append(f"term {term_id}.material must be boolean")

    for pid, parse in parses.items():
        term_ids = parse.get("term_ids")
        if not isinstance(term_ids, list) or not term_ids:
            errors.append(f"claim parse {pid} requires non-empty term_ids")
            continue
        if len(set(term_ids)) != len(term_ids):
            errors.append(f"claim parse {pid} repeats term ids")
        unknown = sorted({t for t in term_ids if t not in terms})
        if unknown:
            errors.append(f"claim parse {pid} references unknown terms: {', '.join(unknown)}")
        if not isinstance(parse.get("statement"), str) or not parse["statement"]:
            errors.append(f"claim parse {pid} requires statement")
        if parse.get("origin") not in {"SURFACE", "INFERENCE"}:
            errors.append(f"claim parse {pid} has invalid origin")
        if parse.get("origin") == "INFERENCE" and (not isinstance(parse.get("derivation"), str) or not parse["derivation"]):
            errors.append(f"claim parse {pid} requires derivation")

    assumptions = _index(discovery.get("assumptions", []), "assumptions", errors)
    for aid, row in assumptions.items():
        if row.get("status") not in {"EXPLICIT", "Unknown"}:
            errors.append(f"assumption {aid} has invalid status")
        if not isinstance(row.get("statement"), str) or not row["statement"]:
            errors.append(f"assumption {aid} requires statement")
        if not isinstance(row.get("effect_if_false"), str) or not row["effect_if_false"]:
            errors.append(f"assumption {aid} requires effect_if_false")
        if not isinstance(row.get("source_ids", []), list) or any(s not in sources for s in row.get("source_ids", [])):
            errors.append(f"assumption {aid} has invalid source_ids")

    protocol = discovery.get("search_protocol")
    if not isinstance(protocol, dict):
        errors.append("search_protocol must be an object")
        protocol = {}
    queries = protocol.get("queries", [])
    if not isinstance(queries, list):
        errors.append("search_protocol.queries must be an array")
        queries = []
    qids: list[str] = []
    for i, query in enumerate(queries):
        if not isinstance(query, dict):
            errors.append(f"search_protocol.queries[{i}] must be an object")
            continue
        qid = query.get("id")
        if not isinstance(qid, str) or not _ID.fullmatch(qid):
            errors.append(f"search_protocol.queries[{i}].id is invalid")
        else:
            qids.append(qid)
        for field in ("query", "target", "source_scope"):
            if not isinstance(query.get(field), str) or not query[field]:
                errors.append(f"search query {qid or i} requires {field}")
    for qid in sorted(_duplicates(qids)):
        errors.append(f"duplicate search query id: {qid}")

    if require_complete:
        if not parses:
            errors.append("freeze requires at least one claim parse")
        if not terms:
            errors.append("freeze requires at least one term")
        material_terms = [tid for tid, row in terms.items() if row.get("material") is True]
        if not material_terms:
            errors.append("freeze requires at least one material term")
        referenced = {tid for parse in parses.values() for tid in (parse.get("term_ids") or []) if isinstance(tid, str)}
        for tid in material_terms:
            if tid not in referenced:
                errors.append(f"material term {tid} is not referenced by any claim parse")
            if not (per_term[tid] - excluded):
                errors.append(f"material term {tid} has no active interpretation")
        if not sources:
            errors.append("freeze requires at least one source")
        cutoff = _timestamp(protocol.get("evidence_cutoff"))
        if cutoff is None:
            errors.append("freeze requires timezone-aware search_protocol.evidence_cutoff")
        if not queries:
            errors.append("freeze requires a recorded search protocol query")
        if not isinstance(protocol.get("stopping_rule"), str) or not protocol["stopping_rule"]:
            errors.append("freeze requires search_protocol.stopping_rule")
        saturation = protocol.get("saturation_observations")
        if not isinstance(saturation, list) or not saturation:
            errors.append("freeze requires saturation_observations")
        else:
            for i, row in enumerate(saturation):
                if not isinstance(row, dict):
                    errors.append(f"saturation_observations[{i}] must be an object")
                    continue
                if not isinstance(row.get("round"), int) or row["round"] < 1:
                    errors.append(f"saturation_observations[{i}].round must be a positive integer")
                ids = row.get("new_material_interpretation_ids")
                if not isinstance(ids, list) or any(iid not in interpretations for iid in ids):
                    errors.append(f"saturation_observations[{i}] has invalid new_material_interpretation_ids")
        limitations = protocol.get("limitations")
        if not isinstance(limitations, list) or any(not isinstance(x, str) or not x for x in limitations):
            errors.append("search_protocol.limitations must be an array of non-empty strings")
        if cutoff is not None:
            for sid, source in sources.items():
                retrieved = _timestamp(source.get("retrieved_at"))
                if retrieved is not None and retrieved > cutoff:
                    errors.append(f"source {sid} was retrieved after evidence_cutoff")

    compat = discovery.get("compatibility_exclusions", [])
    if not isinstance(compat, list):
        errors.append("compatibility_exclusions must be an array")
        compat = []
    excluded_combos: set[tuple[str, tuple[tuple[str, str], ...]]] = set()
    for i, row in enumerate(compat):
        if not isinstance(row, dict):
            errors.append(f"compatibility_exclusions[{i}] must be an object")
            continue
        pid, assignments = row.get("claim_parse_id"), row.get("assignments")
        if pid not in parses:
            errors.append(f"compatibility exclusion references unknown parse {pid}")
            continue
        if not isinstance(assignments, dict):
            errors.append(f"compatibility exclusion {i} requires assignments")
            continue
        required = {tid for tid in parses[pid].get("term_ids", []) if tid in terms and terms[tid].get("material") is True}
        if set(assignments) != required:
            errors.append(f"compatibility exclusion {i} assignments must exactly cover material terms for {pid}")
        for tid, iid in assignments.items():
            if iid not in interpretations:
                errors.append(f"compatibility exclusion {i} references unknown interpretation {iid}")
            elif interpretations[iid].get("term_id") != tid:
                errors.append(f"compatibility exclusion {i} assigns {iid} to wrong term {tid}")
            elif iid in excluded:
                errors.append(f"compatibility exclusion {i} redundantly uses excluded interpretation {iid}")
        key = (pid, tuple(sorted((str(k), str(v)) for k, v in assignments.items())))
        if key in excluded_combos:
            errors.append(f"duplicate compatibility exclusion for {pid}: {dict(assignments)}")
        excluded_combos.add(key)
        if not isinstance(row.get("reason"), str) or not row["reason"]:
            errors.append(f"compatibility exclusion {i} requires reason")
        if not isinstance(row.get("source_ids", []), list) or any(s not in sources for s in row.get("source_ids", [])):
            errors.append(f"compatibility exclusion {i} has invalid source_ids")

    candidate_keys: dict[tuple[str, tuple[tuple[str, str], ...]], str] = {}
    for cid, row in candidates.items():
        pid, assignments = row.get("claim_parse_id"), row.get("assignments")
        if pid not in parses:
            errors.append(f"contract candidate {cid} references unknown parse {pid}")
            continue
        if not isinstance(assignments, dict):
            errors.append(f"contract candidate {cid} requires assignments")
            continue
        required = {tid for tid in parses[pid].get("term_ids", []) if tid in terms and terms[tid].get("material") is True}
        if set(assignments) != required:
            errors.append(f"contract candidate {cid} assignments must exactly cover material terms for {pid}")
        for tid, iid in assignments.items():
            if iid not in interpretations:
                errors.append(f"contract candidate {cid} references unknown interpretation {iid}")
            elif interpretations[iid].get("term_id") != tid:
                errors.append(f"contract candidate {cid} assigns {iid} to wrong term {tid}")
            elif iid in excluded:
                errors.append(f"contract candidate {cid} uses excluded interpretation {iid}")
        key = (pid, tuple(sorted((str(k), str(v)) for k, v in assignments.items())))
        if key in candidate_keys:
            errors.append(f"duplicate contract candidate assignments: {cid} and {candidate_keys[key]}")
        candidate_keys[key] = cid
        contract = row.get("contract")
        if not isinstance(contract, dict):
            errors.append(f"contract candidate {cid}.contract must be an object")
        elif row.get("sha256") != sha256_json(contract):
            errors.append(f"contract candidate {cid}.sha256 mismatch")

    if require_complete and parses and terms:
        expected: set[tuple[str, tuple[tuple[str, str], ...]]] = set()
        for pid, parse in parses.items():
            material = [tid for tid in parse.get("term_ids", []) if tid in terms and terms[tid].get("material") is True]
            options = [sorted(per_term[tid] - excluded) for tid in material]
            if material and all(options):
                for values in itertools.product(*options):
                    key = (pid, tuple(sorted(zip(material, values))))
                    if key not in excluded_combos:
                        expected.add(key)
        missing, extra = expected - set(candidate_keys), set(candidate_keys) - expected
        if missing:
            errors.append(f"contract family omits {len(missing)} admissible interpretation combination(s)")
        if extra:
            errors.append(f"contract family contains {len(extra)} non-admissible interpretation combination(s)")

    evaluations = manifest.get("evaluations")
    if not isinstance(evaluations, list):
        errors.append("evaluations must be an array")
        evaluations = []
    if evaluations and status != "FROZEN":
        errors.append("evaluations are prohibited before freeze")
    eval_ids: list[str] = []
    frozen_at = _timestamp(freeze.get("frozen_at"))
    for i, row in enumerate(evaluations):
        if not isinstance(row, dict):
            errors.append(f"evaluations[{i}] must be an object")
            continue
        cid = row.get("contract_id")
        if cid not in candidates:
            errors.append(f"evaluation references unknown contract {cid}")
            continue
        eval_ids.append(cid)
        if row.get("contract_sha256") != candidates[cid].get("sha256"):
            errors.append(f"evaluation {cid} contract hash mismatch")
        if row.get("outcome") not in EVALUATION_OUTCOMES:
            errors.append(f"evaluation {cid} has invalid outcome")
        evaluated_at = _timestamp(row.get("evaluated_at"))
        if evaluated_at is None:
            errors.append(f"evaluation {cid} requires timezone-aware evaluated_at")
        elif frozen_at is not None and evaluated_at < frozen_at:
            errors.append(f"evaluation {cid} predates freeze")
        if not isinstance(row.get("evidence_refs"), list):
            errors.append(f"evaluation {cid}.evidence_refs must be an array")
    for cid in sorted(_duplicates(eval_ids)):
        errors.append(f"duplicate evaluation for contract {cid}")

    if status == "FROZEN":
        if frozen_at is None:
            errors.append("FROZEN manifest requires timezone-aware frozen_at")
        digest = freeze.get("intake_sha256")
        if not isinstance(digest, str) or not _HEX64.fullmatch(digest):
            errors.append("FROZEN manifest requires intake_sha256")
        elif digest != sha256_json({"raw_input": manifest.get("raw_input"), "discovery": discovery}):
            errors.append("freeze intake_sha256 mismatch")
    return errors


def freeze_manifest(manifest: dict[str, Any], *, frozen_at: str | None = None) -> dict[str, Any]:
    if manifest.get("freeze", {}).get("status") == "FROZEN":
        raise ValueError("manifest is already frozen")
    if manifest.get("evaluations"):
        raise ValueError("cannot freeze a manifest that already contains evaluations")
    errors = validate_manifest(manifest, require_complete=True)
    if errors:
        raise ValueError("cannot freeze invalid manifest: " + "; ".join(errors))
    result = copy.deepcopy(manifest)
    stamp = frozen_at or datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    if _timestamp(stamp) is None:
        raise ValueError("frozen_at must be timezone-aware RFC3339/ISO-8601")
    result["freeze"] = {
        "status": "FROZEN",
        "frozen_at": stamp,
        "intake_sha256": sha256_json({"raw_input": result["raw_input"], "discovery": result["discovery"]}),
    }
    return result


def aggregate_manifest(manifest: dict[str, Any]) -> dict[str, Any]:
    errors = validate_manifest(manifest)
    if errors:
        return {"outcome": "INVALID", "errors": errors, "contract_outcomes": {}}
    if manifest.get("freeze", {}).get("status") != "FROZEN":
        return {"outcome": "INCOMPLETE", "errors": ["manifest is not frozen"], "contract_outcomes": {}}
    candidates = {row["id"]: row for row in manifest["discovery"].get("contract_candidates", [])}
    evaluations = {row["contract_id"]: row["outcome"] for row in manifest.get("evaluations", [])}
    if set(evaluations) != set(candidates):
        missing = sorted(set(candidates) - set(evaluations))
        extra = sorted(set(evaluations) - set(candidates))
        messages = (["missing evaluations: " + ", ".join(missing)] if missing else []) + (["unexpected evaluations: " + ", ".join(extra)] if extra else [])
        return {"outcome": "INCOMPLETE", "errors": messages, "contract_outcomes": evaluations}
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
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError("manifest root must be an object")
    return data


def _dump(value: Any) -> str:
    return json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="far-intake", description="Project FAR governed pre-contract intake")
    sub = parser.add_subparsers(dest="command", required=True)
    init_p = sub.add_parser("init", help="create a draft intake manifest")
    init_p.add_argument("raw_text"); init_p.add_argument("--id", default="FAR-INTAKE-DRAFT"); init_p.add_argument("--write")
    validate_p = sub.add_parser("validate", help="validate an intake manifest")
    validate_p.add_argument("file"); validate_p.add_argument("--ready", action="store_true", help="require freeze-readiness")
    freeze_p = sub.add_parser("freeze", help="freeze a complete intake manifest")
    freeze_p.add_argument("file"); freeze_p.add_argument("--write"); freeze_p.add_argument("--frozen-at")
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
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(_dump({"valid": False, "errors": [str(exc)]}), end="")
        return 1
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
