# External System Investigation — Classical Propositional Logic

Status: provisional

## Purpose

Evaluate whether classical propositional logic, described independently of FAR, can be represented by FAR/FARA without treating representation success as universality or minimality evidence.

## Independent System Description

Classical propositional logic studies truth-functional reasoning over propositional variables and formulas built with connectives such as negation, conjunction, disjunction, implication, and biconditional. Its primary objects are formulas, valuations assigning truth values to propositional variables, truth tables or equivalent semantic clauses, inference rules or proof systems, premises, and conclusions. A formula is valid when it is true under all valuations. A proof system is sound when derivable formulas are semantically valid and complete when semantic validity is derivable.

The scope of this investigation is standard two-valued truth-functional propositional logic, not modal, many-valued, intuitionistic, paraconsistent, relevance, or resource-sensitive variants.

## Assumptions

- The target system is the ordinary bivalent, truth-functional system described in standard logic references.
- Truth-table semantics and rule-based derivations are both admissible evidence for the target reasoning process.
- Metatheorems such as soundness and completeness are not themselves proved here; they are treated as source-described features of the target system.

## Source Evidence

- Primary/standard reference: Stanford Encyclopedia of Philosophy, "Classical Logic", especially the sections describing formal language, semantics, and proof systems; retrieved during this investigation on 2026-07-12.
- Standard textbook evidence: Enderton, *A Mathematical Introduction to Logic*, sections on propositional syntax, truth assignments, and tautological consequence.
- Existing Project FAR contextual evidence: `theory/applications/classical-logic.md`, used only after the independent description.

## Claim Separation

- Syntactic encoding: propositional formulas can be recorded as strings or abstract syntax trees.
- Representability: formulas, valuations, consequence relations, and inference steps can be assigned FAR/FARA roles.
- Faithful representation: the mapping preserves truth-functional semantics and derivability at the scoped level.
- Operational equivalence: a target derivation or truth-table check corresponds to FAR/FARA transitions with the same input formulas and validity result.
- Explanatory adequacy: the mapping explains propositional reasoning as explicit object, structure, interpretation, and rule-governed transformation.
- Universality: not claimed; only this scoped system is evaluated.
- Necessity: component use is reported for this investigation only.
- Minimality: not established; no ablation proof is performed.

## FAR/FARA Representation

| FAR/FARA Component | Target-System Mapping | Notes |
|---|---|---|
| Investigation | Determine whether a conclusion follows from premises or whether a formula is valid. | Scoped to bivalent truth-functional logic. |
| Representation | Propositional variables, formulas, premises, conclusions, valuations, derivation lines. | Formulas may be represented syntactically. |
| Representational Structure | Formula parse trees, premise-conclusion relation, valuation space, derivation dependency graph. | Includes connective arity and subformula structure. |
| Interpretation | Truth-value assignment and truth-functional semantic clauses. | Supplies meaning for connectives and validity. |
| Reasoning Calculus | Truth-table evaluation, semantic consequence checking, and proof rules such as natural deduction or Hilbert rules. | Multiple calculi can be represented as alternatives. |
| Reasoning State | Current formula set, valuation under test, or derivation state. | FARA state is useful for proof or table execution. |
| Transition Signature | Apply connective semantics, extend a derivation, or check next valuation. | Depends on chosen calculus. |
| Candidate | Candidate proof step, candidate valuation, candidate conclusion, or candidate countermodel. | |
| Admissibility Structure (Ω) | Well-formedness constraints, rule applicability, valuation completeness. | |
| Resolution Rule | Accept derivation, reject invalid step, identify satisfying/invalidating valuation, or mark formula valid. | |
| Resolution | The validity, satisfiability, derivability, or non-consequence result. | |

## Preservation Review

### Representation Fidelity

Target: formulas, valuations, proof steps, and validity judgments. Evidence: SEP and textbook descriptions. Preserving element: Representation plus Representational Structure. Procedure: compare each target object type with a mapped FAR/FARA role. Result: `pass`. Justification: no target object requires redefinition; the mapping records formulas, valuations, and derivation artifacts directly.

### Semantic Preservation

