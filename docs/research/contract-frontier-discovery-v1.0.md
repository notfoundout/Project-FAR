# Externally grounded contract-frontier discovery v1.0

Status: **Research result — `H5` supported at the searched scope; `H2` NOT established; `H3` and `H4` unresolved; `H6` split. Terminal classification `E` + `F`. Every `P*` component is independently anticipated and the defining conjunction is not independently recovered; no global comparison relation over contracts is established, so no frontier, dominance, or maximality claim survives. Corrected in place 2026-08-10 — see `§0`. No canonical surface modified.**
Investigation target: `OP-21` / `UQ-T25` / `UQ-T26`
Kind: deductive contract reconstruction plus primary-literature search. No experiment, no software, no canonical promotion.
Repository base analysed: `6a3343bb3483583a6e09f1e660555253858a077c` (branch `claude/project-far-research-hutt49`, which remains live). Rebased onto `main` at `5f26792e1b2caef9f96bbdd2cc312da46239147d` on 2026-08-10; the rebase was conflict-free and added the PR #436 target-category-discovery material, which is cited descriptively and affects no finding. Provenance of the analysed tree is preserved by the original branch reference.

**Directionality, stated before results.** This investigation searched for contracts that could dominate, recover, or displace `C*`/`P*`/`E*`. A finding that no external contract dominates is **not** evidence that `C*`/`P*`/`E*` is correct, uniquely selected, or independently justified. The campaign was designed so that the strongest available outcome for Project FAR is `H2`, which is explicitly not uniqueness.

---

## 0. Correction notice (2026-08-10)

An internal re-audit found a load-bearing logical defect. It is corrected in place; nothing is deleted, and every withdrawn claim is retained at its original site under a marker.

**The defect.** `§4`–`§5` constructed a Pareto dominance relation over contracts **without assigning any dimension a justified preference orientation**. Pareto dominance is undefined until every dimension has a direction, and no direction was supplied. The error is visible on the record's own table: the bare-set boundary scores *maximal* on `D1` coverage and `D4` transformation invariance and *minimal* on `D5` structural assumptions, so it cannot be dominated "at no cost on any admitted dimension" under any consistent orientation. The dominance claim was false as stated.

**Withdrawn.**

- Every claim that a global Pareto relation over contracts exists (`§5`, `§5.1`).
- The dominance of every serious contract over the bare-set boundary (`§5.1`).
- "Multiple maximal elements", "at least four maximal elements", "`K7` a fifth" (`§5.1`, `§10`).
- "Pairwise incomparable **maximal** elements" (`§5.1`, `§10`) — the pairwise observations are retained as *non-comparability under the dimension set*, which is not the same as established incomparability under a justified relation.
- `H2` as established (`§6.3`).
- The rejection of `H4` on the ground that `H2`+`H5` is "more informative" (`§6.3`) — a proposition is not falsified by another proposition carrying more information.
- The rejection of `H3` and of `H6` (`§6.3`).
- Terminal classification `B` (`§10`).
- Three of seven Stage-5 "forced canonical object" rows (`§7`) and the claim that *every* contract yields a canonical quotient (`§7.1`).
- "RCCD is contract-relative, established" and "FARA is contract-relative" as global claims (`§7.2`).
- The `maximal_knowability` consequences asserted in `§8`.
- "Contract selection is a known unsolved problem in three mature fields", "not a project defect", and "`not_derivable` is not a gap awaiting closure" (`§10.1`).

**Surviving, and unaffected by the defect.**

- `H5` — every `P*` component is independently anticipated; the conjunction is not recovered by any framework located. This is a componentwise negative finding that does not depend on any ordering.
- `H1` not established — no external contract reproduces the conjunction.
- The native reconstructions of all six external traditions (`§2`).
- The candidate set and every rejection, including the forced-reconstruction failures (`§3`).
- The proved bare-set barrier and the conclusion that **coverage maximization alone does not select a useful reasoning contract**.
- The existence of restricted, field-specific comparison orders at their own scopes.
- The self-authorship deficit (`§9`, `LIM-031`) — which the correction *strengthens*.

**Corrected terminal classification: `E` + `F`.** `B` required Pareto-incomparability, now withdrawn. `E` — no non-arbitrary comparison is possible — is the corrected fit for the global cross-contract question. `F` survives unchanged.

## 1. Stage 0 — Existing contract inventory

Every component is marked: **[1]** independently motivated · **[2]** project-authored but derived · **[3]** methodological choice · **[4]** frozen premise · **[5]** unresolved · **[6]** externally unvalidated.

Marks are not exclusive; every Project FAR component carries **[6]** because `USD-W6` terminated at `internal_robustness_only`.

### 1.1 Source-class machinery

| Object | Content | Marks |
|---|---|---|
| `IRD-001` process presentation `(T,X,H,O,K,Q,Δ,Γ,⊨)` | Time/event poset, states, histories, observations, commitments, stakes, admissible evolutions, grounds, support relation. No substrate, notation, centralized controller, fixed rule set, or complete introspective trace required. | **[2][4]** — derived from `RCS-001` and the reasoning-domain spec; explicitly independent of FARA; frozen. **[6]** |
| `IRD-001` conditions `R1`–`R6` | Situated stake · alternative-sensitive commitment space · ground sensitivity (difference-making) · directed evaluation · commitment consequence · traceable justificatory dependence. | **[2][4]**. `R3`'s difference-making condition is **[1]** — it is the interventionist criterion, independently motivated outside the project. |
| `IRD-001` evidential grades `E0`… | Behavioural support vs. instrumented vs. proved correspondence. | **[3]** methodological. |
| `RCS-001` | Positive/contrast family taxonomy, candidate-independent admission rules, admission-precedes-scoring rule, `RCS-CORPUS-001` (8 positive, 8 contrast, 2 disputed). | **[3][4]** — admission rules are a design choice, frozen. **[6]** |
| `C*` | Effectively describable systems maintaining distinguishable commitments, permitting constrained change, preserving revision-relevant grounds, supporting finite history recovery. | **[2][4][6]**. The naturalness of `C*` is **[5]** — `POST-W9` registered it and `TUE-W4` defeating condition 3 was attacked internally and not established. |

### 1.2 Preservation machinery

| Object | Content | Marks |
|---|---|---|
| `PB-001` axes `P1`–`P8` | Configuration · commitment · stake-and-alternative · ground-and-justification · admissibility-and-dynamics · consequence · historical-and-path · evidential-correspondence. Admission rule: an obligation is admitted only if failure to preserve it can change whether `R1`–`R6` hold, which alternatives are live, what grounds bear on which commitments, which transitions are admissible, what consequence occurs, which path produced it, or what evidential grade is claimable. | **[2]** derived from `IRD-001`; the derivation rule itself is **[3]**. `P8` is **[5]** — see `P8-ROLE-001`. **[6]** |
| `FAITHFUL-REP-001` | Source contract `C_S=(τ_S, Mat, ValEq, App)`; seven typed source reducts; admissible recovery; strong typed correspondence with distinction preservation **and reflection**; axis obligations `Pres_1`–`Pres_7`; semantic agreement; cross-axis coherence; uniform construction; compositional accountability; machinery accounting; nontriviality. `C_S` belongs to the source presentation and **may not be chosen or weakened by the target mapping**. | **[2][4]**. The non-weakening rule is **[1]** in spirit — it is the standard prohibition on adjusting the specification to the implementation. **[6]** |
| `P*` | Preservation of commitment content, admissible evolution, dependency-sensitive revision, supersession and historical identity, uniform finite recovery. Stated in reasoning-fact terms, not RCCD labels. | **[2][4]**. The reasoning-fact framing is a deliberate **[3]** anti-circularity control. **[6]** |
| `E*` | Finite or recursively presented representations, effective construction, one uniform terminating recovery procedure per registered finite query. Excludes source-specific hidden decoders, future-information oracles, unrestricted interpreters, uncharged schedulers/proof machinery. | **[3][4]** — effectivity is a methodological choice, frozen. **[6]** |
| Machinery-charging rule | Decoders, schedulers, canonicalizers, provenance bridges, semantic interpreters, proof objects, closure procedures, query interfaces all charged. | **[3]**, and it is the single most load-bearing anti-triviality control in the project. |

