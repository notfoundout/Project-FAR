# Deduction-First Proof Roadmap

## Purpose

This roadmap defines the primary path for answering Project FAR's central question by deduction. It does not assume a favorable result. Every stage may produce a proof, refutation, countermodel, impossibility result, scope restriction, or unresolved obligation.

## Governing dependency graph

```text
Formal scope and source class
            ↓
Definitions and semantics
            ↓
Explicit axioms and admissibility conditions
            ↓
Faithful-representation specification
            ↓
Construction lemmas and obstruction lemmas
            ↓
Scoped existence / representation theorem or refutation
            ↓
Primitive independence and lower bounds
            ↓
Minimality / equivalence / uniqueness or impossibility
            ↓
Mechanized proof verification
            ↓
Independent proof review and adversarial counterexample search
```

Independent empirical replication is a parallel supporting track. It is not a parent dependency of the representation theorem.

## Stage D1 — Freeze the theorem target

**Status:** complete prospectively through:

- `docs/research/thm-target-001-v1.0.md`;
- `theory/evaluation/thm-target-001.json`;
- `theory/evaluation/thm-target-001-premise-ledger.json`.

`THM-TARGET-001` now separates:

1. common-schema existence for the finite explicit IRD core `S_core`;
2. faithful representation of `S_core`;
3. extension to the broader IRD class `S_IRD`;
4. evidential correspondence under a selected P8 mode;
5. primitive necessity or derivability;
6. minimality within a declared candidate universe;
7. equivalence, uniqueness, incomparability, or impossibility.

The target defines a theorem-facing FARA package, representation-witness signature, preservation obligations, nontriviality conditions, failure rules, and nonclaims.

**Result boundary:** freezing the target does not establish that the target is satisfiable or that any theorem is proved.

## Stage D2 — Complete the premise and semantics audit

**Status:** in progress.

The premise ledger classifies every current dependency as one of:

- definition;
- typing or well-formedness condition;
- substantive axiom;
- imported frozen specification;
- scope restriction;
- evidence condition;
- conjecture;
- unresolved theorem parameter.

Open items are:

- formal semantics of `Pres_1` through `Pres_7`;
- formal semantics of `Faithful_m8`;
- the theorem role of P8;
- the reconstruction class for necessity;
- the candidate universe and equivalence relation for minimality.

The source boundary may not define reasoning by FARA representability. The target boundary may not use unconstrained decoding, hidden interpreters, or FARA-native labels as preservation criteria.

**Exit condition:** a complete theorem-facing semantic specification with no hidden assumptions relevant to the next proof stage.

## Stage D3 — Formalize faithful representation

**Status:** active immediate stage.

Expand the predicate schema fixed by `THM-TARGET-001` into exact definitions for:

- source-object and target-object identity;
- typed encoding and admissible recovery;
- configuration preservation;
- commitment preservation;
- stake-and-alternative preservation;
- ground-and-justification preservation;
- admissibility-and-dynamics preservation;
- consequence preservation;
- historical-and-path preservation;
- semantic interpretation;
- evidential correspondence;
- machinery accounting;
- uniformity and compositionality.

State which obligations apply to every source object and which are conditional on features present in a source object.

The definition must formally exclude:

- label-only mappings;
- output-only lookup tables;
- opaque universal states;
- hidden interpreters or operators;
- metadata smuggling;
- evaluator repair;
- dependency collapse;
- history erasure;
- unsupported evidential upgrading.

P8 must be fixed as `coordinate`, `side_condition`, or `split`, or registered as an explicit blocker requiring a target revision.

**Exit condition:** a frozen faithful-representation specification suitable for proof or refutation and strong enough to distinguish representation from unrestricted coding.

## Stage D4 — Construction and obstruction lemmas

Attempt constructive lemmas showing how each admitted source component maps into the target.

In parallel, search for obstruction lemmas showing that the construction cannot be total, faithful, finite, computable, compositional, or minimal under stated assumptions.

Required outputs include:

