# FARE Proof

## Identifier

FARE-P016

---

# Title

Redundant Support Elimination

---

## Status

Accepted

---

# Objective

Demonstrate that redundant supporting assessments may be removed from a finite sufficient support set while preserving sufficiency until a minimal support set remains.

---

# Definitions Used

- Support
- Support Set
- Sufficient Support
- Unnecessary Support
- Minimal Support Set

Canonical support terminology is defined in:

`frameworks/FARE/theory/support-theory.md`

---

# Dependencies

- Support Theory
- FARE-P005 — Minimal Supporting Sets

---

# Theorem

Let **S** be a finite sufficient support set.

If **S** contains one or more unnecessary supporting assessments, those assessments may be removed one at a time while preserving sufficiency until a minimal support set remains.

---

# Proof

Let **S** be a finite sufficient support set.

Suppose **S** contains an unnecessary supporting assessment.

By the definition of unnecessary support, removing that assessment preserves the sufficiency of the remaining support set.

If the resulting support set is minimal, the process terminates.

Otherwise, another unnecessary supporting assessment exists.

Again remove one unnecessary supporting assessment.

Each removal strictly decreases the number of assessments contained in the support set.

Since **S** is finite, this process cannot continue indefinitely.

Therefore the process terminates after finitely many removals.

Termination occurs only when no unnecessary supporting assessment remains.

By the definition of a minimal support set, the remaining support set is minimal.

Therefore every finite sufficient support set can be reduced to a minimal support set through successive elimination of unnecessary supporting assessments.

**Q.E.D.**

---

# Corollary 1

Every finite sufficient support set contains a redundancy-free sufficient support set.

---

# Corollary 2

Every redundancy elimination process terminates after finitely many steps.

---

# Corollary 3

Different elimination orders may produce different minimal support sets.

Minimal support sets therefore need not be unique.

---

# Consequences

Support graphs may be simplified without affecting sufficiency.

Redundant evidence may be removed while preserving evaluative justification.

Support optimization algorithms are mathematically justified.

Minimal support computation is guaranteed to terminate for finite support sets.

---

# Notes

This theorem concerns finite support sets only.

Infinite support structures require separate treatment and are outside the scope of the present theory.

The theorem establishes existence of a terminating reduction process, not uniqueness of the resulting minimal support set.