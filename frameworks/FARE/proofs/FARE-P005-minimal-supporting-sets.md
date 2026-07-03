# FARE Proof

## Identifier

FARE-P005

---

# Title

Minimal Supporting Sets

---

## Status

Draft

---

# Objective

Demonstrate that every assessment possesses one or more minimal supporting sets consisting of the smallest collections of supporting assessments sufficient to sustain the assessment.

---

# Definitions Used

- Assessment
- Assessment Graph
- Assessment Dependency
- Dependency Closure

---

# Theorem

Every supported assessment possesses at least one minimal supporting set.

---

# Proof

Let A be an assessment possessing one or more supporting assessments.

By FARE-P004, A possesses a dependency closure containing every assessment upon which A depends.

The dependency closure itself supports A.

If the closure contains unnecessary supporting assessments, remove one.

If A remains supported, the removed assessment was unnecessary.

Repeat this process.

Because the dependency closure is finite, repeated removal must eventually terminate.

Termination occurs when removing any remaining supporting assessment would prevent adequate support for A.

The remaining collection is therefore minimal.

Hence every supported assessment possesses at least one minimal supporting set.

∎

---

# Corollary 1

Minimal supporting sets need not be unique.

Different collections of supporting assessments may independently provide sufficient support.

---

# Corollary 2

Every minimal supporting set is contained within the dependency closure.

---

# Corollary 3

The dependency closure generally contains more assessments than any individual minimal supporting set.

---

# Consequences

Minimal supporting sets provide a formal basis for:

- dependency reduction;
- explanation generation;
- impact analysis;
- justification minimization;
- efficient reevaluation.

---

# Dependencies

FARE-028

FARE-P004

---

# Notes

This theorem establishes existence only.

It does not establish algorithms for computing minimal supporting sets.