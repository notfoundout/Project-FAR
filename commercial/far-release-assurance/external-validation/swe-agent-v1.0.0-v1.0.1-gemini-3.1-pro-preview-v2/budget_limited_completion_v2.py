from __future__ import annotations

import shutil
import stat
from pathlib import Path
from typing import Any, Callable

BUDGET_STATUS = "submitted (exit_cost)"
COMPLETE_CATEGORY = "complete_with_budget_limited_patch"
CORRECTION_SCHEMA = "far-swe-agent-budget-completion-reclassification/1.0"

_ALLOWED_INVOCATION_SCHEMAS = {
    "far-swe-agent-invocation/1.1",
    "far-swe-agent-invocation/1.2",
    "far-swe-agent-invocation/1.3",
}
_ALLOWED_RECORD_SCHEMAS = {
    "far-swe-agent-run-record/1.0",
    "far-swe-agent-run-record/1.1",
    "far-swe-agent-run-record/1.2",
}


def wrap_classifier(
    delegate: Callable[..., Any], outcome_type: type[Any]
) -> Callable[..., Any]:
    """Treat the exact frozen call-budget autosubmission as complete evidence."""

    def classify_execution(**kwargs: Any) -> Any:
        outcome = delegate(**kwargs)
        if not (
            outcome.state == "failed_terminal"
            and outcome.category == "terminal_agent_error"
            and outcome.internal_status == BUDGET_STATUS
            and kwargs.get("outer_returncode") == 0
            and outcome.patch_present is True
            and outcome.no_change_submission is False
            and outcome.evidence.get("provider_classification_signal") is None
        ):
            return outcome

        evidence = dict(outcome.evidence)
        evidence.update(
            {
                "completion_boundary": "frozen_per_instance_call_limit",
                "benchmark_quality_evaluated": False,
                "budget_limited_autosubmission": True,
            }
        )
        return outcome_type(
            COMPLETE_CATEGORY,
            "complete",
            False,
            outcome.internal_status,
            True,
            False,
            (
                "SWE-agent reached the frozen API-call limit and autosubmitted a "
                "non-empty prediction; execution evidence is complete while "
                "benchmark quality remains unevaluated"
            ),
            evidence,
        )

    return classify_execution


def _terminal(
    core: Any, run: dict[str, Any], reason: str, evidence: dict[str, Any]
):
    return {}, core.ExecutionOutcome(
        "terminal_agent_error",
        "failed_terminal",
        False,
        None,
        False,
        False,
        reason,
        {"run_id": run["run_id"], **evidence},
    )


def _safe_output_path(base: Any, value: Any, label: str) -> Path:
    if not isinstance(value, str) or not value:
        raise SystemExit(f"{label} is missing")
    relative = Path(value)
    if relative.is_absolute() or ".." in relative.parts:
        raise SystemExit(f"{label} escapes execution-output: {value}")
    return base.OUTPUT_DIR / relative


def _local_regular(path: Path, root: Path) -> bool:
    try:
        relative = path.relative_to(root)
        current = root
        if root.is_symlink() or not root.is_dir():
            return False
        for part in relative.parts:
            current = current / part
            mode = current.lstat().st_mode
            if stat.S_ISLNK(mode):
                return False
        return stat.S_ISREG(path.lstat().st_mode)
    except (OSError, ValueError):
        return False


