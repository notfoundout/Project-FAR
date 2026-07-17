"""Append-only execution and deterministic replay tooling for CRE-004.

This module does not generate evaluator answers. It validates submitted answers,
records them without mutation, scores them using the frozen scorer, and rebuilds
reports deterministically from the preserved ledger.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import pathlib
from collections import Counter, defaultdict
from datetime import datetime, timezone
from typing import Any, Iterable


BASE = pathlib.Path(__file__).resolve().parent
LEDGER_NAME = "responses.jsonl"
REPORT_NAME = "results.generated.json"
PROTOCOL_VERSION = "CRE-004-v1.0"
NORMATIVE_FILES = (
    "preregistration.json",
    "response.schema.json",
    "scoring.py",
    "decision_tree.md",
    "automatic_scoring.md",
    "hidden_reintroduction.md",
    "evaluator_packet.md",
    "calibration_cases.json",
)


def _load_scorer():
    spec = importlib.util.spec_from_file_location("cre004_scoring", BASE / "scoring.py")
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load CRE-004 scorer")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.score_response


score_response = _load_scorer()


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def protocol_manifest() -> dict[str, Any]:
    files = {}
    for name in NORMATIVE_FILES:
        path = BASE / name
        if not path.is_file():
            raise FileNotFoundError(path)
        files[name] = sha256_bytes(path.read_bytes())
    return {"protocol_version": PROTOCOL_VERSION, "files": files}


def validate_response(response: dict[str, Any]) -> None:
    required = {
        "protocol_version",
        "evaluator_id",
        "evaluator_type",
        "case_label",
        "candidate_label",
        "source_difference",
        "translated_difference",
        "difference_carriers",
        "confidence",
        "submitted_at",
    }
    missing = sorted(required - response.keys())
    if missing:
        raise ValueError(f"missing required fields: {missing}")
    allowed = required | {"other_function", "supersedes_record_id"}
    extra = sorted(response.keys() - allowed)
    if extra:
        raise ValueError(f"unregistered fields: {extra}")
    if response["protocol_version"] != PROTOCOL_VERSION:
        raise ValueError("protocol_version does not match frozen execution version")
    if response["evaluator_type"] not in {"human", "ai_agent"}:
        raise ValueError("invalid evaluator_type")
    for key in ("evaluator_id", "case_label", "candidate_label"):
        if not isinstance(response[key], str) or not response[key]:
            raise ValueError(f"{key} must be a non-empty string")
    try:
        datetime.fromisoformat(response["submitted_at"].replace("Z", "+00:00"))
    except (AttributeError, ValueError) as exc:
        raise ValueError("submitted_at must be an ISO-8601 date-time") from exc
    score_response(response)


def record_id_for(response: dict[str, Any], manifest: dict[str, Any]) -> str:
    material = {"response": response, "protocol_manifest": manifest}
    return sha256_bytes(canonical_json(material).encode("utf-8"))


def read_ledger(path: pathlib.Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    records = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            records.append(json.loads(line))
        except json.JSONDecodeError as exc:
            raise ValueError(f"invalid JSON on ledger line {line_number}") from exc
    return records


def append_response(response_path: pathlib.Path, ledger_path: pathlib.Path) -> dict[str, Any]:
    response = json.loads(response_path.read_text(encoding="utf-8"))
    validate_response(response)
    manifest = protocol_manifest()
    record_id = record_id_for(response, manifest)
    existing = read_ledger(ledger_path)
    if any(record.get("record_id") == record_id for record in existing):
        raise ValueError("identical response is already recorded")
    supersedes = response.get("supersedes_record_id")
    if supersedes and not any(record.get("record_id") == supersedes for record in existing):
        raise ValueError("supersedes_record_id does not exist in the ledger")
    record = {
        "record_id": record_id,
        "recorded_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        "protocol_manifest": manifest,
        "response": response,
        "score": score_response(response),
    }
    ledger_path.parent.mkdir(parents=True, exist_ok=True)
    with ledger_path.open("a", encoding="utf-8") as handle:
        handle.write(canonical_json(record) + "\n")
    return record


def verify_records(records: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    verified = []
    current_manifest = protocol_manifest()
    seen: set[str] = set()
    for index, record in enumerate(records, 1):
        response = record.get("response")
        if not isinstance(response, dict):
            raise ValueError(f"record {index} has no response object")
        validate_response(response)
        expected_id = record_id_for(response, record.get("protocol_manifest"))
        if record.get("record_id") != expected_id:
            raise ValueError(f"record {index} has an invalid record_id")
        if record["record_id"] in seen:
            raise ValueError(f"record {index} duplicates a prior record_id")
        seen.add(record["record_id"])
        if record.get("protocol_manifest") != current_manifest:
            raise ValueError(f"record {index} was produced under a different protocol manifest")
        expected_score = score_response(response)
        if record.get("score") != expected_score:
            raise ValueError(f"record {index} score does not replay deterministically")
        supersedes = response.get("supersedes_record_id")
        if supersedes and supersedes not in seen:
            raise ValueError(f"record {index} supersedes an unknown or later record")
        verified.append(record)
    return verified


def active_records(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    superseded = {
        record["response"].get("supersedes_record_id")
        for record in records
        if record["response"].get("supersedes_record_id")
    }
    return [record for record in records if record["record_id"] not in superseded]


def aggregate(records: list[dict[str, Any]]) -> dict[str, Any]:
    verified = verify_records(records)
    active = active_records(verified)
    by_candidate: dict[str, Counter[str]] = defaultdict(Counter)
    by_case: dict[str, Counter[str]] = defaultdict(Counter)
    by_evaluator: dict[str, Counter[str]] = defaultdict(Counter)
    hidden = Counter()
    overall = Counter()
    for record in active:
        response = record["response"]
        score = record["score"]
        classification = score["classification"]
        overall[classification] += 1
        by_candidate[response["candidate_label"]][classification] += 1
        by_case[response["case_label"]][classification] += 1
        by_evaluator[response["evaluator_id"]][classification] += 1
        hidden[str(score["hidden_reintroduction"]).lower()] += 1
    return {
        "protocol_manifest": protocol_manifest(),
        "record_count": len(verified),
        "active_record_count": len(active),
        "superseded_record_count": len(verified) - len(active),
        "overall": dict(sorted(overall.items())),
        "hidden_reintroduction": dict(sorted(hidden.items())),
        "by_candidate": {key: dict(sorted(value.items())) for key, value in sorted(by_candidate.items())},
        "by_case": {key: dict(sorted(value.items())) for key, value in sorted(by_case.items())},
        "by_evaluator": {key: dict(sorted(value.items())) for key, value in sorted(by_evaluator.items())},
    }


def write_report(ledger_path: pathlib.Path, report_path: pathlib.Path) -> dict[str, Any]:
    report = aggregate(read_ledger(ledger_path))
    report_path.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    manifest_parser = subparsers.add_parser("manifest")
    manifest_parser.add_argument("--output", type=pathlib.Path)

    validate_parser = subparsers.add_parser("validate")
    validate_parser.add_argument("response", type=pathlib.Path)

    append_parser = subparsers.add_parser("append")
    append_parser.add_argument("response", type=pathlib.Path)
    append_parser.add_argument("--ledger", type=pathlib.Path, default=BASE / LEDGER_NAME)

    replay_parser = subparsers.add_parser("replay")
    replay_parser.add_argument("--ledger", type=pathlib.Path, default=BASE / LEDGER_NAME)
    replay_parser.add_argument("--report", type=pathlib.Path, default=BASE / REPORT_NAME)

    args = parser.parse_args()
    if args.command == "manifest":
        text = json.dumps(protocol_manifest(), indent=2, sort_keys=True) + "\n"
        if args.output:
            args.output.write_text(text, encoding="utf-8")
        else:
            print(text, end="")
    elif args.command == "validate":
        validate_response(json.loads(args.response.read_text(encoding="utf-8")))
    elif args.command == "append":
        print(json.dumps(append_response(args.response, args.ledger), indent=2, sort_keys=True))
    elif args.command == "replay":
        print(json.dumps(write_report(args.ledger, args.report), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
