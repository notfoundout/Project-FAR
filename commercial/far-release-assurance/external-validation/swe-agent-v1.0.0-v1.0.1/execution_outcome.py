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
    try:
        value = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        raise ValueError(f"cannot parse internal status file: {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ValueError(f"internal status file is not a mapping: {path}")
    return value


def _normalize_instance_lists(value: Any) -> dict[str, list[str]]:
    if not isinstance(value, dict):
        raise ValueError("instances_by_exit_status is missing or not a mapping")
    normalized: dict[str, list[str]] = {}
    for status, instances in value.items():
        if (
            not isinstance(status, str)
            or not isinstance(instances, list)
            or not all(isinstance(item, str) for item in instances)
        ):
            raise ValueError("instances_by_exit_status contains malformed entries")
        normalized[status] = instances
    return normalized


def parse_internal_status(path: Path, task_id: str) -> tuple[str, dict[str, Any]]:
    payload = _read_yaml_mapping(path)
    groups = _normalize_instance_lists(payload.get("instances_by_exit_status"))
    matches = [status for status, instances in groups.items() if task_id in instances]
    if len(matches) != 1:
        raise ValueError(
            f"target instance must appear in exactly one internal status group; found {matches}"
        )
    return matches[0], payload


def _extract_prediction(
    value: Any,
    task_id: str,
    *,
    allow_implicit_instance: bool,
    target_bound: bool = False,
) -> tuple[bool, str | None, bool]:
    if isinstance(value, dict):
        if (
            (value.get("instance_id") == task_id or target_bound)
            and "model_patch" not in value
        ):
            raise ValueError(
                "prediction for target instance is missing model_patch"
            )
        if "model_patch" in value:
            instance_id = value.get("instance_id")
            if instance_id is not None and instance_id != task_id:
                return False, None, False
            if instance_id is None and not allow_implicit_instance:
                return False, None, False
            patch = value.get("model_patch")
            if patch is not None and not isinstance(patch, str):
                raise ValueError("prediction model_patch must be a string or null")
            no_change = bool(
                value.get("no_change") is True
                or value.get("submission_type") == "no_change"
            )
            if isinstance(patch, str) and patch.strip() and no_change:
                raise ValueError(
                    "prediction cannot contain both a non-empty patch and no-change"
                )
            return True, patch if isinstance(patch, str) else None, no_change
        if task_id in value:
            return _extract_prediction(
                value[task_id],
                task_id,
                allow_implicit_instance=True,
                target_bound=True,
            )
        if "predictions" in value:
            return _extract_prediction(
                value["predictions"], task_id, allow_implicit_instance=False
            )
    if isinstance(value, list):
        matches = [
            item
            for item in value
            if isinstance(item, dict) and item.get("instance_id") == task_id
        ]
        if len(matches) > 1:
            raise ValueError("prediction collection contains duplicate target entries")
        if len(matches) == 1:
            return _extract_prediction(
                matches[0], task_id, allow_implicit_instance=True
            )
    return False, None, False


def _read_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise ValueError(f"cannot read prediction file: {path}: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"prediction file is invalid JSON: {path}: {exc}") from exc


def read_prediction(swe_output: Path, task_id: str) -> tuple[str | None, bool, str]:
    prediction_files = sorted(swe_output.rglob("*.pred"))
    aggregate_files = sorted(swe_output.rglob("preds.json"))
    matches: list[tuple[str | None, bool, str]] = []
    target_prediction_files: list[str] = []

    for path in prediction_files:
        found, patch, no_change = _extract_prediction(
            _read_json(path),
            task_id,
            allow_implicit_instance=path.stem == task_id,
        )
        if path.stem == task_id and not found:
            raise ValueError(
                f"exact prediction file does not identify target instance: {path}"
            )
        if not found:
            continue
        target_prediction_files.append(str(path))
        matches.append((patch, no_change, str(path)))

    if len(target_prediction_files) > 1:
        raise ValueError(
            "multiple .pred files identify the target instance: "
            + ", ".join(target_prediction_files)
        )

    for path in aggregate_files:
        found, patch, no_change = _extract_prediction(
            _read_json(path), task_id, allow_implicit_instance=False
        )
        if found:
            matches.append((patch, no_change, str(path)))

    if not matches:
        return None, False, ""

    signatures = {(patch, no_change) for patch, no_change, _ in matches}
    if len(signatures) != 1:
        raise ValueError(
            "conflicting prediction evidence for target instance: "
            + ", ".join(path for _, _, path in matches)
        )
    patch, no_change = next(iter(signatures))
    return patch, no_change, ";".join(path for _, _, path in matches)


def _provider_outcome(
    *,
    quota_detected: bool,
    retryable_provider_detected: bool,
    internal_status: str | None,
    patch_present: bool,
    no_change: bool,
    evidence: dict[str, Any],
    context: str,
) -> ExecutionOutcome | None:
    if quota_detected:
        return ExecutionOutcome(
            "provider_quota_exhaustion",
            "failed_retryable",
            True,
            internal_status,
            patch_present,
            no_change,
            f"provider quota exhaustion detected {context}",
            evidence,
        )
    if retryable_provider_detected:
        return ExecutionOutcome(
            "retryable_provider_error",
            "failed_retryable",
            True,
            internal_status,
            patch_present,
            no_change,
            f"retryable provider/model error detected {context}",
            evidence,
        )
    return None


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
    retryable_provider_detected = any(
        marker in combined for marker in RETRYABLE_PROVIDER_MARKERS
    )
    status_files = sorted(swe_output.rglob("run_batch_exit_statuses.yaml"))
    base_evidence: dict[str, Any] = {
        "outer_returncode": outer_returncode,
        "status_files": [str(path) for path in status_files],
    }

    if len(status_files) != 1:
        provider = _provider_outcome(
            quota_detected=quota_detected,
            retryable_provider_detected=retryable_provider_detected,
            internal_status=None,
            patch_present=False,
            no_change=False,
            evidence=base_evidence,
            context="before a unique internal status file was available",
        )
        if provider is not None:
            return provider
        return ExecutionOutcome(
            "terminal_agent_error",
            "failed_terminal",
            False,
            None,
            False,
            False,
            f"expected exactly one run_batch_exit_statuses.yaml, found {len(status_files)}",
            base_evidence,
        )

    try:
        internal_status, status_payload = parse_internal_status(
            status_files[0], task_id
        )
    except ValueError as exc:
        evidence = {**base_evidence, "status_file": str(status_files[0])}
        provider = _provider_outcome(
            quota_detected=quota_detected,
            retryable_provider_detected=retryable_provider_detected,
            internal_status=None,
            patch_present=False,
            no_change=False,
            evidence=evidence,
            context="with malformed internal status evidence",
        )
        if provider is not None:
            return provider
        return ExecutionOutcome(
            "terminal_agent_error",
            "failed_terminal",
            False,
            None,
            False,
            False,
            str(exc),
            evidence,
        )

    try:
        patch, no_change, prediction_path = read_prediction(swe_output, task_id)
    except ValueError as exc:
        evidence = {
            "outer_returncode": outer_returncode,
            "status_file": str(status_files[0]),
            "internal_status": internal_status,
            "prediction_error": str(exc),
            "internal_summary": status_payload,
        }
        provider = _provider_outcome(
            quota_detected=quota_detected,
            retryable_provider_detected=retryable_provider_detected,
            internal_status=internal_status,
            patch_present=False,
            no_change=False,
            evidence=evidence,
            context="before valid prediction evidence was available",
        )
        if provider is not None:
            return provider
        return ExecutionOutcome(
            "terminal_agent_error",
            "failed_terminal",
            False,
            internal_status,
            False,
            False,
            str(exc),
            evidence,
        )

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

    # Final validated success outranks transient provider errors emitted during
    # retries. Provider markers only control classification when the final
    # status, return code, or prediction evidence is not successful.
    if internal_status in SUCCESS_STATUSES and outer_returncode == 0:
        if patch_present:
            return ExecutionOutcome(
                "success_with_patch",
                "complete",
                False,
                internal_status,
                True,
                False,
                "successful internal status with non-empty patch",
                evidence,
            )
        if no_change and allow_no_change:
            return ExecutionOutcome(
                "valid_no_change",
                "complete",
                False,
                internal_status,
                False,
                True,
                "protocol-permitted no-change submission",
                evidence,
            )

    provider = _provider_outcome(
        quota_detected=quota_detected,
        retryable_provider_detected=retryable_provider_detected,
        internal_status=internal_status,
        patch_present=patch_present,
        no_change=no_change,
        evidence=evidence,
        context="in the final unsuccessful execution outcome",
    )
    if provider is not None:
        return provider

    if internal_status in ERROR_STATUSES:
        reason = "SWE-agent reported an internal error"
    elif internal_status not in SUCCESS_STATUSES:
        reason = "unrecognized or non-success SWE-agent status"
    elif outer_returncode != 0:
        reason = (
            f"outer process returned {outer_returncode} despite a success-like "
            "internal status"
        )
    else:
        reason = (
            "successful status without a non-empty patch or permitted no-change "
            "declaration"
        )
    return ExecutionOutcome(
        "terminal_agent_error",
        "failed_terminal",
        False,
        internal_status,
        patch_present,
        no_change,
        reason,
        evidence,
    )
