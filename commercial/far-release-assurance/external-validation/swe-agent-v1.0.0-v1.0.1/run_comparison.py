from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
from pathlib import Path

from validate_manifest import validate

CASE_DIR = Path(__file__).parent
MANIFEST_PATH = CASE_DIR / "manifest.json"
CONFIG_PATH = CASE_DIR / "agent-config.yaml"
OUTPUT_DIR = CASE_DIR / "execution-output"
RESOLVED_DIGEST_PATH = CASE_DIR / "resolved-image-digest.txt"
DIGEST_RE = re.compile(r"sha256:[0-9a-f]{64}")


def run(command: list[str], *, cwd: Path | None = None) -> str:
    completed = subprocess.run(command, cwd=cwd, check=True, text=True, capture_output=True)
    return completed.stdout.strip()


def load_manifest() -> dict:
    payload = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    validate(payload)
    return payload


def tagged_reference(reference: str) -> str:
    final = reference.rsplit("/", 1)[-1]
    return reference if (":" in final or "@" in final) else f"{reference}:latest"


def parse_digest(text: str) -> str:
    matches = DIGEST_RE.findall(text)
    unique = list(dict.fromkeys(matches))
    if len(unique) != 1:
        raise ValueError(f"Expected exactly one immutable digest, found {unique!r}")
    return unique[0]


def resolve_image_digest(reference: str) -> str:
    if shutil.which("docker") is None:
        raise SystemExit("Docker is required to resolve the immutable environment image")

    tagged = tagged_reference(reference)
    errors: list[str] = []

    # Primary path: query the registry descriptor without downloading image layers.
    try:
        output = run(["docker", "buildx", "imagetools", "inspect", tagged])
        return parse_digest(output)
    except (subprocess.CalledProcessError, ValueError) as exc:
        errors.append(f"buildx imagetools inspect: {exc}")

    # Independent fallback: Docker manifest inspection also avoids layer downloads.
    try:
        output = run(["docker", "manifest", "inspect", "--verbose", tagged])
        payload = json.loads(output)
        descriptors = payload if isinstance(payload, list) else [payload]
        candidates = []
        for item in descriptors:
            descriptor = item.get("Descriptor", {}) if isinstance(item, dict) else {}
            digest = descriptor.get("digest")
            if isinstance(digest, str):
                candidates.append(digest)
        return parse_digest("\n".join(candidates))
    except (subprocess.CalledProcessError, json.JSONDecodeError, ValueError) as exc:
        errors.append(f"docker manifest inspect: {exc}")

    raise SystemExit(
        "Could not resolve the registry digest without downloading image layers. "
        + " | ".join(errors)
    )


def write_resolved_digest(digest: str) -> Path:
    parse_digest(digest)
    temporary = RESOLVED_DIGEST_PATH.with_suffix(".txt.tmp")
    temporary.write_text(digest + "\n", encoding="utf-8")
    temporary.replace(RESOLVED_DIGEST_PATH)
    persisted = RESOLVED_DIGEST_PATH.read_text(encoding="utf-8").strip()
    if persisted != digest:
        raise SystemExit("Resolved image digest was not persisted exactly")
    return RESOLVED_DIGEST_PATH


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
    secret_name = manifest["execution_requirements"]["required_secret"]
    if require_secret and not os.environ.get(secret_name):
        raise SystemExit(f"{secret_name} is required; no run was started")
    config_hash = hashlib.sha256(CONFIG_PATH.read_bytes()).hexdigest()
    if config_hash != manifest["frozen_inputs"]["agent_config_sha256"]:
        raise SystemExit("agent-config.yaml does not match the frozen hash")


def write_execution_plan(manifest: dict, digest: str) -> Path:
    OUTPUT_DIR.mkdir(exist_ok=True)
    plan = {
        "schema": "far-external-execution-plan/0.2",
        "case_id": manifest["case_id"],
        "manifest_sha256": hashlib.sha256(MANIFEST_PATH.read_bytes()).hexdigest(),
        "agent_config_sha256": hashlib.sha256(CONFIG_PATH.read_bytes()).hexdigest(),
        "environment_image": f"{manifest['frozen_inputs']['environment_image_reference']}@{digest}",
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
    parser.add_argument("mode", choices=("resolve-image", "preflight", "plan"))
    args = parser.parse_args()

    manifest = load_manifest()
    if args.mode == "resolve-image":
        digest = resolve_image_digest(manifest["frozen_inputs"]["environment_image_reference"])
        target = write_resolved_digest(digest)
        print(f"Resolved and persisted {digest} to {target}")
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
