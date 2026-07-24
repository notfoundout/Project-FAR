from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
from pathlib import Path

from validate_manifest import validate

CASE_DIR = Path(__file__).parent
MANIFEST_PATH = CASE_DIR / "manifest.json"
CONFIG_PATH = CASE_DIR / "agent-config.yaml"
OUTPUT_DIR = CASE_DIR / "execution-output"


def load_manifest() -> dict:
    payload = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    validate(payload)
    return payload


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_environment_lock(manifest: dict) -> dict:
    frozen = manifest["frozen_inputs"]
    if manifest["status"] != "execution_inputs_frozen":
        raise SystemExit("SWE-bench environment is not frozen")
    lock_path = CASE_DIR / frozen["environment_lock_path"]
    if not lock_path.is_file():
        raise SystemExit(f"Missing frozen environment lock: {lock_path}")
    actual_hash = sha256_file(lock_path)
    if actual_hash != frozen["environment_lock_sha256"]:
        raise SystemExit("Frozen environment lock hash mismatch")
    lock = json.loads(lock_path.read_text(encoding="utf-8"))
    if lock.get("local_image_id") != frozen["local_image_id"]:
        raise SystemExit("Frozen local image ID does not match environment lock")
    if lock.get("immutable_image_reference") != frozen["immutable_image_reference"]:
        raise SystemExit("Frozen immutable image reference does not match environment lock")
    if lock.get("registry_digest") != frozen["registry_digest"]:
        raise SystemExit("Frozen registry digest does not match environment lock")
    if lock.get("task_id") != frozen["task_id"]:
        raise SystemExit("Frozen task ID does not match environment lock")
    if lock.get("swebench_harness_commit") != frozen["swebench_harness_commit"]:
        raise SystemExit("Frozen SWE-bench harness commit does not match environment lock")
    if lock.get("cross_runner_portable") is not True:
        raise SystemExit("Environment lock is not cross-runner portable")
    if lock.get("outcome_data_exported") is not False:
        raise SystemExit("Environment lock does not prove outcome-bearing artifacts were excluded")
    if lock.get("model_call_started") is not False:
        raise SystemExit("Environment lock violates the pre-execution model-call boundary")
    return lock


def pull_and_verify_frozen_image(lock: dict) -> None:
    reference = lock["immutable_image_reference"]
    expected_digest = lock["registry_digest"]
    subprocess.run(["docker", "pull", reference], check=True)
    result = subprocess.run(
        ["docker", "image", "inspect", reference, "--format", "{{json .RepoDigests}}"],
        check=True,
        text=True,
        capture_output=True,
    )
    repo_digests = json.loads(result.stdout.strip())
    if not isinstance(repo_digests, list) or reference not in repo_digests:
        raise SystemExit(f"Pulled image does not expose the frozen digest reference: {repo_digests!r}")
    if not reference.endswith("@" + expected_digest):
        raise SystemExit("Frozen image reference and digest disagree")


def preflight(manifest: dict, *, require_secret: bool) -> dict:
    if shutil.which("git") is None:
        raise SystemExit("git is required")
    if shutil.which("docker") is None:
        raise SystemExit("Docker is required")
    secret_name = manifest["execution_requirements"]["required_secret"]
    if require_secret and not os.environ.get(secret_name):
        raise SystemExit(f"{secret_name} is required; no run was started")
    config_hash = sha256_file(CONFIG_PATH)
    if config_hash != manifest["frozen_inputs"]["agent_config_sha256"]:
        raise SystemExit("agent-config.yaml does not match the frozen hash")
    lock = load_environment_lock(manifest)
    pull_and_verify_frozen_image(lock)
    return lock


def write_execution_plan(manifest: dict, lock: dict) -> Path:
    OUTPUT_DIR.mkdir(exist_ok=True)
    plan = {
        "schema": "far-external-execution-plan/0.4",
        "case_id": manifest["case_id"],
        "manifest_sha256": sha256_file(MANIFEST_PATH),
        "agent_config_sha256": sha256_file(CONFIG_PATH),
        "environment_lock_sha256": manifest["frozen_inputs"]["environment_lock_sha256"],
        "immutable_image_reference": lock["immutable_image_reference"],
        "registry_digest": lock["registry_digest"],
        "task_id": manifest["frozen_inputs"]["task_id"],
        "model": manifest["frozen_inputs"]["model"],
        "free_tier": True,
        "maximum_model_cost_usd": 0.0,
        "sequential_only": True,
        "quota_policy": "Stop cleanly on provider quota exhaustion and resume the same frozen run after reset; never substitute another model.",
        "runs": [
            {
                **item,
                "workspace": f"workspaces/{item['release']}-run-{item['repetition']}",
                "trajectory": f"trajectories/{item['trajectory_artifact']}",
                "outcomes_accessible": False,
                "state": "pending",
            }
            for item in manifest["execution_requirements"]["runs"]
        ],
        "next_gate": "Execute one frozen run at a time, preserve raw trajectories, compile FAR packages, and hash-freeze the primary comparison before outcome reveal.",
    }
    target = OUTPUT_DIR / "execution-plan.json"
    target.write_text(json.dumps(plan, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return target


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("preflight", "plan"))
    args = parser.parse_args()

    manifest = load_manifest()
    lock = preflight(manifest, require_secret=args.mode == "plan")
    if args.mode == "preflight":
        print("Frozen digest-pinned SWE-bench environment and inputs verified. No model call was started.")
        return

    target = write_execution_plan(manifest, lock)
    print(f"Wrote {target}. No benchmark outcome was accessed and no model call was started.")


if __name__ == "__main__":
    main()
