# Core Lemmas

## Purpose

This document breaks major Project FAR proofs into smaller reusable lemmas.

---

## L-001 — Representation Necessity

### Statement

For any scoped reasoning process, satisfaction of Project FAR Axiom 1 requires the existence, for Project FAR evaluation, of at least one explicit representation admitted for that process.

### Proof

Axiom 1 requires every scoped reasoning process to admit one or more explicit representations. Assume a scoped reasoning process satisfies the Axiom 1 requirement while no explicit representation is admitted for that process for Project FAR evaluation. Then the process does not admit one or more explicit representations, contradicting Axiom 1. Therefore satisfaction of Axiom 1 requires at least one explicit representation admitted for that process.

---

## L-002 — Structure Necessity

### Statement

No participating collection of representations satisfies Project FAR Axiom 2 unless it possesses representational structure.

### Proof

Axiom 2 requires every collection of representations participating in a reasoning process to possess a representational structure. Assume a participating collection of representations lacks representational structure. Then the collection fails the condition imposed by Axiom 2. Therefore a participating collection of representations satisfies Axiom 2 only if it possesses representational structure.

---

## L-003 — Interpretation Necessity

### Statement

A participating representation cannot satisfy Project FAR Axiom 3 without interpretation.

### Proof

Axiom 3 requires every participating representation to be interpreted within an investigation. Assume a participating representation has no interpretation. Then Axiom 3 is not satisfied. Therefore interpretation is necessary.

---

## L-004 — Investigation Necessity

### Statement

A scoped reasoning process cannot satisfy Project FAR Axiom 4 without an investigation.

### Proof

Axiom 4 requires every reasoning process to occur within exactly one investigation. Assume a reasoning process has no investigation. Then it does not occur within exactly one investigation. This contradicts Axiom 4. Therefore investigation is necessary.

---

## L-005 — Calculus Necessity

### Statement

A scoped reasoning process cannot satisfy Project FAR Axiom 5 without a reasoning calculus.

### Proof

Axiom 5 requires every reasoning process to proceed according to a reasoning calculus. Assume a reasoning process has no calculus. Then Axiom 5 is not satisfied. Therefore reasoning calculus is necessary.

---

## L-006 — Canonical Role Pairing

### Statement

If two canonical FAR representations represent the same scoped reasoning process, then each required role in one has exactly one counterpart in the other.

### Proof

Canonical representations omit no required role and include no redundant role. If both represent the same scoped reasoning process, they contain the same required role inventory. Therefore each required role in the first representation has exactly one counterpart in the second.

---

## L-007 — Finite Normalization Termination

### Statement

A normalization procedure over a finite FAR representation terminates when each normalization step strictly reduces unresolved ordering, labeling, or redundancy.

### Proof

A finite FAR representation contains finitely many representations, relations, semantic assignments, rules, and transition signatures. Each normalization step resolves or removes at least one unresolved item. Since the unresolved set is finite and no step increases it, the procedure terminates.

---

## L-008 — Transition Signature Construction

### Statement

Every explicit admissible transition can be represented as a transition signature when source state, target state, rule, and admissibility status are specified.

### Proof

A transition signature is defined as a representation of a transformation execution between reasoning states. If source state, target state, rule, and admissibility status are specified, then all required components of the signature are present. Therefore the transition can be represented as a transition signature.
