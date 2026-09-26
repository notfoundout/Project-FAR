"""far-ir/2.0 errata 1 and current verification rule v1.1.

Defects found by the 2026-09 root-of-trust audit, corrected as successor material: the frozen
baseline ``contract_v2`` and rule v1.0 ``contract_v2_strict`` stay byte-identical. Expected
sequences are derived by hand from specification sections 3.3, 5 and 9, errata 1, and RFC 8259,
not recorded from the verifier. Under the baseline, a repeated class id merged two declared classes,
so ``P1`` below was certified as the exact observational quotient.
"""
from __future__ import annotations

import copy
import importlib.util
import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from mechanization.far_mechanization import contract_v2_errata1, contract_v2_strict_v11
from mechanization.far_mechanization.contract_v2 import validate_contract as validate_baseline
from mechanization.far_mechanization.contract_v2_strict import validate_contract as validate_rule_v1_0
from mechanization.far_mechanization.diagnostic_vocabulary import (
    FAR_IR_2_0_DIAGNOSTIC_CODES,
    FAR_IR_2_0_ERRATA_1_DIAGNOSTIC_CODES,
    FAR_IR_2_0_STRICT_DIAGNOSTIC_CODES,
)

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "conformance" / "far-ir-2.0"
ERRATA = ROOT / "docs" / "specification" / "far-ir-2.0-errata-1.md"
# Audit records built to trigger exactly the corrected defects; every other tracked record must be unaffected.
AUDIT_DEFECT_RECORDS = {
    f"research/root-of-trust-audit-2026-09/oracle_far_ir_2_0/adversarial/ADV-{n}.json" for n in (27, 51, 56, 70)
}


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def codes(result) -> list[str]:
    return [diagnostic.code for diagnostic in result.diagnostics]


class Errata1RegressionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.quotient = load(FIXTURES / "valid-quotient.json")  # beta: a,b -> x ; c,d -> y

    def with_classes(self, classes: list[dict]) -> dict:
        document = copy.deepcopy(self.quotient)
        document["report"]["evidence"]["classes"] = classes
        return document

    def test_repeated_class_id_cannot_certify_a_split_partition(self) -> None:
        document = self.with_classes([
            {"id": "k", "case_ids": ["case.a"]},
            {"id": "k", "case_ids": ["case.b"]},
            {"id": "class.y", "case_ids": ["case.c", "case.d"]},
        ])
        self.assertEqual(codes(validate_baseline(document)), [], "baseline defect no longer reproduces")
        # Declared classes {a},{b},{c,d}: only the ordered pairs (a,b) and (b,a) break the kernel.
        self.assertEqual(
            codes(contract_v2_errata1.validate_contract(document)),
            ["DUPLICATE_QUOTIENT_CLASS", "QUOTIENT_NOT_EXACT_BEHAVIOR_KERNEL", "QUOTIENT_NOT_EXACT_BEHAVIOR_KERNEL"],
        )

    def test_repeated_class_id_is_rejected_even_on_the_exact_partition(self) -> None:
        document = self.with_classes([
            {"id": "k", "case_ids": ["case.a", "case.b"]},
            {"id": "k", "case_ids": ["case.c", "case.d"]},
        ])
        self.assertEqual(codes(contract_v2_errata1.validate_contract(document)), ["DUPLICATE_QUOTIENT_CLASS"])

    def test_overlapping_classes_are_not_a_partition(self) -> None:
        document = self.with_classes([
            {"id": "class.x", "case_ids": ["case.a", "case.b"]},
            {"id": "class.y", "case_ids": ["case.b", "case.c", "case.d"]},
        ])
        self.assertEqual(codes(contract_v2_errata1.validate_contract(document)), ["QUOTIENT_OVERLAP", "QUOTIENT_NOT_PARTITION"])

    def test_frozen_record_requires_rfc3339_freeze_time(self) -> None:
        for frozen_at in ("2026-08-29 20:00:00Z", "2026-02-30T00:00:00Z", "2026-08-29T20:00:00", "yesterday"):
            with self.subTest(frozen_at=frozen_at):
                document = copy.deepcopy(self.quotient)
                document["freeze"]["frozen_at"] = frozen_at
                self.assertEqual(codes(validate_baseline(document)), [])
                self.assertEqual(codes(contract_v2_errata1.validate_contract(document)), ["FREEZE_TIME_INVALID"])

    def test_freeze_time_precedes_freeze_hash_in_stage_two(self) -> None:
        document = copy.deepcopy(self.quotient)
        document["freeze"]["frozen_at"] = "yesterday"
        document["freeze"]["contract_sha256"] = "0" * 64
        document["contract"]["observation_contexts"].append(copy.deepcopy(document["contract"]["observation_contexts"][0]))
        self.assertEqual(
            codes(contract_v2_errata1.validate_contract(document)),
            ["DUPLICATE_OBSERVATION_CONTEXT", "FREEZE_TIME_INVALID", "FREEZE_HASH_MISMATCH"],
        )

    def test_intake_rejects_non_json_constants_and_duplicate_keys(self) -> None:
        text = (FIXTURES / "valid-factorization.json").read_text(encoding="utf-8")
        self.assertEqual(json.loads(text)["report"]["outcome"], "PROVED")
        variants = {
            "nan": text.replace('"report": {', '"report": {"extensions": {"audit.probe": NaN}, ', 1),
            "duplicate-key": text.replace('"outcome": "PROVED"', '"outcome": "REFUTED", "outcome": "PROVED"', 1),
        }
        for name, variant in variants.items():
            self.assertNotEqual(variant, text, name)
            with self.subTest(variant=name), tempfile.TemporaryDirectory() as tmp:
                path = Path(tmp) / "record.json"
                path.write_text(variant, encoding="utf-8")
                for module in (contract_v2_errata1, contract_v2_strict_v11):
                    self.assertEqual(codes(module.load_and_validate(path)), ["UNREADABLE_CONTRACT"], module.__name__)

    def test_in_memory_non_finite_number_is_not_a_json_value(self) -> None:
        document = copy.deepcopy(self.quotient)
        document["contract"]["required_behavior"]["table"][0]["value"] = float("nan")
        self.assertEqual(codes(contract_v2_errata1.validate_contract(document)), ["SCHEMA_CONSTRAINT_VIOLATION"])


