from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "theory/evaluation/comparative-representation/experiments/CRE-002"
RESULT = BASE / "execution/cre002-comparison.json"
VOCABS = ["CRE-001-VOCAB-A-1.0", "CRE-001-VOCAB-B-1.0", "CRE-001-VOCAB-C-1.0"]


class Cre002ExecutionTests(unittest.TestCase):
    def test_execution_artifacts_match_deterministic_regeneration(self) -> None:
        result = subprocess.run(
            [sys.executable, "tools/cre002_execute.py", "--check"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_all_vocabularies_receive_preregistered_unsupported_outcome(self) -> None:
        summary = json.loads(RESULT.read_text())
        self.assertEqual([row["vocabulary_id"] for row in summary["candidates"]], VOCABS)
        for row in summary["candidates"]:
            self.assertEqual(row["outcome"], "unsupported")
            self.assertFalse(row["native_compilation_attempted"])
            self.assertFalse(row["behavioral_verification_attempted"])
            self.assertIsNone(row["shortest_counterexample"])
        self.assertFalse(summary["licensing_audit"]["all_required_commitments_licensed"])

    def test_missing_capabilities_are_explicit(self) -> None:
        summary = json.loads(RESULT.read_text())
        missing = set(summary["licensing_audit"]["missing_constructs"])
        self.assertEqual(
            missing,
            {"D_nondeterminism", "D_concurrency", "D_priority", "D_provenance", "D_rule_modification"},
        )

    def test_mutation_audit_passes(self) -> None:
        summary = json.loads(RESULT.read_text())
        mutation = summary["mutation_audit"]
        self.assertTrue(mutation["passed"])
        self.assertTrue(all(case["detected"] for case in mutation["cases"]))

    def test_results_preserve_nonclaims(self) -> None:
        summary = json.loads(RESULT.read_text())
        required = {
            "universal sufficiency", "primitive-only sufficiency", "necessity",
            "minimality", "independence", "superiority", "FAR proof",
            "universal structure of reasoning",
            "the informal vocabularies are inherently incapable of representing CRE-002",
            "behavioral failure of any candidate vocabulary",
        }
        self.assertTrue(required.issubset(summary["nonclaims"]))
        self.assertFalse(summary["aggregate"]["existential_complete"])
        self.assertFalse(summary["aggregate"]["reproducible_complete"])

    def test_execution_was_prospectively_authorized(self) -> None:
        control = json.loads((BASE / "execution-lock.json").read_text())
        self.assertTrue(control["execution_permitted"])


if __name__ == "__main__":
    unittest.main()
