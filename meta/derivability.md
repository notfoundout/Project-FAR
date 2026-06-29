# Derivability

## Purpose

This document defines derivability within the meta-theory of Project FAR.

Derivability specifies when one concept is completely determined by other concepts within the framework.

It provides the formal basis for distinguishing primitive concepts from derived concepts.

---

# Definition

A concept is **derivable** if it can be uniquely determined from a specified collection of concepts according to the proof system of Project FAR.

If no such determination exists, the concept is **non-derivable** relative to that collection.

Derivability is always relative to an explicitly identified set of assumptions.

---

# Relative Nature of Derivability

Derivability is not an absolute property.

Instead, every statement of derivability must specify:

- the target concept;
- the concepts assumed;
- the proof system employed.

Accordingly, statements concerning derivability should always be interpreted relative to an explicitly defined context.

---

# Primitive Concepts

A primitive concept is one whose meaning is accepted without derivation within the object theory.

A primitive concept may nevertheless be investigated for possible derivation during theoretical development.

Only concepts shown to be non-derivable relative to the adopted primitive architecture remain primitive within the canonical theory.

---

# Derived Concepts

A derived concept is one whose definition or existence follows from previously established concepts.

Derived concepts should be preferred whenever they preserve the expressive power of the framework.

---

# Derivation

A derivation is a finite sequence of logically valid steps demonstrating that a target concept is uniquely determined by the assumed concepts.

Every derivation should explicitly identify:

- assumptions;
- definitions;
- intermediate results;
- conclusion.

---

# Non-Derivability

A concept is non-derivable if no valid derivation exists from the specified assumptions.

Establishing non-derivability generally requires stronger justification than establishing derivability.

The methods by which non-derivability is established remain an active area of research within Project FAR.

---

# Dependency

If concept B is derivable from concept A, then B depends upon A.

Dependency therefore induces a directed relationship between concepts.

Dependency analysis is treated separately within the meta-theory.

---

# Relationship to Primitive Architecture

The objective of primitive reduction is to maximize derivability while preserving expressive power.

Accordingly:

- unnecessary primitives should be eliminated;
- derived concepts should replace primitive concepts whenever possible;
- primitive concepts should remain only when non-derivability has been established.

---

# Relationship to Theorems

Derivability plays a central role in several flagship theorems of Project FAR.

Most notably:

- T-MINIMAL-PRIMITIVE-ARCHITECTURE;
- T-SUFFICIENCY-OF-PRIMITIVE-ARCHITECTURE;
- T-EXPRESSIVE-SUFFICIENCY.

The interpretation of these theorems depends upon the definition established in this document.

---

# Current Research

The following questions remain under investigation.

- What constitutes sufficient evidence for non-derivability?
- Can model separation universally establish non-derivability?
- Are different proof strategies required for different classes of concepts?
- Can derivability itself be characterized purely structurally?
