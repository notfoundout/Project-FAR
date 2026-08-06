from __future__ import annotations

import hashlib
import importlib.util
import json
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest import mock

MODULE_PATH = Path(__file__).resolve().parents[1] / "research/external-validation/swe-agent-v3/verify_design.py"
SPEC = importlib.util.spec_from_file_location("swe_v3_verify", MODULE_PATH)
verify_module = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(verify_module)


def git_blob_sha1(path: Path) -> str:
    data = path.read_bytes()
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


class SweAgentV3DesignTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        source = MODULE_PATH.parent
        target = self.root / "research/external-validation/swe-agent-v3"
        target.parent.mkdir(parents=True)
        shutil.copytree(source, target)
        self.here = target

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def run_verify(self) -> None:
        with mock.patch.object(verify_module, "ROOT", self.root), \
             mock.patch.object(verify_module, "HERE", self.here), \
             mock.patch.object(verify_module, "MANIFEST", self.here / "design-manifest-v1.0.json"):
            verify_module.verify()

    def rewrite_manifest(self) -> None:
        manifest_path = self.here / "design-manifest-v1.0.json"
        manifest = json.loads(manifest_path.read_text())
        for entry in manifest["artifacts"]:
            path = self.root / entry["path"]
            entry.clear()
            entry.update(
                path=str(path.relative_to(self.root)).replace("\\", "/"),
                git_blob_sha1=git_blob_sha1(path),
                bytes=path.stat().st_size,
            )
        manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")

    def mutate_json(self, name: str, fn) -> None:
        path = self.here / name
        data = json.loads(path.read_text())
        fn(data)
        path.write_text(json.dumps(data, indent=2) + "\n")
        self.rewrite_manifest()

    def test_canonical_design_passes(self) -> None:
        self.run_verify()

    def test_execution_authorization_is_rejected(self) -> None:
        self.mutate_json("execution-gate-v1.0.json", lambda d: d.__setitem__("execution_authorized", True))
        with self.assertRaises(verify_module.DesignError):
            self.run_verify()

    def test_any_true_gate_is_rejected(self) -> None:
        self.mutate_json(
            "execution-gate-v1.0.json",
            lambda d: d["gates"].__setitem__("theory_version_frozen", True),
        )
        with self.assertRaises(verify_module.DesignError):
            self.run_verify()

    def test_missing_placebo_arm_is_rejected(self) -> None:
        self.mutate_json("preregistration-v1.0.json", lambda d: d["arms"].pop(1))
        with self.assertRaises(verify_module.DesignError):
            self.run_verify()

    def test_weak_placebo_matching_is_rejected(self) -> None:
        self.mutate_json(
            "preregistration-v1.0.json",
            lambda d: d["arms"][1]["matching_requirements"].__setitem__(
                "utf8_bytes_relative_tolerance", 0.25
            ),
        )
        with self.assertRaises(verify_module.DesignError):
            self.run_verify()

    def test_preregistration_tolerances_cannot_drift_below_contract(self) -> None:
        self.mutate_json(
            "preregistration-v1.0.json",
            lambda d: d["arms"][1]["matching_requirements"].__setitem__(
                "frozen_tokenizer_tokens_relative_tolerance", 0.005
            ),
        )
        with self.assertRaises(verify_module.DesignError):
            self.run_verify()

    def test_project_far_task_prohibition_is_required(self) -> None:
        self.mutate_json(
            "preregistration-v1.0.json",
            lambda d: d["task_population"].__setitem__("prohibited_task_repositories", []),
        )
        with self.assertRaises(verify_module.DesignError):
            self.run_verify()

    def test_too_few_tasks_is_rejected(self) -> None:
        self.mutate_json(
            "preregistration-v1.0.json",
            lambda d: d["task_population"].__setitem__("minimum_task_count", 4),
        )
        with self.assertRaises(verify_module.DesignError):
            self.run_verify()

    def test_v2_pooling_is_rejected(self) -> None:
        self.mutate_json(
            "preregistration-v1.0.json",
            lambda d: d.__setitem__("historical_v2_pooling_permitted", True),
        )
        with self.assertRaises(verify_module.DesignError):
            self.run_verify()

    def test_invalid_repetition_cannot_be_averaged_away(self) -> None:
        self.mutate_json(
            "preregistration-v1.0.json",
            lambda d: d["analysis"]["invalid_run_and_cell_policy"].__setitem__(
                "retained_invalid_repetition_makes_entire_task_arm_cell_missing", False
            ),
        )
        with self.assertRaises(verify_module.DesignError):
            self.run_verify()

    def test_decision_categories_cannot_overlap_harm(self) -> None:
        self.mutate_json(
            "preregistration-v1.0.json",
            lambda d: d["analysis"]["decision_categories"].__setitem__(
                "no_practical_advantage", "95% paired-task bootstrap upper bound < 0.10"
            ),
        )
        with self.assertRaises(verify_module.DesignError):
            self.run_verify()

    def test_bootstrap_seed_must_be_committed_before_reveal(self) -> None:
        self.mutate_json(
            "preregistration-v1.0.json",
            lambda d: d["analysis"].__setitem__(
                "bootstrap_seed_status", "selected_after_outcome_reveal"
            ),
        )
        with self.assertRaises(verify_module.DesignError):
            self.run_verify()

    def test_capsule_source_cannot_be_pretended_frozen(self) -> None:
        self.mutate_json(
            "treatment-capsule-contract-v1.0.json",
            lambda d: d["source"].__setitem__("commit_sha", "a" * 40),
        )
        with self.assertRaises(verify_module.DesignError):
            self.run_verify()

    def test_capsule_runtime_constraints_are_exact(self) -> None:
        mutations = {
            "read_only": False,
            "network_access": True,
            "writes_outside_run_evidence_directory": True,
            "extra_tool_permissions": True,
            "extra_context_window": True,
            "extra_model_calls": True,
            "mutable_remote_dependencies": True,
        }
        for key, value in mutations.items():
            with self.subTest(key=key):
                with tempfile.TemporaryDirectory() as tmp:
                    source = self.here
                    clone = Path(tmp) / "research/external-validation/swe-agent-v3"
                    clone.parent.mkdir(parents=True)
                    shutil.copytree(source, clone)
                    data_path = clone / "treatment-capsule-contract-v1.0.json"
                    data = json.loads(data_path.read_text())
                    data["runtime_constraints"][key] = value
                    data_path.write_text(json.dumps(data, indent=2) + "\n")
                    manifest_path = clone / "design-manifest-v1.0.json"
                    manifest = json.loads(manifest_path.read_text())
                    clone_root = Path(tmp)
                    for entry in manifest["artifacts"]:
                        path = clone_root / entry["path"]
                        entry.clear()
                        entry.update(
                            path=str(path.relative_to(clone_root)).replace("\\", "/"),
                            git_blob_sha1=git_blob_sha1(path),
                            bytes=path.stat().st_size,
                        )
                    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
                    with mock.patch.object(verify_module, "ROOT", clone_root), \
                         mock.patch.object(verify_module, "HERE", clone), \
                         mock.patch.object(verify_module, "MANIFEST", manifest_path):
                        with self.assertRaises(verify_module.DesignError):
                            verify_module.verify()

    def test_numeric_boolean_equivalents_are_rejected(self) -> None:
        for field, value in (("read_only", 1), ("network_access", 0)):
            with self.subTest(field=field):
                with tempfile.TemporaryDirectory() as tmp:
                    clone_root = Path(tmp)
                    clone = clone_root / "research/external-validation/swe-agent-v3"
                    clone.parent.mkdir(parents=True)
                    shutil.copytree(self.here, clone)
                    data_path = clone / "treatment-capsule-contract-v1.0.json"
                    data = json.loads(data_path.read_text())
                    data["runtime_constraints"][field] = value
                    data_path.write_text(json.dumps(data, indent=2) + "\n")
                    manifest_path = clone / "design-manifest-v1.0.json"
                    manifest = json.loads(manifest_path.read_text())
                    for entry in manifest["artifacts"]:
                        path = clone_root / entry["path"]
                        entry.clear()
                        entry.update(
                            path=str(path.relative_to(clone_root)).replace("\\", "/"),
                            git_blob_sha1=git_blob_sha1(path),
                            bytes=path.stat().st_size,
                        )
                    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
                    with mock.patch.object(verify_module, "ROOT", clone_root), \
                         mock.patch.object(verify_module, "HERE", clone), \
                         mock.patch.object(verify_module, "MANIFEST", manifest_path):
                        with self.assertRaises(verify_module.DesignError):
                            verify_module.verify()

    def test_capsule_placebo_matching_contract_is_exact(self) -> None:
        self.mutate_json(
            "treatment-capsule-contract-v1.0.json",
            lambda d: d["placebo_matching"].__setitem__("read_order_exact", False),
        )
        with self.assertRaises(verify_module.DesignError):
            self.run_verify()

    def test_capsule_placebo_required_must_be_boolean(self) -> None:
        self.mutate_json(
            "treatment-capsule-contract-v1.0.json",
            lambda d: d["placebo_matching"].__setitem__("required", 1),
        )
        with self.assertRaises(verify_module.DesignError):
            self.run_verify()

    def test_manifest_tamper_is_rejected(self) -> None:
        path = self.here / "question-v1.0.md"
        path.write_text(path.read_text() + "\npost hoc mutation\n")
        with self.assertRaises(verify_module.DesignError):
            self.run_verify()

    def test_manifest_byte_count_tamper_is_rejected(self) -> None:
        manifest_path = self.here / "design-manifest-v1.0.json"
        manifest = json.loads(manifest_path.read_text())
        manifest["artifacts"][0]["bytes"] += 1
        manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
        with self.assertRaises(verify_module.DesignError):
            self.run_verify()

    def test_manifest_blob_identity_tamper_is_rejected(self) -> None:
        manifest_path = self.here / "design-manifest-v1.0.json"
        manifest = json.loads(manifest_path.read_text())
        manifest["artifacts"][0]["git_blob_sha1"] = "0" * 40
        manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
        with self.assertRaises(verify_module.DesignError):
            self.run_verify()

    def test_legacy_sha256_manifest_field_is_rejected(self) -> None:
        manifest_path = self.here / "design-manifest-v1.0.json"
        manifest = json.loads(manifest_path.read_text())
        manifest["artifacts"][0]["sha256"] = "0" * 64
        manifest_path.write_text(json.dumps(manifest, indent=2) + "\n")
        with self.assertRaises(verify_module.DesignError):
            self.run_verify()

    def test_symlinked_governed_artifact_is_rejected(self) -> None:
        target = self.here / "question-v1.0.md"
        copy = self.here / "question-copy.md"
        copy.write_bytes(target.read_bytes())
        target.unlink()
        target.symlink_to(copy.name)
        with self.assertRaises(verify_module.DesignError):
            self.run_verify()


if __name__ == "__main__":
    unittest.main()
