from __future__ import annotations

from pathlib import Path
from typing import Any

import execution_outcome as base


def _normalized_prediction(patch: str | None, no_change: bool) -> tuple[str | None, bool]:
    """Normalize SWE-agent's equivalent empty-patch encodings."""
    if patch is None or not patch.strip():
        patch = None
    return patch, no_change


def read_prediction(swe_output: Path, task_id: str) -> tuple[str | None, bool, str]:
    """Read the canonical per-instance and aggregate SWE-agent predictions.

    SWE-agent v1.0.x writes the same target prediction twice: once as the
    per-instance ``<instance>.pred`` file and once in ``preds.json``. Those two
    carriers are corroborating evidence when their normalized payloads agree.
    Multiple target ``.pred`` files, multiple target aggregate files, malformed
    target entries, or disagreeing payloads remain terminal evidence defects.
    """
    if swe_output.is_symlink() or not swe_output.is_dir():
        raise ValueError(f"prediction output path is not a local directory: {swe_output}")

    prediction_matches: list[tuple[str | None, bool, str]] = []
    aggregate_matches: list[tuple[str | None, bool, str]] = []

    for path in sorted(swe_output.rglob("*.pred")):
        if not base._is_local_regular_file(path, swe_output):
            raise ValueError(f"prediction path is not a local regular file: {path}")
        found, patch, no_change = base._extract_prediction(
            base._read_json(path),
            task_id,
            allow_implicit_instance=path.stem == task_id,
        )
        if path.stem == task_id and not found:
            raise ValueError(
                f"exact prediction file does not identify target instance: {path}"
            )
        if found:
            prediction_matches.append((patch, no_change, str(path)))

    if len(prediction_matches) > 1:
        raise ValueError(
            "multiple .pred files identify the target instance: "
            + ", ".join(path for _, _, path in prediction_matches)
        )

    for path in sorted(swe_output.rglob("preds.json")):
        if not base._is_local_regular_file(path, swe_output):
            raise ValueError(f"prediction path is not a local regular file: {path}")
        found, patch, no_change = base._extract_prediction(
            base._read_json(path), task_id, allow_implicit_instance=False
        )
        if found:
            aggregate_matches.append((patch, no_change, str(path)))

    if len(aggregate_matches) > 1:
        raise ValueError(
            "multiple aggregate prediction files identify the target instance: "
            + ", ".join(path for _, _, path in aggregate_matches)
        )

    matches = prediction_matches + aggregate_matches
    if not matches:
        return None, False, ""

    normalized = {
        _normalized_prediction(patch, no_change)
        for patch, no_change, _path in matches
    }
    if len(normalized) != 1:
        raise ValueError(
            "conflicting prediction evidence for target instance: "
            + ", ".join(path for _, _, path in matches)
        )

    patch, no_change = next(iter(normalized))
    return patch, no_change, ";".join(path for _, _, path in matches)


def classify_execution(
    *,
    outer_returncode: int,
    swe_output: Path,
    task_id: str,
    stdout: str,
    stderr: str,
    allow_no_change: bool = False,
) -> base.ExecutionOutcome:
    """Classify an execution using the actual SWE-agent v1.0.x output contract."""
    combined = (stdout + "\n" + stderr).lower()
    quota_detected = any(marker in combined for marker in base.QUOTA_MARKERS)
    retryable_provider_detected = any(
        marker in combined for marker in base.RETRYABLE_PROVIDER_MARKERS
    )
    if swe_output.is_symlink() or not swe_output.is_dir():
        return base.ExecutionOutcome(
            "terminal_agent_error",
            "failed_terminal",
            False,
            None,
            False,
            False,
            f"execution output path is not a local directory: {swe_output}",
            {"outer_returncode": outer_returncode, "status_files": []},
        )

    status_files = sorted(swe_output.rglob("run_batch_exit_statuses.yaml"))
    base_evidence: dict[str, Any] = {
        "outer_returncode": outer_returncode,
        "status_files": [str(path) for path in status_files],
    }

    if len(status_files) != 1:
        provider = base._provider_outcome(
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
        return base.ExecutionOutcome(
            "terminal_agent_error",
            "failed_terminal",
            False,
            None,
            False,
            False,
            f"expected exactly one run_batch_exit_statuses.yaml, found {len(status_files)}",
            base_evidence,
        )

    if not base._is_local_regular_file(status_files[0], swe_output):
        return base.ExecutionOutcome(
            "terminal_agent_error",
            "failed_terminal",
            False,
            None,
            False,
            False,
            f"internal status path is not a local regular file: {status_files[0]}",
            base_evidence,
        )

    try:
        internal_status, status_payload = base.parse_internal_status(
            status_files[0], task_id
        )
    except ValueError as exc:
        evidence = {**base_evidence, "status_file": str(status_files[0])}
        provider = base._provider_outcome(
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
        return base.ExecutionOutcome(
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
        return base.ExecutionOutcome(
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

    if internal_status in base.SUCCESS_STATUSES and outer_returncode == 0:
        if patch_present:
            return base.ExecutionOutcome(
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
            return base.ExecutionOutcome(
                "valid_no_change",
                "complete",
                False,
                internal_status,
                False,
                True,
                "protocol-permitted no-change submission",
                evidence,
            )

    provider = base._provider_outcome(
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

    if internal_status in base.ERROR_STATUSES:
        reason = "SWE-agent reported an internal error"
    elif internal_status not in base.SUCCESS_STATUSES:
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
    return base.ExecutionOutcome(
        "terminal_agent_error",
        "failed_terminal",
        False,
        internal_status,
        patch_present,
        no_change,
        reason,
        evidence,
    )


def install(core: Any, hardening: Any) -> None:
    """Route live and restored execution classification through this contract."""
    core.classify_execution = classify_execution
    hardening.classify_execution = classify_execution
