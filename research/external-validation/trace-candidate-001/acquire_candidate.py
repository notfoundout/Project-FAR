from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

CANDIDATE = Path(__file__).with_name("candidate.json")


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def acquire(output_directory: Path) -> dict[str, Any]:
    try:
        import pyarrow.compute as pc
        import pyarrow.parquet as pq
        from huggingface_hub import hf_hub_download
    except ImportError as exc:
        raise RuntimeError(
            "acquisition requires huggingface_hub and pyarrow; "
            "install with: python -m pip install huggingface_hub pyarrow"
        ) from exc

    candidate = json.loads(CANDIDATE.read_text(encoding="utf-8"))
    source = candidate["source"]
    parquet_path = Path(
        hf_hub_download(
            repo_id=source["repository"],
            repo_type="dataset",
            revision=source["revision"],
            filename=source["file"],
        )
    )

    generator_columns = [
        "20240402_sweagent_gpt4",
        "20240620_sweagent_claude3.5sonnet",
        "20240721_amazon-q-developer-agent-20240719-dev",
        "20240628_autocoderover-v20240620",
    ]
    table = pq.read_table(
        parquet_path,
        columns=[
            "filename",
            "trajectory",
            "submission",
            "resolved",
            "steps",
            "api_calls",
            "exit_status",
            "model_stats",
            *generator_columns,
        ],
    )
    # The filename is the stable row identity. Generator flags are preserved as
    # observed metadata rather than used as an unverified selection predicate.
    mask = pc.equal(table["filename"], candidate["trajectory_filename"])
    selected = table.filter(mask)
    if selected.num_rows != 1:
        raise RuntimeError(f"expected exactly one candidate row, found {selected.num_rows}")
    row = selected.to_pylist()[0]

    output_directory.mkdir(parents=True, exist_ok=True)
    trajectory = output_directory / candidate["trajectory_filename"]
    submission = output_directory / "submission.diff"
    metadata = output_directory / "source-metadata.json"

    trajectory.write_text(row["trajectory"], encoding="utf-8")
    submission.write_text(row["submission"], encoding="utf-8")
    _write_json(
        metadata,
        {
            "candidate_id": candidate["candidate_id"],
            "instance_id": candidate["instance_id"],
            "source_repository": source["repository"],
            "source_revision": source["revision"],
            "source_file": source["file"],
            "selection_basis": {"filename": row["filename"]},
            "generator_flags": {column: row[column] for column in generator_columns},
            "filename": row["filename"],
            "resolved": row["resolved"],
            "steps": row["steps"],
            "api_calls": row["api_calls"],
            "exit_status": row["exit_status"],
            "model_stats": row["model_stats"],
        },
    )

    manifest = {
        "schema_version": "far-artifact-manifest/0.1",
        "candidate_id": candidate["candidate_id"],
        "source_dataset": {
            "repository": source["repository"],
            "revision": source["revision"],
            "file": source["file"],
            "downloaded_sha256": _sha256(parquet_path),
        },
        "artifacts": [
            {"path": trajectory.name, "sha256": _sha256(trajectory)},
            {"path": submission.name, "sha256": _sha256(submission)},
            {"path": metadata.name, "sha256": _sha256(metadata)},
        ],
    }
    _write_json(output_directory / "artifact-manifest.json", manifest)
    return manifest


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-directory", default="build/trace-candidate-001/raw")
    args = parser.parse_args(argv)
    manifest = acquire(Path(args.output_directory))
    print(json.dumps(manifest, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
