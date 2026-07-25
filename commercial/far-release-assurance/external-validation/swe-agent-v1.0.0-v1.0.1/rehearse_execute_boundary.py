from __future__ import annotations

import argparse
import json
import os
import shutil
import stat
import subprocess
import tempfile
from pathlib import Path

import execute_controller as controller


SENTINEL_EXIT = 86


def write_wrapper(path: Path, real_executable: Path, sentinel: Path) -> None:
    script = f'''#!/usr/bin/env python3
import json
import os
import sys

REAL = {str(real_executable)!r}
SENTINEL = {str(sentinel)!r}
args = sys.argv[1:]
if "--print_config" in args:
    os.execv(REAL, [REAL, *args])
with open(SENTINEL, "w", encoding="utf-8") as handle:
    json.dump({{
        "argv": args,
        "gemini_key_present": bool(os.environ.get("GEMINI_API_KEY")),
        "github_token_present": bool(os.environ.get("GITHUB_TOKEN")),
        "gh_token_present": bool(os.environ.get("GH_TOKEN")),
    }}, handle, indent=2, sort_keys=True)
    handle.write("\\n")
sys.exit({SENTINEL_EXIT})
'''
    path.write_text(script, encoding="utf-8")
    path.chmod(path.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)


def prepare_state(target_release: str) -> None:
    manifest, lock, _task = controller.frozen_inputs()
    plan_sha = controller.validate_plan(manifest, lock)
    state = controller.initial_state(manifest, lock, plan_sha)
    if target_release == "v1.0.1":
        for run in state["runs"][:2]:
            run["state"] = "complete"
    controller.save_state(state)


def assert_rehearsal(target_release: str, sentinel: Path, returncode: int) -> None:
    if returncode != SENTINEL_EXIT:
        raise SystemExit(f"Expected sentinel exit {SENTINEL_EXIT}, got {returncode}")
    if not sentinel.is_file():
        raise SystemExit("Execution wrapper was not reached")

    launch = json.loads(sentinel.read_text(encoding="utf-8"))
    if not launch["gemini_key_present"]:
        raise SystemExit("Execution boundary did not preserve model credential presence")
    if launch["github_token_present"] or launch["gh_token_present"]:
        raise SystemExit("Execution boundary leaked GitHub credentials")
    if "--print_config" in launch["argv"]:
        raise SystemExit("Sentinel captured parser validation instead of final execution")

    state = controller.read_json(controller.STATE_PATH)
    run = next(item for item in state["runs"] if item["state"] == "failed_retryable")
    if run["release"] != target_release or run["attempts"] != 1:
        raise SystemExit("Rehearsal did not advance the intended frozen run exactly once")

    run_dir = controller.RUNS_DIR / run["run_id"]
    required = [
        run_dir / "instance.json",
        run_dir / "invocation.json",
        run_dir / "stdout.log",
        run_dir / "stderr.log",
        run_dir / "run-record.json",
    ]
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise SystemExit(f"Rehearsal artifacts missing: {missing}")

    invocation = controller.read_json(run_dir / "invocation.json")
    record = controller.read_json(run_dir / "run-record.json")
    if invocation.get("schema") != "far-swe-agent-invocation/1.1":
        raise SystemExit("Invocation schema mismatch")
    if invocation.get("benchmark_outcomes_accessible") is not False:
        raise SystemExit("Invocation exposed benchmark outcomes")
    if record.get("benchmark_outcomes_accessed") is not False:
        raise SystemExit("Run record exposed benchmark outcomes")
    if record.get("state") != "failed_retryable" or record.get("returncode") != SENTINEL_EXIT:
        raise SystemExit("Sentinel stop was not recorded deterministically")
    if list(controller.TRAJECTORY_DIR.glob("*.traj")):
        raise SystemExit("No-model rehearsal unexpectedly produced a trajectory")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--agent-repo", type=Path, required=True)
    parser.add_argument("--release", choices=("v1.0.0", "v1.0.1"), required=True)
    parser.add_argument("--commit", required=True)
    args = parser.parse_args()

    agent_repo = args.agent_repo.resolve()
    controller.verify_agent_checkout(agent_repo, args.commit)

    real_executable = shutil.which("sweagent")
    if real_executable is None:
        raise SystemExit("Installed pinned SWE-agent entry point is missing")

    shutil.rmtree(controller.OUTPUT_DIR, ignore_errors=True)
    env = os.environ.copy()
    env["GEMINI_API_KEY"] = "far-no-model-rehearsal-key"
    subprocess.run(
        ["python", "run_comparison.py", "plan"],
        cwd=controller.CASE_DIR,
        env=env,
        check=True,
        text=True,
    )
    prepare_state(args.release)

    with tempfile.TemporaryDirectory(prefix="far-sweagent-rehearsal-") as temp:
        temp_path = Path(temp)
        wrapper = temp_path / "sweagent"
        sentinel = temp_path / "launch-boundary.json"
        write_wrapper(wrapper, Path(real_executable).resolve(), sentinel)
        original_path = os.environ.get("PATH", "")
        os.environ["PATH"] = f"{temp_path}{os.pathsep}{original_path}"
        os.environ["GEMINI_API_KEY"] = "far-no-model-rehearsal-key"
        try:
            returncode = controller.execute_one(agent_repo)
        finally:
            os.environ["PATH"] = original_path
            os.environ.pop("GEMINI_API_KEY", None)
        assert_rehearsal(args.release, sentinel, returncode)

    print(json.dumps({
        "release": args.release,
        "commit": args.commit,
        "parser": "actual pinned SWE-agent",
        "image": "actual frozen digest verified locally",
        "final_launch_boundary_reached": True,
        "model_call_started": False,
        "sentinel_exit": SENTINEL_EXIT,
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
