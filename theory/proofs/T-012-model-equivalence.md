# T-012 — FAR Model Equivalence Theorem

## Status

Established relative to a specified preservation profile.

---

## Statement

Two FAR models are equivalent relative to a preservation profile `Q` if and only if every property in `Q` is preserved between them.

---

## Definitions

A preservation profile `Q` is a finite set of properties selected from structural, semantic, calculative, trace, and investigation-relative properties.

Two models `A` and `B` are `Q`-equivalent when:

```text
A ≡Q B
```

meaning every property in `Q` holds in `A` exactly when the corresponding property holds in `B`.

---

## Proof

Forward direction: Assume `A ≡Q B`. By definition of `Q`-equivalence, every property in `Q` is preserved between `A` and `B`. Therefore all properties in `Q` are preserved.

Reverse direction: Assume every property in `Q` is preserved between `A` and `B`. By definition of preservation-profile equivalence, this is exactly the condition for `A ≡Q B`. Therefore `A` and `B` are `Q`-equivalent.

Thus two FAR models are equivalent relative to `Q` if and only if every property in `Q` is preserved between them.

---

## Corollary

Model equivalence is not absolute in FAR. It is always relative to the properties selected for preservation.

---

## Limitation

This theorem is definitional but necessary. Stronger equivalence theorems require specifying particular preservation profiles and proving nontrivial mappings between models.
