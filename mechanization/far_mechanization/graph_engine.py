"""Reasoning graph construction, reference resolution, and dependency validation."""
from __future__ import annotations
from dataclasses import dataclass
from collections import defaultdict, deque
from typing import Mapping, Iterable

from .core import IRKind, Identifier, Reference, freeze_metadata
from .diagnostics import Diagnostic, DiagnosticCode, DiagnosticSeverity
from .ir import (
    FARDocument, GraphEdge, GraphEdgeKind, GraphNode, GraphNodeKind,
    ReasoningGraph, Representation, RepresentationalStructure, Interpretation,
    Investigation, Claim, Assumption, Evidence, Operation, ReasoningStep,
    Dependency, Proof,
)

_KIND_TO_NODE = {
    IRKind.REPRESENTATION: GraphNodeKind.REPRESENTATION,
    IRKind.STRUCTURE: GraphNodeKind.STRUCTURE,
    IRKind.INTERPRETATION: GraphNodeKind.INTERPRETATION,
    IRKind.INVESTIGATION: GraphNodeKind.INVESTIGATION,
    IRKind.CLAIM: GraphNodeKind.CLAIM,
    IRKind.ASSUMPTION: GraphNodeKind.ASSUMPTION,
    IRKind.EVIDENCE: GraphNodeKind.EVIDENCE,
    IRKind.OPERATION: GraphNodeKind.OPERATION,
    IRKind.REASONING_STEP: GraphNodeKind.REASONING_STEP,
    IRKind.DEPENDENCY: GraphNodeKind.DEPENDENCY,
    IRKind.PROOF: GraphNodeKind.PROOF,
}
_NODE_TO_IR = {v: k for k, v in _KIND_TO_NODE.items()}
_ALLOWED_DEPENDENCY_RELATIONS = {"depends_on", "supports", "contradicts", "interprets", "scopes", "transforms", "derives", "cites", "records"}

@dataclass(frozen=True, slots=True)
class ResolvedReference:
    source_identifier: str
    reference: Reference
    target: object | GraphNode | GraphEdge | None

@dataclass(frozen=True, slots=True)
class ReferenceResolutionResult:
    resolved: tuple[ResolvedReference, ...]
    diagnostics: tuple[Diagnostic, ...]
    @property
    def success(self) -> bool: return not self.diagnostics

@dataclass(frozen=True, slots=True)
class GraphBuildResult:
    graph: ReasoningGraph | None
    diagnostics: tuple[Diagnostic, ...]
    @property
    def success(self) -> bool: return self.graph is not None and not self.diagnostics

@dataclass(frozen=True, slots=True)
class ReachabilityResult:
    roots: tuple[str, ...]
    reachable: tuple[str, ...]
    unreachable: tuple[str, ...]
    components: tuple[tuple[str, ...], ...]
    diagnostics: tuple[Diagnostic, ...]

@dataclass(frozen=True, slots=True)
class GraphValidationResult:
    diagnostics: tuple[Diagnostic, ...]
    reachability: ReachabilityResult
    cycles: tuple[tuple[str, ...], ...]
    @property
    def success(self) -> bool: return not self.diagnostics

@dataclass(frozen=True, slots=True)
class GraphStatistics:
    node_count: int
    edge_count: int
    dependency_count: int
    root_count: int
    orphan_count: int
    cycle_count: int
    reachable_count: int
    unreachable_count: int
    component_count: int
    diagnostic_count: int

def _diag(code: DiagnosticCode, message: str, ident: str | None = None, details: Mapping[str, object] | None = None) -> Diagnostic:
    return Diagnostic(code, DiagnosticSeverity.ERROR, message, related_identifier=ident, details=details or {})

def _objects(document: FARDocument) -> tuple[object, ...]:
    return (document.investigation, *document.representations, *document.structures, *document.interpretations, *document.claims, *document.assumptions, *document.evidence, *document.operations, *document.reasoning_steps, *document.dependencies, *document.proofs)

def _object_kind(obj: object) -> IRKind:
    return getattr(obj, "kind")

def _index(document: FARDocument) -> tuple[dict[str, object], tuple[Diagnostic, ...]]:
    idx: dict[str, object] = {}
    diagnostics: list[Diagnostic] = []
    for obj in _objects(document):
        key = str(obj.identifier)
        if key in idx:
            diagnostics.append(_diag(DiagnosticCode.DUPLICATE_REFERENCE, f"duplicate identifier: {key}", key))
        else:
            idx[key] = obj
    return idx, tuple(diagnostics)

