from __future__ import annotations

from copy import deepcopy
from decimal import getcontext
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from jsonschema import Draft202012Validator
from mechanization.far_mechanization.epistemic import (
    EpistemicDocument, EpistemicValidationError, calibration, recurring_failure_modes,
    score_binary, sha256_commitment, snapshot_payload, validate_document,
)

ROOT = Path(__file__).parents[1]
FIXTURE = ROOT / "examples/epistemic/complete-learning-loop.json"
SCHEMA = ROOT / "schemas/far-epistemic-v1.schema.json"


class EpistemicLearningTests(unittest.TestCase):
    def setUp(self) -> None:
        self.data = json.loads(FIXTURE.read_text(encoding="utf-8"))

    def assert_invalid(self, mutate, contains: str) -> None:
        value = deepcopy(self.data); mutate(value)
        with self.assertRaises(EpistemicValidationError) as caught:
            EpistemicDocument.from_dict(value)
        self.assertIn(contains, str(caught.exception))

    def record(self, kind: str, occurrence: int = 0):
        return [x for x in self.data["records"] if x["kind"] == kind][occurrence]

    def test_schema_runtime_round_trip_and_replay_are_one_contract(self) -> None:
        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        self.assertEqual([], list(Draft202012Validator(schema).iter_errors(self.data)))
        document = EpistemicDocument.from_dict(self.data)
        restored = EpistemicDocument.loads(document.dumps())
        self.assertEqual(document, restored)
        self.assertEqual(document.digest, restored.audit_event()["content_hash"])
        malformed = deepcopy(self.data); malformed["records"][2].pop("belief_ref")
        self.assertTrue(list(Draft202012Validator(schema).iter_errors(malformed)))
        self.assertTrue(validate_document(malformed))

    def test_all_malformed_leaf_types_fail_closed_without_exceptions(self) -> None:
        # Replacing every leaf in turn exercises schema/native validation totality.
        def paths(value, prefix=()):
            if isinstance(value, dict):
                for key, child in value.items(): yield from paths(child, prefix + (key,))
            elif isinstance(value, list):
                for index, child in enumerate(value): yield from paths(child, prefix + (index,))
            else: yield prefix
        for path in list(paths(self.data)):
            mutated = deepcopy(self.data); cursor = mutated
            for part in path[:-1]: cursor = cursor[part]
            cursor[path[-1]] = {"malformed": object()}
            with self.subTest(path=path):
                errors = validate_document(mutated)
                self.assertTrue(errors)
                self.assertEqual(tuple(sorted(errors)), errors)
        for token in ("NaN", "Infinity", "-Infinity"):
            with self.assertRaises(EpistemicValidationError): EpistemicDocument.loads('{"x": '+token+'}')
        with self.assertRaises(EpistemicValidationError): EpistemicDocument.loads('{"x":1,"x":2}')

    def test_structural_defects_identified_by_review_are_rejected(self) -> None:
        prediction_index = self.data["records"].index(self.record("prediction"))
        cases = [
            (lambda d: d["records"][prediction_index].pop("belief_ref"), "schema"),
            (lambda d: d["records"][prediction_index].update(id="not valid"), "schema"),
            (lambda d: d["records"][0]["hypotheses"][0]["uncertainty"].update(kind="GUESS"), "schema"),
            (lambda d: d["records"][0]["revisions"][1].pop("update_rule"), "schema"),
            (lambda d: d["records"][0]["provenance"].pop("far_refs"), "schema"),
            (lambda d: d.update(metadata=[]), "metadata"),
            (lambda d: d["records"][1]["edges"][0].pop("mechanism"), "schema"),
            (lambda d: d["records"][prediction_index].update(probability=float("nan")), "binary floating-point"),
        ]
        for mutation, message in cases:
            with self.subTest(message=message):
                if message == "schema":
                    value=deepcopy(self.data); mutation(value)
                    self.assertTrue(validate_document(value))
                else: self.assert_invalid(mutation, message)

    def test_every_cross_record_reference_requires_existence_and_kind(self) -> None:
        self.assert_invalid(lambda d: self._mutate_kind(d, "prediction", "belief_ref", "decision.umbrella.1"), "expected belief, got decision")
        self.assert_invalid(lambda d: self._mutate_kind(d, "decision", "prediction_ref", "missing"), "unknown record id missing")
        self.assert_invalid(lambda d: self._mutate_kind(d, "outcome", "decision_ref", "belief.weather"), "expected decision, got belief")
        self.assert_invalid(lambda d: self._mutate_kind(d, "error", "outcome_ref", "prediction.rain.1"), "expected outcome, got prediction")
        self.assert_invalid(lambda d: d["records"][0]["provenance"]["elenchus_session_refs"].append("missing"), "unknown FAR-ELENCHUS-1.0 session")

    @staticmethod
    def _mutate_kind(data, kind, field, value):
        next(x for x in data["records"] if x["kind"] == kind)[field] = value

    def test_lifecycle_and_provenance_bindings_are_mandatory(self) -> None:
        self.assert_invalid(lambda d: self._mutate_kind(d, "prediction", "probability", "0.400000"), "must equal snapshot hypothesis probability")
        self.assert_invalid(lambda d: self._mutate_kind(d, "decision", "belief_snapshot_ref", "snapshot.revised"), "decision must use prediction's frozen belief snapshot")
        self.assert_invalid(lambda d: self._mutate_kind(d, "outcome", "prediction_ref", "prediction.rain.2"), "outcome prediction and decision are not linked")
        self.assert_invalid(lambda d: d["records"][0]["revisions"][1].update(timestamp="2025-01-01T00:00:00Z"), "strictly chronological")
        self.assert_invalid(lambda d: d["records"][0]["revisions"][2]["evidence_refs"].append("e.outcome.2"), "absent from belief provenance")
        self.assert_invalid(lambda d: d["records"][0]["revisions"][2].update(trigger_outcome_ref="outcome.weather.2"), "triggering outcome evidence must be included")
        self.assert_invalid(lambda d: d["records"][0]["revisions"][2].update(timestamp="2026-01-02T00:00:00Z"), "must occur after outcome resolution")
        self.assert_invalid(lambda d: self._mutate_kind(d, "prediction", "provenance", {**self.record("prediction")["provenance"], "evidence_refs": []}), "must equal snapshot evidence_refs")
        self.assert_invalid(lambda d: d["snapshots"][0].update(sha256="sha256:"+"0"*64), "digest does not match")
        self.assert_invalid(lambda d: d["evidence"][0]["provenance"].update(artifact_sha256="sha256:"+"0"*64), "commit to UTF-8 statement bytes")

    def test_snapshot_commitment_has_exact_canonical_target(self) -> None:
        snapshot = self.data["snapshots"][0]
        self.assertEqual(snapshot["sha256"], sha256_commitment(snapshot_payload(snapshot)))
        changed = deepcopy(snapshot); changed["evidence_refs"].append("e.base")
        self.assertNotEqual(snapshot["sha256"], sha256_commitment(snapshot_payload(changed)))

    def test_scoring_is_fixed_context_and_rejects_ambiguous_numbers(self) -> None:
        old = getcontext().prec
        try:
            getcontext().prec = 6; first = score_binary("0.300000", 0)
            getcontext().prec = 40; second = score_binary("0.300000", 0)
        finally: getcontext().prec = old
        self.assertEqual({"brier": "0.090000000000", "log": "0.356674943939"}, first)
        self.assertEqual(first, second)
        for probability in ("0.000000", "1.000000", "0.3", "NaN", 0.3):
            with self.assertRaises(EpistemicValidationError): score_binary(probability, 0)

    def test_calibration_requires_declared_bins_and_comparable_class(self) -> None:
        rows = [{"probability":"0.300000","binary_outcome":0,"reference_class":"daily"},{"probability":"0.700000","binary_outcome":1,"reference_class":"daily"}]
        result = calibration(rows, bin_edges=["0","0.5","1"])
        self.assertEqual("0.090000000000", result["mean_brier"])
        self.assertEqual("0.300000", result["bins"][0]["mean_probability"])
        with self.assertRaises(EpistemicValidationError): calibration([], bin_edges=["0","1"])
        bad = deepcopy(rows); bad[1]["reference_class"] = "other"
        with self.assertRaises(EpistemicValidationError): calibration(bad, bin_edges=["0","1"])
        with self.assertRaises(EpistemicValidationError): calibration(rows, bin_edges=["0","0.5","0.5","1"])

    def test_evpi_tail_risk_and_regret_are_recomputed(self) -> None:
        self.assert_invalid(lambda d: self._mutate_kind(d, "decision", "expected_value_of_perfect_information", "3.000000"), "expected 2.400000")
        self.assert_invalid(lambda d: next(x for x in d["records"] if x["kind"]=="decision")["actions"][0]["tail_risk"].update(probability_at_or_below="0.200000"), "expected 0.700000")
        self.assert_invalid(lambda d: self._mutate_kind(d, "outcome", "regret", "1.000000"), "expected 0.000000")
        self.assert_invalid(lambda d: self._mutate_kind(d, "outcome", "regret", "-0.000000"), "negative zero is not canonical")

    def test_learning_result_is_derived_from_later_comparable_outcome(self) -> None:
        self.assert_invalid(lambda d: self._mutate_kind(d, "retest", "result", "WORSE"), "expected IMPROVED")
        self.assert_invalid(lambda d: self._mutate_kind(d, "retest", "comparison_outcome_refs", ["outcome.weather.1"]), "comparisons must be later outcomes")
        self.assert_invalid(lambda d: self._mutate_kind(d, "retest", "reference_class", "other"), "must equal every compared prediction")
        self.assert_invalid(lambda d: self._mutate_kind(d, "error", "belief_revision_ref", "rev.forecast"), "revision must be triggered by error outcome")
        errors = [self.record("error")]
        second = deepcopy(errors[0]); second["id"] = "error.weather.2"; second["root_cause"] = "different prose"
        modes = recurring_failure_modes([errors[0], second])
        self.assertEqual("NO_ERROR_CALIBRATION_OBSERVATION", modes[0]["failure_mode_code"])
        self.assertEqual(2, modes[0]["count"])

    def test_causal_contract_and_canonical_elenchus_are_typed(self) -> None:
        self.assert_invalid(lambda d: d["records"][1]["edges"].append({"cause":"rain","effect":"front","mechanism":"cycle","assumption_refs":[]}), "causal graph must be acyclic")
        self.assert_invalid(lambda d: d["records"][1]["interventions"][0].update(target_ref="missing"), "unknown variable")
        value=deepcopy(self.data); value["records"][1]["identification"]["status"]="PROVED"; self.assertTrue(validate_document(value))
        self.assert_invalid(lambda d: d["elenchus_sessions"][0]["record"]["commitments"][0].update(source_event_id="missing"), "ELENCHUS_COMMITMENT_UNKNOWN_SOURCE")

    def test_cli_validate_and_calibration_fail_closed(self) -> None:
        base=[sys.executable,"-m","mechanization.far_mechanization.cli","epistemic"]
        valid=subprocess.run(base+["validate",str(FIXTURE)],cwd=ROOT,text=True,capture_output=True,check=True)
        self.assertTrue(json.loads(valid.stdout)["valid"])
        result=subprocess.run(base+["calibration",str(FIXTURE),"--bin-edges","0,0.5,1"],cwd=ROOT,text=True,capture_output=True,check=True)
        self.assertEqual(2,json.loads(result.stdout)["resolved_count"])
        with tempfile.TemporaryDirectory() as directory:
            malformed=Path(directory)/"invalid-epistemic.json"
            malformed.write_text('{"probability": NaN}',encoding="utf-8")
            failed=subprocess.run(base+["validate",str(malformed)],cwd=ROOT,text=True,capture_output=True)
            self.assertNotEqual(0,failed.returncode); self.assertFalse(json.loads(failed.stdout)["valid"])


if __name__ == "__main__": unittest.main()
