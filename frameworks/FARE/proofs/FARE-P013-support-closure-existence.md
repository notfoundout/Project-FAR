# FARE Proof

## Identifier

FARE-P013

---

# Title

Support Closure Existence

---

## Status

Accepted

---

# Objective

Demonstrate that every assessment possesses a unique support closure.

---

# Definitions Used

- Assessment
- Support
- Support Set
- Support Closure

Canonical support terminology is defined in:

`frameworks/FARE/theory/support-theory.md`

---

# Dependencies

- Relationship Definitions
- Graph Definitions
- Support Theory

---

# Theorem

Every assessment possesses a support closure.

---

# Proof

Let **A** be an assessment.

By the definition of Support Closure, the construction begins with the set containing only **A**.

Every assessment directly supporting **A** is then added.

The same operation is applied recursively to every newly added supporting assessment.

If no additional supporting assessments exist, the construction terminates immediately.

Otherwise, the process continues until no further supporting assessments remain.

At termination, the resulting collection satisfies the definition of Support Closure.

Therefore every assessment possesses a support closure.

**Q.E.D.**

---

# Corollary 1

Every assessment belongs to its own support closure.

---

# Corollary 2

Every supporting assessment of an assessment belongs to its support closure.

---

# Consequences

Support analysis may always be performed over a well-defined collection of supporting assessments.

Subsequent support theorems may assume the existence of support closures.

---

# Notes

This theorem establishes existence only.

It does not establish uniqueness.

Uniqueness is established separately by FARE-P014.