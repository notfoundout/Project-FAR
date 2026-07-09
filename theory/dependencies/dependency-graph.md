# Dependency Graph

## Purpose

This document records explicit dependencies among Project FAR definitions, axioms, propositions, lemmas, and theorems.

A proof may rely only on items earlier in its dependency chain. If a proof depends on itself, directly or indirectly, it fails the circularity audit.

---

# Primitive Definitions

- D-INV: Investigation
- D-REP: Representation
- D-STRUCT: Representational Structure
- D-INT: Interpretation
- D-CALC: Reasoning Calculus

---

# Core Axioms

- A1: Explicit Representation
- A2: Representational Organization
- A3: Interpretation
- A4: Investigation
- A5: Reasoning Calculus

---

# Proposition Dependencies

## P-001 — Representation Requirement

Depends on: A1, D-REP.

## P-002 — Structural Requirement

Depends on: A2, D-REP, D-STRUCT.

## P-003 — Semantic Relativity

Depends on: D-REP, D-INT.

## P-004 — Investigation Relativity

Depends on: D-INV, D-INT, D-CALC.

## P-005 — Calculus Relativity of Admissibility

Depends on: D-CALC, D-INV.

## P-006 — Syntax/Semantics Separation

Depends on: D-STRUCT, D-INT, P-003.

## P-007 — Trace/Process Distinction

Depends on: D-REP, D-STRUCT, D-CALC.

## P-008 — Resolution Dependence

Depends on: D-CALC, D-STRUCT.

---

# Lemma Dependencies

## L-001 — Representation Necessity

Depends on: A1, D-REP.

## L-002 — Structure Necessity

Depends on: A2, D-STRUCT.

## L-003 — Interpretation Necessity

Depends on: A3, D-INT.

## L-004 — Investigation Necessity

Depends on: A4, D-INV.

## L-005 — Calculus Necessity

Depends on: A5, D-CALC.

## L-006 — Canonical Role Pairing

Depends on: D-REP, D-STRUCT, D-INT, D-CALC.

## L-007 — Finite Normalization Termination

Depends on: D-REP, D-STRUCT, D-INT, D-CALC.

## L-008 — Transition Signature Construction

Depends on: D-REP, D-CALC.

---

# Theorem Dependencies

## T-001 — Conditional Primitive Minimality

Depends on: L-001, L-002, L-003, L-004, L-005.

## T-002 — Conditional Primitive Independence

Depends on: T-001, L-001, L-002, L-003, L-004, L-005.

## T-003 — Representation Theorem

Depends on: A1, A2, A3, A4, A5, P-001, P-002, P-003, P-004, P-005.

## T-004 — Semantic Preservation Theorem

Depends on: DEF-030, DEF-031, DEF-034.

## T-005 — Transition Completeness Theorem

Depends on: D-CALC, L-008, T-003.

## T-006 — Primitive Sufficiency Theorem

Depends on: derived-concept registry, D-INV, D-REP, D-STRUCT, D-INT, D-CALC.

## T-007 — Primitive Completeness Theorem

Depends on: T-003, T-006.

## T-008 — Canonical Representation Equivalence

Depends on: L-006, T-004.

## T-009 — Canonical Normal Form Theorem

Depends on: L-007.

## T-010 — Reconstruction Theorem

Depends on: T-003, T-004, P-007.

## T-011 — Conservative Extension Theorem

Depends on: T-006 and the definition policy.

## T-012 — FAR Model Equivalence Theorem

Depends on: FAR model theory.

## T-013 — Relative Soundness Theorem

Depends on: D-CALC, T-005.

## T-014 — Relative Completeness Theorem

Depends on: D-CALC, T-005.

## T-015 — Explicit Reasoning Meta-Theorem

Depends on: T-003, T-007, FAR model theory.

---

# Dependency Rule

No theorem may cite a theorem with a higher number unless it is explicitly marked as a later revision. No theorem may cite itself. No definition may be justified by a theorem that depends on that definition.
