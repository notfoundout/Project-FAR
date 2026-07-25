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


class _UniqueKeyLoader(yaml.SafeLoader):
    """Safe YAML loader that rejects mappings whose meaning is ambiguous."""


def _construct_unique_mapping(loader: yaml.SafeLoader, node: yaml.MappingNode):
    loader.flatten_mapping(node)
    mapping: dict[Any, Any] = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=False)
        try:
            duplicate = key in mapping
        except TypeError as exc:
            raise yaml.constructor.ConstructorError(
                "while constructing a mapping",
                node.start_mark,
                "found an unhashable mapping key",
                key_node.start_mark,
            ) from exc
        if duplicate:
            raise yaml.constructor.ConstructorError(
                "while constructing a mapping",
                node.start_mark,
                f"found duplicate key {key!r}",
                key_node.start_mark,
            )
        mapping[key] = loader.construct_object(value_node, deep=False)
    return mapping


_UniqueKeyLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _construct_unique_mapping
)


def _require_local_regular_file(path: Path, root: Path, label: str) -> None:
    if path.is_symlink() or not path.is_file():
        raise ValueError(f"{label} is not a regular file: {path}")
    try:
        path.resolve().relative_to(root.resolve())
    except ValueError as exc:
        raise ValueError(f"{label} escapes execution output: {path}") from exc


def _read_yaml_mapping(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise ValueError(f"missing internal status file: {path}")
    try:
        _require_local_regular_file(path, path.parent, "internal status file")
        value = yaml.load(path.read_text(encoding="utf-8"), Loader=_UniqueKeyLoader)
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
) -> tuple[bool, str | None, bool]:
    if isinstance(value, dict):
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
                raise ValueError("prediction cannot contain both a non-empty patch and no-change")
            return True, patch if isinstance(patch, str) else None, no_change
        if task_id in value:
            return _extract_prediction(
                value[task_id], task_id, allow_implicit_instance=True
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
        _require_local_regular_file(path, path.parent, "prediction file")
        return json.loads(path.read_text(encoding="utf-8"))
    except OSError as exc:
        raise ValueError(f"cannot read prediction file: {path}: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"prediction file is invalid JSON: {path}: {exc}") from exc


def read_prediction(swe_output: Path, task_id: str) -> tuple[str | None, bool, str]:
    exact_files = sorted(
        path for path in swe_output.rglob("*.pred") if path.stem == task_id
    )
    aggregate_files = sorted(swe_output.rglob("preds.json"))
    matches: list[tuple[str | None, bool, str]] = []

    for path in exact_files:
        found, patch, no_change = _extract_prediction(
            _read_json(path), task_id, allow_implicit_instance=True
        )
        if not found:
            raise ValueError(f"exact prediction file does not identify target instance: {path}")
        matches.append((patch, no_change, str(path)))

    for path in aggregate_files:
        found, patch, no_change = _extract_prediction(
            _read_json(path), task_id, allow_implicit_instance=False
        )
        if found:
            matches.append((patch, no_change, str(path)))

    if not matches:
        raise ValueError("missing prediction evidence for target instance")
    if len(matches) != 1:
        signatures = {(patch, no_change) for patch, no_change, _ in matches}
        kind = "conflicting" if len(signatures) != 1 else "duplicate"
        raise ValueError(
            f"{kind} prediction evidence for target instance: "
            + ", ".join(path for _, _, path in matches)
        )
    return matches[0]


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
    if swe_output.is_symlink() or not swe_output.is_dir():
        return ExecutionOutcome(
            "terminal_agent_error",
            "failed_terminal",
            False,
            None,
            False,
            False,
            f"SWE-agent output is not a local regular directory: {swe_output}",
            {"outer_returncode": outer_returncode, "swe_output": str(swe_output)},
        )
    status_files = sorted(swe_output.rglob("run_batch_exit_statuses.yaml"))
    unsafe_status_files = [path for path in status_files if path.is_symlink()]
    base_evidence: dict[str, Any] = {
        "outer_returncode": outer_returncode,
        "status_files": [str(path) for path in status_files],
    }

    if len(status_files) != 1 or unsafe_status_files:
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
            "expected exactly one regular run_batch_exit_statuses.yaml, "
            f"found {len(status_files)} with {len(unsafe_status_files)} symlinks",
            base_evidence,
        )

    try:
        internal_status, status_payload = parse_internal_status(
            status_files[0], task_id
        )
    except ValueError as exc:
        evidence = {**base_evidence, "status_file": str(status_files[0])}
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
