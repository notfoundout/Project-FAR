from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import yaml

SUCCESS_STATUSES = {"submitted", "completed", "success", "exit_success"}
ERROR_STATUSES = {"exit_error", "error", "failed", "failure"}
QUOTA_MARKERS = (
    "resource_exhausted",
    "rate limit",
    "ratelimit",
    "quota exceeded",
    "quota exhaustion",
    "too many requests",
    "status code: 429",
    "http 429",
    "request-per-minute",
    "request-per-day",
    "input-token-per-minute",
    "input-token-per-day",
)
RETRYABLE_PROVIDER_MARKERS = (
    "timeout",
    "timed out",
    "temporarily unavailable",
    "service unavailable",
    "connection reset",
    "connection aborted",
    "connection error",
    "gateway timeout",
    "bad gateway",
    "status code: 500",
    "status code: 502",
    "status code: 503",
    "status code: 504",
    "http 500",
    "http 502",
    "http 503",
    "http 504",
)


@dataclass(frozen=True)
class ExecutionOutcome:
    category: str
    state: str
    retryable: bool
    internal_status: str | None
    patch_present: bool
    no_change_submission: bool
    reason: str
    evidence: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def _read_yaml_mapping(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise ValueError(f"missing internal status file: {path}")
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"internal status file is not a mapping: {path}")
    return value


def _normalize_instance_lists(value: Any) -> dict[str, list[str]]:
    if not isinstance(value, dict):
        raise ValueError("instances_by_exit_status is missing or not a mapping")
    normalized: dict[str, list[str]] = {}
    for status, instances in value.items():
        if not isinstance(status, str) or not isinstance(instances, list) or not all(isinstance(item, str) for item in instances):
            raise ValueError("instances_by_exit_status contains malformed entries")
        normalized[status] = instances
    return normalized


def parse_internal_status(path: Path, task_id: str) -> tuple[str, dict[str, Any]]:
    payload = _read_yaml_mapping(path)
    groups = _normalize_instance_lists(payload.get("instances_by_exit_status"))
    matches = [status for status, instances in groups.items() if task_id in instances]
    if len(matches) != 1:
        raise ValueError(f"target instance must appear in exactly one internal status group; found {matches}")
    return matches[0], payload


def _extract_patch(value: Any, task_id: str) -> tuple[str | None, bool]:
    if isinstance(value, dict):
        if "model_patch" in value:
            patch = value.get("model_patch")
            no_change = bool(value.get("no_change") is True or value.get("submission_type") == "no_change")
            return patch if isinstance(patch, str) else None, no_change
        if task_id in value:
            return _extract_patch(value[task_id], task_id)
        if "predictions" in value:
            return _extract_patch(value["predictions"], task_id)
    if isinstance(value, list):
        matches = [item for item in value if isinstance(item, dict) and item.get("instance_id") == task_id]
        if len(matches) == 1:
            return _extract_patch(matches[0], task_id)
    return None, False


def read_prediction(swe_output: Path, task_id: str) -> tuple[str | None, bool, str]:
    candidates = sorted(swe_output.rglob("*.pred"))
    exact = [path for path in candidates if path.stem == task_id]
    ordered = exact + [path for path in candidates if path not in exact]
    for path in [*ordered, *sorted(swe_output.rglob("preds.json"))]:
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        patch, no_change = _extract_patch(value, task_id)
        if patch is not None or no_change:
            return patch, no_change, str(path)
    return None, False, ""


def classify_execution(
    *,
    outer_returncode: int,
    swe_output: Path,
    task_id: str,
    stdout: str,
    stderr: str,
    allow_no_change: bool = False,
) -> ExecutionOutcome:
    combined = (stdout + "\n" + stderr).lower()
    quota_detected = any(marker in combined for marker in QUOTA_MARKERS)
    retryable_provider_detected = any(marker in combined for marker in RETRYABLE_PROVIDER_MARKERS)
    status_files = sorted(swe_output.rglob("run_batch_exit_statuses.yaml"))
    base_evidence: dict[str, Any] = {
        "outer_returncode": outer_returncode,
        "status_files": [str(path) for path in status_files],
    }

    if len(status_files) != 1:
        if quota_detected:
            return ExecutionOutcome(
                "provider_quota_exhaustion", "failed_retryable", True, None, False, False,
                "provider quota exhaustion detected before a unique internal status file was available", base_evidence,
            )
        if retryable_provider_detected:
            return ExecutionOutcome(
                "retryable_provider_error", "failed_retryable", True, None, False, False,
                "retryable provider/model error detected before a unique internal status file was available", base_evidence,
            )
        return ExecutionOutcome(
            "terminal_agent_error", "failed_terminal", False, None, False, False,
            f"expected exactly one run_batch_exit_statuses.yaml, found {len(status_files)}", base_evidence,
        )

    try:
        internal_status, status_payload = parse_internal_status(status_files[0], task_id)
    except ValueError as exc:
        evidence = {**base_evidence, "status_file": str(status_files[0])}
        if quota_detected:
            return ExecutionOutcome(
                "provider_quota_exhaustion", "failed_retryable", True, None, False, False,
                "provider quota exhaustion detected with malformed internal status evidence", evidence,
            )
        if retryable_provider_detected:
            return ExecutionOutcome(
                "retryable_provider_error", "failed_retryable", True, None, False, False,
                "retryable provider/model error detected with malformed internal status evidence", evidence,
            )
        return ExecutionOutcome(
            "terminal_agent_error", "failed_terminal", False, None, False, False, str(exc), evidence,
        )

    patch, no_change, prediction_path = read_prediction(swe_output, task_id)
    patch_present = isinstance(patch, str) and bool(patch.strip())
    evidence = {
        "outer_returncode": outer_returncode,
        "status_file": str(status_files[0]),
        "internal_status": internal_status,
        "prediction_path": prediction_path or None,
        "patch_present": patch_present,
        "no_change_submission": no_change,
        "internal_summary": status_payload,
    }

    if quota_detected:
        return ExecutionOutcome("provider_quota_exhaustion", "failed_retryable", True, internal_status, patch_present, no_change, "provider quota exhaustion detected", evidence)
    if retryable_provider_detected:
        return ExecutionOutcome("retryable_provider_error", "failed_retryable", True, internal_status, patch_present, no_change, "retryable provider/model error detected", evidence)
    if internal_status in ERROR_STATUSES:
        return ExecutionOutcome("terminal_agent_error", "failed_terminal", False, internal_status, patch_present, no_change, "SWE-agent reported an internal error", evidence)
    if internal_status not in SUCCESS_STATUSES:
        return ExecutionOutcome("terminal_agent_error", "failed_terminal", False, internal_status, patch_present, no_change, "unrecognized or non-success SWE-agent status", evidence)
    if outer_returncode != 0:
        return ExecutionOutcome("terminal_agent_error", "failed_terminal", False, internal_status, patch_present, no_change, f"outer process returned {outer_returncode} despite a success-like internal status", evidence)
    if patch_present:
        return ExecutionOutcome("success_with_patch", "complete", False, internal_status, True, False, "successful internal status with non-empty patch", evidence)
    if no_change and allow_no_change:
        return ExecutionOutcome("valid_no_change", "complete", False, internal_status, False, True, "protocol-permitted no-change submission", evidence)
    return ExecutionOutcome("terminal_agent_error", "failed_terminal", False, internal_status, False, no_change, "successful status without a non-empty patch or permitted no-change declaration", evidence)
