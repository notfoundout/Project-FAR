"""Defense-in-depth verifier for PR #435 review-closure contracts."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
import verify_amendment_v1_1 as amendment
import verify_integrity as integrity

DesignError = integrity.DesignError
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SEED = HERE / "bootstrap-seed-commitment-contract-v1.0.json"
TASK = HERE / "task-manifest-contract-v1.0.json"
GATE = HERE / "execution-gate-v1.0.json"

SEED_BLOB = "e5a9b94a0ccbce383cfbc7237d98e400af9d853d"
TASK_BLOB = "02f12f061a0dcfa61212b27c40ce9a12bdb2c9a0"
CAPSULE_BLOB = "e011c8f9972a5682e03526f739437f62e973e76d"
GATE_BLOB = "99eabd1fee9a59770a3a61a07c151abcba23683f"
RECORD_SCHEMA_DIGEST = "f50dd9a937e3b09a23cb368f92c2c3d03c2e9671677657ab245864a78093fa11"
TASK_BUNDLE_ROOT_DIGEST = "a80bcfddd677cf601b93f47fc1aafa381cd7ca8c16c0ab49834cb3f887dba4ee"
REPOSITORY_IDENTITY_DIGEST = "5f0bd3495437391a2e1f1b57eaba93a5411c718eae49587ce3e66a1aac47a5e3"
SEED_HEX = "76764013d297cadd3865295298e160a9fbb1a39833aac5860b0dfb13f54fdf87"
SEED_PAYLOAD = (
    "FAR-SWE-V3-001/bootstrap-seed/v1\n"
    "treatment_capsule_git_blob_sha1=e011c8f9972a5682e03526f739437f62e973e76d\n"
    "execution_gate_git_blob_sha1=99eabd1fee9a59770a3a61a07c151abcba23683f\n"
)


def _blob(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


def _digest(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False).encode("utf-8")).hexdigest()


def _require_current_blob(relative: str, expected: str) -> bytes:
    committed = integrity._committed_blob_bytes(relative)
    if _blob(committed) != expected:
        raise DesignError(f"committed blob identity drifted: {relative}")
    return committed


def verify_task_identity_contract(path: Path = TASK) -> None:
    raw = integrity._read_regular(path)
    if _blob(raw) != TASK_BLOB:
        raise DesignError("task manifest contract bytes drifted")
    data = integrity._decode_json(raw, str(path))
    if not isinstance(data, dict):
        raise DesignError("task manifest contract must be object")
    if _digest(data.get("record_schema")) != RECORD_SCHEMA_DIGEST:
        raise DesignError("complete task record schema drifted")
    if _digest(data.get("task_bundle_root_contract")) != TASK_BUNDLE_ROOT_DIGEST:
        raise DesignError("complete task-bundle root contract drifted")
    if _digest(data.get("repository_identity_contract")) != REPOSITORY_IDENTITY_DIGEST:
        raise DesignError("complete repository identity contract drifted")


def verify_seed_contract(path: Path = SEED) -> None:
    raw = integrity._read_regular(path)
    if _blob(raw) != SEED_BLOB:
        raise DesignError("bootstrap seed commitment bytes drifted")
    data = integrity._decode_json(raw, str(path))
    if not isinstance(data, dict):
        raise DesignError("bootstrap seed commitment must be object")
    if (data.get("schema_version"), data.get("program_id"), data.get("artifact_status"), data.get("commitment_status")) != (
        "1.0", "FAR-SWE-V3-001", "Research", "frozen_pre_execution"
    ):
        raise DesignError("bootstrap seed commitment identity drifted")

    authority = data.get("authority")
    expected_authority = {
        "base_design_head": "b578239e008617362f66ad5cf069f87b7d0e6d8b",
        "base_preregistration_git_blob_sha1": "c6c9b5399ef2699ddcd2652dbb2acdd8e820bee1",
        "superseded_subject": "/analysis/bootstrap_seed_status",
        "precedence": "This prospective contract freezes the bootstrap seed required by preregistration-v1.0.json; every other preregistration field remains unchanged.",
        "outcome_exposure_status": "none",
        "model_calls_authorized": False,
        "pilot_execution_authorized": False,
        "benchmark_execution_authorized": False,
        "confirmatory_execution_authorized": False,
    }
    if authority != expected_authority:
        raise DesignError("bootstrap seed authority or non-authorization boundary drifted")

    rng = data.get("rng_contract")
    if rng != {
        "procedure_id": "sha256_rejection_stream_v1",
        "seed_encoding": "64 lowercase hexadecimal characters decoded as exactly 32 bytes",
        "seed_hex": SEED_HEX,
    }:
        raise DesignError("bootstrap RNG or committed seed drifted")

    derivation = data.get("derivation")
    if not isinstance(derivation, dict):
        raise DesignError("bootstrap seed derivation missing")
    if derivation.get("method") != "SHA-256 over the exact UTF-8 bytes of canonical_payload":
        raise DesignError("bootstrap seed derivation method drifted")
    if derivation.get("canonical_payload") != SEED_PAYLOAD:
        raise DesignError("bootstrap seed canonical payload drifted")
    if hashlib.sha256(SEED_PAYLOAD.encode("utf-8")).hexdigest() != SEED_HEX:
        raise DesignError("bootstrap seed recomputation failed")
    if derivation.get("sha256") != SEED_HEX:
        raise DesignError("bootstrap seed digest record drifted")
    if derivation.get("outcome_or_grade_inputs_permitted") is not False or derivation.get("task_identity_inputs_permitted") is not False:
        raise DesignError("post-outcome or task-identity seed inputs were enabled")
    if derivation.get("inputs") != [
        {"path": "research/external-validation/swe-agent-v3/treatment-capsule-contract-v1.0.json", "git_blob_sha1": CAPSULE_BLOB},
        {"path": "research/external-validation/swe-agent-v3/execution-gate-v1.0.json", "git_blob_sha1": GATE_BLOB},
    ]:
        raise DesignError("bootstrap seed input identity drifted")

    _require_current_blob("research/external-validation/swe-agent-v3/treatment-capsule-contract-v1.0.json", CAPSULE_BLOB)
    _require_current_blob("research/external-validation/swe-agent-v3/execution-gate-v1.0.json", GATE_BLOB)
    timing = data.get("timing")
    if not isinstance(timing, dict) or set(timing) != {
        "must_be_committed_and_integrity_rooted_before_any_sacrificial_pilot_execution",
        "must_be_committed_and_integrity_rooted_before_any_confirmatory_execution",
        "must_precede_any_pilot_or_confirmatory_outcome_reveal",
        "immutable_after_commitment",
    } or any(value is not True for value in timing.values()):
        raise DesignError("bootstrap seed timing contract drifted")


def verify_gate_closed(path: Path = GATE) -> None:
    data = integrity._load_json(path)
    for key in (
        "execution_authorized", "model_calls_authorized", "benchmark_execution_authorized",
        "pilot_execution_authorized", "confirmatory_execution_authorized",
    ):
        if data.get(key) is not False:
            raise DesignError(f"execution gate opened: {key}")


def verify() -> None:
    integrity.ROOT = ROOT
    integrity.HERE = HERE
    verify_task_identity_contract()
    verify_seed_contract()
    amendment.validate()
    verify_gate_closed()


if __name__ == "__main__":
    try:
        verify()
    except (DesignError, amendment.AmendmentError) as exc:
        raise SystemExit(f"FAIL: {exc}")
    print("PASS: PR #435 review-closure contracts are exact, prospective, and execution remains blocked.")