def _refs_for(obj: object) -> tuple[tuple[str, Reference, GraphEdgeKind], ...]:
    sid = str(obj.identifier)
    if isinstance(obj, RepresentationalStructure):
        return tuple((sid, r, GraphEdgeKind.RECORDS) for r in obj.representations)
    if isinstance(obj, Interpretation):
        return ((sid, obj.representation, GraphEdgeKind.INTERPRETS),)
    if isinstance(obj, Evidence):
        return tuple((sid, r, GraphEdgeKind.CITES) for r in obj.cites)
    if isinstance(obj, Operation):
        return tuple((sid, r, GraphEdgeKind.TRANSFORMS) for r in (*obj.inputs, *obj.outputs))
    if isinstance(obj, ReasoningStep):
        refs = []
        if obj.operation is not None: refs.append((sid, obj.operation, GraphEdgeKind.RECORDS))
        refs += [(sid, r, GraphEdgeKind.DEPENDS_ON) for r in obj.premises]
        refs += [(sid, r, GraphEdgeKind.DERIVES) for r in obj.conclusions]
        return tuple(refs)
    if isinstance(obj, Dependency):
        return ((sid, obj.source_ref, GraphEdgeKind.RECORDS), (sid, obj.target_ref, GraphEdgeKind.RECORDS), (str(obj.source_ref.identifier), obj.target_ref, GraphEdgeKind.DEPENDS_ON))
    if isinstance(obj, Proof):
        return ((sid, obj.claim, GraphEdgeKind.DERIVES), *[(sid, r, GraphEdgeKind.RECORDS) for r in obj.steps], *[(sid, r, GraphEdgeKind.DEPENDS_ON) for r in obj.assumptions], *[(sid, r, GraphEdgeKind.SUPPORTS) for r in obj.evidence])
    return ()

def resolve_references(document: FARDocument, graph: ReasoningGraph | None = None) -> ReferenceResolutionResult:
    idx, diagnostics = _index(document)
    gnodes = {str(n.identifier): n for n in graph.nodes} if graph else {}
    gedges = {str(e.identifier): e for e in graph.edges} if graph else {}
    resolved: list[ResolvedReference] = []
    ds = list(diagnostics)
    for obj in _objects(document):
        for source, ref, _edge_kind in _refs_for(obj):
            key = str(ref.identifier)
            target = idx.get(key) or gnodes.get(key) or gedges.get(key)
            if target is None:
                ds.append(_diag(DiagnosticCode.MISSING_REFERENCE, f"missing reference: {key}", key, {"source": source}))
            elif ref.expected_kind is not None:
                actual = _object_kind(target) if hasattr(target, "kind") else _NODE_TO_IR.get(target.node_kind) if isinstance(target, GraphNode) else None
                if actual is not None and actual != ref.expected_kind:
                    ds.append(_diag(DiagnosticCode.DEPENDENCY_KIND_MISMATCH, f"reference {key} expected {ref.expected_kind.value} but found {actual.value}", key, {"source": source}))
            resolved.append(ResolvedReference(source, ref, target))
    return ReferenceResolutionResult(tuple(sorted(resolved, key=lambda r: (r.source_identifier, str(r.reference.identifier)))), tuple(ds))

def _edge_id(kind: GraphEdgeKind, source: str, target: str) -> Identifier:
    return Identifier(f"edge:{kind.value}:{source}:{target}")

def build_graph(document: FARDocument) -> GraphBuildResult:
    nodes: list[GraphNode] = []
    edges: list[GraphEdge] = []
    idx, ds = _index(document)
    for obj in _objects(document):
        nodes.append(GraphNode(obj.identifier, _KIND_TO_NODE[_object_kind(obj)], obj.source, obj.metadata))
    root = str(document.investigation.identifier)
    for obj in _objects(document):
        oid = str(obj.identifier)
        if oid != root:
            edges.append(GraphEdge(_edge_id(GraphEdgeKind.SCOPES, root, oid), GraphEdgeKind.SCOPES, Reference(Identifier(root), IRKind.INVESTIGATION), Reference(obj.identifier, _object_kind(obj)), obj.source, obj.metadata))
        for source, ref, kind in _refs_for(obj):
            edges.append(GraphEdge(_edge_id(kind, source, str(ref.identifier)), kind, Reference(Identifier(source), _object_kind(idx[source]) if source in idx else None), ref, getattr(obj, "source", None), getattr(obj, "metadata", {})))
    graph = ReasoningGraph(tuple(sorted(nodes, key=lambda n: str(n.identifier))), tuple(sorted(edges, key=lambda e: str(e.identifier))), document.metadata)
    return GraphBuildResult(graph, tuple(ds))

