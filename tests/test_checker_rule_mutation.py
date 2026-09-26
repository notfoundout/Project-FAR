import importlib.util
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("checker_rule_mutation", ROOT / "tools/checker_rule_mutation.py")
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
assert SPEC.loader
SPEC.loader.exec_module(MODULE)

SOURCE = """def validate(data):
    errors = []
    if data.get("a"):
        errors.append("a is set")
    problems = []
    if data.get("b"):
        problems.extend(["x"])
    total = errors.append("expressions that are not whole statements are skipped") or 0
    failures = []
    failures.append(
        "multi-line calls are not single-line rules")
    return errors
"""


class CheckerRuleMutationTest(unittest.TestCase):
    def test_single_line_rules_are_found(self):
        self.assertEqual([3, 6], MODULE.rule_lines(SOURCE))

    def test_mutation_replaces_only_the_rule_and_keeps_indentation(self):
        mutated = MODULE.mutate(SOURCE, 3).split("\n")
        self.assertEqual("        pass", mutated[3])
        self.assertEqual(SOURCE.split("\n")[:3] + SOURCE.split("\n")[4:], mutated[:3] + mutated[4:])
        compile("\n".join(mutated), "mutant", "exec")

    def test_non_rule_line_is_rejected(self):
        with self.assertRaises(ValueError):
            MODULE.mutate(SOURCE, 0)

    def test_evaluation_rejects_vacuous_and_low_scores(self):
        checker = "tools/check_semantic_consistency.py"
        survived = MODULE.Mutant(checker, 1, "errors.append(x)", False)
        killed = MODULE.Mutant(checker, 2, "errors.append(y)", True)
        self.assertEqual([], MODULE.evaluate({checker: [killed]}))
        self.assertTrue(MODULE.evaluate({checker: [killed, survived]}))
        self.assertTrue(any("vacuous" in e for e in MODULE.evaluate({checker: []})))

    def test_registry_names_existing_checkers_and_test_modules(self):
        for checker, entry in MODULE.REGISTRY.items():
            self.assertTrue((ROOT / checker).is_file(), checker)
            self.assertTrue(MODULE.rule_lines((ROOT / checker).read_text(encoding="utf-8")), checker)
            for module in entry["tests"]:
                self.assertTrue((ROOT / (module.replace(".", "/") + ".py")).is_file(), module)
            self.assertGreaterEqual(float(entry["min_kill"]), 0.9)

    def test_end_to_end_on_a_registered_checker_without_touching_the_tree(self):
        path = ROOT / "tools/check_claim_status_ceiling.py"
        before = path.read_bytes()
        results = MODULE.run(["tools/check_claim_status_ceiling.py"])
        self.assertEqual(before, path.read_bytes())
        mutants = results["tools/check_claim_status_ceiling.py"]
        self.assertTrue(mutants)
        self.assertTrue(all(m.killed for m in mutants), [m for m in mutants if not m.killed])


if __name__ == "__main__":
    unittest.main()
