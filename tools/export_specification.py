#!/usr/bin/env python3
"""Deterministically export the Project FAR public specification surface."""
from __future__ import annotations

import hashlib
import json
import os
import re
import shutil
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

EXPORT_VERSION = "1.0.0"
EXPORTER_VERSION = "1.0.0"
SCHEMA_VERSION = "far-ir/1.0"
COMPATIBILITY_VERSION = "1.0.0"
EXPORT_DIRNAME = "far-spec-v1"
ROOT = Path(__file__).resolve().parents[1]
EXPORT_ROOT = ROOT / "exports" / EXPORT_DIRNAME

@dataclass(frozen=True)
class Artifact:
    source: Path | None
    destination: Path
    category: str
    status: str = "canonical"

ARTIFACTS: tuple[Artifact, ...] = (
    Artifact(ROOT / "spec/far-yaml-grammar.md", Path("grammar/far-yaml-grammar.md"), "grammar"),
    Artifact(ROOT / "spec/far-yaml.schema.json", Path("schemas/far-yaml.schema.json"), "schemas"),
    Artifact(ROOT / "schemas/far-document.schema.json", Path("schemas/far-document.schema.json"), "schemas"),
    Artifact(ROOT / "theory/proof-objects/proof-object-schema.yaml", Path("schemas/proof-object-schema.yaml"), "schemas"),
    Artifact(ROOT / "theory/semantics/proof-step-semantics.md", Path("semantics/proof-step-semantics.md"), "semantics"),
    Artifact(ROOT / "theory/proof-objects/proof-step-rules.md", Path("semantics/proof-step-rules.md"), "semantics"),
    Artifact(ROOT / "theory/proof-objects/semantic-proof-checking.md", Path("semantics/semantic-proof-checking.md"), "semantics"),
    Artifact(ROOT / "theory/semantics/construction.md", Path("semantics/construction.md"), "semantics"),
    Artifact(ROOT / "theory/semantics/model-theory.md", Path("semantics/model-theory.md"), "semantics"),
    Artifact(ROOT / "theory/semantics/scope.md", Path("semantics/scope.md"), "semantics"),
    Artifact(ROOT / "theory/formal-semantics/far-semantics.md", Path("semantics/far-semantics.md"), "semantics"),
    Artifact(ROOT / "theory/definitions/definitions.md", Path("terminology/definitions.md"), "terminology"),
    Artifact(ROOT / "theory/definitions/derived-concepts.md", Path("terminology/derived-concepts.md"), "terminology"),
    Artifact(ROOT / "theory/definitions/derivation.md", Path("terminology/derivation.md"), "terminology"),
    Artifact(ROOT / "theory/definitions/meta-theory-definitions.md", Path("terminology/meta-theory-definitions.md"), "terminology"),
    Artifact(ROOT / "theory/metadata/definitions.yaml", Path("terminology/definitions.yaml"), "terminology"),
    Artifact(ROOT / "conformance/far-ir-1.0/valid/minimal.json", Path("examples/valid/minimal.json"), "examples"),
    Artifact(ROOT / "conformance/far-ir-1.0/valid/complete.json", Path("examples/valid/complete.json"), "examples"),
    Artifact(ROOT / "conformance/far-ir-1.0/invalid/missing-format-version.json", Path("examples/invalid/missing-format-version.json"), "examples"),
    Artifact(ROOT / "conformance/far-ir-1.0/invalid/broken-reference.json", Path("examples/invalid/broken-reference.json"), "examples"),
)

EXAMPLE_METADATA = {
    "valid/minimal.json": {"expected_validity": "valid", "schema_version": SCHEMA_VERSION, "purpose": "Minimal valid FAR IR document."},
    "valid/complete.json": {"expected_validity": "valid", "schema_version": SCHEMA_VERSION, "purpose": "Representative complete valid FAR IR document."},
    "invalid/missing-format-version.json": {"expected_validity": "invalid", "schema_version": SCHEMA_VERSION, "purpose": "Rejects documents without required format_version."},
    "invalid/broken-reference.json": {"expected_validity": "invalid", "schema_version": SCHEMA_VERSION, "purpose": "Rejects dependency references to unknown objects."},
}

