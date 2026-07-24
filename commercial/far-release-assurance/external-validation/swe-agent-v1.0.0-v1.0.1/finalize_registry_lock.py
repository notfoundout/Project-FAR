from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

CASE_DIR = Path(__file__).parent
FREEZE_DIR = CASE_DIR / "execution-output" / "environment-freeze"
LOCK_PATH = FREEZE_DIR / "environment-lock.json"
SIDECAR_PATH = FREEZE_DIR / "environment-lock.sha256"
DIGEST_RE = re.compile(r"^sha256:[0-9a-f]{64}$")


def canonical_json(value: object) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8")


def finalize(reference: str, digest: str) -> dict:
    if not reference.startswith("ghcr.io/") or "@" in reference or ":" in reference.removeprefix("ghcr.io/"):
        raise SystemExit(f"Malformed GHCR repository reference: {reference!r}")
    if not DIGEST_RE.fullmatch(digest):
        raise SystemExit(f"Malformed immutable image digest: {digest!r}")
    if not LOCK_PATH.is_file():
        raise SystemExit(f"Missing environment lock: {LOCK_PATH}")

    lock = json.loads(LOCK_PATH.read_text(encoding="utf-8"))
    if lock.get("model_call_started") is not False:
        raise SystemExit("Cannot finalize a lock after model execution started")
    if lock.get("outcome_data_exported") is not False:
        raise SystemExit("Cannot publish a lock that exported outcome-bearing data")

    lock["schema"] = "far-swebench-environment-lock/1.2"
    lock["registry_repository"] = reference
    lock["registry_digest"] = digest
    lock["immutable_image_reference"] = f"{reference}@{digest}"
    lock["cross_runner_portable"] = True

    payload = canonical_json(lock)
    LOCK_PATH.write_bytes(payload)
    SIDECAR_PATH.write_text(hashlib.sha256(payload).hexdigest() + "\n", encoding="utf-8")
    return lock


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--reference", required=True)
    parser.add_argument("--digest", required=True)
    args = parser.parse_args()
    lock = finalize(args.reference, args.digest)
    print(json.dumps(lock, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
