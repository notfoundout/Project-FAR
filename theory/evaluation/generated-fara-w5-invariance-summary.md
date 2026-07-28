# Generated FARA W5 cross-representation invariance summary

Generated deterministically by `python tools/check_fara_w5_invariance.py --write`.

## Authority recovery

UQ-T4 asks whether FAR/FARA/FARO boundaries remain adequate under representation escape and semantic change; W5 executes the narrower necessary test of whether registered FAR/FARA conclusions are invariant across materially different admissible representations.

**Prompt discrepancy:** No repository artifact names cross-representation invariance as canonical FARA W5. The prompt supplies the W5 label and broader fixture list; repository authority supplies UQ-T4, UQ-T7 and OP-05. This execution is additive and does not rewrite those questions.

## Representation families

- **graphs — directed graphs or hypergraphs:** typed vertices and directed (hyper)edges with explicit edge roles
- **logic — logical theories:** typed signature, formulas, consequence relation, revision/intervention rules
- **lsts — labeled state-transition systems:** states, typed labels, transition relation, observation map
- **tables — table-driven executable models:** finite typed tables for state, rule, step, observation and history
- **traces — event or trace structures:** events, labels, causality/conflict order and observations
- **trs — typed relational structures:** many-sorted carriers, typed relations, interpretation and provenance relations

## Preservation and conclusion-agreement matrix

| Fixture | Pair | S/Sem/O/D/I/H | Recovery | Agreement | Result |
|---|---|---|---|---|---|
| W5-FIX-001 deterministic transitions | lsts ↔ tables | Pass/Pass/Pass/Pass/Pass/Pass | exact | True | positive |
| W5-FIX-002 probabilistic information | trs ↔ tables | Pass/Pass/Pass/Pass/Pass/Pass | exact | True | positive |
| W5-FIX-003 nonmonotonic revision | logic ↔ traces | Pass/Pass/Pass/Pass/Fail/Pass | partial | False | negative |
| W5-FIX-004 paraconsistent consequence | logic ↔ graphs | Pass/Fail/Pass/Pass/Pass/Pass | impossible | False | negative |
| W5-FIX-005 causal intervention | graphs ↔ logic | Pass/Pass/Pass/Pass/Pass/Fail | partial | False | negative |
| W5-FIX-006 changing rules or semantics | trs ↔ traces | Pass/Pass/Pass/Fail/Pass/Pass | impossible | False | negative |
| W5-FIX-007 identity merge and deletion | graphs ↔ trs | Pass/Pass/Pass/Pass/Fail/Pass | partial | False | negative |
| W5-FIX-008 provenance-sensitive history | tables ↔ traces | Pass/Fail/Pass/Pass/Pass/Pass | impossible | False | negative |
| W5-FIX-009 distributed partial order | lsts ↔ traces | Pass/Pass/Pass/Pass/Pass/Fail | partial | False | negative |
| W5-FIX-010 external oracle dependence | lsts ↔ tables | Partial/Unknown/Partial/Partial/Unknown/Unknown | unknown | Unknown | unresolved |
| W5-FIX-011 continuous case | trs ↔ tables | Partial/Unknown/Partial/Partial/Unknown/Unknown | unknown | Unknown | unresolved |
| W5-FIX-012 embodied case | graphs ↔ traces | Partial/Unknown/Partial/Partial/Unknown/Unknown | unknown | Unknown | unresolved |

## Counterexamples

- **CE-W5-001 (equivalent-source/different-conclusion):** nonmonotonic trace retains defeat order while extensional logical closure omits it; revision admissibility differs
- **CE-W5-002 (inequivalent-source/collapse):** causal models with identical observational graph distributions differ under intervention
- **CE-W5-003 (representation-dependent-minimality):** partial-order trace needs no scheduler; LSTS linearization requires one and makes it appear necessary
- **CE-W5-004 (decoder-smuggling):** paraconsistent consequence agrees only when the decoder imports the source consequence policy
- **CE-W5-005 (circularity):** defining equivalence as equal FAR/FARA conclusions makes invariance tautological and is rejected

## Strongest established result

Two frozen finite pairs exhibit bounded invariance, but registered nonmonotonic, causal, partial-order and semantic-policy witnesses produce representation-sensitive conclusions; therefore representation independence is refuted for the registered campaign.

## Refuted claims

- shared output establishes semantic invariance
- successful simulation establishes recoverability
- all registered representations preserve FAR/FARA conclusions
- representation-independent minimality in the registered campaign

## Unresolved claims

- oracle-dependent invariance
- faithful finite continuous invariance
- embodied/tacit invariance
- invariance beyond the frozen families and fixtures

## Explicit nonclaims

- notation invariance implies representational invariance
- simulation implies semantic invariance
- reconstruction implies invariance
- bounded invariance implies universal invariance
- W3 or W4 proves W5
- finite coverage proves representation independence

## Remaining obligations

- independent specification and replication of each family
- formal semantic equivalence for nonclassical consequence
- nonfinite recovery theory for continuous systems
- environment-inclusive embodied equivalence
- oracle transcript/live-service boundary adjudication

## Self-review

- hidden encoding assumptions disclosed per case
- semantic leakage rejected by CE-W5-004
- circular equivalence rejected by CE-W5-005
- fixture coverage is adversarial but not population-complete
- family-native structures checked against superficial renaming
- reconstruction is not counted as invariance
- no finite-to-universal promotion
- W3 is not consumed and W4 is only a declared boundary dependency
