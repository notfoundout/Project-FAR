from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

CASE_DIR = Path(__file__).resolve().parent
PRIMARY_DIR = CASE_DIR / "primary-freeze"
SOURCE_LOCK_PATH = PRIMARY_DIR / "source-artifact-lock.json"
FREEZE_PATH = PRIMARY_DIR / "primary-freeze.json"
FREEZE_HASH_PATH = PRIMARY_DIR / "primary-freeze.sha256"
ADJUDICATION_PATH = PRIMARY_DIR / "outcome-blind-adjudication.json"
REVEAL_DIR = CASE_DIR / "post-freeze-reveal"

CASE_ID = "swe-agent-v1.0.0-v1.0.1-gemini-3.1-pro-preview-v2"
TASK_ID = "scikit-learn__scikit-learn-14125"
SOURCE_SCHEMA = "far-swe-agent-v2-source-artifact-lock/1.0"
FREEZE_SCHEMA = "far-swe-agent-v2-primary-freeze/1.0"
REVEAL_SCHEMA = "far-swe-agent-v2-post-freeze-reveal/1.0"
REPORT_SCHEMA = "far-swe-agent-v2-final-report/1.0"

FORBIDDEN_OUTCOME_KEYS = {
    "fail_to_pass",
    "pass_to_pass",
    "resolved",
    "resolution_status",
    "grader",
    "grader_output",
    "evaluation",
    "score",
    "reward",
    "tests_passed",
    "tests_failed",
    "swebench_result",
}
EXPECTED_RUNS = (
    ("v1.0.0-r1", "v1.0.0", 1),
    ("v1.0.0-r2", "v1.0.0", 2),
    ("v1.0.1-r1", "v1.0.1", 1),
    ("v1.0.1-r2", "v1.0.1", 2),
)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def canonical_json(value: object) -> bytes:
    return (
        json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    ).encode("utf-8")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def read_json(path: Path) -> Any:
    if not path.is_file():
        raise SystemExit(f"Missing required file: {path}")
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON in {path}: {exc}") from exc


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(canonical_json(value))