def _node_ids(graph: ReasoningGraph) -> list[str]: return [str(n.identifier) for n in graph.nodes]
def _edge_pairs(graph: ReasoningGraph, kinds: set[GraphEdgeKind] | None = None) -> list[tuple[str, str]]:
    return [(str(e.source.identifier), str(e.target.identifier)) for e in graph.edges if kinds is None or e.edge_kind in kinds]

def detect_cycles(graph: ReasoningGraph) -> tuple[tuple[str, ...], ...]:
    adj: dict[str, list[str]] = defaultdict(list)
    for s, t in _edge_pairs(graph, {GraphEdgeKind.DEPENDS_ON}):
        adj[s].append(t)
    for key in adj:
        adj[key].sort()
    cycles: set[tuple[str, ...]] = set()

    def canon(cycle: list[str]) -> tuple[str, ...]:
        body = cycle[:-1]
        rotations = [tuple(body[i:] + body[:i]) for i in range(len(body))]
        first = min(rotations)
        return first + (first[0],)

    for start in sorted(adj):
        stack: list[tuple[str, int]] = [(start, 0)]
        path: list[str] = [start]
        in_path = {start}
        while stack:
            node, index = stack[-1]
            neighbors = adj.get(node, [])
            if index >= len(neighbors):
                stack.pop()
                in_path.remove(path.pop())
                continue
            nxt = neighbors[index]
            stack[-1] = (node, index + 1)
            if nxt in in_path:
                cycles.add(canon(path[path.index(nxt):] + [nxt]))
                continue
            path.append(nxt)
            in_path.add(nxt)
            stack.append((nxt, 0))
    return tuple(sorted(cycles))

def compute_reachability(graph: ReasoningGraph) -> ReachabilityResult:
    nodes = set(_node_ids(graph))
    roots = tuple(sorted(str(n.identifier) for n in graph.nodes if n.node_kind == GraphNodeKind.INVESTIGATION))
    adj: dict[str, set[str]] = {n: set() for n in nodes}
    undirected: dict[str, set[str]] = {n: set() for n in nodes}
    for s, t in _edge_pairs(graph):
        if s in nodes and t in nodes:
            adj[s].add(t); undirected[s].add(t); undirected[t].add(s)
    reachable: set[str] = set()
    q=deque(roots)
    while q:
        cur=q.popleft()
        if cur in reachable: continue
        reachable.add(cur); q.extend(sorted(adj.get(cur,set())-reachable))
    unseen=set(nodes); comps=[]
    while unseen:
        start=sorted(unseen)[0]; comp=set(); q=deque([start])
        while q:
            cur=q.popleft()
            if cur in comp: continue
            comp.add(cur); q.extend(sorted(undirected.get(cur,set())-comp))
        comps.append(tuple(sorted(comp))); unseen-=comp
    unreachable = tuple(sorted(nodes - reachable))
    ds = tuple(_diag(DiagnosticCode.UNREACHABLE_NODE, f"unreachable node: {n}", n) for n in unreachable)
    return ReachabilityResult(roots, tuple(sorted(reachable)), unreachable, tuple(comps), ds)

def dependency_closure(graph: ReasoningGraph, roots: Iterable[str]) -> tuple[str, ...]:
    adj: dict[str, set[str]] = defaultdict(set)
    for s, t in _edge_pairs(graph, {GraphEdgeKind.DEPENDS_ON}): adj[s].add(t)
    seen=set(); q=deque(sorted(roots))
    while q:
        cur=q.popleft()
        if cur in seen: continue
        seen.add(cur); q.extend(sorted(adj.get(cur,set())-seen))
    return tuple(sorted(seen))

