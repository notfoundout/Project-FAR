# Independent process semantics and end-to-end preservation

## Purpose

This layer removes the previous dependence on manually supplied `ProcessSpecification` objects.

`IndependentProcessModel` is defined independently of FAR representation types. It specifies:

- source states and their meanings;
- an initial state;
- terminal-state classification;
- labeled transitions;
- transition closure over the state set;
- an ordered observable trace.

The verified extraction function converts that source model into a `ProcessSpecification`. The canonical FAR constructor then produces a `FARRepresentation`.

## End-to-end theorem

`compileIndependentModel_preserves_behavior` proves preservation from the independent source model through extraction and FAR construction.

The registered preservation contract covers:

- investigation identity;
- entity/state encoding;
- transition structure;
- admissible transition labels;
- ordered observable trace;
- state semantics;
- initial-state marking;
- terminal-state marking.

Initial and terminal status are preserved as an observable encoding in the generated representation content. They are not yet primitive fields of `FARRepresentation`.

## Adversarial rejection

`lossyCompiler` deliberately erases transition relations and transition permissions while retaining a well-typed FAR tuple.

`lossyCompiler_rejected_when_transition_exists` proves that the verifier rejects this compiler for every source model containing at least one transition. Concrete rejection theorems cover all four examples.

## Examples

The complete pipeline is instantiated for four structurally different process families:

1. deductive proof;
2. defeasible legal reasoning;
3. probabilistic belief update and decision;
4. rule-modifying reasoning with an explicit change from an old active rule to a replacement rule.

These examples demonstrate that one compiler and preservation theorem apply across different transition topologies and reasoning styles. They do not prove universal coverage of all reasoning processes.

## Claim boundary

The source models remain formal artifacts written by the project. This layer proves that extraction and FAR construction preserve the observables declared by those models. It does not prove that a source model is empirically correct about an external human, legal, scientific, or software process.

The work also does not establish model-theoretic independence of A1–A5. That requires a separately defined model class and countermodels satisfying all-but-one axiom for each independence claim.
