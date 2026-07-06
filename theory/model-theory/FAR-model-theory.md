# FAR Model Theory

## Status

Initial canonical model-theory specification.

---

## Purpose

This document defines the model-theoretic apparatus used to interpret FAR structures.

The goal is not to impose one logic on all reasoning. The goal is to give Project FAR a general semantic layer capable of describing when a FAR representation satisfies a reasoning process, investigation, or theory-relative condition.

---

## Definition 1 — FAR Signature

A FAR signature is a tuple:

```text
Σ = <P, Rel, Func>
```

where:

- `P` is a set of primitive sorts;
- `Rel` is a set of relation symbols over those sorts;
- `Func` is a set of mapping symbols over those sorts.

For the current Project FAR architecture:

```text
P = { Investigation, Representation, RepresentationalStructure, Interpretation, ReasoningCalculus }
```

---

## Definition 2 — FAR Structure

A FAR structure over `Σ` is a tuple:

```text
A = <I, Rep, S, Int, C>
```

where:

- `I` is a nonempty set of investigations;
- `Rep` is a nonempty set of representations;
- `S` assigns representational relations over subsets of `Rep`;
- `Int` assigns semantic content to representations relative to investigations;
- `C` assigns admissible transition rules relative to investigations.

---

## Definition 3 — FAR Model

A FAR model is a FAR structure satisfying the current Project FAR axioms.

Thus `A` is a FAR model if:

1. every scoped reasoning process represented in `A` has explicit representations;
2. every participating representation collection in `A` has representational structure;
3. every participating representation in `A` is interpreted within an investigation;
4. every represented reasoning process in `A` occurs within exactly one investigation;
5. every represented reasoning process in `A` proceeds according to a reasoning calculus.

---

## Definition 4 — Satisfaction

A FAR model `A` satisfies a Project FAR statement `φ`, written:

```text
A ⊨ φ
```

if `φ` holds under the interpretations, structures, and calculi assigned by `A`.

Satisfaction is always relative to:

- a model;
- an interpretation;
- a scope;
- and the reasoning calculus governing admissibility.

---

## Definition 5 — Validity

A Project FAR statement `φ` is valid relative to a class of FAR models `K` if every model in `K` satisfies `φ`:

```text
K ⊨ φ iff for every A in K, A ⊨ φ
```

---

## Definition 6 — Model Equivalence

Two FAR models `A` and `B` are equivalent relative to a property set `Q` if every property in `Q` is preserved between `A` and `B`.

Model equivalence is not absolute. It is always relative to the specified preserved properties.

---

## Definition 7 — Representation of a Reasoning Process

A FAR model `A` represents a reasoning process `R` if there exists a tuple:

```text
<I, Rep, S, Int, C, T>
```

inside `A` satisfying the Representation Theorem for `R`.

---

## Definition 8 — Sound FAR Representation

A FAR representation of a reasoning process is sound relative to a target calculus if every transition marked admissible by the FAR representation is admissible under that target calculus.

---

## Definition 9 — Complete FAR Representation

A FAR representation of a reasoning process is complete relative to a target objective if it contains every representation, structural relation, interpretation assignment, calculus rule, and transition signature required to achieve that objective.

Completeness is objective-relative, not absolute.

---

## Immediate Results

1. Every FAR model separates syntax from semantics.
2. Every FAR model relativizes reasoning to an investigation.
3. Every FAR model relativizes admissibility to a reasoning calculus.
4. Every FAR model supports multiple interpretations of the same representation.
5. Every FAR model can compare two reasoning processes by comparing their tuples component by component.

---

## Open Work

Future model-theory work should define:

- homomorphisms between FAR models;
- submodels;
- model compression;
- conservative extension;
- representation-equivalence classes;
- preservation theorems for specific transformation families.
