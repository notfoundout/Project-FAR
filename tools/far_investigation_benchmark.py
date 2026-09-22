#!/usr/bin/env python3
"""Fail-closed validator/analyzer entry point for FAR Investigation Benchmark v0.1."""

from __future__ import annotations
import argparse, hashlib, json, pathlib, sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas/far-research-campaign-v1.schema.json"
ZERO64 = "0" * 64
ANALYZABLE = {"unblinded", "completed", "completed_imported_sealed"}
FROZEN_OR_LATER = {"frozen", *ANALYZABLE}
REQUIRED_FROZEN_NAMES = {
    "cases.jsonl",
    "case-selection-config.json",
    "case-selection-declarations.json",
    "condition-contracts-v0.1.md",
    "resource-budget-v0.1.json",
    "adjudication-rubric-v0.1.md",
    "reference-evidence-protocol-v0.1.md",
    "analysis-parameters-v0.1.json",
}

def load(path: pathlib.Path):
    return json.loads(path.read_text(encoding="utf-8"))

def sha256(path: pathlib.Path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def contains_unfrozen(value):
    if isinstance(value, str):
        return value == "UNASSIGNED" or "TO_BE_" in value or "PLACEHOLDER" in value
    if isinstance(value, dict):
        return any(contains_unfrozen(v) for v in value.values())
    if isinstance(value, list):
        return any(contains_unfrozen(v) for v in value)
    return False

def validate(manifest_path: pathlib.Path):
    m = load(manifest_path)
    errors = []
    required = {"schema_version","campaign_id","status","target","evaluators","environment","protocol","stages","source_manifest","artifacts","times","final_adjudication","replay","limitations"}
    if set(m) != required:
        errors.append(f"schema <root>: fields differ; missing={sorted(required-set(m))}, extra={sorted(set(m)-required)}")
    if m.get("schema_version") != "1.0":
        errors.append("schema schema_version: must be 1.0")
    if m.get("status") not in {"prepared","frozen","unblinded","completed","completed_imported_sealed","blocked"}:
        errors.append("schema status: invalid")
    target = m.get("target")
    if not isinstance(target, dict) or set(target) != {"repository","commit","tree","theory_or_question","hashes"}:
        errors.append("schema target: invalid fields")
    evaluators = m.get("evaluators")
    evaluator_fields = {"id","identity","provider","model","prior_exposure","conflicts","lane"}
    if not isinstance(evaluators, list) or not evaluators or any(not isinstance(e, dict) or set(e) != evaluator_fields for e in (evaluators if isinstance(evaluators, list) else [])):
        errors.append("schema evaluators: invalid")
    stages = m.get("stages")
    stage_fields = {"id","name","allow","deny","freeze_before_next","unblinding"}
    if not isinstance(stages, list) or not stages or any(not isinstance(x, dict) or set(x) != stage_fields or not isinstance(x.get("allow"), list) or not isinstance(x.get("deny"), list) or not isinstance(x.get("freeze_before_next"), bool) or not isinstance(x.get("unblinding"), bool) for x in (stages if isinstance(stages, list) else [])):
        errors.append("schema stages: invalid")
    if not isinstance(m.get("source_manifest"), list):
        errors.append("schema source_manifest: array required")
    artifacts_schema = m.get("artifacts")
    artifact_fields = {"path","sha256","role","verify_current_path"}
    if not isinstance(artifacts_schema, list) or not artifacts_schema or any(not isinstance(x, dict) or set(x) != artifact_fields for x in (artifacts_schema if isinstance(artifacts_schema, list) else [])):
        errors.append("schema artifacts: invalid")
    times = m.get("times")
    if not isinstance(times, dict) or set(times) != {"freeze_time","unblinding_time"}:
        errors.append("schema times: invalid")
    replay = m.get("replay")
    if not isinstance(replay, dict) or set(replay) != {"commands","deterministic_claim"} or not isinstance(replay.get("commands") if isinstance(replay, dict) else None, list):
        errors.append("schema replay: invalid")
    limitations = m.get("limitations")
    if not isinstance(limitations, list) or not limitations:
        errors.append("schema limitations: non-empty array required")
    protocol_schema = m.get("protocol")
    if not isinstance(protocol_schema, dict) or set(protocol_schema) != {"id","version","path","sha256"}:
        errors.append("schema protocol: invalid")

    status = m.get("status")
    artifacts = m.get("artifacts", [])
    protocol = m.get("protocol", {})

    for i, artifact in enumerate(artifacts):
        path = artifact.get("path")
        digest = artifact.get("sha256")
        if not path:
            continue
        fp = ROOT / path
        if artifact.get("verify_current_path") and not fp.exists():
            errors.append(f"artifact {i} path missing: {path}")
        if status in FROZEN_OR_LATER and artifact.get("verify_current_path") and fp.exists() and digest != sha256(fp):
            errors.append(f"artifact {i} hash mismatch: {path}")

    if status in FROZEN_OR_LATER:
        if contains_unfrozen(m):
            errors.append("frozen-or-later manifest contains an unset placeholder")
        if not m.get("times", {}).get("freeze_time"):
            errors.append("frozen-or-later manifest requires freeze_time")
        if status == "frozen" and m.get("times", {}).get("unblinding_time") is not None:
            errors.append("frozen manifest must not have unblinding_time")
        if not m.get("source_manifest"):
            errors.append("frozen-or-later manifest requires a non-empty source_manifest")
        if len(m.get("evaluators", [])) < 3:
            errors.append("frozen-or-later manifest requires two primary raters plus a third adjudicator")
        if protocol.get("sha256") in {"", ZERO64}:
            errors.append("frozen-or-later manifest requires a real protocol hash")
        ppath = protocol.get("path")
        if ppath and (ROOT / ppath).exists() and protocol.get("sha256") != sha256(ROOT / ppath):
            errors.append("protocol hash mismatch")
        names = {pathlib.PurePosixPath(a.get("path", "")).name for a in artifacts}
        missing = sorted(REQUIRED_FROZEN_NAMES - names)
        if missing:
            errors.append(f"frozen-or-later manifest missing required freeze artifacts: {missing}")
        for i, artifact in enumerate(artifacts):
            if artifact.get("sha256") == ZERO64:
                errors.append(f"frozen-or-later artifact {i} retains zero hash sentinel")

    if errors:
        for error in errors:
            print("ERROR:", error, file=sys.stderr)
        return 1
    print(f"VALID {m.get('campaign_id', '<unknown>')} status={status}")
    return 0

def analyze(manifest_path: pathlib.Path):
    m = load(manifest_path)
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
