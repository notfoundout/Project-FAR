# Expanded Fixture Analysis for v0.3.0 Reasoning Systems

Status: Provisional v0.3.0 evidence analysis.

Scope: This document analyzes only the ten expanded v0.3.0 reasoning-system fixtures. The v0.2.0 conclusions remain a frozen baseline and are not rewritten here.

Primitive-counterexample standard: a system is a genuine primitive counterexample only if it performs explicit reasoning and the missing capability cannot be represented by Investigation, Representation, Representational Structure, Interpretation, Reasoning Calculus, any derived concept, or conservative extension of Interpretation, Reasoning Calculus, or Representational Structure.

## Summary

No expanded v0.3.0 fixture demonstrates a genuine primitive counterexample. Eight systems are conservative extensions because they require specialized interpretation, structure, calculus, or derived vocabulary. Theorem provers and SAT solving fit FAR directly. The recurring pressure points are indexed semantics, constraint-governed transitions, and mode-relative admissibility; these are registered as D-033 through D-035 rather than as a sixth primitive.

## Modal Logic

### Overview
Modal logic reasons about necessity, possibility, and related operators over worlds or states connected by accessibility relations.

### Reasoning characteristics
The fixture uses propositions evaluated relative to accessible worlds. The characteristic reasoning move is from a claim at one world plus an accessibility/modal rule to a modal conclusion.

### Primitive mapping
- Investigation: determines whether modal consequence can be established across accessible alternatives.
- Representation: modal formulas, worlds, accessibility claims, and modal conclusions are explicit represented items.
- Representational Structure: the accessibility relation organizes worlds and determines which represented alternatives are relevant.
- Interpretation: truth is assigned relative to a world and accessibility frame rather than absolutely.
- Reasoning Calculus: modal introduction, elimination, necessitation, and frame-sensitive rules govern admissible transitions.

### Required derived concepts
D-033 Indexed Interpretation and D-035 Modalized Admissibility.

### Classification
Conservative extension.

### Justification
World-relativity puts pressure on Interpretation, but it does not require a new primitive because the index is a structural parameter and the modal truth condition is an interpretation policy. Frame rules are calculus policies. The missing capability is therefore representable by extending Interpretation and Reasoning Calculus.

### Confidence
Medium.

### Remaining open questions
Which modal systems require separate calculus profiles, and whether unusual neighborhood or impossible-world semantics require additional derived concepts.

## Temporal Logic

### Overview
Temporal logic reasons over ordered times, states, or paths using operators such as next, eventually, always, and until.

### Reasoning characteristics
The fixture evaluates a proposition at a current time and derives a claim about a successor time under a preservation or transition rule.

### Primitive mapping
- Investigation: determines whether a time-indexed conclusion follows from temporal premises.
- Representation: temporal formulas, moments, paths, and operator applications are represented explicitly.
- Representational Structure: order, successor, branching, or path relations structure temporal positions.
- Interpretation: truth is evaluated at temporal indices or along paths.
- Reasoning Calculus: temporal transition rules and operator rules determine admissible moves.

### Required derived concepts
D-033 Indexed Interpretation and D-035 Modalized Admissibility.

### Classification
Conservative extension.

### Justification
The pressure is temporal indexing and path dependence. Both are representational structure plus indexed interpretation. Temporal proof rules are calculus rules, so no sixth primitive is indicated.

### Confidence
Medium.

### Remaining open questions
Whether fairness, liveness, and infinite path conditions need a separate derived concept or are already covered by existing infinite-reasoning and trace concepts.

## Deontic Logic

### Overview
Deontic logic reasons about obligations, permissions, prohibitions, norm conflicts, and contrary-to-duty cases.

### Reasoning characteristics
The fixture treats normative statuses as explicit claims governed by norm accessibility, priority, conflict, and repair policies.

### Primitive mapping
- Investigation: determines what is obligatory, permitted, forbidden, or normatively resolved.
- Representation: norms, actions, obligations, permissions, violations, and conclusions are explicit representations.
- Representational Structure: norm-dependency, priority, exception, and conflict relations organize normative claims.
- Interpretation: formulas receive normative meanings rather than purely alethic truth meanings.
- Reasoning Calculus: deontic inference, conflict-resolution, priority, and contrary-to-duty rules govern transitions.

### Required derived concepts
D-033 Indexed Interpretation and D-035 Modalized Admissibility.

### Classification
Conservative extension.

### Justification
Deontic pressure arises when normative status is not simple truth. FAR can represent that status by Interpretation and can represent norm conflicts by structure and calculus. Because conflict handling can be conservative in the same way as the v0.2.0 paraconsistent case, no primitive counterexample is present.

