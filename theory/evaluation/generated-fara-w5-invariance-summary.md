# Generated FARA W5 cross-representation invariance summary

Generated deterministically by `python tools/check_fara_w5_invariance.py --write`.

## Terminal adjudication

Two executable, exactly recoverable, all-six-preserving pairs establish bounded invariance. No admissible same-source pair with different conclusions was produced; representation independence therefore remains unresolved.

## Executed fixture matrix

| Fixture | Pair | S/Sem/O/D/I/H | Recovery | Admissible | Agreement | Classification |
|---|---|---|---|---:|---|---|
| W5-FIX-001 deterministic transitions | lsts ↔ tables | Pass/Pass/Pass/Pass/Pass/Pass | exact | true | True | positive |
| W5-FIX-002 probabilistic information | trs ↔ tables | Pass/Pass/Pass/Pass/Pass/Pass | exact | true | True | positive |
| W5-FIX-003 nonmonotonic revision | logic ↔ traces | Pass/Pass/Pass/Pass/Fail/Pass | partial | false | Unknown | inadmissible_boundary |
| W5-FIX-004 paraconsistent consequence | logic ↔ graphs | Pass/Fail/Pass/Pass/Pass/Pass | partial | false | Unknown | inadmissible_boundary |
| W5-FIX-005 causal intervention | graphs ↔ logic | Pass/Pass/Pass/Pass/Pass/Fail | partial | false | Unknown | inadmissible_boundary |
| W5-FIX-006 changing rules or semantics | trs ↔ traces | Pass/Pass/Pass/Fail/Pass/Pass | partial | false | Unknown | inadmissible_boundary |
| W5-FIX-007 identity merge and deletion | graphs ↔ trs | Pass/Pass/Pass/Pass/Fail/Pass | partial | false | Unknown | inadmissible_boundary |
| W5-FIX-008 provenance-sensitive history | tables ↔ traces | Pass/Fail/Pass/Pass/Pass/Pass | partial | false | Unknown | inadmissible_boundary |
| W5-FIX-009 distributed partial order | lsts ↔ traces | Pass/Pass/Pass/Pass/Pass/Fail | partial | false | Unknown | inadmissible_boundary |
| W5-FIX-010 external oracle dependence | lsts ↔ tables | Unknown/Unknown/Unknown/Unknown/Unknown/Unknown | unknown | false | Unknown | unresolved |
| W5-FIX-011 continuous case | trs ↔ tables | Unknown/Unknown/Unknown/Unknown/Unknown/Unknown | unknown | false | Unknown | unresolved |
| W5-FIX-012 embodied case | graphs ↔ traces | Unknown/Unknown/Unknown/Unknown/Unknown/Unknown | unknown | false | Unknown | unresolved |

## Failed counterexample attempts

- **CE-W5-001 (equivalent-source/different-conclusion):** rejected as inadmissible — the compared trace/logical pair loses information and is not commitment-equivalent
- **CE-W5-002 (inequivalent-source/collapse):** retained as a representation-boundary witness, not an invariance counterexample — source inequivalence violates the same-source requirement
- **CE-W5-003 (representation-dependent-minimality):** rejected as an invariance refutation — the linearized form loses historical partial order
- **CE-W5-004 (decoder-smuggling):** rejected — decoder-held semantics is forbidden hidden machinery
- **CE-W5-005 (circularity):** rejected — equivalence defined by conclusion agreement is circular

## Refuted claims

- shared output establishes semantic invariance
- successful simulation establishes recoverability
- lossy representation pairs refute invariance

## Unresolved claims

- representation independence across the registered families
- oracle-dependent invariance
- faithful finite continuous invariance
- embodied or tacit invariance
- invariance beyond the frozen fixtures

## Explicit nonclaims

- notation invariance implies representational invariance
- simulation implies semantic invariance
- reconstruction implies invariance
- bounded invariance implies universal invariance
- W3 or W4 proves W5
- finite coverage proves representation independence
- inadmissible pairs refute invariance

## Remaining obligations

- produce an exact all-six-preserving same-source pair with different conclusions or retain unresolved
- independent specification and replication of each family
- formal semantic equivalence for nonclassical consequence
- nonfinite recovery theory for continuous systems
- environment-inclusive embodied equivalence
- oracle transcript/live-service boundary adjudication

## Self-review

- negative pairs were reclassified as inadmissible boundaries
- fixture executions now construct encodings and run recovery
- hidden encoding assumptions are charged
- circular equivalence is rejected
- coverage is not population-complete
- reconstruction is not counted as invariance
- no finite-to-universal promotion
- W3 is not consumed and W4 is only a declared boundary dependency
