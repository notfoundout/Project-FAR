from __future__ import annotations

import re
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class CRE001SemanticRegressionTests(unittest.TestCase):
    def test_semantics_are_prospective_not_retrospective(self):
        formal = (
            ROOT
            / "theory/evaluation/comparative-representation/experiments/CRE-001/semantics/formal-semantics.md"
        ).read_text(encoding="utf-8")
        generated = (ROOT / "docs/reports/project-status-generated.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("formalized after completion of deterministic CRE-001", formal)
        self.assertIn("frozen for future experiments beginning with CRE-002", formal)
        self.assertIn("not independent evidence supporting CRE-001", formal)
        self.assertIn("cannot be used as retrospective validation of CRE-001", formal)
        self.assertIn(
            "CRE-001: deterministic comparison complete at its registered retrospective scope under compiler-authored declared interpretations",
            generated,
        )
        self.assertNotIn("Established at CRE-001 vocabulary-semantics scope", generated)
        self.assertNotRegex(
            generated, "CRE-001.*formal vocabulary licensing.*established"
        )

    def test_frozen_semantic_specification_is_consistent(self):
        cp = subprocess.run(
            [sys.executable, "tools/check_cre001_semantics.py"],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        self.assertEqual(cp.returncode, 0, cp.stdout + cp.stderr)
        self.assertIn("CRE-001 SEMANTIC CHECK PASSED", cp.stdout)

    def test_generated_task_ids_and_provenance_are_unambiguous(self):
        path = ROOT / "docs/planning/next-actions.md"
        before = path.read_text(encoding="utf-8")
        cp = subprocess.run(
            [sys.executable, "tools/generate_next_tasks.py"],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        self.assertEqual(cp.returncode, 0, cp.stdout + cp.stderr)
        text = path.read_text(encoding="utf-8")
        self.assertEqual(text, before)
        ranked = text.split("## Maintainer Boundaries", 1)[0]
        ids = re.findall(r"^### ([A-Z]+-\d{3}):", ranked, re.M)
        self.assertEqual(len(ids), len(set(ids)))
        self.assertEqual(ids, [f"STRATEGIC-{number:03d}" for number in range(10, 15)])
        self.assertEqual(len(ids), 5)
        self.assertEqual(
            ranked.count(
                "- Source: [docs/governance/post-closure-assurance-and-application-program-v1.0.md]"
            ),
            5,
        )
        self.assertEqual(ranked.count("- Expected outcome:"), 5)
        self.assertIn("Program: `POST-CLOSURE-001`.", ranked)
        self.assertIn(
            "Current governing theory: `PROJECT-FAR-CORE-THEORY-1.1`.", ranked
        )
        self.assertIn(
            "Canonical next workstream: `PCA-W2-PROOF-ASSISTANT-FORMALIZATION`.", ranked
        )
        self.assertIn(
            "### STRATEGIC-010: Close the bounded MLL formalization bridge", ranked
        )
        self.assertIn("### STRATEGIC-011: Implement the contract schema", ranked)
        self.assertIn(
            "### STRATEGIC-012: Develop domain comparison contracts", ranked
        )
        self.assertIn(
            "### STRATEGIC-013: Specify approximation and cost orders", ranked
        )
        self.assertIn("### STRATEGIC-014: Test audit utility", ranked)
        self.assertIn(
            "- Registered workstream: `PCA-W2-PROOF-ASSISTANT-FORMALIZATION`", ranked
        )
        self.assertIn("- Priority: active", ranked)
        self.assertIn("The core theory is closed after the governed v1.1 correction.", ranked)
        self.assertIn(
            "The hostile correction audit remains non-independent.",
            ranked,
        )
        self.assertIn(
            "14 PROVED, no correction, novelty/priority not established",
            ranked,
        )
        self.assertIn("do not reopen the core without a genuine contradiction", ranked)
        for stale in (
            "POST-TERM-EVAL-001",
            "PTE-W1-INDEPENDENT-REVIEW",
            "POST-TUE-UPP-001",
            "There is no `UPP-W16`.",
            "W5 remains blocked",
            "Candidate testing is not complete",
            "648 atomic trials require execution",
            "structural indispensability remains unresolved",
            "Global Primitive Minimality",
            "Global Primitive Independence",
            "### STRATEGIC-010: Review the closed core independently",
            "### STRATEGIC-011: Formalize the factorization core",
        ):
            self.assertNotIn(stale, ranked)


if __name__ == "__main__":
    unittest.main()
