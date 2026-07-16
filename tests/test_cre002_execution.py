from __future__ import annotations
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "theory/evaluation/comparative-representation/experiments/CRE-002"
GENERATED = BASE / "execution/generated"
VOCABS = ["CRE-001-VOCAB-A-1.0", "CRE-001-VOCAB-B-1.0", "CRE-001-VOCAB-C-1.0"]


class Cre002ExecutionTests(unittest.TestCase):
    def test_execution_regenerates_deterministically(self) -> None:
        result = subprocess.run([sys.executable, "tools/cre002_execute.py", "--write", "--check"], cwd=ROOT, text=True, capture_output=True, check=False)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_all_vocabularies_pass_every_frozen_gate(self) -> None:
        summary = json.loads((BASE / "execution/cre002-comparison.json").read_text())
        self.assertEqual(len(summary["vocabulary_results"]), 3)
        for row in summary["vocabulary_results"]:
            self.assertEqual(row["outcome"], "complete")
            self.assertTrue(all(row["gates"].values()))
            self.assertIsNone(row["shortest_counterexample"])
            self.assertGreater(row["state_count"], 1)
            self.assertGreater(row["edge_count"], 1)

    def test_native_representations_are_structurally_distinct(self) -> None:
        primitive_sets = []
        record_kinds = []
        for vocab in VOCABS:
            native = json.loads((GENERATED / vocab / "native-representation.json").read_text())
            primitive_sets.append(tuple(native["primitive_categories"]))
            record_kinds.append(tuple(sorted({record["primitive"] for record in native["records"]})))
        self.assertEqual(len(set(primitive_sets)), 3)
        self.assertEqual(len(set(record_kinds)), 3)

    def test_trace_replay_and_mutations_pass(self) -> None:
        for vocab in VOCABS:
            trace = json.loads((GENERATED / vocab / "trace-replay-report.json").read_text())
            mutation = json.loads((GENERATED / vocab / "mutation-test-report.json").read_text())
            self.assertTrue(trace["passed"])
            self.assertGreaterEqual(trace["trace_entries"], 5)
            self.assertTrue(mutation["passed"])
            self.assertEqual(len(mutation["cases"]), 8)
            self.assertTrue(all(case["detected"] for case in mutation["cases"]))

    def test_results_preserve_nonclaims_and_prohibit_ranking(self) -> None:
        summary = json.loads((BASE / "execution/cre002-comparison.json").read_text())
        required = {"universal sufficiency", "primitive-only sufficiency", "necessity", "minimality", "independence", "superiority", "FAR proof", "universal structure of reasoning"}
        self.assertTrue(required.issubset(summary["unsupported_conclusions"]))
        self.assertFalse(summary["vocabulary_level"]["ranking_permitted"])

    def test_execution_was_prospectively_authorized(self) -> None:
        control = json.loads((BASE / "execution-lock.json").read_text())
        self.assertTrue(control["execution_permitted"])


if __name__ == "__main__":
    unittest.main()
