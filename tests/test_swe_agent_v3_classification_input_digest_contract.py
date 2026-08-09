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
    def _write_json(self, value, *, directory: Path | None = None, name: str | None = None):
        if directory is None:
            handle = tempfile.NamedTemporaryFile("w", suffix=".json", encoding="utf-8", delete=False)
            with handle:
                json.dump(value, handle, ensure_ascii=False, indent=2)
                handle.write("\n")
            return Path(handle.name)
        path = directory / (name or "value.json")
        path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        return path

    def _binding(self, kind: str, locator: str, data: bytes):
        return {
            "kind": kind,
            "locator": locator,
            "sha256": hashlib.sha256(data).hexdigest(),
            "bytes": len(data),
        }

    def _valid_descriptor(
        self,
        task_id: str,
        *,
        all_true: bool = False,
        source_binding: dict | None = None,
        patch_binding: dict | None = None,
    ):
        inputs = {key: all_true for key in digest_contract.CLASSIFICATION_INPUTS}
        if all_true:
            source_binding = source_binding or self._binding("source_evidence_locator", "source.txt", b"source")
            patch_binding = patch_binding or self._binding("sealed_reference_patch_attestation", "patch.diff", b"patch")
            bindings = {
                key: copy.deepcopy(
                    patch_binding if key == "sealed_reference_patch_touches_multiple_files" else source_binding
                )
                for key in digest_contract.CLASSIFICATION_INPUTS
            }
        else:
            bindings = {
                key: {"kind": "unverifiable", "locator": None, "sha256": None, "bytes": None}
                for key in digest_contract.CLASSIFICATION_INPUTS
            }
        descriptor = {
            "algorithm_id": "far-swe-v3-classification-input-digest-v2",
            "task_identity_sha256": task_id,
            "classification_inputs": inputs,
            "evidence_bindings": bindings,
        }
        return descriptor, hashlib.sha256(digest_contract._canonical_json(descriptor)).hexdigest()

    def _build_population(self, directory: Path, repository_assignments: list[int] | None = None):
        repository_assignments = repository_assignments or [repo for repo in range(5) for _ in range(5)]
        evidence_dir = directory / "evidence"
        evidence_dir.mkdir(parents=True, exist_ok=True)
        source_bytes = b"sealed source evidence\n"
        patch_bytes = b"diff --git a/a b/a\n--- a/a\n+++ b/a\n"
        (evidence_dir / "source.txt").write_bytes(source_bytes)
        (evidence_dir / "reference.patch").write_bytes(patch_bytes)
        source_binding = self._binding("source_evidence_locator", "evidence/source.txt", source_bytes)
        patch_binding = self._binding(
            "sealed_reference_patch_attestation", "evidence/reference.patch", patch_bytes
        )

        manifest = []
        evidence = []
        strata = ["bug_fix", "test_failure", "behavioral_regression", "API_or_contract_change", "multi_file_change"]
        for index, repository_index in enumerate(repository_assignments):
            payload = f"task-{index}".encode("utf-8")
            identity_descriptor = {
                "algorithm_id": "far-swe-v3-authoritative-task-identity-v1",
                "repository_provider": "github.com",
                "repository_provider_id": 1000 + repository_index,
                "canonical_repository_url": f"https://github.com/example/repo-{repository_index}",
                "repository_commit_sha": f"{repository_index + 1:040x}",
                "task_payload_sha256": hashlib.sha256(payload).hexdigest(),
                "task_payload_bytes": len(payload),
            }
            task_id = hashlib.sha256(required_closure._canonical_json(identity_descriptor)).hexdigest()
            classification_descriptor, classification_sha = self._valid_descriptor(
                task_id,
                all_true=True,
                source_binding=source_binding,
                patch_binding=patch_binding,
            )
            bundle_descriptor = {
                "algorithm_id": "far-swe-v3-task-bundle-root-v4",
                "task_identity_sha256": task_id,
                "task_strata": strata,
                "classification_inputs_sha256": classification_sha,
            }
            bundle_root = hashlib.sha256(required_closure._canonical_json(bundle_descriptor)).hexdigest()
            blind_task_id = f"TASK-{index + 1:06d}"
            manifest.append({
                "blind_task_id": blind_task_id,
                "repository_blind_id": f"REPO-{repository_index + 1:04d}",
                "task_strata": strata,
                "task_identity_sha256": task_id,
                "task_bundle_root_sha256": bundle_root,
            })
            evidence.append({
                "blind_task_id": blind_task_id,
                "task_identity_descriptor": identity_descriptor,
                "classification_descriptor": classification_descriptor,
                "task_bundle_descriptor": bundle_descriptor,
            })
        manifest_path = self._write_json(manifest, directory=directory, name="task-manifest.json")
        evidence_path = self._write_json(evidence, directory=directory, name="evidence-registry.json")
        return manifest, evidence, manifest_path, evidence_path

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

    def test_descriptor_requires_exact_evidence_identity_and_false_for_unverifiable(self):
        task_id = "c" * 64
        descriptor, _ = self._valid_descriptor(task_id)
        key = digest_contract.CLASSIFICATION_INPUTS[0]
        descriptor["classification_inputs"][key] = True
        expected = hashlib.sha256(digest_contract._canonical_json(descriptor)).hexdigest()
        with self.assertRaises(digest_contract.DesignError):
            digest_contract.validate_descriptor(task_id, descriptor, expected)

        descriptor, _ = self._valid_descriptor(task_id, all_true=True)
        descriptor["evidence_bindings"][key]["sha256"] = "not-a-digest"
        expected = hashlib.sha256(digest_contract._canonical_json(descriptor)).hexdigest()
        with self.assertRaises(digest_contract.DesignError):
            digest_contract.validate_descriptor(task_id, descriptor, expected)

        descriptor, _ = self._valid_descriptor(task_id, all_true=True)
        descriptor["evidence_bindings"][key]["locator"] = "../escape.txt"
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
        reordered["evidence_bindings"][first_key] = {
            "bytes": None,
            "sha256": None,
            "locator": None,
            "kind": "unverifiable",
        }
        self.assertEqual(digest_contract.validate_descriptor(task_id, reordered, expected), expected)
        extra = copy.deepcopy(reordered)
        extra["unexpected"] = False
        with self.assertRaises(digest_contract.DesignError):
            digest_contract.validate_descriptor(task_id, extra, expected)

    def test_required_preexecution_path_validates_full_population_and_cli(self):
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            manifest, evidence, manifest_path, evidence_path = self._build_population(directory)
            required_closure.validate_instantiated_task_manifest(manifest_path, evidence_path)
            self.assertEqual(
                required_closure.main([
                    "--task-manifest", str(manifest_path),
                    "--evidence-registry", str(evidence_path),
                ]),
                0,
            )

            transplanted = copy.deepcopy(evidence)
            transplanted[0]["classification_descriptor"]["task_identity_sha256"] = "e" * 64
            transplanted_path = self._write_json(transplanted, directory=directory, name="transplanted.json")
            with self.assertRaises(required_closure.DesignError):
                required_closure.validate_instantiated_task_manifest(manifest_path, transplanted_path)

            numeric = copy.deepcopy(evidence)
            numeric[0]["classification_descriptor"]["classification_inputs"][digest_contract.CLASSIFICATION_INPUTS[0]] = 1
            numeric_path = self._write_json(numeric, directory=directory, name="numeric.json")
            with self.assertRaises(required_closure.DesignError):
                required_closure.validate_instantiated_task_manifest(manifest_path, numeric_path)

    def test_preexecution_rejects_missing_or_drifted_retained_evidence(self):
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            _, _, manifest_path, evidence_path = self._build_population(directory)
            source = directory / "evidence/source.txt"
            source.write_bytes(b"changed after commitment\n")
            with self.assertRaises(required_closure.DesignError):
                required_closure.validate_instantiated_task_manifest(manifest_path, evidence_path)
            source.unlink()
            with self.assertRaises(required_closure.DesignError):
                required_closure.validate_instantiated_task_manifest(manifest_path, evidence_path)

    def test_preexecution_rejects_population_below_minimum(self):
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            manifest, evidence, _, _ = self._build_population(directory)
            manifest_path = self._write_json(manifest[:1], directory=directory, name="small-manifest.json")
            evidence_path = self._write_json(evidence[:1], directory=directory, name="small-evidence.json")
            with self.assertRaises(required_closure.DesignError):
                required_closure.validate_instantiated_task_manifest(manifest_path, evidence_path)

    def test_preexecution_rejects_repository_cap_and_blind_id_aliasing(self):
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            assignments = [0] * 6 + [1] * 5 + [2] * 5 + [3] * 5 + [4] * 4
            _, _, manifest_path, evidence_path = self._build_population(directory, assignments)
            with self.assertRaises(required_closure.DesignError):
                required_closure.validate_instantiated_task_manifest(manifest_path, evidence_path)

        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            manifest, evidence, _, evidence_path = self._build_population(directory)
            manifest[1]["repository_blind_id"] = "REPO-9999"
            manifest_path = self._write_json(manifest, directory=directory, name="aliased-manifest.json")
            with self.assertRaises(required_closure.DesignError):
                required_closure.validate_instantiated_task_manifest(manifest_path, evidence_path)

    def test_preexecution_rejects_symlinked_retained_evidence(self):
        with tempfile.TemporaryDirectory() as tmp:
            directory = Path(tmp)
            _, _, manifest_path, evidence_path = self._build_population(directory)
            source = directory / "evidence/source.txt"
            target = directory / "evidence/source-target.txt"
            target.write_bytes(source.read_bytes())
            source.unlink()
            try:
                source.symlink_to(target.name)
            except (OSError, NotImplementedError):
                self.skipTest("symlinks are unavailable on this platform")
            with self.assertRaises(required_closure.DesignError):
                required_closure.validate_instantiated_task_manifest(manifest_path, evidence_path)


if __name__ == "__main__":
    unittest.main()
