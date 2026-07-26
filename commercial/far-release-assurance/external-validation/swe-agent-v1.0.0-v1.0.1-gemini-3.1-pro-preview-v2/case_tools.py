from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

CASE_DIR = Path(__file__).resolve().parent
MANIFEST_PATH = CASE_DIR / "manifest.json"
CONFIG_PATH = CASE_DIR / "agent-config.yaml"
LOCK_PATH = CASE_DIR / "environment-freeze/environment-lock.json"
TASK_PATH = CASE_DIR / "environment-freeze/task-record.public.json"
SHARED_LOCK_PATH = CASE_DIR / "shared-implementation-lock.json"
OUTPUT_DIR = CASE_DIR / "execution-output"
PLAN_PATH = OUTPUT_DIR / "execution-plan.json"
STATUS_PATH = CASE_DIR / "EXECUTION-STATUS.md"

PENDING = "preregistered_access_pending"
FROZEN = "execution_inputs_frozen"
CASE_ID = "swe-agent-v1.0.0-v1.0.1-gemini-3.1-pro-preview-v2"
MODEL = "gemini-3.1-pro-preview"
MODEL_NAME = f"gemini/{MODEL}"
ACCESS_SCHEMA = "far-provider-access-attestation/1.0"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def canonical(value: object) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True) + "\n").encode()


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def blob_sha(path: Path) -> str:
    data = path.read_bytes()
    return hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()