def scan_forbidden(value: Any, path: str = "root") -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            normalized = str(key).strip().lower()
            if normalized in FORBIDDEN_OUTCOME_KEYS:
                raise SystemExit(
                    f"Outcome-bearing field forbidden before freeze: {path}.{key}"
                )
            scan_forbidden(child, f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            scan_forbidden(child, f"{path}[{index}]")


def safe_relative(root: Path, relative: str) -> Path:
    rel = Path(relative)
    if rel.is_absolute() or ".." in rel.parts:
        raise SystemExit(f"Unsafe relative path in evidence manifest: {relative}")
    path = root / rel
    try:
        path.resolve().relative_to(root.resolve())
    except ValueError as exc:
        raise SystemExit(f"Evidence path escapes root: {relative}") from exc
    return path


def actual_tree(root: Path) -> list[dict[str, Any]]:
    if root.is_symlink() or not root.is_dir():
        raise SystemExit(f"Artifact root is not a local directory: {root}")
    entries: list[dict[str, Any]] = []
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        if path.is_symlink():
            raise SystemExit(f"Symlink forbidden in artifact tree: {path}")
        entries.append(
            {
                "path": path.relative_to(root).as_posix(),
                "sha256": sha256_file(path),
                "size_bytes": path.stat().st_size,
            }
        )
    return entries


def verify_source(artifact_root: Path) -> dict[str, Any]:
    lock = read_json(SOURCE_LOCK_PATH)
    if lock.get("schema") != SOURCE_SCHEMA or lock.get("case_id") != CASE_ID:
        raise SystemExit("Source artifact lock schema or case mismatch")
    if lock.get("outcomes_accessed") is not False:
        raise SystemExit("Source artifact lock violates the outcome boundary")
    expected = lock.get("files")
    if not isinstance(expected, list) or lock.get("file_count") != len(expected):
        raise SystemExit("Source artifact lock file count mismatch")
    actual = actual_tree(artifact_root)
    if actual != expected:
        expected_map = {entry["path"]: entry for entry in expected}
        actual_map = {entry["path"]: entry for entry in actual}
        missing = sorted(set(expected_map) - set(actual_map))
        extra = sorted(set(actual_map) - set(expected_map))
        changed = sorted(
            path
            for path in set(expected_map) & set(actual_map)
            if expected_map[path] != actual_map[path]
        )
        raise SystemExit(
            "Source artifact tree mismatch: "
            f"missing={missing}, extra={extra}, changed={changed}"
        )
    root_hash = sha256_bytes(canonical_json(actual))
    if root_hash != lock.get("content_root_sha256"):
        raise SystemExit("Source artifact content root mismatch")

    state = read_json(artifact_root / "execution-output/execution-state.json")
    if state.get("schema") != "far-swe-agent-execution-state/1.1":
        raise SystemExit("Execution-state schema mismatch")
    if state.get("case_id") != CASE_ID:
        raise SystemExit("Execution-state case mismatch")
    runs = state.get("runs")
    if not isinstance(runs, list) or len(runs) != 4:
        raise SystemExit("Exactly four execution runs are required")
    observed = []
    for run in runs:
        observed.append((run.get("run_id"), run.get("release"), run.get("repetition")))
        if run.get("state") != "complete" or run.get("attempts") != 1:
            raise SystemExit(f"Run is not a one-attempt completion: {run.get('run_id')}")
        if run.get("outcome_category") != "complete_with_budget_limited_patch":
            raise SystemExit(f"Unexpected completion category: {run.get('run_id')}")
        record = read_json(
            safe_relative(
                artifact_root / "execution-output", str(run.get("record"))
            )
        )
        if record.get("benchmark_outcomes_accessed") is not False:
            raise SystemExit(f"Run record violates outcome boundary: {run.get('run_id')}")
        trajectory = safe_relative(
            artifact_root / "execution-output", str(run.get("trajectory"))
        )
        if not trajectory.is_file() or sha256_file(trajectory) != run.get(
            "trajectory_sha256"
        ):
            raise SystemExit(f"Trajectory binding mismatch: {run.get('run_id')}")
    if tuple(observed) != EXPECTED_RUNS:
        raise SystemExit(f"Execution matrix order mismatch: {observed}")

    for path in artifact_root.rglob("*"):
        if path.is_file() and path.suffix in {".json", ".traj"}:
            try:
                value = json.loads(path.read_text(encoding="utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError):
                continue
            scan_forbidden(value, path.relative_to(artifact_root).as_posix())
    return lock


def verify_freeze() -> dict[str, Any]:
    freeze = read_json(FREEZE_PATH)
    if freeze.get("schema") != FREEZE_SCHEMA or freeze.get("case_id") != CASE_ID:
        raise SystemExit("Primary freeze schema or case mismatch")
    if freeze.get("outcomes_accessed") is not False:
        raise SystemExit("Primary freeze violates the outcome boundary")
    entries = freeze.get("artifacts")
    if not isinstance(entries, list) or freeze.get("artifact_count") != len(entries):
        raise SystemExit("Primary freeze artifact count mismatch")
    for entry in entries:
        path = safe_relative(PRIMARY_DIR, str(entry.get("path")))
        if (
            not path.is_file()
            or sha256_file(path) != entry.get("sha256")
            or path.stat().st_size != entry.get("size_bytes")
        ):
            raise SystemExit(f"Primary freeze verification failed: {entry.get('path')}")
        value = read_json(path)
        scan_forbidden(value, str(entry.get("path")))
    if freeze.get("root_sha256") != sha256_bytes(canonical_json(entries)):
        raise SystemExit("Primary freeze root hash mismatch")
    if freeze.get("source_content_root_sha256") != read_json(
        SOURCE_LOCK_PATH
    ).get("content_root_sha256"):
        raise SystemExit("Primary freeze is not bound to the source artifact root")
    if freeze.get("outcome_blind_adjudication_sha256") != sha256_file(
        ADJUDICATION_PATH
    ):
        raise SystemExit("Primary freeze adjudication binding mismatch")
    expected_sidecar = FREEZE_HASH_PATH.read_text(encoding="utf-8").strip()
    if expected_sidecar != sha256_file(FREEZE_PATH):
        raise SystemExit("Primary freeze SHA-256 sidecar mismatch")
    return freeze


def prediction_source_path(artifact_root: Path, run_id: str) -> Path:
    return (
        artifact_root
        / "execution-output"
        / "runs"
        / run_id
        / "sweagent-output"
        / TASK_ID
        / f"{TASK_ID}.pred"
    )


def patch_source_path(artifact_root: Path, run_id: str) -> Path:
    return (
        artifact_root
        / "execution-output"
        / "runs"
        / run_id
        / "sweagent-output"
        / TASK_ID
        / f"{TASK_ID}.patch"
    )


def materialize_predictions(artifact_root: Path, output_dir: Path) -> list[Path]:
    verify_freeze()
    verify_source(artifact_root)
    state = read_json(artifact_root / "execution-output/execution-state.json")
    paths: list[Path] = []
    for run in state["runs"]:
        run_id = run["run_id"]
        pred_path = prediction_source_path(artifact_root, run_id)
        patch_path = patch_source_path(artifact_root, run_id)
        prediction = read_json(pred_path)
        patch = patch_path.read_text(encoding="utf-8")
        if prediction.get("instance_id") != TASK_ID:
            raise SystemExit(f"Prediction task mismatch: {run_id}")
        model_patch = prediction.get("model_patch")
        if not isinstance(model_patch, str) or not model_patch.strip():
            raise SystemExit(f"Prediction has no non-empty patch: {run_id}")
        if model_patch != patch:
            raise SystemExit(f"Prediction and patch file disagree: {run_id}")
        payload = {
            "instance_id": TASK_ID,
            "model_name_or_path": run_id,
            "model_patch": patch,
        }
        target = output_dir / f"{run_id}.jsonl"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(
            json.dumps(payload, sort_keys=True, ensure_ascii=False).encode("utf-8")
            + b"\n"
        )
        paths.append(target)
    return paths


def collect_outcomes(evaluation_root: Path) -> dict[str, Any]:
    outcomes: dict[str, Any] = {}
    for run_id, release, repetition in EXPECTED_RUNS:
        run_dir = evaluation_root / run_id
        report_path = run_dir / "report.json"
        output_path = run_dir / "test_output.txt"
        log_path = run_dir / "run_instance.log"
        report = read_json(report_path)
        task_report = report.get(TASK_ID)
        if not isinstance(task_report, dict) or not isinstance(
            task_report.get("resolved"), bool
        ):
            raise SystemExit(f"Malformed SWE-bench report for {run_id}")
        if not output_path.is_file() or not log_path.is_file():
            raise SystemExit(f"Incomplete evaluation evidence for {run_id}")
        outcomes[run_id] = {
            "release": release,
            "repetition": repetition,
            "resolved": task_report["resolved"],
            "report_sha256": sha256_file(report_path),
            "test_output_sha256": sha256_file(output_path),
            "run_instance_log_sha256": sha256_file(log_path),
            "report": task_report,
        }
    return outcomes


def decision_summary(outcomes: dict[str, Any]) -> tuple[dict[str, int], str]:
    counts = {
        release: sum(
            1
            for value in outcomes.values()
            if value["release"] == release and value["resolved"]
        )
        for release in ("v1.0.0", "v1.0.1")
    }
    if counts["v1.0.1"] > counts["v1.0.0"]:
        observed = "candidate_higher_observed_resolution"
    elif counts["v1.0.1"] < counts["v1.0.0"]:
        observed = "candidate_lower_observed_resolution"
    else:
        observed = "no_observed_resolution_difference"
    return counts, observed


def reveal(artifact_root: Path, evaluation_root: Path, output_dir: Path) -> list[Path]:
    freeze = verify_freeze()
    verify_source(artifact_root)
    outcomes = collect_outcomes(evaluation_root)
    counts, observed = decision_summary(outcomes)
    mapping = {"System-A": "v1.0.0", "System-B": "v1.0.1"}
    reveal_payload = {
        "schema": REVEAL_SCHEMA,
        "case_id": CASE_ID,
        "revealed_at": utc_now(),
        "primary_freeze_sha256": sha256_file(FREEZE_PATH),
        "primary_root_sha256": freeze["root_sha256"],
        "source_content_root_sha256": freeze["source_content_root_sha256"],
        "blind_mapping": mapping,
        "outcomes": outcomes,
        "resolved_counts": counts,
        "observed_resolution_result": observed,
        "claim_boundary": (
            "Outcomes were attached only after primary-freeze verification. "
            "Two repetitions per release on one task do not establish general superiority."
        ),
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    reveal_path = output_dir / "outcome-reveal.json"
    write_json(reveal_path, reveal_payload)

    adjudication = read_json(ADJUDICATION_PATH)
    overall = (
        "REVIEW_REQUIRED"
        if adjudication.get("overall_decision") == "REVIEW_REQUIRED"
        else adjudication.get("overall_decision", "UNKNOWN")
    )
    final = {
        "schema": REPORT_SCHEMA,
        "case_id": CASE_ID,
        "generated_at": utc_now(),
        "primary_freeze_sha256": sha256_file(FREEZE_PATH),
        "outcome_reveal_sha256": sha256_file(reveal_path),
        "execution_matrix_complete": True,
        "resolved_counts": counts,
        "observed_resolution_result": observed,
        "outcome_blind_integrity_decision": adjudication.get("overall_decision"),
        "bounded_case_decision": overall,
        "primary_questions": adjudication.get("findings"),
        "limitations": [
            "One SWE-bench task was evaluated.",
            "Each release has two repetitions.",
            "All four runs ended at the same frozen call-budget autosubmission boundary.",
            "Benchmark resolution does not resolve the outcome-blind provenance ambiguity.",
            "The blocked Gemini 2.5 Pro case is separate and is not pooled.",
        ],
        "claim_boundary": (
            "This report is a bounded external version-to-version case. "
            "It does not establish universal accuracy, safety, compliance, commercial "
            "readiness, enterprise readiness, or general release superiority."
        ),
    }
    final_path = output_dir / "final-comparison-report.json"
    write_json(final_path, final)

    table_rows = "\n".join(
        f"| `{run_id}` | `{value['release']}` | {value['repetition']} | "
        f"{'Resolved' if value['resolved'] else 'Unresolved'} |"
        for run_id, value in outcomes.items()
    )
    markdown = f"""# SWE-agent v1.0.0 vs v1.0.1 — bounded external case report

## Result

- Baseline v1.0.0: **{counts['v1.0.0']}/2 resolved**
- Candidate v1.0.1: **{counts['v1.0.1']}/2 resolved**
- Observed benchmark result: `{observed}`
- Outcome-blind integrity decision: `{adjudication.get('overall_decision')}`
- Bounded case decision: `{overall}`

## Run outcomes

| Run | Release | Repetition | SWE-bench outcome |
|---|---|---:|---|
{table_rows}

## Outcome-blind findings

The primary adjudication was hash-frozen before benchmark outcomes were accessed.
It found no authorization bypass or undeclared external-state use. It required review
because behavior varied materially within releases and the candidate recorded additional
configuration/provenance fields whose operational significance was not established.

## Interpretation

The benchmark count is an observed result for one task and two repetitions per release.
It is not a population estimate and does not establish general superiority. All four
executions reached the same frozen 30-call limit and autosubmitted non-empty patches.

## Claim boundary

This report does not establish universal accuracy, safety, compliance, commercial
readiness, enterprise readiness, or general release superiority. The blocked Gemini
2.5 Pro case remains separate and is not pooled.
"""
    markdown_path = output_dir / "final-comparison-report.md"
    markdown_path.write_text(markdown, encoding="utf-8")

    bundle_entries = []
    for path in sorted((reveal_path, final_path, markdown_path)):
        bundle_entries.append(
            {
                "path": path.name,
                "sha256": sha256_file(path),
                "size_bytes": path.stat().st_size,
            }
        )
    bundle = {
        "schema": "far-swe-agent-v2-final-bundle/1.0",
        "case_id": CASE_ID,
        "created_at": utc_now(),
        "artifacts": bundle_entries,
        "root_sha256": sha256_bytes(canonical_json(bundle_entries)),
    }
    bundle_path = output_dir / "bundle-sha256.json"
    write_json(bundle_path, bundle)
    return [reveal_path, final_path, markdown_path, bundle_path]


def verify_reveal(output_dir: Path) -> dict[str, Any]:
    reveal_path = output_dir / "outcome-reveal.json"
    report_path = output_dir / "final-comparison-report.json"
    markdown_path = output_dir / "final-comparison-report.md"
    bundle_path = output_dir / "bundle-sha256.json"
    reveal_value = read_json(reveal_path)
    report_value = read_json(report_path)
    bundle = read_json(bundle_path)
    if reveal_value.get("schema") != REVEAL_SCHEMA:
        raise SystemExit("Outcome reveal schema mismatch")
    if report_value.get("schema") != REPORT_SCHEMA:
        raise SystemExit("Final report schema mismatch")
    if report_value.get("outcome_reveal_sha256") != sha256_file(reveal_path):
        raise SystemExit("Final report reveal binding mismatch")
    entries = bundle.get("artifacts")
    if not isinstance(entries, list):
        raise SystemExit("Final bundle entries missing")
    for entry in entries:
        path = safe_relative(output_dir, entry["path"])
        if (
            not path.is_file()
            or sha256_file(path) != entry["sha256"]
            or path.stat().st_size != entry["size_bytes"]
        ):
            raise SystemExit(f"Final bundle verification failed: {entry['path']}")
    if bundle.get("root_sha256") != sha256_bytes(canonical_json(entries)):
        raise SystemExit("Final bundle root hash mismatch")
    if not markdown_path.is_file():
        raise SystemExit("Final Markdown report missing")
    return report_value


def main() -> None:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    source = sub.add_parser("verify-source")
    source.add_argument("--artifact-root", type=Path, required=True)
    sub.add_parser("verify-freeze")
    materialize = sub.add_parser("materialize-predictions")
    materialize.add_argument("--artifact-root", type=Path, required=True)
    materialize.add_argument("--output-dir", type=Path, required=True)
    reveal_parser = sub.add_parser("reveal")
    reveal_parser.add_argument("--artifact-root", type=Path, required=True)
    reveal_parser.add_argument("--evaluation-root", type=Path, required=True)
    reveal_parser.add_argument("--output-dir", type=Path, default=REVEAL_DIR)
    verify = sub.add_parser("verify-reveal")
    verify.add_argument("--output-dir", type=Path, default=REVEAL_DIR)
    args = parser.parse_args()

    if args.command == "verify-source":
        print(json.dumps(verify_source(args.artifact_root.resolve()), indent=2))
    elif args.command == "verify-freeze":
        print(json.dumps(verify_freeze(), indent=2))
    elif args.command == "materialize-predictions":
        print(
            "\n".join(
                str(path)
                for path in materialize_predictions(
                    args.artifact_root.resolve(), args.output_dir.resolve()
                )
            )
        )
    elif args.command == "reveal":
        print(
            "\n".join(
                str(path)
                for path in reveal(
                    args.artifact_root.resolve(),
                    args.evaluation_root.resolve(),
                    args.output_dir.resolve(),
                )
            )
        )
    else:
        print(json.dumps(verify_reveal(args.output_dir.resolve()), indent=2))


if __name__ == "__main__":
    main()
