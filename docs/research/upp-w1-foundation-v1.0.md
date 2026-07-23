# UPP-W1 Formal Foundation v1.0

## Purpose

This workstream defines the typed semantic objects needed by the Universal Proof Program. It does not define the target reasoning class, the full faithfulness contract, the admissible representation universe, machinery closure, RCCD equivalence, or any necessity or sufficiency theorem.

The foundation is deliberately weaker than RCCD. It provides a language in which later workstreams can state and test claims without treating the vocabulary itself as proof.

## Primitive sorts

The foundation includes identifiers, natural-number time indices, commitments, states, transitions, dependencies, history events, reasoning facts, observations, recovery witnesses, and reasoning systems.

These are data sorts, not universal obligations. A later proof may show that a faithful representation requires structure equivalent to some of them, but their presence in this ontology does not establish that result.

## Core distinctions

The following distinctions are frozen because collapsing them would make later theorem statements ambiguous:

1. Identity versus content equality.
2. System state versus an observation of that state.
3. A transition occurring versus a transition being admissible.
4. Dependency versus temporal succession or correlation.
5. Historical occurrence versus an encoding stored in a present state.
6. Representation versus the procedure used to recover facts from it.
7. Failed recovery versus unresolved or inaccessible recovery.
8. Normative status versus empirical occurrence.

## Well-formedness

A foundation instance is well formed only when identifiers are nonempty and globally unique where identity is asserted; references resolve; time indices are nonnegative; history ordering is coherent; dependency endpoints resolve to commitments or reasoning facts; recovered witnesses identify a procedure and output; and evidential Unknown is not silently promoted.

Well-formedness is syntactic and referential integrity. It is not reasoning faithfulness and does not imply RCCD.

## Neutrality discipline

UPP-W1 does not define class membership using RCCD, R1-R5, or their named formulations. The executable module exports a prohibited-term set for the class-neutrality audit in UPP-W2. That lexical control is necessary but not sufficient: UPP-W2 must also detect semantic equivalents and construct loading.

The foundation contains types named `Commitment`, `Transition`, `Dependency`, `HistoryEvent`, and `RecoveryWitness` because the registered theorem must quantify over corresponding candidate facts. This is metalanguage availability, not an assumption that every system possesses all five RCCD obligations.

## Assumption classification

Every downstream assumption must be classified as definitional, logical, computational, normative, empirical, or methodological. A theorem may use an assumption without proving it, but the final audit must expose that dependency rather than report the result as unconditional.

## Executable model

`theory/foundation/upp_foundation_v1.py` provides immutable typed records and deterministic validation. The validation checks referential integrity, history ordering, dependency endpoints, recovery-witness consistency, and the separation between executed transitions and rejected proposals.

The executable model is a reference semantics for artifact construction and tests. Python execution is not the trusted proof kernel for the final theorem. Later workstreams must mechanize central claims in the repository's formal proof layer.

## Downstream interfaces

UPP-W2 may define the target class only using foundation-level, RCCD-independent predicates.

UPP-W3 may define faithfulness obligations over `ReasoningFact`, observations, histories, and recovery results without assuming the RCCD conclusion.

UPP-W4 may define representations and effective procedures that map to these semantic objects.

UPP-W5 and later workstreams may extend representations with charged auxiliary machinery, but may not mutate the semantic meaning of the foundation objects retroactively.

## Result

`typed_foundation_established_without_rccd_entailment`

The sole next action is PR #283, `UPP-W2-CLASS`.
