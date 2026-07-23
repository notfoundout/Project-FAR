from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATH = ROOT / "theory" / "independence" / "upp_component_independence_v1.py"
SPEC = importlib.util.spec_from_file_location("upp_component_independence_v1", PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)


class ComponentIndependenceTests(unittest.TestCase):
    def test_canonical_certificate_proves_independence(self):
        self.assertEqual(MODULE.canonical_certificate().adjudicate(), MODULE.Verdict.PROVED)

    def test_every_component_has_a_separation_witness(self):
        targets = {w.target for w in MODULE.canonical_witnesses()}
        self.assertEqual(targets, set(MODULE.COMPONENTS))

    def test_missing_witness_refutes(self):
        cert = MODULE.canonical_certificate()
        broken = MODULE.IndependenceCertificate(cert.witnesses[:-1], True, True, True, True)
        self.assertEqual(broken.adjudicate(), MODULE.Verdict.REFUTED)

    def test_target_cannot_be_in_its_source_set(self):
        w = MODULE.SeparationWitness("historical_trace", frozenset(MODULE.COMPONENTS), "event_identity")
        self.assertEqual(w.adjudicate(), MODULE.Verdict.REFUTED)

    def test_wrong_lost_obligation_refutes(self):
        w = MODULE.SeparationWitness("semantic_interpretation", frozenset(set(MODULE.COMPONENTS)-{"semantic_interpretation"}), "event_identity")
        self.assertEqual(w.adjudicate(), MODULE.Verdict.REFUTED)

    def test_vacuous_witness_refutes(self):
        w = MODULE.canonical_witnesses()[0]
        broken = MODULE.SeparationWitness(w.target, w.preserved_sources, w.target_obligation_lost, nonvacuous=False)
        self.assertEqual(broken.adjudicate(), MODULE.Verdict.REFUTED)

    def test_open_machinery_refutes(self):
        w = MODULE.canonical_witnesses()[1]
        broken = MODULE.SeparationWitness(w.target, w.preserved_sources, w.target_obligation_lost, closed=False)
        self.assertEqual(broken.adjudicate(), MODULE.Verdict.REFUTED)

    def test_unresolved_witness_is_unknown(self):
        w = MODULE.canonical_witnesses()[2]
        unknown = MODULE.SeparationWitness(w.target, w.preserved_sources, w.target_obligation_lost, unresolved=True)
        self.assertEqual(unknown.adjudicate(), MODULE.Verdict.UNKNOWN)

    def test_circular_reduction_refutes(self):
        attempt = MODULE.ReductionAttempt("dependency_structure", frozenset({"semantic_interpretation"}), MODULE.OBLIGATIONS["dependency_structure"], True, True, True, True, circular=True)
        self.assertEqual(attempt.adjudicate(), MODULE.Verdict.REFUTED)

    def test_incomplete_reduction_refutes(self):
        attempt = MODULE.ReductionAttempt("recoverable_commitment", frozenset({"historical_trace"}), frozenset({"commitment_identity"}), True, True, True, True)
        self.assertEqual(attempt.adjudicate(), MODULE.Verdict.REFUTED)

    def test_non_effective_reduction_refutes(self):
        attempt = MODULE.ReductionAttempt("semantic_interpretation", frozenset({"dependency_structure"}), MODULE.OBLIGATIONS["semantic_interpretation"], False, True, True, True)
        self.assertEqual(attempt.adjudicate(), MODULE.Verdict.REFUTED)

    def test_unknown_reduction_stays_unknown(self):
        attempt = MODULE.ReductionAttempt("historical_trace", frozenset({"recoverable_commitment"}), frozenset(), True, True, True, True, unresolved=True)
        self.assertEqual(attempt.adjudicate(), MODULE.Verdict.UNKNOWN)

    def test_pairwise_aliasing_control_is_required(self):
        cert = MODULE.canonical_certificate()
        broken = MODULE.IndependenceCertificate(cert.witnesses, False, True, True, True)
        self.assertEqual(broken.adjudicate(), MODULE.Verdict.REFUTED)

    def test_joint_reduction_control_is_required(self):
        cert = MODULE.canonical_certificate()
        broken = MODULE.IndependenceCertificate(cert.witnesses, True, False, True, True)
        self.assertEqual(broken.adjudicate(), MODULE.Verdict.REFUTED)

    def test_interactions_must_be_preserved(self):
        cert = MODULE.canonical_certificate()
        broken = MODULE.IndependenceCertificate(cert.witnesses, True, True, False, True)
        self.assertEqual(broken.adjudicate(), MODULE.Verdict.REFUTED)

    def test_all_120_component_renamings_preserve_verdict(self):
        self.assertTrue(MODULE.all_component_permutations_preserve_verdict())


if __name__ == "__main__":
    unittest.main()
