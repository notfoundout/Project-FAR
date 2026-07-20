from __future__ import annotations
from collections import defaultdict, deque
from typing import Any
from s_core_w3_schema import REQUIRED_A_FIELDS, REQUIRED_W_FIELDS, W3Error

def machinery_ledger() -> dict[str, Any]:
    nodes = [
        {"id": "schema:FARA-WITNESS-1.0", "kind": "schema", "version": "1.0"},
        {"id": "schema:DIR-INCIDENCE-1.0", "kind": "schema", "version": "1.0"},
        {"id": "schema:DYN-HISTORY-1.0", "kind": "schema", "version": "1.0"},
        {"id": "algorithm:validate-source", "kind": "algorithm", "version": "1.0"},
        {"id": "algorithm:allocate", "kind": "algorithm", "version": "1.0"},
        {"id": "algorithm:direct-axes", "kind": "algorithm", "version": "1.0"},
        {"id": "algorithm:dynamics-history", "kind": "algorithm", "version": "1.0"},
        {"id": "algorithm:semantics", "kind": "algorithm", "version": "1.0"},
        {"id": "algorithm:decomposition", "kind": "algorithm", "version": "1.0"},
        {"id": "algorithm:recover-target", "kind": "algorithm", "version": "1.0"},
        {"id": "algorithm:verify-witness", "kind": "algorithm", "version": "1.0"},
        {"id": "algorithm:component-view", "kind": "algorithm", "version": "1.0"},
        {"id": "data:value-equivalence", "kind": "semantic_bridge", "version": "source-owned"},
        {"id": "data:interpretation", "kind": "semantic_bridge", "version": "source-owned"},
    ]
    edges = [
        ["algorithm:validate-source", "schema:FARA-WITNESS-1.0"],
        ["algorithm:allocate", "algorithm:validate-source"],
        ["algorithm:direct-axes", "algorithm:allocate"],
        ["algorithm:direct-axes", "schema:DIR-INCIDENCE-1.0"],
        ["algorithm:dynamics-history", "algorithm:allocate"],
        ["algorithm:dynamics-history", "schema:DYN-HISTORY-1.0"],
        ["algorithm:semantics", "algorithm:allocate"],
        ["algorithm:semantics", "data:interpretation"],
        ["algorithm:semantics", "data:value-equivalence"],
        ["algorithm:decomposition", "algorithm:allocate"],
        ["algorithm:recover-target", "schema:FARA-WITNESS-1.0"],
        ["algorithm:verify-witness", "algorithm:recover-target"],
        ["algorithm:verify-witness", "algorithm:semantics"],
        ["algorithm:verify-witness", "algorithm:decomposition"],
        ["algorithm:component-view", "algorithm:recover-target"],
        ["algorithm:component-view", "algorithm:decomposition"],
    ]
    field_producers = {
        "A.U": "algorithm:allocate", "A.Pi": "algorithm:allocate", "A.R": "algorithm:direct-axes",
        "A.Rep": "algorithm:allocate", "A.S": "algorithm:allocate", "A.I": "algorithm:semantics",
        "A.Inv": "schema:FARA-WITNESS-1.0", "A.C": "algorithm:dynamics-history",
        "A.Sigma": "algorithm:dynamics-history", "A.Theta": "algorithm:dynamics-history",
        "A.H": "algorithm:dynamics-history", "A.Omega": "algorithm:dynamics-history",
        "A.Res": "algorithm:decomposition", "A.Prov": "algorithm:dynamics-history",
        "W.E": "algorithm:allocate", "W.D": "algorithm:recover-target", "W.M": "algorithm:allocate",
        "W.iota": "algorithm:semantics", "W.kappa": "schema:FARA-WITNESS-1.0",
    }
    return {
        "schema": "MACHINERY-LEDGER-1.0",
        "nodes": nodes,
        "edges": edges,
        "field_producers": field_producers,
        "external_dependencies": [],
        "normalization_rules": ["canonical_json_sort", "finite_exact_fraction"],
        "equivalence_rules": ["source_owned_value_equivalence", "target_isomorphism"],
        "composition_rules": ["induced_component_interface_substructure"],
        "forbidden": {"source_oracle": False, "case_database": False, "network": False, "evaluator_repair": False, "undeclared_executable": False},
    }


def validate_kappa(kappa: dict[str, Any]) -> None:
    if kappa.get("schema") != "MACHINERY-LEDGER-1.0":
        raise W3Error("wrong machinery-ledger schema")
    nodes = {str(item.get("id", "")): item for item in kappa.get("nodes", [])}
    if not nodes or "" in nodes or len(nodes) != len(kappa.get("nodes", [])):
        raise W3Error("machinery nodes must have unique ids")
    outgoing: dict[str, set[str]] = defaultdict(set)
    indegree = {node: 0 for node in nodes}
    for edge in kappa.get("edges", []):
        if not isinstance(edge, list) or len(edge) != 2 or set(map(str, edge)) - set(nodes):
            raise W3Error("machinery edge references unknown node")
        left, right = map(str, edge)
        if right not in outgoing[left]:
            outgoing[left].add(right); indegree[right] += 1
    queue = deque(sorted(node for node, degree in indegree.items() if degree == 0))
    seen = 0
    while queue:
        node = queue.popleft(); seen += 1
        for child in outgoing[node]:
            indegree[child] -= 1
            if indegree[child] == 0:
                queue.append(child)
    if seen != len(nodes):
        raise W3Error("machinery dependency graph must be acyclic")
    required_fields = {f"A.{x}" for x in REQUIRED_A_FIELDS} | {f"W.{x}" for x in REQUIRED_W_FIELDS}
    producers = kappa.get("field_producers", {})
    if set(producers) != required_fields:
        raise W3Error("machinery field producers are incomplete")
    if set(producers.values()) - set(nodes):
        raise W3Error("machinery field producer references unknown node")
    if kappa.get("external_dependencies") != []:
        raise W3Error("external dependencies are not allowed in W3 recovery")
    forbidden = kappa.get("forbidden", {})
    if any(forbidden.get(key) is not False for key in ("source_oracle", "case_database", "network", "evaluator_repair", "undeclared_executable")):
        raise W3Error("forbidden machinery flag changed")
