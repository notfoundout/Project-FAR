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

**Status:** next.

Create a versioned theorem-target artifact that states:

- the exact source class quantified over;
- the exact target structure;
- the candidate representation relation;
- the properties that must be preserved;
- the role of IRD-001;
- the role of PB-001 or any proposed revision;
- the treatment of P8;
- nontriviality exclusions;
- theorem consequences;
- explicit nonclaims.

The theorem target must separate at least:

1. scoped existence;
2. faithful representability;
3. universality within the declared scope;
4. primitive necessity;
5. minimality;
6. equivalence or uniqueness.

These must not be collapsed into one statement.

**Exit condition:** the statement is mathematically well-formed, candidate-neutral at the source boundary, and contains no undefined universal quantifier over reasoning.

## Stage D2 — Audit definitions and axioms

Classify every premise used by the theorem as one of:

- definition;
- typing or well-formedness condition;
- substantive axiom;
- theorem imported from an earlier artifact;
- scope restriction;
- evidence condition;
- conjecture.

Resolve circularity risks, including:

- defining reasoning by its representability in FARA;
- defining faithful preservation using FARA-native labels alone;
- allowing an unrestricted representation map to compute the missing structure;
- using P8 simultaneously as a coordinate and as evidence that the coordinate is preserved.

**Exit condition:** a complete premise ledger with no hidden assumptions.

## Stage D3 — Formalize faithful representation

Define the source and target objects and a representation relation with explicit obligations for:

- source-object identity;
- state or configuration;
- commitment status;
- alternatives and stakes where present;
- grounds and justification relations;
- admissible transitions and dynamics;
- consequences;
- historical and dependency structure;
- semantic interpretation;
- evidential correspondence.

State which obligations are universal across the scope and which are conditional on features present in a source system.

**Exit condition:** negative controls such as label-only mappings, lookup tables, hidden interpreters, dependency collapse, and history erasure are formally excluded rather than rejected only by evaluator judgment.

## Stage D4 — Construction and obstruction lemmas

Attempt constructive lemmas showing how each admitted source component maps into the target.

In parallel, search for obstruction lemmas showing that the construction cannot be total, faithful, finite, computable, compositional, or minimal under stated assumptions.

Required outputs include:

- construction for ordinary finite systems;
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

Prove or refute a theorem of the general form:

> For every reasoning system in the frozen source class satisfying assumptions A, there exists a FARA structure and representation map satisfying preservation obligations P.

The exact theorem may be weaker, stronger, or split into multiple theorems. It must be stated before the final proof is accepted.

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

A valid necessity proof must quantify over all admissible reconstructions in the declared candidate class, not merely the mappings tested experimentally.

**Exit condition:** no retained primitive is called necessary solely because an ablation experiment failed.

## Stage D7 — Minimality, equivalence, and uniqueness

Define the universe over which minimality is claimed.

Then establish one or more of:

- a lower bound on required distinctions;
- local minimality of a frozen vocabulary;
- equivalence classes of successful bases;
- uniqueness up to isomorphism or translation;
- incomparable minimal bases;
- absence of a global minimum;
- impossibility of finite universal representation.

**Exit condition:** every use of "minimal" is indexed to a declared universe and cost/equivalence relation.

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

## Immediate next artifact

Create and freeze `THM-TARGET-001`, the scoped representation-theorem target and premise ledger.

It must not contain a proof claim. It must state the exact theorem family, source scope, target structure, preservation obligations, P8 treatment alternatives, nontriviality conditions, and failure conditions.

## Current nonclaims

This roadmap does not establish that:

- THM-TARGET-001 is satisfiable;
- IRD-001 defines every form of reasoning;
- PB-001 is the correct preservation basis;
- FARA admits the required representation;
- any primitive is necessary;
- FARA is minimal or unique;
- a universal finite reasoning architecture exists.