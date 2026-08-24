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
        cls.kernel = checker.load_source_kernel(cls.manifest)
        cls.model = cls.kernel.sample_model()
        cls.mapping = {
            sort_name: {
                member: f"renamed::{sort_name}::{index}"
                for index, member in enumerate(cls.model["sorts"][sort_name])
            }
            for sort_name in checker.EXPECTED_SORTS
        }
        cls.renamed = checker.rename_model(cls.model, cls.mapping)

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

    def test_identity_criteria_mutation_fails(self):
        manifest = copy.deepcopy(self.manifest)
        manifest["identity_criteria"]["literal_identifier_spelling_semantic"] = True
        self.assertIn(
            "identity criteria mismatch",
            checker.validate(manifest, check_files=False),
        )

    def test_equivalence_relation_mutation_fails(self):
        manifest = copy.deepcopy(self.manifest)
        manifest["model_equivalence"]["requires_bijection_per_sort"] = False
        self.assertIn(
            "model equivalence relation mismatch",
            checker.validate(manifest, check_files=False),
        )

    def test_candidate_role_mutation_fails(self):
        manifest = copy.deepcopy(self.manifest)
        manifest["candidate_roles"]["typed-hypergraph"] = "canonical"
        self.assertIn(
            "candidate role adjudication mismatch",
            checker.validate(manifest, check_files=False),
        )

    def test_historical_role_registry_mutation_fails(self):
        manifest = copy.deepcopy(self.manifest)
        manifest["primitive_registry_unchanged"].remove("Property")
        self.assertIn(
            "historical seven-role registry changed",
            checker.validate(manifest, check_files=False),
        )

    def test_terminal_reclassification_mutation_fails(self):
        manifest = copy.deepcopy(self.manifest)
        manifest["terminal_reclassification"]["current_classification"] = "global-primitives"
        self.assertIn(
            "terminal schema-role reclassification mismatch",
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

    def test_sort_preserving_renaming_is_equivalent(self):
        self.assertEqual([], self.kernel.validate_model(self.renamed))
        self.assertEqual(
            [],
            checker.validate_model_isomorphism(
                self.model,
                self.renamed,
                self.mapping,
            ),
        )

    def test_occurrence_identity_collapse_is_not_equivalent(self):
        mapping = copy.deepcopy(self.mapping)
        first, second = self.model["sorts"]["RelationOccurrence"][:2]
        mapping["RelationOccurrence"][second] = mapping["RelationOccurrence"][first]
        errors = checker.validate_model_isomorphism(
            self.model,
            self.renamed,
            mapping,
        )
        self.assertIn(
            "isomorphism is not injective: RelationOccurrence",
            errors,
        )

    def test_provenance_loss_is_not_equivalent(self):
        changed = copy.deepcopy(self.renamed)
        changed["relations"]["provenance_of"].pop()
        self.assertIn(
            "relation not preserved and reflected: provenance_of",
            checker.validate_model_isomorphism(
                self.model,
                changed,
                self.mapping,
            ),
        )

    def test_precedence_reversal_is_not_equivalent(self):
        changed = copy.deepcopy(self.renamed)
        changed["relations"]["precedes"] = [
            list(reversed(row)) for row in changed["relations"]["precedes"]
        ]
        self.assertIn(
            "relation not preserved and reflected: precedes",
            checker.validate_model_isomorphism(
                self.model,
                changed,
                self.mapping,
            ),
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

    def test_canonical_relation_deletion_fails(self):
        text = self.canonical_text.replace(
            "| `participant` | `RelationOccurrence × Role × Object` |\n",
            "",
        )
        self.assertIn(
            "canonical kernel relation missing: participant",
            checker.validate(
                self.manifest,
                check_files=False,
                canonical_text=text,
            ),
        )

    def test_canonical_equivalence_deletion_fails(self):
        text = self.canonical_text.replace(
            "sort-preserving relational isomorphism",
            "unspecified equivalence",
        )
        self.assertIn(
            "canonical kernel marker missing: sort-preserving relational isomorphism",
            checker.validate(
                self.manifest,
                check_files=False,
                canonical_text=text,
            ),
        )

    def test_canonical_schema_role_list_mutation_fails(self):
        text = self.primitive_text.replace(
            "| Reasoning Calculus |", "| Operation |"
        )
        self.assertIn(
            "canonical schema-role list changed",
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