def git(*args: str, optional: bool = False) -> str:
    try:
        return subprocess.check_output(["git", *args], cwd=ROOT, text=True, stderr=subprocess.DEVNULL).strip()
    except subprocess.CalledProcessError:
        if optional:
            return ""
        raise

def sha256(path: Path) -> str:
    h = hashlib.sha256(); h.update(path.read_bytes()); return h.hexdigest()

def copy_artifacts(out: Path) -> list[dict]:
    seen = set(); records = []
    for artifact in ARTIFACTS:
        if artifact.destination.as_posix() in seen:
            raise ValueError(f"duplicate artifact name: {artifact.destination}")
        seen.add(artifact.destination.as_posix())
        if artifact.source is None or not artifact.source.exists():
            raise FileNotFoundError(artifact.source)
        dest = out / artifact.destination
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(artifact.source, dest)
        records.append({
            "path": artifact.destination.as_posix(),
            "category": artifact.category,
            "status": artifact.status,
            "source": artifact.source.relative_to(ROOT).as_posix(),
        })
    return records

def write_generated(out: Path) -> list[dict]:
    (out / "compatibility").mkdir(parents=True, exist_ok=True)
    compat = out / "compatibility/compatibility-spec.md"
    compat.write_text(f"""# Project FAR Specification Compatibility Policy\n\nVersion: {COMPATIBILITY_VERSION}\n\n## Supported integration surface\n\nExternal projects may rely only on files exported in `exports/{EXPORT_DIRNAME}` and recorded in `manifest.json` and `checksums.json`. Project FAR internal paths, implementation modules, tests, and repository layout are not supported integration surfaces.\n\n## Stable content\n\nThe stable surface consists of exported grammar, normative schemas, canonical semantic contracts, canonical terminology, compatibility policy, and representative examples. Stability means changes are intentional, versioned, checksummed, and represented by a new export artifact set.\n\n## Semantic versioning\n\nExport versions use `MAJOR.MINOR.PATCH`. MAJOR changes may alter or remove stable contracts. MINOR changes may add backward-compatible artifacts or constraints. PATCH changes correct packaging, metadata, or documentation without changing Project FAR semantics.\n\n## Compatibility guarantees\n\nFor a fixed major export version, artifact paths, schema identifiers, documented grammar references, and checksum verification remain reproducible. Consumers must verify checksums before use and must treat the manifest as authoritative for the export contents.\n\n## Deprecation policy\n\nDeprecated artifacts remain present for at least one minor release within the same major version unless removal is necessary to avoid publishing obsolete or experimental material as normative. Deprecations are announced in this compatibility specification or a successor compatibility artifact.\n\n## Unsupported assumptions\n\nConsumers must not depend on Project FAR source tree paths, Python APIs, test fixtures outside the export, generated file ordering not recorded in the manifest, unexported schemas, research notes, archived artifacts, or inferred semantics not stated by exported canonical artifacts.\n""", encoding="utf-8")
    (out / "examples").mkdir(exist_ok=True)
    (out / "examples/README.md").write_text("# Project FAR Specification Examples\n\nEach example is copied from the canonical conformance suite and described in `examples/index.json`.\n", encoding="utf-8")
    (out / "examples/index.json").write_text(json.dumps(EXAMPLE_METADATA, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return [
        {"path":"compatibility/compatibility-spec.md","category":"compatibility","status":"generated","source":None},
        {"path":"examples/README.md","category":"examples","status":"generated","source":None},
        {"path":"examples/index.json","category":"examples","status":"generated","source":None},
    ]

def existing_vcs_metadata(out: Path) -> dict[str, str]:
    manifest_path = out / "manifest.json"
    if not manifest_path.exists():
        return {}
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    keys = ("project_far_repository", "active_branch", "commit_sha", "export_timestamp")
    return {key: manifest[key] for key in keys if isinstance(manifest.get(key), str) and manifest[key]}

def vcs_metadata(out: Path) -> dict[str, str]:
    preserved = existing_vcs_metadata(out)
    if preserved:
        return preserved
    return {
        "project_far_repository": git("config", "--get", "remote.origin.url", optional=True) or ROOT.as_posix(),
        "active_branch": git("rev-parse", "--abbrev-ref", "HEAD"),
        "commit_sha": git("rev-parse", "HEAD"),
        "export_timestamp": git("show", "-s", "--format=%cI", "HEAD"),
    }

def build(out: Path) -> None:
    metadata = vcs_metadata(out)
    if out.exists(): shutil.rmtree(out)
    for d in ["grammar","schemas","semantics","terminology","compatibility","examples/valid","examples/invalid"]:
        (out/d).mkdir(parents=True, exist_ok=True)
    records = copy_artifacts(out) + write_generated(out)
    files = sorted(p for p in out.rglob("*") if p.is_file() and p.name not in {"manifest.json","checksums.json"})
    checksums = {p.relative_to(out).as_posix(): sha256(p) for p in files}
    records = sorted(records, key=lambda r: r["path"])
    for r in records: r["sha256"] = checksums[r["path"]]
    manifest = {
        **metadata,
        "export_version": EXPORT_VERSION,
        "exporter_version": EXPORTER_VERSION,
        "schema_version": SCHEMA_VERSION,
        "compatibility_version": COMPATIBILITY_VERSION,
        "artifacts": records,
    }
    (out/"manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True)+"\n", encoding="utf-8")
    all_files = sorted(p for p in out.rglob("*") if p.is_file() and p.name != "checksums.json")
    checksums = {p.relative_to(out).as_posix(): sha256(p) for p in all_files}
    (out/"checksums.json").write_text(json.dumps({"algorithm":"SHA-256","files": checksums}, indent=2, sort_keys=True)+"\n", encoding="utf-8")
    validate(out)

def validate(out: Path) -> None:
    manifest = json.loads((out/"manifest.json").read_text())
    checksum_doc = json.loads((out/"checksums.json").read_text())
    required_metadata = ["project_far_repository", "active_branch", "commit_sha", "export_timestamp", "export_version", "exporter_version", "schema_version", "compatibility_version"]
    missing = [key for key in required_metadata if not manifest.get(key)]
    if missing: raise ValueError(f"missing manifest metadata: {missing}")
    if not re.fullmatch(r"[0-9a-f]{40}", manifest["commit_sha"]): raise ValueError("manifest commit_sha is not a full Git SHA")
    paths = [a["path"] for a in manifest["artifacts"]]
    if len(paths) != len(set(paths)): raise ValueError("duplicate artifact names exist")
    for rel in paths + ["manifest.json"]:
        path = out/rel
        if not path.exists(): raise FileNotFoundError(rel)
        expected = checksum_doc["files"].get(rel)
        if expected != sha256(path): raise ValueError(f"checksum mismatch: {rel}")
    actual = sorted(p.relative_to(out).as_posix() for p in out.rglob("*") if p.is_file() and p.name != "checksums.json")
    if sorted(paths + ["manifest.json"]) != actual: raise ValueError("manifest does not match exported files")
    md_link = re.compile(r"\[[^\]]+\]\((?!https?://|mailto:|#)([^)]+)\)")
    for p in out.rglob("*.md"):
        for ref in md_link.findall(p.read_text(encoding="utf-8")):
            target = (p.parent / ref.split('#')[0]).resolve()
            if ref.split('#')[0] and out.resolve() in target.parents and not target.exists():
                raise ValueError(f"broken reference in {p}: {ref}")

def verify_deterministic() -> None:
    with tempfile.TemporaryDirectory() as td:
        a = Path(td)/"a"; b = Path(td)/"b"
        build(a); build(b)
        for pa in sorted(p for p in a.rglob("*") if p.is_file()):
            pb = b / pa.relative_to(a)
            if pa.read_bytes() != pb.read_bytes():
                raise ValueError(f"non-deterministic output: {pa.relative_to(a)}")

def main() -> None:
    build(EXPORT_ROOT)
    verify_deterministic()
    print(f"Exported {EXPORT_ROOT.relative_to(ROOT)}")

if __name__ == "__main__":
    main()
