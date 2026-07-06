# T-006 — Primitive Sufficiency Theorem

## Status

Established relative to the current derivation registry and canonical definitions.

---

## Statement

Every current non-primitive concept in Project FAR is constructible from the primitive architecture:

```text
P = { Investigation, Representation, Representational Structure, Interpretation, Reasoning Calculus }
```

For every derived concept `d` currently used by Project FAR, there exists a finite definitional construction from `P`.

---

## Dependency Standard

This theorem is registry-relative. A concept is covered only if it appears in the current canonical definitions or derived-concept layer. New concepts introduced later require extension of this proof or a new sufficiency audit.

---

## Proof

Let `d` be an arbitrary current non-primitive concept in Project FAR.

By the Project FAR definition policy, every non-primitive concept must be defined in terms of canonical primitives, previously derived concepts, or explicit combinations of those concepts.

Proceed by structural induction over the derivation order.

Base case: A first-level derived concept is defined directly using one or more primitives from `P`. Therefore it is constructible from `P`.

Inductive step: Assume every derived concept at depth `n` or lower is constructible from `P`. Let `d` be a derived concept at depth `n + 1`. By definition policy, `d` is defined using primitives and previously derived concepts. Every previously derived concept in that definition has depth at most `n`. By the induction hypothesis, each is constructible from `P`. Substituting those constructions into the definition of `d` yields a finite construction of `d` from `P`.

Therefore every current derived concept is constructible from `P`.

---

## Corollary

The current derived layer is definitionally conservative over the primitive architecture. It adds expressive convenience but no new primitive kind.

---

## Limitation

This theorem depends on the current derivation registry being complete. If a document uses an undefined or extra-primitive term, that term is not covered until it is registered and derived.
