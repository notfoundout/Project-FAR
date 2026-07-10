from __future__ import annotations

from mechanization.far_mechanization.core import IRKind, Identifier, Reference
from mechanization.far_mechanization.graph_engine import build_graph, dependency_closure, detect_cycles, graph_statistics, validate_graph
from mechanization.far_mechanization.ir import Claim, Dependency, FARDocument, Investigation
from mechanization.far_mechanization.normalization import normalize_ir_document
from mechanization.far_mechanization.serialization import serialize_json, serialize_yaml


def _large_document(size: int = 1000) -> FARDocument:
    claims = tuple(Claim(Identifier(f"C{i}"), statement=f"claim {i}") for i in range(size))
    deps = tuple(
        Dependency(
            Identifier(f"D{i}"),
            source_ref=Reference(Identifier(f"C{i}"), IRKind.CLAIM),
            target_ref=Reference(Identifier(f"C{i-1}"), IRKind.CLAIM),
            relation="depends_on",
        )
        for i in range(1, size)
    )
    return FARDocument(Identifier("DOC-large"), Investigation(Identifier("INV-large"), question="Large?"), claims=claims, dependencies=deps)


def test_thousand_node_graph_and_dependency_chain_are_iterative_and_stable():
    document = _large_document(1000)
    graph = build_graph(document).graph
    stats = graph_statistics(graph)
    assert stats.node_count == 2000  # 1 investigation + 1000 claims + 999 dependency records
    assert stats.dependency_count == 999
    assert validate_graph(graph, document).cycles == ()
    closure = dependency_closure(graph, ["C999"])
    assert len([x for x in closure if x.startswith("C")]) == 1000


def test_multiple_independent_cycles_are_reported_without_recursion_failure():
    document = _large_document(10)
    extra = (
        Dependency(Identifier("DX1"), source_ref=Reference(Identifier("C1"), IRKind.CLAIM), target_ref=Reference(Identifier("C2"), IRKind.CLAIM), relation="depends_on"),
        Dependency(Identifier("DX2"), source_ref=Reference(Identifier("C2"), IRKind.CLAIM), target_ref=Reference(Identifier("C1"), IRKind.CLAIM), relation="depends_on"),
        Dependency(Identifier("DX3"), source_ref=Reference(Identifier("C7"), IRKind.CLAIM), target_ref=Reference(Identifier("C8"), IRKind.CLAIM), relation="depends_on"),
        Dependency(Identifier("DX4"), source_ref=Reference(Identifier("C8"), IRKind.CLAIM), target_ref=Reference(Identifier("C7"), IRKind.CLAIM), relation="depends_on"),
    )
    document = FARDocument(document.identifier, document.investigation, claims=document.claims, dependencies=document.dependencies + extra)
    cycles = detect_cycles(build_graph(document).graph)
    assert len(cycles) >= 2


def test_repeated_normalization_and_serialization_are_deterministic():
    document = _large_document(20)
    first = normalize_ir_document(document)
    second = normalize_ir_document(first.document.to_ir()[0])
    assert first.document == second.document
    assert serialize_json(document).text == serialize_json(document).text
    assert serialize_yaml(document).text == serialize_yaml(document).text
