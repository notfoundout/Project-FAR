# Deduction-First Research Standard

## Status

Prospective and controlling upon merge.

## Purpose

Project FAR's central question is mathematical:

> Does there exist a common structure instantiated by every reasoning process in the justified scope, and if so, is that structure universal and minimal?

The primary route to an answer is therefore deductive. The central claim must stand or fall on explicit definitions, assumptions, constructions, proofs, countermodels, lower bounds, equivalence results, or impossibility results.

Empirical evaluation, comparative representation experiments, mechanized executions, and independent replication remain valuable. They test interpretation, implementation, robustness, and applicability. They do not create the truth of a mathematical theorem and do not gate construction of a proof.

## Controlling distinction

Project FAR separates two questions.

### Mathematical question

What follows from a declared formal domain, definitions, and axioms?

This question is answered by proof or refutation.

### Verification and application questions

Have the definitions been interpreted consistently? Is the proof correct? Does an implementation satisfy the formal contract? Do independently selected examples fit the stated scope? Can independent researchers reproduce an evaluation?

These questions are answered by proof checking, mechanization, review, replication, adversarial testing, and bounded empirical work.

The verification track may discover an error that invalidates a proof. It does not serve as an axiomatic premise merely because a result is replicated.

## Evidence hierarchy for the central question

For claims of existence, representation, universality within a formal scope, necessity, independence, minimality, uniqueness, equivalence, or impossibility, the repository uses the following order of force:

1. machine-checked proof from frozen definitions and assumptions;
2. complete human-checkable proof from frozen definitions and assumptions;
3. partial proof, lemma, lower bound, or formally stated countermodel;
4. exhaustive result over a fully defined finite universe;
5. mechanized conformance or model checking over a bounded universe;
6. comparative experiment, case study, or replicated evaluation;
7. informal argument or intuition.

A lower item may motivate, challenge, or test a higher item. It may not be reported as logically equivalent to it.

## Primary deductive program

The active central program is:

1. freeze the exact target theorem and justified scope;
2. freeze the formal object class and semantics of reasoning systems;
3. state all assumptions and distinguish definitions from substantive axioms;
4. define faithful representation without FAR-native circularity;
5. resolve whether PB-001, a revision, or another basis supplies the theorem obligations;
6. prove or refute scoped existence and faithful representation;
7. prove lower bounds, primitive independence, or explicit derivability results;
8. prove minimality relative to a declared candidate universe, or state why global minimality is not derivable;
9. characterize equivalence, uniqueness, incomparability, or impossibility;
10. mechanize the proof or the largest sound fragment;
11. invite independent proof review and adversarial counterexample search.

## Required theorem discipline

Every theorem artifact must identify:

- theorem identifier and version;
- exact statement;
- scope and quantified domain;
- imported definitions;
- assumptions and axioms;
- dependencies on prior lemmas;
- proof status;
- machine-check status;
- known countermodels and boundary cases;
- consequences actually established;
- stronger claims not established.

A theorem statement may not quantify over "all reasoning" unless the quantified class is independently and formally defined.

A proof may not hide domain-specific behavior in an unrestricted interpreter, metadata field, oracle, evaluator repair, or representation relation whose own power is left unconstrained.

## Representation theorem requirements

A faithful representation theorem must provide, at minimum:

1. a source class of reasoning systems;
2. a target FARA structure or precisely defined successor;
3. a representation map or constructive existence rule;
4. preserved commitments and an explicit preservation relation;
5. admissibility and transition correspondence;
6. history and dependency preservation where required by the scope;
7. treatment of semantic interpretation and evidential correspondence;
8. nontriviality conditions excluding label-only, lookup-table, hidden-interpreter, and evaluator-repaired encodings;
9. a proof that the construction is defined for every source object in scope;
10. a proof of the declared preservation properties.

If P8 is not an ordinary preservation coordinate, its role must be formalized as an evidence condition, theorem side condition, or separate correspondence theorem. It may not remain an informal qualifier in a completed theorem.

## Necessity and minimality discipline

Necessity and minimality are distinct.

- Primitive necessity requires a proof that removing a primitive prevents the required representation or forces an equivalent commitment under the declared cost/equivalence model.
- Local minimality concerns a frozen candidate vocabulary or architecture.
- Global minimality requires a declared universe of alternatives and a lower-bound or uniqueness theorem over that universe.

Experimental ablation may discover candidate derivations or counterexamples. It does not by itself prove necessity over an unbounded class.

## Counterexample and negative-result priority

A valid countermodel, impossibility theorem, nonrepresentation theorem, or strictly simpler equivalent construction is a central result, not a failure of the project.

The project must preserve:

- failed proof attempts that expose a substantive obstruction;
- minimal counterexamples;
- assumptions required to repair a theorem;
- alternative non-equivalent bases;
- scope restrictions;
- undecidability, incompleteness, or no-go results.

A theorem repaired by changing definitions or scope after a counterexample becomes a new version. The earlier failure remains part of the record.

## Role of PBTS-001 and independent replication

PBTS-001, RUN-001, the independent replication package, and the RUN-001 coordinator controls remain valid repository artifacts.

Their role is secondary:

- test whether PB-001 distinctions are operationally understandable;
- expose ambiguous preservation judgments;
- test evaluator and implementation robustness;
- discover countermodels or missing obligations;
- support bounded claims about reproducibility.

They are not prerequisites for drafting, proving, refuting, or mechanizing the scoped representation theorem.

Independent replication remains required before claiming independent empirical confirmation of PBTS results. It is not required before attempting a mathematical proof.

## Role of external review

External review is an error-detection and confidence mechanism.

Independent reviewers may:

- check definitions and proofs;
- attempt formal reconstruction;
- search for countermodels;
- test mechanized artifacts;
- challenge scope and hidden assumptions.

The theorem's validity depends on whether the proof follows from the assumptions, not on reviewer agreement. Reviewer disagreement may nevertheless reveal an error, ambiguity, or unsupported premise that must be resolved.

## Work admission order

Core work is prioritized as follows:

1. theorem statement and formal scope;
2. definitions, semantics, and axioms;
3. lemmas and constructive mappings;
4. countermodels and impossibility analysis;
5. representation proof or refutation;
6. necessity, independence, and lower bounds;
7. minimality, equivalence, and uniqueness;
8. mechanized proof verification;
9. independent proof review;
10. secondary empirical validation and applications.

Infrastructure enters the active queue only when it directly supports one of these items.

## Claim policy

The repository may claim a theorem only when the proof artifact identifies its assumptions, scope, and dependencies and has passed the applicable proof gate.

The repository may claim independent verification only when the applicable review or replication evidence exists.

These are separate claims. Failure to obtain external replication does not convert a valid proof into a non-proof. A proof defect discovered internally or externally invalidates the theorem claim regardless of replication status.

## Nonclaims

Adopting this standard does not establish:

- that a universal reasoning structure exists;
- that FAR or FARA is that structure;
- that IRD-001 or PB-001 is sufficient or correct;
- that a representation theorem is currently proved;
- that FARA is necessary, independent, minimal, or unique;
- that mechanization or independent proof review has occurred.

It changes the dependency structure of the research program: deduction is primary, and empirical replication is supporting rather than constitutive.