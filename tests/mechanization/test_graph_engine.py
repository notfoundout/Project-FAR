from pathlib import Path
import unittest

from mechanization.far_mechanization import (
    Claim, DiagnosticCode, FARDocument, GraphEdge, GraphEdgeKind, GraphNode,
    GraphNodeKind, Identifier, Investigation, ReasoningGraph, Reference,
    build_graph, compute_reachability, dependency_closure, detect_cycles,
    graph_statistics, resolve_references, validate_dependencies, validate_graph,
)
from mechanization.far_mechanization.parser import parse_json_file

ROOT = Path(__file__).resolve().parents[2]
GRAPH_VALID = ROOT / "tests" / "fixtures" / "mechanization" / "graph" / "valid"
GRAPH_INVALID = ROOT / "tests" / "fixtures" / "mechanization" / "graph" / "invalid"

class GraphEngineTests(unittest.TestCase):
    def parse(self, path):
        result = parse_json_file(path)
        self.assertTrue(result.success, result.diagnostics)
        return result.document

    def test_graph_construction_and_stable_ordering(self):
        doc = self.parse(GRAPH_VALID / "valid-graph.json")
        result = build_graph(doc)
        self.assertTrue(result.success, result.diagnostics)
        ids = [str(n.identifier) for n in result.graph.nodes]
        self.assertEqual(ids, sorted(ids))
        self.assertIn("INV-g", ids)
        self.assertTrue(any(e.edge_kind == GraphEdgeKind.SCOPES for e in result.graph.edges))

    def test_reference_resolution_and_missing_reference_diagnostic(self):
        doc = self.parse(GRAPH_VALID / "valid-graph.json")
        graph = build_graph(doc).graph
        self.assertTrue(resolve_references(doc, graph).success)
        broken = self.parse(GRAPH_INVALID / "broken-reference.json")
        diagnostics = resolve_references(broken, build_graph(broken).graph).diagnostics
        self.assertTrue(any(d.code == DiagnosticCode.MISSING_REFERENCE for d in diagnostics))

    def test_dependency_validation_unknown_self_and_kind_mismatch(self):
        unknown = self.parse(GRAPH_INVALID / "unknown-dependency.json")
        diagnostics = validate_dependencies(unknown)
        self.assertTrue(any(d.code == DiagnosticCode.UNKNOWN_DEPENDENCY_TYPE for d in diagnostics))
        doc = FARDocument(
            Identifier("DOC-self"), Investigation(Identifier("INV"), question="q"),
            claims=(Claim(Identifier("C"), statement="c"),),
        )
        graph = ReasoningGraph((GraphNode(Identifier("C"), GraphNodeKind.CLAIM),), (GraphEdge(Identifier("E"), GraphEdgeKind.DEPENDS_ON, Reference(Identifier("C")), Reference(Identifier("C"))),))
        self.assertTrue(any(d.code == DiagnosticCode.INVALID_DEPENDENCY_DIRECTION for d in validate_graph(graph, doc).diagnostics))

    def test_cycle_detection_multiple_cycles(self):
        graph = ReasoningGraph(
            nodes=tuple(GraphNode(Identifier(x), GraphNodeKind.CLAIM) for x in ["A","B","C","D"]),
            edges=(
                GraphEdge(Identifier("E1"), GraphEdgeKind.DEPENDS_ON, Reference(Identifier("A")), Reference(Identifier("B"))),
                GraphEdge(Identifier("E2"), GraphEdgeKind.DEPENDS_ON, Reference(Identifier("B")), Reference(Identifier("A"))),
                GraphEdge(Identifier("E3"), GraphEdgeKind.DEPENDS_ON, Reference(Identifier("C")), Reference(Identifier("D"))),
                GraphEdge(Identifier("E4"), GraphEdgeKind.DEPENDS_ON, Reference(Identifier("D")), Reference(Identifier("C"))),
            ),
        )
        cycles = detect_cycles(graph)
        self.assertEqual(len(cycles), 2)
        diagnostics = validate_graph(graph).diagnostics
        self.assertGreaterEqual(sum(1 for d in diagnostics if d.code == DiagnosticCode.DEPENDENCY_CYCLE), 2)

    def test_reachability_closure_statistics_and_orphans(self):
        doc = self.parse(GRAPH_VALID / "dependency-chain.json")
        graph = build_graph(doc).graph
        reach = compute_reachability(graph)
        self.assertIn("INV-g", reach.roots)
        self.assertEqual(reach.unreachable, ())
        closure = dependency_closure(graph, ["C3"])
        self.assertEqual(closure, ("A1", "C1", "C2", "C3"))
        stats = graph_statistics(graph)
        self.assertEqual(stats.node_count, len(graph.nodes))
        self.assertGreater(stats.dependency_count, 0)
        orphan_graph = ReasoningGraph((GraphNode(Identifier("INV"), GraphNodeKind.INVESTIGATION), GraphNode(Identifier("C"), GraphNodeKind.CLAIM)), ())
        self.assertTrue(any(d.code == DiagnosticCode.ORPHAN_NODE for d in validate_graph(orphan_graph).diagnostics))

    def test_duplicate_graph_node_edge_and_invalid_edge_endpoint(self):
        graph = ReasoningGraph(
            nodes=(GraphNode(Identifier("INV"), GraphNodeKind.INVESTIGATION), GraphNode(Identifier("INV"), GraphNodeKind.INVESTIGATION)),
            edges=(GraphEdge(Identifier("E"), GraphEdgeKind.SUPPORTS, Reference(Identifier("INV")), Reference(Identifier("MISSING"))), GraphEdge(Identifier("E"), GraphEdgeKind.SUPPORTS, Reference(Identifier("INV")), Reference(Identifier("INV")))),
        )
        diagnostics = validate_graph(graph).diagnostics
        codes = {d.code for d in diagnostics}
        self.assertIn(DiagnosticCode.DUPLICATE_GRAPH_NODE, codes)
        self.assertIn(DiagnosticCode.DUPLICATE_GRAPH_EDGE, codes)
        self.assertIn(DiagnosticCode.INVALID_EDGE, codes)

    def test_large_graph_determinism(self):
        claims = tuple(Claim(Identifier(f"C{i:03d}"), statement="c") for i in range(80))
        doc = FARDocument(Identifier("DOC-large"), Investigation(Identifier("INV-large"), question="q"), claims=claims)
        g1 = build_graph(doc).graph
        g2 = build_graph(doc).graph
        self.assertEqual(g1, g2)
        self.assertEqual(len(g1.nodes), 81)

if __name__ == "__main__":
    unittest.main()
