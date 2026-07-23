import importlib.util
import sys
import unittest
from pathlib import Path


MODULE_PATH = Path(__file__).parents[1] / "theory" / "foundation" / "upp_dependency_structure_v1.py"
SPEC = importlib.util.spec_from_file_location("upp_dependency_structure_v1", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)

Truth = MODULE.Truth
Verdict = MODULE.Verdict
DependencyKind = MODULE.DependencyKind
DependencyEdge = MODULE.DependencyEdge
DependencyAssessment = MODULE.DependencyAssessment


def edge(**updates):
    data = dict(
        edge_id="e1",
        source_id="c1",
        target_id="c2",
        kind=DependencyKind.SUPPORT,
        active_at=("t0",),
        recoverable=Truth.YES,
        operationally_relevant=Truth.YES,
        equivalence_stable=Truth.YES,
        machinery_charged=Truth.YES,
    )
    data.update(updates)
    return DependencyEdge(**data)


def assessment(**updates):
    data = dict(
        target_class_member=Truth.YES,
        representation_admissible=Truth.YES,
        machinery_closed=Truth.YES,
        fully_faithful=Truth.YES,
        equivalence_preserved=Truth.YES,
        dependency_queries_total=Truth.YES,
        failure_unknown_separated=Truth.YES,
        nodes=("c1", "c2"),
        edges=(edge(),),
    )
    data.update(updates)
    return DependencyAssessment(**data)


class DependencyStructureTests(unittest.TestCase):
    def test_valid_support_graph_proves_witness(self):
        a = assessment()
        self.assertEqual(MODULE.assess_dependency_structure(a), Verdict.PROVED)
        self.assertTrue(MODULE.theorem_witness_exists(a))

    def test_false_premise_refutes(self):
        self.assertEqual(MODULE.assess_dependency_structure(assessment(fully_faithful=Truth.NO)), Verdict.REFUTED)

    def test_unknown_premise_remains_unknown(self):
        self.assertEqual(MODULE.assess_dependency_structure(assessment(machinery_closed=Truth.UNKNOWN)), Verdict.UNKNOWN)

    def test_empty_edges_are_unknown_not_proved(self):
        self.assertEqual(MODULE.assess_dependency_structure(assessment(edges=())), Verdict.UNKNOWN)

    def test_unknown_endpoint_refutes(self):
        self.assertEqual(MODULE.assess_dependency_structure(assessment(edges=(edge(target_id="missing"),))), Verdict.REFUTED)

    def test_missing_temporal_scope_refutes(self):
        self.assertEqual(MODULE.assess_dependency_structure(assessment(edges=(edge(active_at=()),))), Verdict.REFUTED)

    def test_hidden_machinery_refutes(self):
        self.assertEqual(MODULE.assess_dependency_structure(assessment(edges=(edge(machinery_charged=Truth.NO),))), Verdict.REFUTED)

    def test_unknown_recoverability_is_unknown(self):
        self.assertEqual(MODULE.assess_dependency_structure(assessment(edges=(edge(recoverable=Truth.UNKNOWN),))), Verdict.UNKNOWN)

    def test_nonoperational_correlation_refutes(self):
        self.assertEqual(MODULE.assess_dependency_structure(assessment(edges=(edge(operationally_relevant=Truth.NO),))), Verdict.REFUTED)

    def test_representation_dependent_kind_refutes(self):
        self.assertEqual(MODULE.assess_dependency_structure(assessment(edges=(edge(equivalence_stable=Truth.NO),))), Verdict.REFUTED)

    def test_provenance_only_graph_is_insufficient(self):
        self.assertEqual(MODULE.assess_dependency_structure(assessment(edges=(edge(kind=DependencyKind.PROVENANCE),))), Verdict.REFUTED)

    def test_duplicate_node_identity_refutes(self):
        self.assertEqual(MODULE.assess_dependency_structure(assessment(nodes=("c1", "c1", "c2"))), Verdict.REFUTED)

    def test_duplicate_edge_identity_refutes(self):
        second = edge(source_id="c2", target_id="c1")
        self.assertEqual(MODULE.assess_dependency_structure(assessment(edges=(edge(), second))), Verdict.REFUTED)

    def test_conflicting_duplicate_relation_raises(self):
        with self.assertRaises(ValueError):
            MODULE.construct_dependency_relation((edge(edge_id="a"), edge(edge_id="b")))


if __name__ == "__main__":
    unittest.main()
