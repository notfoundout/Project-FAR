"""Current far-ir/2.0 verification rejects determinate outcomes the verifier did not recompute.

The frozen baseline skips claim-specific checks unless evidence is ``CHECKED_FINITE_EXPLICIT``.
These tests pin that the baseline gap is real, that the strict verifier closes it, that the
strict verifier accepts every checked record the baseline accepts, and that a file is read and
parsed exactly once so baseline and strict rules can never apply to different byte snapshots.
"""
from __future__ import annotations

import ast
import builtins
import copy
import importlib.util
import io
import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from mechanization.far_mechanization import contract_v2_strict
from mechanization.far_mechanization.contract_v2 import contract_sha256
from mechanization.far_mechanization.contract_v2 import validate_contract as validate_baseline
from mechanization.far_mechanization.contract_v2_strict import load_and_validate, validate_contract
from mechanization.far_mechanization.diagnostic_vocabulary import (
    FAR_IR_2_0_DIAGNOSTIC_CODES,
    FAR_IR_2_0_STRICT_DIAGNOSTIC_CODES,
)

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


class _SnapshotSwitchingReader:
    """Count every open of ``target`` and serve ``first`` once, ``later`` afterwards."""

    def __init__(self, target: Path, first: bytes, later: bytes) -> None:
        self.target = target.resolve()
        self.first = first
        self.later = later
        self.reads = 0
        self._real_open = io.open

    def __call__(self, file, mode="r", *args, **kwargs):
        try:
            matches = Path(file).resolve() == self.target
        except TypeError:
            matches = False
        if not matches:
            return self._real_open(file, mode, *args, **kwargs)
        self.reads += 1
        data = self.first if self.reads == 1 else self.later
        if "b" in mode:
            return io.BytesIO(data)
        return io.StringIO(data.decode("utf-8"))


class StrictContractV2Tests(unittest.TestCase):
    def test_baseline_accepts_contradicted_unchecked_proved_record(self) -> None:
        """Documents the baseline gap; if this starts failing, the frozen baseline changed."""
        self.assertTrue(validate_baseline(colliding_unchecked_proved()).success)

    def test_strict_rejects_contradicted_unchecked_proved_record(self) -> None:
        result = validate_contract(colliding_unchecked_proved())
        self.assertFalse(result.success)
        self.assertEqual(codes(result), ["DETERMINATE_OUTCOME_UNCHECKED"])

    def test_strict_rejects_unchecked_refuted_record(self) -> None:
        document = load(FIXTURES / "valid-collision.json")
        document["report"]["evidence"]["status"] = "DECLARED_UNCHECKED"
        self.assertTrue(validate_baseline(document).success)
        self.assertEqual(codes(validate_contract(document)), ["DETERMINATE_OUTCOME_UNCHECKED"])

    def test_strict_keeps_checked_failure_diagnostics(self) -> None:
        document = colliding_unchecked_proved()
        document["report"]["evidence"]["status"] = "CHECKED_FINITE_EXPLICIT"
        self.assertEqual(codes(validate_contract(document)), ["FACTORIZATION_FAILURE"])

    def test_strict_allows_unchecked_nondeterminate_outcome(self) -> None:
        document = colliding_unchecked_proved()
        document["report"]["outcome"] = "OPEN"
        self.assertTrue(validate_baseline(document).success)
        self.assertTrue(validate_contract(document).success)

    def test_strict_accepts_every_baseline_accepted_checked_record(self) -> None:
        paths = sorted(FIXTURES.glob("valid-*.json")) + sorted(W4_RESULTS.glob("*-repaired.json")) + sorted(
            W4_RESULTS.glob("*-lossy.json")
        )
        self.assertGreaterEqual(len(paths), 15)
        for path in paths:
            with self.subTest(record=path.name):
                document = load(path)
                self.assertTrue(validate_baseline(document).success)
                self.assertTrue(validate_contract(document).success)

    def test_strict_does_not_mutate_input(self) -> None:
        document = colliding_unchecked_proved()
        before = copy.deepcopy(document)
        validate_contract(document)
        self.assertEqual(document, before)

    def test_named_aliases_are_the_strict_functions(self) -> None:
        self.assertIs(contract_v2_strict.validate_contract_strict, validate_contract)
        self.assertIs(contract_v2_strict.load_and_validate_strict, load_and_validate)

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
        self.assertTrue(set(FAR_IR_2_0_STRICT_DIAGNOSTIC_CODES) <= emitted)
        self.assertTrue(emitted <= set(FAR_IR_2_0_DIAGNOSTIC_CODES) | set(FAR_IR_2_0_STRICT_DIAGNOSTIC_CODES))
        self.assertFalse(set(FAR_IR_2_0_STRICT_DIAGNOSTIC_CODES) & set(FAR_IR_2_0_DIAGNOSTIC_CODES))


