from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
SEED = b"Project-FAR-trace-candidate-002"
EXCLUDED = "django__django-15044.traj"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def run(command: list[str], allowed: set[int] = {0}) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, check=False)
    if result.returncode not in allowed:
        raise RuntimeError(
            f"command failed with exit {result.returncode}: {' '.join(command)}\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        )
    return result


def acquire_pre_outcome(output: Path) -> tuple[Path, Path, int]:
    try:
        import pyarrow.compute as pc
        import pyarrow.parquet as pq
        from huggingface_hub import hf_hub_download
    except ImportError as exc:
        raise RuntimeError("install huggingface_hub and pyarrow") from exc

    protocol = json.loads((HERE / "protocol.json").read_text(encoding="utf-8"))
    source = protocol["selection"]
    parquet = Path(hf_hub_download(
        repo_id=source["source_repository"], repo_type="dataset",
        revision=source["source_revision"], filename=source["source_file"],
    ))
    table = pq.read_table(parquet, columns=["filename", "trajectory", "submission"])
    rows = [row for row in table.to_pylist()
            if row.get("filename") != EXCLUDED and row.get("trajectory") and row.get("submission")]
    rows.sort(key=lambda row: row["filename"])
    if not rows:
        raise RuntimeError("no eligible Candidate 002 rows")
    index = int(hashlib.sha256(SEED).hexdigest()[:8], 16) % len(rows)
    selected = rows[index]

    raw = output / "raw"
    raw.mkdir(parents=True, exist_ok=True)
    trajectory = raw / selected["filename"]
    submission = raw / "submission.diff"
    trajectory.write_text(selected["trajectory"], encoding="utf-8")
    submission.write_text(selected["submission"], encoding="utf-8")
    write_json(raw / "selection.json", {
        "schema_version": "far-blind-selection/0.1",
        "candidate_id": "trace-candidate-002",
        "eligible_count": len(rows),
        "selection_index": index,
        "selected_filename": selected["filename"],
        "forbidden_outcome_fields_read": False,
        "source_dataset_sha256": sha256(parquet),
        "trajectory_sha256": sha256(trajectory),
        "submission_sha256": sha256(submission),
    })
    return parquet, trajectory, index


def execute_pre_outcome(output: Path) -> dict[str, Any]:
    parquet, trajectory, selection_index = acquire_pre_outcome(output)
    derived = output / "derived"
    evidence = output / "evidence"
    package = derived / "decision-package.json"
    adjudication = evidence / "adjudication-report.json"
    run(["far-external-trace", str(trajectory), "--format", "swe-agent",
         "--trace-id", "trace-candidate-002", "--output", str(package)])
    result = run(["far-decision", str(package), "--output", str(adjudication)], {0, 30, 31, 32})
    report = json.loads(adjudication.read_text(encoding="utf-8"))
    primary = {
        "schema_version": "far-blind-primary-result/0.1",
        "candidate_id": "trace-candidate-002",
        "selection_index": selection_index,
        "forbidden_outcome_fields_read": False,
        "decision_package_sha256": sha256(package),
        "adjudication_sha256": sha256(adjudication),
        "adjudication_status": report["status"],
        "adjudication_exit_code": result.returncode,
        "finding_ids": sorted(item["rule_id"] for item in report["findings"]),
        "claims_sha256": sha256(HERE / "claims.json"),
        "protocol_sha256": sha256(HERE / "protocol.json"),
    }
    primary_path = evidence / "primary-result.json"
    write_json(primary_path, primary)
    freeze = {
        "schema_version": "far-primary-freeze/0.1",
        "candidate_id": "trace-candidate-002",
        "stage": "primary-result-frozen-before-outcome-reveal",
        "primary_result_sha256": sha256(primary_path),
        "decision_package_sha256": sha256(package),
        "adjudication_sha256": sha256(adjudication),
        "source_dataset_sha256": sha256(parquet),
    }
    write_json(evidence / "primary-freeze.json", freeze)
    return primary


def reveal_outcome(output: Path) -> dict[str, Any]:
    freeze_path = output / "evidence" / "primary-freeze.json"
    selection_path = output / "raw" / "selection.json"
    if not freeze_path.exists() or not selection_path.exists():
        raise RuntimeError("primary result must be frozen before outcome reveal")
    freeze_hash_before = sha256(freeze_path)
    selection = json.loads(selection_path.read_text(encoding="utf-8"))

    import pyarrow.compute as pc
    import pyarrow.parquet as pq
    from huggingface_hub import hf_hub_download
    protocol = json.loads((HERE / "protocol.json").read_text(encoding="utf-8"))
    source = protocol["selection"]
    parquet = Path(hf_hub_download(
        repo_id=source["source_repository"], repo_type="dataset",
        revision=source["source_revision"], filename=source["source_file"],
    ))
    table = pq.read_table(parquet, columns=["filename", "resolved", "exit_status"])
    selected = table.filter(pc.equal(table["filename"], selection["selected_filename"]))
    if selected.num_rows != 1:
        raise RuntimeError("selected outcome row not unique")
    row = selected.to_pylist()[0]
    reveal = {
        "schema_version": "far-outcome-reveal/0.1",
        "candidate_id": "trace-candidate-002",
        "primary_freeze_sha256_before_reveal": freeze_hash_before,
        "selected_filename": selection["selected_filename"],
        "resolved": row.get("resolved"),
        "exit_status": row.get("exit_status"),
        "blind_order_preserved": sha256(freeze_path) == freeze_hash_before,
    }
    write_json(output / "evidence" / "outcome-reveal.json", reveal)
    return reveal


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-directory", default="build/trace-candidate-002")
    parser.add_argument("--stage", choices=["pre-outcome", "reveal", "all"], default="all")
    args = parser.parse_args(argv)
    output = Path(args.output_directory)
    if args.stage in {"pre-outcome", "all"}:
        execute_pre_outcome(output)
    if args.stage in {"reveal", "all"}:
        reveal_outcome(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