def _read_raw_execution(
    core: Any,
    run: dict[str, Any],
    task_id: str,
    *,
    plan_sha256: str | None = None,
    image: str | None = None,
):
    base = core.base
    run_dir = base.RUNS_DIR / run["run_id"]
    record_path = core._record_path(run)
    invocation_path = run_dir / "invocation.json"
    instance_path = run_dir / "instance.json"
    stdout_path = run_dir / "stdout.log"
    stderr_path = run_dir / "stderr.log"
    swe_output = run_dir / "sweagent-output"

    missing = [
        label
        for label, path in {
            "run_record": record_path,
            "invocation": invocation_path,
            "instance": instance_path,
            "stdout": stdout_path,
            "stderr": stderr_path,
        }.items()
        if not path.is_file()
    ]
    if not swe_output.is_dir():
        missing.append("sweagent_output")
    if missing:
        raise SystemExit(
            f"Budget-limited completion evidence is incomplete for {run['run_id']}: "
            + ", ".join(sorted(missing))
        )

    record = base.read_json(record_path)
    invocation = base.read_json(invocation_path)
    returncode = record.get("returncode")
    if not isinstance(returncode, int):
        raise SystemExit(
            f"Budget-limited run has no integer return code: {run['run_id']}"
        )

    outcome = core.classify_execution(
        outer_returncode=returncode,
        swe_output=swe_output,
        task_id=task_id,
        stdout=stdout_path.read_text(encoding="utf-8", errors="replace"),
        stderr=stderr_path.read_text(encoding="utf-8", errors="replace"),
        allow_no_change=False,
    )
    if outcome.state != "complete" or outcome.category != COMPLETE_CATEGORY:
        return record, invocation, outcome, run_dir, swe_output

    if plan_sha256 is None or image is None:
        manifest, lock, _task = base.frozen_inputs()
        plan_sha256 = base.validate_plan(manifest, lock)
        image = lock["immutable_image_reference"]

    invalid: list[str] = []
    if invocation.get("schema") not in _ALLOWED_INVOCATION_SCHEMAS:
        invalid.append("invocation_schema")
    if record.get("schema") not in _ALLOWED_RECORD_SCHEMAS:
        invalid.append("run_record_schema")
    common = {
        "run_id": run["run_id"],
        "release": run["release"],
        "commit": run["full_commit"],
        "task_id": task_id,
    }
    for key, expected in common.items():
        if invocation.get(key) != expected:
            invalid.append(f"invocation_{key}")
        if record.get(key) != expected:
            invalid.append(f"run_record_{key}")
    if record.get("repetition") != run["repetition"]:
        invalid.append("run_record_repetition")
    if record.get("attempt") != run.get("attempts"):
        invalid.append("run_record_attempt")
    if run.get("record") != str(record_path.relative_to(base.OUTPUT_DIR)):
        invalid.append("canonical_record_binding")
    if record.get("state") != "failed_terminal":
        invalid.append("historical_run_record_state")
    raw_outcome = record.get("outcome")
    if (
        not isinstance(raw_outcome, dict)
        or raw_outcome.get("category") != "terminal_agent_error"
    ):
        invalid.append("historical_run_record_outcome")
    if invocation.get("benchmark_outcomes_accessible") is not False:
        invalid.append("invocation_outcome_boundary")
    if record.get("benchmark_outcomes_accessed") is not False:
        invalid.append("run_record_outcome_boundary")
    if invocation.get("agent_config_sha256") != base.sha256_file(base.CONFIG_PATH):
        invalid.append("invocation_agent_config")
    for source, label in ((invocation, "invocation"), (record, "run_record")):
        if source.get("execution_plan_sha256") != plan_sha256:
            invalid.append(f"{label}_execution_plan")
        if source.get("image") != image:
            invalid.append(f"{label}_image")
    if record.get("artifact_sha256") != core._current_artifact_hashes(run_dir):
        invalid.append("current_artifact_sha256")
    if not isinstance(record.get("completed_at"), str) or not record["completed_at"]:
        invalid.append("completed_at")
    if invalid:
        raise SystemExit(
            f"Budget-limited run failed preserved provenance validation: {sorted(invalid)}"
        )
    return record, invocation, outcome, run_dir, swe_output


def _next_correction_path(base: Any, run: dict[str, Any]) -> Path:
    root = base.OUTPUT_DIR / "corrections"
    attempt = int(run.get("attempts", 0))
    stem = f"{run['run_id']}-attempt-{attempt:03d}-budget-completion"
    candidate = root / f"{stem}.json"
    if not candidate.exists():
        return candidate
    index = 1
    while True:
        candidate = root / f"{stem}-{index:02d}.json"
        if not candidate.exists():
            return candidate
        index += 1


