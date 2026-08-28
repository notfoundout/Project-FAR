#!/usr/bin/env python3
"""Validate FAR-CORE v1.1 formalization alignment and generate its inventory/views."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import jsonschema  # noqa: E402

LEDGER_PATH = "theory/evaluation/far-core-formalization-ledger-v1.0.json"
ASSURANCE_PATH = "theory/evaluation/far-core-assurance-v1.0.json"
CORE_PATH = "theory/terminal/project-far-core-theory-v1.1.json"
INVENTORY_PATH = "artifacts/mechanization/lean-inventory-v1.0.json"
REPORT_PATH = "docs/mechanization/far-core-v1.1-formalization.md"
INVENTORY_SCHEMA = "schemas/far-lean-inventory-v1.schema.json"
W2_MODULES = {
    "mechanization/lean/FARCoreV11Substrate.lean",
    "mechanization/lean/FARCoreV11Claims001To012.lean",
    "mechanization/lean/FARCoreV11Omega.lean",
    "mechanization/lean/FARCoreV11SSS.lean",
    "mechanization/lean/FARCoreV11Mutations.lean",
    "mechanization/lean/FARCoreV11AxiomAudit.lean",
}
EXPECTED_KERNEL_AXIOMS = {
    "FAR-CORE-001": ["Classical.choice"],
    "FAR-CORE-002": ["Classical.choice", "Quot.sound"],
    "FAR-CORE-003": ["Quot.sound"],
    "FAR-CORE-004": ["none"],
    "FAR-CORE-005": ["none"],
    "FAR-CORE-006": ["Classical.choice", "Quot.sound", "propext"],
    "FAR-CORE-007": ["none"],
    "FAR-CORE-008": ["Quot.sound"],
    "FAR-CORE-009": ["none"],
    "FAR-CORE-010": ["Quot.sound", "propext"],
    "FAR-CORE-011": ["none"],
    "FAR-CORE-012": ["none"],
    "FAR-CORE-013": ["none"],
    "FAR-CORE-014": ["propext"],
}
FORBIDDEN = re.compile(r"(?m)^\s*(?:axiom\b|sorry\b|admit\b|unsafe\s+(?:def|theorem)\b)")
DECLARATION = re.compile(
    r"(?m)^\s*(?:(?:noncomputable|protected)\s+)?"
    r"(?:def|theorem|structure|inductive|abbrev)\s+([A-Za-z_][A-Za-z0-9_']*)"
)


def load(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def declared(text: str, qualified: str) -> bool:
    terminal = qualified.rsplit(".", 1)[-1]
    return bool(re.search(
        rf"(?m)^\s*(?:(?:noncomputable|protected)\s+)?"
        rf"(?:def|theorem|structure|inductive|abbrev)\s+{re.escape(terminal)}\b",
        text,
    ))


def inventory(ledger: dict) -> dict:
    files = []
    forbidden_count = 0
    for path in sorted((ROOT / "mechanization/lean").glob("*.lean")):
        relative = path.relative_to(ROOT).as_posix()
        text = path.read_text(encoding="utf-8")
        forbidden_count += len(FORBIDDEN.findall(text))
        files.append({
            "path": relative,
            "sha256": digest(path),
            "line_count": len(text.splitlines()),
            "imports": sorted(set(re.findall(r"(?m)^import\s+([^\s]+)\s*$", text))),
            "declarations": sorted(set(DECLARATION.findall(text))),
            "role": "W2_CORE_V1_1" if relative in W2_MODULES else "LEGACY_OR_OTHER_SCOPE",
        })
    statuses = [claim["formalization_status"] for claim in ledger["claims"]]
    checks = {claim["kernel_check"] for claim in ledger["claims"]}
    return {
        "schema_version": "1.0",
        "inventory_id": "PROJECT-FAR-LEAN-INVENTORY-1.0",
        "authority": "generated_inventory_not_theory_authority",
        "toolchain": ledger["lean_toolchain"],
        "files": files,
        "w2_summary": {
            "formalized": statuses.count("FORMALIZED"),
            "partial_obstruction": statuses.count("PARTIAL/OBSTRUCTION"),
            "contradiction_reopen_required": statuses.count("CONTRADICTION/REOPEN REQUIRED"),
            "kernel_check": checks.pop() if len(checks) == 1 else "MIXED",
            "forbidden_placeholders": forbidden_count,
        },
    }


def alignment_errors(ledger: dict, assurance: dict, core: dict, generated: dict) -> list[str]:
    errors: list[str] = []
    expected_ids = [f"FAR-CORE-{index:03d}" for index in range(1, 15)]
    ledger_claims = ledger["claims"]
    assurance_by_id = {item["id"]: item for item in assurance["claims"]}
    core_by_id = {item["id"]: item for item in core["claims"]}
    axiom_audit = (ROOT / "mechanization/lean/FARCoreV11AxiomAudit.lean").read_text(encoding="utf-8")
    if [item["id"] for item in ledger_claims] != expected_ids:
        errors.append("formalization ledger must cover FAR-CORE-001 through 014 in order")
    if set(assurance_by_id) != set(expected_ids) or set(core_by_id) != set(expected_ids):
        errors.append("core/assurance/formalization claim coverage differs")
    for item in ledger_claims:
        identifier = item["id"]
        if item["canonical_prose_statement"] != core_by_id[identifier]["claim"]:
            errors.append(f"{identifier}: canonical prose drift")
        module = ROOT / item["intended_lean_module"]
        if not module.is_file():
            errors.append(f"{identifier}: missing Lean module {item['intended_lean_module']}")
            continue
        text = module.read_text(encoding="utf-8")
        for declaration in item["lean_declarations"]:
            if not declared(text, declaration):
                errors.append(f"{identifier}: missing declaration {declaration}")
            if f"#print axioms {declaration}" not in axiom_audit:
                errors.append(f"{identifier}: declaration absent from kernel-assumption audit: {declaration}")
        if item["kernel_axioms"] != EXPECTED_KERNEL_AXIOMS[identifier]:
            errors.append(f"{identifier}: recorded kernel assumptions drifted")
        assurance_status = item["formalization_status"].replace("/", "_")
        if assurance_by_id[identifier]["formalization_status"] != assurance_status:
            errors.append(f"{identifier}: assurance/formalization status drift")
        if assurance_by_id[identifier]["lean_declarations"] != item["lean_declarations"]:
            errors.append(f"{identifier}: assurance/ledger Lean declaration drift")
        for source in item["source_locations"]:
            source_path = ROOT / source["path"]
            if not source_path.is_file() or digest(source_path) != source["sha256"]:
                errors.append(f"{identifier}: canonical source hash drift at {source['path']}")
        if item["formalization_status"] == "FORMALIZED" and item["obstruction"]["classification"] != "none":
            errors.append(f"{identifier}: formalized claim retains an obstruction")
    if [item["formalization_status"] for item in ledger_claims[:13]] != ["FORMALIZED"] * 13:
        errors.append("FAR-CORE-001 through 013 must be FORMALIZED")
    last = ledger_claims[-1]
    if last["formalization_status"] != "PARTIAL/OBSTRUCTION":
        errors.append("FAR-CORE-014 must remain PARTIAL/OBSTRUCTION until actual MLL witnesses compile")
    if last["obstruction"]["classification"] == "none":
        errors.append("FAR-CORE-014 partial status has no classified obstruction")
    if core_by_id["FAR-CORE-014"]["status"] != "supported_derived":
        errors.append("FAR-CORE-014 historical/application provenance status was overwritten")
    if assurance_by_id["FAR-CORE-014"]["truth_disposition"] != "PROVED":
        errors.append("FAR-CORE-014 truth disposition was conflated with provenance")
    if generated["w2_summary"] != {
        "formalized": 13,
        "partial_obstruction": 1,
        "contradiction_reopen_required": 0,
        "kernel_check": "PASS",
        "forbidden_placeholders": 0,
    }:
        errors.append(f"unexpected W2 inventory summary: {generated['w2_summary']}")
    mutations = (ROOT / "mechanization/lean/FARCoreV11Mutations.lean").read_text(encoding="utf-8")
    for item in ledger_claims:
        for control in item["mutation_negative_controls"]:
            if control.startswith("FARCoreV11Mutations.") and not declared(mutations, control):
                errors.append(f"{item['id']}: missing mutation control {control}")
    return sorted(set(errors))


def render_report(ledger: dict, generated: dict) -> str:
    rows = []
    for claim in ledger["claims"]:
        declarations = "<br>".join(f"`{value}`" for value in claim["lean_declarations"])
        axioms = "<br>".join(f"`{value}`" for value in claim["kernel_axioms"])
        obstruction = "—" if claim["obstruction"]["classification"] == "none" else claim["obstruction"]["details"]
        rows.append(
            f"| `{claim['id']}` | `{claim['formalization_status']}` | `{claim['kernel_check']}` | "
            f"{axioms} | {declarations} | {obstruction} |"
        )
    w2_files = [item for item in generated["files"] if item["role"] == "W2_CORE_V1_1"]
    file_rows = [
        f"| `{item['path']}` | `{item['sha256']}` | {item['line_count']} | "
        f"{', '.join(f'`{value}`' for value in item['imports']) or 'none'} |"
        for item in w2_files
    ]
    obstruction = ledger["claims"][-1]["obstruction"]
    return """# FAR-CORE v1.1 proof-assistant formalization

