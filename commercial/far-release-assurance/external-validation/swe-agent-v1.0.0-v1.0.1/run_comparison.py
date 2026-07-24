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


def run(command: list[str], *, cwd: Path | None = None) -> str:
    completed = subprocess.run(command, cwd=cwd, check=True, text=True, capture_output=True)
    return completed.stdout.strip()


def load_manifest() -> dict:
    payload = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    validate(payload)
    return payload


def resolve_image_digest(reference: str) -> str:
    if shutil.which("docker") is None:
        raise SystemExit("Docker is required to resolve the immutable environment image")
    run(["docker", "pull", reference])
    value = run(["docker", "image", "inspect", reference, "--format", "{{index .RepoDigests 0}}"])
    if "@sha256:" not in value:
        raise SystemExit("Docker did not return an immutable image digest")
    return value.split("@", 1)[1]


def verify_frozen_environment(manifest: dict) -> str:
    frozen = manifest["frozen_inputs"]
    actual = resolve_image_digest(frozen["environment_image_reference"])
    expected = frozen["environment_image_digest"]
    if expected is None:
        raise SystemExit(
            f"Resolved {actual}. Commit it to manifest.json and change status to "
            "execution_inputs_frozen. No model call was started."
        )
    if actual != expected:
        raise SystemExit(f"Environment digest mismatch: expected {expected}, resolved {actual}")
    return actual


def preflight(manifest: dict, *, require_secret: bool) -> None:
    if shutil.which("git") is None:
        raise SystemExit("git is required")
    if shutil.which("docker") is None:
        raise SystemExit("Docker is required")
    if require_secret and not os.environ.get(manifest["execution_requirements"]["required_secret"]):
        raise SystemExit("ANTHROPIC_API_KEY is required; no run was started")
    config_hash = hashlib.sha256(CONFIG_PATH.read_bytes()).hexdigest()
    if config_hash != manifest["frozen_inputs"]["agent_config_sha256"]:
        raise SystemExit("agent-config.yaml does not match the frozen hash")


def write_execution_plan(manifest: dict, digest: str) -> Path:
    OUTPUT_DIR.mkdir(exist_ok=True)
    plan = {
        "schema": "far-external-execution-plan/0.1",
        "case_id": manifest["case_id"],
        "manifest_sha256": hashlib.sha256(MANIFEST_PATH.read_bytes()).hexdigest(),
        "agent_config_sha256": hashlib.sha256(CONFIG_PATH.read_bytes()).hexdigest(),
        "environment_image": f"{manifest['frozen_inputs']['environment_image_reference']}@{digest}",
        "task_id": manifest["frozen_inputs"]["task_id"],
        "model": manifest["frozen_inputs"]["model"],
        "runs": [
            {
                **item,
                "workspace": f"workspaces/{item['release']}-run-{item['repetition']}",
                "trajectory": f"trajectories/{item['release']}-run-{item['repetition']}.traj",
                "outcomes_accessible": False,
            }
            for item in manifest["execution_requirements"]["runs"]
        ],
        "next_gate": "Execute each run in an isolated checkout, then compile trajectories and hash-freeze the primary FAR comparison before outcome reveal.",
    }
    target = OUTPUT_DIR / "execution-plan.json"
    target.write_text(json.dumps(plan, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return target


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("resolve-image", "preflight", "plan"))
    args = parser.parse_args()

    manifest = load_manifest()
    if args.mode == "resolve-image":
        digest = resolve_image_digest(manifest["frozen_inputs"]["environment_image_reference"])
        print(digest)
        return

    preflight(manifest, require_secret=args.mode == "plan")
    digest = verify_frozen_environment(manifest)
    if args.mode == "preflight":
        print("Execution environment and frozen inputs verified. No model call was started.")
        return

    target = write_execution_plan(manifest, digest)
    print(f"Wrote {target}. No benchmark outcome was accessed and no model call was started.")


if __name__ == "__main__":
    main()
