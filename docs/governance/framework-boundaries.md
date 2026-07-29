# Framework-Boundary Specification

Status: **Accepted architectural specification**

| Layer | Owns | May depend on | Must not claim |
|---|---|---|---|
| foundations | motivation, declared scope/assumptions, grounding records | earlier foundations | validation or methodology as a premise |
| shared theory | common definitions, semantics, operators and scoped formal results | foundations, earlier shared theory | framework procedures as axioms |
| FARA | representational objects, states, transitions, admissibility architecture, and the scoped `FARA-FORMAL-KERNEL-001` carrier/identity/equivalence contract | foundations, shared theory | FAR workflow or FARO operations as primitives; global uniqueness, universality, primitive necessity/minimality, completeness, or unregistered scope expansion from the formal kernel |
| FAR | investigation workflow and selections | foundations, shared theory, FARA | that its procedural choices are FARA theorems |
| FARO | execution, audit, comparison, disagreement and reporting operations | foundations, shared theory, FARA, FAR | that operational choices follow necessarily from FARA/FAR |

The only canonical direction is **foundations → shared theory → FARA → FAR → FARO**. Methodology, validation, research, examples, papers, commercial material, and archive material are downstream evidence, applications, or history. FARE and FARM are support/coordination surfaces and do not alter this chain or own FAR/FARA/FARO primitives.

`FARA-FORMAL-KERNEL-001` is Accepted only for Project FAR v1.0 finite explicit auditable representational architecture. It specifies an identity-bearing many-sorted relational carrier architecture, typed occurrence-sensitive identity, and sort-preserving relational isomorphism as kernel-equivalence. It does not derive FAR methodology, FARO operations, or the seven candidate primitive classifications. Typed-hypergraph and algebraic/state-transition forms remain derived views rather than upstream prerequisites.

Definitions used by several frameworks belong upstream in shared theory. A downstream need may motivate a proposed upstream change, but is not itself a derivation. A stability milestone is a repository state, not proof of necessity, sufficiency, universality, or correctness.