- construction for the ordinary finite core;
- treatment of self-modification;
- treatment of nonmonotonic revision;
- treatment of probabilistic or graded commitment;
- treatment of distributed reasoning;
- treatment of semantic change;
- treatment of hidden or partially observed state;
- treatment of open-ended or nonterminating processes;
- explicit countermodels where construction fails.

**Exit condition:** every source feature in scope has either a construction lemma or a registered obstruction.

## Stage D5 — Scoped representation theorem

Prove or refute the frozen theorem family, beginning with:

- `THM-CORE-COMMON-001`;
- `THM-CORE-REP-001`;
- `THM-IMP-001` as the negative alternative.

Only after the finite-core result is resolved may the project attempt `THM-IRD-EXT-001` over `S_IRD`.

Allowed outcomes:

- proved within scope;
- disproved by countermodel;
- proved only after explicit scope restriction;
- proved only after theory revision;
- unresolved because a lemma remains open;
- impossible under stated assumptions.

**Exit condition:** a complete proof or a complete refutation/countermodel with the strongest remaining theorem stated precisely.

## Stage D6 — Primitive independence and lower bounds

For every retained primitive or preservation commitment, prove one of:

- indispensable within the theorem's scope;
- derivable from other commitments;
- replaceable by an equivalent commitment;
- necessary only under an added assumption;
- not necessary;
- unresolved.

A valid necessity proof must quantify over all admissible reconstructions in the declared reconstruction class, not merely the mappings tested experimentally.

**Exit condition:** no retained primitive is called necessary solely because an ablation experiment failed.

## Stage D7 — Minimality, equivalence, and uniqueness

Define the candidate universe, equivalence relation, and cost preorder before making a minimality claim.

Then establish one or more of:

- a lower bound on required distinctions;
- local minimality of a frozen vocabulary;
- equivalence classes of successful bases;
- uniqueness up to isomorphism or translation;
- incomparable minimal bases;
- absence of a global minimum;
- impossibility of finite universal representation.

**Exit condition:** every use of “minimal” is indexed to a declared universe and cost/equivalence relation.

## Stage D8 — Mechanization

Encode the frozen definitions, axioms, and theorem chain in an appropriate proof assistant or verified formal system.

Mechanization must distinguish:

- trusted kernel assumptions;
- axioms introduced by Project FAR;
- executable definitions;
- proved lemmas;
- admitted or unfinished obligations;
- extraction or implementation claims.

**Exit condition:** the largest sound theorem fragment is machine checked, and every unmechanized dependency is listed.

## Stage D9 — Independent proof review

Invite independent reviewers to:

- reconstruct the proof;
- challenge definitions and scope;
- identify hidden assumptions;
- produce countermodels;
- verify mechanized artifacts;
- test whether stronger conclusions were inferred than proved.

Independent review strengthens confidence and may discover defects. It is not a logical premise of the theorem.

## Parallel track E — Empirical and replication work

PBTS-001 independent replication, comparative experiments, boundary cases, and application tests remain active when resources are available.

Their outputs may:

- reveal ambiguous definitions;
- produce counterexamples;
- suggest missing theorem obligations;
- test human comprehensibility;
- validate implementations;
- support bounded empirical claims.

They may not be used as a substitute for D1-D8 when making a mathematical universality, necessity, or minimality claim.

## Immediate next artifacts

1. Freeze the faithful-representation specification expanding `Pres_1` through `Pres_7`, `Faithful_m8`, admissible recovery, semantic agreement, and machinery accounting.
2. Resolve P8 as `coordinate`, `side_condition`, or `split`, or register a versioned blocker.
3. Add construction and obstruction lemma ledgers for `S_core` only after the first two artifacts are frozen.

## Current nonclaims

This roadmap does not establish that:

- `THM-TARGET-001` is satisfiable;
- IRD-001 defines every form of reasoning;
- PB-001 is the correct preservation basis;
- FARA admits the required representation;
- any primitive is necessary;
- FARA is minimal or unique;
- a universal finite reasoning architecture exists;
- any proof is machine checked or independently reviewed.
