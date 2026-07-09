# T-009 — Canonical Normal Form Theorem

## Status

Established in revised conditional form for finite scoped FAR representations with explicit, total, preservation-respecting, terminating normalization rules.

---

## Statement

Every finite scoped FAR representation admits a canonical normal form when supplied normalization rules for ordering, labeling, and redundancy removal are explicit, total on the representation's finite components, preserve required FAR information, and each normalization step strictly decreases a finite unresolved-item measure without introducing any new unresolved item.

---

## Normalization Procedure

Given:

```text
FAR(R) = <I, Rep, S, Int, C, T>
```

and supplied normalization rules satisfying the statement conditions, construct `NF(R)` by:

1. removing representations not required by the investigation;
2. assigning canonical identifiers to remaining representations by dependency order;
3. sorting structural relations over canonical identifiers;
4. replacing equivalent semantic labels with canonical semantic labels under `Int`;
5. recording calculus rules by canonical rule identifiers;
6. recording transitions by source, rule, target, admissibility status, and order.

---

## Proof

Let `FAR(R)` be finite and scoped, and let the supplied normalization rules satisfy the statement conditions.

Because the normalization rules operate on finite components, strictly decrease a finite unresolved-item measure, and introduce no new unresolved item, L-007 gives termination of the normalization procedure.

Because the supplied ordering and labeling rules are total on the finite components, canonical identifiers can be assigned to remaining representations. If dependency order is partial, the supplied total rule includes the deterministic tie-break needed to produce a total order.

Because `S` is finite over `Rep`, its relation inventory can be sorted after identifiers are assigned.

Because the supplied labeling rules are explicit and total for the finite semantic assignments, each semantic assignment can be replaced with its canonical semantic label.

Because the supplied rule-labeling rules are explicit and total for the finite calculus-rule inventory, each rule can be replaced with its canonical rule identifier.

Because `T` is finite, transitions can be rewritten into the canonical transition-signature format.

By the preservation condition, these steps preserve the required representational, structural, semantic, calculative, and trace information.

Therefore every finite scoped FAR representation admits canonical normal form under supplied normalization rules satisfying the stated conditions.

---

## Corollary

Canonical normal forms make equivalence testing possible by comparing normalized tuples rather than raw documents.

---

## Limitation

This theorem requires finiteness and explicit, total, preservation-respecting, L-007-terminating normalization rules. Infinite representations, underdefined semantic registries, partial ordering rules, or normalization procedures that can introduce new unresolved items require additional machinery.
