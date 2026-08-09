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

    def _valid_descriptor(self, task_id: str, *, all_true: bool = False):
        inputs = {key: all_true for key in digest_contract.CLASSIFICATION_INPUTS}
        bindings = {
            key: ({"kind": "source_evidence_locator", "locator": f"sealed://{key}"} if all_true else {"kind": "unverifiable", "locator": None})
            for key in digest_contract.CLASSIFICATION_INPUTS
        }
        descriptor = {
            "algorithm_id": "far-swe-v3-classification-input-digest-v2",
            "task_identity_sha256": task_id,
            "classification_inputs": inputs,
            "evidence_bindings": bindings,
        }
        return descriptor, hashlib.sha256(digest_contract._canonical_json(descriptor)).hexdigest()

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
        descriptor, expected = self._valid_descriptor(task_a)
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
        descriptor, _ = self._valid_descriptor(task_id)
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

    def test_descriptor_accepts_json_object_reordering_but_not_shape_drift(self):
        task_id = "d" * 64
        descriptor, expected = self._valid_descriptor(task_id)
        reordered = {
            "evidence_bindings": dict(reversed(list(descriptor["evidence_bindings"].items()))),
            "classification_inputs": dict(reversed(list(descriptor["classification_inputs"].items()))),
            "task_identity_sha256": descriptor["task_identity_sha256"],
            "algorithm_id": descriptor["algorithm_id"],
        }
        first_key = digest_contract.CLASSIFICATION_INPUTS[0]
        reordered["evidence_bindings"][first_key] = {"locator": None, "kind": "unverifiable"}
        self.assertEqual(digest_contract.validate_descriptor(task_id, reordered, expected), expected)
        extra = copy.deepcopy(reordered)
        extra["unexpected"] = False
        with self.assertRaises(digest_contract.DesignError):
            digest_contract.validate_descriptor(task_id, extra, expected)

    def test_required_preexecution_path_recomputes_every_task_binding(self):
        identity_descriptor = {
            "algorithm_id": "far-swe-v3-authoritative-task-identity-v1",
            "repository_provider": "github.com",
            "repository_provider_id": 123,
            "canonical_repository_url": "https://github.com/example/repo",
            "repository_commit_sha": "1" * 40,
            "task_payload_sha256": "2" * 64,
            "task_payload_bytes": 1234,
        }
        task_id = hashlib.sha256(required_closure._canonical_json(identity_descriptor)).hexdigest()
        classification_descriptor, classification_sha = self._valid_descriptor(task_id, all_true=True)
        strata = ["bug_fix", "test_failure", "behavioral_regression", "API_or_contract_change", "multi_file_change"]
        bundle_descriptor = {
            "algorithm_id": "far-swe-v3-task-bundle-root-v4",
            "task_identity_sha256": task_id,
            "task_strata": strata,
            "classification_inputs_sha256": classification_sha,
        }
        bundle_root = hashlib.sha256(required_closure._canonical_json(bundle_descriptor)).hexdigest()
        manifest = [{
            "blind_task_id": "TASK-000001",
            "repository_blind_id": "REPO-0001",
            "task_strata": strata,
            "task_identity_sha256": task_id,
            "task_bundle_root_sha256": bundle_root,
        }]
        evidence = [{
            "blind_task_id": "TASK-000001",
            "task_identity_descriptor": identity_descriptor,
            "classification_descriptor": classification_descriptor,
            "task_bundle_descriptor": bundle_descriptor,
        }]
        manifest_path = self._write_json(manifest)
        evidence_path = self._write_json(evidence)
        try:
            required_closure.validate_instantiated_task_manifest(manifest_path, evidence_path)
            transplanted = copy.deepcopy(evidence)
            transplanted[0]["classification_descriptor"]["task_identity_sha256"] = "e" * 64
            transplanted_path = self._write_json(transplanted)
            try:
                with self.assertRaises(required_closure.DesignError):
                    required_closure.validate_instantiated_task_manifest(manifest_path, transplanted_path)
            finally:
                transplanted_path.unlink(missing_ok=True)
            numeric = copy.deepcopy(evidence)
            numeric[0]["classification_descriptor"]["classification_inputs"][digest_contract.CLASSIFICATION_INPUTS[0]] = 1
            numeric_path = self._write_json(numeric)
            try:
                with self.assertRaises(required_closure.DesignError):
                    required_closure.validate_instantiated_task_manifest(manifest_path, numeric_path)
            finally:
                numeric_path.unlink(missing_ok=True)
        finally:
            manifest_path.unlink(missing_ok=True)
            evidence_path.unlink(missing_ok=True)


if __name__ == "__main__":
    unittest.main()
