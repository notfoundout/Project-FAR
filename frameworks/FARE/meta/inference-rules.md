# FARE Inference Rules

## Purpose

This document defines the inference rules permitted within the Formal Architecture of Reasoning Evaluation.

Every accepted proof shall derive its conclusions using only the inference rules defined herein or additional rules explicitly accepted through future investigation.

---

# Rule R1 — Definition Introduction

A canonical definition may introduce a formally defined concept.

Definitions establish meaning.

Definitions do not establish truth.

---

# Rule R2 — Definition Substitution

A formally defined concept may be replaced by its canonical definition.

Likewise, a canonical definition may be replaced by the concept it defines.

---

# Rule R3 — Previously Proven Result

An accepted theorem may be used as a premise in a subsequent proof.

Every referenced theorem shall appear within the proof dependencies.

---

# Rule R4 — Modus Ponens

If:

- P
- P implies Q

have both been established,

then Q may be concluded.

---

# Rule R5 — Contradiction

If an assumption necessarily produces a contradiction with accepted premises, that assumption may be rejected.

---

# Rule R6 — Equivalence Substitution

Equivalent representations may replace one another wherever the established equivalence relation applies.

---

# Rule R7 — Universal Instantiation

A universally established property may be applied to a particular instance satisfying its conditions.

---

# Rule R8 — Universal Generalization

A universally quantified conclusion may be established only after demonstrating that the proof does not depend upon properties unique to a particular instance.

---

# Rule R9 — Dependency Introduction

A proof may reference another result only through an explicit dependency.

Implicit dependencies are prohibited.

---

# Rule R10 — Dependency Elimination

A dependency may be removed only if the proof remains complete without it.

Unused dependencies shall be eliminated.

---

# Rule R11 — Case Analysis

A proof may consider multiple mutually exclusive cases.

The conclusion is established only if every possible case reaches the same result.

---

# Rule R12 — Mathematical Induction

When reasoning over recursively defined or well-ordered structures, induction may be employed provided:

- a base case is established;
- the inductive step is proven.

---

# Rule R13 — Structural Induction

For recursively defined representations or graphs, structural induction may replace ordinary mathematical induction.

---

# Rule R14 — Proof by Construction

Existence may be established by explicitly constructing an object satisfying the required properties.

---

# Rule R15 — Proof by Exhaustion

A conclusion may be established by demonstrating every possible case individually when the domain is finite.

---

# Rule R16 — Dependency Transparency

Every inference shall identify the premises upon which it depends.

Hidden reasoning is prohibited.

---

# Relationship to Proofs

Every accepted proof within FARE shall be expressible entirely through:

- accepted axioms;
- canonical definitions;
- accepted premises;
- accepted inference rules.

---

# Notes

Future investigations may extend this inference system.

No accepted proof may rely upon an inference rule that has not been formally admitted into the framework.