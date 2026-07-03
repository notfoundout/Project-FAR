# FARE Proof

## Identifier

FARE-P017

---

# Title

Dependency Support Propagation

---

## Status

Accepted

---

# Objective

Demonstrate that support propagates through dependency relationships under preserved evaluation conditions.

---

# Definitions Used

- Assessment
- Dependency
- Support
- Support Set

Canonical terminology is defined in:

- `frameworks/FARE/definitions/relationship-definitions.md`
- `frameworks/FARE/theory/support-theory.md`

---

# Dependencies

- Relationship Definitions
- Support Theory
- FARE-P005 — Minimal Supporting Sets

---

# Theorem

Let **A**, **B**, and **C** be assessments.

If:

- **A** depends upon **B**,
- **B** is supported by **C**, and
- the dependency between **A** and **B** is preserved,

then the support provided by **C** contributes indirectly to the support of **A**.

---

# Proof

Assume **A** depends upon **B**.

By the definition of dependency, evaluation of **A** requires **B**.

Assume **B** is supported by **C**.

By the definition of support, **C** contributes positively to the justification of **B**.

Since **B** is required for evaluating **A**, every contribution to the justification of **B** necessarily contributes to the evaluation of **A** while the dependency remains unchanged.

Therefore the support supplied by **C** propagates indirectly to **A** through **B**.

**Q.E.D.**

---

# Corollary 1

Support may propagate across chains of dependency.

---

# Corollary 2

Indirect support may exist even when no direct support relationship exists.

---

# Corollary 3

Removing an intermediate dependency interrupts support propagation.

---

# Consequences

Support analysis may consider indirect supporting assessments.

Dependency graphs become sufficient for computing propagated support.

Future algorithms may distinguish direct support from propagated support.

---

# Notes

This theorem does not state that support is transitive.

It establishes only that support may propagate through dependency relationships under preserved evaluation conditions.

Whether propagated support is equivalent to direct support remains a separate investigation.