# PCA-W4 domain-contract results

Status: **COMPLETE AT THE RECORDED FINITE-EXPLICIT SCOPES**

Native freeze commit: `f823c4daf08b61241483bc1cc50d88d22746fa83`

Controlled mapping commit: `8f8ad0a9b18f704a892c8bdb1b5fe304e18aae17`

## Results

| Domain | Deliberately lossy representation | Collision result | Explicit repair | Repair result |
|---|---|---|---|---|
| formal logic | satisfiability bit | `REFUTED`: both theories satisfiable; only one entails `q` | explicit model set over `p,q` | `PROVED` finite factorization |
| Bayesian/causal | observational joint distribution | `REFUTED`: observationally equal; `P(Y=1 | do(X=0))` is `0` vs `1/2` | declared intervention response distribution | `PROVED` finite factorization |
| argumentation | attack graph without preference | `REFUTED`: same mutual attack; grounded extension is `{A}` vs `{B}` | preference and derived defeat graph | `PROVED` finite factorization |
| model-based reasoning | initial output | `REFUTED`: same initial output; `[a]` trace is `[0,0]` vs `[0,1]` | transition and output tables | `PROVED` finite factorization |
| type theory | raw term without context | `REFUTED`: same `x`; `succ x : Nat` succeeds vs fails | raw term plus typing context | `PROVED` finite factorization |
| proof theory | end-sequent | `REFUTED`: same `A |- A`; one derivation contains Cut | explicit derivation tree | `PROVED` finite factorization |

The generic `far-ir/2.0` verifier independently recomputes all 12 encoded collision/factorization claims. The W4 checker additionally reconstructs each native behavior and representation from the case payload, verifies memo/source hashes, enforces the paired contract dimensions, and checks bibliography identity. Mutation tests demonstrate rejection of changed behavior, changed repair data, and changed provenance hashes.

Wolfram independently enumerated the small witnesses. Its first argumentation decoder failed because of a malformed nested pure-function slot; that failed run is retained. The corrected run returned `allCollisions=True` and `allRepairsFactorize=True`. This is internal computational corroboration, not independent domain review.

## Interpretation

Each collision refutes only its named lossy representation under its frozen observation contract. Each repair proves only finite-table sufficiency for the two recorded cases. The repairs are not shown minimal, unique, natural, efficient, or complete for their domains.

The literature supplies independently motivated native comparison dimensions—consequence, intervention response, preference-sensitive defeat, trace behavior, context-indexed typing, and derivation structure. Project FAR selected and encoded the finite witnesses. No external domain expert selected or evaluated the mappings, so this work does not close framing- or evaluator-independence limitations and does not establish novelty or priority.

## Next boundary

`PCA-W5-APPROXIMATION-AND-COST` is next. W4 establishes no approximation metric, tolerance, loss, computational cost order, or universal optimum. `PCA-W6-EMPIRICAL-AUDIT-UTILITY` remains open.
