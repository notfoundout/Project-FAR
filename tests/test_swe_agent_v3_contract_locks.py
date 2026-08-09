from __future__ import annotations

import importlib.util
import json
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest import mock

MODULE_PATH = Path(__file__).resolve().parents[1] / "research/external-validation/swe-agent-v3/verify_design.py"
SPEC = importlib.util.spec_from_file_location("swe_v3_contract_verify", MODULE_PATH)
verify_module = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(verify_module)


class SweAgentV3ContractLockTests(unittest.TestCase):
    """Semantic mutation tests that commit mutated fixture bytes before verification."""

    def setUp(self) -> None:
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.here = self.root / "research/external-validation/swe-agent-v3"
        self.here.parent.mkdir(parents=True)
        shutil.copytree(MODULE_PATH.parent, self.here)
        self.manifest = self.here / "design-manifest-v1.0.json"
        self.sync_committed()

    def tearDown(self) -> None:
        self.tmp.cleanup()

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

    def refresh_manifest_and_commit_fixture(self) -> None:
        # The reviewed Git tree is the current-byte authority. Mutations become the
        # fixture's new committed HEAD without rewriting a second hash registry.
        self.sync_committed()

    def mutate_json(self, name: str, mutation) -> None:
        path = self.here / name
        data = json.loads(path.read_text(encoding="utf-8"))
        mutation(data)
        path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8", newline="\n")
        self.refresh_manifest_and_commit_fixture()

    def mutate_text(self, name: str, old: str, new: str) -> None:
        path = self.here / name
        text = path.read_text(encoding="utf-8")
        self.assertIn(old, text)
        path.write_text(text.replace(old, new, 1), encoding="utf-8", newline="\n")
        self.refresh_manifest_and_commit_fixture()

    def verifier_context(self):
        return (
            mock.patch.object(verify_module, "ROOT", self.root),
            mock.patch.object(verify_module, "HERE", self.here),
            mock.patch.object(verify_module, "MANIFEST", self.manifest),
            mock.patch.object(verify_module, "_committed_blob_bytes", side_effect=self.committed_blob),
            mock.patch.object(verify_module.integrity, "ROOT", self.root),
            mock.patch.object(verify_module.integrity, "HERE", self.here),
            mock.patch.object(verify_module.integrity, "MANIFEST", self.manifest),
            mock.patch.object(verify_module.integrity, "_committed_blob_bytes", side_effect=self.committed_blob),
        )

    def assert_method_rejected_after_repin(self, method) -> None:
        contexts = self.verifier_context()
        with contexts[0], contexts[1], contexts[2], contexts[3], contexts[4], contexts[5], contexts[6], contexts[7]:
            with self.assertRaises(verify_module.DesignError):
                method()

    def reset_fixture(self) -> None:
        self.tearDown()
        self.setUp()

    def test_blinding_contract_is_exact_after_repin(self) -> None:
        mutations = (
            lambda d: d.pop("blinding"),
            lambda d: d.__setitem__("blinding", {}),
            lambda d: d["blinding"].pop("arm_labels_blinded_to_graders"),
            lambda d: d["blinding"].__setitem__("arm_labels_blinded_to_graders", False),
            lambda d: d["blinding"].__setitem__("arm_labels_blinded_to_graders", 1),
            lambda d: d["blinding"].__setitem__("operator_identity_blinded", True),
        )
        for index, mutation in enumerate(mutations):
            with self.subTest(index=index):
                self.reset_fixture(); self.mutate_json("preregistration-v1.0.json", mutation)
                self.assert_method_rejected_after_repin(verify_module.verify_preregistration)

    def test_complete_arm_treatment_semantics_are_exact_after_repin(self) -> None:
        mutations = (
            lambda d: d["arms"][2].__setitem__("extra_capsule", None),
            lambda d: d["arms"][2].pop("capsule_contract"),
            lambda d: d["arms"][0].__setitem__("extra_capsule", "far"),
            lambda d: d["arms"][1].__setitem__("extra_capsule", None),
            lambda d: d["arms"][2].__setitem__("budget", "larger_than_other_arms"),
            lambda d: d["arms"][1]["matching_requirements"].__setitem__("file_count_exact", False),
            lambda d: d["arms"][1]["matching_requirements"].__setitem__("file_count_exact", 1),
            lambda d: d["arms"][1]["forbidden_content"].remove("hidden tests"),
        )
        for index, mutation in enumerate(mutations):
            with self.subTest(index=index):
                self.reset_fixture(); self.mutate_json("preregistration-v1.0.json", mutation)
                self.assert_method_rejected_after_repin(verify_module.verify_preregistration)

    def test_complete_analysis_interval_and_outcome_contracts_are_exact_after_repin(self) -> None:
        mutations = (
            lambda d: d.pop("outcomes"),
            lambda d: d["outcomes"]["primary"].__setitem__("invalid_is_not_resolved", False),
            lambda d: d["outcomes"]["primary"].__setitem__("invalid_is_not_resolved", 1),
            lambda d: d["outcomes"]["primary"].__setitem__("source", "operator_judgment"),
            lambda d: d["outcomes"]["secondary"].remove("budget_exhausted"),
            lambda d: d["analysis"]["bootstrap_interval_spec"].__setitem__("confidence_level", 0.9),
            lambda d: d["analysis"]["bootstrap_interval_spec"].__setitem__("lower_tail_probability", 0.05),
            lambda d: d["analysis"]["bootstrap_interval_spec"].__setitem__("resample_unit", "repetition"),
            lambda d: d["analysis"]["bootstrap_interval_spec"].__setitem__("draws_with_replacement", 1),
            lambda d: d["analysis"]["bootstrap_interval_spec"]["task_order"].__setitem__("sealed_identity_ledger", "optional"),
        )
        for index, mutation in enumerate(mutations):
            with self.subTest(index=index):
                self.reset_fixture(); self.mutate_json("preregistration-v1.0.json", mutation)
                self.assert_method_rejected_after_repin(verify_module.verify_preregistration)

    def test_task_population_assignment_and_nonclaims_are_exact_after_repin(self) -> None:
        mutations = (
            lambda d: d["task_population"].pop("prohibited_tasks"),
            lambda d: d["task_population"].__setitem__("minimum_task_count", 12),
            lambda d: d["task_population"].__setitem__("sealed_identity_ledger_contract", "none"),
            lambda d: d["assignment"].__setitem__("order", "fixed"),
            lambda d: d["assignment"].__setitem__("paired_design", 1),
            lambda d: d["assignment"].__setitem__("randomization_seed_status", "selected_after_outcome_reveal"),
            lambda d: d["nonclaims"].remove("commercial readiness"),
        )
        for index, mutation in enumerate(mutations):
            with self.subTest(index=index):
                self.reset_fixture(); self.mutate_json("preregistration-v1.0.json", mutation)
                self.assert_method_rejected_after_repin(verify_module.verify_preregistration)

    def test_complete_capsule_contract_is_exact_after_repin(self) -> None:
        mutations = (
            lambda d: d.pop("required_outputs"),
            lambda d: d["required_outputs"].__setitem__("capsule_root_sha256", "premature"),
            lambda d: d["forbidden_content_classes"].remove("confirmatory repository names"),
            lambda d: d["allowed_content_classes"].append("general software-engineering advice unrelated to FAR"),
            lambda d: d["runtime_constraints"].__setitem__("read_only", 1),
            lambda d: d["runtime_constraints"].__setitem__("extra_context_window", True),
            lambda d: d["placebo_matching"].__setitem__("required", 1),
            lambda d: d["freeze_sequence"].clear(),
            lambda d: d["invalidation_rules"].clear(),
        )
        for index, mutation in enumerate(mutations):
            with self.subTest(index=index):
                self.reset_fixture(); self.mutate_json("treatment-capsule-contract-v1.0.json", mutation)
                self.assert_method_rejected_after_repin(verify_module.verify_capsule_contract)

    def test_evidence_and_pre_submission_contracts_are_semantically_rejected_after_repin(self) -> None:
        mutations = (
            (
                "- model provider, endpoint, model version, parameters, and provider request identifier;\n",
                "",
            ),
            (
                "- frozen task-manifest Git blob identity and frozen sealed identity-ledger Git blob identity;\n",
                "- frozen task-manifest Git blob identity;\n",
            ),
            (
                "## Pre-submission behavior contract\n\nThe agent must retain:\n",
                "## Pre-submission behavior contract\n\n",
            ),
            (
                "3. at least one observation that discriminates that hypothesis from an alternative;\n",
                "3. any observation;\n",
            ),
            (
                "6. a patch that modifies an intended repository path, unless the run terminates with an explicit no-patch failure.\n",
                "",
            ),
        )
        for index, (old, new) in enumerate(mutations):
            with self.subTest(index=index):
                self.reset_fixture(); self.mutate_text("evidence-and-analysis-plan-v1.0.md", old, new)
                self.assert_method_rejected_after_repin(verify_module.verify_text_boundaries)


if __name__ == "__main__":
    unittest.main()
