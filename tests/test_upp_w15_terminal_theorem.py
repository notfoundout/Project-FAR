from __future__ import annotations

import importlib.util
import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
PATH = ROOT / "theory" / "terminal" / "upp_terminal_theorem_v1.py"
spec = importlib.util.spec_from_file_location("upp_terminal_theorem_v1_test", PATH)
assert spec and spec.loader
m = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = m
spec.loader.exec_module(m)


class TestUPPTerminalTheorem(unittest.TestCase):
    def test_canonical_selects_strictly_weakened_outcome(self):
        a = m.adjudicate(m.canonical_evidence())
        self.assertEqual(a.verdict, m.Verdict.PROVED)
        self.assertEqual(a.outcome, m.Outcome.WEAKENED)
        self.assertTrue(a.public_evaluation_authorized)

    def test_kernel_checked_variant_selects_full_outcome(self):
        e = m.canonical_evidence()
        e = m.TerminalEvidence(**{**e.__dict__, "central_semantic_theorem_kernel_checked": True})
        self.assertEqual(m.adjudicate(e).outcome, m.Outcome.FULL)

    def test_missing_workstream_blocks(self):
        e = m.canonical_evidence()
        e = m.TerminalEvidence(**{**e.__dict__, "completed_workstreams": frozenset(range(281, 295))})
        self.assertEqual(m.adjudicate(e).outcome, m.Outcome.BLOCKED)

    def test_refuted_property_defeats(self):
        e = m.canonical_evidence()
        e = m.TerminalEvidence(**{**e.__dict__, "refuted_properties": frozenset({"rccd_sufficiency_by_reconstruction"})})
        self.assertEqual(m.adjudicate(e).outcome, m.Outcome.DEFEATED)

    def test_unresolved_property_blocks(self):
        e = m.canonical_evidence()
        e = m.TerminalEvidence(**{**e.__dict__, "unresolved_properties": frozenset({"relative_maximality"})})
        self.assertEqual(m.adjudicate(e).verdict, m.Verdict.UNKNOWN)

    def test_open_world_overclaim_defeats(self):
        e = m.canonical_evidence()
        e = m.TerminalEvidence(**{**e.__dict__, "open_world_maximality_claimed": True})
        self.assertEqual(m.adjudicate(e).outcome, m.Outcome.DEFEATED)

    def test_metaphysical_overclaim_defeats(self):
        e = m.canonical_evidence()
        e = m.TerminalEvidence(**{**e.__dict__, "unrestricted_metaphysical_claimed": True})
        self.assertEqual(m.adjudicate(e).outcome, m.Outcome.DEFEATED)

    def test_hidden_machinery_failure_blocks(self):
        e = m.canonical_evidence()
        e = m.TerminalEvidence(**{**e.__dict__, "hidden_machinery_charged": False})
        self.assertEqual(m.adjudicate(e).outcome, m.Outcome.BLOCKED)

    def test_unknown_collapse_blocks(self):
        e = m.canonical_evidence()
        e = m.TerminalEvidence(**{**e.__dict__, "unknown_preserved": False})
        self.assertEqual(m.adjudicate(e).outcome, m.Outcome.BLOCKED)

    def test_non_circularity_required(self):
        e = m.canonical_evidence()
        e = m.TerminalEvidence(**{**e.__dict__, "definitions_non_circular": False})
        self.assertEqual(m.adjudicate(e).outcome, m.Outcome.BLOCKED)

    def test_no_executable_composition_blocks_weakened_proof(self):
        e = m.canonical_evidence()
        e = m.TerminalEvidence(**{**e.__dict__, "executable_composition_verified": False})
        self.assertEqual(m.adjudicate(e).outcome, m.Outcome.BLOCKED)


if __name__ == "__main__":
    unittest.main()
