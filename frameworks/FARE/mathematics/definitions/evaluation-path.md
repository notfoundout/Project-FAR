# Mathematical Definition

## Identifier

MDEF-003

---

# Title

Evaluation Path

---

# Purpose

This document defines evaluation paths within an evaluation space.

Evaluation paths represent finite sequences of admissible evaluation transformations connecting one evaluation to another.

They provide the fundamental notion of connectivity within evaluation spaces.

---

# Motivation

Individual transformations describe single changes.

Many reasoning processes require multiple successive transformations.

Evaluation paths formalize these transformation sequences.

---

# Dependencies

- MDEF-001 — Evaluation Space
- MDEF-002 — Evaluation Transformation

---

# Definition

An **evaluation path** is a finite ordered sequence of admissible evaluation transformations `P = (tau_1, tau_2, ..., tau_n)` such that `tau_i: E_i -> E_{i+1}` for every `i = 1, ..., n`.

The codomain of each transformation shall equal the domain of the next transformation.

---

# Initial Evaluation

The initial evaluation of a path is the domain of its first transformation.

---

# Terminal Evaluation

The terminal evaluation of a path is the codomain of its final transformation.

---

# Length

The **length** of an evaluation path is the number of transformations it contains.

Formally, `ell(P) = n`.

---

# Empty Path

Every evaluation possesses an empty path of length zero.

The empty path consists solely of the identity transformation.

---

# Closed Path

A path is **closed** if its initial and terminal evaluations are identical.

---

# Simple Path

A path is **simple** if no evaluation appears more than once, except that the initial and terminal evaluations may coincide for a closed path.

---

# Path Composition

If

- path `P_1` terminates at evaluation `E`, and
- path `P_2` begins at evaluation `E`,

then their concatenation `P_2 circ P_1` is an evaluation path.

---

# Reachability

Evaluation `E_2` is **reachable** from `E_1` if an evaluation path exists from `E_1` to `E_2`.

---

# Connectivity

Two evaluations are **connected** if an evaluation path exists between them.

Whether connectivity is directed or undirected depends upon the class of transformations under consideration.

---

# Structural Properties

This definition does not assume:

- shortest paths;
- uniqueness;
- optimality;
- invertibility;
- distance.

These concepts require additional mathematical definitions.

---

# Relationship to Evaluation Space

Evaluation paths describe finite navigation through an evaluation space.

They form the basis for:

- reachability;
- connectedness;
- distance;
- geodesics;
- neighborhoods;
- convergence.

---

# Notes

Evaluation paths are purely structural objects.

They describe permissible transformation sequences without assigning any notion of cost, efficiency, or optimality.

Such concepts are introduced separately through later mathematical definitions.