class RuleV11Tests(unittest.TestCase):
    def test_rule_v1_1_is_errata_1_plus_the_rule_v1_0_determinate_outcome_check(self) -> None:
        document = load(FIXTURES / "valid-quotient.json")
        document["report"]["evidence"]["status"] = "DECLARED_UNCHECKED"
        document["freeze"]["frozen_at"] = "yesterday"
        self.assertEqual(codes(validate_rule_v1_0(document)), ["DETERMINATE_OUTCOME_UNCHECKED"])
        self.assertEqual(codes(contract_v2_errata1.validate_contract(document)), ["FREEZE_TIME_INVALID"])
        self.assertEqual(
            codes(contract_v2_strict_v11.validate_contract(document)),
            ["FREEZE_TIME_INVALID", "DETERMINATE_OUTCOME_UNCHECKED"],
        )

    def test_corrections_leave_every_other_tracked_record_unchanged(self) -> None:
        tracked = subprocess.run(["git", "ls-files", "*.json"], cwd=ROOT, capture_output=True, text=True, check=True)
        checked = 0
        for rel in tracked.stdout.split():
            try:
                document = json.loads((ROOT / rel).read_text(encoding="utf-8"))
            except (UnicodeDecodeError, ValueError):
                continue
            if not isinstance(document, dict) or document.get("format_version") != "far-ir/2.0":
                continue
            checked += 1
            baseline = codes(validate_baseline(document))
            corrected = codes(contract_v2_errata1.validate_contract(document))
            with self.subTest(record=rel):
                if rel in AUDIT_DEFECT_RECORDS:
                    self.assertNotEqual(baseline, corrected)
                else:
                    self.assertEqual(baseline, corrected)
                    self.assertEqual(codes(validate_rule_v1_0(document)), codes(contract_v2_strict_v11.validate_contract(document)))
        self.assertGreater(checked, len(AUDIT_DEFECT_RECORDS))


