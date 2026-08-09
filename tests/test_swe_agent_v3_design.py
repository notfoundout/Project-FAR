from __future__ import annotations

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


class SweAgentV3DesignTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self._reset_fixture()

    def tearDown(self) -> None:
        self.tmp.cleanup()

    def _reset_fixture(self) -> None:
        self.root = Path(self.tmp.name)
        if self.root.exists():
            for child in self.root.iterdir():
                if child.is_dir():
                    shutil.rmtree(child)
                else:
                    child.unlink()
        self.here = self.root / "research/external-validation/swe-agent-v3"
        self.here.parent.mkdir(parents=True)
        shutil.copytree(MODULE_PATH.parent, self.here)
        self.sync_committed()

    def sync_committed(self) -> None:
        self.committed = {
            str(path.relative_to(self.root)).replace("\\", "/"): path.read_bytes()
            for path in self.here.rglob("*")
            if path.is_file() and not path.is_symlink()
        }

    def committed_blob(self, relative: str) -> bytes:
        try:
            return self.committed[relative]
        except KeyError as exc:
            raise verify_module.DesignError(f"test committed blob missing: {relative}") from exc

    def run_verify(self) -> None:
        manifest = self.here / "design-manifest-v1.0.json"
        with (
            mock.patch.object(verify_module, "ROOT", self.root),
            mock.patch.object(verify_module, "HERE", self.here),
            mock.patch.object(verify_module, "MANIFEST", manifest),
            mock.patch.object(verify_module, "_committed_blob_bytes", side_effect=self.committed_blob),
            mock.patch.object(verify_module.integrity, "ROOT", self.root),
            mock.patch.object(verify_module.integrity, "HERE", self.here),
            mock.patch.object(verify_module.integrity, "MANIFEST", manifest),
            mock.patch.object(verify_module.integrity, "_committed_blob_bytes", side_effect=self.committed_blob),
        ):
            verify_module.verify()

    def refresh_manifest(self, commit: bool = True) -> None:
        if commit:
            self.sync_committed()

    def mutate_json(self, name: str, mutation) -> None:
        path = self.here / name
        data = json.loads(path.read_text(encoding="utf-8"))
        mutation(data)
        path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8", newline="\n")
        self.refresh_manifest()

    def rejected(self) -> None:
        with self.assertRaises(verify_module.DesignError):
            self.run_verify()

    def test_canonical_design_passes(self) -> None:
        self.run_verify()

    def test_execution_arm_and_launch_binding_weakening_are_rejected(self) -> None:
        cases = (
            ("execution-gate-v1.0.json", lambda d: d.__setitem__("execution_authorized", True)),
            ("execution-gate-v1.0.json", lambda d: d["gates"].__setitem__("theory_version_frozen", True)),
            ("execution-gate-v1.0.json", lambda d: d["pilot_gates"].pop("critical_harm_thresholds_frozen_and_verified")),
            ("execution-gate-v1.0.json", lambda d: d["launch_record_required_bindings"].remove("sealed_identity_ledger_git_blob_sha1")),
            ("preregistration-v1.0.json", lambda d: d["arms"].pop(1)),
            ("preregistration-v1.0.json", lambda d: d.__setitem__("historical_v2_pooling_permitted", True)),
        )
        for name, mutation in cases:
            with self.subTest(name=name):
                original = (self.here / name).read_bytes(); self.mutate_json(name, mutation); self.rejected()
                (self.here / name).write_bytes(original); self.refresh_manifest()

    def test_execution_control_source_and_ledger_shapes_are_exact(self) -> None:
        cases = (
            ("preregistration-v1.0.json", lambda d: d.__setitem__("execution_controls", {})),
            ("preregistration-v1.0.json", lambda d: d["execution_controls"].pop("same_tools_across_arms")),
            ("preregistration-v1.0.json", lambda d: d["execution_controls"].__setitem__("same_hidden_state_across_arms", True)),
            ("preregistration-v1.0.json", lambda d: d["execution_controls"].__setitem__("same_tools_across_arms", False)),
            ("preregistration-v1.0.json", lambda d: d["task_population"].__setitem__("sealed_identity_ledger_contract", "none")),
            ("task-manifest-contract-v1.0.json", lambda d: d["sealed_identity_ledger_contract"].__setitem__("access_control", "agent may inspect identities")),
            ("task-manifest-contract-v1.0.json", lambda d: d["sealed_identity_ledger_contract"].__setitem__("population_rule", "count blind labels")),
            ("treatment-capsule-contract-v1.0.json", lambda d: d["source"].pop("repository")),
            ("treatment-capsule-contract-v1.0.json", lambda d: d["source"].__setitem__("repository", "example/unrelated")),
            ("treatment-capsule-contract-v1.0.json", lambda d: d["source"].__setitem__("branch", "main")),
            ("treatment-capsule-contract-v1.0.json", lambda d: d["source"].__setitem__("commit_sha", "0" * 40)),
        )
        for name, mutation in cases:
            with self.subTest(name=name):
                original = (self.here / name).read_bytes(); self.mutate_json(name, mutation); self.rejected()
                (self.here / name).write_bytes(original); self.refresh_manifest()

    def test_tolerance_contract_is_exact(self) -> None:
        cases = (
            ("preregistration-v1.0.json", lambda d: d["arms"][1]["matching_requirements"]["relative_tolerance"].__setitem__("reference_count", "placebo_count")),
            ("preregistration-v1.0.json", lambda d: d["arms"][1]["matching_requirements"]["relative_tolerance"].__setitem__("rounding", "nearest percent")),
            ("treatment-capsule-contract-v1.0.json", lambda d: d["placebo_matching"]["relative_tolerance"].__setitem__("integer_acceptance_rule", "abs(placebo_count-far_treatment_count)*100 < far_treatment_count")),
        )
        for name, mutation in cases:
            with self.subTest(name=name):
                original = (self.here / name).read_bytes(); self.mutate_json(name, mutation); self.rejected()
                (self.here / name).write_bytes(original); self.refresh_manifest()

    def test_task_order_identity_strata_and_ledger_contract_is_exact(self) -> None:
        cases = (
            ("preregistration-v1.0.json", lambda d: d["analysis"]["bootstrap_interval_spec"]["task_order"].__setitem__("sequence_rule", "numeric runtime sort")),
            ("preregistration-v1.0.json", lambda d: d["analysis"]["bootstrap_interval_spec"]["task_order"].__setitem__("sealed_identity_ledger", "optional")),
            ("task-manifest-contract-v1.0.json", lambda d: d["record_schema"]["blind_task_id"].__setitem__("unicode_permitted", True)),
            ("task-manifest-contract-v1.0.json", lambda d: d["record_schema"]["task_bundle_root_sha256"].__setitem__("unique", False)),
            ("task-manifest-contract-v1.0.json", lambda d: d["record_schema"]["strata"].__setitem__("coverage_rule", "optional coverage")),
            ("task-manifest-contract-v1.0.json", lambda d: d["order_contract"].__setitem__("authoritative_sequence", "locale-sorted blind_task_id")),
        )
        for name, mutation in cases:
            with self.subTest(name=name):
                original = (self.here / name).read_bytes(); self.mutate_json(name, mutation); self.rejected()
                (self.here / name).write_bytes(original); self.refresh_manifest()

    def test_recursive_type_exactness_rejects_python_equal_json_distinct_values(self) -> None:
        cases = (
            ("preregistration-v1.0.json", lambda d: d["assignment"].__setitem__("paired_design", 1)),
            ("preregistration-v1.0.json", lambda d: d["arms"][1].__setitem__("required", 1)),
            ("preregistration-v1.0.json", lambda d: d["outcomes"]["primary"].__setitem__("invalid_is_not_resolved", 1)),
            ("preregistration-v1.0.json", lambda d: d["pilot"].__setitem__("required", 1)),
            ("preregistration-v1.0.json", lambda d: d["arms"][1]["matching_requirements"]["relative_tolerance"].__setitem__("floating_point_permitted", 0)),
            ("treatment-capsule-contract-v1.0.json", lambda d: d["placebo_matching"].__setitem__("required", 1)),
            ("treatment-capsule-contract-v1.0.json", lambda d: d["runtime_constraints"].__setitem__("read_only", 1)),
            ("execution-gate-v1.0.json", lambda d: d.__setitem__("execution_authorized", 0)),
            ("critical-harm-thresholds-v1.0.json", lambda d: d.__setitem__("execution_authorized", 0)),
        )
        for name, mutation in cases:
            with self.subTest(name=name):
                original = (self.here / name).read_bytes(); self.mutate_json(name, mutation); self.rejected()
                (self.here / name).write_bytes(original); self.refresh_manifest()

    def test_strict_json_rejects_nonfinite_duplicate_and_bom(self) -> None:
        cases = (
            ("preregistration-v1.0.json", lambda text: text.replace('"minimum_task_count": 24', '"minimum_task_count": NaN')),
            ("preregistration-v1.0.json", lambda text: text.replace('"maximum_fraction_from_one_repository": 0.2', '"maximum_fraction_from_one_repository": Infinity')),
            ("execution-gate-v1.0.json", lambda text: text.replace('"execution_authorized": false,', '"execution_authorized": false,\n  "execution_authorized": false,', 1)),
        )
        for name, mutation in cases:
            with self.subTest(name=name):
                path = self.here / name; original = path.read_bytes()
                path.write_text(mutation(original.decode()), encoding="utf-8", newline="\n"); self.refresh_manifest(); self.rejected()
                path.write_bytes(original); self.refresh_manifest()
        path = self.here / "preregistration-v1.0.json"; original = path.read_bytes()
        path.write_bytes(b"\xef\xbb\xbf" + original); self.refresh_manifest(); self.rejected()

    def test_committed_bytes_and_manifest_are_fail_closed(self) -> None:
        readme = self.here / "README.md"
        readme.write_bytes(readme.read_bytes().replace(b"\n", b"\r\n")); self.rejected(); self.setUp_after_drift()
        manifest = self.here / "design-manifest-v1.0.json"
        manifest.write_text(manifest.read_text() + "\n", encoding="utf-8", newline="\n"); self.rejected()

    def test_seed_value_drift_is_rejected_by_byte_authority_without_semantic_hash_mirror(self) -> None:
        seed = self.here / "bootstrap-seed-commitment-contract-v1.0.json"
        data = json.loads(seed.read_text(encoding="utf-8"))
        data["rng_contract"]["seed_hex"] = "0" * 64
        seed.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8", newline="\n")
        # Model the mutation as a newly committed HEAD. The semantic seed verifier
        # must reject the changed frozen value independently of byte-identity drift.
        self.refresh_manifest()
        self.rejected()

    def setUp_after_drift(self) -> None:
        self._reset_fixture()

    def test_byte_policy_symlinks_and_manifest_metadata_are_rejected(self) -> None:
        policy = self.here / ".gitattributes"
        policy.write_text("* text=auto\n", encoding="utf-8", newline="\n"); self.refresh_manifest(); self.rejected(); self.setUp_after_drift()
        manifest = self.here / "design-manifest-v1.0.json"; data = json.loads(manifest.read_text())
        data["artifacts"][0]["git_blob_sha1"] = "0" * 40; manifest.write_text(json.dumps(data, indent=2) + "\n"); self.sync_committed(); self.rejected(); self.setUp_after_drift()
        target = self.here / "question-v1.0.md"; copy = self.here / "question-copy.md"; copy.write_bytes(target.read_bytes()); target.unlink(); target.symlink_to(copy.name); self.rejected()

    def test_missingness_decisions_seed_and_harm_semantics_are_exact(self) -> None:
        cases = (
            ("treatment-capsule-contract-v1.0.json", lambda d: d["runtime_constraints"].__setitem__("extra_context_window", True)),
            ("preregistration-v1.0.json", lambda d: d["analysis"]["invalid_run_and_cell_policy"].__setitem__("retained_invalid_repetition_makes_entire_task_arm_cell_missing", False)),
            ("preregistration-v1.0.json", lambda d: d["analysis"]["decision_categories"].__setitem__("no_practical_advantage", "upper bound < 0.10")),
            ("preregistration-v1.0.json", lambda d: d["analysis"].__setitem__("bootstrap_seed_status", "selected_after_outcome_reveal")),
            ("bootstrap-seed-commitment-contract-v1.0.json", lambda d: d["commitment"].__setitem__("mutable_launch_inputs_permitted", True)),
            ("critical-harm-thresholds-v1.0.json", lambda d: d["rate_harms"]["invalid_run_rate"].__setitem__("critical_threshold", {"numerator": 1, "denominator": 5})),
            ("critical-harm-thresholds-v1.0.json", lambda d: d["rate_harms"]["regression_introduction_rate"].__setitem__("slot_numerator", "operator-attributed regressions only")),
            ("critical-harm-thresholds-v1.0.json", lambda d: d["zero_tolerance_harms"]["hidden_task_leakage"].__setitem__("trigger_rule", "slot_numerator > 1")),
            ("critical-harm-thresholds-v1.0.json", lambda d: d["evidence_retention"]["required_for_each_zero_tolerance_harm"].remove("slot_denominator")),
        )
        for name, mutation in cases:
            with self.subTest(name=name):
                original = (self.here / name).read_bytes(); self.mutate_json(name, mutation); self.rejected()
                (self.here / name).write_bytes(original); self.refresh_manifest()


if __name__ == "__main__":
    unittest.main()
