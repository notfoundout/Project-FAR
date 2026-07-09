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

The current primitive architecture is minimal relative to the current Project FAR scope, definitions, and axioms.

Proof: `../proofs/T-001-primitive-minimality.md`

Status: Established, conditional.

---

## T-002 — Conditional Primitive Independence

No current primitive is derivable from the other four without loss of expressive power under the current Project FAR reduction standard.

Proof: `../proofs/T-002-primitive-independence.md`

Status: Established, conditional.

---

## T-003 — Representation Theorem

Every reasoning process within the stated scope of Project FAR admits a FAR representation of the form:

```text
<I, Rep, S, Int, C, T>
```

Proof: `../proofs/T-003-representation-theorem.md`

Status: Established within Project FAR scope.

---

## T-004 — Semantic Preservation Theorem

Every interpretation-preserving representation mapping preserves semantic content.

Proof: `../proofs/T-004-semantic-preservation.md`

Status: Established.

---

## T-005 — Transition Completeness Theorem

Every explicitly specified admissible reasoning transition within a scoped reasoning process can be represented by a transition signature.

Proof: `../proofs/T-005-transition-completeness.md`

Status: Established within scope.

---

## T-006 — Primitive Sufficiency Theorem

Every current non-primitive concept in Project FAR is constructible from the primitive architecture.

Proof: `../proofs/T-006-primitive-sufficiency.md`

Status: Established relative to the current derivation registry and canonical definitions.

---

## T-007 — Primitive Completeness Theorem

The primitive architecture is complete for constructing the objects required to represent any scoped explicit reasoning process.

Proof: `../proofs/T-007-primitive-completeness.md`

Status: Established relative to scoped explicit reasoning processes.

---

## T-008 — Canonical Representation Equivalence

Any two canonical FAR representations of the same scoped reasoning process under the same required role inventory are equivalent up to meaning-preserving renaming.

Proof: `../proofs/T-008-canonical-representation-equivalence.md`

Status: Established for canonical FAR representations.

---

## T-009 — Canonical Normal Form Theorem

Every finite scoped FAR representation admits a canonical normal form when supplied normalization rules for ordering, labeling, and redundancy removal are explicit, total on the representation's finite components, preserve required FAR information, and each normalization step strictly decreases a finite unresolved-item measure without introducing any new unresolved item.

Proof: `../proofs/T-009-canonical-normal-form.md`

Status: Established in revised conditional form for finite scoped FAR representations with explicit, total, preservation-respecting, terminating normalization rules.

---

## T-010 — Reconstruction Theorem

Given a complete FAR representation, the represented reasoning process can be reconstructed up to semantic equivalence.

Proof: `../proofs/T-010-reconstruction-theorem.md`

Status: Established up to semantic equivalence for complete FAR representations.

---

## T-011 — Conservative Extension Theorem

If an extension introduces no new primitive, alters no canonical definition, and changes no established axiom or theorem dependency, then it is conservative over the established core theory.

Proof: `../proofs/T-011-conservative-extension.md`

Status: Established for definitionally conservative FAR extensions.

---

## T-012 — FAR Model Equivalence Theorem

Two FAR models are equivalent relative to a preservation profile if and only if every property in that profile is preserved between them.

Proof: `../proofs/T-012-model-equivalence.md`

Status: Established relative to a specified preservation profile.

---

## T-013 — Relative Soundness Theorem

If a FAR representation marks a transition as admissible only when that transition is admissible under the supplied target calculus, then the FAR representation is sound relative to that calculus.

Proof: `../proofs/T-013-soundness.md`

Status: Established relative to a supplied target calculus.

---

## T-014 — Relative Completeness Theorem

If a FAR representation includes a transition signature for every transition permitted by the supplied calculus within a specified transition domain, then the representation is complete relative to that calculus and domain.

Proof: `../proofs/T-014-relative-completeness.md`

Status: Established relative to a supplied target calculus and explicit transition domain.

---

## T-015 — Explicit Reasoning Meta-Theorem

Every explicit reasoning system satisfying Project FAR scope assumptions is representable as a FAR model.

Proof: `../proofs/T-015-explicit-reasoning-meta-theorem.md`

Status: Established for explicit reasoning systems satisfying Project FAR scope assumptions.

---

# Planned Theorems

## T-016 — Model Homomorphism Preservation

Demonstrate which properties are preserved under structure-preserving mappings between FAR models.

Status: Research.

---

## T-017 — Compression without Semantic Loss

Define when two FAR representations can be compressed without loss of specified semantic or structural content.

Status: Research.

---

## T-018 — Dependency Graph Acyclicity Conditions

Identify conditions under which a FAR dependency graph is acyclic, cyclic, or fixed-point dependent.

Status: Research.
