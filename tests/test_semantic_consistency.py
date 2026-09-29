import copy
import importlib.util
import json
import shutil
import tempfile
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("semantic_check", ROOT / "tools/check_semantic_consistency.py")
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(MODULE)


DATA = json.loads(MODULE.REGISTRY.read_text(encoding="utf-8"))


def mutated(change):
    data = copy.deepcopy(DATA)
    change(data)
    return MODULE.validate(data)


class SemanticConsistencyTest(unittest.TestCase):
    def test_registry_and_canonical_documents_are_consistent(self):
        self.assertEqual([], MODULE.validate())

    def test_frozen_swe_agent_evidence_is_not_a_required_theory_input(self):
        data = __import__("json").loads(MODULE.REGISTRY.read_text(encoding="utf-8"))
        self.assertFalse(any("swe-agent-v2" in path for path in data["required_documents"]))

    def assertRejected(self, change, expected):
        errors = mutated(change)
        self.assertTrue(any(expected in error for error in errors), errors)

    def test_reversed_dependency_is_rejected(self):
        self.assertRejected(lambda d: d["dependencies"].append(["foundations", "FAR"]), "reversed/circular dependency: foundations -> FAR")

    def test_self_dependency_is_rejected(self):
        self.assertRejected(lambda d: d["dependencies"].append(["FARA", "FARA"]), "reversed/circular dependency: FARA -> FARA")

    def test_every_canonical_edge_reversed_is_rejected(self):
        for dependent, prerequisite in DATA["dependencies"]:
            self.assertRejected(lambda d, a=dependent, b=prerequisite: d["dependencies"].append([b, a]), f"reversed/circular dependency: {prerequisite} -> {dependent}")

    def test_unknown_dependency_layer_is_rejected(self):
        self.assertRejected(lambda d: d["dependencies"].append(["FARX", "FAR"]), "unknown dependency layer: FARX -> FAR")

    def test_duplicate_dependency_layer_is_rejected(self):
        self.assertRejected(lambda d: d["dependency_order"].append("FAR"), "dependency_order contains duplicates")

    def test_duplicate_term_ownership_is_rejected(self):
        self.assertRejected(lambda d: d["canonical_terms"].append(dict(d["canonical_terms"][0], owner="FARO")), "duplicate canonical term ownership: " + DATA["canonical_terms"][0]["term"])

    def test_unowned_or_unclassified_term_is_rejected(self):
        self.assertRejected(lambda d: d["canonical_terms"][0].pop("owner"), "unclassified canonical term: " + DATA["canonical_terms"][0]["term"])
        self.assertRejected(lambda d: d["canonical_terms"][0].__setitem__("status", "theorem"), "unclassified canonical term: " + DATA["canonical_terms"][0]["term"])

    def test_duplicate_strong_claim_is_rejected(self):
        self.assertRejected(lambda d: d["strong_claims"].append(dict(d["strong_claims"][0])), "duplicate strong-claim identifier")

    def test_strong_claim_without_status_or_scope_is_rejected(self):
        self.assertRejected(lambda d: d["strong_claims"][0].__setitem__("scope", ""), "strong claim lacks status/scope: FAR-CORE-001")
        self.assertRejected(lambda d: d["strong_claims"][0].pop("status"), "strong claim lacks status/scope: FAR-CORE-001")

    def test_missing_required_procedure_is_rejected(self):
        self.assertRejected(lambda d: d["procedures"].remove("uncertainty output"), "unclassified procedure(s): uncertainty output")

    def test_missing_theorem_families_is_rejected(self):
        self.assertRejected(lambda d: d.__setitem__("theorem_families", []), "theorem/proof families are not classified")

    def test_missing_required_document_is_rejected(self):
        self.assertRejected(lambda d: d["required_documents"].append("docs/governance/absent.md"), "missing canonical audit document: docs/governance/absent.md")

    def _root_copy(self, directory):
        root = Path(directory)
        for relative in ["README.md", "docs/ARCHITECTURE.md", "docs/CANONICAL_MAP.md", "docs/glossary/canonical-terminology.md", *DATA["required_documents"]]:
            target = root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(MODULE.ROOT / relative, target)
        return root

    def test_legacy_terminology_in_active_document_is_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            root = self._root_copy(directory)
            self.assertEqual([], MODULE.validate(DATA, root))
            with (root / "docs/ARCHITECTURE.md").open("a", encoding="utf-8") as handle:
                handle.write("\nThe Accepted Root Theory governs.\n")
            self.assertIn("active canonical document promotes legacy terminology: docs/ARCHITECTURE.md", MODULE.validate(DATA, root))

    def test_term_missing_from_terminology_authority_is_rejected(self):
        term = DATA["canonical_terms"][0]["term"]
        with tempfile.TemporaryDirectory() as directory:
            root = self._root_copy(directory)
            path = root / "docs/glossary/canonical-terminology.md"
            path.write_text(path.read_text(encoding="utf-8").replace(f"| {term} |", "| removed |"), encoding="utf-8")
            self.assertIn(f"registry term missing from terminology authority: {term}", MODULE.validate(DATA, root))


if __name__ == "__main__":
    unittest.main()
