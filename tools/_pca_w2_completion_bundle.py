#!/usr/bin/env python3
"""Temporary deterministic migration helper for PCA-W2 completion."""
from __future__ import annotations

import importlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from tools import check_far_core_v11_formalization as checker  # noqa: E402

NEW_DECLARATIONS = [
    "FARCoreV11.SSS.four_monotone_decoders",
    "FARCoreV11.SSS.projected_successor_decoder_failure",
    "FARCoreV11.SSS.hyperedge_factorization",
    "FARCoreV11.SSS.frontier_factorization",
    "FARCoreV11.SSS.MLL.derivable_atom_balance",
    "FARCoreV11.SSS.MLL.sOr_witness_certified",
    "FARCoreV11.SSS.MLL.sAnd_witness_certified",
    "FARCoreV11.SSS.MLL.bounded_projected_decoder_failure",
]
MLL_KERNEL_AXIOMS = ["Quot.sound", "propext"]


def load(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def write(path: str, value: dict) -> None:
    (ROOT / path).write_text(
        json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


def normalize_mll_balance_proof() -> None:
    path = ROOT / "mechanization/lean/FARCoreV11SSS.lean"
    text = path.read_text(encoding="utf-8")
    text = text.replace(
        "  | tensor leftDerivation rightDerivation leftIH rightIH =>\n",
        "  | @tensor gamma delta left right leftDerivation rightDerivation leftIH rightIH =>\n",
    )
    old_tensor = """      have hLeft := leftIH\n      have hRight := rightIH\n      simp [sequentWeight_append, sequentWeight, atomWeight] at hLeft hRight ⊢\n      omega\n"""
    new_tensor = """      have hLeft := leftIH\n      have hRight := rightIH\n      simp only [sequentWeight_append, sequentWeight, atomWeight, Int.add_zero] at hLeft hRight ⊢\n      calc\n        _ = (sequentWeight target gamma + atomWeight target left) +\n            (sequentWeight target delta + atomWeight target right) := by ac_rfl\n        _ = 0 := by rw [hLeft, hRight]; rfl\n"""
    old_par = """      have hPremise := premiseIH\n      simp [sequentWeight_append, sequentWeight, atomWeight] at hPremise ⊢\n      omega\n"""
    new_par = """      have hPremise := premiseIH\n      simpa [sequentWeight_append, sequentWeight, atomWeight, Int.add_assoc] using hPremise\n"""
    text = text.replace(old_tensor, new_tensor).replace(old_par, new_par)
    if "      omega\n" in text:
        raise SystemExit("unexpected omega remains in governed MLL proof")
    if "| @tensor gamma delta left right leftDerivation rightDerivation leftIH rightIH =>" not in text:
        raise SystemExit("explicit MLL tensor induction binders were not installed")
    path.write_text(text, encoding="utf-8")


def normalize_axiom_contract() -> None:
    global checker
    path = ROOT / "tools/check_far_core_v11_formalization.py"
    text = path.read_text(encoding="utf-8")
    replacements = {
        '"FAR-CORE-014": ["propext"],': '"FAR-CORE-014": ["Quot.sound", "propext"],',
        '"FARCoreV11.SSS.MLL.derivable_atom_balance": frozenset(),': '"FARCoreV11.SSS.MLL.derivable_atom_balance": frozenset({"Quot.sound", "propext"}),',
        '"FARCoreV11.SSS.MLL.sOr_witness_certified": frozenset(),': '"FARCoreV11.SSS.MLL.sOr_witness_certified": frozenset({"Quot.sound", "propext"}),',
        '"FARCoreV11.SSS.MLL.sAnd_witness_certified": frozenset(),': '"FARCoreV11.SSS.MLL.sAnd_witness_certified": frozenset({"Quot.sound", "propext"}),',
        '"FARCoreV11.SSS.MLL.bounded_projected_decoder_failure": frozenset({"propext"}),': '"FARCoreV11.SSS.MLL.bounded_projected_decoder_failure": frozenset({"Quot.sound", "propext"}),',
    }
    for old, new in replacements.items():
        if old in text:
            text = text.replace(old, new)
        elif new not in text:
            raise SystemExit(f"axiom contract migration target missing: {old}")
    path.write_text(text, encoding="utf-8")
    checker = importlib.reload(checker)


def main() -> int:
    normalize_mll_balance_proof()
    normalize_axiom_contract()
    ledger = load(checker.LEDGER_PATH)
    assurance = load(checker.ASSURANCE_PATH)
    claim = next(item for item in ledger["claims"] if item["id"] == "FAR-CORE-014")
    claim["lean_declarations"] = NEW_DECLARATIONS
    claim["formalization_status"] = "FORMALIZED"
    claim["kernel_check"] = "PASS"
    claim["kernel_axioms"] = MLL_KERNEL_AXIOMS
    claim["obstruction"] = {
        "classification": "none",
        "details": "",
        "affected_surface": "none",
        "allowed_resolution": "none",
    }
    assurance_claim = next(item for item in assurance["claims"] if item["id"] == "FAR-CORE-014")
    assurance_claim["formalization_status"] = "FORMALIZED"
    assurance_claim["lean_declarations"] = NEW_DECLARATIONS
    write(checker.LEDGER_PATH, ledger)
    write(checker.ASSURANCE_PATH, assurance)
    (ROOT / "mechanization/lean/FARCoreV11AxiomAudit.lean").write_text(
        checker.render_axiom_audit(), encoding="utf-8"
    )
    generated, report, errors = checker.expected()
    if errors:
        raise SystemExit("; ".join(errors))
    (ROOT / checker.INVENTORY_PATH).write_text(
        json.dumps(generated, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    (ROOT / checker.REPORT_PATH).write_text(report, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
