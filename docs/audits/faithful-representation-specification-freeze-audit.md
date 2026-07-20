# Faithful Representation Specification Freeze Audit

## Audit target

This audit covers the prospective freeze of:

- `docs/research/faithful-representation-specification-v1.0.md`;
- `theory/evaluation/faithful-representation-specification-v1.0.json`;
- premise-ledger revision `THM-TARGET-001-PREMISES` v1.1;
- the corresponding RG-09 and RG-10 gate transitions.

## Audit question

Does the change complete the formal meaning of faithful representation for `THM-TARGET-001` without assuming that FARA satisfies the definition or promoting any theorem claim?

## Result

**Pass prospectively.**

The change freezes a theorem-facing predicate suitable for construction, countermodel, and proof work. It does not provide a representation witness, uniform constructor, proof, mechanization, or independent review.

## Scope integrity

The specification preserves the frozen source and target boundaries:

- source theorem scope remains `S_core`;
- broader `S_IRD` remains an extension target;
- target interface remains `A_FARA`;
- witness signature remains `W=(E,D,M,iota,kappa)`;
- theorem family remains unchanged;
- P8 alternatives remain exactly `coordinate`, `side_condition`, and `split`;
- no FARA primitive is added or declared necessary.

## Formal obligations added

The specification makes the prior signatures exact by registering:

1. a source-owned materiality, value-equivalence, and applicability contract;
2. finite typed source reducts for P1 through P7;
3. target-only deterministic recovery with no source identifier, evaluator, external narrative, or hidden oracle;
4. total typed source-target correspondence;
5. element injectivity and material-sort distinction;
6. relation preservation and reflection;
7. source-declared attribute equivalence, with exact equality as default;
8. finite labeled or finite labeled probabilistic bisimulation for P5;
9. order embedding plus revision, provenance, and path reflection for P7;
10. semantic agreement without lexical-label shortcuts or semantic strengthening;
11. cross-axis coherence;
12. one fixed source-isomorphism-equivariant constructor family;
13. compositional accountability where the source declares a decomposition;
14. a finite complete machinery dependency graph;
15. formal negative-control failure locations;
16. the complete parameterized `Faithful_{m_8}` conjunction.

## Anti-triviality assessment

The definition does not accept output equality, arbitrary decodability, or vocabulary labels as sufficient.

The following loopholes are explicitly blocked:

- output-only lookup;
- dependency collapse;
- history erasure;
- hidden rule modification;
- label-only semantics;
- unrestricted interpreters;
- hidden auxiliary state;
- provenance deletion;
- output-equivalent process substitution;
- primitive or metadata smuggling;
- evaluator repair;
- incoherent per-axis encodings.

Formal rejection of all possible invalid representations is not claimed. The registered control families still require proof lemmas.

## Premise-ledger assessment

`PRM-011` and `PRM-012` are revised from incomplete signatures to `semantics_frozen_unproved_satisfiability`.

The revision does not convert either entry into an axiom or theorem. Open items remain:

- P8 mode selection;
- reconstruction class for necessity;
- candidate universe and equivalence relation for minimality.

No substantive axiom asserting FARA adequacy, PB-001 completeness, primitive necessity, minimality, or universal structure is introduced.

## Gate assessment

The following transitions are justified as artifact-completion gates:

- RG-09 `premise-ledger-and-semantics`: `satisfied`;
- RG-10 `faithful-representation-definition`: `satisfied`.

The following remain closed:

- RG-11 scoped representation proof;
- RG-12 primitive lower bounds;
- RG-13 minimality universe and proof;
- RG-14 mechanized proof verification;
- RG-15 independent proof review.

A satisfied definition gate means that the required formal definition exists and is registered. It does not mean that the predicate is satisfiable or that FARA satisfies it.

## P8 assessment

All three P8 clauses are frozen, but no mode is selected.

This is internally consistent because the faithful predicate is a parameterized family. `THM-CORE-REP-001` remains blocked by `p8_resolution` and unproved.

The next versioned artifact must select one mode or register a target defect. A new fourth mode or content-changing alteration requires a theorem-target and faithful-specification revision.

## Claim audit

No central claim is promoted.

The repository still does not establish:

- existence of a common reasoning structure;
- a uniform FARA constructor;
- satisfiability of `Faithful_{m_8}`;
- faithful representation of `S_core` or `S_IRD`;
- PB-001 sufficiency or completeness;
- universality;
- necessity;
- minimality;
- equivalence or uniqueness;
- impossibility;
- machine verification;
- independent proof review.

## Machine enforcement

`tools/check_faithful_representation.py` checks:

- required artifacts and identifiers;
- source-contract ownership and closure;
- P1-P7 reduct registration;
- recovery restrictions;
- preservation and reflection requirements;
- semantic and cross-axis constraints;
- all three frozen P8 clauses;
- uniformity, composition, and machinery accounting;
- NC-01 through NC-10 diagnostic mapping;
- gate and premise-ledger integration;
- continued absence of a proof claim.

The checker is wired into `make research-check`, `make health-fast`, and `make health`.

## Next action

Freeze the P8 theorem-role decision. After selection, create the `S_core` construction-and-obstruction lemma ledger and prove formal negative-control lemmas alongside constructive work.
