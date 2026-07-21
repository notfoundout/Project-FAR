from __future__ import annotations

import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from check_w3_5_factorization import EXPECTED_DIMENSIONS, ValidationError, validate, validate_static  # noqa: E402
from w3_5_factorization import (  # noqa: E402
    FactorizationError,
    authoritative_projection,
    compile_projection,
    compile_record,
    decode_grel,
    encode_grel,
    load_records,
    run_factorization,
    validate_grel,
)

class W35FactorizationTests(unittest.TestCase):
    def test_complete_factorization_passes(self) -> None:
        report = validate(ROOT)
        self.assertEqual(report["status"], "pass")
        self.assertEqual(report["instance_count"], 18)
        self.assertEqual(report["dimensions"], EXPECTED_DIMENSIONS)

    def test_all_three_corpus_classes_factor(self) -> None:
        report = run_factorization(ROOT)
        self.assertEqual(report["scope"]["class_counts"], {"positive": 8, "contrast": 8, "disputed": 2})
        self.assertTrue(all(item["status"] == "pass" for item in report["records"]))

    def test_factorization_is_candidate_neutral(self) -> None:
        record = load_records(ROOT)[0]
        baseline = compile_record(record)
        mutated = copy.deepcopy(record)
        mutated.update({"title": "changed", "family": "changed", "admission_decision": "disputed", "admission_rationale": "changed", "candidate_exposure_status": "changed"})
        self.assertEqual(compile_record(mutated), baseline)

    def test_grel_round_trip_is_exact(self) -> None:
        value = {"b": [1, True, None], "a": {"x": "y"}}
        self.assertEqual(decode_grel(encode_grel(value)), value)

    def test_grel_mediates_candidate_neutral_projection_before_fara_adapter(self) -> None:
        record = load_records(ROOT)[0]
        projection = authoritative_projection(record)
        recovered = decode_grel(encode_grel(projection))
        self.assertEqual(recovered, projection)
        self.assertEqual(compile_projection(recovered), compile_record(record))

    def test_grel_digest_corruption_is_rejected(self) -> None:
        package = encode_grel({"a": 1})
        package["typed_attributes"][0]["value"] = "value:missing"
        with self.assertRaises(FactorizationError):
            validate_grel(package)

    def test_hidden_case_database_is_rejected(self) -> None:
        package = encode_grel({"a": 1})
        package["canonical_encoder"]["case_database"] = True
        with self.assertRaises(FactorizationError):
            validate_grel(package)

    def test_hidden_interpreter_is_rejected(self) -> None:
        package = encode_grel({"a": 1})
        package["machinery_ledger"]["forbidden"]["hidden_interpreter"] = True
        with self.assertRaises(FactorizationError):
            validate_grel(package)

    def test_relation_loss_is_rejected_or_changes_recovery(self) -> None:
        package = encode_grel({"a": 1, "b": 2})
        package["typed_nary_relation_occurrences"].pop()
        self.assertNotEqual(decode_grel(package), {"a": 1, "b": 2})

    def test_dimension_record_is_not_collapsed(self) -> None:
        static = validate_static(ROOT)
        self.assertEqual(static["result"]["dimensions"], EXPECTED_DIMENSIONS)
        self.assertEqual(len(static["result"]["dimensions"]), 6)
        self.assertEqual(static["result"]["dimensions"]["reasoning_specificity"], "not_established")

    def test_operational_factorization_is_not_primitive_reduction(self) -> None:
        contract = validate_static(ROOT)["result"]["factorization_contract"]
        self.assertFalse(contract["primitive_reduction_established"])
        self.assertIn("fixed FARA-oriented compile_projection source adapter", contract["reintroduced_machinery"])
        self.assertIn("accepted SCORE-W3 construct_witness implementation", contract["reintroduced_machinery"])

    def test_factorization_does_not_promote_specificity_or_w5(self) -> None:
        static = validate_static(ROOT)
        gate_map = {item["name"]: item for item in static["gates"]["gates"]}
        self.assertEqual(gate_map["baseline-factorization-resolved"]["status"], "satisfied")
        self.assertEqual(gate_map["fara-specificity-resolved"]["status"], "not_satisfied")
        self.assertEqual(gate_map["reasoning-contrast-execution"]["status"], "not_satisfied")
        self.assertFalse(static["w35"]["w5_authorized"])
        self.assertFalse(static["target"]["w5_authorization"]["authorized"])

    def test_status_only_factorization_promotion_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            for relative in (
                "theory/evaluation/w3-5-factorization-result-v1.0.json",
                "theory/evaluation/w3-5-factorization-witnesses-v1.0.json",
                "theory/evaluation/generic-relational-baseline-v1.0.json",
                "theory/evaluation/w3-5-specificity-and-discovery-gate.json",
                "theory/evaluation/research-gates.json",
                "theory/evaluation/thm-target-001.json",
            ):
                source, target = ROOT / relative, root / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(source.read_bytes())
            w35_path = root / "theory/evaluation/w3-5-specificity-and-discovery-gate.json"
            w35 = json.loads(w35_path.read_text(encoding="utf-8"))
            next(item for item in w35["required_result_artifacts"] if item["id"] == "W35-FACTOR-RESULT")["content_sha256"] = "0" * 64
            w35_path.write_text(json.dumps(w35), encoding="utf-8")
            with self.assertRaises(ValidationError):
                validate_static(root)

    def test_makefile_runs_factorization_checker_three_times(self) -> None:
        text = (ROOT / "Makefile").read_text(encoding="utf-8")
        self.assertEqual(text.count("python tools/check_w3_5_factorization.py"), 3)

if __name__ == "__main__":
    unittest.main()