class Errata1VocabularyTests(unittest.TestCase):
    def test_errata_codes_are_emitted_published_and_new(self) -> None:
        source = Path(contract_v2_errata1.__file__).read_text(encoding="utf-8")
        emitted = set(re.findall(r'ContractDiagnostic\(\s*"([A-Z0-9_]+)"', source))
        self.assertTrue(set(FAR_IR_2_0_ERRATA_1_DIAGNOSTIC_CODES) <= emitted)
        self.assertTrue(emitted <= set(FAR_IR_2_0_DIAGNOSTIC_CODES) | set(FAR_IR_2_0_ERRATA_1_DIAGNOSTIC_CODES))
        self.assertFalse(set(FAR_IR_2_0_ERRATA_1_DIAGNOSTIC_CODES) & set(FAR_IR_2_0_DIAGNOSTIC_CODES))
        self.assertFalse(set(FAR_IR_2_0_ERRATA_1_DIAGNOSTIC_CODES) & set(FAR_IR_2_0_STRICT_DIAGNOSTIC_CODES))
        published = set(re.findall(r"^\| `([A-Z0-9_]+)` \|", ERRATA.read_text(encoding="utf-8"), re.MULTILINE))
        self.assertTrue(set(FAR_IR_2_0_ERRATA_1_DIAGNOSTIC_CODES) <= published)
        self.assertTrue(published <= set(FAR_IR_2_0_DIAGNOSTIC_CODES) | set(FAR_IR_2_0_ERRATA_1_DIAGNOSTIC_CODES))


class StandaloneLoadTests(unittest.TestCase):
    def test_successors_load_without_their_package(self) -> None:
        """The commercial bridge loads verifier files standalone; the successors must survive that."""
        document = load(FIXTURES / "valid-quotient.json")
        document["report"]["evidence"]["classes"] = [
            {"id": "k", "case_ids": ["case.a", "case.b"]},
            {"id": "k", "case_ids": ["case.c", "case.d"]},
        ]
        document["report"]["evidence"]["status"] = "DECLARED_UNCHECKED"
        expected = {
            contract_v2_errata1: [],
            contract_v2_strict_v11: ["DETERMINATE_OUTCOME_UNCHECKED"],
        }
        for module, expected_codes in expected.items():
            with self.subTest(module=module.__name__):
                spec = importlib.util.spec_from_file_location(f"_standalone_{module.__name__.rsplit('.', 1)[1]}", module.__file__)
                standalone = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(standalone)
                self.assertTrue(standalone.validate_contract(load(FIXTURES / "valid-factorization.json")).success)
                self.assertEqual(codes(standalone.validate_contract(document)), expected_codes)
                checked = copy.deepcopy(document)
                checked["report"]["evidence"]["status"] = "CHECKED_FINITE_EXPLICIT"
                self.assertEqual(codes(standalone.validate_contract(checked)), ["DUPLICATE_QUOTIENT_CLASS"])


class CliTests(unittest.TestCase):
    def test_cli_exit_codes(self) -> None:
        for module in ("contract_v2_errata1", "contract_v2_strict_v11"):
            command = [sys.executable, "-m", f"mechanization.far_mechanization.{module}"]
            with self.subTest(module=module), tempfile.TemporaryDirectory() as tmp:
                document = load(FIXTURES / "valid-quotient.json")
                document["freeze"]["frozen_at"] = "yesterday"
                bad = Path(tmp) / "bad.json"
                bad.write_text(json.dumps(document), encoding="utf-8")
                failed = subprocess.run([*command, str(bad), "--json"], cwd=ROOT, capture_output=True, text=True)
                self.assertEqual(failed.returncode, 1, failed.stderr)
                self.assertEqual([item["code"] for item in json.loads(failed.stdout)["diagnostics"]], ["FREEZE_TIME_INVALID"])
                passed = subprocess.run([*command, str(FIXTURES / "valid-quotient.json")], cwd=ROOT, capture_output=True, text=True)
                self.assertEqual(passed.returncode, 0, passed.stdout + passed.stderr)


if __name__ == "__main__":
    unittest.main()
