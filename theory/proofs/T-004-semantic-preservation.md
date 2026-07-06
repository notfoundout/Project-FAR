# T-004 — Semantic Preservation Theorem

## Status

Established for interpretation-preserving representation mappings.

---

## Statement

Let `M` be a representation mapping from a source representational structure `S1` to a target representational structure `S2`.

If `M` preserves interpretation for every mapped representation, then `M` preserves semantic content.

---

## Formal Condition

For every representation `r` in the domain of `M`:

```text
Int1(r) = Int2(M(r))
```

Then:

```text
SemanticContent(Int1, r) = SemanticContent(Int2, M(r))
```

---

## Dependencies

- Representation Mapping
- Interpretation
- Semantic Content
- Semantic Equivalence

---

## Proof

By definition, semantic content is the meaning assigned to a representation under a specified interpretation.

Assume `M` is interpretation-preserving. Then for every source representation `r`, the meaning assigned to `r` under `Int1` is identical to the meaning assigned to `M(r)` under `Int2`.

Therefore, for every mapped representation, the semantic content before mapping equals the semantic content after mapping.

By definition of semantic equivalence, `r` and `M(r)` are semantically equivalent under the paired interpretations.

Therefore `M` preserves semantic content.

---

## Corollary

A FAR transformation can preserve meaning only if semantic preservation is specified or proved. Structural preservation alone is insufficient.

---

## Limitation

This theorem gives a sufficient condition for semantic preservation. It does not claim that interpretation preservation is the only possible condition under which semantic preservation can occur.
