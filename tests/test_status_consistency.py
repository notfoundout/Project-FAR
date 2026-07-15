from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

import check_status_consistency as csc


class StatusConsistencyTests(unittest.TestCase):
    def rec(self, cls, title, status, ident=None):
        return csc.StatusRecord("fixture.md", cls, 1, 1, ident, title, status, csc.normalize_status(status))

    def test_scoped_conditional_titles_do_not_match_broad_global_questions(self):
        resolved_min = self.rec("theorem", "Conditional Primitive Minimality", "Established (Conditional)", "T-001")
        research_min = self.rec("investigation", "Primitive Minimality", "Research", "VI-002")
        global_min = self.rec("open_question", "Global Primitive Minimality", "Active")
        resolved_ind = self.rec("theorem", "Conditional Primitive Independence", "Established (Conditional)", "T-002")
        research_ind = self.rec("investigation", "Primitive Independence", "Research", "VI-003")
        global_ind = self.rec("open_question", "Global Primitive Independence", "Active")
        findings = csc.find_contradictions([resolved_min, research_min, global_min, resolved_ind, research_ind, global_ind])
        self.assertEqual(findings, [])

    def test_unrelated_titles_sharing_only_primitive_do_not_match(self):
        a = self.rec("theorem", "Primitive Minimality", "Established")
        b = self.rec("open_question", "Primitive Weather Forecast", "Active")
        self.assertIsNone(csc.match_reason(a, b))

    def test_exact_unscoped_conditional_established_versus_research_is_contradiction(self):
        a = self.rec("theorem", "Primitive Independence", "Established (conditional)")
        b = self.rec("open_question", "Primitive Independence", "Research")
        findings = csc.find_contradictions([a, b])
        self.assertEqual(len(findings), 1)
        self.assertEqual(a.normalized_status, "established conditional")

    def test_exact_conditional_resolved_question_matches_conditional_theorem(self):
        a = self.rec("theorem", "Conditional Primitive Minimality", "Established (Conditional)")
        b = self.rec("open_question", "Conditional Primitive Minimality", "Resolved (Conditional)")
        self.assertIsNotNone(csc.match_reason(a, b))
        self.assertEqual(csc.find_contradictions([a, b]), [])

    def test_parsers_handle_malformed_or_missing_status_sections(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "VI-999-malformed.md"
            p.write_text("# Validation Investigation\n\n## Investigation ID\n\nVI-999\n\n## Title\n\nMalformed Primitive\n", encoding="utf-8")
            records = csc.parse_investigation(p)
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0].title, "Malformed Primitive")
        self.assertEqual(records[0].normalized_status, "missing")
        self.assertEqual(records[0].category, "unknown")


if __name__ == "__main__":
    unittest.main()
