from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "mechanization/lean/ProcessSemantics.lean"
DOC = ROOT / "mechanization/lean/PROCESS-SEMANTICS.md"


class ProcessSemanticsTests(unittest.TestCase):
    def test_required_results_exist(self):
        text = LEAN.read_text(encoding="utf-8")
        required = [
            "structure IndependentProcessModel",
            "def extractProcessSpecification",
            "def compileIndependentModel",
            "def EndToEndPreservation",
            "theorem compileIndependentModel_preserves_behavior",
            "def lossyCompiler",
            "theorem lossyCompiler_rejected_when_transition_exists",
            "def deductiveModel",
            "def defeasibleLegalModel",
            "def probabilisticDecisionModel",
            "def ruleModifyingModel",
            "theorem deductive_end_to_end",
            "theorem defeasible_legal_end_to_end",
            "theorem probabilistic_end_to_end",
            "theorem rule_modifying_end_to_end",
            "theorem lossy_deductive_rejected",
            "theorem lossy_legal_rejected",
            "theorem lossy_probabilistic_rejected",
            "theorem lossy_rule_modifying_rejected",
        ]
        for marker in required:
            with self.subTest(marker=marker):
                self.assertIn(marker, text)

    def test_no_axioms_or_placeholder_proofs(self):
        text = LEAN.read_text(encoding="utf-8")
        for token in ("axiom", "sorry", "admit"):
            with self.subTest(token=token):
                self.assertIsNone(re.search(rf"(?m)^\s*{token}\b", text))

    def test_documentation_states_claim_boundary(self):
        text = DOC.read_text(encoding="utf-8").lower()
        self.assertIn("independent of far representation types", text)
        self.assertIn("do not prove universal coverage", text)
        self.assertIn("terminal status is preserved as an observable encoding", text)
        self.assertIn("lossy compiler", text)
        self.assertIn("model-theoretic independence", text)


if __name__ == "__main__":
    unittest.main()
