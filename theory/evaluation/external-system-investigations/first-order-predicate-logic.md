# External System Investigation — First-Order Predicate Logic

Status: provisional

## Purpose

Evaluate whether standard first-order predicate logic can be represented by FAR/FARA while preserving the distinction between encoding, faithful representation, operational equivalence, universality, necessity, and minimality.

## Independent System Description

First-order predicate logic extends propositional logic with variables, terms, predicates, functions, quantifiers, and domains of discourse. Its primary objects include signatures, terms, formulas, structures or models, variable assignments, axioms, premises, conclusions, and derivations. Semantics evaluate terms and formulas relative to a structure and variable assignment; universal and existential quantifiers range over the model domain. Reasoning procedures include proof calculi and semantic consequence: a conclusion follows from premises when every model satisfying the premises also satisfies the conclusion.

The scope is ordinary single-sorted first-order logic with standard Tarskian semantics. Higher-order quantification, free logic, modal logic, infinitary logic, and non-classical variants are excluded.

## Assumptions

- The target system is explicit first-order logic with a fixed vocabulary, formation rules, model semantics, and derivation rules.
- Domain-specific theories such as groups or arithmetic are treated as first-order applications, not as changes to the logic itself.
- Completeness and compactness metatheorems are not proved in this investigation.

## Source Evidence

- Primary/standard reference: Alfred Tarski, "On the Concept of Following Logically" / logical consequence tradition, for model-based consequence.
- Standard reference: Stanford Encyclopedia of Philosophy, "Classical Logic", sections on first-order language, semantics, and proof systems; retrieved 2026-07-12.
- Standard textbook evidence: Enderton, *A Mathematical Introduction to Logic*, chapters on first-order languages and semantics.
- Existing Project FAR contextual evidence: `theory/applications/first-order-logic.md`, used only after the independent description.

## Claim Separation

- Syntactic encoding: terms and formulas can be stored as strings or trees.
- Representability: vocabulary, terms, formulas, structures, assignments, consequence, and proof steps can be mapped to FAR/FARA roles.
- Faithful representation: the mapping preserves the scoped semantics of satisfaction, quantification, and derivation.
- Operational equivalence: target proof steps or model-evaluation steps correspond to FAR/FARA transitions under stated rules.
- Explanatory adequacy: the mapping explains first-order reasoning through explicit objects, domains, interpretation functions, and derivation/evaluation rules.
- Universality: not claimed.
- Necessity: limited to this investigation.
- Minimality: not claimed.

## FAR/FARA Representation

| FAR/FARA Component | Target-System Mapping | Notes |
|---|---|---|
| Investigation | Determine validity, satisfiability, or consequence for first-order formulas. | |
| Representation | Signature, variables, terms, formulas, premises, conclusions, models, assignments, proof lines. | |
| Representational Structure | Term/formula syntax trees, binding structure, scopes, model domains, relations, functions, proof dependencies. | Binding structure is essential. |
| Interpretation | Model-theoretic interpretation of constants, functions, predicates, equality, and quantifiers. | Tarskian semantics. |
| Reasoning Calculus | Proof rules, semantic consequence checks, model construction, countermodel search, unification where used. | Domain-specific theories are calculus inputs or axioms. |
| Reasoning State | Current formula set, assignment, model, substitution, proof state, or search state. | |
| Transition Signature | Apply inference rule, evaluate a quantifier, extend assignment, instantiate a variable, or construct/refine a model. | |
| Candidate | Candidate proof step, substitution, witness, model, or countermodel. | |
| Admissibility Structure (Ω) | Formation rules, free/bound variable constraints, rule side conditions, model membership. | |
| Resolution Rule | Accept derivation, accept model/countermodel, reject invalid step, or mark unresolved. | |
| Resolution | Validity, satisfiability, derivability, independence from given premises, or countermodel. | |

## Preservation Review

### Representation Fidelity

Target: first-order vocabulary, formulas, models, assignments, and derivations. Evidence: standard syntax/semantics references. Preserving element: Representation and Representational Structure. Procedure: verify every target object type has a corresponding mapped role. Result: `pass`. Justification: no target object is omitted for the scoped standard system.

