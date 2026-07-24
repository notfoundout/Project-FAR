from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
CANDIDATE_DIR = Path(__file__).resolve().parent


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _run(command: list[str], *, allowed: set[int] = {0}) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, check=False)
    if result.returncode not in allowed:
        raise RuntimeError(
            f"command failed with exit {result.returncode}: {' '.join(command)}\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        )
    return result


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def execute(output_directory: Path) -> dict[str, Any]:
    raw = output_directory / "raw"
    derived = output_directory / "derived"
    evidence = output_directory / "evidence"
    for directory in (raw, derived, evidence):
        directory.mkdir(parents=True, exist_ok=True)

    _run([
        sys.executable,
        str(CANDIDATE_DIR / "acquire_candidate.py"),
        "--output-directory",
        str(raw),
    ])

    candidate = _read_json(CANDIDATE_DIR / "candidate.json")
    claims = _read_json(CANDIDATE_DIR / "claims.json")
    trajectory = raw / candidate["trajectory_filename"]
    package = derived / "decision-package.json"
    adjudication = evidence / "adjudication-report.json"

    _run([
        "far-external-trace",
        str(trajectory),
        "--format",
        "swe-agent",
        "--trace-id",
        candidate["candidate_id"],
        "--output",
        str(package),
    ])
    adjudication_result = _run(
        ["far-decision", str(package), "--output", str(adjudication)],
        allowed={0, 30, 31, 32},
    )

    artifact_manifest = _read_json(raw / "artifact-manifest.json")
    decision_report = _read_json(adjudication)
    package_payload = _read_json(package)
    execution_report = {
        "schema_version": "far-trace-candidate-execution/0.1",
        "candidate_id": candidate["candidate_id"],
        "instance_id": candidate["instance_id"],
        "contamination": candidate["contamination"],
        "blind_detection_value_permitted": False,
        "source_manifest": artifact_manifest,
        "claims_sha256": _sha256(CANDIDATE_DIR / "claims.json"),
        "decision_package": {
            "path": str(package.relative_to(output_directory)),
            "sha256": _sha256(package),
            "trace_completeness": package_payload["trace_completeness"],
            "semantic_completeness_verified": package_payload["metadata"].get(
                "semantic_completeness_verified", False
            ),
        },
        "adjudication": {
            "path": str(adjudication.relative_to(output_directory)),
            "sha256": _sha256(adjudication),
            "status": decision_report["status"],
            "exit_code": adjudication_result.returncode,
            "finding_ids": sorted(item["rule_id"] for item in decision_report["findings"]),
        },
        "registered_claim_count": len(claims.get("claims", [])),
        "claim_boundary": (
            "Candidate 001 validates acquisition, hashing, ingestion, provenance, compilation, "
            "adjudication, and determinism only; it cannot establish blind detection value."
        ),
    }
    report_path = evidence / "execution-report.json"
    _write_json(report_path, execution_report)

    bundle_manifest = {
        "schema_version": "far-evidence-bundle/0.1",
        "candidate_id": candidate["candidate_id"],
        "files": [
            {"path": str(path.relative_to(output_directory)), "sha256": _sha256(path)}
            for path in sorted(output_directory.rglob("*"))
            if path.is_file()
            and path.name != "bundle-manifest.json"
            and path.suffix != ".log"
        ],
    }
    _write_json(evidence / "bundle-manifest.json", bundle_manifest)
    return execution_report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-directory", default="build/trace-candidate-001")
    args = parser.parse_args(argv)
    report = execute(Path(args.output_directory))
    print(json.dumps(report, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
