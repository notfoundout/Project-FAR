import dataclasses
import unittest

from mechanization.far_mechanization import (
    Assumption, Claim, Dependency, DiagnosticCode, DiagnosticSeverity, Evidence,
    FARDocument, GraphEdge, GraphEdgeKind, GraphNode, GraphNodeKind, Identifier,
    Interpretation, Investigation, IRKind, Operation, Proof, ReasoningGraph,
    ReasoningStep, Reference, Representation, RepresentationalStructure,
    SourceLocation,
)


class CanonicalIRTests(unittest.TestCase):
    def ident(self, value="ID-1"):
        return Identifier(value)

    def test_valid_identifier_construction(self):
        self.assertEqual(Identifier("Claim:001").validate(), ())
        self.assertNotEqual(Identifier("Claim").value, Identifier("claim").value)

    def test_invalid_identifier_rejection_through_diagnostics(self):
        diagnostics = Identifier("bad id").validate()
        self.assertEqual(diagnostics[0].code, DiagnosticCode.INVALID_IDENTIFIER)
        self.assertEqual(diagnostics[0].severity, DiagnosticSeverity.ERROR)
        self.assertIn("must match", diagnostics[0].message)

    def test_source_location_validation(self):
        self.assertEqual(SourceLocation("doc.md", 1, 1, 1, 2).validate(), ())
        diagnostics = SourceLocation("doc.md", 2, 4, 1, 1).validate()
        self.assertEqual(diagnostics[0].code, DiagnosticCode.INVALID_SOURCE_RANGE)

    def test_creation_of_each_core_ir_type(self):
        rep = Representation(Identifier("R1"), content="representation content")
        structure = RepresentationalStructure(Identifier("S1"), representations=(Reference(Identifier("R1"), IRKind.REPRESENTATION),), description="structure")
        interpretation = Interpretation(Identifier("I1"), representation=Reference(Identifier("R1"), IRKind.REPRESENTATION), meaning="meaning")
        investigation = Investigation(Identifier("INV1"), question="question")
        claim = Claim(Identifier("C1"), statement="claim")
        assumption = Assumption(Identifier("A1"), statement="assumption")
        evidence = Evidence(Identifier("E1"), description="evidence")
        operation = Operation(Identifier("O1"), description="operation")
        step = ReasoningStep(Identifier("RS1"), order=1, rationale="rationale")
        dependency = Dependency(Identifier("D1"), source_ref=Reference(Identifier("C1")), target_ref=Reference(Identifier("A1")))
        proof = Proof(Identifier("P1"), claim=Reference(Identifier("C1"), IRKind.CLAIM), steps=(Reference(Identifier("RS1"), IRKind.REASONING_STEP),))
        document = FARDocument(Identifier("DOC1"), investigation, representations=(rep,), structures=(structure,), interpretations=(interpretation,), claims=(claim,), assumptions=(assumption,), evidence=(evidence,), operations=(operation,), reasoning_steps=(step,), dependencies=(dependency,), proofs=(proof,))
        self.assertEqual(document.validate(), ())

    def test_duplicate_identifier_detection_inside_far_document(self):
        inv = Investigation(Identifier("INV1"), question="question")
        document = FARDocument(Identifier("DOC1"), inv, claims=(Claim(Identifier("DUP"), statement="a"),), assumptions=(Assumption(Identifier("DUP"), statement="b"),))
        diagnostics = document.validate()
        self.assertTrue(any(d.code == DiagnosticCode.DUPLICATE_LOCAL_IDENTIFIER for d in diagnostics))

    def test_typed_reference_construction(self):
        ref = Reference(Identifier("C1"), IRKind.CLAIM, SourceLocation("source.md", 1))
        self.assertEqual(ref.expected_kind, IRKind.CLAIM)
        self.assertEqual(ref.validate(), ())

    def test_graph_node_and_edge_construction(self):
        node = GraphNode(Identifier("C1"), GraphNodeKind.CLAIM)
        edge = GraphEdge(Identifier("E1"), GraphEdgeKind.SUPPORTS, Reference(Identifier("A1"), IRKind.ASSUMPTION), Reference(Identifier("C1"), IRKind.CLAIM))
        graph = ReasoningGraph(nodes=(node,), edges=(edge,))
        self.assertEqual(graph.validate(), ())

    def test_stable_diagnostic_codes(self):
        self.assertEqual(DiagnosticCode.INVALID_IDENTIFIER.value, "FAR-IR-001")
        self.assertEqual(DiagnosticCode.DUPLICATE_LOCAL_IDENTIFIER.value, "FAR-IR-003")

    def test_deterministic_equality(self):
        self.assertEqual(Claim(Identifier("C1"), statement="x"), Claim(Identifier("C1"), statement="x"))
        self.assertNotEqual(Claim(Identifier("C1"), statement="x"), Claim(Identifier("c1"), statement="x"))

    def test_immutability_policy(self):
        claim = Claim(Identifier("C1"), statement="x", metadata={"a": 1})
        with self.assertRaises(dataclasses.FrozenInstanceError):
            claim.statement = "changed"
        with self.assertRaises(TypeError):
            claim.metadata["b"] = 2

    def test_no_dependency_on_json_yaml_specific_behavior(self):
        claim = Claim(Identifier("C1"), statement="x", metadata={"native": ("tuple",)})
        self.assertEqual(claim.metadata["native"], ("tuple",))
        self.assertEqual(claim.validate(), ())


if __name__ == "__main__":
    unittest.main()
