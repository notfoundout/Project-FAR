from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PKG = ROOT / "theory/evaluation/comparative-representation/experiments/CRE-002-EXT-001"
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

from cre002_ext001_execute import build
from cre002_ext001_native import DERIVED, VOCABS


class CRE002EXT001ExecutionTests(unittest.TestCase):
    def test_frozen_inputs_still_pass_checksum_verification(self) -> None:
        cp = subprocess.run(
            [sys.executable, "tools/check_cre002_ext001_checksums.py"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(cp.returncode, 0, cp.stdout + cp.stderr)

    def test_all_three_candidates_complete_all_gates(self) -> None:
        comparison, reference, bundles = build()
        self.assertGreater(reference["state_count"], 1)
        self.assertGreater(reference["edge_count"], 1)
        self.assertEqual(set(bundles), set(VOCABS))
        self.assertEqual(comparison["candidate_outcome_counts"]["complete"], 3)
        self.assertEqual(comparison["candidate_outcome_counts"]["partial"], 0)
        for row in comparison["candidates"]:
            self.assertEqual(row["outcome"], "complete")
            self.assertEqual(row["semantic_licensing_by_role"]["status"], "pass")
            self.assertEqual(set(row["derived_constructs_used"]), DERIVED)
            self.assertEqual(row["trace_replay_status"], "pass")
            self.assertEqual(row["behavioral_verification_status"], "pass")
            self.assertEqual(row["deterministic_regeneration_status"], "pass")
            self.assertEqual(row["mutation_status"], "pass")
            self.assertIsNone(row["shortest_counterexample"])

    def test_native_representations_are_structurally_distinct(self) -> None:
        _, _, bundles = build()
        primitive_sets = {
            vocab: {record["primitive"] for record in bundle["native"]["records"]}
            for vocab, bundle in bundles.items()
        }
        self.assertEqual(len({tuple(sorted(value)) for value in primitive_sets.values()}), 3)

    def test_mutations_cover_every_baseline_derived_construct(self) -> None:
        comparison, _, _ = build()
        for row in comparison["candidates"]:
            cases = row["mutation_report"]["cases"]
            self.assertEqual({case["mutation"] for case in cases}, DERIVED)
            self.assertTrue(all(case["detected"] for case in cases))

    def test_forbidden_comparison_fields_are_absent(self) -> None:
        comparison, _, _ = build()
        schema = json.loads((PKG / "output-schema.json").read_text(encoding="utf-8"))
        serialized = json.dumps(comparison)
        for field in schema["forbidden_fields"]:
            self.assertNotIn(f'"{field}"', serialized)

    def test_committed_outputs_are_deterministic(self) -> None:
        cp = subprocess.run(
            [sys.executable, "tools/cre002_ext001_execute.py", "--check"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(cp.returncode, 0, cp.stdout + cp.stderr)


if __name__ == "__main__":
    unittest.main()