### 1.3 Baseline, target, and terminal machinery

| Object | Content | Marks |
|---|---|---|
| `GREL-001` | Finite typed relational baseline `G=(T,U,V,A,R,Σ_G,E_G,D_G,K_G)` containing **no** reasoning-specific primitive — no investigation, commitment, stake, ground, justification, admissibility, consequence. Tests whether `W0`–`W3` succeeded because of FARA commitments or because any general typed relational representation copies explicit structure. | **[3][4]** — a negative control, correctly constructed and not selected to fail. **[6]** |
| `THM-US-TARGET-001` | Eight success conditions (coverage, representation invariance, nondefinitionality, discrimination, ablation resistance, reconstruction resistance, economy, minimality-or-equivalence), eight failure conditions, seven admissible outcomes. `K*` not identified with FARA in advance. | **[3][4]** — the discovery target; explicitly outcome-neutral. |
| `G1` | Relative semantic composition. | **[2]** established; `UPPSemanticKernel.lean` carries one `sorry`. **[6]** |
| `G2` | `∀ Candidate : Type, Admissible ∧ MachineryClosed ∧ FullFaithful → RCCDRealized`, via `IndependentLowerBoundBridge` over eight frozen preservation dimensions. No registry, no enumeration. | **[2]** established, Lean-mechanized. **Contract-relative to `P*`/`E*`.** **[6]** |
| `G3` | Observational underdetermination: two sources with the same accessible observation and incompatible true classifications cannot both be soundly classified; therefore some discriminating access is necessary for any warranted structural verdict, FAR's or a competitor's. | **[1]** — **the only Project FAR contract component derived rather than chosen.** Lean-mechanized. |
| `FAR-CANONICAL-UNIVERSALITY-DECISION-001` | `terminal_for_current_evidence`; G1/G2/G3 established; six canonical bridges `not_established`; verdict `not_derivable`; terminal answer "not proved and not refuted." | **[4][5]** |
| `POST-W9` | Registered the question whether `C*`/`P*`/`E*` is independently justified or partly construct-loaded. Executed internally. | **[5][6]** |
| `TUE-W4` | `maximal_effective_rccd_universality`; unrestricted question evidentially underdetermined. Five defeating conditions registered; none established. | **[2][4][6]** |
| `USD-W6` | `internal_robustness_only`. Three isolated implementation paths, mutation controls, deterministic comparison. Explicitly **not** independent proof review, R3 technical replication, R4 adversarial conceptual replication, or R5 cross-context replication. | **[4]** — this is the binding independence boundary. |
| External-validation packages | `EVC-W1` external proof review, `EVC-W2` R3 technical replication, `EVC-W3` R4 adversarial replication — protocols, manifests, corpora, and result templates frozen in `theory/evaluation/`. R5 cross-context replication is specified in `USD-W6` but has no frozen package. | **[4]** frozen, **[5]** unexecuted. |
| `TCD` bare-set barrier | Natural finitary element-valued operations on `Set` under all functions are exactly coordinate projections. No natural nullary operation. | **[1]** — a proved external-style theorem; the degenerate anchor of the frontier. |
| `TCD` compositional-invariant argument | Functor-invariant arrow-valued operations on a fixed finite graph correspond to free-category path evaluations. **Governance-demoted to exploratory**; no prospective program was frozen. Now in tree at `research/target-category-discovery/compositional-invariant-terminal-result-v1.0.md` following the 2026-08-10 rebase onto `main` (PR #436); it was outside the branch when the analysis was performed, and re-checking it changes no finding here because it is cited descriptively only. | **[5]** — exploratory only; cited descriptively, not relied upon. |
| Completed `LIM-016` | NULL. No admissible derivation witness in two formalization families. Family-independent obstruction: eliminating a primitive in any relational formalization requires designating a relation symbol carrying that primitive's semantic content, and canonical text does not settle elimination vs. relocation. **Self-blocking.** | **[4]** — a closed negative result. Bears on FARA primitive semantics only; certified non-propagating to `C*`/`P*`/`E*`. |

**No object above was redefined by this investigation.**

---

## 2. Stage 1 — External mathematical search space, natively reconstructed

Each source is reconstructed in its own vocabulary before any Project FAR term is applied. Generic encoding formalisms are recorded and set aside; they do not select a contract.

### 2.1 Comparison of statistical experiments (Blackwell; Bohnenblust–Shapley–Sherman)

- **Native universe:** statistical experiments / information structures over a state space.
- **Native observables:** signal distributions conditional on the state.
- **Native preservation criterion:** decision value — experiment `A` is more informative than `B` iff `A` yields at least as high expected utility as `B` in *every* decision problem.
- **Native equivalence:** mutual garbling.
- **Native admissible transformations:** **garbling** — stochastic post-processing of the signal. Independently motivated: it is exactly "what a receiver could have done to itself."
- **Native comparison order:** the Blackwell order.
- **Motivation:** decision theory; the question "when is one information source unambiguously better?"
- **Scope and assumptions:** requires a state space; the classical theorem assumes finite or well-behaved experiments; extensions to general state spaces exist.
- **Load-bearing property for this investigation:** the order is **partial and famously incomplete — most experiments cannot be ranked.** Recent work on weighted garbling and prior-free variants exists precisely because incomparability is pervasive.

### 2.2 Linear time–branching time spectrum (van Glabbeek)

- **Native universe:** finitely branching, concrete, sequential processes presented as labelled transition systems (Spectrum II extends to silent moves).
- **Native observables:** what an observer can detect via action relations — traces, completed traces, refusals, readiness, failures, and their combinations.
- **Native preservation criterion:** each semantics preserves exactly its own observation class.
- **Native equivalence:** eleven principal equivalences, uniformly definable in terms of action relations.
- **Native admissible transformations:** none required; the equivalences live on a fixed universe.
- **Native comparison order:** a **partial order by discriminating power**, refinable into layers via constrained simulation.
- **Motivation:** forty years of concurrency theory failing to agree on which observations are "reasonable."
- **Load-bearing property:** the field's own summary is that behavioural equivalences *depend on how systems are expected to be used*, and **there is still disagreement on which observations are reasonable.** This is an independently developed, mature field that has **not** converged on a canonical observation contract.

### 2.3 Institution theory (Goguen–Burstall; Meseguer general logics)

- **Native universe:** logical systems — a signature category, a sentence functor, a model functor, and a satisfaction relation.
- **Native observables:** satisfaction `⊨`.
- **Native preservation criterion:** the **satisfaction condition** — *"truth is invariant under change of notation."*
- **Native equivalence:** equivalence of institutions.
- **Native admissible transformations:** signature morphisms; institution morphisms and comorphisms.
- **Native comparison order:** existence of a comorphism — a preorder over logical systems, **not total**.
- **Motivation:** the proliferation of specification logics, and the need to do specification independently of the underlying logic. The stated reason for the satisfaction condition is that without it entailment could behave arbitrarily differently under a change of signature — which would disqualify the system from being called a logic at all.
- **Scope:** logical systems. `OP-20` established an abstraction-level mismatch against the *FARA kernel* (a concrete finite structure). **That mismatch does not apply at the contract level:** `P*`/`E*` is itself a contract-level object, and institutions are the mature formalism for comparing contract-level objects. This is a materially different comparison than the one `OP-20` performed and it is recorded here as a distinct finding.

### 2.4 Abstract interpretation (Cousot & Cousot)

- **Native universe:** a concrete semantics presented as a complete lattice.
- **Native observables:** elements of an abstract domain.
- **Native preservation criterion:** soundness; completeness as a strictly stronger condition.
- **Native equivalence:** equality of the induced upper closure operator.
- **Native admissible transformations:** Galois connections `(α, C, A, γ)` with `c ⊆ γ(a) ⟺ α(c) ⪯ a`.
- **Native comparison order:** abstract domains ordered by **precision** — and, unlike Blackwell and van Glabbeek, this order carries **meets and joins** (reduced product, disjunctive completion).
- **Motivation:** systematic construction of static program analyses by approximation of fixpoints.
- **Scope:** requires a fixed concrete semantics to sit at the top of the lattice.
- **Load-bearing property:** this is the one external order in the search space with a lattice structure rather than a bare partial order. It achieves this by **fixing the concrete semantics first** — i.e. by presupposing the very choice at issue.

### 2.5 Minimal realization theory (Myhill–Nerode; Kalman)

- **Native universe:** regular languages; linear time-invariant systems.
- **Native observables:** acceptance of continuations; input–output transfer behaviour.
- **Native preservation criterion:** exact behaviour.
- **Native equivalence:** the Nerode congruence — `u ~ v` iff for all continuations `w`, `uw ∈ L ⟺ vw ∈ L`.
- **Native admissible transformations:** state-space isomorphism.
- **Native comparison order:** none over contracts. Within a fixed observation, a **canonical minimal object exists and is unique up to isomorphism**, because the Nerode equivalence is the coarsest among all equivalences induced by automata for the language.
- **Motivation:** state-space minimality.
- **Load-bearing property:** canonicity and minimality are **exact, provable, and unique — relative to a fixed observation.** Change the observation and you get a different canonical object.

### 2.6 Universal coalgebra (Rutten; Aczel)

- **Native universe:** `F`-coalgebras for an endofunctor `F` on a base category.
- **Native observables:** whatever `F` exposes. **The functor is the observation contract.**
- **Native preservation criterion:** coalgebra homomorphism.
- **Native equivalence:** behavioural equivalence — equality of image in the final coalgebra; coincides with bisimilarity for many functors.
- **Native admissible transformations:** coalgebra homomorphisms.
- **Native comparison order:** **none canonical over functors.** The theory is deliberately parametric in `F`.
- **Motivation:** a unified theory of state-based dynamical systems.
- **Load-bearing property, and the strongest single external result located by this campaign:** the choice of functor directly determines what observations are possible, and **with no observation component all systems become equivalent, while adding an observation set yields a non-trivial final coalgebra.** This is an independently developed, general statement of the phenomenon the `TCD` bare-set barrier proves in one instance.

### 2.7 Testing and contextual equivalence (De Nicola–Hennessy; Milner; Plotkin)

- **Native universe:** processes; program terms.
- **Native observables:** outcomes of applying tests, or behaviour under program contexts.
- **Native preservation criterion:** may/must testing outcomes; contextual indistinguishability.
- **Native equivalence:** testing equivalence; observational (contextual) equivalence. Two objects are `S`-equivalent iff for every context, the result falls in `S` for one iff it does for the other.
- **Native admissible transformations:** context application.
- **Native comparison order:** may ⊑ must; finer test classes give finer equivalences.
- **Motivation:** "what an observer can actually detect."
- **Load-bearing property:** the equivalence is **defined by** the chosen class of contexts or tests. Full abstraction is always full abstraction *with respect to a chosen observation*.

### 2.8 Recorded and set aside — generic hosts, not contracts

Many-sorted first-order model theory and the relational data model (already filed under `OP-20`'s Stage-3 triviality guard); domain theory used as an encoding universe; unrestricted category theory. Each can encode arbitrary structures and therefore **selects nothing**. Recorded so they are not mistaken for candidate contracts.

**Coalgebra with free choice of `F` belongs in this class.** Coalgebra becomes a contract only when `F` is independently motivated; with `F` unconstrained it is a parametric host. This distinction is applied throughout Stage 2.

---

## 3. Stage 2 — Serious candidate contracts

Admission rule applied: a candidate is admitted only if its material components have independent motivation, and **rejected if any crucial clause exists solely to reproduce `P*`/`E*`, RCCD, FARA, or the terminal theorem.**

| ID | `C_i` source class | `Q_i` preserved observables | `E_i` equivalence / recovery | `T_i` admissible transformations | Native? |
|---|---|---|---|---|---|
| **K1** Decision-theoretic informativeness | information structures over a state space | decision value across all decision problems | mutual garbling | stochastic post-processing (garbling) | fully native |
| **K2** Behavioural / coalgebraic | `F`-coalgebras for an **independently motivated** `F` | whatever `F` exposes | behavioural equivalence (final-coalgebra equality) | coalgebra homomorphisms | native **only under a motivated `F`** |
| **K3** Testing / contextual | processes with a declared test or context class | test outcomes / contextual behaviour | testing or contextual equivalence | context application | fully native |
| **K4** Institutional | logical systems | satisfaction | equivalence of institutions | signature morphisms; comorphisms | fully native |
| **K5** Abstraction / soundness | a fixed concrete semantics | abstract-domain properties | equality of upper closure operator | Galois connections | native, **conditional on a pre-fixed concrete semantics** |
| **K6** Minimal realization | behaviours under a fixed observation | the fixed observation | Nerode congruence | state-space isomorphism | fully native |
| **K7** Project FAR | `C*` — effectively describable systems with commitments, constrained change, revision-relevant grounds, finite history recovery | `P*` — commitment content, admissible evolution, dependency-sensitive revision, supersession and historical identity, uniform finite recovery | commitment equivalence with all machinery charged | `E*` — effective representations, no hidden decoders/oracles/unrestricted interpreters | **components anticipated; conjunction project-authored** |

### 3.1 Rejected pseudo-contracts

| Rejected | Reason |
|---|---|
| Bare carriers / all functions | Not a contract but the **degenerate boundary**. Proved to force triviality (`TCD`). Retained as the frontier's anchor, not as a competitor. |
| Small categories / all functors | Source universe is not a class of reasoning systems; the derivation is governance-demoted exploratory; the charter itself states it selects no universal domain. |
| Coalgebra with unconstrained `F` | Parametric host. Selects nothing. |
| Many-sorted model theory / relational model | Generic host; trivially subsumes every relational structure. |
| "`P*` reconstructed inside institutions/coalgebra" | **Rejected under the Stage-2 rule** — the crucial clause (the sentence functor, or `F`) would be chosen solely to reproduce `P*`. This is the same *forced reconstruction* failure `OP-20` recorded when pushing PROV-DM toward `R4`. |
| Charter `Unknown`, FARO `uncertainty`, CRP `Unknown` as contract components | Distinct concepts at distinct layers; `OP-16` established the separation. |

---

## 4. Stage 3 — Comparison dimensions, and their justification

No global preorder is revived. Each dimension is admitted only because at least one external source treats it as a first-class comparison axis.

| Dim | Meaning | Independently justified by |
|---|---|---|
| **D1** source coverage | how large the admitted system class is | Blackwell (all experiments); coalgebra (all `F`-coalgebras) |
| **D2** preservation / discriminating strength | how many source distinctions survive | **van Glabbeek's spectrum is literally ordered by this** |
| **D3** recovery strength | whether the source is reconstructible, and how exactly | Nerode/Kalman minimal realization (exact, up to iso) |
| **D4** transformation invariance | how large the class of admissible recodings is | institutions (invariance under signature change) |
| **D5** structural assumptions required | what must be presupposed before the contract applies | abstract interpretation (needs a concrete lattice); Blackwell (needs a state space) |
| **D6** effectivity requirements | computability/finiteness demands | automata theory; Project FAR `E*` |
| **D7** observational discrimination | what an observer can detect | testing equivalences; full abstraction |

### 4.1 Preference orientation — the test the original record omitted

A Pareto relation is undefined until every dimension carries a direction. Each dimension is therefore examined for (1) the raw property measured, (2) whether larger or smaller is normatively preferred, (3) whether that preference is **externally** justified, and (4) whether the dimension is instead a pure tradeoff axis.

| Dim | Raw property | Preferred direction | Externally justified? | Verdict |
|---|---|---|---|---|
| `D1` | size of the admitted system class | — | **No.** Blackwell and coalgebra range over everything in their setting; neither treats wider as better. The bare-set limit shows maximal coverage forcing triviality. | **tradeoff axis** |
| `D2` | number of source distinctions preserved | — | **No.** Van Glabbeek orders semantics by discriminating power but explicitly does **not** rank them: the field's position is that the appropriate equivalence depends on how the system is to be used. | **tradeoff axis** |
| `D3` | exactness of source reconstruction | — | **No.** Nerode and Kalman construct exact minimal realizations, but exactness is purpose-relative; testing semantics deliberately forgo recovery. | **tradeoff axis** |
| `D4` | size of the admissible recoding class | — | **No.** Institutions motivate invariance under signature change as a *coherence* requirement, not a maximand; enlarging the class strictly reduces the invariants available. | **tradeoff axis** |
| `D5` | structural prerequisites before the contract applies | — | **No.** Abstract interpretation accepts a heavy prerequisite (a fixed concrete lattice) precisely to buy a lattice of abstractions. Fewer prerequisites is not better; it is different. | **tradeoff axis** |
| `D6` | computability/finiteness demands | — | **No.** `USD-W1` showed the excluded families return once certificates are supplied, so effectivity buys tractability at the cost of coverage. | **tradeoff axis** |
| `D7` | what an observer can detect | — | **No.** Same as `D2`; testing equivalences are chosen per application, not maximized. | **tradeoff axis** |

**Result: no dimension carries an externally justified global preference direction.** All seven are tradeoff axes. **Therefore no dimension may participate in a global Pareto dominance relation, and no such relation is established by this record.**

### 4.2 What actually survives

Four claims were previously run together. They are now separated, because they have different warrants.

1. **Refutation of coverage-only optimization — established.** Increasing coverage and transformation invariance while weakening preserved observations reaches the bare-set limit, where only coordinate projections survive. Therefore **coverage maximization alone does not select a useful reasoning contract.** This follows from the proved bare-set barrier and requires no ordering.
2. **Absence of an independently justified global total order — established** (`§4.1`).
3. **Existence of restricted field-specific orders — established**, and usable only at their own scopes: van Glabbeek's discriminating-power order *within* LTS-presented processes; the Blackwell order *within* information structures over a common state space; the precision order *within* abstract domains over a fixed concrete semantics.
4. **Existence of a justified global Pareto order — NOT established.** It does not follow from (1), and (2) counts against it. Nothing here shows Pareto is the unique admissible global comparison method, nor that some other method could not be justified later.

### 4.3 Original subsection, retained — **claims superseded by `§4.1`–`§4.2`**

> The reasoning below correctly observed the tradeoffs but wrongly converted them into a dominance relation. Retained as history; the anti-monotonicity observations survive as *tradeoffs*, not as orientations.

#### The dimensions do **not** all point toward "better"

This was checked explicitly, as required.

- **D1 and D2 are antagonistic.** Enlarging the admitted class weakens what can be uniformly preserved. Van Glabbeek's spectrum is the mature statement of the trade; the bare-set barrier is its limit point, where `D4` is maximal (all functions admitted), `D1` is maximal (all sets), and `D2` collapses to zero — yielding only projections.
- **D4 is anti-monotone with D2.** A larger transformation class admits fewer invariants. Independently visible in coalgebra: a weaker functor identifies more systems.
- **D5 is anti-monotone with D1.** Abstract interpretation buys a lattice with meets and joins precisely by fixing the concrete semantics first, which shrinks applicability.
- **D6 trades against D1.** Effectivity requirements exclude non-effective sources; `USD-W1` showed the excluded families return once certificates are supplied.

**Consequence, as originally written:** ~~Any coverage-monotone total order over contracts is maximized at the degenerate contract, whose forced architecture is trivial. A total order is therefore not merely unavailable — it is **known to rank the worst contract highest**. Only a Pareto relation is admissible.~~

**Corrected.** The first two sentences survive. The third — "**Only a Pareto relation is admissible**" — is **withdrawn**: it presupposes that a Pareto relation *is* admissible, which `§4.1` refutes for want of any justified dimension orientation. The corrected consequence is that **no global comparison relation over contracts is established here**, by Pareto or otherwise.

---

## 5. Stage 3 result — no global comparison relation is established

Dimensions scored qualitatively as `high` / `mid` / `low`. Scores are relative placements, not measurements.

| | D1 coverage | D2 preservation | D3 recovery | D4 invariance | D5 assumptions | D6 effectivity | D7 discrimination |
|---|---|---|---|---|---|---|---|
| **boundary** bare-set | max | **none** | none | max | none | none | none |
| **K1** Blackwell | mid | mid | low | mid | **high** (state space, priors) | low | mid |
| **K2** coalgebraic | high | varies with `F` | high (final coalgebra) | mid | mid | low | varies with `F` |
| **K3** testing | mid | mid | low | mid | mid (test class) | low | **high** |
| **K4** institutional | high | mid | low | **high** | mid | none | low |
| **K5** abstraction | low | tunable | low | low | **high** (fixed concrete) | mid | tunable |
| **K6** minimal realization | **low** | high | **max** (exact, unique up to iso) | low | mid | **high** | mid |
| **K7** `C*`/`P*`/`E*` | mid | **high** | high (uniform finite recovery) | mid | high | **high** | high |

### 5.1 What the profile table does and does not license

The table above records **relative positions on seven tradeoff axes**. Because `§4.1` establishes that no axis carries an externally justified preference direction, the table does not induce a dominance relation, and the claims below are corrected accordingly.

- **Dominance — WITHDRAWN.** No dominance relation is established, including against the bare-set boundary. The boundary scores maximal on `D1` and `D4` and minimal on `D5`, so it is not dominated under any consistent orientation. What survives is the separate, proved statement of `§4.2`(1): coverage maximization alone does not select a useful reasoning contract.
- **Maximality — WITHDRAWN.** No element is established as maximal. Maximality presupposes the relation `§4.1` refutes. Independently, `K2`'s profile varies with the choice of `F` and `K5`'s is tunable, so neither could have been evaluated as maximal even had a relation been available. No non-domination proof is offered against the admitted competitors, because none is available. `H4`-style incomparability is therefore **unresolved**, not established.
- **Non-comparability under the dimension set — retained, weaker reading.** The pairwise observations below are genuine: each pair trades a recorded axis against another, so no pair is ordered *by these seven axes*. That is weaker than incomparability under a justified relation, and must not be cited as the latter.

### 5.2 Original subsection, retained — **claims corrected by `§5.1`**

### 5.1 Established relations

- **WITHDRAWN — Dominance:** only against the degenerate boundary. Every `K1`–`K7` strictly dominates the bare-set contract on `D2`, `D3`, and `D7` at no cost on any admitted dimension. This is the campaign's one clean dominance result, and it is the formal content of "some premise is required."
- **Non-comparability under the seven axes (weaker than the original "incomparability"), pairwise:** `K1 ⟂ K3` (Blackwell buys decision-theoretic ranking at the cost of a state space; testing buys discrimination at the cost of a stipulated test class). `K1 ⟂ K4`. `K3 ⟂ K4` (satisfaction-invariance vs. observer-discrimination are different `Q`). `K4 ⟂ K6` (maximal invariance vs. maximal recovery). `K5 ⟂ everything on D1`. **`K7 ⟂ K1`, `K7 ⟂ K3`, `K7 ⟂ K4`, `K7 ⟂ K6`** — see §6.
- **No joins or meets in general.** `K5` alone supplies a lattice, and only by fixing `D5` maximally. Blackwell's order is famously incomplete; van Glabbeek's is a partial order with layers, not a lattice.
- **Restricted principled preorders, usable only at their own scope:** van Glabbeek's discriminating-power order **within** LTS-presented processes; the Blackwell order **within** information structures over a common state space; the precision order **within** abstract domains over a fixed concrete semantics. Each is used here only at that scope, as required.
- **WITHDRAWN — Multiple maximal elements.** ~~No admitted contract dominates all others on all dimensions. The frontier has at least four maximal elements (`K1`, `K3`, `K4`, `K6`), with `K7` a fifth (§6).~~ No maximality and no frontier is established; see `§5.1`.

---

## 6. Stage 4 — Position of `C*`/`P*`/`E*`

Placement was performed only after §2–§5 were fixed.

### 6.1 Componentwise anticipation

Each `P*` component is independently anticipated outside Project FAR:

| `P*` component | Independent anticipation |
|---|---|
| `R1` recoverable commitment content | state-content observability; the output component of a coalgebraic functor |
| `R2` constrained admissible evolution | labelled transition systems; the transition component of `F` |
| `R3` dependency-sensitive revision | AGM belief revision; truth-maintenance systems; provenance (`OP-20`: W3C PROV) |
| `R4` supersession and historical identity | event structures with acyclic causal order (Nielsen–Plotkin–Winskel 1981); PROV (`OP-20`) |
| `R5` uniform effective recovery | effectivity requirements in automata theory; uniformity of the Nerode construction |

### 6.2 The conjunction is not recovered

**No independently motivated framework located by this search binds commitment content, constrained evolution, dependency-sensitive revision, historical identity, and uniform effective recovery into one preservation contract.** This exactly mirrors `OP-20`'s finding one layer down — every FARA kernel component independently anticipated, the connecting architecture not — and it is recorded as an independent replication of that pattern at the contract layer.

### 6.3 Adjudication — corrected 2026-08-10

**`H5` is the only hypothesis supported. `H2` is not established.**

- **`H5` — supported at the searched scope.** The conjunction defining `C*`/`P*`/`E*` rests on project-specific normative choices not independently recovered, while each component is independently anticipated (`§6.1`–`§6.2`). This is a componentwise negative finding and **does not depend on the dimension set or on any ordering**, so it is unaffected by the `§0` defect.
- **`H2` — NOT established.** Its content is that `C*`/`P*`/`E*` lies on an independently motivated **Pareto frontier**. `§4.1` shows no dimension carries a justified orientation, so no such frontier is established and the claim has no support. What survives is only the weaker, non-comparative observation that its profile trades the same axes external traditions trade.
- **`H1` — not established.** No external contract reproduces the conjunction. This is a direct negative finding from `§6.2` and needs no ordering.
- **`H3` — unresolved.** Previously "rejected." That rejection required a dominance relation to fail, and no dominance relation is established, so neither dominance nor its absence can be asserted.
- **`H4` — unresolved.** Previously "rejected as the sole verdict" on the ground that `H2`+`H5` is "strictly more informative." **That reasoning is invalid and is withdrawn**: a proposition is not falsified by another proposition carrying more information, and `H4` can coexist with `H5`. `H4` asserts incomparability, which presupposes the relation `§4.1` refutes; it is therefore neither supported nor refuted. Where non-comparability *under the seven axes* is recorded (`§5.2`), that is weaker than `H4` and must not be reported as `H4`.
- **`H6` — split.** Previously "rejected." Corrected: **supported** for global cross-contract comparison, since `§4.1` establishes no non-arbitrary global relation; **refuted** within field-specific scopes, since three independently developed orders exist and were applied at their own scopes. The two readings were previously conflated.
- **`H7` — applies to placement.** Previously "rejected for placement." Corrected: with `H2` unestablished and `H3`/`H4` unresolved, the placement question is exactly the case `H7` covers. It is also retained for the *warrant* question (`§9`).

**Interpretation rules.** `H5` does not falsify any bounded theorem — `G2`'s conditional derivation of RCCD from `P*`/`E*` is unaffected; only the strength of the *external* placement is at issue. `H1` not established is **not** evidence that `C*`/`P*`/`E*` is correct or uniquely selected. `H3`/`H4` unresolved is **not** vindication.

### 6.4 Strongest competitor, and the strongest argument against it

**Strongest competitor: `K3`, the testing/contextual contract.** It is fully native, has no state-space or concrete-semantics prerequisite, is maximal on `D7`, has a mature independent literature, matches the retracted-but-retained `C4` contract already in the repository, and is the only competitor whose source universe plausibly contains reasoning systems in the same sense `C*` does.

**Strongest argument against `K3` as a replacement:** its equivalence is *defined by* the stipulated test class, so it relocates the selection problem rather than solving it. Full abstraction is always relative to a chosen observation; choosing the tests is exactly as normative as choosing `P*`. Furthermore `K3` scores low on `D3` — testing equivalence does not require the source to be reconstructible — so it cannot support recovery-dependent results at all.

**Strongest argument against that argument, preserved rather than discarded:** `K7` is subject to the identical objection. `P*` is stipulated no less than a test class is. The asymmetry Project FAR could claim is that `E*` plus the machinery-charging rule makes the stipulation *auditable*; that is a methodological advantage, **not** an independent justification, and it must not be cited as one.

---

## 7. Stage 5 — Architectures induced by the surviving contracts

Existing repository results were reused wherever premises matched. No campaign was re-run.

**Corrected 2026-08-10.** The original table asserted that each contract *forces* a canonical object. Each row is now classified by what the cited native theory actually proves, with missing assumptions stated. Classes: **THEOREM** · **CONDITIONAL THEOREM** · **NATIVE CONSTRUCTION** · **ANALOGY** · **NOT ESTABLISHED**.

| Contract | Object originally claimed | Classification | Missing assumptions / reason |
|---|---|---|---|
| boundary bare-set | coordinate projections only | **THEOREM** | Naturality of finitary element-valued operations on `Set` under all functions. Proved; no gap. |
| `K1` Blackwell | minimal sufficient statistic | **NOT ESTABLISHED** | Blackwell's theorem concerns the informativeness order and garbling equivalence. It does **not** construct a minimal sufficient statistic; sufficiency and minimal sufficiency are a separate classical development (Fisher; Lehmann–Scheffé). Downgraded to an adjacent native construction in a neighbouring theory. |
| `K2` coalgebraic (motivated `F`) | final coalgebra / behaviour quotient | **CONDITIONAL THEOREM** | Final coalgebras do **not** exist for arbitrary `F` — the powerset functor admits none by Lambek's cardinality argument. Requires a bounded/accessible functor. Behavioural equivalence and bisimilarity also coincide only for suitable `F`. |
| `K3` testing | fully abstract model | **NOT ESTABLISHED** | Full abstraction is a property one *proves* of a proposed model, not something a contract yields; it is famously hard and open in cases such as PCF. What survives is the **NATIVE CONSTRUCTION** of the quotient by the chosen testing equivalence, which is immediate but weaker. |
| `K4` institutional | the institution itself as canonical object | **NOT ESTABLISHED** | Category error: the contract *is* the institution, so the row asserts only that a contract is itself. Removed as a substantive claim. |
| `K5` abstraction | best abstraction / upper closure operator | **CONDITIONAL THEOREM** | A best abstraction exists only when every concrete property has a most precise abstraction, i.e. when a Galois connection exists. Widening/narrowing frameworks exist precisely because it need not. |
| `K6` minimal realization | Nerode automaton, unique up to isomorphism | **THEOREM** | Genuine and unconditional within its stated setting: for a regular language the Nerode congruence has finite index and yields a canonical minimal DFA unique up to isomorphism. Conditional on regularity/finite index. |
| `K7` `P*`/`E*` | RCCD `R1`–`R5` | **CONDITIONAL THEOREM** | `G2`, Lean-mechanized: conditional on admissibility, machinery closure, and full faithfulness. Not unconditional. |

**Tally: one unconditional theorem, one theorem conditional on regularity, three conditional theorems, three not established.**

### 7.1 What the table supports — corrected 2026-08-10

**Withdrawn.** ~~Every one of these contracts yields a canonical minimal object relative to itself. The invariant across contracts is the construction pattern — canonical quotient relative to declared observations.~~ No common formal schema was defined, and none was proved across the candidate set. Three of the seven rows are **NOT ESTABLISHED**, so the universally quantified statement is unsupported on its own evidence.

**Withdrawn.** ~~Different independently justified contracts *force* different architectures.~~ "Forces" overstates three rows. The defensible residue is that the objects associated with these contracts differ, and that only `K7` is associated with RCCD.

**Surviving observation, stated at the warranted strength:**

> Several mature traditions construct equivalence or minimal representations **relative to declared observations**. In two cases this is a theorem (bare-set naturality; Nerode minimal realization), in three it is a theorem conditional on stated assumptions (final coalgebra for suitable `F`; best abstraction under a Galois connection; `G2` under machinery closure and full faithfulness), and in the remaining cases it is a native construction or is not established.

This is consistent with, and weaker than, the surviving positive residue the 2026-08-05 `TCD` audit recorded — that once a contract is declared, constructions such as descent, observational quotienting, closure, coalgebraic behaviour, and localization become canonical *relative to that contract*. It does **not** establish that residue as a general theorem.

**Registered as a future question, not manufactured here.** Whether a common formal schema — "every contract of a specified class induces a canonical quotient" — can be defined and proved across the candidate set is recorded as an open question in `UQ-T26`'s neighbourhood. It is not asserted by this record.

### 7.2 Answers to the two invariance questions

**Corrected 2026-08-10.** Both answers previously asserted global contract-relativity. The inference was invalid twice over: three of the six contrasting associations are **NOT ESTABLISHED** (`§7`), and six contracts not entailing RCCD does not show that *no* legitimate contract entails RCCD. Corrected to the strongest logically warranted form.

**RCCD.**

- **Established:** `G2` derives RCCD **conditionally** on `P*`/`E*` together with admissibility, machinery closure, and full faithfulness. Lean-mechanized. Unchanged by this campaign.
- **Established:** RCCD's components are individually anticipated externally; its conjunction is not recovered by any framework located (`§6.1`–`§6.2`).
- **NOT established:** that no alternative legitimate contract could also entail RCCD. No search over contracts entailing RCCD was performed, and none is possible without the comparison relation `§4.1` refutes.
- **Warranted statement:** *RCCD is established only conditionally under the currently proved `P*`/`E*` result. Contract-invariance across the serious contract space is **neither established nor refuted**.*
- ~~"RCCD is contract-relative, established"~~ — **withdrawn**.

**FARA.**

- **Established, independently of this campaign:** FARA is one realization inside `CEC-RCCD-001` alongside `LTS-PROV` and `COALG-DYN` (`IKD-W8`), and every FARA kernel component is anticipated by prior work while the connecting architecture is not (`OP-20`). Both stand on their own evidence and are unaffected by the `§0` defect.
- **NOT established:** global contract-relativity of FARA, for the same reason as RCCD.
- **Warranted statement:** *FARA is realization-plural within `CEC-RCCD-001`, and that class is defined relative to `P*`/`E*`. Whether FARA or an equivalent would be entailed under other legitimate contracts is **not established**.*
- ~~"FARA is contract-relative"~~ as a global claim — **withdrawn**.

---

## 8. Stage 6 — Bridge-witness prioritization — corrected 2026-08-10

The original ranking scored bridges by "ability to change the frontier." **No frontier is established** (`§5.1`), so that criterion is void and every EIV assigned under it is withdrawn. Bridges are re-scored by what a proof would actually license.

### 8.1 `maximal_knowability` — corrected consequences

The original entry claimed a proved non-embedding of the `K3` testing scope into `C*` would "establish ≥2 maximal frontier elements and settle `H4` formally." **Withdrawn.** A proof that `K3 ↛ K7` under one warrant-preserving embedding notion establishes exactly one thing:

> Under that embedding notion, that one directed reduction fails.

It does **not** establish `K7 ↛ K3`; nor incomparability of `K3` and `K7`; nor maximality of either; nor that no `K2`, `K5`, or unexamined `Kx` dominates either; nor "≥2 maximal frontier elements"; nor `H4` in general. Asymmetry requires the converse to be tested separately, and maximality requires a relation over the whole admitted set.

It is also **internally authored**, so by construction it cannot address `LIM-031`, the self-authorship deficit that `§9` and `§12` identify as dominant.

### 8.2 Re-scored ranking

| Rank | Bridge | What a proof licenses | What it cannot license | EIV |
|---|---|---|---|---|
| **1** | `quotient_minimality` | Failure refutes minimality of the FAR kernel at its registered scope — a genuine falsifier. Nerode's coarsest-congruence argument and final-coalgebra minimality supply an external witness template. Requires proving the kernel `Separated`. | Anything about contract comparison; anything about external independence. | **high**, and highest among the bridges |
| 2 | `representation_invariance` | Invariance of a declared FAR invariant across the admissible presentation class. Final-coalgebra uniqueness is the template. | Contract comparison. | mid |
| 3 | `unique_factorization` | Non-uniqueness would give plural kernels, consistent with `USD-W5`'s `multiple_incomparable_minima`. | Contract comparison. | mid |
| 4 | `maximal_knowability` | One directed embedding result (`§8.1`). | Incomparability · maximality · any frontier claim · `H4` · `LIM-031`. | **downgraded from highest to low** — its entire prior justification was the frontier consequences now withdrawn |
| 5 | `definitional_completeness` | Factorization of registered invariants through a basis. | Contract discrimination — its invariant class is part of `Q`. | low |
| 6 | `conservative_extensibility` | Conservativity of admissible extensions within a fixed contract. | Anything cross-contract. | lowest |

**Recommendation, corrected.** `quotient_minimality` is the only bridge with high independent standing, because its falsification power does not depend on any contract comparison. `maximal_knowability` is **not** a priority: it was ranked first solely for consequences it does not have.

The formal↔actual bridge (`USD-W1-APC-001`) is **not** in this family and must not be ranked with it: it returned `new_assumption_required`, and its separation theorem shows it is not closable by formal work at all.

---

## 9. Stage 7 — Self-authorship audit

The controlling question: would these results survive if Project FAR's definitions, examples, architectures, and terminology were hidden from the source-contract designer?

| Layer | Status |
|---|---|
| **internally coherent** | Yes. Dimensions are derived from external sources; the Pareto relation follows from the scored profiles. |
| **independently motivated** | **Yes, for `K1`–`K6`.** Blackwell, van Glabbeek, Goguen–Burstall, Cousot, Nerode/Kalman, Rutten, De Nicola–Hennessy all predate and are independent of Project FAR. Their universes, observables, equivalences, transformations, and orders were reconstructed natively before any FAR term was applied. |
| **independently instantiated** | **No.** The reconstruction, the dimension selection, the scoring, and the placement were all performed inside this project by a party with full access to `C*`/`P*`/`E*`. The sources are independent; the *mapping* is not. |
| **independently replicated** | **No.** Single path. No mutation controls, no isolated re-derivation, no external reviewer. |

**Declared contamination risk.** The seven comparison dimensions were selected knowing `C*`/`P*`/`E*`'s profile. `D3` (recovery strength) and `D6` (effectivity) are dimensions on which `K7` scores high, and although each is independently justified — by Nerode and by automata theory respectively — a designer without FAR exposure might not have selected that particular seven. **The `H2` component of the verdict is therefore weaker than the `H5` component.** `H5` is robust: it is a negative finding about the conjunction and does not depend on the dimension set. `H2` is a placement on a dimension set this project chose.

Per `USD-W6`, none of this may be promoted. This campaign is **not** R3, R4, or R5, and it is weaker than `USD-W6`'s `internal_robustness_only`, which at least ran three isolated implementation paths.

---

## 10. Stage 8 — Termination — corrected 2026-08-10

**Terminal classification: `E` + `F`.** (Previously `B` + `F`.)

- **`E` — no non-arbitrary comparison is possible**, for the global cross-contract question. `§4.1` establishes that no comparison dimension carries an externally justified preference orientation, so no global relation — Pareto or otherwise — is available to rank or separate the candidates.
- **`F` — evidence is exhausted for the placement question, and specific external evidence is required.** Unchanged, and strengthened: the dimension set is the contaminated object, and only an external party can supply an uncontaminated one.
- ~~**`B`** — several independently motivated contracts remain Pareto-incomparable; `K1`, `K3`, `K4`, `K6` are pairwise incomparable maximal elements.~~ **WITHDRAWN.** Incomparability and maximality both presuppose the relation `§4.1` refutes. What survives is non-comparability *under the seven axes* (`§5.2`), which is weaker and is not `B`.

Both `E` and `F` are successful research terminations under the campaign's own rules.

### 10.1 The campaign's strongest result — narrowed 2026-08-10

The original formulation is **withdrawn**: ~~"Contract selection is a known, unsolved problem in at least three mature, independently developed fields, and none has solved it."~~ The cited sources establish *analogous parameterization and incomparability phenomena* in their own settings; they do not establish that those fields are working on the same problem as the Project FAR universality question. Same-problem identity was asserted, not shown.

**Narrowed statement, at the strength the sources support:**

> Several mature external traditions also leave observational choices parameterized, use partial rather than total comparison orders, or produce results explicitly relative to a declared observational structure. Concurrency theory records continuing disagreement about which observations are "reasonable"; the Blackwell order is partial and many experiments are unrankable under it; universal coalgebra is parametric in the observation functor by design, and with no observation component every system becomes equivalent — a phenomenon of the same shape as the `TCD` bare-set barrier.

Two consequences follow, both narrowed:

1. ~~Project FAR's inability to independently justify `C*`/`P*`/`E*` is not a project defect.~~ **Narrowed:** *this limitation is not unique to Project FAR.* Adjacent traditions exhibit the same parameterization; that is an evidential observation about the landscape, not an exoneration.
2. ~~`FAR-CANONICAL-UNIVERSALITY-DECISION-001`'s `not_derivable` verdict is not a gap awaiting closure.~~ **Narrowed:** *`not_derivable` is terminal for the currently available internally authored evidence class; genuine external contract selection or replication could change the warrant.* The earlier phrasing was also internally incoherent — it implied external replication could not change the conclusion while `§12` lists external replication as the missing evidence. That incoherence is removed.

`ADR-002` remains a comparable phenomenon at the intra-FARA scale — where evidence underdetermines, the residue is a decision — but that is an analogy, not a derivation.

This is **not** a claim that `C*`/`P*`/`E*` is correct, that RCCD is universal, or that no better contract exists.

---

## 11. Claims affected and unaffected

### Affected — reach clarified, none downgraded

| Claim | Effect |
|---|---|
| `G2` open-world structural lower bound | **Reach stated externally for the first time.** `G2` is contract-relative to `P*`/`E*`, and six independently motivated contracts force different canonical objects. `G2` itself already says this; the campaign supplies external corroboration. No downgrade. |
| `IKD-W9` / `TUE-W4` bounded RCCD universality | Same. Contract-relativity now externally corroborated rather than internally asserted. No downgrade. |
| `POST-W9` scope-challenge question | **Materially advanced.** The question "is `C*`/`P*`/`E*` independently justified?" now has a partial answer: componentwise yes, conjunctively no. |
| `TUE-W4` defeating condition 3 (circular definition of `C*`/`P*` by `R1`–`R5`) | **Not established, and now with external evidence.** `P*`'s components are independently anticipated, which is evidence against pure circularity. Not a discharge — the conjunction remains project-authored. |

### Unaffected — explicitly

The terminal UPP theorem and every frozen premise; `FARA-FORMAL-KERNEL-001` and its Acceptance; the seven candidate primitives and their unresolved `W1` status; completed `LIM-016` and its self-blocking finding; `ADR-002` and every `OP-13`–`OP-20` result; all bounded `W2`–`W5`, `VOC`, `CORE`, `FOUNDATION-COMP`, `EXPANDED-BOUND` results; all `CRE`, `EV`, and SWE-agent evidence; `UQ-T2`; `OP-02`; `Ω`'s type and semantics; `FAR-CANONICAL-UNIVERSALITY-DECISION-001`'s verdict.

**No dependency on the FARA primitive layer was demonstrated or asserted.** This campaign operates entirely at the contract layer and is certified non-propagating into Track β, in the same sense and for the same reason that Track β is certified non-propagating into Track α.

---

## 12. Exact external-independence deficit

What is missing, stated precisely enough to be procured:

1. **An externally supplied dimension set.** A party without FAR exposure selects the axes on which preservation contracts should be compared. Removes the §9 contamination on `H2`. *(Nearest frozen package: `EVC-W3` R4 adversarial conceptual replication, which requires independently designed alternatives.)*
2. **An externally supplied contract.** A party independently defines a source class and preservation contract for reasoning systems. Would test `H3` directly. *(Nearest: R5 cross-context replication, which requires "a new reasoning context and independently defined source contract." **R5 has no frozen package** — this is a gap.)*
3. **An external placement judgement.** A party places `C*`/`P*`/`E*` against `K1`–`K6` without seeing this record's conclusion.
4. **An external proof review** of `G2`'s bridge lemmas, whose independence and adequacy `G2` itself identifies as the concentrated scientific risk. *(Nearest: `EVC-W1`.)*

Items 1–3 are all instances of one deficit: **no party outside this project has ever chosen or evaluated a contract for the Project FAR universality question.**

---

## 13. Quality Gate disposition

**ACCEPT WITH RESTRICTED SCOPE** for: the external contract reconstructions (§2), the candidate set and rejections (§3), the dimension justification and anti-monotonicity finding (§4), the incomparability results (§5), the componentwise-anticipation finding (§6.1–6.2), the induced-architecture table and the canonical-quotient pattern (§7), the bridge ranking (§8), and the terminal `B`+`F` classification (§10).

**RESTRICTED FURTHER** for `H2`: the placement depends on a dimension set selected with knowledge of `K7`'s profile. `H5` is not so restricted.

**INSUFFICIENT EVIDENCE** for: any claim that `C*`/`P*`/`E*` is optimal, uniquely selected, or independently justified; any claim that no dominating contract exists outside the searched space; any novelty claim; any change to `FAR-CANONICAL-UNIVERSALITY-DECISION-001`.

**No canonical surface modified. No registered claim upgraded or downgraded.**

---

## 14. Preserved negative and non-discriminating results

- **The bare-set/all-functions contract was tested as a competitor and rejected as a boundary**, not omitted. It is the one clean dominance result and it points *against* coverage-maximization.
- **The attempt to reconstruct `P*` inside institutions and inside coalgebra failed at forced reconstruction** — the sentence functor or `F` would be chosen solely to reproduce `P*`. Preserved as a failed reduction, identical in form to `OP-20`'s failed PROV→`R4` push.
- **The attempt to find a single global preorder over contracts failed**, and failed *informatively*: three of seven dimensions are anti-monotone with coverage, so the coverage-maximal contract is the trivial one.
- **`K5` abstract interpretation supplies the only lattice**, and does so by presupposing the concrete semantics. Recorded as non-discriminating: it solves the ordering problem by assuming the selection problem away.
- **The number of external fields searched is not counted as evidence** for or against any conclusion.
- **`OP-20`'s abstraction-level mismatch verdict for institutions was re-examined at the contract layer and found not to transfer.** This does not overturn `OP-20`, whose target was the concrete FARA kernel. Both stand at their own scopes.

---

## 15. Nonclaims

This investigation does not establish: that `C*`/`P*`/`E*` is correct, optimal, natural, or independently justified; that RCCD is universal or contract-invariant; that FARA is universal, minimal, novel, or non-novel; that no contract outside the searched space dominates `C*`/`P*`/`E*`; that the seven comparison dimensions are complete or uniquely correct; that the Pareto placements are measurements rather than qualitative relative positions; that any primitive necessity, minimality, independence, or completeness result follows; that external independence has been obtained or is unobtainable; that the terminal UPP theorem, `FARA-FORMAL-KERNEL-001`, or any bounded result is altered.

No canonical surface, evaluation record, frozen evidence, primitive classification, or software was modified.

---

## 16. Sources, classified

**Corrected 2026-08-10.** The original section was headed "Primary sources" and mixed original papers with encyclopaedia entries, repository mirrors, and later surveys. Sources are now classified by kind. Substantive claims in this record rest on the primary tier; the secondary tier is retained as navigational aid only and carries no evidential weight.

### 16.1 Primary — original works

| Result used | Citation |
|---|---|
| Informativeness order; sufficiency and garbling | D. Blackwell, "Comparison of Experiments", *Proc. 2nd Berkeley Symposium on Mathematical Statistics and Probability* (1951), 93–102; and "Equivalent Comparisons of Experiments", *Annals of Mathematical Statistics* 24(2) (1953), 265–272. |
| Partial order of process semantics by discriminating power | R. J. van Glabbeek, "The Linear Time – Branching Time Spectrum", *CONCUR '90*, LNCS 458 (1990), 278–297; "The Linear Time – Branching Time Spectrum II", *CONCUR '93*, LNCS 715 (1993), 66–81. |
| Institutions; the satisfaction condition | J. A. Goguen and R. M. Burstall, "Institutions: Abstract Model Theory for Specification and Programming", *Journal of the ACM* 39(1) (1992), 95–146. |
| General logics; entailment systems and proof calculi | J. Meseguer, "General Logics", *Logic Colloquium '87*, North-Holland (1989), 275–329. |
| Abstract interpretation; Galois connections; lattice of abstractions | P. Cousot and R. Cousot, "Abstract Interpretation: A Unified Lattice Model for Static Analysis of Programs by Construction or Approximation of Fixpoints", *POPL* (1977), 238–252. |
| Testing equivalences | R. De Nicola and M. Hennessy, "Testing Equivalences for Processes", *Theoretical Computer Science* 34(1–2) (1984), 83–133. |
| Universal coalgebra; behavioural equivalence; finality | J. J. M. M. Rutten, "Universal Coalgebra: A Theory of Systems", *Theoretical Computer Science* 249(1) (2000), 3–80. |
| Nerode congruence; canonical minimal automaton | A. Nerode, "Linear Automaton Transformations", *Proc. AMS* 9(4) (1958), 541–544; J. Myhill, "Finite Automata and the Representation of Events", WADD TR-57-624 (1957). |
| Minimal state-space realization | R. E. Kalman, "Mathematical Description of Linear Dynamical Systems", *SIAM J. Control* 1(2) (1963), 152–192. |
| Multi-extension argumentation semantics (`CE-ADM-001` witnesses) | P. M. Dung, "On the Acceptability of Arguments and its Fundamental Role in Nonmonotonic Reasoning, Logic Programming and n-Person Games", *Artificial Intelligence* 77(2) (1995), 321–357. |
| Ranking-based semantics (used by `OP-14`) | L. Amgoud and J. Ben-Naim, "Ranking-Based Semantics for Argumentation Frameworks", *SUM 2013*, LNCS 8078, 134–147. |

### 16.2 Authoritative technical sources — used for formal definitions only

Final-coalgebra existence and the cardinality obstruction for the powerset functor (Lambek's lemma) and the standard treatment of accessible/bounded functors, as presented in the coalgebra literature; the standard treatment of sufficiency and minimal sufficiency (Fisher; Lehmann–Scheffé) in mathematical statistics; full abstraction as a property of a proposed model (Milner; Plotkin) in programming-language semantics.

### 16.3 Secondary and expository — **not primary; no evidential weight**

Retained only as navigational aids. These are encyclopaedia entries, indexing-service mirrors, later surveys, and expository notes; none is cited in support of a substantive claim above.

- Wikipedia, ["Blackwell's informativeness theorem"](https://en.wikipedia.org/wiki/Blackwell%27s_informativeness_theorem) — *encyclopaedia entry*.
- [Semantic Scholar](https://www.semanticscholar.org/paper/The-Linear-Time-Branching-Time-Spectrum-I-Glabbeek/7fd6e52fa68830a31c86ed9aabc020bb8bb45057) and [ResearchGate](https://www.researchgate.net/publication/228376347_Three_Decades_of_Institution_Theory) records — *indexing-service mirrors of the primary works above; not independent sources*.
- ["Three Decades of Institution Theory"](https://www.researchgate.net/publication/228376347_Three_Decades_of_Institution_Theory) — *later survey*.
- ["Unifying the Linear Time-Branching Time Spectrum of Process Semantics"](https://arxiv.org/abs/1304.6574); ["The Spectrum of Strong Behavioral Equivalences for Nondeterministic and Probabilistic Processes"](https://arxiv.org/pdf/1306.2696) — *later refinements, consistent with but not the source of the claims used*.
- [A Galois Connection Calculus for Abstract Interpretation](https://cs.nyu.edu/~pcousot/publications.www/CousotCousot-POPL14-ACM-p2-3-2014.pdf); [Abstract Interpretation Frameworks](https://faculty.sist.shanghaitech.edu.cn/faculty/songfu/cav/AIF.pdf) — *later expositions by the original authors*.
- [The Method of Coalgebra](https://ir.cwi.nl/pub/28550/rutten.pdf); [Characterising Behavioural Equivalence](https://link.springer.com/content/pdf/10.1007/978-3-642-03741-2_8.pdf) — *expository*.
- [A Congruence-based Perspective on Automata Minimization Algorithms](https://arxiv.org/pdf/1906.06194); [General Myhill–Nerode Theorems](https://coalg.org/cmcs24/papers/2-iwaniack.pdf) — *later generalizations*.
- [Observation equivalence as a testing equivalence](https://www.sciencedirect.com/science/article/pii/030439758790065X); [Definability and full abstraction](https://www.irif.fr/~curien/gordon-fs-plc.pdf) — *related primary work and expository notes respectively, not load-bearing here*.

### 16.4 Verification boundary

Bibliographic details in `§16.1` are recorded from standard citation data. They have **not** been verified against the physical publications by this investigation, and no claim in this record depends on a page range. Any citation found to be inaccurate should be corrected without disturbing the substantive findings, which rest on the results themselves rather than on their pagination.
