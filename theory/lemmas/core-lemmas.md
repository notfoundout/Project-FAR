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

No participating representation satisfies Project FAR Axiom 3 unless it is interpreted within an investigation.

### Proof

Axiom 3 requires every representation participating in a reasoning process to be interpreted within an investigation. Assume a participating representation is not interpreted within an investigation. Then the condition imposed by Axiom 3 is not satisfied for that representation. Therefore no participating representation satisfies Axiom 3 unless it is interpreted within an investigation.

---

## L-004 — Investigation Necessity

### Statement

No scoped reasoning process satisfies Project FAR Axiom 4 unless it occurs within exactly one investigation.

### Proof

Axiom 4 requires every reasoning process within the stated Project FAR scope to occur within exactly one investigation. Assume a scoped reasoning process does not occur within exactly one investigation. Then the process fails the condition imposed by Axiom 4. Therefore no scoped reasoning process satisfies Axiom 4 unless it occurs within exactly one investigation.

---

## L-005 — Calculus Necessity

### Statement

No scoped reasoning process satisfies Project FAR Axiom 5 unless it proceeds according to a reasoning calculus governing its admissible reasoning transitions.

### Proof

Axiom 5 requires every reasoning process within the stated Project FAR scope to proceed according to a reasoning calculus governing its admissible reasoning transitions. Assume a scoped reasoning process does not proceed according to such a reasoning calculus. Then the process fails the condition imposed by Axiom 5. Therefore no scoped reasoning process satisfies Axiom 5 unless it proceeds according to a reasoning calculus governing its admissible reasoning transitions.

---

## L-006 — Canonical Role Pairing

### Statement

If two canonical FAR representations represent the same scoped reasoning process under the same required role inventory, then each required role in one representation has exactly one counterpart in the other.

### Proof

Canonical FAR representations omit no required role and include no redundant required role relative to their required role inventory. If two canonical FAR representations represent the same scoped reasoning process under the same required role inventory, then both contain exactly that required role inventory. Therefore each required role in the first representation has exactly one counterpart in the second.

---

## L-007 — Finite Normalization Termination

### Statement

A normalization procedure over a finite FAR representation terminates if each normalization step strictly decreases a finite unresolved-item measure for ordering, labeling, and redundancy and introduces no new unresolved item.

### Proof

A finite FAR representation has a finite unresolved-item measure for ordering, labeling, and redundancy. Assume each normalization step strictly decreases that measure and introduces no new unresolved item. The measure is a natural-number-valued quantity and therefore cannot decrease strictly forever. Therefore the normalization procedure terminates.

---

## L-008 — Transition Signature Construction

### Statement

Every explicit admissible transition can be represented as a transition signature when source state, target state, rule, and admissibility status are specified.

### Proof

A transition signature is defined as a representation of a transformation execution between reasoning states. If source state, target state, rule, and admissibility status are specified, then all required components of the signature are present. Therefore the transition can be represented as a transition signature.
