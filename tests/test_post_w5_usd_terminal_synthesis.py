from __future__ import annotations

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SYN = ROOT / "theory/evaluation/post-w5-usd-terminal-synthesis-v1.0.json"
NEXT = ROOT / "theory/evaluation/post-w5-usd-next-program-v1.0.json"
CHECKER = ROOT / "tools/check_post_w5_usd_terminal_synthesis.py"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


class PostW5UsdTerminalSynthesisTests(unittest.TestCase):
    def test_checker_passes(self) -> None:
        completed = subprocess.run(
            [sys.executable, str(CHECKER)], cwd=ROOT, text=True,
            capture_output=True, check=False,
        )
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        self.assertIn("PASS", completed.stdout)

    def test_all_workstreams_are_aggregated(self) -> None:
        inputs = load(SYN)["inputs"]
        self.assertEqual(len(inputs), 6)
        self.assertIn("USD-W1-SCOPE-EXT", inputs)
        self.assertIn("USD-W6-INDEPENDENCE", inputs)

    def test_universal_claim_is_blocked(self) -> None:
        syn = load(SYN)
        claims = syn["claim_effect"]
        self.assertEqual(claims["one_universal_kernel"], "not_established")
        self.assertEqual(claims["FARA_is_universal"], "not_established")
        self.assertEqual(claims["LTS_PROV_is_universal"], "not_established")
        self.assertEqual(claims["independent_verification"], "not_established")

    def test_bounded_frontier_is_preserved(self) -> None:
        syn = load(SYN)
        self.assertEqual(
            syn["terminal_program_classification"],
            "bounded_incomparable_kernels_external_validation_pending",
        )
        self.assertEqual(syn["valid_program_outcome_mapping"], "incomparable_kernels")
        self.assertEqual(
            syn["hypothesis_disposition"]["USD-H-MIN"],
            "resolved_as_multiple_incomparable_minima_in_frozen_universe",
        )

    def test_next_program_requires_real_external_evidence(self) -> None:
        nxt = load(NEXT)
        self.assertEqual(nxt["status"], "registered_unexecuted")
        workstreams = {item["id"]: item for item in nxt["workstreams"]}
        self.assertIn("separate human or organization", workstreams["EVC-W2-R3-TECHNICAL-REPLICATION"]["required_independence"])
        self.assertIn("materially new", workstreams["EVC-W4-CANDIDATE-EXPANSION"]["minimum_requirement"])
        self.assertIn("measurement error model", workstreams["EVC-W6-EMPIRICAL-BRIDGE"]["minimum_requirement"])


if __name__ == "__main__":
    unittest.main()