def reclassify_budget_limited_failure(
    core: Any, state: dict[str, Any], task_id: str
) -> bool:
    run = next((item for item in state["runs"] if item["state"] != "complete"), None)
    if (
        run is None
        or run.get("state") != "failed_terminal"
        or run.get("outcome_category") != "terminal_agent_error"
    ):
        return False

    record, _invocation, outcome, run_dir, swe_output = _read_raw_execution(
        core, run, task_id
    )
    if outcome.state != "complete" or outcome.category != COMPLETE_CATEGORY:
        return False

    base = core.base
    source = base.locate_trajectory(swe_output, task_id)
    if not _local_regular(source, swe_output):
        raise SystemExit(f"Native trajectory is not a local regular file: {source}")
    base.TRAJECTORY_DIR.mkdir(parents=True, exist_ok=True)
    target = base.TRAJECTORY_DIR / run["trajectory_artifact"]
    source_hash = base.sha256_file(source)
    if target.exists():
        if not _local_regular(target, base.TRAJECTORY_DIR):
            raise SystemExit(
                f"Canonical trajectory is not a local regular file: {target}"
            )
        if base.sha256_file(target) != source_hash:
            raise SystemExit(
                "Canonical trajectory conflicts with preserved native trajectory"
            )
    else:
        shutil.copy2(source, target)

    correction_path = _next_correction_path(base, run)
    correction = {
        "schema": CORRECTION_SCHEMA,
        "corrected_at": base.utc_now(),
        "run_id": run["run_id"],
        "attempts_preserved": run.get("attempts"),
        "before_state": run.get("state"),
        "after_state": "complete",
        "before_outcome_category": run.get("outcome_category"),
        "after_outcome_category": COMPLETE_CATEGORY,
        "previous_correction": run.get("correction"),
        "run_record": str(core._record_path(run).relative_to(base.OUTPUT_DIR)),
        "run_record_sha256": base.sha256_file(core._record_path(run)),
        "raw_artifact_sha256": base.collect_hashes(run_dir),
        "source_trajectory": str(source.relative_to(base.OUTPUT_DIR)),
        "source_trajectory_sha256": source_hash,
        "canonical_trajectory": str(target.relative_to(base.OUTPUT_DIR)),
        "canonical_trajectory_sha256": source_hash,
        "raw_run_record_preserved": True,
        "benchmark_outcomes_accessed": False,
        "outcome": outcome.to_dict(),
    }
    base.write_json(correction_path, correction)
    state.setdefault("corrections", []).append(correction)

    before_state = run.get("state")
    run.update(
        {
            "state": "complete",
            "record": str(core._record_path(run).relative_to(base.OUTPUT_DIR)),
            "outcome_category": COMPLETE_CATEGORY,
            "corrected_from": before_state,
            "correction": str(correction_path.relative_to(base.OUTPUT_DIR)),
            "completed_at": record["completed_at"],
            "trajectory": str(target.relative_to(base.OUTPUT_DIR)),
            "trajectory_sha256": source_hash,
        }
    )
    base.save_state(state)
    return True


