from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

import evidence_pipeline_v2 as pipeline


EXPECTED_BUNDLE_FILES = {
    "outcome-reveal.json",
    "final-comparison-report.json",
    "final-comparison-report.md",
}


def fail(message: str) -> None:
    raise SystemExit(message)


def parse_timestamp(value: Any, field: str) -> None:
    if not isinstance(value, str):
        fail(f"{field} must be an ISO-8601 timestamp")
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise SystemExit(f"{field} must be an ISO-8601 timestamp") from exc


def validate_outcomes(outcomes: Any) -> dict[str, Any]:
    if not isinstance(outcomes, dict):
        fail("Outcome reveal outcomes must be an object")
    expected_ids = [run_id for run_id, _, _ in pipeline.EXPECTED_RUNS]
    if list(outcomes) != expected_ids:
        fail("Outcome reveal run order or membership mismatch")
    for run_id, release, repetition in pipeline.EXPECTED_RUNS:
        value = outcomes[run_id]
        if not isinstance(value, dict):
            fail(f"Malformed outcome: {run_id}")
        if value.get("release") != release or value.get("repetition") != repetition:
            fail(f"Outcome identity mismatch: {run_id}")
        if not isinstance(value.get("resolved"), bool):
            fail(f"Outcome resolution must be boolean: {run_id}")
        report = value.get("report")
        if not isinstance(report, dict) or report.get("resolved") is not value["resolved"]:
            fail(f"Embedded report disagrees with outcome: {run_id}")
        for key in ("report_sha256", "test_output_sha256", "run_instance_log_sha256"):
            digest = value.get(key)
            if not isinstance(digest, str) or len(digest) != 64:
                fail(f"Malformed evidence digest {key}: {run_id}")
    return outcomes


def expected_report(reveal: dict[str, Any]) -> dict[str, Any]:
    adjudication = pipeline.read_json(pipeline.ADJUDICATION_PATH)
    overall = (
        "REVIEW_REQUIRED"
        if adjudication.get("overall_decision") == "REVIEW_REQUIRED"
        else adjudication.get("overall_decision", "UNKNOWN")
    )
    counts, observed = pipeline.decision_summary(reveal["outcomes"])
    return {
        "schema": pipeline.REPORT_SCHEMA,
        "case_id": pipeline.CASE_ID,
        "primary_freeze_sha256": reveal["primary_freeze_sha256"],
        "outcome_reveal_sha256": None,
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


def expected_markdown(reveal: dict[str, Any]) -> str:
    outcomes = reveal["outcomes"]
    counts, observed = pipeline.decision_summary(outcomes)
    adjudication = pipeline.read_json(pipeline.ADJUDICATION_PATH)
    overall = (
        "REVIEW_REQUIRED"
        if adjudication.get("overall_decision") == "REVIEW_REQUIRED"
        else adjudication.get("overall_decision", "UNKNOWN")
    )
    rows = "\n".join(
        f"| `{run_id}` | `{value['release']}` | {value['repetition']} | "
        f"{'Resolved' if value['resolved'] else 'Unresolved'} |"
        for run_id, value in outcomes.items()
    )
    return f"""# SWE-agent v1.0.0 vs v1.0.1 — bounded external case report

## Result

- Baseline v1.0.0: **{counts['v1.0.0']}/2 resolved**
- Candidate v1.0.1: **{counts['v1.0.1']}/2 resolved**
- Observed benchmark result: `{observed}`
- Outcome-blind integrity decision: `{adjudication.get('overall_decision')}`
- Bounded case decision: `{overall}`

## Run outcomes

| Run | Release | Repetition | SWE-bench outcome |
|---|---|---:|---|
{rows}

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


def verify(output_dir: Path) -> dict[str, Any]:
    pipeline.verify_freeze()
    freeze = pipeline.read_json(pipeline.FREEZE_PATH)
    source_lock = pipeline.read_json(pipeline.SOURCE_LOCK_PATH)

    reveal_path = output_dir / "outcome-reveal.json"
    report_path = output_dir / "final-comparison-report.json"
    markdown_path = output_dir / "final-comparison-report.md"
    bundle_path = output_dir / "bundle-sha256.json"

    reveal = pipeline.read_json(reveal_path)
    report = pipeline.read_json(report_path)
    bundle = pipeline.read_json(bundle_path)

    if reveal.get("schema") != pipeline.REVEAL_SCHEMA or reveal.get("case_id") != pipeline.CASE_ID:
        fail("Outcome reveal schema or case mismatch")
    parse_timestamp(reveal.get("revealed_at"), "revealed_at")

    bindings = {
        "primary_freeze_sha256": pipeline.sha256_file(pipeline.FREEZE_PATH),
        "primary_root_sha256": freeze.get("root_sha256"),
        "source_content_root_sha256": source_lock.get("content_root_sha256"),
    }
    for field, expected in bindings.items():
        if reveal.get(field) != expected:
            fail(f"Outcome reveal {field} does not match the current primary freeze")

    outcomes = validate_outcomes(reveal.get("outcomes"))
    counts, observed = pipeline.decision_summary(outcomes)
    if reveal.get("resolved_counts") != counts:
        fail("Outcome reveal resolved counts are not derivable from outcomes")
    if reveal.get("observed_resolution_result") != observed:
        fail("Outcome reveal decision is not derivable from outcomes")

    expected = expected_report(reveal)
    if report.get("schema") != pipeline.REPORT_SCHEMA or report.get("case_id") != pipeline.CASE_ID:
        fail("Final report schema or case mismatch")
    parse_timestamp(report.get("generated_at"), "generated_at")
    expected["outcome_reveal_sha256"] = pipeline.sha256_file(reveal_path)
    comparable = dict(report)
    comparable.pop("generated_at", None)
    if comparable != expected:
        fail("Final JSON report is not the deterministic derivation of the reveal")

    if not markdown_path.is_file() or markdown_path.read_text(encoding="utf-8") != expected_markdown(reveal):
        fail("Final Markdown report is not the deterministic derivation of the reveal")

    entries = bundle.get("artifacts")
    if not isinstance(entries, list) or {entry.get("path") for entry in entries} != EXPECTED_BUNDLE_FILES:
        fail("Final bundle membership mismatch")
    expected_entries = []
    for name in sorted(EXPECTED_BUNDLE_FILES):
        path = output_dir / name
        expected_entries.append(
            {"path": name, "sha256": pipeline.sha256_file(path), "size_bytes": path.stat().st_size}
        )
    if entries != expected_entries:
        fail("Final bundle entries do not match the committed outputs")
    if bundle.get("root_sha256") != pipeline.sha256_bytes(pipeline.canonical_json(expected_entries)):
        fail("Final bundle root hash mismatch")
    return report


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, default=pipeline.REVEAL_DIR)
    args = parser.parse_args()
    print(json.dumps(verify(args.output_dir.resolve()), indent=2))


if __name__ == "__main__":
    main()
