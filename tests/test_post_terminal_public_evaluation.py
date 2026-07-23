from __future__ import annotations

import importlib.util
import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
PATH = ROOT / "theory" / "evaluation" / "post_terminal_public_evaluation_v1.py"
spec = importlib.util.spec_from_file_location("post_terminal_public_evaluation_v1_test", PATH)
assert spec and spec.loader
m = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = m
spec.loader.exec_module(m)


class TestPostTerminalPublicEvaluation(unittest.TestCase):
    def replace(self, submission, **changes):
        values = dict(submission.__dict__)
        values.update(changes)
        return m.Submission(**values)

    def test_canonical_independent_review_upgrades_only_evidence(self):
        result = m.assess(m.canonical_submission())
        self.assertEqual(result.verdict, m.Verdict.CONFIRMED)
        self.assertEqual(result.impact, m.Impact.UPGRADE_EVIDENCE)

    def test_missing_disclosure_is_inadmissible(self):
        s = m.canonical_submission()
        result = m.assess(self.replace(s, disclosure_fields=frozenset()))
        self.assertEqual(result.verdict, m.Verdict.INADMISSIBLE)

    def test_overclaim_is_inadmissible(self):
        s = m.canonical_submission()
        result = m.assess(self.replace(s, prohibited_promotions=frozenset({"open_world_maximality"})))
        self.assertEqual(result.verdict, m.Verdict.INADMISSIBLE)

    def test_unresolved_challenge_stays_unknown(self):
        s = m.canonical_submission()
        result = m.assess(self.replace(s, challenge_resolved=False, challenge_confirms_claim=False))
        self.assertEqual(result.verdict, m.Verdict.UNKNOWN)
        self.assertEqual(result.impact, m.Impact.RECORD_UNKNOWN)

    def test_confirmed_defect_requires_revision(self):
        s = m.canonical_submission()
        result = m.assess(self.replace(s, challenge_confirms_claim=False, challenge_defeats_claim=True))
        self.assertEqual(result.verdict, m.Verdict.DEFEATED)
        self.assertEqual(result.impact, m.Impact.REVISE)

    def test_conflicting_submission_stays_unknown(self):
        s = m.canonical_submission()
        result = m.assess(self.replace(s, challenge_defeats_claim=True, challenge_confirms_claim=True))
        self.assertEqual(result.verdict, m.Verdict.UNKNOWN)

    def test_internal_support_does_not_upgrade_independence(self):
        s = m.canonical_submission()
        result = m.assess(self.replace(s, independent=False))
        self.assertEqual(result.verdict, m.Verdict.CONFIRMED)
        self.assertEqual(result.impact, m.Impact.NONE)

    def test_missing_provenance_is_inadmissible(self):
        s = m.canonical_submission()
        result = m.assess(self.replace(s, immutable_artifact=False))
        self.assertEqual(result.verdict, m.Verdict.INADMISSIBLE)


if __name__ == "__main__":
    unittest.main()
