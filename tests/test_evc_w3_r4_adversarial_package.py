import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class EvcW3R4AdversarialPackageTests(unittest.TestCase):
    def load(self, relative):
        return json.loads((ROOT / relative).read_text())

    def test_canonical_checker(self):
        result = subprocess.run(
            [sys.executable, str(ROOT / "tools/check_evc_w3_r4_adversarial_package.py")],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("PASS", result.stdout)

    def test_parent_program_registers_r4(self):
        parent = self.load("theory/evaluation/post-w5-usd-next-program-v1.0.json")
        ids = {item["id"] for item in parent["workstreams"]}
        self.assertIn("EVC-W3-R4-ADVERSARIAL-REPLICATION", ids)

    def test_all_challenges_are_explicit_and_unique(self):
        corpus = self.load("theory/evaluation/evc-w3-r4-adversarial-challenge-corpus-v1.0.json")
        ids = [item["id"] for item in corpus["challenges"]]
        self.assertEqual(len(ids), 12)
        self.assertEqual(len(set(ids)), 12)

    def test_manifest_includes_parent_and_corpus(self):
        manifest = self.load("theory/evaluation/evc-w3-r4-adversarial-package-manifest-v1.0.json")
        groups = {g["group"]: g for g in manifest["required_artifact_groups"]}
        self.assertIn(
            "theory/evaluation/post-w5-usd-next-program-v1.0.json",
            groups["program_and_terminal_synthesis"]["artifacts"],
        )
        self.assertIn(
            "theory/evaluation/evc-w3-r4-adversarial-challenge-corpus-v1.0.json",
            groups["adversarial_instruments"]["artifacts"],
        )

    def test_unexecuted_claim_boundary(self):
        protocol = self.load("theory/evaluation/evc-w3-r4-adversarial-replication-protocol-v1.0.json")
        manifest = self.load("theory/evaluation/evc-w3-r4-adversarial-package-manifest-v1.0.json")
        self.assertEqual(protocol["status"], "frozen_unexecuted")
        self.assertEqual(manifest["status"], "frozen_unreleased")
        self.assertFalse(manifest["release_state"]["adversarial_team_recruited"])
        self.assertFalse(manifest["release_state"]["replication_started"])
        self.assertFalse(manifest["release_state"]["replication_completed"])

    def test_result_template_matches_protocol(self):
        protocol = self.load("theory/evaluation/evc-w3-r4-adversarial-replication-protocol-v1.0.json")
        template = self.load("theory/evaluation/evc-w3-r4-adversarial-result-template-v1.0.json")
        self.assertEqual(set(template["allowed_verdicts"]), set(protocol["terminal_outcomes"]))
        self.assertIsNone(template["initial_verdict"])
        self.assertIsNone(template["final_verdict"])


if __name__ == "__main__":
    unittest.main()
