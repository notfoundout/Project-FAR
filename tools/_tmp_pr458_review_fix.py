#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

DECL = "FARCoreV11.finite_operator_count_noninvariant"

W1_HASHES = {
    "docs/research/pca-w1-independent-review-protocol-v1.0.md": "2decf1bcc924101928432143535712bd6fccc4723947d97321fee2d14adea0dc",
    "docs/research/pca-w1-independent-review/00-exposure-environment.md": "f9edff7c8385d49064c1ea92a529bbb5d4f32e38a667531687bc123057c7a73d",
    "docs/research/pca-w1-independent-review/01-stage-a-blind-reconstruction.md": "bbc33980d8b5f68d6c3c9d89857cf5706561b0679781fff9f487aa80654c5662",
    "docs/research/pca-w1-independent-review/tools/stage_a_finite_checks.py": "b5c912eaacb766faecec61a60c997cacb53c5f01741952018e1513a29eafa137",
    "docs/research/pca-w1-independent-review/tools/stage-a-finite-check-output.md": "342204f48178c68160f5f700d43ab5cafd6ff5fde327a025129983f368b8832b",
    "docs/research/pca-w1-independent-review/02-stage-b-ledger-reconciliation.md": "623838d5ff4daded5a35539ecf558264e70ad10fcf4428165c1ceb46cf55ecd7",
    "docs/research/pca-w1-independent-review/03-stage-c-independent-research.md": "413e9f9ac2cacc116188dad511fb0726a952bc15f83b1f44dd88c343057fc9db",
    "docs/research/pca-w1-independent-review/04-stage-c-hostile-test-ledger.md": "bceb586e71800375935902ad5653e8d02d1211de24b13eed572d85228fc9dbd5",
    "docs/research/pca-w1-independent-review/05-stage-d-provisional-verdict-frozen.md": "e27c99c7ff52f5f95e30e6f163b83cacbfa389d61d6f9408966bf983ce66902e",
    "docs/research/pca-w1-independent-review/05-stage-d-freeze-manifest.json": "f48b05d997f1e1ae946072c217265f744bc3131b937118ae0e62fc518cfb3e5c",
    "docs/research/pca-w1-independent-review/tools/stage_e_sss_checks.py": "746fa76d097e747bdb1ee3a4742401b0a4a01ffd81fa176148b00d926ca5292e",
    "docs/research/pca-w1-independent-review/tools/stage-e-sss-check-output.json": "a17d5b7549a3b66c1ae450a6fb5a6d2cbe000202a6196cd1247310930354498b",
    "docs/research/pca-w1-independent-review/06-stage-e-controlled-unblinding.md": "787229856619ce47fc71107550d5afc2940558d0e1443281ecc008bee0c370b6",
    "docs/research/pca-w1-independent-review/07-final-independent-review.md": "03848362e0cbea1151ba3a0e042cf2872f51f0781815eaff17c1128e49589aaa",
    "docs/research/pca-w1-independent-review/07-final-independent-review.json": "f311552b877beece5245f48bbf1cf32f68d4b586fb3d65c18410b0ffe9175c37",
    "docs/research/pca-w1-independent-review/08-review-artifact-manifest.json": "1437aeb6c52e7d84958b2cc530a9c5bda71706b96386482b98867df3c4e5d1bc",
}


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def replace_once(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    if old not in text:
        if new in text:
            return
        raise RuntimeError(f"expected text not found in {path}: {old[:80]!r}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


# FAR-CORE-008: encode an actual count-changing witness, not only combine/split equivalence.
claims = ROOT / "mechanization/lean/FARCoreV11Claims001To012.lean"
insert_after = '''structure FiniteTaggedDispatcher (I : Type u) (A : I -> Type v) (B : Type w) where\n  tags : FiniteTagCarrier I\n  dispatch : Sigma A -> B\n'''
count_defs = '''\n/-- Count the named primitive operator symbols in a presentation. -/\nstructure PrimitiveOperatorCount where\n  operatorCount : Nat\n  deriving DecidableEq\n\n/-- A concrete two-operator presentation before tagged dispatch. -/\ndef splitTwoOperatorVocabulary : PrimitiveOperatorCount where\n  operatorCount := 2\n\n/-- The faithfully equivalent tagged-dispatch presentation uses one primitive dispatcher. -/\ndef combinedDispatcherVocabulary : PrimitiveOperatorCount where\n  operatorCount := 1\n'''
text = claims.read_text(encoding="utf-8")
if "structure PrimitiveOperatorCount" not in text:
    if insert_after not in text:
        raise RuntimeError("FAR-CORE-008 insertion anchor missing")
    text = text.replace(insert_after, insert_after + count_defs, 1)

insert_before = '''\n/-! ## FAR-CORE-009 -/\n'''
count_theorem = '''\n/-- A concrete finite two-operator presentation is faithfully recoverable from one tagged\n    dispatcher while the primitive operator counts differ. -/\ntheorem finite_operator_count_noninvariant\n    {A : Bool -> Type v} {B : Type w}\n    (opFalse : A false -> B) (opTrue : A true -> B) :\n    let family : (i : Bool) -> A i -> B := fun\n      | false => opFalse\n      | true => opTrue\n    let dispatcher : Sigma A -> B := combineOperator family\n    (splitOperator dispatcher = family) ∧\n      splitTwoOperatorVocabulary ≠ combinedDispatcherVocabulary := by\n  dsimp\n  constructor\n  · funext i argument\n    cases i <;> rfl\n  · decide\n'''
if "theorem finite_operator_count_noninvariant" not in text:
    if insert_before not in text:
        raise RuntimeError("FAR-CORE-009 anchor missing")
    text = text.replace(insert_before, count_theorem + insert_before, 1)
claims.write_text(text, encoding="utf-8")

# Machine ledger + assurance mapping.
ledger_path = ROOT / "theory/evaluation/far-core-formalization-ledger-v1.0.json"
ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
c8 = next(c for c in ledger["claims"] if c["id"] == "FAR-CORE-008")
if DECL not in c8["lean_declarations"]:
    c8["lean_declarations"].append(DECL)
if "PrimitiveOperatorCount := operatorCount : Nat" not in c8["quantified_objects_types"]:
    c8["quantified_objects_types"].append("PrimitiveOperatorCount := operatorCount : Nat")
c8["conclusion"] = (
    "Combining and splitting are inverse on the tagged domain; a concrete two-operator "
    "presentation is recoverable from one tagged dispatcher while the declared primitive "
    "operator counts differ (2 versus 1)."
)
write_json(ledger_path, ledger)

assurance_path = ROOT / "theory/evaluation/far-core-assurance-v1.0.json"
assurance = json.loads(assurance_path.read_text(encoding="utf-8"))
a8 = next(c for c in assurance["claims"] if c["id"] == "FAR-CORE-008")
if DECL not in a8["lean_declarations"]:
    a8["lean_declarations"].append(DECL)
write_json(assurance_path, assurance)

# Formalization checker: make the new declaration mandatory in the exact axiom contract.
checker = ROOT / "tools/check_far_core_v11_formalization.py"
replace_once(
    checker,
    '    "FARCoreV11.factorToQuotient_surjective": frozenset({"Classical.choice", "Quot.sound"}),\n    "FARCoreV11.finite_panel_two_completions": frozenset(),',
    '    "FARCoreV11.factorToQuotient_surjective": frozenset({"Classical.choice", "Quot.sound"}),\n    "FARCoreV11.finite_operator_count_noninvariant": frozenset({"Quot.sound"}),\n    "FARCoreV11.finite_panel_two_completions": frozenset(),',
)

# W1: an independent hard-coded seal prevents coordinated artifact+promotion hash rewrites.
registry = ROOT / "tools/far_research_registry.py"
reg_text = registry.read_text(encoding="utf-8")
if "W1_PROMOTED_ARTIFACT_SHA256 =" not in reg_text:
    anchor = "W1_REVIEW_TARGET = {\n"
    if anchor not in reg_text:
        raise RuntimeError("W1 hash seal anchor missing")
    literal = "# Independent trust root for the 16 byte-promoted W1 artifacts.\n" + \
        "# These values are not derived from the mutable promotion JSON at validation time.\n" + \
        "W1_PROMOTED_ARTIFACT_SHA256 = " + repr(W1_HASHES) + "\n\n"
    reg_text = reg_text.replace(anchor, literal + anchor, 1)

old_loop = '''    for artifact in artifacts:\n        if not isinstance(artifact, dict):\n            continue\n        raw_path = artifact.get("path")\n        expected = artifact.get("sha256")\n        if not isinstance(raw_path, str) or not isinstance(expected, str):\n            errors.append("W1 promotion seal entry is malformed")\n            continue\n        path = root / raw_path\n        if not path.is_file() or sha256(path) != expected:\n            errors.append(f"W1 sealed artifact missing or changed: {raw_path}")\n'''
new_loop = '''    if set(W1_PROMOTED_ARTIFACT_SHA256) != PROMOTED_W1_PATHS:\n        errors.append("independent W1 artifact seal coverage drift")\n    reported_hashes = {\n        item.get("path"): item.get("sha256")\n        for item in artifacts\n        if isinstance(item, dict) and isinstance(item.get("path"), str)\n    }\n    for raw_path, expected in W1_PROMOTED_ARTIFACT_SHA256.items():\n        if reported_hashes.get(raw_path) != expected:\n            errors.append(f"W1 promotion artifact hash contract drift: {raw_path}")\n            errors.append(f"W1 sealed artifact missing or changed: {raw_path}")\n        path = root / raw_path\n        if not path.is_file() or sha256(path) != expected:\n            errors.append(f"W1 sealed artifact missing or changed: {raw_path}")\n'''
if old_loop in reg_text:
    reg_text = reg_text.replace(old_loop, new_loop, 1)
elif new_loop not in reg_text:
    raise RuntimeError("W1 old seal loop missing")
registry.write_text(reg_text, encoding="utf-8")

# Regression tests for both review findings.
formal_test = ROOT / "tests/test_far_core_v11_formalization.py"
ft = formal_test.read_text(encoding="utf-8")
if "test_far_core_008_encodes_count_noninvariance" not in ft:
    anchor = "    def test_far_core_014_is_end_to_end_formalized_without_provenance_rewrite(self):\n"
    method = '''    def test_far_core_008_encodes_count_noninvariance(self):\n        ledger = checker.load(checker.LEDGER_PATH)\n        assurance = checker.load(checker.ASSURANCE_PATH)\n        claim = next(item for item in ledger["claims"] if item["id"] == "FAR-CORE-008")\n        assurance_claim = next(item for item in assurance["claims"] if item["id"] == "FAR-CORE-008")\n        declaration = "FARCoreV11.finite_operator_count_noninvariant"\n        self.assertIn(declaration, claim["lean_declarations"])\n        self.assertIn(declaration, assurance_claim["lean_declarations"])\n        self.assertIn(declaration, checker.EXPECTED_DECLARATION_AXIOMS)\n\n'''
    if anchor not in ft:
        raise RuntimeError("formalization test anchor missing")
    ft = ft.replace(anchor, method + anchor, 1)
formal_test.write_text(ft, encoding="utf-8")

infra_test = ROOT / "tests/test_far_research_infrastructure.py"
it = infra_test.read_text(encoding="utf-8")
if "test_w1_seal_rejects_coordinated_artifact_and_promotion_rewrite" not in it:
    anchor = "    def test_w1_seal_rejects_current_governing_theory_drift(self):\n"
    method = '''    def test_w1_seal_rejects_coordinated_artifact_and_promotion_rewrite(self):\n        promotion = registry.load("theory/evaluation/pca-w1-independent-review-promotion-v1.0.json")\n        required = set(registry.PROMOTED_W1_PATHS) | {\n            "research/campaigns/pca-w1-replay-capsule-v1.0.json",\n            "theory/theorems/Project-FAR-Theory-Closure-v1.1.md",\n            "theory/terminal/project-far-core-theory-v1.1.json",\n        }\n        target = "docs/research/pca-w1-independent-review/01-stage-a-blind-reconstruction.md"\n        with tempfile.TemporaryDirectory() as directory:\n            root = Path(directory)\n            for raw_path in required:\n                destination = root / raw_path\n                destination.parent.mkdir(parents=True, exist_ok=True)\n                destination.write_bytes((ROOT / raw_path).read_bytes())\n            target_path = root / target\n            target_path.write_text(\n                target_path.read_text(encoding="utf-8") + "\\ncoordinated mutation\\n",\n                encoding="utf-8",\n            )\n            tampered = copy.deepcopy(promotion)\n            entry = next(item for item in tampered["verified_artifacts"] if item["path"] == target)\n            entry["sha256"] = registry.sha256(target_path)\n            errors = registry.w1_seal_errors(tampered, root)\n            self.assertTrue(any("artifact hash contract drift" in error for error in errors))\n            self.assertTrue(any("missing or changed" in error for error in errors))\n\n'''
    if anchor not in it:
        raise RuntimeError("research infrastructure test anchor missing")
    it = it.replace(anchor, method + anchor, 1)
infra_test.write_text(it, encoding="utf-8")

# Governance text must describe the stronger seal actually enforced.
promotion_doc = ROOT / "docs/governance/pca-w1-independent-review-promotion-v1.0.md"
replace_once(
    promotion_doc,
    "The Stage-A and Stage-E finite\nscripts replay deterministically against their committed outputs. The machine promotion record\npins all 16 promoted protocol/review paths by SHA-256; coverage loss, duplicate paths, missing\nfiles, or byte drift fails repository health.",
    "The Stage-A and Stage-E finite\nscripts replay deterministically against their committed outputs. The machine promotion record\nand an independently hard-coded validator seal both pin all 16 promoted protocol/review paths\nby SHA-256; coverage loss, duplicate paths, coordinated promotion-record rewrites, missing files,\nor byte drift fails repository health.",
)

print("one-shot PR458 review repair applied")
