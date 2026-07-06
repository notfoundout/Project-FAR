# T-009 — Canonical Normal Form Theorem

## Status

Established for finite scoped FAR representations with explicit ordering rules.

---

## Statement

Every finite scoped FAR representation admits a canonical normal form once ordering, labeling, and redundancy-removal rules are supplied.

---

## Normalization Procedure

Given:

```text
FAR(R) = <I, Rep, S, Int, C, T>
```

construct `NF(R)` by:

1. removing representations not required by the investigation;
2. assigning canonical identifiers to remaining representations by dependency order;
3. sorting structural relations over canonical identifiers;
4. replacing equivalent semantic labels with canonical semantic labels under `Int`;
5. recording calculus rules by canonical rule identifiers;
6. recording transitions by source, rule, target, admissibility status, and order.

---

## Proof

Let `FAR(R)` be finite and scoped.

Because `Rep` is finite, redundancy-removal terminates after finitely many deletion checks.

Because the remaining representation set is finite, canonical identifiers can be assigned by any specified total ordering. If dependency order is partial, a deterministic tie-break rule produces a total order.

Because `S` is finite over `Rep`, its relation inventory can be sorted after identifiers are assigned.

Because `Int` is explicit, each semantic assignment can be replaced with its canonical semantic label whenever the semantic registry supplies one.

Because `C` is explicit, each rule can be replaced with its canonical rule identifier.

Because `T` is finite, transitions can be rewritten into the canonical transition-signature format.

Each step terminates and preserves the required representational, structural, semantic, calculative, and trace information.

Therefore every finite scoped FAR representation admits canonical normal form under supplied normalization rules.

---

## Corollary

Canonical normal forms make equivalence testing possible by comparing normalized tuples rather than raw documents.

---

## Limitation

This theorem requires finiteness and explicit normalization rules. Infinite representations or underdefined semantic registries require additional machinery.
