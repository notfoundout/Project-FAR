from __future__ import annotations

import importlib.util
import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIR = ROOT / "research/external-validation/swe-agent-v3"
STRATA = ["bug_fix", "test_failure", "behavioral_regression", "API_or_contract_change", "multi_file_change"]


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


class SingleSourceIntegrityTests(unittest.TestCase):
    def test_mutable_current_identity_mirrors_are_absent(self) -> None:
        sources = {
            name: (DIR / name).read_text(encoding="utf-8")
            for name in (
                "verify_integrity.py",
                "verify_design.py",
                "verify_review_closure.py",
                "verify_amendment_v1_1.py",
            )
        }
        forbidden = {
            "verify_integrity.py": ("EXPECTED_MANIFEST_GIT_BLOB_SHA1",),
            "verify_design.py": ("ARTIFACT_BLOBS", "PILOT_DIGEST", "FREEZE_SEQUENCE_DIGEST", "INVALIDATION_RULES_DIGEST"),
            "verify_review_closure.py": (
                "SEED_BLOB", "TASK_BLOB", "CAPSULE_BLOB", "GATE_BLOB", "RECORD_SCHEMA_DIGEST",
                "TASK_BUNDLE_ROOT_DIGEST", "REPOSITORY_IDENTITY_DIGEST", "CAPSULE_REL", "GATE_REL",
            ),
            "verify_amendment_v1_1.py": (
                "AMEND_SHA", "README_SHA", "REPL_DIGEST", "ARITH_DIGEST", "PREREG_BLOB", "PLAN_BLOB",
            ),
        }
        for filename, tokens in forbidden.items():
            for token in tokens:
                self.assertNotIn(token, sources[filename], f"mutable/current duplicate identity survived: {filename}:{token}")

    def test_historical_authority_is_self_contained_and_not_git_history_dependent(self) -> None:
        verifier = (DIR / "verify_amendment_v1_1.py").read_text(encoding="utf-8")
        for token in ("import subprocess", "git fetch --unshallow", "rev-parse", "cat-file", "merge-base", "--is-ancestor"):
            self.assertNotIn(token, verifier)
        authority = json.loads((DIR / "historical-authority-v1.0.json").read_text(encoding="utf-8"))
        self.assertEqual(authority["base_design_head"], "83c951aca9be6a09a4517044ae531a3ed1bcc9a9")
        self.assertEqual(authority["artifact_status"], "Archive")
        self.assertFalse(authority["current_design_authority"])
        self.assertFalse(authority["execution_authorized"])
        self.assertEqual(len(authority["snapshots"]), 2)
        self.assertEqual(
            {entry["historical_git_blob_sha1"] for entry in authority["snapshots"]},
            {"7147f6814f76eb0f73fd0741b17b2501e38e6f57", "15b352d54a524d9caf827018b608028c004f8f13"},
        )

    def test_every_governed_final_contract_is_in_design_manifest(self) -> None:
        manifest = json.loads((DIR / "design-manifest-v1.0.json").read_text(encoding="utf-8"))
        paths = {entry["path"] for entry in manifest["artifacts"]}
        required = {
            "research/external-validation/swe-agent-v3/bootstrap-seed-commitment-contract-v1.0.json",
            "research/external-validation/swe-agent-v3/critical-harm-thresholds-v1.0.json",
            "research/external-validation/swe-agent-v3/historical-authority-v1.0.json",
            "research/external-validation/swe-agent-v3/historical-base-83c951/preregistration-v1.0.json",
            "research/external-validation/swe-agent-v3/historical-base-83c951/evidence-and-analysis-plan-v1.0.md",
            "research/external-validation/swe-agent-v3/task-manifest-contract-v1.0.json",
        }
        self.assertTrue(required.issubset(paths))

    def test_seed_is_direct_commitment_not_mutable_launch_derivation(self) -> None:
        data = json.loads((DIR / "bootstrap-seed-commitment-contract-v1.0.json").read_text(encoding="utf-8"))
        self.assertEqual(data["schema_version"], "1.1")
        self.assertEqual(data["commitment"]["method"], "direct_precommitted_value")
        self.assertFalse(data["commitment"]["artifact_inputs_permitted"])
        self.assertFalse(data["commitment"]["mutable_launch_inputs_permitted"])
        self.assertFalse(data["commitment"]["task_identity_inputs_permitted"])
        self.assertFalse(data["commitment"]["outcome_or_grade_inputs_permitted"])
        self.assertRegex(data["rng_contract"]["seed_hex"], r"^[0-9a-f]{64}$")
        source = (DIR / "verify_review_closure.py").read_text(encoding="utf-8")
        self.assertNotIn("treatment_capsule_git_blob_sha1", source)
        self.assertNotIn("execution_gate_git_blob_sha1", source)

    def test_schema_1_4_identity_and_strata_contract_is_preserved(self) -> None:
        data = json.loads((DIR / "task-manifest-contract-v1.0.json").read_text(encoding="utf-8"))
        self.assertEqual(data["schema_version"], "1.4")
        self.assertFalse(data["execution_authorized"])
        self.assertEqual(data["repository_identity_contract"]["supported_provider"], "github.com only")
        self.assertIn("positive JSON integer", data["task_bundle_root_contract"]["descriptor_values"]["repository_provider_id"])
        self.assertTrue(data["record_schema"]["blind_task_id"]["unique"])
        self.assertTrue(data["record_schema"]["task_bundle_root_sha256"]["unique"])
        self.assertEqual(data["record_schema"]["strata"]["allowed_values_in_canonical_order"], STRATA)
        self.assertFalse(data["order_contract"]["runtime_sorting_permitted"])

    def test_instantiated_manifest_enforces_unique_roots_canonical_strata_and_coverage(self) -> None:
        module = load_module("single_source_review_closure_records", DIR / "verify_review_closure.py")
        records = [
            {
                "blind_task_id": f"TASK-{i + 1:06d}",
                "repository_blind_id": f"REPO-{i + 1:04d}",
                "task_bundle_root_sha256": f"{i + 1:064x}",
                "strata": [label],
            }
            for i, label in enumerate(STRATA)
        ]
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "tasks.json"
            path.write_text(json.dumps(records, indent=2) + "\n", encoding="utf-8")
            self.assertEqual(len(module.validate_instantiated_task_manifest(path)), 5)
            cases = []
            duplicate_root = json.loads(json.dumps(records)); duplicate_root[1]["task_bundle_root_sha256"] = duplicate_root[0]["task_bundle_root_sha256"]; cases.append(duplicate_root)
            missing_stratum = json.loads(json.dumps(records)); missing_stratum[-1]["strata"] = [STRATA[0]]; cases.append(missing_stratum)
            bad_order = json.loads(json.dumps(records)); bad_order[0]["strata"] = [STRATA[1], STRATA[0]]; cases.append(bad_order)
            duplicate_stratum = json.loads(json.dumps(records)); duplicate_stratum[0]["strata"] = [STRATA[0], STRATA[0]]; cases.append(duplicate_stratum)
            for altered in cases:
                path.write_text(json.dumps(altered, indent=2) + "\n", encoding="utf-8")
                with self.assertRaises(module.DesignError):
                    module.validate_instantiated_task_manifest(path)

    def test_semantic_weakening_fails_without_repinning_verifier(self) -> None:
        module = load_module("single_source_review_closure", DIR / "verify_review_closure.py")
        data = json.loads((DIR / "task-manifest-contract-v1.0.json").read_text(encoding="utf-8"))
        mutations = (
            lambda d: d.__setitem__("schema_version", "1.3"),
            lambda d: d["record_schema"]["task_bundle_root_sha256"].__setitem__("unique", False),
            lambda d: d["record_schema"]["strata"].__setitem__("allowed_values_in_canonical_order", STRATA[:-1]),
            lambda d: d["task_bundle_root_contract"]["descriptor_values"].__setitem__("repository_provider_id", "owner/name string"),
            lambda d: d["order_contract"].__setitem__("runtime_sorting_permitted", True),
        )
        for mutation in mutations:
            altered = json.loads(json.dumps(data)); mutation(altered)
            with tempfile.TemporaryDirectory() as tmp:
                path = Path(tmp) / "task.json"
                path.write_text(json.dumps(altered, indent=2) + "\n", encoding="utf-8")
                with self.assertRaises(module.DesignError):
                    module.verify_task_identity_contract(path)

    def test_critical_harm_weakening_fails_semantically(self) -> None:
        module = load_module("single_source_review_closure_harm", DIR / "verify_review_closure.py")
        data = json.loads((DIR / "critical-harm-thresholds-v1.0.json").read_text(encoding="utf-8"))
        mutations = (
            lambda d: d["rate_harms"]["invalid_run_rate"].__setitem__("critical_threshold", {"numerator": 1, "denominator": 5}),
            lambda d: d["rate_harms"]["regression_introduction_rate"].__setitem__("slot_denominator", "complete cases only"),
            lambda d: d["zero_tolerance_harms"]["hidden_task_leakage"].__setitem__("trigger_rule", "count > 1"),
            lambda d: d.__setitem__("versioning_rule", "thresholds may change after exposure"),
        )
        for mutation in mutations:
            altered = json.loads(json.dumps(data)); mutation(altered)
            with tempfile.TemporaryDirectory() as tmp:
                path = Path(tmp) / "harm.json"
                path.write_text(json.dumps(altered, indent=2) + "\n", encoding="utf-8")
                with self.assertRaises(module.DesignError):
                    module.verify_critical_harm_contract(path)


if __name__ == "__main__":
    unittest.main()
