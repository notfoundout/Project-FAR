from __future__ import annotations

import argparse
import json
import os
import shutil
import stat
import subprocess
import tempfile
from pathlib import Path

import execute_controller as base
import validated_execute_controller as controller


SENTINEL_PROCESS_EXIT = 86
EXPECTED_CONTROLLER_RETURN = 75


def write_wrapper(
    path: Path,
    real_executable: Path,
    sentinel: Path,
    task_id: str,
) -> None:
    script = f'''#!/usr/bin/env python3
import json
import os
import sys
from pathlib import Path

REAL = {str(real_executable)!r}
SENTINEL = {str(sentinel)!r}
TASK_ID = {task_id!r}
PROCESS_EXIT = {SENTINEL_PROCESS_EXIT}
args = sys.argv[1:]
if "--print_config" in args:
    os.execv(REAL, [REAL, *args])
output_arg = next((item for item in args if item.startswith("--output_dir=")), None)
if output_arg is None:
    raise SystemExit("frozen output_dir argument missing")
output_dir = Path(output_arg.split("=", 1)[1])
output_dir.mkdir(parents=True, exist_ok=True)
(output_dir / "run_batch_exit_statuses.yaml").write_text(
    "instances_by_exit_status:\\n"
    "  exit_error:\\n"
    f"    - {{TASK_ID}}\\n",
    encoding="utf-8",
)
(output_dir / f"{{TASK_ID}}.pred").write_text(
    json.dumps({{"instance_id": TASK_ID, "model_patch": None}}),
    encoding="utf-8",
)
with open(SENTINEL, "w", encoding="utf-8") as handle:
    json.dump({{
        "argv": args,
        "gemini_key_present": bool(os.environ.get("GEMINI_API_KEY")),
        "github_token_present": bool(os.environ.get("GITHUB_TOKEN")),
        "gh_token_present": bool(os.environ.get("GH_TOKEN")),
        "status_file": str(output_dir / "run_batch_exit_statuses.yaml"),
        "prediction_file": str(output_dir / f"{{TASK_ID}}.pred"),
    }}, handle, indent=2, sort_keys=True)
    handle.write("\\n")
print("HTTP 429 RESOURCE_EXHAUSTED request-per-day", file=sys.stderr)
sys.exit(PROCESS_EXIT)
'''
    path.write_text(script, encoding="utf-8")
    path.chmod(path.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)


def write_valid_completed_run(
    run: dict[str, object],
    task_id: str,
    plan_sha256: str,
    image: str,
) -> None:
    run_id = str(run["run_id"])
    run_dir = base.RUNS_DIR / run_id
    output = run_dir / "sweagent-output"
    output.mkdir(parents=True, exist_ok=True)
    (output / "run_batch_exit_statuses.yaml").write_text(
        "instances_by_exit_status:\n"
        "  submitted:\n"
        f"    - {task_id}\n",
        encoding="utf-8",
    )
    (output / f"{task_id}.pred").write_text(
        json.dumps({"instance_id": task_id, "model_patch": "rehearsal-patch"}),
        encoding="utf-8",
    )
    base.write_json(run_dir / "instance.json", [{"id": task_id}])
    invocation = {
        "schema": "far-swe-agent-invocation/1.3",
        "run_id": run_id,
        "release": run["release"],
        "commit": run["full_commit"],
        "task_id": task_id,
        "image": image,
        "agent_config_sha256": base.sha256_file(base.CONFIG_PATH),
        "execution_plan_sha256": plan_sha256,
        "benchmark_outcomes_accessible": False,
    }
    base.write_json(run_dir / "invocation.json", invocation)
    (run_dir / "stdout.log").write_text("", encoding="utf-8")
    (run_dir / "stderr.log").write_text("", encoding="utf-8")

    trajectory_path = base.OUTPUT_DIR / str(run["trajectory"])
    trajectory_path.parent.mkdir(parents=True, exist_ok=True)
    base.write_json(trajectory_path, {"rehearsal": True, "run_id": run_id})
    trajectory_sha256 = base.sha256_file(trajectory_path)
    completed_at = base.utc_now()
    record = {
        "schema": "far-swe-agent-run-record/1.2",
        "run_id": run_id,
        "release": run["release"],
        "commit": run["full_commit"],
        "repetition": run["repetition"],
        "task_id": task_id,
        "image": image,
        "execution_plan_sha256": plan_sha256,
        "state": "complete",
        "returncode": 0,
        "completed_at": completed_at,
        "benchmark_outcomes_accessed": False,
        "trajectory": run["trajectory"],
        "trajectory_sha256": trajectory_sha256,
        "artifact_sha256": controller._current_artifact_hashes(run_dir),
    }
    record_path = run_dir / "run-record.json"
    base.write_json(record_path, record)
    run.update(
        {
            "state": "complete",
            "attempts": 1,
            "completed_at": completed_at,
            "record": str(record_path.relative_to(base.OUTPUT_DIR)),
            "outcome_category": "success_with_patch",
            "trajectory_sha256": trajectory_sha256,
        }
    )


def prepare_state(target_release: str) -> None:
    manifest, lock, task = base.frozen_inputs()
    plan_sha = base.validate_plan(manifest, lock)
    state = base.initial_state(manifest, lock, plan_sha)
    if target_release == "v1.0.1":
        for run in state["runs"][:2]:
            write_valid_completed_run(
                run,
                task["instance_id"],
                plan_sha,
                lock["immutable_image_reference"],
            )
    base.save_state(state)


