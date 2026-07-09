# T-008 — Canonical Representation Equivalence

## Status

Established for canonical FAR representations.

---

## Statement

Any two canonical FAR representations of the same scoped reasoning process under the same required role inventory are equivalent up to meaning-preserving renaming.

---

## Equivalence Condition

Let:

```text
A = <I, Rep, S, Int, C, T>
B = <I2, Rep2, S2, Int2, C2, T2>
```

`A` and `B` are canonically equivalent when each required role in `A` corresponds to exactly one required role in `B`, and the following are preserved:

1. investigation role;
2. structural relation;
3. assigned meaning;
4. admissibility under the calculus;
5. trace order.

---

## Proof

Let `A` and `B` be canonical FAR representations of the same scoped reasoning process `R` under the same required role inventory.

Because both are canonical, neither omits a required representation and neither adds a redundant representation.

Each representation in `A` therefore fills one required role in the shared required role inventory for `R`. Each representation in `B` fills the same required role inventory for `R`.

Pair each representation in `A` with the representation in `B` that fills the same role.

This pairing is total because every required role in `A` appears in `B`.

This pairing is one-to-one because canonicality excludes duplicate role occupants.

This pairing is onto because every required role in `B` appears in `A`.

The paired representations preserve structure because both represent the same dependency and transition organization of `R`.

They preserve assigned meaning because both represent the same interpreted process.

They preserve admissibility because both encode the same calculus-governed transition roles.

They preserve trace order because both are canonical traces of the same process.

Therefore `A` and `B` are equivalent up to meaning-preserving renaming.

---

## Limitation

This theorem applies only after canonicalization. Raw representations may contain redundancy, omission, compression, or alternate encoding.
