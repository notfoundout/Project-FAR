# Meta-Theory Definitions

## Purpose

This document establishes the canonical terminology of the Meta-Theory.

The definitions contained herein apply throughout Project FAR unless explicitly overridden by a subsystem.

Only concepts common to formal theories in general belong in this document.

---

# Definition 1 — Formal Theory

A **formal theory** is a formally specified system consisting of:

- a language;
- definitions;
- assumptions;
- inference rules; and
- derivable statements.

A formal theory determines how formal objects are represented, interpreted, and reasoned about.

---

# Definition 2 — Formal Object

A **formal object** is any explicitly identifiable object belonging to a formal theory.

Examples include:

- terms;
- definitions;
- axioms;
- inference rules;
- propositions;
- theorems;
- proofs;
- models; and
- interpretations.

---

# Definition 3 — Definition

A **definition** specifies the meaning of a formal term.

Definitions introduce terminology.

They neither assert nor prove formal statements.

---

# Definition 4 — Primitive

A **primitive** is a formal object whose meaning is not defined in terms of other formal objects within the same theory.

Primitive status is always relative to a particular theory.

---

# Definition 5 — Statement

A **statement** is a formal object capable of possessing a truth value within a formal theory.

Statements may function as assumptions, propositions, or theorems.

---

# Definition 6 — Axiom

An **axiom** is a statement accepted without proof within a formal theory.

Axioms constitute the foundational assumptions from which additional statements are derived.

---

# Definition 7 — Proposition

A **proposition** is a statement formally derived from previously established statements but not designated as a principal result of the theory.

---

# Definition 8 — Theorem

A **theorem** is a proposition designated as a principal formally established result of the theory.

The distinction between propositions and theorems is one of theoretical significance rather than logical status.

---

# Definition 9 — Proof

A **proof** is a finite sequence of statements in which every statement is either:

- an assumption;
- an axiom; or
- obtained from previous statements by admissible inference rules.

The final statement is the conclusion established by the proof.

---

# Definition 10 — Inference Rule

An **inference rule** specifies a formally admissible pattern by which one or more statements justify another statement.

Inference rules determine the valid proof steps of a formal theory.

---

# Definition 11 — Derivation

A **derivation** is the construction of a formal object from previously established formal objects according to admissible inference rules.

Every proof is a derivation.

Not every derivation is necessarily presented as a proof.

---

# Definition 12 — Model

A **model** is a mathematical structure that assigns meaning to the formal objects of a theory in such a way that the theory may be interpreted and analyzed.

---

# Definition 13 — Interpretation

An **interpretation** assigns semantic meaning to the formal language of a theory within a model.

---

# Definition 14 — Derivability

A formal object is **derivable** from a specified collection of premises if there exists a finite derivation of that object according to the inference rules of the theory.

---

# Definition 15 — Independence

A formal object is **independent** of a specified collection of formal objects if it is not derivable from that collection.

---

# Definition 16 — Consistency

A formal theory is **consistent** if no statement and its negation are both derivable within the theory.

---

# Definition 17 — Soundness

A proof system is **sound** with respect to a semantics if every derivable statement is semantically valid.

---

# Definition 18 — Completeness

A proof system is **complete** with respect to a semantics if every semantically valid statement is derivable.

---

# Definition 19 — Minimality

A collection of formal objects is **minimal** if no member is derivable from the remaining members while preserving the intended capabilities of the theory.

---

# Definition 20 — Sufficiency

A collection of formal objects is **sufficient** if it is capable of generating every formal object intended to be derivable within the theory.

---

# Definition 21 — Canonical

A **canonical** formal object is one that has been officially incorporated into the formal theory.

Canonical objects are distinguished from provisional objects appearing only within research documents.
