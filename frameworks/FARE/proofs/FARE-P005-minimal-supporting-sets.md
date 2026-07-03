# FARE Proof

## Identifier

FARE-P005

---

# Title

Minimal Supporting Sets

---

## Status

Accepted

---

# Objective

Demonstrate that every finite sufficient support set contains at least one minimal support set.

---

# Definitions Used

- Support
- Support Set
- Sufficient Support
- Necessary Support
- Minimal Support Set

Canonical support terminology is defined in:

`frameworks/FARE/theory/support-theory.md`

---

# Dependencies

- Relationship Definitions
- Support Theory

---

# Theorem

Every finite sufficient support set contains at least one minimal support set.

---

# Proof

Let $begin:math:text$S$end:math:text$ be a finite sufficient support set.

If no assessment can be removed from $begin:math:text$S$end:math:text$ without destroying sufficiency, then $begin:math:text$S$end:math:text$ is already minimal.

Otherwise, remove one assessment whose removal preserves sufficiency.

The resulting support set remains sufficient.

If this new support set is minimal, the proof is complete.

Otherwise, repeat the removal process.

Because the support set is finite, the number of removable assessments is finite.

Each iteration strictly decreases the number of assessments contained in the support set.

Therefore the process must terminate.

Termination can occur only when no further supporting assessment may be removed without destroying sufficiency.

By Definition 6 of Support Theory, the resulting support set is a minimal support set.

Therefore every finite sufficient support set contains at least one minimal support set.

**Q.E.D.**

---

# Corollary 1

Every finite sufficient support set possesses at least one irreducible subset.

---

# Corollary 2

Minimal support sets are not necessarily unique.

Different reduction orders may produce different minimal support sets.

---

# Consequences

Support analysis may ignore redundant supporting assessments once a minimal support set has been identified.

Algorithms may reduce finite support sets without losing sufficiency.

Support optimization becomes formally well-defined.

---

# Notes

This theorem guarantees existence only.

It does not establish uniqueness.

It does not prescribe an algorithm for computing every minimal support set.