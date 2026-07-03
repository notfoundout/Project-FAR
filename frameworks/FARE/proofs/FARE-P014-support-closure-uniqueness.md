# FARE Proof

## Identifier

FARE-P014

---

# Title

Support Closure Uniqueness

---

## Status

Accepted

---

# Objective

Demonstrate that every assessment possesses exactly one support closure.

---

# Definitions Used

- Assessment
- Support
- Support Closure

Canonical support terminology is defined in:

`frameworks/FARE/theory/support-theory.md`

---

# Dependencies

- Support Theory
- FARE-P013 — Support Closure Existence

---

# Theorem

Every assessment possesses exactly one support closure.

---

# Proof

Let **A** be an assessment.

By FARE-P013, a support closure exists for **A**.

Suppose two distinct support closures exist for **A**, denoted **C₁** and **C₂**.

By the definition of Support Closure, each closure contains:

- **A**;
- every assessment directly supporting **A**;
- every assessment recursively supporting those assessments.

Suppose **C₁** contains an assessment not contained in **C₂**.

Then **C₂** has omitted an assessment required by the recursive definition of support closure.

Therefore **C₂** does not satisfy the definition of Support Closure.

Similarly, if **C₂** contains an assessment not contained in **C₁**, then **C₁** fails to satisfy the same definition.

Therefore neither closure may differ from the other.

Hence **C₁ = C₂**.

Therefore every assessment possesses exactly one support closure.

**Q.E.D.**

---

# Corollary 1

Support closure is a well-defined mathematical object.

---

# Corollary 2

Every assessment has a uniquely determined support dependency structure.

---

# Consequences

Support closure may be referenced unambiguously throughout FARE.

Algorithms operating on support closures always operate on the same mathematical object.

Subsequent proofs may refer to "the support closure" without ambiguity.

---

# Notes

This theorem establishes uniqueness.

Existence is established by FARE-P013.

Together, FARE-P013 and FARE-P014 establish that support closure is a well-defined construct within FARE.