### Confidence
Medium.

### Remaining open questions
How many deontic conflict policies should be distinguished before analysis becomes system-specific rather than primitive-sufficiency evidence.

## Intuitionistic Logic

### Overview
Intuitionistic logic treats truth through constructive proof and rejects unrestricted excluded middle.

### Reasoning characteristics
A conclusion is admissible only when a construction or proof object is available under the current context.

### Primitive mapping
- Investigation: determines whether a constructive proof of the target exists.
- Representation: propositions, contexts, assumptions, proof objects, and judgments are explicit representations.
- Representational Structure: proof-dependency and context-extension relations organize constructions.
- Interpretation: propositions are interpreted by construction/proof conditions rather than classical bivalence.
- Reasoning Calculus: introduction, elimination, normalization, and constructive admissibility rules govern derivation.

### Required derived concepts
D-033 Indexed Interpretation and D-035 Modalized Admissibility.

### Classification
Conservative extension.

### Justification
The absence of unrestricted excluded middle is not a missing primitive; it is a different admissibility policy in Reasoning Calculus and a constructive Interpretation. Proof objects remain representations, and proof dependencies remain structure.

### Confidence
Medium.

### Remaining open questions
Whether higher-order constructive systems should be analyzed together with type theory or as separate expanded fixtures.

## Fuzzy Logic

### Overview
Fuzzy logic reasons with graded truth values and threshold-sensitive inference rather than binary truth alone.

### Reasoning characteristics
The system assigns degrees to propositions and derives conclusions using degree-combining rules.

### Primitive mapping
- Investigation: determines a degree-valued conclusion or whether a threshold is met.
- Representation: propositions, degree assignments, thresholds, and conclusions are explicit represented items.
- Representational Structure: ordering, aggregation, and dependency relations connect degrees and formulas.
- Interpretation: semantic values are degrees in an ordered scale rather than only true/false.
- Reasoning Calculus: t-norm, implication, aggregation, and threshold rules govern valid transitions.

### Required derived concepts
D-033 Indexed Interpretation and D-035 Modalized Admissibility.

### Classification
Conservative extension.

### Justification
Degree-valued semantics pressures Interpretation, but FAR does not require Interpretation to be bivalent. Calculus rules can transform degrees explicitly. Thus fuzzy reasoning is conservative over the primitives.

### Confidence
Medium.

### Remaining open questions
Which families of many-valued calculi should be treated as separate fixtures, and whether probabilistic and fuzzy degree semantics should remain distinct derived patterns.

## Causal Reasoning

### Overview
Causal reasoning uses causal graphs, interventions, counterfactual changes, and effect estimation.

### Reasoning characteristics
The fixture represents variables and causal relations, then applies an intervention/update rule to infer causal effects.

### Primitive mapping
- Investigation: determines whether an effect follows under an intervention or causal model.
- Representation: variables, graph nodes, edges, interventions, observations, and effect claims are explicit representations.
- Representational Structure: directed causal graphs and dependency relations organize variables.
- Interpretation: edges and interventions receive causal/counterfactual meaning, not merely correlational meaning.
- Reasoning Calculus: do-calculus, graph surgery, adjustment, or counterfactual update rules govern transitions.

### Required derived concepts
D-034 Constraint Transition System.

### Classification
Conservative extension.

### Justification
Causal direction and intervention are specialized structure and calculus. The counterfactual meaning is an Interpretation extension. Since all causal moves can be recorded as explicit graph transformations or model updates, no new primitive is required.

### Confidence
Medium.

### Remaining open questions
Whether hidden variables and statistical identifiability require a separate derived concept or are covered by candidate, admissibility, and constraint-transition vocabulary.

## Type Theory

### Overview
Type theory reasons about terms, types, contexts, judgments, and derivations.

### Reasoning characteristics
The fixture derives a typing judgment from context membership by applying a typing rule.

### Primitive mapping
- Investigation: determines whether a judgment is derivable in a context.
- Representation: terms, types, contexts, rules, judgments, and derivation objects are explicit representations.
- Representational Structure: context membership, dependency, binding, and context-extension relations organize terms and assumptions.
- Interpretation: judgments are interpreted as type assignment, construction, or propositions-as-types statements.
- Reasoning Calculus: typing, formation, introduction, elimination, conversion, and substitution rules govern transitions.

### Required derived concepts
D-033 Indexed Interpretation and D-034 Constraint Transition System.

### Classification
Conservative extension.

### Justification
Contexts and dependency create pressure on representational structure, and judgments create pressure on interpretation. Both are explicit and rule-governed. Because typing derivations are calculus-governed transitions over representations, type theory does not force a sixth primitive.

### Confidence
Medium.

