# Framework-Boundary Specification

Status: **Accepted architectural specification**

| Layer | Owns | May depend on | Must not claim |
|---|---|---|---|
| foundations | motivation, declared scope/assumptions, grounding records | earlier foundations | validation or methodology as a premise |
| shared theory | common definitions, semantics, operators and scoped formal results | foundations, earlier shared theory | framework procedures as axioms |
| FARA | representational objects, states, transitions and admissibility architecture | foundations, shared theory | FAR workflow or FARO operations as primitives |
| FAR | investigation workflow and selections | foundations, shared theory, FARA | that its procedural choices are FARA theorems |
| FARO | execution, audit, comparison, disagreement and reporting operations | foundations, shared theory, FARA, FAR | that operational choices follow necessarily from FARA/FAR |

The only canonical direction is **foundations → shared theory → FARA → FAR → FARO**. Methodology, validation, research, examples, papers, commercial material, and archive material are downstream evidence, applications, or history. FARE and FARM are support/coordination surfaces and do not alter this chain or own FAR/FARA/FARO primitives.

Definitions used by several frameworks belong upstream in shared theory. A downstream need may motivate a proposed upstream change, but is not itself a derivation. A stability milestone is a repository state, not proof of necessity, sufficiency, universality, or correctness.
