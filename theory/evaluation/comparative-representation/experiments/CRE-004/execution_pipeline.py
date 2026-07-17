"""Deterministic validation, scoring, aggregation, and replay for CRE-004.

This module does not collect evaluator responses. It processes preserved JSON
responses under the frozen CRE-004 protocol and refuses execution when pinned
protocol artifacts have changed.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable, Mapping

ROOT = Path(__file__).resolve().parent
REQUIRED_RESPONSE_FIELDS = {
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
OPTIONAL_RESPONSE_FIELDS = {"other_function"}


def git_blob_sha1(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def verify_protocol_lock(root: Path = ROOT) -> dict[str, str]:
    lock = load_json(root / "protocol_lock.json")
    if lock.get("algorithm") != "git-blob-sha1":
        raise ValueError("unsupported protocol lock algorithm")
    checked: dict[str, str] = {}
    for relative, expected in sorted(lock["files"].items()):
        path = root / relative
        if not path.is_file():
            raise FileNotFoundError(f"locked protocol artifact missing: {relative}")
        actual = git_blob_sha1(path.read_bytes())
        if actual != expected:
            raise ValueError(
                f"protocol lock mismatch for {relative}: expected {expected}, got {actual}"
            )
        checked[relative] = actual
    return checked


def load_scorer(root: Path = ROOT):
    spec = importlib.util.spec_from_file_location("cre004_scoring", root / "scoring.py")
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load frozen scoring module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.score_response


def validate_response_shape(response: Mapping[str, Any]) -> None:
    keys = set(response)
    missing = REQUIRED_RESPONSE_FIELDS - keys
    extras = keys - REQUIRED_RESPONSE_FIELDS - OPTIONAL_RESPONSE_FIELDS
    if missing:
        raise ValueError(f"missing response fields: {sorted(missing)}")
    if extras:
        raise ValueError(f"unregistered response fields: {sorted(extras)}")
    if response["protocol_version"] != "CRE-004-v1.0":
        raise ValueError("response protocol_version is not CRE-004-v1.0")
    if response["evaluator_type"] not in {"human", "ai_agent"}:
        raise ValueError("evaluator_type must be human or ai_agent")
    for field in ("evaluator_id", "case_label", "candidate_label", "submitted_at"):
        if not isinstance(response[field], str) or not response[field].strip():
            raise ValueError(f"{field} must be a non-empty string")


def validate_manifest(manifest: Mapping[str, Any]) -> None:
    required = {
        "execution_id",
        "protocol_version",
        "randomization_seed",
        "expected_case_labels",
        "expected_candidate_labels",
        "eligible_evaluators",
    }
    missing = required - set(manifest)
    if missing:
        raise ValueError(f"missing manifest fields: {sorted(missing)}")
    if manifest["protocol_version"] != "CRE-004-v1.0":
        raise ValueError("manifest protocol_version is not CRE-004-v1.0")
    if not isinstance(manifest["randomization_seed"], int):
        raise ValueError("randomization_seed must be an integer")
    for field in ("expected_case_labels", "expected_candidate_labels"):
        values = manifest[field]
        if not isinstance(values, list) or not values or len(values) != len(set(values)):
            raise ValueError(f"{field} must be a non-empty unique list")
    evaluators = manifest["eligible_evaluators"]
    if not isinstance(evaluators, list) or not evaluators:
        raise ValueError("eligible_evaluators must be a non-empty list")
    ids = [item.get("evaluator_id") for item in evaluators]
    if any(not item for item in ids) or len(ids) != len(set(ids)):
        raise ValueError("eligible evaluator IDs must be non-empty and unique")
    for item in evaluators:
        if item.get("calibration_passed") is not True:
            raise ValueError(f"evaluator {item.get('evaluator_id')} has not passed calibration")


def read_responses(paths: Iterable[Path]) -> list[dict[str, Any]]:
    responses: list[dict[str, Any]] = []
    for path in sorted(paths, key=lambda value: value.as_posix()):
        payload = load_json(path)
        if not isinstance(payload, dict):
            raise ValueError(f"response file must contain one JSON object: {path}")
        payload = dict(payload)
        payload["_source_file"] = path.as_posix()
        responses.append(payload)
    return responses


def validate_and_score(
    manifest: Mapping[str, Any], responses: list[dict[str, Any]], root: Path = ROOT
) -> list[dict[str, Any]]:
    validate_manifest(manifest)
    verify_protocol_lock(root)
    scorer = load_scorer(root)
    eligible = {item["evaluator_id"] for item in manifest["eligible_evaluators"]}
    cases = set(manifest["expected_case_labels"])
    candidates = set(manifest["expected_candidate_labels"])
    seen: set[tuple[str, str, str]] = set()
    scored: list[dict[str, Any]] = []

    for raw in responses:
        source_file = raw.pop("_source_file", None)
        validate_response_shape(raw)
        if raw["evaluator_id"] not in eligible:
            raise ValueError(f"ineligible evaluator: {raw['evaluator_id']}")
        if raw["case_label"] not in cases:
            raise ValueError(f"unregistered case label: {raw['case_label']}")
        if raw["candidate_label"] not in candidates:
            raise ValueError(f"unregistered candidate label: {raw['candidate_label']}")
        key = (raw["evaluator_id"], raw["case_label"], raw["candidate_label"])
        if key in seen:
            raise ValueError(f"duplicate evaluator/case/candidate response: {key}")
        seen.add(key)
        score = scorer(raw)
        scored.append({**raw, **score, "source_file": source_file})

    return sorted(
        scored,
        key=lambda row: (row["candidate_label"], row["case_label"], row["evaluator_id"]),
    )


def aggregate(scored: list[Mapping[str, Any]]) -> dict[str, Any]:
    overall = Counter(row["classification"] for row in scored)
    hidden = sum(bool(row["hidden_reintroduction"]) for row in scored)
    by_candidate: dict[str, Counter[str]] = defaultdict(Counter)
    for row in scored:
        by_candidate[row["candidate_label"]][row["classification"]] += 1
    return {
        "response_count": len(scored),
        "classifications": dict(sorted(overall.items())),
        "hidden_reintroduction_count": hidden,
        "by_candidate": {
            candidate: dict(sorted(counts.items()))
            for candidate, counts in sorted(by_candidate.items())
        },
    }


def write_outputs(scored: list[dict[str, Any]], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    columns = [
        "evaluator_id",
        "evaluator_type",
        "case_label",
        "candidate_label",
        "classification",
        "hidden_reintroduction",
        "functional_carriers",
        "confidence",
        "submitted_at",
        "source_file",
    ]
    with (output_dir / "results.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        for row in scored:
            projected = {key: row[key] for key in columns}
            projected["functional_carriers"] = ";".join(row["functional_carriers"])
            writer.writerow(projected)
    with (output_dir / "summary.json").open("w", encoding="utf-8") as handle:
        json.dump(aggregate(scored), handle, indent=2, sort_keys=True)
        handle.write("\n")


def replay(manifest_path: Path, response_dir: Path, output_dir: Path) -> None:
    manifest = load_json(manifest_path)
    responses = read_responses(response_dir.glob("*.json"))
    scored = validate_and_score(manifest, responses)
    write_outputs(scored, output_dir)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("response_dir", type=Path)
    parser.add_argument("output_dir", type=Path)
    args = parser.parse_args()
    replay(args.manifest, args.response_dir, args.output_dir)


if __name__ == "__main__":
    main()
