from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

CASE_DIR = Path(__file__).parent
MANIFEST_PATH = CASE_DIR / "manifest.json"
OUTPUT_DIR = CASE_DIR / "execution-output"


def run(command: list[str], *, cwd: Path | None = None) -> str:
    completed = subprocess.run(command, cwd=cwd, check=True, text=True, capture_output=True)
    return completed.stdout.strip()


def resolve_image_digest(reference: str) -> str:
    run(["docker", "pull", reference])
    digest = run(["docker", "image", "inspect", reference, "--format", "{{index .RepoDigests 0}}"])
    if "@sha256:" not in digest:
        raise RuntimeError("Docker did not return an immutable image digest")
    return digest.split("@", 1)[1]


def main() -> None:
    if not os.environ.get("ANTHROPIC_API_KEY"):
        raise SystemExit("ANTHROPIC_API_KEY is required; no run was started")
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    frozen = manifest["frozen_inputs"]
    digest = resolve_image_digest(frozen["environment_image_reference"])
    if frozen["environment_image_digest"] not in (None, digest):
        raise SystemExit("Resolved image digest differs from the frozen digest")
    if frozen["environment_image_digest"] is None:
        raise SystemExit(
            f"Resolved {digest}. Commit this digest to manifest.json and set status to "
            "execution_inputs_frozen before any model call. No run was started."
        )

    OUTPUT_DIR.mkdir(exist_ok=True)
    source_manifest = {
        "case_id": manifest["case_id"],
        "manifest_sha256": hashlib.sha256(MANIFEST_PATH.read_bytes()).hexdigest(),
        "environment_image_digest": digest,
        "runs": manifest["execution_requirements"]["runs"],
    }
    (OUTPUT_DIR / "source-manifest.json").write_text(
        json.dumps(source_manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    print("Execution inputs are fully frozen.")
    print("Run each release in an isolated checkout using agent-config.yaml and preserve raw trajectories.")
    print("Outcome fields remain forbidden until the FAR comparison and primary hash manifest are written.")
    return None


if __name__ == "__main__":
    main()
