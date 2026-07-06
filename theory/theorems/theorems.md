# Theorems

## Purpose

This document records the theorem catalog of Project FAR.

A theorem is a formal result proved from the canonical definitions, axioms, established propositions, and previously established theorems.

Theorems are always scope-relative. A theorem marked Established is established only relative to the dependencies and limitations recorded in its corresponding proof document.

---

## Canonical Prerequisites

Theorems must reference:

- current canonical definitions in `../definitions/definitions.md`;
- current canonical axioms in `../axioms/axioms.md`;
- applicable semantic scope in `../semantics/scope.md`;
- any previously established propositions or theorems.

---

# Established Theorems

## T-001 — Conditional Primitive Minimality

### Statement

The current primitive architecture:

```text
{ Investigation, Representation, Representational Structure, Interpretation, Reasoning Calculus }
```

is minimal relative to the current Project FAR scope, definitions, and axioms.

### Proof

`../proofs/T-001-primitive-minimality.md`

### Status

Established, conditional.

### Limitation

This does not prove that no future lower-level theory can reduce the primitive set. It proves that deletion of any current primitive reduces expressive power under the current framework.

---

## T-002 — Conditional Primitive Independence

### Statement

No current primitive is derivable from the other four without loss of expressive power under the current Project FAR reduction standard.

### Proof

`../proofs/T-002-primitive-independence.md`

### Status

Established, conditional.

### Limitation

This is framework-relative independence, not absolute metaphysical irreducibility.

---

## T-003 — Representation Theorem

### Statement

Every reasoning process within the stated scope of Project FAR admits a FAR representation of the form:

```text
<I, Rep, S, Int, C, T>
```

### Proof

`../proofs/T-003-representation-theorem.md`

### Status

Established within Project FAR scope.

### Limitation

This applies only to explicit reasoning processes satisfying the scope criterion.

---

## T-004 — Semantic Preservation Theorem

### Statement

Every interpretation-preserving representation mapping preserves semantic content.

### Proof

`../proofs/T-004-semantic-preservation.md`

### Status

Established.

### Limitation

This gives a sufficient condition for semantic preservation, not a necessary condition.

---

## T-005 — Transition Completeness Theorem

### Statement

Every explicitly specified admissible reasoning transition within a scoped reasoning process can be represented by a transition signature.

### Proof

`../proofs/T-005-transition-completeness.md`

### Status

Established within scope.

### Limitation

This does not cover hidden or unspecified transitions unless reconstructed and made explicit.

---

# Planned Theorems

## T-006 — FAR Model Homomorphism Preservation

Demonstrate which properties are preserved under structure-preserving mappings between FAR models.

Status: Research.

## T-007 — Conservative Extension

Define and prove conditions under which a new FAR subsystem extends the canonical theory without altering established results.

Status: Research.

## T-008 — Model Compression

Define when two FAR representations can be compressed without loss of specified semantic or structural content.

Status: Research.
