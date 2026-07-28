# Generated FARA W4 representation boundary summary

Generated deterministically by `python tools/check_fara_w4_representation.py --write`.

## Frozen contract

A declared reasoning system S=(X,R,Sem,Step,Obs,Hist,Ext) with explicit identity criteria and a declared observation interface.

finite_tagged_archive_v1: a finite JSON tree of typed, identity-bearing source records; it is data, not an interpreter, oracle, physical coupling, or proof assistant.

## Registered cases

| ID | Topic | Kind | Preservation S/Sem/O/D/I/H | Recovery | Hidden | Narrowed |
|---|---|---|---|---|---:|---:|
| W4-C01 | changing rule sets | positive | Pass/Pass/Pass/Pass/Pass/Pass | exact | false | false |
| W4-C02 | changing semantic interpretations | positive | Pass/Pass/Pass/Pass/Pass/Pass | exact | false | false |
| W4-C03 | incompatible or evolving ontologies | failure | Partial/Fail/Partial/Fail/Fail/Partial | impossible | false | true |
| W4-C04 | nonmonotonic revision | positive | Pass/Pass/Pass/Pass/Pass/Pass | exact | false | false |
| W4-C05 | paraconsistency | failure | Pass/Fail/Fail/Fail/Partial/Pass | partial | false | false |
| W4-C06 | probabilistic information | positive | Pass/Pass/Pass/Pass/Pass/Pass | exact | false | false |
| W4-C07 | causal and counterfactual structure | failure | Fail/Fail/Partial/Fail/Fail/Unknown | impossible | false | true |
| W4-C08 | continuous state | failure | Partial/Unknown/Partial/Unknown/Fail/Partial | impossible | false | true |
| W4-C09 | embodied or tacit information | unresolved | Partial/Unknown/Fail/Fail/Unknown/Partial | unknown | true | true |
| W4-C10 | external observation or oracle access | failure | Partial/Partial/Fail/Fail/Fail/Partial | partial | true | false |
| W4-C11 | identity-changing merge or quotient operations | failure | Partial/Partial/Pass/Fail/Fail/Fail | impossible | false | true |
| W4-C12 | deletion and constraint relaxation | positive | Pass/Pass/Pass/Pass/Pass/Pass | exact | false | false |
| W4-C13 | provenance-sensitive histories | failure | Partial/Partial/Partial/Fail/Fail/Fail | impossible | false | true |
| W4-C14 | changing rules with hidden interpreter | failure | Partial/Partial/Pass/Fail/Fail/Partial | partial | true | false |

## Strongest bounded result

For any source in the finite explicit contract scope, E is injective up to declared identifier renaming, D(E(S)) is commitment-equivalent to S, and total-table replay preserves full-interface finite traces; therefore the source is losslessly representable under this auxiliary contract.

## Explicit nonclaims

- all reasoning systems are representable
- finite examples prove universal faithfulness
- simulation proves recovery
- behavioral equivalence proves semantic equivalence
- one-way encoding proves bidirectional translation
- unknown is pass
- W1 primitive independence is resolved
- W2 global minimality is established
- W3 evidence is consumed

## Unresolved obligations

- semantic identity across undeclared interpretations
- complete explicit identity criteria for embodied or tacit reasoning
- general infinite, continuous, open-world, or oracle-dependent representation
- any universal lossless-representation theorem