Status: **Generated W2 assurance view; not governing theory authority**

Sources: [`theory/evaluation/far-core-formalization-ledger-v1.0.json`](../../theory/evaluation/far-core-formalization-ledger-v1.0.json)
and [`artifacts/mechanization/lean-inventory-v1.0.json`](../../artifacts/mechanization/lean-inventory-v1.0.json).
Edit the machine ledger or Lean sources and regenerate this view.

Lean proves machine-checked derivations relative to the encoded premises. It does not establish
novelty, empirical validity, universal architecture, or correctness of an unencoded narrative
application bridge. The W1 truth verdicts and proof-assistant status remain separate dimensions.

## Outcome matrix

| Claim | W2 outcome | Kernel | Kernel assumptions | Declarations | Obstruction |
|---|---|---|---|---|---|
""" + "\n".join(rows) + f"""

## FAR-CORE-014 governed obstruction

- Classification: `{obstruction['classification']}`
- Affected surface: {obstruction['affected_surface']}
- Reproducible detail: {obstruction['details']}
- Allowed resolution: {obstruction['allowed_resolution']}

This is not a refutation. The decoder enumeration, Boolean witness-profile theorem, conditional
hyperedge factorization, and conditional frontier factorization are kernel-checked. What is absent
is an end-to-end Lean derivation of the actual MLL witness facts.

