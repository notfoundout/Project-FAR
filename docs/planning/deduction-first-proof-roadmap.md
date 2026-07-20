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
P8 theorem-role decision
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

`THM-TARGET-001` separates common-schema existence, faithful representation of `S_core`, extension to `S_IRD`, P8 correspondence, primitive necessity, minimality, equivalence, uniqueness, incomparability, and impossibility.

**Result boundary:** freezing the target does not establish that the target is satisfiable or that any theorem is proved.

## Stage D2 — Complete the premise and semantics audit

**Status:** complete prospectively through:

- `theory/evaluation/thm-target-001-premise-ledger.json` v1.1;
- `docs/research/faithful-representation-specification-v1.0.md`;
- `theory/evaluation/faithful-representation-specification-v1.0.json`.

The premise ledger classifies every current dependency as a definition, typing or well-formedness condition, substantive axiom, imported frozen specification, scope restriction, evidence condition, conjecture, or unresolved theorem parameter.

`PRM-011` and `PRM-012` now have frozen semantics. Remaining open parameters are explicit:

- the theorem-facing P8 mode;
- the reconstruction class for necessity;
- the candidate universe and equivalence relation for minimality.

No substantive axiom asserting FARA adequacy, PB-001 completeness, primitive necessity, or universal structure has been admitted.

**Exit result:** the premise and semantics gate is satisfied without promoting any conjecture.

## Stage D3 — Formalize faithful representation

**Status:** complete prospectively through `FAITHFUL-REP-001`.

The specification fixes:

- the source materiality contract and axis applicability;
- canonical finite source reducts for P1–P7;
- admissible target-only recovery;
- total typed correspondence;
- injectivity and sort preservation;
- relation preservation and reflection;
- source-declared attribute equivalence;
- P5 finite labeled bisimulation;
- P7 order embedding and path preservation;
- semantic agreement;
- cross-axis coherence;
- uniform source-isomorphism-equivariant construction;
- compositional accountability;
- complete machinery accounting;
- formal nontriviality and negative-control diagnostics;
- all three parameterized P8 clauses;
- the complete `Faithful_{m_8}` conjunction.

The definition formally rejects label-only mappings, output-only lookup, opaque universal states, hidden interpreters, metadata smuggling, evaluator repair, dependency collapse, history erasure, incoherent per-axis encodings, and unsupported evidential upgrading.

**Result boundary:** the definition is frozen, but satisfiability and existence of a uniform FARA constructor are unproved.

## Stage D3.5 — Select the P8 theorem role

**Status:** active immediate stage.

Select and justify exactly one frozen mode:

1. `coordinate` — P8 is an eighth internal strong-embedding obligation;
2. `side_condition` — process-to-presentation correspondence is external to the internal representation theorem;
3. `split` — internal provenance is preserved and actual-process correspondence is a separate theorem or evidence contract.

The decision artifact must state:

- why the selected mode matches IRD-001 and PB-001;
- which theorem clauses it activates;
- which application claims remain external;
- whether `THM-P8-CORR-001` remains separate;
- effects on existing evidence and nonclaims;
- counterarguments and failure conditions.

A content-changing choice outside the three frozen clauses requires a new theorem-target version. Selecting among the frozen clauses does not prove the representation theorem.

**Exit condition:** one P8 mode is frozen and `THM-CORE-REP-001` is no longer blocked by an unresolved theorem parameter.

## Stage D4 — Construction and obstruction lemmas

**Status:** blocked only by the P8 decision.

Attempt constructive lemmas showing how each admitted `S_core` component maps into the target under `FAITHFUL-REP-001`.

In parallel, search for obstruction lemmas showing that the construction cannot be total, faithful, finite, effective, uniform, compositional, or nontrivial under stated assumptions.

Required outputs include:

- ordinary finite configurations and commitments;
- stakes and live alternatives;
- typed grounds and justificatory roles;
- finite deterministic and finite-support probabilistic dynamics;
- nonmonotonic revision and retraction;
- self-modification and rule-version change;
- distributed composition and cross-component dependence;
- consequences and downstream status;
- path-dependent history;
- formal negative-control lemmas;
- explicit countermodels where construction fails.

Broader `S_IRD` features such as continuous carriers, open-ended histories, hidden state, and semantic change remain extension obligations rather than prerequisites for the finite-core theorem.

**Exit condition:** every `S_core` source feature has either a construction lemma or a registered obstruction.

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

Their outputs may reveal ambiguous definitions, produce counterexamples, suggest missing theorem obligations, test human comprehensibility, validate implementations, or support bounded empirical claims.

They may not be used as a substitute for D1–D8 when making a mathematical universality, necessity, or minimality claim.

## Immediate next artifacts

1. Freeze the P8 theorem-role decision.
2. Create the `S_core` construction-and-obstruction lemma ledger under the selected P8 mode.
3. Register formal negative-control lemmas and minimal countermodel fixtures concurrently with constructive work.

## Current nonclaims

This roadmap does not establish that:

- `THM-TARGET-001` is satisfiable;
- `Faithful_{m_8}` is satisfiable;
- IRD-001 defines every form of reasoning;
- PB-001 is the correct or complete preservation basis;
- FARA admits the required representation;
- any primitive is necessary;
- FARA is minimal or unique;
- a universal finite reasoning architecture exists;
- any proof is machine checked or independently reviewed.
