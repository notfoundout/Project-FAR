# Central Research Program

## Purpose

Project FAR exists to determine whether there is a universal and minimal structure underlying reasoning.

This document defines the primary research program governing the long-term direction of the project. It establishes the central question, the admissible routes to an answer, the current formal stage, and the criteria by which success is judged.

Every theoretical development, mechanization effort, proof, external validation, implementation, and supporting framework should contribute directly or indirectly to this program.

## Why?

The purpose of Project FAR is not merely to construct a reasoning framework. Its purpose is to answer a foundational question about reasoning itself.

Without an explicit central program, the project risks improving FAR as an artifact without determining whether FAR accurately represents the phenomenon it was created to investigate. Infrastructure, implementation, case accumulation, and administration may support the research objective but may not replace it.

## Scope

This document governs the project's primary research direction.

It does not introduce new mathematical primitives, accept a theorem, revise Foundation v1.0, or declare FAR correct. Substantive mathematical change still requires the applicable Foundation Revision, Theory Revision, or Research Investigation process.

## Governing standards

This program is controlled by:

- `docs/governance/deduction-first-research-standard.md`;
- `docs/governance/anti-self-validation-standard.md`;
- `docs/governance/anti-self-validation-deduction-clarification.md`;
- `docs/governance/evidence-replication-and-freeze-standard-v1.0.md`;
- `docs/governance/research-priority-reset.md`;
- `docs/research/thm-target-001-v1.0.md`;
- `theory/evaluation/research-gates.json`.

The deduction-first standard controls the dependency between proof and empirical validation. Anti-self-validation and replication standards continue to control claims of independent confirmation.

## Design rationale

Project FAR is fundamentally a research project. The framework exists because of the question, not the other way around.

The central question is mathematical once its source class, target class, semantics, and assumptions are fixed. The primary route to an answer is therefore deduction: explicit definitions, axioms, lemmas, constructions, countermodels, lower bounds, equivalence results, and impossibility results.

Experiments and replication remain important because they can expose ambiguous definitions, implementation defects, hidden assumptions, omitted cases, or human interpretation failures. They support the proof program but do not serve as a logical premise merely because evaluators agree.

The program is neutral among favorable and unfavorable outcomes. A proof that FAR works, a counterexample showing it fails, a theorem establishing only a bounded scope, multiple incomparable structures, or a no-go result are all legitimate central results.

## Central research question

> Does every reasoning process necessarily instantiate a common underlying structure, and if so, is that structure both universal and minimal?

This question contains distinct obligations:

1. whether a common structure exists;
2. whether every reasoning process in a formally justified scope can be faithfully represented;
3. whether each retained commitment is necessary;
4. whether the complete structure is minimal within a declared candidate universe;
5. whether successful structures are unique, equivalent, or incomparable;
6. whether a universal finite structure is impossible under some assumptions.

These obligations must not be collapsed into one favorable claim.

## Research position

Project FAR treats the existence of a universal structure of reasoning as an open hypothesis.

The project does not assume that such a structure exists. It does not assume that FAR or FARA is that structure. A result against the current framework is a valid research result when established by proof, countermodel, bounded exhaustive analysis, or rigorous supporting evidence.

No accepted artifact is protected from criticism merely because it supports the current framework.

## Frozen theorem target

`THM-TARGET-001` v1.0 is the current theorem-family boundary.

It separates:

- `S_core`, the finite explicit IRD-001 source class used for the first exact theorem attempt;
- `S_IRD`, the broader extension class;
- the theorem-facing FARA interface `A_FARA`;
- the representation-witness signature;
- P1-P7 preservation obligations;
- P8 as an unresolved theorem parameter;
- common-schema, faithful-representation, extension, necessity, minimality, equivalence, and impossibility theorem families.

Freezing this target establishes a stable proposition for proof or refutation. It does not establish that the proposition is true, satisfiable, machine checked, or independently verified.

A material change to source scope, target structure, theorem family, representation-witness requirements, P8 content, or failure conditions requires a new target version.

## Primary research objectives

### Objective I — Formal existence

Determine whether a common structure exists for a precisely defined class of reasoning systems.