def assert_rehearsal(
    target_release: str, task_id: str, sentinel: Path, returncode: int
) -> None:
    if returncode != EXPECTED_CONTROLLER_RETURN:
        raise SystemExit(
            f"Expected validated controller return {EXPECTED_CONTROLLER_RETURN}, got {returncode}"
        )
    if not sentinel.is_file():
        raise SystemExit("Execution wrapper was not reached")

    launch = json.loads(sentinel.read_text(encoding="utf-8"))
    if not launch["gemini_key_present"]:
        raise SystemExit("Execution boundary did not preserve model credential presence")
    if launch["github_token_present"] or launch["gh_token_present"]:
        raise SystemExit("Execution boundary leaked GitHub credentials")
    if "--print_config" in launch["argv"]:
        raise SystemExit("Sentinel captured parser validation instead of final execution")
    for field in ("status_file", "prediction_file"):
        if not Path(launch[field]).is_file():
            raise SystemExit(f"Sentinel did not preserve {field}")

    state = base.read_json(base.STATE_PATH)
    failed = [item for item in state["runs"] if item["state"] == "failed_retryable"]
    if len(failed) != 1:
        raise SystemExit(f"Expected exactly one retryable run, found {len(failed)}")
    run = failed[0]
    if run["release"] != target_release or run["attempts"] != 1:
        raise SystemExit("Rehearsal did not execute the intended frozen run exactly once")
    if run.get("outcome_category") != "provider_quota_exhaustion":
        raise SystemExit("Validated controller did not classify the simulated quota failure")
    if target_release == "v1.0.1":
        prior = state["runs"][:2]
        if any(item["state"] != "complete" for item in prior):
            raise SystemExit("Validated restoration rejected valid prior completions")

    run_dir = base.RUNS_DIR / run["run_id"]
    required = [
        run_dir / "instance.json",
        run_dir / "invocation.json",
        run_dir / "stdout.log",
        run_dir / "stderr.log",
        run_dir / "run-record.json",
        run_dir / "sweagent-output" / "run_batch_exit_statuses.yaml",
        run_dir / "sweagent-output" / f"{task_id}.pred",
    ]
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise SystemExit(f"Rehearsal artifacts missing: {missing}")

    invocation = base.read_json(run_dir / "invocation.json")
    record = base.read_json(run_dir / "run-record.json")
    if invocation.get("schema") != "far-swe-agent-invocation/1.3":
        raise SystemExit("Validated invocation schema mismatch")
    if invocation.get("benchmark_outcomes_accessible") is not False:
        raise SystemExit("Invocation exposed benchmark outcomes")
    if record.get("schema") != "far-swe-agent-run-record/1.2":
        raise SystemExit("Validated run-record schema mismatch")
    if record.get("benchmark_outcomes_accessed") is not False:
        raise SystemExit("Run record exposed benchmark outcomes")
    if record.get("state") != "failed_retryable" or record.get("returncode") != SENTINEL_PROCESS_EXIT:
        raise SystemExit("Sentinel stop was not recorded deterministically")
    outcome = record.get("outcome", {})
    if outcome.get("category") != "provider_quota_exhaustion" or outcome.get("retryable") is not True:
        raise SystemExit("Validated outcome evidence is missing or incorrect")
    if list(base.TRAJECTORY_DIR.glob("*.traj")):
        raise SystemExit("No-model rehearsal unexpectedly produced a trajectory")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--agent-repo", type=Path, required=True)
    parser.add_argument("--release", choices=("v1.0.0", "v1.0.1"), required=True)
    parser.add_argument("--commit", required=True)
    args = parser.parse_args()

    agent_repo = args.agent_repo.resolve()
    base.verify_agent_checkout(agent_repo, args.commit)

    real_executable = shutil.which("sweagent")
    if real_executable is None:
        raise SystemExit("Installed pinned SWE-agent entry point is missing")

    shutil.rmtree(base.OUTPUT_DIR, ignore_errors=True)
    env = os.environ.copy()
    env["GEMINI_API_KEY"] = "far-no-model-rehearsal-key"
    subprocess.run(
        ["python", "run_comparison.py", "plan"],
        cwd=base.CASE_DIR,
        env=env,
        check=True,
        text=True,
    )
    manifest, _lock, task = base.frozen_inputs()
    prepare_state(args.release)

    with tempfile.TemporaryDirectory(prefix="far-sweagent-rehearsal-") as temp:
        temp_path = Path(temp)
        wrapper = temp_path / "sweagent"
        sentinel = temp_path / "launch-boundary.json"
        write_wrapper(
            wrapper,
            Path(real_executable).resolve(),
            sentinel,
            task["instance_id"],
        )
        original_path = os.environ.get("PATH", "")
        os.environ["PATH"] = f"{temp_path}{os.pathsep}{original_path}"
        os.environ["GEMINI_API_KEY"] = "far-no-model-rehearsal-key"
        try:
            returncode = controller.execute_one(agent_repo)
        finally:
            os.environ["PATH"] = original_path
            os.environ.pop("GEMINI_API_KEY", None)
        assert_rehearsal(args.release, task["instance_id"], sentinel, returncode)

    print(
        json.dumps(
            {
                "case_id": manifest["case_id"],
                "release": args.release,
                "commit": args.commit,
                "controller": "validated_execute_controller",
                "parser": "actual pinned SWE-agent",
                "image": "actual frozen digest verified locally",
                "final_launch_boundary_reached": True,
                "model_call_started": False,
                "simulated_provider_failure": "provider_quota_exhaustion",
                "controller_return": EXPECTED_CONTROLLER_RETURN,
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
