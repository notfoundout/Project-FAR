from __future__ import annotations

import copy
import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PKG = ROOT / "research/external-validation/swe-agent-v3"
sys.path.insert(0, str(PKG))

import verify_classification_input_digest_contract as digest_contract
import verify_review_closure_v1_2 as required_closure


class ClassificationInputDigestContractTests(unittest.TestCase):
    def _write_json(self, value):
        handle = tempfile.NamedTemporaryFile("w", suffix=".json", encoding="utf-8", delete=False)
        with handle:
            json.dump(value, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
        return Path(handle.name)

    def test_canonical_contract_and_required_validator_pass(self):
        digest_contract.validate_contract()
        required_closure.validate()

    def test_required_validator_rejects_post_outcome_classification_timing(self):
        data = json.loads(required_closure.AMENDMENT.read_text(encoding="utf-8"))
        data["task_manifest_effective_contract"]["task_strata"]["classification_timing"] = "computed after outcome reveal"
        path = self._write_json(data)
        try:
            with self.assertRaises(required_closure.DesignError):
                required_closure.validate(path)
        finally:
            path.unlink(missing_ok=True)

    def test_contract_rejects_weakened_task_identity_binding(self):
        data = json.loads(digest_contract.CONTRACT.read_text(encoding="utf-8"))
        data["digest_contract"]["task_identity_sha256"]["cross_task_transplantation_permitted"] = True
        path = self._write_json(data)
        try:
            with self.assertRaises(digest_contract.DesignError):
                digest_contract.validate_contract(path)
        finally:
            path.unlink(missing_ok=True)

    def test_descriptor_rejects_cross_task_transplantation_and_numeric_bool(self):
        task_a, task_b = "a" * 64, "b" * 64
        inputs = {key: False for key in digest_contract.CLASSIFICATION_INPUTS}
        bindings = {key: {"kind": "unverifiable", "locator": None} for key in digest_contract.CLASSIFICATION_INPUTS}
        descriptor = {"algorithm_id":"far-swe-v3-classification-input-digest-v2","task_identity_sha256":task_a,"classification_inputs":inputs,"evidence_bindings":bindings}
        expected = hashlib.sha256(digest_contract._canonical_json(descriptor)).hexdigest()
        self.assertEqual(digest_contract.validate_descriptor(task_a, descriptor, expected), expected)
        with self.assertRaises(digest_contract.DesignError):
            digest_contract.validate_descriptor(task_b, descriptor, expected)
        numeric = copy.deepcopy(descriptor)
        numeric["classification_inputs"][digest_contract.CLASSIFICATION_INPUTS[0]] = 0
        numeric_digest = hashlib.sha256(digest_contract._canonical_json(numeric)).hexdigest()
        with self.assertRaises(digest_contract.DesignError):
            digest_contract.validate_descriptor(task_a, numeric, numeric_digest)

    def test_descriptor_requires_evidence_and_false_for_unverifiable(self):
        task_id = "c" * 64
        inputs = {key: False for key in digest_contract.CLASSIFICATION_INPUTS}
        bindings = {key: {"kind": "unverifiable", "locator": None} for key in digest_contract.CLASSIFICATION_INPUTS}
        descriptor = {"algorithm_id":"far-swe-v3-classification-input-digest-v2","task_identity_sha256":task_id,"classification_inputs":inputs,"evidence_bindings":bindings}
        key = digest_contract.CLASSIFICATION_INPUTS[0]
        descriptor["classification_inputs"][key] = True
        expected = hashlib.sha256(digest_contract._canonical_json(descriptor)).hexdigest()
        with self.assertRaises(digest_contract.DesignError):
            digest_contract.validate_descriptor(task_id, descriptor, expected)
        descriptor["classification_inputs"][key] = False
        descriptor["evidence_bindings"][key] = {"kind":"source_evidence_locator","locator":""}
        expected = hashlib.sha256(digest_contract._canonical_json(descriptor)).hexdigest()
        with self.assertRaises(digest_contract.DesignError):
            digest_contract.validate_descriptor(task_id, descriptor, expected)


if __name__ == "__main__":
    unittest.main()