An existence result must state its assumptions and scope. Failure may be established by an obstruction, countermodel, inconsistency, or impossibility theorem.

### Objective II — Faithful representation

If a candidate structure exists, determine whether every source system in the declared scope admits a faithful representation without ad hoc theory change, unrestricted hidden interpretation, evaluator repair, or loss of protected commitments.

A representation result must define the source class, target class, representation relation, preservation obligations, recovery procedure, semantic agreement, and all counted machinery.

### Objective III — Necessity and independence

Determine whether every retained primitive or preservation commitment is indispensable, derivable, replaceable, scope-dependent, or unnecessary.

Experimental ablation may discover candidate dependencies. Necessity requires a deductive lower bound or equivalent proof over the declared reconstruction class.

### Objective IV — Minimality

Determine whether the structure is irreducible within a declared universe of alternatives and an explicit equivalence or cost relation.

Local minimality, bounded minimality, and global minimality are different claims. Global minimality may not be claimed from a finite comparison unless the candidate universe is proved exhaustive.

### Objective V — Equivalence, uniqueness, and impossibility

Characterize whether successful structures are unique up to isomorphism or translation, form multiple equivalent classes, remain incomparable, or cannot be finite and universal under stated assumptions.

## Primary deductive method

The active central method is:

1. preserve the frozen theorem family and quantified scope;
2. complete the premise and semantics ledger;
3. formalize faithful representation and nontriviality;
4. resolve the role of semantic and evidential correspondence, including P8;
5. construct mappings and prove preservation lemmas for `S_core`;
6. search concurrently for obstruction lemmas and countermodels;
7. prove or refute the finite-core representation theorem;
8. determine whether the result extends to `S_IRD`;
9. establish primitive independence, derivability, or lower bounds;
10. establish minimality, equivalence, uniqueness, incomparability, or impossibility within a declared universe;
11. mechanize the largest sound theorem fragment;
12. obtain independent proof review and adversarial counterexample search.

The canonical detailed sequence is `docs/planning/deduction-first-proof-roadmap.md`.

## Current active stage

The formal-theorem-target gate is satisfied through:

- `docs/research/thm-target-001-v1.0.md`;
- `theory/evaluation/thm-target-001.json`;
- `theory/evaluation/thm-target-001-premise-ledger.json`.

The premise-ledger-and-semantics gate remains in progress.

The immediate central task is to formalize:

- `Pres_1` through `Pres_7`;
- `Faithful_m8`;
- typed source-target encoding;
- admissible recovery;
- semantic agreement;
- transition and admissibility correspondence;
- dependency, consequence, and history preservation;
- uniformity and compositionality;
- complete machinery accounting.

P8 must then be resolved as `coordinate`, `side_condition`, or `split`, or registered as a theorem-target revision blocker.

No construction proof may be accepted before those semantics and the P8 role are frozen.

## Theorem discipline

Every theorem artifact must identify:

- theorem identifier and version;
- exact statement;
- quantified domain and scope;
- definitions and axioms used;
- dependency lemmas;
- proof or refutation status;
- machine-check status;
- known countermodels and boundary cases;
- consequences actually established;
- stronger nonclaims.

A theorem may not quantify over all reasoning unless the quantified class is independently and formally defined.

A representation theorem may not hide missing structure in an unrestricted interpreter, oracle, metadata field, lookup table, evaluator repair, or unconstrained representation relation.

A proof over `S_core` may not be reported as a proof over `S_IRD`.

## Supporting empirical method

Where useful, the project may:

1. freeze vocabulary-neutral source observations;
2. register positive and negative controls;
3. execute comparative representations;
4. perform primitive ablations and bounded searches;
5. test implementations and proof artifacts;
6. seek independent replication;
7. preserve complete result distributions, failures, and nonclaims.

These activities may reveal counterexamples, ambiguity, hidden assumptions, implementation defects, or scope pressure. Their conclusions remain bounded by their design.

They do not gate drafting, proving, refuting, or mechanizing a theorem. Independent replication gates only claims of independent empirical confirmation.

## Evidence hierarchy

For mathematical claims, evidence is ordered by force as follows:

