import json
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
LEAN = ROOT / "mechanization/lean/FARCanonicalBridge.lean"
REGISTRY = ROOT / "theory/terminal/far-canonical-bridge-v1.0.json"


class FARCanonicalBridgeAlignmentTests(unittest.TestCase):
    def test_no_unsafe_proof_escape(self):
        text = LEAN.read_text(encoding="utf-8")
        for forbidden in ("axiom ", "sorry", "admit", "unsafe"):
            self.assertNotIn(forbidden, text)

    def test_all_six_bridges_are_explicit(self):
        text = LEAN.read_text(encoding="utf-8")
        required = [
            "uniqueFactorizationForFAR",
            "representationInvariantRecovery",
            "quotientSeparationForFAR",
            "allReasoningInvariantsDefinable",
            "everyAdmissibleExtensionConservative",
            "warrantedScopeEmbedsIntoFAR",
        ]
        for token in required:
            self.assertIn(token, text)

    def test_registry_is_partial_not_full(self):
        data = json.loads(REGISTRY.read_text(encoding="utf-8"))
        self.assertEqual(data["current_adjudication"], "partial")
        self.assertEqual(len(data["remaining_far_specific_bridges"]), 6)

    def test_abstract_instantiation_is_not_treated_as_far_proof(self):
        data = json.loads(REGISTRY.read_text(encoding="utf-8"))
        self.assertIn(
            "abstract theorem instantiation alone proves FAR canonicality",
            data["nonclaims"],
        )


if __name__ == "__main__":
    unittest.main()
