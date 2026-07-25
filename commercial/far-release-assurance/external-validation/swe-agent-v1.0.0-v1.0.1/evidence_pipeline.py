from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

CASE_DIR = Path(__file__).parent
OUTPUT_DIR = CASE_DIR / "execution-output"
STATE_PATH = OUTPUT_DIR / "execution-state.json"
TRAJECTORY_DIR = OUTPUT_DIR / "trajectories"
PRIMARY_DIR = OUTPUT_DIR / "primary"
PACKAGES_DIR = PRIMARY_DIR / "packages"
COMPARISON_PATH = PRIMARY_DIR / "blinded-comparison.json"
FREEZE_PATH = OUTPUT_DIR / "primary-freeze.json"
REVEAL_DIR = OUTPUT_DIR / "post-freeze-reveal"

PACKAGE_SCHEMA = "far-swe-agent-evidence-package/1.0"
COMPARISON_SCHEMA = "far-swe-agent-blinded-comparison/1.0"
FREEZE_SCHEMA = "far-swe-agent-primary-freeze/1.0"
REVEAL_SCHEMA = "far-swe-agent-post-freeze-reveal/1.0"

FORBIDDEN_OUTCOME_KEYS = {
    "fail_to_pass", "pass_to_pass", "patch", "test_patch", "resolved",
    "resolution_status", "grader", "grader_output", "evaluation", "score",
    "reward", "tests_passed", "tests_failed", "swebench_result",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def canonical_json(value: object) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def read_json(path: Path) -> Any:
    if not path.is_file():
        raise SystemExit(f"Missing required file: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(canonical_json(value))


def scan_forbidden(value: Any, path: str = "root") -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            normalized = str(key).strip().lower()
            if normalized in FORBIDDEN_OUTCOME_KEYS:
                raise SystemExit(f"Outcome-bearing field forbidden before freeze: {path}.{key}")
            scan_forbidden(child, f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            scan_forbidden(child, f"{path}[{index}]")


def load_completed_state() -> dict[str, Any]:
    state = read_json(STATE_PATH)
    if state.get("schema") != "far-swe-agent-execution-state/1.1":
        raise SystemExit("Execution-state schema mismatch")
    runs = state.get("runs")
    if not isinstance(runs, list) or len(runs) != 4:
        raise SystemExit("Exactly four execution runs are required")
    for run in runs:
        if run.get("state") != "complete":
            raise SystemExit(f"Run is not complete: {run.get('run_id')}")
        trajectory = OUTPUT_DIR / str(run.get("trajectory"))
        if not trajectory.is_file():
            raise SystemExit(f"Missing trajectory: {trajectory}")
        if sha256_file(trajectory) != run.get("trajectory_sha256"):
            raise SystemExit(f"Trajectory hash mismatch: {run.get('run_id')}")
        record = OUTPUT_DIR / str(run.get("record"))
        record_value = read_json(record)
        if record_value.get("benchmark_outcomes_accessed") is not False:
            raise SystemExit(f"Run record violates outcome boundary: {run.get('run_id')}")
    return state


def structural_summary(trajectory: Any) -> dict[str, Any]:
    scan_forbidden(trajectory)
    summary = {
        "root_type": type(trajectory).__name__,
        "top_level_keys": sorted(trajectory.keys()) if isinstance(trajectory, dict) else [],
        "list_lengths": {},
        "scalar_field_count": 0,
        "mapping_count": 0,
        "list_count": 0,
    }

    def walk(value: Any, path: str) -> None:
        if isinstance(value, dict):
            summary["mapping_count"] += 1
            for key, child in value.items():
                walk(child, f"{path}.{key}")
        elif isinstance(value, list):
            summary["list_count"] += 1
            summary["list_lengths"][path] = len(value)
            for index, child in enumerate(value):
                walk(child, f"{path}[{index}]")
        else:
            summary["scalar_field_count"] += 1

    walk(trajectory, "root")
    summary["list_lengths"] = dict(sorted(summary["list_lengths"].items()))
    return summary


def blind_aliases(runs: list[dict[str, Any]]) -> dict[str, str]:
    releases = sorted({str(run["release"]) for run in runs})
    if len(releases) != 2:
        raise SystemExit("Exactly two releases are required for blinding")
    ranked = sorted(releases, key=lambda release: sha256_bytes(release.encode("utf-8")))
    return {ranked[0]: "System-A", ranked[1]: "System-B"}


def compile_primary() -> list[Path]:
    state = load_completed_state()
    aliases = blind_aliases(state["runs"])
    PACKAGES_DIR.mkdir(parents=True, exist_ok=True)
    package_paths: list[Path] = []
    package_rows: list[dict[str, Any]] = []
    for run in state["runs"]:
        trajectory_path = OUTPUT_DIR / run["trajectory"]
        trajectory = read_json(trajectory_path)
        summary = structural_summary(trajectory)
        package = {
            "schema": PACKAGE_SCHEMA,
            "case_id": state["case_id"],
            "blind_system": aliases[run["release"]],
            "repetition": run["repetition"],
            "run_id_blinded": f"{aliases[run['release']]}-r{run['repetition']}",
            "source_trajectory_sha256": sha256_file(trajectory_path),
            "execution_plan_sha256": state["execution_plan_sha256"],
            "environment_lock_sha256": state["environment_lock_sha256"],
            "outcomes_accessed": False,
            "evidence": summary,
            "limitations": [
                "Structural evidence package only; semantic FAR adjudication must remain outcome-blind.",
                "No benchmark pass/fail, grader output, gold patch, or hidden test information is included.",
            ],
        }
        target = PACKAGES_DIR / f"{package['run_id_blinded']}.json"
        write_json(target, package)
        package_paths.append(target)
        package_rows.append({
            "blind_system": package["blind_system"],
            "repetition": package["repetition"],
            "package": str(target.relative_to(OUTPUT_DIR)),
            "package_sha256": sha256_file(target),
            "trajectory_sha256": package["source_trajectory_sha256"],
            "evidence": summary,
        })

    by_system: dict[str, list[dict[str, Any]]] = {}
    for row in package_rows:
        by_system.setdefault(row["blind_system"], []).append(row)
    comparison = {
        "schema": COMPARISON_SCHEMA,
        "case_id": state["case_id"],
        "generated_at": utc_now(),
        "outcomes_accessed": False,
        "systems": {
            system: {
                "repetitions": len(rows),
                "packages": [{k: row[k] for k in ("repetition", "package", "package_sha256", "trajectory_sha256")} for row in sorted(rows, key=lambda x: x["repetition"])],
                "structural_ranges": {
                    key: [min(row["evidence"][key] for row in rows), max(row["evidence"][key] for row in rows)]
                    for key in ("scalar_field_count", "mapping_count", "list_count")
                },
            }
            for system, rows in sorted(by_system.items())
        },
        "decision_boundary": "This file records outcome-blind structural comparison evidence only and makes no performance or superiority claim.",
    }
    write_json(COMPARISON_PATH, comparison)
    return package_paths + [COMPARISON_PATH]


def freeze_primary() -> Path:
    paths = compile_primary()
    entries = []
    for path in sorted(paths):
        entries.append({
            "path": str(path.relative_to(OUTPUT_DIR)),
            "sha256": sha256_file(path),
            "size_bytes": path.stat().st_size,
        })
    freeze = {
        "schema": FREEZE_SCHEMA,
        "created_at": utc_now(),
        "outcomes_accessed": False,
        "artifact_count": len(entries),
        "artifacts": entries,
        "root_sha256": sha256_bytes(canonical_json(entries)),
        "reveal_permitted_only_after_verification": True,
    }
    write_json(FREEZE_PATH, freeze)
    verify_freeze()
    return FREEZE_PATH


def verify_freeze() -> dict[str, Any]:
    freeze = read_json(FREEZE_PATH)
    if freeze.get("schema") != FREEZE_SCHEMA or freeze.get("outcomes_accessed") is not False:
        raise SystemExit("Primary freeze schema or outcome boundary mismatch")
    entries = freeze.get("artifacts")
    if not isinstance(entries, list) or freeze.get("artifact_count") != len(entries):
        raise SystemExit("Primary freeze artifact count mismatch")
    for entry in entries:
        path = OUTPUT_DIR / entry["path"]
        if not path.is_file() or sha256_file(path) != entry["sha256"] or path.stat().st_size != entry["size_bytes"]:
            raise SystemExit(f"Primary freeze verification failed: {entry['path']}")
    if freeze.get("root_sha256") != sha256_bytes(canonical_json(entries)):
        raise SystemExit("Primary freeze root hash mismatch")
    return freeze


def reveal(outcomes_path: Path) -> Path:
    freeze = verify_freeze()
    outcomes = read_json(outcomes_path)
    if not isinstance(outcomes, dict):
        raise SystemExit("Outcome reveal input must be a JSON object")
    expected = {run["run_id"] for run in load_completed_state()["runs"]}
    provided = set(outcomes)
    if provided != expected:
        raise SystemExit(f"Outcome keys must exactly match frozen run IDs; missing={sorted(expected-provided)}, extra={sorted(provided-expected)}")
    reveal_payload = {
        "schema": REVEAL_SCHEMA,
        "revealed_at": utc_now(),
        "primary_freeze_sha256": sha256_file(FREEZE_PATH),
        "primary_root_sha256": freeze["root_sha256"],
        "outcomes_source_sha256": sha256_file(outcomes_path),
        "outcomes": outcomes,
        "claim_boundary": "Outcomes were attached after primary artifact verification; association does not establish general superiority or external validation.",
    }
    target = REVEAL_DIR / "outcome-reveal.json"
    write_json(target, reveal_payload)
    return target


def main() -> None:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("compile")
    sub.add_parser("freeze")
    sub.add_parser("verify-freeze")
    reveal_parser = sub.add_parser("reveal")
    reveal_parser.add_argument("--outcomes", type=Path, required=True)
    args = parser.parse_args()
    if args.command == "compile":
        print("\n".join(str(path) for path in compile_primary()))
    elif args.command == "freeze":
        print(freeze_primary())
    elif args.command == "verify-freeze":
        print(json.dumps(verify_freeze(), indent=2, sort_keys=True))
    else:
        print(reveal(args.outcomes.resolve()))


if __name__ == "__main__":
    main()