## W2 module inventory

| File | SHA-256 | Lines | Imports |
|---|---|---:|---|
""" + "\n".join(file_rows) + """

The inventory also records every pre-existing Lean file as `LEGACY_OR_OTHER_SCOPE`. Those files
were searched and retained; they do not silently count as coverage of FAR-CORE-001--014.
"""


def expected() -> tuple[dict, str, list[str]]:
    ledger = load(LEDGER_PATH)
    assurance = load(ASSURANCE_PATH)
    core = load(CORE_PATH)
    for exc in jsonschema.Draft202012Validator(load("schemas/far-core-formalization-ledger-v1.schema.json")).iter_errors(ledger):
        raise ValueError(f"formalization ledger schema: {exc.message}")
    generated = inventory(ledger)
    for exc in jsonschema.Draft202012Validator(load(INVENTORY_SCHEMA)).iter_errors(generated):
        raise ValueError(f"Lean inventory schema: {exc.message}")
    return generated, render_report(ledger, generated), alignment_errors(ledger, assurance, core, generated)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args(argv)
    try:
        generated, report, errors = expected()
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"FAIL: {exc}")
        return 1
    if errors:
        print("FAIL: " + "; ".join(errors))
        return 1
    outputs = {
        INVENTORY_PATH: json.dumps(generated, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        REPORT_PATH: report,
    }
    if args.write:
        for path, content in outputs.items():
            target = ROOT / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8")
        print("wrote FAR-CORE v1.1 Lean inventory and report")
        return 0
    stale = [path for path, content in outputs.items()
             if not (ROOT / path).is_file() or (ROOT / path).read_text(encoding="utf-8") != content]
    if stale:
        print("FAIL: stale generated formalization outputs: " + ", ".join(stale))
        return 1
    print("FAR-CORE v1.1 formalization alignment: PASS (13 FORMALIZED, 1 PARTIAL/OBSTRUCTION)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