1. machine-checked proof from frozen assumptions;
2. complete human-checkable proof;
3. partial proof, lemma, lower bound, or formal countermodel;
4. exhaustive result over a fully defined finite universe;
5. bounded mechanized conformance or model checking;
6. comparative experiment or independently replicated evaluation;
7. informal argument or intuition.

Lower-ranked evidence may motivate or challenge a proof but may not be described as logically equivalent to it.

Formal proof supports only the propositions and assumptions it actually establishes. Mechanization demonstrates only what the formal encoding and trusted kernel establish. Case studies and replication provide bounded evidence. Failure to discover a counterexample does not prove universality.

## Counterexample policy

Potential counterexamples are primary research objects and must not be dismissed merely because they pressure the current theory.

Each candidate must be classified as one of:

- **Formal Countermodel** — satisfies the frozen source definition and violates the proposed theorem conclusion;
- **Impossibility Witness** — supports a no-go or lower-bound result under stated assumptions;
- **Representation Failure** — the attempted mapping fails, but framework failure has not been established;
- **Interpretation Dispute** — the outcome depends on unresolved semantics or reconstruction;
- **Scope-Boundary Case** — lies outside a previously and independently justified scope;
- **Non-Reasoning Process** — fails the independently stated source definition;
- **Inconclusive** — available information does not support a stable classification;
- **Successfully Represented** — required commitments are preserved without protected-theory change.

A candidate may not be excluded by redefining reasoning after exposure. Any scope restriction must be versioned and defended independently.

## Theory revision policy

Protected Foundation and theory artifacts must not be modified silently.

If a proof attempt or countermodel requires mathematical change, it must enter an explicit revision process. A revised theorem, source class, preservation basis, target structure, or P8 treatment becomes a new version. Earlier failed or weaker versions remain part of the record.

Documentation, repository restructuring, terminology cleanup, or mechanization changes may not conceal substantive theoretical revision.

## Relationship to mechanization

Mechanization formalizes definitions and proofs, exposes missing assumptions, checks derivations, and supports reproducible counterexample analysis.

A proof assistant can provide strong verification when the theorem and assumptions are faithfully encoded. It does not erase questionable axioms, circular definitions, or an unjustified source scope.

Executability alone does not establish universality, necessity, minimality, or truth.

## Relationship to PBTS-001 and independent replication

PBTS-001, its internal RUN-001, the independent replication package, and coordinator controls remain valid supporting artifacts.

They test the operational clarity and robustness of PB-001 judgments. They may expose missing theorem obligations or counterexamples. They do not constitute a representation theorem and are not prerequisites for attempting one.

Independent replication remains required before claiming independent confirmation of PBTS results. It is not a prerequisite for mathematical deduction.

## Anti-self-validation governance

Project-authored experiments may establish internal coherence or implementation robustness but may not be described as independent confirmation.

This restriction applies to empirical and review claims. It does not prohibit the project from developing a proof. A proof claim is governed by theorem correctness, explicit assumptions, and the applicable proof gates. Independent review remains necessary before claiming independent proof verification.

## Possible outcomes

The program recognizes at least:

1. no universal structure of reasoning exists under the declared assumptions;
2. a universal structure exists, but FAR is not that structure;
3. FAR is universal only within an explicitly bounded formal domain;
4. FAR is sufficient under stated assumptions but not necessary or minimal;
5. FAR is one of multiple equivalent or incomparable structures;
6. FAR is universal and minimal within a declared candidate universe;
7. no finite universal architecture exists under stated assumptions;
8. the proof obligations remain unresolved.

Project success does not require a favorable conclusion about FAR. It requires the strongest justified conclusion.

## Current research boundary

The repository currently provides:

- a frozen Foundation v1.0;
- a prospective architecture-neutral reasoning domain;
- IRD-001;
- PB-001 as a candidate preservation basis;
- PBTS-001 and an internal execution;
- an independently executable replication package and coordinator controls;
- a mechanization MVP;
- deduction-first governance;
- `THM-TARGET-001` v1.0 and its premise ledger.

These results establish readiness for formal faithful-representation work and systematic challenge. They do not answer the central research question.

The immediate central task is faithful-representation formalization and P8 resolution. Independent PBTS replication continues as a parallel supporting track when real qualified participants are available.
