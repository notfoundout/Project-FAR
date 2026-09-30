#!/usr/bin/env python3
"""Deterministic, fail-closed reconciliation for the FAR research corpus.

The curated corpus is Research data.  This program verifies immutable source
bytes, validates its dependency graph, and derives views; it never promotes a
scientific or project status.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parents[1]
CORPUS = Path("research/corpus/corpus-v1.0.json")
OUTPUT = Path("research/corpus/synthesis-v1.0.json")
STATUS = Path("docs/research/current-research-frontier.md")
LEVELS = {"EVIDENCE", "INFERENCE", "HYPOTHESIS", "UNRESOLVED"}
ARCH = {"already_representable_enforceable", "representable_assurance_incomplete", "existing_extension_point", "genuine_architecture_gap", "contradiction", "unresolved"}


def canonical(value: object) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n").encode()


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load(path: Path) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def validate(data: dict, root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    schema = json.loads((ROOT / "schemas/far-research-corpus-v1.schema.json").read_text())
    for error in jsonschema.Draft202012Validator(schema).iter_errors(data):
        errors.append("schema: " + error.message)
    collections = ("sources", "findings", "mechanisms", "conclusions", "frontier")
    ids: dict[str, str] = {}
    for collection in collections:
        rows = data.get(collection)
        if not isinstance(rows, list):
            errors.append(f"{collection} must be a list")
            continue
        for row in rows:
            rid = row.get("id") if isinstance(row, dict) else None
            if not isinstance(rid, str) or not re.fullmatch(r"[A-Z][A-Z0-9-]+", rid):
                errors.append(f"invalid {collection} identity {rid!r}")
            elif rid in ids:
                errors.append(f"duplicate identity {rid}")
            else:
                ids[rid] = collection
    source_ids = {r.get("id") for r in data.get("sources", [])}
    finding_ids = {r.get("id") for r in data.get("findings", [])}
    mechanism_ids = {r.get("id") for r in data.get("mechanisms", [])}
    conclusion_ids = {r.get("id") for r in data.get("conclusions", [])}
    for source in data.get("sources", []):
        if source.get("availability") == "available":
            path = root / source.get("path", "")
            if not path.is_file() or path.is_symlink():
                errors.append(f"source unavailable or unsafe: {source.get('id')}")
            elif digest(path.read_bytes()) != source.get("sha256"):
                errors.append(f"source hash mismatch: {source.get('id')}")
        elif source.get("availability") not in {"missing", "withdrawn"}:
            errors.append(f"invalid availability: {source.get('id')}")
        if source.get("kind") in {"ai_summary", "scheduled_task_summary"} and source.get("evidence_usable"):
            errors.append(f"AI/summary source promoted as evidence: {source.get('id')}")
    for finding in data.get("findings", []):
        if finding.get("epistemic_class") not in LEVELS:
            errors.append(f"invalid epistemic class: {finding.get('id')}")
        refs = finding.get("source_ids", [])
        if not refs or any(ref not in source_ids for ref in refs):
            errors.append(f"finding has missing source: {finding.get('id')}")
        if finding.get("epistemic_class") == "EVIDENCE":
            usable = [s for s in data.get("sources", []) if s.get("id") in refs and s.get("evidence_usable") and s.get("availability") == "available"]
            if not usable:
                errors.append(f"evidence lacks verified available source: {finding.get('id')}")
    for mechanism in data.get("mechanisms", []):
        refs = mechanism.get("finding_ids", [])
        if not refs or any(ref not in finding_ids for ref in refs):
            errors.append(f"mechanism has missing finding: {mechanism.get('id')}")
        if mechanism.get("architecture_class") not in ARCH:
            errors.append(f"invalid architecture class: {mechanism.get('id')}")
        if not mechanism.get("literal_comparison"):
            errors.append(f"missing literal architecture comparison: {mechanism.get('id')}")
    graph: dict[str, list[str]] = {}
    for conclusion in data.get("conclusions", []):
        if conclusion.get("epistemic_class") not in LEVELS:
            errors.append(f"invalid conclusion class: {conclusion.get('id')}")
        refs = conclusion.get("mechanism_ids", [])
        if any(ref not in mechanism_ids for ref in refs):
            errors.append(f"conclusion has missing mechanism: {conclusion.get('id')}")
        deps = conclusion.get("depends_on", [])
        if any(ref not in conclusion_ids for ref in deps):
            errors.append(f"conclusion has missing dependency: {conclusion.get('id')}")
        graph[conclusion.get("id", "")] = deps
    visiting: set[str] = set()
    visited: set[str] = set()
    def visit(node: str) -> None:
        if node in visiting:
            errors.append(f"circular support at {node}")
            return
        if node in visited:
            return
        visiting.add(node)
        for dep in graph.get(node, []): visit(dep)
        visiting.remove(node); visited.add(node)
    for node in graph: visit(node)
    for item in data.get("frontier", []):
        if any(ref not in conclusion_ids for ref in item.get("conclusion_ids", [])):
            errors.append(f"frontier has missing conclusion: {item.get('id')}")
    return sorted(set(errors))


def derive(data: dict) -> dict:
    material = [s["id"] for s in data["sources"] if s.get("material")]
    accounted = sorted({sid for f in data["findings"] for sid in f["source_ids"]} | {s["id"] for s in data["sources"] if s.get("exclusion_reason")})
    return {
        "format_version": "far-research-synthesis/1.0",
        "authority": "Research",
        "corpus_sha256": digest(canonical(data)),
        "material_input_accounting": {"expected": sorted(material), "accounted": accounted, "complete": sorted(material) == accounted},
        "counts": {k: len(data[k]) for k in ("sources", "findings", "mechanisms", "conclusions", "frontier")},
        "mechanisms": [{k: m[k] for k in ("id", "name", "architecture_class", "literal_comparison", "finding_ids")} for m in sorted(data["mechanisms"], key=lambda x:x["id"])],
        "conclusions": sorted(data["conclusions"], key=lambda x:x["id"]),
        "frontier": sorted(data["frontier"], key=lambda x:x["id"]),
        "nonclaims": data["nonclaims"],
    }


def markdown(result: dict) -> str:
    lines = ["# Current FAR research frontier", "", "Status: **Generated Research synthesis; not scientific promotion authority**", "", f"Corpus identity: `{result['corpus_sha256']}`", "", "This view is generated by `tools/reconcile_research_corpus.py`. EVIDENCE records source-bound observations; INFERENCE, HYPOTHESIS, and UNRESOLVED remain distinct. Repetition is not treated as independence or added evidential strength.", "", "## Reconciled hypotheses", "", "| Conclusion | Class | Disposition | Supported statement |", "|---|---|---|---|"]
    for row in result["conclusions"]:
        lines.append(f"| `{row['id']}` | **{row['epistemic_class']}** | `{row['disposition']}` | {row['statement']} |")
    lines += ["", "## Mechanism-to-architecture comparison", "", "| Mechanism | Classification | Literal comparison |", "|---|---|---|"]
    for row in result["mechanisms"]:
        lines.append(f"| `{row['id']}` {row['name']} | `{row['architecture_class']}` | {row['literal_comparison']} |")
    lines += ["", "## Frontier", ""]
    for row in result["frontier"]:
        lines += [f"### {row['id']}: {row['question']}", "", f"**{row['epistemic_class']} — {row['status']}.** {row['next_evidence']}", ""]
    lines += ["## Corpus accounting and nonclaims", "", f"All `{len(result['material_input_accounting']['expected'])}` registered material inputs are accounted for: **{str(result['material_input_accounting']['complete']).lower()}**.", ""]
    lines.extend(f"- {x}" for x in result["nonclaims"])
    return "\n".join(lines) + "\n"


def freeze_external(path: Path, origin: str) -> None:
    raw = path.read_bytes(); sha = digest(raw)
    out = ROOT / "research/corpus/external" / f"{sha}.bin"
    out.parent.mkdir(parents=True, exist_ok=True)
    if out.exists() and out.read_bytes() != raw: raise SystemExit("hash collision")
    out.write_bytes(raw)
    receipt = {"format_version":"far-frozen-input/1.0", "sha256":sha, "size":len(raw), "origin":origin, "authority":"discovery_lead", "executable":False, "primary_evidence_verified":False}
    (out.with_suffix(".json")).write_bytes(canonical(receipt))
    print(out.relative_to(ROOT))


def main() -> int:
    parser=argparse.ArgumentParser(); parser.add_argument("--write", action="store_true"); parser.add_argument("--ingest", type=Path); parser.add_argument("--origin", default="outside_scheduler")
    args=parser.parse_args()
    if args.ingest: freeze_external(args.ingest, args.origin); return 0
    data=load(CORPUS); errors=validate(data)
    if errors:
        print("\n".join(errors), file=sys.stderr); return 1
    result=derive(data)
    if not result["material_input_accounting"]["complete"]:
        print("material input accounting incomplete", file=sys.stderr); return 1
    outputs={OUTPUT:canonical(result), STATUS:markdown(result).encode()}
    if args.write:
        for path, raw in outputs.items(): (ROOT/path).write_bytes(raw)
    else:
        for path, raw in outputs.items():
            if not (ROOT/path).is_file() or (ROOT/path).read_bytes()!=raw:
                print(f"stale generated output: {path}", file=sys.stderr); return 1
    print(f"research corpus valid: {result['corpus_sha256']}")
    return 0

if __name__ == "__main__": raise SystemExit(main())