def validate_graph(graph: ReasoningGraph, document: FARDocument | None = None) -> GraphValidationResult:
    ds: list[Diagnostic] = list(graph.validate())
    node_ids=[]; edge_ids=[]
    node_set=set()
    for n in graph.nodes:
        key=str(n.identifier); node_ids.append(key)
        if key in node_set: ds.append(_diag(DiagnosticCode.DUPLICATE_GRAPH_NODE, f"duplicate graph node: {key}", key))
        node_set.add(key)
        if n.node_kind not in set(GraphNodeKind): ds.append(_diag(DiagnosticCode.INVALID_NODE, f"invalid node kind for {key}", key))
    edge_set=set(); incident=set()
    for e in graph.edges:
        eid=str(e.identifier); edge_ids.append(eid)
        if eid in edge_set: ds.append(_diag(DiagnosticCode.DUPLICATE_GRAPH_EDGE, f"duplicate graph edge: {eid}", eid))
        edge_set.add(eid)
        s=str(e.source.identifier); t=str(e.target.identifier)
        if s not in node_set or t not in node_set:
            ds.append(_diag(DiagnosticCode.INVALID_EDGE, f"edge endpoint missing: {eid}", eid, {"source": s, "target": t}))
        else:
            incident.update({s,t})
        if e.edge_kind not in set(GraphEdgeKind): ds.append(_diag(DiagnosticCode.INVALID_EDGE, f"unsupported edge kind: {eid}", eid))
        if e.edge_kind == GraphEdgeKind.DEPENDS_ON and s == t:
            ds.append(_diag(DiagnosticCode.INVALID_DEPENDENCY_DIRECTION, f"self dependency: {s}", s))
    for n in sorted(node_set - incident): ds.append(_diag(DiagnosticCode.ORPHAN_NODE, f"orphan node: {n}", n))
    cycles = detect_cycles(graph)
    for c in cycles: ds.append(_diag(DiagnosticCode.DEPENDENCY_CYCLE, "dependency cycle: " + " -> ".join(c), c[0], {"cycle": c}))
    reach = compute_reachability(graph)
    ds.extend(reach.diagnostics)
    if not reach.roots: ds.append(_diag(DiagnosticCode.INVALID_ROOT, "graph has no investigation root"))
    if len(reach.roots) > 1: ds.append(_diag(DiagnosticCode.INVALID_ROOT, "graph has multiple investigation roots", details={"roots": reach.roots}))
    if reach.unreachable: ds.append(_diag(DiagnosticCode.GRAPH_DISCONNECTED, "graph has nodes unreachable from investigation", details={"unreachable": reach.unreachable}))
    return GraphValidationResult(tuple(ds), reach, cycles)

def validate_dependencies(document: FARDocument, graph: ReasoningGraph | None = None) -> tuple[Diagnostic, ...]:
    graph = graph or build_graph(document).graph
    ds: list[Diagnostic] = []
    seen: set[tuple[str, str, str]] = set()
    for dep in document.dependencies:
        rel = dep.relation
        s=str(dep.source_ref.identifier); t=str(dep.target_ref.identifier)
        if rel not in _ALLOWED_DEPENDENCY_RELATIONS:
            ds.append(_diag(DiagnosticCode.UNKNOWN_DEPENDENCY_TYPE, f"unknown dependency type: {rel}", str(dep.identifier)))
        if s == t:
            ds.append(_diag(DiagnosticCode.INVALID_DEPENDENCY_DIRECTION, f"self dependency: {s}", str(dep.identifier)))
        key=(s,t,rel)
        if key in seen: ds.append(_diag(DiagnosticCode.BROKEN_DEPENDENCY, f"duplicate dependency: {s} {rel} {t}", str(dep.identifier)))
        seen.add(key)
    ds.extend(resolve_references(document, graph).diagnostics)
    if graph is not None:
        ds.extend(d for d in validate_graph(graph, document).diagnostics if d.code in {DiagnosticCode.DEPENDENCY_CYCLE, DiagnosticCode.INVALID_DEPENDENCY_DIRECTION, DiagnosticCode.INVALID_EDGE})
    return tuple(ds)

def graph_statistics(graph: ReasoningGraph, diagnostics: tuple[Diagnostic, ...] = ()) -> GraphStatistics:
    reach=compute_reachability(graph); cycles=detect_cycles(graph)
    orphan_count=len([n for n in _node_ids(graph) if all(n not in pair for pair in _edge_pairs(graph))])
    return GraphStatistics(len(graph.nodes), len(graph.edges), len([e for e in graph.edges if e.edge_kind == GraphEdgeKind.DEPENDS_ON]), len(reach.roots), orphan_count, len(cycles), len(reach.reachable), len(reach.unreachable), len(reach.components), len(diagnostics))
