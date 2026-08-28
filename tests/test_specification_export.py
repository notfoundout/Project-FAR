import hashlib
import json
import shutil
from pathlib import Path

from tools import export_specification

ROOT = Path(__file__).resolve().parents[1]
V1_SHA256 = "b7cbd28d54686da33773a66edf9af9480044ffaabfeb83cfa4bfc1a12fe862a5"


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
    assert manifest["export_version"] == "1.2.0"
    assert manifest["exporter_version"] == "1.2.0"
    assert manifest["export_version"] == export_specification.EXPORT_VERSION
    assert manifest["schema_version"] == export_specification.SCHEMA_VERSION
    assert manifest["compatibility_version"] == export_specification.COMPATIBILITY_VERSION
    assert manifest["core_theory_id"] == "PROJECT-FAR-CORE-THEORY-1.1"
    assert manifest["core_theory_id"] == export_specification.CORE_THEORY_ID

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


def test_export_carries_exact_core_theory():
    """Retain the historical exact-byte regression under the v1.2 export policy."""
    export_dir = ROOT / "exports" / "far-spec-v1"
    source_v1 = ROOT / "theory/theorems/Project-FAR-Theory-Closure-v1.0.md"
    exported_v1 = export_dir / "theorems/Project-FAR-Theory-Closure-v1.0.md"

    assert exported_v1.read_bytes() == source_v1.read_bytes()
    assert hashlib.sha256(exported_v1.read_bytes()).hexdigest() == V1_SHA256

    manifest = json.loads((export_dir / "manifest.json").read_text())
    assert manifest["export_version"] == "1.2.0"
    assert manifest["exporter_version"] == "1.2.0"
    assert manifest["core_theory_id"] == "PROJECT-FAR-CORE-THEORY-1.1"
    entries = {artifact["path"]: artifact for artifact in manifest["artifacts"]}
    record = entries["theorems/Project-FAR-Theory-Closure-v1.0.md"]
    assert record["category"] == "theorems"
    assert record["status"] == "historical"
    assert record["source"] == "theory/theorems/Project-FAR-Theory-Closure-v1.0.md"
    assert record["sha256"] == V1_SHA256


def test_export_carries_canonical_v1_1_and_historical_v1_0():
    export_dir = ROOT / "exports" / "far-spec-v1"
    source_v1 = ROOT / "theory/theorems/Project-FAR-Theory-Closure-v1.0.md"
    source_v11 = ROOT / "theory/theorems/Project-FAR-Theory-Closure-v1.1.md"
    source_ledger = ROOT / "theory/terminal/project-far-core-theory-v1.1.json"
    exported_v1 = export_dir / "theorems/Project-FAR-Theory-Closure-v1.0.md"
    exported_v11 = export_dir / "theorems/Project-FAR-Theory-Closure-v1.1.md"
    exported_ledger = export_dir / "theorems/project-far-core-theory-v1.1.json"

    assert exported_v1.read_bytes() == source_v1.read_bytes()
    assert hashlib.sha256(exported_v1.read_bytes()).hexdigest() == V1_SHA256
    assert exported_v11.read_bytes() == source_v11.read_bytes()
    assert exported_ledger.read_bytes() == source_ledger.read_bytes()

    manifest = json.loads((export_dir / "manifest.json").read_text())
    entries = {artifact["path"]: artifact for artifact in manifest["artifacts"]}

    old = entries["theorems/Project-FAR-Theory-Closure-v1.0.md"]
    assert old["category"] == "theorems"
    assert old["status"] == "historical"
    assert old["source"] == "theory/theorems/Project-FAR-Theory-Closure-v1.0.md"
    assert old["sha256"] == V1_SHA256

    current = entries["theorems/Project-FAR-Theory-Closure-v1.1.md"]
    assert current["category"] == "theorems"
    assert current["status"] == "canonical"
    assert current["source"] == "theory/theorems/Project-FAR-Theory-Closure-v1.1.md"

    ledger = entries["theorems/project-far-core-theory-v1.1.json"]
    assert ledger["category"] == "theorems"
    assert ledger["status"] == "canonical"
    assert ledger["source"] == "theory/terminal/project-far-core-theory-v1.1.json"
