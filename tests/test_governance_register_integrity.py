import importlib.util
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("governance_register_integrity", ROOT / "tools/check_governance_register_integrity.py")
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(MODULE)


class GovernanceRegisterIntegrityTest(unittest.TestCase):
    def setUp(self):
        self._directory = tempfile.TemporaryDirectory()
        self.root = Path(self._directory.name)
        for relative in (MODULE.LIMITATIONS, MODULE.OPEN_PROBLEMS, *MODULE.SURFACES):
            target = self.root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / relative, target)

    def tearDown(self):
        self._directory.cleanup()

    def edit(self, relative, old, new):
        path = self.root / relative
        text = path.read_text(encoding="utf-8")
        self.assertIn(old, text)
        path.write_text(text.replace(old, new, 1), encoding="utf-8")

    def assertRejected(self, expected):
        errors = MODULE.validate(self.root)
        self.assertTrue(any(expected in error for error in errors), errors)

    def test_repository_passes(self):
        self.assertEqual([], MODULE.validate())
        completed = subprocess.run([sys.executable, "tools/check_governance_register_integrity.py"], cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(0, completed.returncode, completed.stdout)

    def test_benign_edits_pass(self):
        # A whole-file hash pin fails these; a semantic guard must not.
        for relative in (MODULE.LIMITATIONS, MODULE.STATUS, "README.md", "docs/governance/claim-status-matrix.md"):
            with (self.root / relative).open("a", encoding="utf-8") as handle:
                handle.write("\nEditorial note: formatting only.\n")
        self.assertEqual([], MODULE.validate(self.root))

    def test_new_register_entries_pass(self):
        with (self.root / MODULE.LIMITATIONS).open("a", encoding="utf-8") as handle:
            handle.write("| LIM-999 | New limitation. | Scope | Open. |\n")
        self.assertEqual([], MODULE.validate(self.root))

    def test_deleted_limitation_is_rejected(self):
        self.edit(MODULE.LIMITATIONS, "| LIM-002 |", "| REMOVED |")
        self.assertRejected("register entries removed: LIM-002")

    def test_deleted_open_problem_is_rejected(self):
        text = (self.root / MODULE.OPEN_PROBLEMS).read_text(encoding="utf-8")
        row = next(line for line in text.splitlines() if line.startswith("| OP-28 |"))
        self.edit(MODULE.OPEN_PROBLEMS, row + "\n", "")
        self.assertRejected("register entries removed: OP-28")

    def test_empty_status_cell_is_rejected(self):
        self.edit(MODULE.LIMITATIONS, "| Open; requires an equivalence design. |", "|  |")
        self.assertRejected("LIM-002 has an empty status/completion cell")

    def test_status_surface_promotion_is_rejected(self):
        self.edit(MODULE.STATUS,
                  "I2 verified isolation, I3 external replication, novelty, and priority are not established.",
                  "I2 verified isolation, I3 external replication, novelty, and priority are established.")
        self.assertRejected("docs/project-status.md: unnegated assurance promotion")

    def test_claim_matrix_promotion_is_rejected(self):
        self.edit("docs/governance/claim-status-matrix.md", "but not I2/I3 external validation", "and I2/I3 external validation established")
        self.assertRejected("claim-status-matrix.md: unnegated assurance promotion")

    def test_readme_universality_claim_is_rejected(self):
        with (self.root / "README.md").open("a", encoding="utf-8") as handle:
            handle.write("\nProject FAR is proven to be the universal architecture of all reasoning.\n")
        self.assertRejected("README.md: unnegated assurance promotion")

    def test_canonical_map_novelty_claim_is_rejected(self):
        with (self.root / "docs/CANONICAL_MAP.md").open("a", encoding="utf-8") as handle:
            handle.write("\nNovelty and priority are established by the W1 review.\n")
        self.assertRejected("CANONICAL_MAP.md: unnegated assurance promotion")

    def test_removed_boundary_statement_is_rejected(self):
        path = self.root / MODULE.STATUS
        kept = [line for line in path.read_text(encoding="utf-8").splitlines() if "priority" not in line.lower()]
        path.write_text("\n".join(kept) + "\n", encoding="utf-8")
        self.assertRejected("no negated boundary statement for priority")

    def test_missing_surface_is_rejected(self):
        (self.root / "docs/CANONICAL_MAP.md").unlink()
        self.assertEqual(["missing governance surface: docs/CANONICAL_MAP.md"], MODULE.validate(self.root))

    def test_negated_or_conditional_mentions_pass(self):
        for clause in (
            "Universality remains unresolved.",
            "Novelty is not established.",
            "Priority would be established only if an external search found no earlier work.",
            "I3 replication cannot be established by internal reruns.",
        ):
            self.assertEqual([], MODULE.promotion_clauses(clause), clause)


if __name__ == "__main__":
    unittest.main()
