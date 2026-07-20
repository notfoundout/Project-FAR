# THM-TARGET-001 v1.0 — Scoped Representation-Theorem Target

## Status

Frozen prospective theorem target and premise boundary.

This artifact states the propositions Project FAR will attempt to prove or refute. It contains no proof, does not establish that FARA represents the source class, and does not establish universality, necessity, minimality, equivalence, uniqueness, or impossibility.

## Governing artifacts

This target depends on:

- `docs/research/reasoning-domain-specification-v1.0.md`;
- `docs/research/independent-reasoning-definition-v1.0.md` (`IRD-001`);
- `docs/research/preservation-basis-investigation-v1.0.md` (`PB-001`);
- `theory/definitions/definitions.md`;
- `frameworks/FARA/architecture.md`;
- `frameworks/FARA/primitives.md`;
- `docs/governance/deduction-first-research-standard.md`;
- `theory/evaluation/thm-target-001-premise-ledger.json`.

The machine-readable registration is `theory/evaluation/thm-target-001.json`.

## Research question decomposition

The central question is split into separate theorem families:

1. whether a common target schema exists for a frozen source class;
2. whether every source object in that class has a faithful target representation;
3. whether the construction extends beyond the finite explicit core;
4. whether any target commitment is necessary;
5. whether the target is minimal in a declared candidate universe;
6. whether successful targets are equivalent, unique, incomparable, or impossible.

No result in one family automatically establishes another.

## 1. Source language

### 1.1 IRD process presentation

A source presentation is the IRD-001 tuple

\[
\mathcal P=(T,X,\mathcal H,\mathcal O,\mathcal K,\mathcal Q,\Delta,\Gamma,\Vdash).
\]

A scoped source object is a pair `(P,J)` where `J` is an episode region and R1–R6 hold under a declared source interpretation.

### 1.2 Finite explicit core `S_core`

`S_core` contains exactly those scoped source objects `(P,J)` satisfying all of the following:

1. the event region `J` is a finite partially ordered set;
2. every state, commitment, stake, ground, alternative, consequence, and history distinction used by R1–R6 is explicitly represented in a finite carrier set;
3. admissible continuations in `Delta` are given by an explicit finite relation or a finite-support probability kernel;
4. grounds, constraints, and the support relation are explicitly specified for the episode;
5. historical order, revision, retraction, supersession, and rule-change distinctions relevant to the episode are explicit;
6. the source interpretation identifies which distinctions are material to R1–R6 and PB-001;
7. the source is a mathematical presentation, not an unsupported claim that the presentation corresponds to every hidden property of a physical process;
8. arbitrary labeled transitions, output-only lookup, hidden-operator systems, and post-hoc narratives do not enter `S_core` unless they independently satisfy IRD-001.

`S_core` is the first proof target because it admits exact finite objects while retaining nonmonotonicity, finite-support uncertainty, distributed episodes, self-modification, changing stakes, and path dependence when those features are explicitly represented.

### 1.3 General extension class `S_IRD`

`S_IRD` contains all well-formed IRD-001 reasoning episodes, including potentially infinite, continuous, partially observed, open-ended, stochastic, subsymbolic, distributed, or semantically changing presentations.

`S_IRD` is an extension target, not a premise already established representable. A proof over `S_core` may not be reported as a theorem over `S_IRD`.

### 1.4 Application correspondence

A theorem about a formal source presentation establishes only a result about that presentation. Applying it to an actual human, machine, institution, or physical process requires a separately justified correspondence between the process and the presentation.

## 2. Target language

### 2.1 FARA theorem-facing package

A target package is a tuple

\[
\mathcal A=(U,\Pi,R,Rep,S,I,Inv,C,\Sigma,\Theta,H,\Omega,Res,Prov)
\]

with:

- `U`: explicitly distinguishable objects;
- `Pi`: properties assigned to objects;
- `R`: typed relations among objects;
- `Rep`: representations;
- `S`: a representational structure over `Rep`;
- `I`: an interpretation assigning semantic content;
- `Inv`: an investigation fixing objective, scope, and relevant conditions;
- `C`: a reasoning calculus specifying admissible transformations, inference, admissibility, and resolution procedures;
- `Sigma`: reasoning-state representations;
- `Theta`: transition signatures and transformation-execution records;
- `H`: a reasoning trace with ordering and revision history;
- `Omega`: an admissibility structure;
- `Res`: resolution records and their consequences;
- `Prov`: explicit provenance and evidence-status annotations.

This package is an interface assembled from existing canonical FARA concepts. It does not add a new primitive or prove that every listed component is necessary.

### 2.2 Target-class constraint

`A_FARA` is the class of theorem-facing packages that satisfy the canonical category separations in FARA v1.0. A target package may use derived machinery, but every component used by a representation witness must be declared and counted. Unrestricted external interpreters, hidden state, or source-specific executable decoders are not part of the target unless registered as explicit target machinery.

