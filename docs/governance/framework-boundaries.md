# Framework-Boundary Specification

Status: **Accepted architectural specification**

| Layer | Owns | May depend on | Must not claim |
|---|---|---|---|
| foundations | motivation, declared scope/assumptions, and ordinary logical/set/equivalence machinery | earlier foundations | downstream validation or methodology as a premise |
| shared theory | local comparison contracts, typed outcomes, behavior maps, factorization, observational equivalence/quotients, invariance, and boundary theorems | foundations, earlier shared theory | a contract-free primitive inventory or framework procedures as axioms |
| FARA | a selected finite explicit auditable representation target, schema roles, states/transitions when selected, admissibility interfaces, and `FARA-FORMAL-KERNEL-001` | foundations, shared theory | global primitive necessity, unique ontology, universal/minimal architecture, or sufficiency without a contract and factorization proof |
| FAR | contract freezing, representation mapping, factorization/collision audit, contract-relative minimization, common-content protocol, re-presentation attacks, loss and typed terminal reporting | foundations, shared theory, FARA | that every procedural choice is logically forced or that bounded success proves universality |
| FARO | execution, materialization, comparison, disagreement analysis, audit, and reporting | foundations, shared theory, FARA, FAR | that operational choices prove upstream theory or make the contract objective |

The only canonical direction is **foundations → shared theory → FARA → FAR → FARO**. FARE and FARM remain support/coordination surfaces. Methodology, validation, research, examples, papers, software, commercial material, and archive records cannot reverse that direction.

## Terminal classifications

- Object, Property, Relation, Representation, Interpretation, Investigation, and Reasoning Calculus are FARA schema or contract roles, not global primitives.
- Construct, Differentiate, and Restrict are FAR workflow verbs, not a representation-independent operator basis.
- Resolve is a derived application of a declared resolution rule.
- Ω is a derived materialized classification/provenance view; it records results produced by a calculus and does not cause them.
- A reasoning state, transition, or trace is an optional representation whose sufficiency depends on the declared contract.
- `FARA-FORMAL-KERNEL-001` remains Accepted only for finite, explicit, auditable Project FAR v1 records.

All sufficiency and preservation claims concern **contract-relative behavior**. The FARA kernel may intentionally retain distinctions for provenance and audit even when a contract's observational quotient is coarser. That is a declared engineering/cost choice, not global minimality.

Definitions used by several frameworks belong in shared theory. Stability is a maintenance status, not proof of necessity, sufficiency, universality, or correctness.
