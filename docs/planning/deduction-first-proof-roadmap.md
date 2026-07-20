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

- `theory/evaluation/thm-target-001-premise-ledger.json` v1.3;
- `docs/research/faithful-representation-specification-v1.0.md`;
- `theory/evaluation/faithful-representation-specification-v1.0.json`;
- `docs/research/p8-theorem-role-decision-v1.0.md`;
- `theory/evaluation/p8-theorem-role-decision.json`.

The premise ledger classifies every current dependency as a definition, typing or well-formedness condition, substantive axiom, imported frozen specification, scope restriction, evidence condition, conjecture, or unresolved theorem parameter.

`PRM-010` is resolved as `split`. `PRM-011` and `PRM-012` have frozen semantics. Version 1.3 records W0 proof progress without changing a premise. Remaining open parameters concern the reconstruction class for necessity and the candidate universe and equivalence relation for minimality.

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

**Result boundary:** the definition is frozen. W0 now proves the source-side normalization and reduct kernel, but target construction, recovery, preservation, and `Faithful_split` satisfiability remain unproved.

## Stage D3.5 — Select the P8 theorem role

**Status:** complete prospectively through `P8-ROLE-001`.

The selected mode is `split`:

- `Pres_8I` preserves internal provenance and evidential status inside `Faithful_split`;
- `Corr_8E` remains a separate actual-process-to-presentation correspondence obligation;
- `THM-CORE-REP-001` and `THM-IRD-EXT-001` use `Faithful_split`;
- `THM-P8-CORR-001` governs the external correspondence family.

`LEM-SC-002` proves extraction of the source-side P8-I reduct. The target-side `Pres_8I` construction remains the W1 obligation `LEM-SC-014`.

The decision permits formal construction work to proceed without turning empirical correspondence into a logical premise. It does not establish either the internal representation theorem or an application correspondence claim.

**Exit result:** P8 is frozen and no longer blocks D4.

## Stage D4 — Construction and obstruction lemmas

**Status:** active. The dependency decomposition is frozen through:

- `docs/research/s-core-construction-obstruction-ledger-v1.0.md`;
- `theory/evaluation/s-core-construction-obstruction-ledger.json`.

The ledger registers 37 obligations:

- 24 construction obligations;
- 10 obstruction obligations;
- 3 assembly obligations.

Current execution state:

- 4 proved construction lemmas;
- 1 established source-scope boundary;
- 32 open obligations;
- W0 complete;
- W1 active.

### W0 — Source normalization kernel — complete

`SCORE-W0-PROOF-001` proves:

- `LEM-SC-001` — finite source-contract normalization;
- `LEM-SC-002` — canonical P1–P7 and P8-I reduct extraction;
- `LEM-SC-003` — materiality closure and applicability decidability;
- `LEM-SC-004` — source-isomorphism transport.

`OBS-SC-001` is resolved as `scope_boundary_established`: non-finite material closure is incompatible with the frozen `S_core` source requirements.

The proof is project-authored and human-checkable. The executable reference implementation provides bounded corroboration only. Proof-assistant verification and independent review have not occurred.

### W1 — Base carriers and direct axes — active

Resolve:

- `LEM-SC-005` — target carrier allocation;
- `LEM-SC-006` — P1 configuration;
- `LEM-SC-007` — P2 commitments;
- `LEM-SC-008` — P3 stakes and alternatives;
- `LEM-SC-009` — P4 grounds and justificatory roles;
- `LEM-SC-012` — P6 consequences;
- `LEM-SC-014` — P8-I internal evidential status.

Each obligation requires an accepted construction proof or a quantified obstruction. A generic opaque encoding, metadata dump, source-specific decoder, or label-only mapping is inadmissible.

### W2 — Dynamics, history, and revision

Resolve deterministic and finite-support probabilistic P5 dynamics, P7 history, nonmonotonic revision, and self-modification through `LEM-SC-010`, `011`, `013`, `015`, and `016`.

### W3 — Global witness obligations

Resolve recovery, semantics, coherence, machinery accounting, uniformity, distributed composition, and witness assembly through `LEM-SC-017` through `LEM-SC-024`.

### W4 — Obstruction and negative controls

`OBS-SC-001` is complete as a source boundary. `OBS-SC-002` through `OBS-SC-010` remain open, including the formal NC-01 through NC-10 failure family.

### W5 — Theorem assembly

`ASM-SC-001` through `ASM-SC-003` remain blocked until their dependencies are resolved.

Construction and obstruction work proceed concurrently when dependencies permit. A failed attempted witness is not a theorem-level obstruction. Every obstruction must quantify over its registered constructor, witness, target, or source class.

Broader `S_IRD` features such as continuous carriers, open-ended histories, hidden state, and semantic change remain extension obligations rather than prerequisites for the finite-core theorem.

**Exit condition:** every mandatory `S_core` feature has an accepted construction lemma or a quantified obstruction, and `ASM-SC-003` records the strongest justified result.

**Immediate work:** construct or obstruct the W1 obligations.

## Stage D5 — Scoped representation theorem

**Status:** blocked by the 32 open D4 obligations.

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
- unresolved because named ledger obligations remain open;
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

Encode the frozen definitions, assumptions, proved lemmas, unresolved obligations, theorem chain, and countermodels in an appropriate proof assistant or verified formal system.

Mechanization must distinguish:

- trusted kernel assumptions;
- axioms introduced by Project FAR;
- executable definitions;
- proved lemmas;
- admitted or unfinished obligations;
- extraction or implementation claims.

The current W0 reference implementation is not proof-assistant mechanization.

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

`SCORE-W0-PROOF-001` is currently project-authored and has not received independent proof review.

## Parallel track E — Empirical and replication work

PBTS-001 independent replication, comparative experiments, boundary cases, and application tests remain active when resources are available.

Their outputs may reveal ambiguous definitions, produce counterexamples, suggest missing theorem obligations, test human comprehensibility, validate implementations, or support bounded empirical claims.

They may not be used as a substitute for D1–D8 when making a mathematical universality, necessity, or minimality claim.

## Immediate next artifacts

1. Construct or obstruct `LEM-SC-005` through `LEM-SC-009`, `LEM-SC-012`, and `LEM-SC-014` as the W1 package.
2. Register target-side fixtures attacking relation reflection, evidential-status preservation, and primitive smuggling concurrently.
3. Preserve W0 as project-authored human proof with bounded executable corroboration until proof-assistant verification and independent review occur.
4. Do not begin theorem assembly while any required dependency remains open.

## Current nonclaims

This roadmap does not establish that:

- `THM-TARGET-001` is proved;
- `Faithful_split` is satisfiable;
- any W1–W5 obligation is proved;
- IRD-001 defines every form of reasoning;
- PB-001 is the correct or complete preservation basis;
- FARA admits the required representation;
- any primitive is necessary;
- FARA is minimal or unique;
- a universal finite reasoning architecture exists;
- W0 is proof-assistant verified or independently reviewed.
