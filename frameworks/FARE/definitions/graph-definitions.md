# Graph Definitions

## Purpose

This document defines the canonical graph-theoretic terminology used throughout the Formal Architecture of Reasoning Evaluation.

Unless explicitly stated otherwise, every graph-theoretic term appearing elsewhere in FARE refers to the definitions given here.

---

# Definition 1 — Assessment Graph

An **assessment graph** is a directed, typed graph whose nodes represent assessments and whose edges represent formally defined relationships between assessments.

The assessment graph provides the canonical structural representation of an assessment system.

---

# Definition 2 — Node

A **node** is the graph representation of exactly one assessment.

Every assessment corresponds to one node.

---

# Definition 3 — Edge

An **edge** is a directed connection between two nodes representing a formally defined assessment relationship.

Every edge possesses exactly one relationship type.

---

# Definition 4 — Edge Type

An **edge type** identifies the semantic relationship represented by an edge.

Current edge types include:

- Dependency;
- Support;
- Conflict;
- Refinement.

Additional edge types may be introduced through future investigations.

---

# Definition 5 — Directed Path

A **directed path** is an ordered sequence of edges connecting one node to another while preserving edge direction.

A directed path may contain one or more edges.

---

# Definition 6 — Undirected Path

An **undirected path** is an ordered sequence of edges connecting one node to another while ignoring edge direction.

An undirected path may contain one or more edges.

Undirected paths are used only when a definition or theorem explicitly ignores edge direction.

---

# Definition 7 — Reachability

A node is **reachable** from another node if a directed path exists from the first node to the second node.

Reachability always preserves edge direction unless explicitly stated otherwise.

---

# Definition 8 — Cycle

A **cycle** is a directed path beginning and ending at the same node.

Cycle existence is structural.

Cycle admissibility is semantic.

---

# Definition 9 — Subgraph

A **subgraph** is a graph whose nodes and edges are subsets of another assessment graph.

A subgraph preserves the node and edge types inherited from the original graph.

---

# Definition 10 — Weak Connectivity

Two nodes are **weakly connected** if an undirected path exists between them.

Weak connectivity concerns structural connectedness without directional dependency.

---

# Definition 11 — Strong Connectivity

Two nodes are **strongly connected** if each node is reachable from the other by directed paths.

Strong connectivity requires mutual directed reachability.

---

# Definition 12 — Weakly Connected Component

A **weakly connected component** is a maximal subgraph in which every pair of nodes is weakly connected.

---

# Definition 13 — Strongly Connected Component

A **strongly connected component** is a maximal subgraph in which every pair of nodes is strongly connected.

---

# Definition 14 — Dependency Subgraph

A **dependency subgraph** is the subgraph induced exclusively by dependency edges and the nodes incident to those edges.

Assessments with no incident dependency edge are not part of the dependency subgraph unless a theorem explicitly defines an isolated dependency-node convention.

---

# Definition 15 — Dependency Component

A **dependency component** is a connected component of a dependency subgraph under an explicitly specified notion of connectivity.

If the connectivity type is not specified, the term **dependency component** shall not be used in a theorem.

Permitted forms include:

- weak dependency component;
- strong dependency component.

---

# Definition 16 — Weak Dependency Component

A **weak dependency component** is a weakly connected component of a dependency subgraph.

---

# Definition 17 — Strong Dependency Component

A **strong dependency component** is a strongly connected component of a dependency subgraph.

---

# Definition 18 — Conflict Subgraph

A **conflict subgraph** is the subgraph induced by conflict edges and the nodes incident to those edges.

Because conflict is symmetric, conflict subgraphs may be analyzed using undirected connectivity when only incompatibility is under consideration.

---

# Definition 19 — Graph Traversal

A **graph traversal** is a procedure for systematically visiting nodes and edges within an assessment graph.

Traversal order depends upon the chosen traversal method.

---

# Definition 20 — Graph Transformation

A **graph transformation** is an operation that modifies the structure of an assessment graph by adding, removing, or replacing nodes or edges.

---

# Definition 21 — Graph Composition

A **graph composition** combines two or more assessment graphs into a single assessment graph according to explicitly defined composition rules.

---

# Definition 22 — Graph Decomposition

A **graph decomposition** partitions an assessment graph into smaller subgraphs according to explicitly defined decomposition rules.

---

# Definition 23 — Graph Reconstruction

A **graph reconstruction** is the process of reconstructing the structural organization of an assessment system from its assessment graph.

Graph reconstruction concerns structural representation only.

It does not reconstruct semantic interpretation.

---

# Notes

These definitions establish the canonical graph-theoretic vocabulary used throughout FARE.

All graph investigations and graph proofs shall reference these definitions unless explicitly stated otherwise.
