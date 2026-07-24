from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Mapping

EVIDENCE_MANIFEST_VERSION = "far-evidence-manifest/0.1"


def canonical_json_bytes(payload: Mapping[str, Any]) -> bytes:
    return (json.dumps(payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n").encode("utf-8")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def write_evidence_bundle(
    output_directory: str | Path,
    *,
    report_name: str,
    report_payload: Mapping[str, Any],
    source_files: Mapping[str, str | Path],
) -> tuple[Path, Path]:
    root = Path(output_directory)
    root.mkdir(parents=True, exist_ok=True)

    report_path = root / report_name
    report_bytes = canonical_json_bytes(report_payload)
    report_path.write_bytes(report_bytes)

    sources: list[dict[str, str]] = []
    for logical_name, source in sorted(source_files.items()):
        source_path = Path(source)
        try:
            data = source_path.read_bytes()
        except OSError as exc:
            raise ValueError(f"unable to read evidence source {source_path}: {exc}") from exc
        sources.append(
            {
                "name": logical_name,
                "path": str(source_path),
                "sha256": sha256_bytes(data),
            }
        )

    manifest = {
        "schema_version": EVIDENCE_MANIFEST_VERSION,
        "report": {
            "path": report_name,
            "sha256": sha256_bytes(report_bytes),
        },
        "sources": sources,
    }
    manifest_path = root / "manifest.json"
    manifest_path.write_bytes(canonical_json_bytes(manifest))
    return report_path, manifest_path


def verify_evidence_bundle(output_directory: str | Path) -> bool:
    root = Path(output_directory)
    try:
        manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return False
    if manifest.get("schema_version") != EVIDENCE_MANIFEST_VERSION:
        return False
    report = manifest.get("report")
    if not isinstance(report, dict):
        return False
    report_path = root / str(report.get("path", ""))
    try:
        return sha256_bytes(report_path.read_bytes()) == report.get("sha256")
    except OSError:
        return False
