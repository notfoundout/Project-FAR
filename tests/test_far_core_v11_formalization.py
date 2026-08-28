from __future__ import annotations

import unittest

from tools import check_far_core_v11_formalization as checker


class FARCoreV11FormalizationTests(unittest.TestCase):
    def test_machine_ledger_and_lean_sources_align(self):
        generated, _report, errors = checker.expected()
        self.assertEqual(errors, [])
        self.assertEqual(generated["w2_summary"]["formalized"], 13)
        self.assertEqual(generated["w2_summary"]["partial_obstruction"], 1)
        self.assertEqual(generated["w2_summary"]["contradiction_reopen_required"], 0)

    def test_no_w2_axiom_or_placeholder(self):
        generated, _report, _errors = checker.expected()
        self.assertEqual(generated["w2_summary"]["forbidden_placeholders"], 0)

    @staticmethod
    def _valid_axiom_output():
        lines = []
        for declaration, axioms in sorted(checker.EXPECTED_DECLARATION_AXIOMS.items()):
            if axioms:
                lines.append(f"'{declaration}' depends on axioms: [{', '.join(sorted(axioms))}]")
            else:
                lines.append(f"'{declaration}' does not depend on any axioms")
        return "\n".join(lines) + "\n"

    def test_axiom_audit_source_is_generated_and_rejects_output_forgery(self):
        source = checker.render_axiom_audit()
        self.assertEqual(checker.axiom_audit_source_errors(source), [])
        target = "#print axioms FARCoreV11.collision_refutes_sufficiency"
        forged = source.replace(target, f"-- {target}\n#eval IO.println \"fabricated\"")
        self.assertTrue(checker.axiom_audit_source_errors(forged))

    def test_runtime_axiom_output_matches_every_declaration(self):
        ledger = checker.load(checker.LEDGER_PATH)
        self.assertEqual(checker.axiom_output_errors(self._valid_axiom_output(), ledger), [])

    def test_hidden_transitive_axiom_and_constant_are_rejected(self):
        ledger = checker.load(checker.LEDGER_PATH)
        target = "FARCoreV11.collision_refutes_sufficiency"
        original = f"'{target}' does not depend on any axioms"
        hidden = f"'{target}' depends on axioms: [Hidden.secret]"
        errors = checker.axiom_output_errors(self._valid_axiom_output().replace(original, hidden), ledger)
        self.assertTrue(any("actual axiom set" in error and "Hidden.secret" in error for error in errors))
        self.assertIsNotNone(checker.FORBIDDEN.search("constant hidden : False\n"))

    def test_generated_views_are_current(self):
        self.assertEqual(checker.main([]), 0)


if __name__ == "__main__":
    unittest.main()
