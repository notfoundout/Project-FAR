# T-006 — Primitive Sufficiency Theorem

## Status

Established relative to `theory/derivations/derived-concept-registry.md`.

---

## Statement

Every registered non-primitive concept in Project FAR is constructible from the primitive architecture:

```text
P = { Investigation, Representation, Representational Structure, Interpretation, Reasoning Calculus }
```

More precisely:

```text
For every d in RegisteredDerivedConcepts, d is constructible from P by finite definitional substitution.
```

---

## Dependencies

- `theory/derivations/derived-concept-registry.md`
- D-INV — Investigation
- D-REP — Representation
- D-STRUCT — Representational Structure
- D-INT — Interpretation
- D-CALC — Reasoning Calculus

---

## Dependency Standard

This theorem is registry-relative.

A concept is covered only if it appears in the derived-concept registry. Future concepts are not covered until they are added to the registry with a valid derivation path.

---

## Proof

Let `d` be an arbitrary concept in `RegisteredDerivedConcepts`.

By the registry rule, every registered derived concept is assigned a derivation path from either:

1. a primitive concept in `P`; or
2. one or more previously registered derived concepts.

Proceed by induction over registry depth.

Base case: If `d` is first-level, then the registry derives `d` directly from one or more primitives in `P`. Therefore `d` is constructible from `P`.

Inductive step: Assume every registered concept at registry depth `n` or lower is constructible from `P`. Let `d` be a registered concept at depth `n + 1`. By registry construction, `d` derives from primitives and previously registered concepts. Every previously registered concept used in the derivation has depth at most `n`. By the induction hypothesis, each is constructible from `P`. Substituting those primitive constructions into the derivation of `d` yields a finite construction of `d` from `P`.

Therefore every registered derived concept is constructible from `P`.

Since `d` was arbitrary, the result holds for all concepts in the current registry.

---

## Corollary

The registered derived layer is definitionally conservative over the primitive architecture.

---

## Audit Requirement

Whenever a new derived concept is added to Project FAR, T-006 remains valid only if the concept is added to the registry with a finite derivation path from `P`.

---

## Limitation

This theorem does not cover unregistered terms, informal explanatory language, or future concepts not yet added to the registry.