def validate_budget_completion(
    core: Any,
    run: dict[str, Any],
    task_id: str,
    *,
    plan_sha256: str | None = None,
    image: str | None = None,
):
    if (
        run.get("state") != "complete"
        or run.get("outcome_category") != COMPLETE_CATEGORY
        or not isinstance(run.get("correction"), str)
    ):
        return None

    base = core.base
    correction_path = _safe_output_path(base, run["correction"], "correction")
    if not _local_regular(correction_path, base.OUTPUT_DIR):
        return _terminal(
            core,
            run,
            "budget completion correction is not a local regular file",
            {"correction": str(correction_path)},
        )
    correction = base.read_json(correction_path)
    record, _invocation, outcome, run_dir, _swe_output = _read_raw_execution(
        core,
        run,
        task_id,
        plan_sha256=plan_sha256,
        image=image,
    )
    expected_record = core._record_path(run)
    source = _safe_output_path(
        base, correction.get("source_trajectory"), "source trajectory"
    )
    target = _safe_output_path(
        base, correction.get("canonical_trajectory"), "canonical trajectory"
    )
    expected = {
        "schema": CORRECTION_SCHEMA,
        "run_id": run["run_id"],
        "attempts_preserved": run.get("attempts"),
        "before_state": "failed_terminal",
        "after_state": "complete",
        "before_outcome_category": "terminal_agent_error",
        "after_outcome_category": COMPLETE_CATEGORY,
        "run_record": str(expected_record.relative_to(base.OUTPUT_DIR)),
        "run_record_sha256": base.sha256_file(expected_record),
        "raw_artifact_sha256": base.collect_hashes(run_dir),
        "canonical_trajectory": run.get("trajectory"),
        "canonical_trajectory_sha256": run.get("trajectory_sha256"),
        "raw_run_record_preserved": True,
        "benchmark_outcomes_accessed": False,
        "outcome": outcome.to_dict(),
    }
    invalid = [key for key, value in expected.items() if correction.get(key) != value]
    if not isinstance(correction.get("corrected_at"), str) or not correction["corrected_at"]:
        invalid.append("corrected_at")
    if run.get("corrected_from") != "failed_terminal":
        invalid.append("corrected_from")
    source_root = run_dir / "sweagent-output"
    if not _local_regular(source, source_root):
        invalid.append("source_trajectory_path")
    if not _local_regular(target, base.TRAJECTORY_DIR):
        invalid.append("canonical_trajectory_path")
    if _local_regular(source, source_root) and _local_regular(
        target, base.TRAJECTORY_DIR
    ):
        source_hash = base.sha256_file(source)
        target_hash = base.sha256_file(target)
        if correction.get("source_trajectory_sha256") != source_hash:
            invalid.append("source_trajectory_sha256")
        if correction.get("canonical_trajectory_sha256") != target_hash:
            invalid.append("canonical_trajectory_sha256")
        if source_hash != target_hash:
            invalid.append("trajectory_copy_mismatch")
    if run.get("completed_at") != record.get("completed_at"):
        invalid.append("completed_at")
    if invalid:
        return _terminal(
            core,
            run,
            "budget completion correction failed validation",
            {"invalid": sorted(set(invalid)), "correction": str(correction_path)},
        )
    return record, outcome


def install(legacy_module: Any) -> Any:
    core = legacy_module._core
    if getattr(core, "_v2_budget_completion_installed", False):
        return legacy_module

    classifier = wrap_classifier(core.classify_execution, core.ExecutionOutcome)
    core.classify_execution = classifier
    legacy_module._hardening.classify_execution = classifier

    original_preserved = core._classify_preserved_run

    def classify_preserved(
        run: dict[str, Any],
        task_id: str,
        *,
        plan_sha256: str | None = None,
        image: str | None = None,
    ):
        record, outcome = original_preserved(
            run, task_id, plan_sha256=plan_sha256, image=image
        )
        if outcome.state == "complete":
            return record, outcome
        corrected = validate_budget_completion(
            core, run, task_id, plan_sha256=plan_sha256, image=image
        )
        return corrected if corrected is not None else (record, outcome)

    core._classify_preserved_run = classify_preserved

    original_reconcile = core.reconcile_completed_runs

    def reconcile(state: dict[str, Any], task_id: str) -> bool:
        if reclassify_budget_limited_failure(core, state, task_id):
            return True
        return original_reconcile(state, task_id)

    core.reconcile_completed_runs = reconcile

    def reconcile_only() -> dict[str, Any]:
        manifest, lock, task = core.base.frozen_inputs()
        plan_sha256 = core.base.validate_plan(manifest, lock)
        state = core.base.load_state(manifest, lock, plan_sha256)
        changed = core.reconcile_completed_runs(state, task["instance_id"])
        if not changed:
            core._ensure_progressable(state)
        return {"changed": changed, "state": state}

    core.reconcile_only = reconcile_only
    core._v2_budget_completion_installed = True
    return legacy_module