### Remaining open questions
How dependent types, universes, equality reflection, and normalization should be separated in later stress fixtures.

## Theorem Provers

### Overview
Theorem provers produce or check formal derivations using proof states, tactics, kernels, and certificates.

### Reasoning characteristics
The fixture starts with a goal, applies a tactic or rule, and accepts a certificate only if kernel rules validate it.

### Primitive mapping
- Investigation: determines whether a theorem has a valid mechanically checkable proof.
- Representation: goals, lemmas, tactics, proof states, certificates, and kernel responses are represented explicitly.
- Representational Structure: proof-state dependency graphs organize subgoals, lemmas, and certificate dependencies.
- Interpretation: proof statements are interpreted in the object logic implemented by the prover.
- Reasoning Calculus: kernel inference rules and tactic-expansion rules govern admissible transitions.

### Required derived concepts
D-034 Constraint Transition System is useful but not required for direct fixture coverage.

### Classification
Fits FAR.

### Justification
Theorem-prover reasoning is a direct FAR instance: proof traces are representations, proof-state dependencies are structure, object-logic semantics provide interpretation, and the kernel supplies calculus. Variation among proof assistants changes the calculus profile, not the primitive inventory.

### Confidence
High.

### Remaining open questions
Opaque automation inside tactics should be treated like the v0.2.0 opaque-oracle boundary unless proof certificates or traces are available.

## SAT Solving

### Overview
SAT solving determines whether a Boolean formula has a satisfying assignment or proves unsatisfiability through certificates.

### Reasoning characteristics
The fixture verifies that an assignment satisfies each clause of a CNF formula.

### Primitive mapping
- Investigation: determines satisfiability or unsatisfiability of a Boolean constraint system.
- Representation: formulas, variables, literals, clauses, assignments, conflicts, learned clauses, and certificates are explicit representations.
- Representational Structure: clause-variable incidence, implication graphs, and conflict graphs organize search dependencies.
- Interpretation: Boolean valuation semantics assigns truth values to formulas under assignments.
- Reasoning Calculus: DPLL, CDCL, resolution, propagation, decision, backtracking, and certificate-checking rules govern transitions.

### Required derived concepts
D-034 Constraint Transition System is useful but not required for the simple assignment-check fixture.

### Classification
Fits FAR.

### Justification
SAT is explicit constraint reasoning. Even when solver heuristics are complex, a certificate or trace maps to FAR. Search strategy affects calculus efficiency but not primitive sufficiency.

### Confidence
High.

### Remaining open questions
Uncertified black-box SAT answers should be classified under the opaque assertion boundary until a trace or certificate is available.

## Category-Theoretic Reasoning

### Overview
Category-theoretic reasoning uses objects, morphisms, diagrams, composition, commutativity, functors, naturality, and universal properties.

### Reasoning characteristics
The fixture reasons from diagrammatic structure and universal-property conditions to a categorical conclusion.

### Primitive mapping
- Investigation: determines whether a diagram commutes or a universal-property conclusion follows.
- Representation: objects, morphisms, diagrams, equations, cones, functors, and universal-property claims are explicit representations.
- Representational Structure: source/target, composition, commutativity, and diagram relations organize categorical objects.
- Interpretation: categorical semantics assigns meaning to arrows, diagrams, and universal properties.
- Reasoning Calculus: composition, identity, diagram chase, naturality, and universal-property rules govern transitions.

### Required derived concepts
D-034 Constraint Transition System.

### Classification
Conservative extension.

### Justification
Diagrammatic reasoning places pressure on representational structure because relations among arrows carry much of the content. FAR already has Representational Structure for such relations, and categorical inference rules are Reasoning Calculus. Universal properties are structured admissibility conditions, not a sixth primitive.

### Confidence
Medium.

### Remaining open questions
Whether higher categorical coherence data require another derived concept or can remain complex representational structure.

## Cross-System Pressure Points

1. Indexed semantics appears in modal, temporal, deontic, intuitionistic, fuzzy, and type-theoretic reasoning. This supports D-033 and D-035.
2. Constraint-governed transitions appear in SAT, causal reasoning, type theory, theorem provers, and category-theoretic reasoning. This supports D-034.
3. Opaque automation is not a new v0.3.0 counterexample; it reuses the v0.2.0 explicit-reasoning scope boundary. When traces or certificates are absent, the system is outside FAR scope as explicit reasoning evidence until made inspectable.

## Counterexample Assessment

None of the expanded fixtures satisfies the counterexample standard. Each pressure point can be represented by existing primitives, by the new derived concepts D-033 through D-035, or by conservative extensions of Interpretation, Reasoning Calculus, and Representational Structure.