class SingleSnapshotLoadTests(unittest.TestCase):
    """Regression for the double-read defect: both rule sets must see one byte snapshot."""

    # Every public strict loader name; a regression in any one of them must fail.
    LOADERS = ("load_and_validate", "load_and_validate_strict")

    def _run_with_switching_file(self, loader_name: str, first: dict, later: dict):
        loader = getattr(contract_v2_strict, loader_name)
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "record.json"
            path.write_text(json.dumps(first), encoding="utf-8")
            reader = _SnapshotSwitchingReader(
                path, json.dumps(first).encode("utf-8"), json.dumps(later).encode("utf-8")
            )
            with mock.patch.object(io, "open", reader), mock.patch.object(builtins, "open", reader):
                result = loader(path)
            return result, reader.reads

    def test_file_is_opened_exactly_once(self) -> None:
        clean = load(FIXTURES / "valid-factorization.json")
        for name in self.LOADERS:
            with self.subTest(loader=name):
                _result, reads = self._run_with_switching_file(name, clean, clean)
                self.assertEqual(reads, 1)

    def test_clean_first_snapshot_is_not_mixed_with_tampered_later_snapshot(self) -> None:
        for name in self.LOADERS:
            with self.subTest(loader=name):
                result, reads = self._run_with_switching_file(
                    name, load(FIXTURES / "valid-factorization.json"), colliding_unchecked_proved()
                )
                self.assertEqual(reads, 1)
                self.assertTrue(result.success, codes(result))

    def test_tampered_first_snapshot_is_not_mixed_with_clean_later_snapshot(self) -> None:
        for name in self.LOADERS:
            with self.subTest(loader=name):
                result, reads = self._run_with_switching_file(
                    name, colliding_unchecked_proved(), load(FIXTURES / "valid-factorization.json")
                )
                self.assertEqual(reads, 1)
                self.assertEqual(codes(result), ["DETERMINATE_OUTCOME_UNCHECKED"])

    def test_load_validates_the_single_parsed_document_once(self) -> None:
        seen: list[int] = []
        real = contract_v2_strict.validate_contract

        def recording(document):
            seen.append(id(document))
            return real(document)

        with mock.patch.object(contract_v2_strict, "validate_contract", recording):
            contract_v2_strict.load_and_validate(FIXTURES / "valid-factorization.json")
        self.assertEqual(len(seen), 1)

    def test_unreadable_inputs_fail_closed_without_raising(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            missing = Path(tmp) / "missing.json"
            invalid_json = Path(tmp) / "invalid.json"
            invalid_json.write_text("{", encoding="utf-8")
            invalid_utf8 = Path(tmp) / "invalid-utf8.json"
            invalid_utf8.write_bytes(b"\xff\xfe{")
            for name in self.LOADERS:
                for path in (missing, invalid_json, invalid_utf8):
                    with self.subTest(loader=name, path=path.name):
                        result = getattr(contract_v2_strict, name)(path)
                        self.assertEqual(codes(result), ["UNREADABLE_CONTRACT"])


class StandaloneLoadTests(unittest.TestCase):
    def test_module_loads_without_its_package(self) -> None:
        """The commercial bridge loads verifier files standalone; strict mode must survive that."""
        spec = importlib.util.spec_from_file_location("_standalone_strict_probe", contract_v2_strict.__file__)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        self.assertEqual(codes(module.validate_contract(colliding_unchecked_proved())), ["DETERMINATE_OUTCOME_UNCHECKED"])
        self.assertTrue(module.validate_contract(load(FIXTURES / "valid-factorization.json")).success)


class CurrentConformanceTests(unittest.TestCase):
    def test_current_verification_conformance_suite(self) -> None:
        from mechanization.far_mechanization.contract_conformance import run_manifest

        results = run_manifest(ROOT / "conformance" / "far-ir-2.0-current" / "manifest.json")
        self.assertEqual(len(results), 7)
        self.assertEqual([r for r in results if not r.passed], [])

    def test_strict_vocabulary_is_published(self) -> None:
        spec = (ROOT / "docs" / "specification" / "far-ir-2.0-current-verification.md").read_text(encoding="utf-8")
        published = set(re.findall(r"^\| `([A-Z0-9_]+)` \|", spec, re.MULTILINE))
        self.assertEqual(published, set(FAR_IR_2_0_STRICT_DIAGNOSTIC_CODES))


class CliTests(unittest.TestCase):
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
