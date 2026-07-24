from __future__ import annotations

import hashlib
import json
import os
import subprocess
from pathlib import Path

import docker
from datasets import load_dataset
from swebench.harness.docker_build import build_instance_images
from swebench.harness.test_spec.test_spec import make_test_spec

CASE_DIR = Path(__file__).parent
OUTPUT_DIR = CASE_DIR / "execution-output" / "environment-freeze"
MANIFEST_PATH = CASE_DIR / "manifest.json"


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def canonical_json(value: object) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8")


def one_task(dataset_name: str, split: str, task_id: str) -> dict:
    dataset = load_dataset(dataset_name, split=split)
    matches = [dict(row) for row in dataset if row.get("instance_id") == task_id]
    if len(matches) != 1:
        raise SystemExit(f"Expected exactly one task record for {task_id}, found {len(matches)}")
    return matches[0]


def main() -> None:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    frozen = manifest["frozen_inputs"]
    task_id = frozen["task_id"]
    dataset_name = frozen["swebench_dataset"]
    dataset_split = frozen["swebench_split"]
    expected_harness = frozen["swebench_harness_commit"]

    harness_dir = Path(os.environ.get("SWEBENCH_HARNESS_DIR", "")).resolve()
    if not harness_dir.is_dir():
        raise SystemExit("SWEBENCH_HARNESS_DIR must point to the pinned SWE-bench checkout")
    actual_harness = subprocess.run(
        ["git", "-C", str(harness_dir), "rev-parse", "HEAD"],
        check=True,
        text=True,
        capture_output=True,
    ).stdout.strip()
    if actual_harness != expected_harness:
        raise SystemExit(f"SWE-bench harness mismatch: expected {expected_harness}, got {actual_harness}")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    record = one_task(dataset_name, dataset_split, task_id)
    task_bytes = canonical_json(record)
    (OUTPUT_DIR / "task-record.json").write_bytes(task_bytes)

    spec = make_test_spec(record, namespace=None, instance_image_tag="far-frozen", env_image_tag="far-frozen")
    spec_summary = {
        "instance_id": spec.instance_id,
        "platform": spec.platform,
        "base_image_key": spec.base_image_key,
        "env_image_key": spec.env_image_key,
        "instance_image_key": spec.instance_image_key,
    }
    (OUTPUT_DIR / "test-spec.json").write_bytes(canonical_json(spec_summary))
    (OUTPUT_DIR / "Dockerfile.base").write_text(spec.base_dockerfile, encoding="utf-8")
    (OUTPUT_DIR / "Dockerfile.env").write_text(spec.env_dockerfile, encoding="utf-8")
    (OUTPUT_DIR / "Dockerfile.instance").write_text(spec.instance_dockerfile, encoding="utf-8")
    (OUTPUT_DIR / "setup-env.sh").write_text(spec.setup_env_script, encoding="utf-8")
    (OUTPUT_DIR / "setup-repo.sh").write_text(spec.setup_repo_script, encoding="utf-8")

    client = docker.from_env()
    successful, failed = build_instance_images(
        client,
        [record],
        force_rebuild=True,
        max_workers=1,
        namespace=None,
        tag="far-frozen",
        env_image_tag="far-frozen",
    )
    if failed or spec.instance_image_key not in successful:
        raise SystemExit(f"Local SWE-bench image build failed: successful={successful!r}, failed={failed!r}")

    image_id = client.images.get(spec.instance_image_key).id
    if not image_id.startswith("sha256:") or len(image_id) != 71:
        raise SystemExit(f"Malformed local image ID: {image_id!r}")

    files = sorted(path for path in OUTPUT_DIR.iterdir() if path.is_file())
    file_hashes = {path.name: sha256_bytes(path.read_bytes()) for path in files}
    lock = {
        "schema": "far-swebench-local-environment-lock/1.0",
        "task_id": task_id,
        "dataset": dataset_name,
        "split": dataset_split,
        "swebench_harness_commit": actual_harness,
        "image_key": spec.instance_image_key,
        "local_image_id": image_id,
        "platform": spec.platform,
        "file_sha256": file_hashes,
        "outcome_data_accessed": False,
        "model_call_started": False
    }
    lock_bytes = canonical_json(lock)
    (OUTPUT_DIR / "environment-lock.json").write_bytes(lock_bytes)
    (OUTPUT_DIR / "environment-lock.sha256").write_text(sha256_bytes(lock_bytes) + "\n", encoding="utf-8")
    print(json.dumps(lock, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