## 3. Representation witness

A representation witness for `(P,J)` is

\[
W=(E,D,M,\iota,\kappa)
\]

where:

- `E` is a typed encoding from source components and relations into a target package;
- `D` is a declared recovery or observation procedure used only to test registered preservation obligations;
- `M` records the component correspondences and proof obligations;
- `iota` is the source-to-target semantic interpretation agreement;
- `kappa` is a complete machinery ledger for derived constructs, operations, hidden state, metadata, and executable assumptions.

`D` may not contain a source-specific copy of the source system, an unrestricted universal interpreter, or facts unavailable in the target package. Any such machinery must be moved into the target and counted, or the witness is inadmissible.

## 4. Preservation predicates

For each PB-001 axis `Pi`, the source interpretation declares a material-distinction relation `Dist_i(P,J)`. The target witness declares a corresponding recoverability relation `Rec_i(A,W)`.

`Pres_i(P,J,A,W)` holds only when every distinction registered in `Dist_i` remains distinguishable and correctly related under `E`, `I`, and the admissible recovery procedure. Equality of final outputs is insufficient.

The required predicates are:

- `Pres_1`: configuration preservation;
- `Pres_2`: commitment preservation;
- `Pres_3`: stake-and-alternative preservation;
- `Pres_4`: ground-and-justification preservation;
- `Pres_5`: admissibility-and-dynamics preservation;
- `Pres_6`: consequence preservation;
- `Pres_7`: historical-and-path preservation.

The full formal definitions and commutation conditions are the next research artifact. Until they are frozen, the faithful-representation gate remains unsatisfied.

## 5. P8 parameter

The theorem family is parameterized by a value

\[
m_8 \in \{coordinate, side\_condition, split\}.
\]

The admissible interpretations are:

1. `coordinate`: evidential correspondence is an eighth preservation predicate internal to the representation relation;
2. `side_condition`: evidential correspondence constrains when a formal source presentation may be claimed to model an actual process, but is not an internal structural coordinate;
3. `split`: internal provenance and evidence-status distinctions are preserved in the representation, while process-to-presentation correspondence is established by a separate theorem or evidence contract.

No representation proof may be accepted while `m_8` remains unresolved. Selecting a mode requires a versioned theorem-facing P8 decision artifact. A mode change after proof work begins creates a new theorem-target version unless proved definitionally equivalent.

## 6. Faithful-representation predicate

For a fixed P8 mode, define the target predicate schema

\[
Faithful_{m_8}(P,J,A,W)
\]

as the conjunction of:

1. all applicable `Pres_1` through `Pres_7` obligations;
2. the obligation induced by the selected P8 mode;
3. typed source-target correspondence;
4. semantic agreement under the declared interpretations;
5. transition and admissibility correspondence;
6. consequence, dependency, and history correspondence;
7. uniformity and nontriviality conditions below;
8. a complete machinery ledger.

This artifact freezes the signature and mandatory clauses. It does not claim that the clauses are already fully formalized or satisfiable.

## 7. Uniformity and nontriviality

A witness is admissible only if all of the following hold:

1. **Uniform construction:** the encoding method is one declared construction over the source class, not an unrelated hand-built decoder for each source object.
2. **No label-only success:** renaming source states with FARA terminology does not establish preservation.
3. **No output-only lookup:** reproducing observed outputs without preserving admissible dynamics and registered dependencies fails.
4. **No opaque universal state:** one undifferentiated token plus an external decoder containing the source does not count.
5. **No hidden interpreter:** executable behavior required for preservation is included in the target machinery ledger.
6. **No metadata smuggling:** metadata that carries a protected distinction is part of the representation and its cost.
7. **No evaluator repair:** a human or evaluator may not reconstruct a missing distinction from narrative knowledge.
8. **No history erasure:** path-dependent distinctions may not be recovered only from external records.
9. **No evidential upgrade:** a target representation may not support a stronger process claim than the source correspondence permits.
10. **Compositional accountability:** whenever the construction composes source subsystems, the target records how component mappings and cross-component relations compose.

A construction that violates any condition may demonstrate coding capacity, but it does not satisfy this theorem target.

## 8. Frozen theorem family

### THM-CORE-COMMON-001 — Common-schema existence

There exists one fixed FARA theorem-facing interface schema and one uniform construction method such that every `(P,J)` in `S_core` is assigned a target package and witness eligible for the faithful-representation test.

Status: `target_frozen_unproved`.

This theorem alone would not establish that the resulting witnesses are faithful.

### THM-CORE-REP-001 — Finite-core faithful representation

For a selected P8 mode:

\[
\forall (P,J)\in S_{core},\;\exists A\in A_{FARA},\exists W:\;Faithful_{m_8}(P,J,A,W).
\]