def read_json(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise SystemExit(f"Missing required file: {path}")
    value = json.loads(path.read_text())
    if not isinstance(value, dict):
        raise SystemExit(f"Expected JSON object: {path}")
    return value


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(canonical(value))


def validate_manifest(m: dict[str, Any]) -> None:
    if m.get("schema") != "far-external-release-comparison/0.4":
        raise SystemExit("Manifest schema mismatch")
    if m.get("case_id") != CASE_ID or m.get("status") not in {PENDING, FROZEN}:
        raise SystemExit("Manifest case or status mismatch")
    source = m.get("source", {})
    expected_source = {
        "baseline_ref": "v1.0.0",
        "baseline_commit": "8ed382c",
        "candidate_ref": "v1.0.1",
        "candidate_commit": "6aff215",
    }
    if any(source.get(k) != v for k, v in expected_source.items()):
        raise SystemExit("Frozen SWE-agent source drift")
    frozen = m.get("frozen_inputs", {})
    if frozen.get("model") != MODEL_NAME or frozen.get("provider_model") != MODEL:
        raise SystemExit("Exact replacement model drift")
    if frozen.get("task_id") != "scikit-learn__scikit-learn-14125":
        raise SystemExit("Frozen task drift")
    if frozen.get("immutable_image_reference") != (
        "ghcr.io/notfoundout/project-far-swebench-scikit-learn-14125"
        "@sha256:66615e837a9fdc6faf75dab3db90bf469364204b068af9da4d570fba8ab00ab4"
    ):
        raise SystemExit("Frozen image drift")
    expected_runs = [
        ("v1.0.0", "8ed382c", 1, "baseline-run-1.traj"),
        ("v1.0.0", "8ed382c", 2, "baseline-run-2.traj"),
        ("v1.0.1", "6aff215", 1, "candidate-run-1.traj"),
        ("v1.0.1", "6aff215", 2, "candidate-run-2.traj"),
    ]
    runs = m.get("execution_requirements", {}).get("runs", [])
    actual = [
        (x.get("release"), x.get("commit"), x.get("repetition"), x.get("trajectory_artifact"))
        for x in runs if isinstance(x, dict)
    ]
    if actual != expected_runs:
        raise SystemExit("Fresh four-run matrix drift")
    old = m.get("supersedes_case", {})
    if old.get("case_id") != "swe-agent-v1.0.0-v1.0.1" or old.get("disposition") != "BLOCKED":
        raise SystemExit("Prior blocked case is not preserved")
    gate = m.get("provider_access_gate", {})
    if gate.get("probe_model") != MODEL:
        raise SystemExit("Access probe model drift")
    if not all(gate.get(k) is True for k in (
        "benchmark_task_data_forbidden",
        "benchmark_outcomes_forbidden",
        "credential_persistence_forbidden",
    )):
        raise SystemExit("Access probe safety boundary weakened")
    bound = [gate.get("attestation_path"), gate.get("attestation_sha256"), gate.get("verified_at")]
    if m["status"] == PENDING and any(x is not None for x in bound):
        raise SystemExit("Pending case contains premature attestation")
    if m["status"] == FROZEN and not all(isinstance(x, str) and x for x in bound):
        raise SystemExit("Frozen case lacks attestation binding")


def load_manifest() -> dict[str, Any]:
    m = read_json(MANIFEST_PATH)
    validate_manifest(m)
    return m


def verify_shared_implementation() -> None:
    lock = read_json(SHARED_LOCK_PATH)
    if lock.get("schema") != "far-shared-controller-lock/1.0":
        raise SystemExit("Shared implementation lock schema mismatch")
    root = (CASE_DIR / lock["source_case_path"]).resolve()
    for rel, expected in sorted(lock.get("files", {}).items()):
        path = root / rel
        if not path.is_file() or blob_sha(path) != expected:
            raise SystemExit(f"Shared implementation blob drift: {rel}")


def validate_attestation(m: dict[str, Any], required: bool) -> dict[str, Any] | None:
    if m["status"] == PENDING:
        return None
    gate = m["provider_access_gate"]
    path = CASE_DIR / gate["attestation_path"]
    if required and not path.is_file():
        raise SystemExit("Provider access attestation is missing")
    if not path.is_file():
        return None
    if sha256_file(path) != gate["attestation_sha256"]:
        raise SystemExit("Provider access attestation hash mismatch")
    a = read_json(path)
    expected = {
        "schema": ACCESS_SCHEMA,
        "case_id": CASE_ID,
        "requested_model": MODEL,
        "http_status": 200,
        "exact_response": True,
        "probe_is_nonbenchmark": True,
        "benchmark_task_data_accessed": False,
        "benchmark_outcomes_accessed": False,
        "api_key_persisted": False,
    }
    if any(a.get(k) != v for k, v in expected.items()):
        raise SystemExit("Provider access attestation contract mismatch")
    if a.get("prompt_sha256") != gate["probe_prompt_sha256"]:
        raise SystemExit("Provider access probe prompt mismatch")
    return a


def validate_repository(require_frozen: bool = False) -> dict[str, Any]:
    m = load_manifest()
    if require_frozen and m["status"] != FROZEN:
        raise SystemExit("Merge the successful provider-access freeze PR first")
    if sha256_file(CONFIG_PATH) != m["frozen_inputs"]["agent_config_sha256"]:
        raise SystemExit("Agent configuration hash mismatch")
    if sha256_file(LOCK_PATH) != m["frozen_inputs"]["environment_lock_sha256"]:
        raise SystemExit("Environment lock hash mismatch")
    lock, task = read_json(LOCK_PATH), read_json(TASK_PATH)
    if lock.get("file_sha256", {}).get("task-record.public.json") != sha256_file(TASK_PATH):
        raise SystemExit("Public task record hash mismatch")
    if task.get("outcome_fields_included") is not False:
        raise SystemExit("Public task record includes outcomes")
    if lock.get("outcome_data_exported") is not False or lock.get("model_call_started") is not False:
        raise SystemExit("Environment outcome/model boundary violated")
    verify_shared_implementation()
    validate_attestation(m, require_frozen)
    return m


def access_probe() -> Path:
    m = validate_repository()
    if m["status"] != PENDING:
        raise SystemExit("Access probe is only valid before freeze")
    key = os.environ.get("GEMINI_API_KEY", "")
    if not key:
        raise SystemExit("GEMINI_API_KEY is required for the access probe")
    gate = m["provider_access_gate"]
    prompt = gate["probe_prompt"]
    if sha256_bytes(prompt.encode()) != gate["probe_prompt_sha256"]:
        raise SystemExit("Preregistered probe prompt hash mismatch")
    body = {
        "contents": [{"role": "user", "parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.0, "maxOutputTokens": 16},
    }
    request = urllib.request.Request(
        gate["probe_endpoint"],
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json", "x-goog-api-key": key},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            status = int(response.status)
            payload = json.loads(response.read().decode())
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode(errors="replace")
        try:
            error = json.loads(raw).get("error", {})
        except json.JSONDecodeError:
            error = {"message": raw[:1000]}
        failure = {
            "schema": "far-provider-access-probe-failure/1.0",
            "case_id": CASE_ID,
            "requested_model": MODEL,
            "observed_at": now(),
            "http_status": int(exc.code),
            "provider_error": {
                "code": error.get("code"),
                "status": error.get("status"),
                "message": str(error.get("message", ""))[:1000],
            },
            "api_key_persisted": False,
            "probe_is_nonbenchmark": True,
            "benchmark_task_data_accessed": False,
            "benchmark_outcomes_accessed": False,
        }
        target = OUTPUT_DIR / "access-probe-failure.json"
        write_json(target, failure)
        raise SystemExit(f"Exact model access probe failed with HTTP {exc.code}") from None
    parts = payload.get("candidates", [{}])[0].get("content", {}).get("parts", [])
    text = "".join(str(p.get("text", "")) for p in parts if isinstance(p, dict)).strip()
    expected = gate["required_exact_response"]
    if status != 200 or text != expected:
        raise SystemExit("Provider response did not satisfy the exact access contract")
    a = {
        "schema": ACCESS_SCHEMA,
        "case_id": CASE_ID,
        "requested_model": MODEL,
        "provider_endpoint": gate["probe_endpoint"],
        "observed_at": now(),
        "http_status": status,
        "provider_model_version": payload.get("modelVersion"),
        "prompt_sha256": gate["probe_prompt_sha256"],
        "expected_response": expected,
        "response_text_sha256": sha256_bytes(text.encode()),
        "exact_response": True,
        "probe_is_nonbenchmark": True,
        "benchmark_task_data_accessed": False,
        "benchmark_outcomes_accessed": False,
        "api_key_persisted": False,
    }
    target = CASE_DIR / "access-freeze/provider-access-attestation.json"
    write_json(target, a)
    (target.parent / "provider-access-attestation.sha256").write_text(sha256_file(target) + "\n")
    print(f"Exact {MODEL} access verified with a fixed non-benchmark probe.")
    return target


def status_text(a: dict[str, Any]) -> str:
    return f"""# SWE-agent External Comparison v2 Execution Status

- Exact `gemini-3.1-pro-preview` access verified at `{a['observed_at']}`.
- The prior `gemini-2.5-pro` case remains `BLOCKED` and unchanged.
- The v2 task, releases, model, parameters, environment, repetitions, and order are frozen.
- All four v2 slots are untouched and pending.
- No benchmark outcome was accessed.
- No v2 model execution has started.

Planning does not require or read `GEMINI_API_KEY`. Execute one frozen slot at a time only after this freeze is merged. Results may not be pooled with the blocked earlier case.
"""


def finalize_access_freeze() -> None:
    m = validate_repository()
    target = CASE_DIR / "access-freeze/provider-access-attestation.json"
    if m["status"] != PENDING or not target.is_file():
        raise SystemExit("Successful pending access attestation is required")
    a = read_json(target)
    m["status"] = FROZEN
    gate = m["provider_access_gate"]
    gate["attestation_path"] = str(target.relative_to(CASE_DIR))
    gate["attestation_sha256"] = sha256_file(target)
    gate["verified_at"] = a.get("observed_at")
    m["execution_freeze"] = {
        "schema": "far-execution-input-freeze/1.0",
        "frozen_at": now(),
        "trigger": "successful_exact_provider_access_probe",
        "provider_access_attestation_sha256": sha256_file(target),
        "fresh_run_matrix_required": True,
        "prior_case_state_imported": False,
    }
    validate_manifest(m)
    write_json(MANIFEST_PATH, m)
    validate_repository(require_frozen=True)
    STATUS_PATH.write_text(status_text(a))
    print("Execution inputs frozen; four v2 slots remain untouched.")


def environment_lock(m: dict[str, Any]) -> dict[str, Any]:
    lock = read_json(LOCK_PATH)
    expected = {
        "local_image_id": m["frozen_inputs"]["local_image_id"],
        "immutable_image_reference": m["frozen_inputs"]["immutable_image_reference"],
        "registry_digest": m["frozen_inputs"]["registry_digest"],
        "task_id": m["frozen_inputs"]["task_id"],
        "swebench_harness_commit": m["frozen_inputs"]["swebench_harness_commit"],
        "cross_runner_portable": True,
        "outcome_data_exported": False,
        "model_call_started": False,
    }
    if any(lock.get(k) != v for k, v in expected.items()):
        raise SystemExit("Environment lock drift")
    return lock


def pull_image(lock: dict[str, Any]) -> None:
    if shutil.which("docker") is None:
        raise SystemExit("Docker is required")
    ref = lock["immutable_image_reference"]
    subprocess.run(["docker", "pull", ref], check=True)
    result = subprocess.run(
        ["docker", "image", "inspect", ref, "--format", "{{json .RepoDigests}}"],
        check=True, text=True, capture_output=True,
    )
    if ref not in json.loads(result.stdout.strip()):
        raise SystemExit("Pulled image does not expose frozen digest")


def preflight(with_image: bool) -> None:
    m = validate_repository(require_frozen=True)
    lock = environment_lock(m)
    if with_image:
        pull_image(lock)
    print("Frozen v2 inputs and outcome-blind boundaries verified; no model call started.")


def build_plan(m: dict[str, Any], lock: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema": "far-external-execution-plan/0.4",
        "case_id": m["case_id"],
        "manifest_sha256": sha256_file(MANIFEST_PATH),
        "agent_config_sha256": sha256_file(CONFIG_PATH),
        "environment_lock_sha256": sha256_file(LOCK_PATH),
        "provider_access_attestation_sha256": m["provider_access_gate"]["attestation_sha256"],
        "immutable_image_reference": lock["immutable_image_reference"],
        "registry_digest": lock["registry_digest"],
        "task_id": m["frozen_inputs"]["task_id"],
        "model": m["frozen_inputs"]["model"],
        "free_tier": False,
        "provider_billing_may_apply": True,
        "maximum_model_cost_usd": 0.0,
        "cost_field_note": "Compatibility value; not a claim that provider execution is free.",
        "sequential_only": True,
        "quota_policy": "Retry only evidence-supported transient failures; never substitute a model.",
        "runs": [
            {
                **x,
                "workspace": f"workspaces/{x['release']}-run-{x['repetition']}",
                "trajectory": f"trajectories/{x['trajectory_artifact']}",
                "outcomes_accessible": False,
                "state": "pending",
            }
            for x in m["execution_requirements"]["runs"]
        ],
        "next_gate": "Execute one slot at a time and freeze primary evidence before outcome reveal.",
    }


def plan() -> Path:
    m = validate_repository(require_frozen=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    write_json(PLAN_PATH, build_plan(m, environment_lock(m)))
    print(f"Wrote {PLAN_PATH}; no key, model call, or benchmark outcome was used.")
    return PLAN_PATH


def main() -> None:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("validate")
    sub.add_parser("access-probe")
    sub.add_parser("finalize-access-freeze")
    p = sub.add_parser("preflight")
    p.add_argument("--pull-image", action="store_true")
    sub.add_parser("plan")
    args = parser.parse_args()
    if args.command == "validate":
        m = validate_repository()
        print(json.dumps({"case_id": m["case_id"], "status": m["status"], "model": m["frozen_inputs"]["model"]}, indent=2))
    elif args.command == "access-probe":
        access_probe()
    elif args.command == "finalize-access-freeze":
        finalize_access_freeze()
    elif args.command == "preflight":
        preflight(args.pull_image)
    else:
        plan()


if __name__ == "__main__":
    main()
