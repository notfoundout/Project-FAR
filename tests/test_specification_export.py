import json
import shutil
import subprocess
from pathlib import Path

from tools import export_specification

ROOT = Path(__file__).resolve().parents[1]


def test_export_validation_and_determinism(tmp_path):
    first = tmp_path / "first"
    second = tmp_path / "second"

    export_specification.build(first)
    export_specification.build(second)

    export_specification.validate(first)
    export_specification.validate(second)

    first_files = sorted(p.relative_to(first) for p in first.rglob("*") if p.is_file())
    second_files = sorted(p.relative_to(second) for p in second.rglob("*") if p.is_file())
    assert first_files == second_files
    for rel in first_files:
        assert (first / rel).read_bytes() == (second / rel).read_bytes()


def test_manifest_and_checksums_are_complete():
    export_dir = ROOT / "exports" / "far-spec-v1"
    manifest = json.loads((export_dir / "manifest.json").read_text())
    checksums = json.loads((export_dir / "checksums.json").read_text())

    artifact_paths = [artifact["path"] for artifact in manifest["artifacts"]]
    assert len(artifact_paths) == len(set(artifact_paths))
    assert manifest["export_version"] == export_specification.EXPORT_VERSION
    assert manifest["schema_version"] == export_specification.SCHEMA_VERSION
    assert manifest["compatibility_version"] == export_specification.COMPATIBILITY_VERSION

    exported_files = sorted(
        p.relative_to(export_dir).as_posix()
        for p in export_dir.rglob("*")
        if p.is_file() and p.name != "checksums.json"
    )
    assert exported_files == sorted(artifact_paths + ["manifest.json"])
    assert sorted(checksums["files"]) == sorted(exported_files)


def test_committed_export_is_fresh(tmp_path):
    generated = tmp_path / "generated"
    committed = ROOT / "exports" / "far-spec-v1"
    shutil.copytree(committed, generated)
    export_specification.build(generated)

    generated_files = sorted(p.relative_to(generated) for p in generated.rglob("*") if p.is_file())
    committed_files = sorted(p.relative_to(committed) for p in committed.rglob("*") if p.is_file())
    assert generated_files == committed_files
    for rel in generated_files:
        assert (generated / rel).read_bytes() == (committed / rel).read_bytes(), rel