Status: `target_frozen_unproved`.

A proof would establish faithful representability only for `S_core` under the frozen assumptions and definitions.

### THM-IRD-EXT-001 — General IRD extension

For a selected P8 mode:

\[
\forall (P,J)\in S_{IRD},\;\exists A\in A_{FARA},\exists W:\;Faithful_{m_8}(P,J,A,W).
\]

Status: `target_frozen_blocked`.

This target is blocked pending treatment of infinite and continuous carriers, partial observability, open-ended histories, semantic change, stochastic kernels beyond finite support, and any countermodels discovered outside `S_core`.

### THM-P8-CORR-001 — Evidential correspondence

State and prove the internal or external correspondence obligation induced by the selected P8 mode.

Status: `target_frozen_blocked_by_p8_decision`.

### THM-PRIM-NEC-001[i] — Primitive necessity or derivability

For each retained target commitment `i`, prove within a declared reconstruction class that it is indispensable, derivable, replaceable, assumption-dependent, unnecessary, or unresolved.

Status: `target_frozen_blocked_by_reconstruction_class`.

No candidate primitive is asserted necessary by this target.

### THM-MIN-001 — Minimality

Relative to a declared candidate universe `U`, equivalence relation `~`, and cost preorder `<=`, determine whether the successful target is locally minimal, globally minimal, one of several minima, incomparable, or whether no minimum exists.

Status: `target_frozen_blocked_by_candidate_universe`.

### THM-EQUIV-001 — Equivalence or uniqueness

Characterize successful target schemas up to the declared equivalence relation, including uniqueness, translation equivalence, incomparability, or multiple non-equivalent solutions.

Status: `target_frozen_blocked_by_candidate_universe`.

### THM-IMP-001 — Impossibility alternative

Determine whether no finite, uniform, nontrivial target architecture can faithfully represent `S_core`, `S_IRD`, or a precisely identified subclass under the frozen obligations.

Status: `target_frozen_unproved`.

A valid impossibility result is a successful answer to the research program.

## 9. Dependency order

The theorem family may proceed only in this order:

1. freeze this target and premise ledger;
2. formalize `Faithful_m8` and all preservation predicates;
3. resolve P8;
4. prove construction or obstruction lemmas for `S_core`;
5. prove or refute `THM-CORE-COMMON-001` and `THM-CORE-REP-001`;
6. assess extension to `S_IRD`;
7. define reconstruction and candidate universes;
8. attempt necessity, minimality, equivalence, uniqueness, or impossibility results;
9. mechanize the largest sound fragment;
10. obtain independent proof review.

## 10. Failure conditions

This target is refuted, weakened, or revised if any of the following occurs:

- a source object satisfies `S_core` but admits no target witness satisfying the frozen faithful predicate;
- every proposed witness requires prohibited hidden machinery;
- the source class is circularly defined through FARA representability;
- the target package requires a substantive new primitive or semantic commitment not registered here;
- two materially distinct source dependencies or histories are forced into one target commitment class;
- a P8 resolution changes the theorem's mathematical content;
- the uniform construction exists only by embedding an unrestricted source interpreter;
- a strictly simpler target is proved equivalent under the same scope and obligations;
- the premise ledger contains an unstated substantive axiom;
- the finite-core theorem cannot be extended and the stronger scope was claimed.

A repaired target receives a new version. The earlier target and failed proof attempt remain preserved.

## 11. Premise classes

Every dependency is classified in the machine-readable premise ledger as one of:

- definition;
- typing or well-formedness condition;
- imported frozen specification;
- substantive axiom;
- scope restriction;
- evidence condition;
- conjecture;
- unresolved theorem parameter.

This target introduces no accepted substantive axiom asserting FARA adequacy.

## 12. Consequences of freezing this target

Freezing this artifact establishes only that:

- the theorem family is separated into distinct claims;
- the initial source scope and target interface are explicit;
- trivial coding strategies are excluded prospectively;
- the role of P8 is exposed as an unresolved theorem parameter;
- proof and countermodel work may begin against a stable target.

## 13. Nonclaims

This artifact does not establish:

- that `S_core` captures all reasoning;
- that `S_IRD` is one coherent representable class;
- that FARA represents any source object faithfully;
- that `Faithful_m8` is satisfiable;
- that PB-001 is sufficient, independent, or minimal;
- that P8 has been resolved;
- that any FARA candidate primitive is necessary;
- that FARA is minimal, unique, economical, or superior;
- that a universal finite reasoning architecture exists;
- that a proof has been machine checked or independently reviewed.

## 14. Exact next artifact

Create a frozen faithful-representation specification that expands every `Pres_i` predicate, fixes the admissible recovery and interpretation relations, proves the negative controls are excluded by definition, and resolves or separately registers the P8 theorem mode.
