from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

CASE_DIR = Path(__file__).parent
MANIFEST_PATH = CASE_DIR / "manifest.json"
LOCK_PATH = CASE_DIR / "environment-freeze" / "environment-lock.json"
TASK_PATH = CASE_DIR / "environment-freeze" / "task-record.public.json"
CONFIG_PATH = CASE_DIR / "agent-config.yaml"
OUTPUT_DIR = CASE_DIR / "execution-output"
STATE_PATH = OUTPUT_DIR / "execution-state.json"
TRAJECTORY_DIR = OUTPUT_DIR / "trajectories"
RUNS_DIR = OUTPUT_DIR / "runs"

SCHEMA = "far-swe-agent-execution-state/1.0"
RUN_RECORD_SCHEMA = "far-swe-agent-run-record/1.0"
FULL_COMMITS = {
    "8ed382c": "8ed382c1af1a21f63410b9a0cda14759e64b49c0",
    "6aff215": "6aff2155dd6fb2a8d19069f5c344f85a54f6c2fa",
}
QUOTA_MARKERS = (
    "resource_exhausted",
    "rate limit",
    "ratelimit",
    "quota exceeded",
    "too many requests",
    "status code: 429",
    "http 429",
)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def canonical_json(value: object) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def read_json(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise SystemExit(f"Missing required file: {path}")
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise SystemExit(f"Expected JSON object: {path}")
    return value


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(canonical_json(value))


def frozen_inputs() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    manifest = read_json(MANIFEST_PATH)
    lock = read_json(LOCK_PATH)
    task = read_json(TASK_PATH)

    if manifest.get("status") != "execution_inputs_frozen":
        raise SystemExit("Manifest is not frozen")
    frozen = manifest["frozen_inputs"]
    if sha256_file(LOCK_PATH) != frozen.get("environment_lock_sha256"):
        raise SystemExit("Frozen environment lock hash mismatch")
    if lock.get("task_id") != frozen.get("task_id") or task.get("instance_id") != frozen.get("task_id"):
        raise SystemExit("Task identity mismatch across manifest, lock, and public task record")
    if task.get("outcome_fields_included") is not False:
        raise SystemExit("Public task record does not prove outcome-field exclusion")
    if lock.get("outcome_data_exported") is not False or lock.get("model_call_started") is not False:
        raise SystemExit("Environment lock violates pre-execution boundaries")
    immutable = lock.get("immutable_image_reference")
    digest = lock.get("registry_digest")
    repository = lock.get("registry_repository")
    if not isinstance(immutable, str) or immutable != f"{repository}@{digest}":
        raise SystemExit("Environment image is not bound to its immutable registry digest")
    if not isinstance(digest, str) or not digest.startswith("sha256:") or len(digest) != 71:
        raise SystemExit("Malformed registry digest")
    return manifest, lock, task


def expected_runs(manifest: dict[str, Any]) -> list[dict[str, Any]]:
    runs = manifest["execution_requirements"]["runs"]
    if len(runs) != 4:
        raise SystemExit("Exactly four frozen runs are required")
    normalized: list[dict[str, Any]] = []
    for index, item in enumerate(runs, start=1):
        short = item["commit"]
        if short not in FULL_COMMITS:
            raise SystemExit(f"Unknown frozen SWE-agent commit: {short}")
        normalized.append(
            {
                **item,
                "slot": index,
                "run_id": f"{item['release']}-r{item['repetition']}",
                "full_commit": FULL_COMMITS[short],
            }
        )
    return normalized


def initial_state(manifest: dict[str, Any], lock: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema": SCHEMA,
        "case_id": manifest["case_id"],
        "manifest_sha256": sha256_file(MANIFEST_PATH),
        "environment_lock_sha256": sha256_file(LOCK_PATH),
        "immutable_image_reference": lock["immutable_image_reference"],
        "created_at": utc_now(),
        "updated_at": utc_now(),
        "runs": [
            {
                **item,
                "state": "pending",
                "attempts": 0,
                "record": None,
                "trajectory": f"trajectories/{item['trajectory_artifact']}",
            }
            for item in expected_runs(manifest)
        ],
    }


def load_state(manifest: dict[str, Any], lock: dict[str, Any]) -> dict[str, Any]:
    if not STATE_PATH.is_file():
        return initial_state(manifest, lock)
    state = read_json(STATE_PATH)
    if state.get("schema") != SCHEMA:
        raise SystemExit("Execution state schema mismatch")
    if state.get("case_id") != manifest.get("case_id"):
        raise SystemExit("Execution state case mismatch")
    if state.get("manifest_sha256") != sha256_file(MANIFEST_PATH):
        raise SystemExit("Execution state was created for a different manifest")
    if state.get("environment_lock_sha256") != sha256_file(LOCK_PATH):
        raise SystemExit("Execution state was created for a different environment lock")
    if state.get("immutable_image_reference") != lock.get("immutable_image_reference"):
        raise SystemExit("Execution state image mismatch")
    expected = expected_runs(manifest)
    actual = state.get("runs")
    if not isinstance(actual, list) or len(actual) != len(expected):
        raise SystemExit("Execution state run matrix mismatch")
    for frozen, recorded in zip(expected, actual, strict=True):
        for key in ("slot", "run_id", "release", "commit", "full_commit", "repetition", "trajectory_artifact"):
            if recorded.get(key) != frozen.get(key):
                raise SystemExit(f"Execution state drift at run {frozen['run_id']}: {key}")
    return state


def save_state(state: dict[str, Any]) -> None:
    state["updated_at"] = utc_now()
    write_json(STATE_PATH, state)


def verify_agent_checkout(agent_repo: Path, full_commit: str) -> None:
    if not (agent_repo / ".git").is_dir():
        raise SystemExit(f"SWE-agent checkout is missing: {agent_repo}")
    actual = subprocess.run(
        ["git", "-C", str(agent_repo), "rev-parse", "HEAD"],
        check=True,
        text=True,
        capture_output=True,
    ).stdout.strip()
    if actual != full_commit:
        raise SystemExit(f"SWE-agent checkout mismatch: expected {full_commit}, got {actual}")
    for relative in ("run.py", "config/default.yaml", "sweagent/run/run_batch.py"):
        if not (agent_repo / relative).is_file():
            raise SystemExit(f"Pinned SWE-agent interface file is missing: {relative}")


def verify_cli_contract(agent_repo: Path) -> None:
    command = [sys.executable, str(agent_repo / "run.py"), "--help"]
    result = subprocess.run(command, cwd=agent_repo, text=True, capture_output=True)
    combined = result.stdout + "\n" + result.stderr
    if result.returncode != 0:
        raise SystemExit(f"Pinned SWE-agent CLI help failed:\n{combined[-4000:]}")
    required = ("--config", "--instances", "--output_dir", "--num_workers")
    missing = [token for token in required if token not in combined]
    if missing:
        raise SystemExit(f"Pinned SWE-agent CLI contract mismatch; missing {missing}")


def verify_local_image(lock: dict[str, Any]) -> None:
    immutable = lock["immutable_image_reference"]
    result = subprocess.run(
        ["docker", "image", "inspect", immutable, "--format", "{{json .RepoDigests}}"],
        text=True,
        capture_output=True,
    )
    if result.returncode != 0:
        raise SystemExit(f"Frozen image is not present locally: {immutable}")
    repo_digests = json.loads(result.stdout.strip())
    if immutable not in repo_digests:
        raise SystemExit(f"Pulled image does not expose the frozen digest: {repo_digests!r}")


def build_instance_file(task: dict[str, Any], lock: dict[str, Any], target: Path) -> None:
    instance = [
        {
            "image_name": lock["immutable_image_reference"],
            "problem_statement": task["problem_statement"],
            "id": task["instance_id"],
            "repo_name": "testbed",
            "base_commit": task["base_commit"],
            "extra_fields": {
                "far_case_id": read_json(MANIFEST_PATH)["case_id"],
                "outcome_data_accessible": False,
            },
        }
    ]
    write_json(target, instance)


def next_pending(state: dict[str, Any]) -> dict[str, Any] | None:
    for item in state["runs"]:
        if item["state"] in {"pending", "quota_paused", "failed_retryable"}:
            return item
    return None


def classify_failure(stdout: str, stderr: str) -> str:
    combined = (stdout + "\n" + stderr).lower()
    if any(marker in combined for marker in QUOTA_MARKERS):
        return "quota_paused"
    return "failed"


def collect_hashes(root: Path) -> dict[str, str]:
    hashes: dict[str, str] = {}
    if not root.exists():
        return hashes
    for path in sorted(p for p in root.rglob("*") if p.is_file()):
        hashes[str(path.relative_to(root))] = sha256_file(path)
    return hashes


def locate_trajectory(output_dir: Path, task_id: str) -> Path:
    candidates = sorted(output_dir.rglob("*.traj"))
    exact = [path for path in candidates if path.stem == task_id]
    if len(exact) == 1:
        return exact[0]
    if len(candidates) == 1:
        return candidates[0]
    raise SystemExit(f"Expected exactly one trajectory, found {[str(p) for p in candidates]}")


def execute_one(agent_repo: Path) -> int:
    manifest, lock, task = frozen_inputs()
    verify_local_image(lock)
    state = load_state(manifest, lock)
    run = next_pending(state)
    if run is None:
        print("All four frozen runs are complete.")
        return 0

    if not os.environ.get("GEMINI_API_KEY"):
        raise SystemExit("GEMINI_API_KEY is required; no model call was started")

    verify_agent_checkout(agent_repo, run["full_commit"])
    verify_cli_contract(agent_repo)

    run_dir = RUNS_DIR / run["run_id"]
    swe_output = run_dir / "sweagent-output"
    run_dir.mkdir(parents=True, exist_ok=True)
    TRAJECTORY_DIR.mkdir(parents=True, exist_ok=True)
    instance_path = run_dir / "instance.json"
    build_instance_file(task, lock, instance_path)

    command = [
        sys.executable,
        str(agent_repo / "run.py"),
        "--config",
        str(agent_repo / "config" / "default.yaml"),
        "--config",
        str(CONFIG_PATH.resolve()),
        "--instances.type=file",
        f"--instances.path={instance_path.resolve()}",
        f"--output_dir={swe_output.resolve()}",
        "--num_workers=1",
        "--progress_bar=False",
        "--random_delay_multiplier=0",
        "--raise_exceptions=True",
        "--redo_existing=False",
    ]
    invocation = {
        "schema": "far-swe-agent-invocation/1.0",
        "run_id": run["run_id"],
        "release": run["release"],
        "commit": run["full_commit"],
        "task_id": task["instance_id"],
        "image": lock["immutable_image_reference"],
        "agent_config_sha256": sha256_file(CONFIG_PATH),
        "command": command,
        "environment_variables_present": {"GEMINI_API_KEY": True},
        "benchmark_outcomes_accessible": False,
        "started_at": utc_now(),
    }
    write_json(run_dir / "invocation.json", invocation)

    run["attempts"] += 1
    run["state"] = "running"
    run["started_at"] = invocation["started_at"]
    save_state(state)

    started = time.monotonic()
    result = subprocess.run(command, cwd=agent_repo, text=True, capture_output=True, env=os.environ.copy())
    duration = time.monotonic() - started
    (run_dir / "stdout.log").write_text(result.stdout, encoding="utf-8", errors="replace")
    (run_dir / "stderr.log").write_text(result.stderr, encoding="utf-8", errors="replace")

    record = {
        "schema": RUN_RECORD_SCHEMA,
        "run_id": run["run_id"],
        "release": run["release"],
        "commit": run["full_commit"],
        "repetition": run["repetition"],
        "task_id": task["instance_id"],
        "image": lock["immutable_image_reference"],
        "returncode": result.returncode,
        "duration_seconds": round(duration, 3),
        "completed_at": utc_now(),
        "benchmark_outcomes_accessed": False,
    }

    if result.returncode != 0:
        failure_state = classify_failure(result.stdout, result.stderr)
        record["state"] = failure_state
        record["artifact_sha256"] = collect_hashes(run_dir)
        write_json(run_dir / "run-record.json", record)
        run["state"] = failure_state
        run["record"] = str((run_dir / "run-record.json").relative_to(OUTPUT_DIR))
        save_state(state)
        if failure_state == "quota_paused":
            print("Provider quota/rate limit detected. State preserved for exact resume.")
            return 75
        print("SWE-agent run failed. State preserved; inspect run logs.")
        return result.returncode or 1

    trajectory_source = locate_trajectory(swe_output, task["instance_id"])
    trajectory_target = TRAJECTORY_DIR / run["trajectory_artifact"]
    shutil.copy2(trajectory_source, trajectory_target)
    record["state"] = "complete"
    record["trajectory"] = str(trajectory_target.relative_to(OUTPUT_DIR))
    record["trajectory_sha256"] = sha256_file(trajectory_target)
    record["artifact_sha256"] = collect_hashes(run_dir)
    write_json(run_dir / "run-record.json", record)

    run["state"] = "complete"
    run["completed_at"] = record["completed_at"]
    run["record"] = str((run_dir / "run-record.json").relative_to(OUTPUT_DIR))
    run["trajectory_sha256"] = record["trajectory_sha256"]
    save_state(state)
    print(f"Completed frozen run {run['run_id']} and preserved {trajectory_target}.")
    return 0


def validate_only(agent_repo: Path | None) -> None:
    manifest, lock, _ = frozen_inputs()
    state = load_state(manifest, lock)
    if agent_repo is not None:
        pending = next_pending(state)
        if pending is not None:
            verify_agent_checkout(agent_repo, pending["full_commit"])
            verify_cli_contract(agent_repo)
    print(json.dumps({"next_run": next_pending(state), "state": state}, indent=2, sort_keys=True))


def main() -> None:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    validate_parser = sub.add_parser("validate")
    validate_parser.add_argument("--agent-repo", type=Path)
    execute_parser = sub.add_parser("execute-next")
    execute_parser.add_argument("--agent-repo", type=Path, required=True)
    sub.add_parser("status")
    args = parser.parse_args()

    if args.command == "validate":
        validate_only(args.agent_repo)
    elif args.command == "status":
        manifest, lock, _ = frozen_inputs()
        print(json.dumps(load_state(manifest, lock), indent=2, sort_keys=True))
    else:
        raise SystemExit(execute_one(args.agent_repo.resolve()))


if __name__ == "__main__":
    main()
