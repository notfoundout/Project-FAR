# Purpose

This document describes the Prompt 4 executable reasoning graph construction and dependency validation engine for Project FAR mechanization.

# Graph Model

The graph engine operates on canonical IR documents. Nodes represent investigations, representations, structures, interpretations, claims, assumptions, evidence, operations, reasoning steps, dependencies, and proofs. Edges represent scoped, dependency, support, contradiction, interpretation, transformation, derivation, citation, and record relationships.

# Graph Construction

`build_graph` deterministically constructs graph nodes from IR objects and graph edges from explicit IR references, dependencies, proof records, reasoning steps, operations, evidence citations, interpretations, structures, and investigation scope.

# Reference Resolution

`resolve_references` resolves typed references against canonical IR objects and optional graph nodes or graph edges. Missing references, duplicate identifiers, and expected-kind mismatches return diagnostics.

# Dependency Validation

`validate_dependencies` checks dependency records and graph dependency edges for unknown dependency types, duplicate dependency records, self dependencies, missing references, invalid endpoints, invalid directions, and cycles.

# Cycle Detection

`detect_cycles` performs deterministic cycle detection on `depends_on` edges and returns all detected cycles in stable order. It does not stop after the first cycle.

# Reachability

`compute_reachability` computes investigation roots, reachable nodes, unreachable nodes, and isolated connected components. `dependency_closure` computes deterministic dependency closure over `depends_on` edges.

# Graph Statistics

`graph_statistics` reports node count, edge count, dependency count, root count, orphan count, cycle count, reachable count, unreachable count, component count, and diagnostic count.

# Diagnostics

Graph diagnostics reuse the existing diagnostic model. Prompt 4 adds stable graph diagnostic codes for missing references, duplicate references, dependency cycles, broken dependencies, orphan nodes, invalid edges, invalid nodes, graph disconnection, unreachable nodes, invalid dependency directions, invalid roots, duplicate graph nodes, duplicate graph edges, unknown dependency types, and dependency kind mismatches.

# Complexity

Graph construction is linear in the number of IR objects plus emitted edges. Reachability is linear in nodes plus edges. Cycle detection is deterministic depth-first traversal over dependency edges and is suitable for the Phase 3 MVP graph sizes covered by tests.

# Deferred Features

Proof verification, CLI commands, REST API, storage, arbitrary operation execution, and mathematical proof checking remain deferred.
