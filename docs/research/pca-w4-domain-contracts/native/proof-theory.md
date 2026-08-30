# Native contract: proof theory

Status: **FROZEN BEFORE CONTROLLED MAPPING**

## Native comparison question

Does an end-sequent alone determine whether a derivation is already cut-free? Došen surveys proof-identity criteria based on normalization and, for sequent systems, reduction to cut-free form, while emphasizing that proposed criteria coincide only in restricted fragments [dosen2003identity].

## Finite derivations

Both cases conclude `A |- A` in a minimal two-sided sequent presentation.

- `DId` is the identity derivation and contains no cut.
- `DCut` applies cut on `A` to two identity premises `A |- A`, again concluding `A |- A`.

The declared behavior asks whether the supplied derivation is already cut-free. It is true for `DId` and false for `DCut`. The end-sequent alone is identical and cannot determine the answer.

The repaired carrier is the explicit derivation tree with rule labels. The decoder recursively scans the tree for a `Cut` node.

## Scope boundary

The result concerns only the supplied trees and the Boolean cut-occurrence observation. It is not a proof-identity theorem, a normalization proof, a complexity bound, or a claim that cut-free form uniquely identifies proofs.