Target: bivalent truth-functional semantics and validity as truth under all valuations. Evidence: SEP and textbook semantics. Preserving element: Interpretation. Procedure: correspondence argument between truth assignments/connective clauses and FAR interpretation policy. Result: `pass`. Justification: semantic clauses are explicit interpretation policies; no truth condition is replaced by evaluator stipulation.

### Structural Preservation

Target: recursive formula structure, connective arity, premise-conclusion organization, and derivation dependencies. Evidence: standard syntax and proof-system descriptions. Preserving element: Representational Structure. Procedure: reconstruct a formula parse tree and a proof dependency graph from the mapped structure. Result: `pass`. Justification: subformula and dependency relations are explicit structural relations.

### Operational Preservation

Target: truth-table computation and rule-governed derivation. Evidence: standard truth-table and proof calculi. Preserving element: Reasoning Calculus and FARA transition signature. Procedure: trace a sample rule application or valuation update as a state transition. Result: `pass`. Justification: each operation is a rule over explicit states and representations.

### Dependency Preservation

Target: derivation dependencies and semantic dependence on valuations. Evidence: proof lines cite earlier lines; truth tables evaluate formulas under assignments. Preserving element: Representational Structure and Reasoning State. Procedure: check whether dependencies can be listed and replayed. Result: `pass`. Justification: premise dependencies and valuation dependencies remain explicit.

### Information Preservation

Target: information needed to decide validity or verify derivation correctness. Evidence: formula syntax, connective semantics, valuation, and rule set. Preserving element: all five FAR primitives plus FARA state machinery. Procedure: ask whether a later investigator could reconstruct the target validity check from the report. Result: `pass`. Justification: the mapping does not discard syntax, valuation, rule, or result information required by the scoped objective.

## Required FAR/FARA Components

Required: Investigation, Representation, Representational Structure, Interpretation, Reasoning Calculus. For procedural traces, Reasoning State, Transition Signature, Candidate, Admissibility Structure, Resolution Rule, and Resolution are also required.

## Unused FAR/FARA Components

None are inherently unused when both semantic checking and proof execution are included. A purely static semantic mapping could leave some FARA transition components unused, but this investigation includes operational preservation.

## Alternative Representations Considered

- Pure syntactic encoding of formulas was rejected as insufficient because it would not preserve truth-functional semantics.
- Pure semantic truth-table representation was retained as equivalent for validity checking but insufficient alone to explain proof derivations.
- Proof-system-only representation was retained as scoped but insufficient alone to explain model-theoretic validity unless soundness/completeness is separately cited.

## Potential Counterexamples

- Non-classical logics reject or alter classical principles; these are outside this investigation scope and should be investigated separately.
- Exponential valuation growth creates computational difficulty but not a representational failure.
- Treating a formula string as a FAR representation without semantics would be syntactic encoding only, not faithful representation.

## Counterexample Classification

- Non-classical variants: `outside scope` for this investigation; lower-precedence plausible category is conservative extension pressure for future variant-specific investigations.
- Exponential valuation growth: `not a counterexample`; it pressures efficiency, not primitive sufficiency.
- Formula-only encoding: `not a counterexample` to FAR, but a failed investigation mapping if used as the sole representation.

## Classification

`fits FAR`

## Justification

All required preservation claims pass for standard bivalent propositional logic, and no domain-specific machinery beyond explicit syntax, valuation semantics, and rule calculus is required. Under the classification precedence rule, no outside-scope, candidate primitive failure, unresolved status, or conservative extension pressure remains for the scoped system.

## Limitations

This investigation does not cover non-classical propositional logics, complexity-theoretic performance, proof-search heuristics, or philosophical disputes about material implication.

## Implications

### Universality

Provides one positive in-scope instance for representability and faithful representation. It does not establish universality.

### Necessity

Supports the need, for this system, for representations, structure, interpretation, and calculus. It does not prove those components necessary for all reasoning.

### Minimality

Does not establish minimality. No primitive ablation was performed.

## Confidence

High for the scoped system because the target system is formal, explicit, and stable.

## Remaining Questions

- Whether a single report should separately classify semantic-tableau, natural-deduction, Hilbert, and sequent calculi variants.
- Whether mechanized examples should be added for independent replay.
