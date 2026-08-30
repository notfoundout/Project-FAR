# Native contract: argumentation

Status: **FROZEN BEFORE CONTROLLED MAPPING**

## Native comparison question

Does an attack graph alone determine accepted arguments when preferences decide which attacks succeed as defeats? Prakken distinguishes non-evaluative attack from defeat determined by attack plus preference [prakken2010abstract]. Modgil and Prakken explain that accepted arguments are evaluated on the resulting defeat framework [modgil2014aspic].

## Finite frameworks

Both cases have arguments `{A,B}` and attacks `{A -> B, B -> A}`. In `FAB`, `A` is strictly preferred to `B`; in `FBA`, `B` is strictly preferred to `A`. An attack `x -> y` succeeds exactly when `y` is not strictly preferred to `x`.

Thus `FAB` has the single defeat `A -> B` and grounded extension `{A}`; `FBA` has the single defeat `B -> A` and grounded extension `{B}`. The attack graph alone is identical and does not determine the extension.

The repaired carrier includes the strict preference (equivalently, the derived defeat relation). The decoder constructs the defeat graph and computes its grounded extension for these two finite cases.

## Scope boundary

Only two arguments, mutual attack, the stated success rule, and grounded semantics are in scope. The example does not adjudicate other preference liftings, attack types, or semantics, and it does not claim that preference is always necessary.
