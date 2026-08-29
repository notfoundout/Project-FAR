#!/usr/bin/env python3
"""Fail-closed evidence-freeze, staged-access, and replay-capsule validation."""
from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import sys
from pathlib import Path, PurePosixPath
from typing import Iterable

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import jsonschema  # noqa: E402
SCHEMA = ROOT / "schemas/far-research-campaign-v1.schema.json"
DEFAULT_CAPSULE = ROOT / "research/campaigns/pca-w1-replay-capsule-v1.0.json"


class CampaignError(ValueError):
    """A capsule, stage, path, or hash violates the campaign contract."""


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def sha256_path(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def normalize_repo_path(raw: str) -> str:
    if not isinstance(raw, str) or not raw.strip():
        raise CampaignError("repository path must be a non-empty string")
    if "\\" in raw:
        raise CampaignError(f"backslash is not permitted in repository path: {raw!r}")
    path = PurePosixPath(raw)
    if path.is_absolute() or raw.startswith("/"):
        raise CampaignError(f"absolute repository path is prohibited: {raw!r}")
    if any(part in {"", ".", ".."} for part in path.parts):
        raise CampaignError(f"non-canonical repository path is prohibited: {raw!r}")
    normalized = path.as_posix()
    if normalized != raw:
        raise CampaignError(f"repository path must already be canonical: {raw!r}")
    return normalized


def load_capsule(path: Path = DEFAULT_CAPSULE) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    errors = list(jsonschema.Draft202012Validator(schema).iter_errors(data))
    if errors:
        raise errors[0]
    return data


def get_stage(capsule: dict, stage_id: str) -> dict:
    stages = [stage for stage in capsule["stages"] if stage["id"] == stage_id]
    if len(stages) != 1:
        raise CampaignError(f"stage {stage_id!r} must resolve exactly once")
    return stages[0]


def _matches(path: str, patterns: Iterable[str]) -> bool:
    return any(fnmatch.fnmatchcase(path, pattern) for pattern in patterns)


def validate_stage_paths(capsule: dict, stage_id: str, paths: Iterable[str]) -> tuple[str, ...]:
    stage = get_stage(capsule, stage_id)
    accepted: list[str] = []
    for raw in paths:
        path = normalize_repo_path(raw)
        if _matches(path, stage["deny"]):
            raise CampaignError(f"stage {stage_id}: denylisted path: {path}")
        if not _matches(path, stage["allow"]):
            raise CampaignError(f"stage {stage_id}: path is outside allowlist: {path}")
        accepted.append(path)
    if len(accepted) != len(set(accepted)):
        raise CampaignError(f"stage {stage_id}: duplicate requested path")
    return tuple(accepted)


def build_prompt_evidence(root: Path, capsule: dict, stage_id: str, paths: Iterable[str]) -> dict[str, str]:
    """Validate every path before reading any bytes, preventing pre-prompt leakage."""
    accepted = validate_stage_paths(capsule, stage_id, paths)
    resolved: list[tuple[str, Path]] = []
    root_resolved = root.resolve()
    for path in accepted:
        candidate = (root / path).resolve()
        if root_resolved not in candidate.parents:
            raise CampaignError(f"stage {stage_id}: resolved path escapes repository: {path}")
        if not candidate.is_file():
            raise CampaignError(f"stage {stage_id}: allowed path is not a file: {path}")
        resolved.append((path, candidate))
    return {path: candidate.read_text(encoding="utf-8") for path, candidate in resolved}


def validate_capsule(capsule: dict, root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    for field in ("stages", "evaluators", "artifacts"):
        ids = [item.get("id", item.get("path")) for item in capsule[field]]
        if len(ids) != len(set(ids)):
            errors.append(f"duplicate {field} identity")
    stage_ids = [stage["id"] for stage in capsule["stages"]]
    if stage_ids != list(dict.fromkeys(stage_ids)):
        errors.append("stage order/identity is not stable")
    for stage in capsule["stages"]:
        for pattern in stage["allow"] + stage["deny"]:
            try:
                normalize_repo_path(pattern.replace("**", "wildcard").replace("*", "wildcard"))
            except CampaignError as exc:
                errors.append(f"stage {stage['id']} invalid pattern {pattern!r}: {exc}")
        overlap = set(stage["allow"]) & set(stage["deny"])
        if overlap:
            errors.append(f"stage {stage['id']} exact allow/deny overlap: {sorted(overlap)}")
    protocol = capsule.get("protocol", {})
    try:
        protocol_path = normalize_repo_path(protocol["path"])
    except (CampaignError, KeyError, TypeError) as exc:
        errors.append(f"invalid protocol path: {exc}")
    else:
        candidate = root / protocol_path
        if not candidate.is_file():
            errors.append(f"missing protocol artifact: {protocol_path}")
        elif sha256_path(candidate) != protocol.get("sha256"):
            errors.append(f"protocol hash mismatch: {protocol_path}")
    for artifact in capsule["source_manifest"] + capsule["artifacts"]:
        try:
            path = normalize_repo_path(artifact["path"])
        except CampaignError as exc:
            errors.append(str(exc))
            continue
        if artifact["verify_current_path"]:
            candidate = root / path
            if not candidate.is_file():
                errors.append(f"missing artifact: {path}")
            elif sha256_path(candidate) != artifact["sha256"]:
                errors.append(f"artifact hash mismatch: {path}")
    if not capsule["limitations"]:
        errors.append("nondeterminism/reproducibility limitations must be explicit")
    return sorted(set(errors))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--capsule", type=Path, default=DEFAULT_CAPSULE)
    parser.add_argument("--stage")
    parser.add_argument("paths", nargs="*")
    args = parser.parse_args()
    try:
        capsule = load_capsule(args.capsule)
        errors = validate_capsule(capsule)
        if args.stage:
            validate_stage_paths(capsule, args.stage, args.paths)
    except (CampaignError, jsonschema.ValidationError, json.JSONDecodeError) as exc:
        print(f"FAIL: {exc}")
        return 1
    if errors:
        print("FAIL: " + "; ".join(errors))
        return 1
    print(f"research campaign capsule: PASS ({capsule['campaign_id']}; stages={len(capsule['stages'])})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
