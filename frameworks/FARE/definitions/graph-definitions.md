# Graph Definitions

## Purpose

This document defines the graph-theoretic terminology used throughout the Formal Architecture of Reasoning Evaluation.

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

- Dependency
- Support
- Conflict
- Refinement

Additional edge types may be introduced through future investigations.

---

# Definition 5 — Path

A **path** is an ordered sequence of edges connecting one node to another.

A path preserves edge direction.

---

# Definition 6 — Reachability

A node is **reachable** from another node if a directed path exists between them.

---

# Definition 7 — Cycle

A **cycle** is a directed path beginning and ending at the same node.

---

# Definition 8 — Subgraph

A **subgraph** is a graph whose nodes and edges are subsets of another assessment graph.

---

# Definition 9 — Connected Component

A **connected component** is a maximal connected subgraph under a specified notion of connectivity.

Whenever the term **component** is used within FARE, the applicable notion of connectivity shall be explicitly stated.

Examples include:

- weakly connected component;
- strongly connected component.

---

# Definition 10 — Dependency Component

A **dependency component** is a connected component induced exclusively by dependency edges.

The applicable notion of connectivity shall be explicitly specified whenever dependency components are discussed.

---

# Definition 11 — Graph Traversal

A **graph traversal** is a procedure for systematically visiting nodes and edges within an assessment graph.

Traversal order depends upon the chosen traversal method.

---

# Definition 12 — Graph Transformation

A **graph transformation** is an operation that modifies the structure of an assessment graph by adding, removing, or replacing nodes or edges.

---

# Definition 13 — Graph Composition

A **graph composition** combines two or more assessment graphs into a single assessment graph according to explicitly defined composition rules.

---

# Definition 14 — Graph Decomposition

A **graph decomposition** partitions an assessment graph into smaller subgraphs according to explicitly defined decomposition rules.

---

# Definition 15 — Graph Reconstruction

A **graph reconstruction** is the process of reconstructing the structural organization of an assessment system from its assessment graph.

Graph reconstruction concerns structural representation only.

It does not reconstruct semantic interpretation.

---

# Notes

These definitions establish the canonical graph-theoretic vocabulary used throughout FARE.

All graph investigations and graph proofs shall reference these definitions unless explicitly stated otherwise.