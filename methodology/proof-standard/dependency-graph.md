# Canonical Dependency Graph

## Purpose

This document defines the dependency graph governing every accepted artifact within Project FAR.

Every accepted artifact shall appear exactly once within this graph.

No dependency may exist outside this graph.

---

# Dependency Types

Project FAR recognizes the following dependency types.

- Definition
- Investigation
- Construction
- Proof
- Theorem
- Principle
- Primitive

---

# Dependency Rules

A dependency may only point toward previously accepted artifacts.

Forward dependencies are prohibited.

Circular dependencies are prohibited.

---

# Verification Rules

Every accepted artifact shall satisfy:

- Reachability
- Non-circularity
- Explicit dependency listing
- Reconstruction

---

# Canonical Graph

Methodology

↓

Definitions

↓

Investigations

↓

Constructions

↓

Proofs

↓

Accepted Results

↓

Higher Theories

---

# Acceptance Criterion

No artifact becomes canonical until:

- every dependency appears in this graph;
- every dependency is accepted;
- no cycle exists;
- reconstruction succeeds.
