import copy
import importlib.util
import json
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "fara_formal_kernel_promotion_checker",
    ROOT / "tools/check_fara_formal_kernel_promotion.py",
)
checker = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(checker)


class FaraFormalKernelPromotionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = json.loads(checker.MANIFEST.read_text())
        cls.canonical_text = (
            ROOT / cls.manifest["canonical_document"]["path"]
        ).read_text()
        cls.primitive_text = (ROOT / "frameworks/FARA/primitives.md").read_text()

    def test_fresh_promotion_validation(self):
        self.assertEqual([], checker.validate())

    def test_scope_inflation_fails(self):
        manifest = copy.deepcopy(self.manifest)
        manifest["scope"] = "all reasoning systems"
        self.assertIn(
            "manifest scope mismatch",
            checker.validate(manifest, check_files=False),
        )

    def test_lifecycle_stage_cannot_be_skipped(self):
        manifest = copy.deepcopy(self.manifest)
        manifest["lifecycle"]["replication"] = "pending"
        self.assertIn(
            "lifecycle stage not complete: replication",
            checker.validate(manifest, check_files=False),
        )

    def test_gate_registry_mutation_fails(self):
        manifest = copy.deepcopy(self.manifest)
        manifest["mandatory_gates"].pop()
        self.assertIn(
            "mandatory gate registry mismatch",
            checker.validate(manifest, check_files=False),
        )

    def test_sort_registry_mutation_fails(self):
        manifest = copy.deepcopy(self.manifest)
        manifest["sorts"].append("Operation")
        self.assertIn(
            "canonical sort registry mismatch",
            checker.validate(manifest, check_files=False),
        )

    def test_relation_signature_mutation_fails(self):
        manifest = copy.deepcopy(self.manifest)
        manifest["relations"]["participant"] = ["RelationOccurrence", "Object"]
        self.assertIn(
            "canonical relation signature mismatch",
            checker.validate(manifest, check_files=False),
        )

    def test_candidate_role_mutation_fails(self):
        manifest = copy.deepcopy(self.manifest)
        manifest["candidate_roles"]["typed-hypergraph"] = "canonical"
        self.assertIn(
            "candidate role adjudication mismatch",
            checker.validate(manifest, check_files=False),
        )

    def test_primitive_reclassification_fails(self):
        manifest = copy.deepcopy(self.manifest)
        manifest["primitive_registry_unchanged"].remove("Property")
        self.assertIn(
            "candidate primitive registry changed",
            checker.validate(manifest, check_files=False),
        )

    def test_external_independence_claim_fails(self):
        manifest = copy.deepcopy(self.manifest)
        manifest["external_investigator_independence"] = "established"
        self.assertIn(
            "manifest external_investigator_independence mismatch",
            checker.validate(manifest, check_files=False),
        )

    def test_required_nonclaim_removal_fails(self):
        manifest = copy.deepcopy(self.manifest)
        manifest["nonclaims"].remove("global uniqueness")
        self.assertIn(
            "required nonclaim missing",
            checker.validate(manifest, check_files=False),
        )

    def test_evidence_blob_lock_mutation_fails(self):
        manifest = copy.deepcopy(self.manifest)
        manifest["evidence_locks"]["source_spec"]["git_blob_sha"] = "0" * 40
        self.assertIn(
            "artifact blob lock mismatch: theory/formal/fara-canonical-kernel-v1.0.json",
            checker.validate(manifest),
        )

    def test_canonical_global_assertion_fails(self):
        text = self.canonical_text + "\nThe kernel is globally unique.\n"
        self.assertIn(
            "forbidden scope inflation: the kernel is globally unique",
            checker.validate(
                self.manifest,
                check_files=False,
                canonical_text=text,
            ),
        )

    def test_canonical_sort_deletion_fails(self):
        text = self.canonical_text.replace("- `Provenance`\n", "")
        self.assertIn(
            "canonical kernel sort missing: Provenance",
            checker.validate(
                self.manifest,
                check_files=False,
                canonical_text=text,
            ),
        )

    def test_canonical_primitive_list_mutation_fails(self):
        text = self.primitive_text.replace("- Reasoning Calculus", "- Operation")
        self.assertIn(
            "canonical candidate primitive list changed",
            checker.validate(
                self.manifest,
                check_files=False,
                primitive_text=text,
            ),
        )

    def test_authority_surfaces_are_synchronized(self):
        self.assertEqual([], checker.validate_authority_markers())


if __name__ == "__main__":
    unittest.main()