### Semantic Preservation

Target: satisfaction in a structure under variable assignment, including quantifier domain dependence. Evidence: Tarskian semantics and standard first-order logic references. Preserving element: Interpretation. Procedure: correspondence argument between target interpretation functions and FAR interpretation policy. Result: `pass`. Justification: interpretations, domains, and assignments are explicit rather than implicit.

### Structural Preservation

Target: binding, scope, arity, term composition, formula composition, and model relation/function structure. Evidence: first-order formation rules and model definitions. Preserving element: Representational Structure and Ω. Procedure: attempt reconstruction of free-variable status and quantifier scope from the FAR/FARA structure. Result: `pass`. Justification: binding and arity must be recorded, but they fit as structure and admissibility conditions.

### Operational Preservation

Target: inference rules and semantic-evaluation steps. Evidence: proof-calculus and model-evaluation descriptions. Preserving element: Reasoning Calculus and Transition Signature. Procedure: trace universal instantiation, existential witness handling, or satisfaction recursion as transitions. Result: `pass`. Justification: operational rules are explicit transformations over formulas, assignments, or proof states.

### Dependency Preservation

Target: premise dependencies, variable-assignment dependencies, theory axioms, and model-domain dependencies. Evidence: proof and semantic consequence definitions. Preserving element: Representational Structure and Reasoning State. Procedure: list dependencies required for an inference or satisfaction claim. Result: `pass`. Justification: dependencies are representable explicitly.

### Information Preservation

Target: information required to verify formula well-formedness, semantic satisfaction, and proof-step correctness. Evidence: syntax, semantic, and calculus references. Preserving element: all five FAR primitives plus FARA operational components. Procedure: check whether a later investigator can replay a proof/evaluation if vocabulary, model, assignment, and rule set are included. Result: `pass`. Justification: no essential scoped information is lost.

## Required FAR/FARA Components

Required: all five FAR primitives. FARA components are required for explicit proof search, model checking, or countermodel construction traces.

## Unused FAR/FARA Components

No FARA component is unused for operational investigations. Static semantic classification can omit some state-transition detail, but operational equivalence requires it.

## Alternative Representations Considered

- Treating quantifiers as textual operators only was rejected because it loses domain semantics.
- Representing only proof derivations was retained as a scoped alternative but does not by itself preserve model-theoretic consequence.
- Representing only model semantics was retained as a scoped alternative but does not by itself preserve syntactic proof procedures.

## Potential Counterexamples

- Henkin semantics, free logic, and higher-order logic alter the semantic domain or quantification target and are outside this report.
- Undecidability of first-order validity creates computational limits but not a representation failure.
- Ambiguous variable binding would be an investigation defect if binding structure is not recorded.

## Counterexample Classification

- Non-standard variants: `outside scope`; lower-precedence plausible category is conservative extension pressure for separate investigations.
- Undecidability: `not a counterexample`; it limits decision procedures, not representation.
- Missing binding data: `not a counterexample` to FAR, but a failed mapping if an investigator omits required structure.

## Classification

`fits FAR`

## Justification

The scoped target system's objects, semantic interpretation, structural dependencies, and operational rules map directly to the five primitives and FARA state machinery. No preservation dimension fails, and no extension beyond target-system-specific syntax and rule content is required.

## Limitations

The investigation does not evaluate higher-order logic, proof assistant implementations, theorem-prover heuristics, model-theoretic metatheorems, or philosophical objections to Tarskian consequence.

## Implications

### Universality

Adds a positive case for a highly general formal reasoning system. It does not prove universality.

### Necessity

The case supports the practical need for all five primitives when both syntax, semantics, structure, and rule-governed consequence are in scope.

### Minimality

No minimality claim follows. Ablation would be required to show a primitive cannot be removed.

## Confidence

High for ordinary first-order logic because the target system is formal and well documented.

## Remaining Questions

- Whether separate reports should cover many-sorted logic, free logic, infinitary logic, and Henkin semantics.
- Whether mechanized replay examples should be added for representative quantified derivations.
