"""Strict far-ir/2.0 mode rejects determinate outcomes the verifier did not recompute.

The baseline verifier skips claim-specific checks unless evidence is
``CHECKED_FINITE_EXPLICIT``. These tests pin that the baseline gap is real, that strict mode
closes it, and that strict mode accepts every checked record the baseline accepts.
"""
from __future__ import annotations

import ast
import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from mechanization.far_mechanization import contract_v2_strict
from mechanization.far_mechanization.contract_v2 import contract_sha256, validate_contract
from mechanization.far_mechanization.contract_v2_strict import validate_contract_strict
from mechanization.far_mechanization.diagnostic_vocabulary import FAR_IR_2_0_STRICT_DIAGNOSTIC_CODES

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "conformance" / "far-ir-2.0"
W4_RESULTS = ROOT / "research" / "results" / "pca-w4-domain-contracts"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def colliding_unchecked_proved() -> dict:
    """A PROVED factorization whose own explicit tables contain a material collision."""
    document = load(FIXTURES / "valid-factorization.json")
    contract = document["contract"]
    contract["representation"]["table"][1]["value"] = contract["representation"]["table"][0]["value"]
    document["freeze"]["contract_sha256"] = contract_sha256(contract)
    document["report"]["evidence"]["status"] = "DECLARED_UNCHECKED"
    return document


def codes(result) -> list[str]:
    return [diagnostic.code for diagnostic in result.diagnostics]


class StrictContractV2Tests(unittest.TestCase):
    def test_baseline_accepts_contradicted_unchecked_proved_record(self) -> None:
        """Documents the baseline gap; if this starts failing, the frozen baseline changed."""
        self.assertTrue(validate_contract(colliding_unchecked_proved()).success)

    def test_strict_rejects_contradicted_unchecked_proved_record(self) -> None:
        result = validate_contract_strict(colliding_unchecked_proved())
        self.assertFalse(result.success)
        self.assertEqual(codes(result), ["DETERMINATE_OUTCOME_UNCHECKED"])

    def test_strict_rejects_unchecked_refuted_record(self) -> None:
        document = load(FIXTURES / "valid-collision.json")
        document["report"]["evidence"]["status"] = "DECLARED_UNCHECKED"
        self.assertTrue(validate_contract(document).success)
        self.assertEqual(codes(validate_contract_strict(document)), ["DETERMINATE_OUTCOME_UNCHECKED"])

    def test_strict_keeps_checked_failure_diagnostics(self) -> None:
        document = colliding_unchecked_proved()
        document["report"]["evidence"]["status"] = "CHECKED_FINITE_EXPLICIT"
        self.assertEqual(codes(validate_contract_strict(document)), ["FACTORIZATION_FAILURE"])

    def test_strict_allows_unchecked_nondeterminate_outcome(self) -> None:
        document = colliding_unchecked_proved()
        document["report"]["outcome"] = "OPEN"
        self.assertTrue(validate_contract(document).success)
        self.assertTrue(validate_contract_strict(document).success)

    def test_strict_accepts_every_baseline_accepted_checked_record(self) -> None:
        paths = sorted(FIXTURES.glob("valid-*.json")) + sorted(W4_RESULTS.glob("*-repaired.json")) + sorted(
            W4_RESULTS.glob("*-lossy.json")
        )
        self.assertGreaterEqual(len(paths), 15)
        for path in paths:
            with self.subTest(record=path.name):
                document = load(path)
                self.assertTrue(validate_contract(document).success)
                self.assertTrue(validate_contract_strict(document).success)

    def test_strict_does_not_mutate_input(self) -> None:
        document = colliding_unchecked_proved()
        before = copy.deepcopy(document)
        validate_contract_strict(document)
        self.assertEqual(document, before)

    def test_declared_vocabulary_matches_emission_sites(self) -> None:
        tree = ast.parse(Path(contract_v2_strict.__file__).read_text(encoding="utf-8"))
        emitted = {
            node.args[0].value
            for node in ast.walk(tree)
            if isinstance(node, ast.Call)
            and getattr(node.func, "id", None) == "ContractDiagnostic"
            and node.args
            and isinstance(node.args[0], ast.Constant)
        }
        self.assertEqual(emitted, set(FAR_IR_2_0_STRICT_DIAGNOSTIC_CODES))

    def test_cli_exit_codes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            bad = Path(tmp) / "bad.json"
            bad.write_text(json.dumps(colliding_unchecked_proved()), encoding="utf-8")
            command = [sys.executable, "-m", "mechanization.far_mechanization.contract_v2_strict"]
            failed = subprocess.run([*command, str(bad), "--json"], cwd=ROOT, capture_output=True, text=True)
            self.assertEqual(failed.returncode, 1, failed.stderr)
            self.assertEqual(
                [item["code"] for item in json.loads(failed.stdout)["diagnostics"]],
                ["DETERMINATE_OUTCOME_UNCHECKED"],
            )
            passed = subprocess.run(
                [*command, str(FIXTURES / "valid-factorization.json")], cwd=ROOT, capture_output=True, text=True
            )
            self.assertEqual(passed.returncode, 0, passed.stdout + passed.stderr)
            missing = subprocess.run([*command, str(Path(tmp) / "missing.json")], cwd=ROOT, capture_output=True, text=True)
            self.assertEqual(missing.returncode, 1)
            self.assertIn("UNREADABLE_CONTRACT", missing.stdout)


if __name__ == "__main__":
    unittest.main()
