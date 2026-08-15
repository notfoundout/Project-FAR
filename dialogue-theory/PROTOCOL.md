# PROTOCOL — recovered specification of the frozen experiment $\mathfrak{E}_0$

Status: **recovered, not redesigned.** Every rule below is transcribed from the supplied
Claude↔GPT dialogue with a source locator. Where the dialogue is ambiguous or silent, that
is recorded as such rather than filled in.

This document is **not** a Project FAR artifact. It records the state of an independent
dialogue-built research programme. Repository governance controls file mutation here; it
does not confer or withhold authority over the mathematical content. See `README.md` in
this directory.

## 0. Source corpus and verification

| ID | File | Coverage | SHA-256 (verified) | Lines |
|---|---|---|---|---|
| `TR-1` | `# CLAUDE TURN 1.md` | turns 1–10 | `2c5bf81202a345ed04e23336c44cf360d559742cb1498cbf3513ac2e38a4ec96` | 7,189 |
| `TR-11` | `# CLAUDE TURN 11.md` | turns 11–30 | `9bf15fbcf3fa775d7855ab8ffd2b9f4fc0e76faa79b02958dc9951bfd686037f` | 10,979 |
| `TR-31` | `# CLAUDE TURN 31.md` | turns 31–35 + GPT 35 | `65146a43ba4c02d652bb598244ee36501ad30268b9bc7ad4be536a974034c347` | 1,622 |

All three hashes match the manifest supplied in the closure prompt. Locators below are
`TR-11:4084` = file `TR-11`, line 4084.

**Turn 36 is NOT in the supplied corpus.** The transcripts terminate at GPT Turn 35
(`TR-31:1622`). The closure prompt's "Adjudicated resume state" summarises a Turn 36 and its
GPT adjudication that are not available as exact text. That summary is used as the resume
state, and is recorded as **`RESUME-SUMMARY`, non-verbatim provenance**. No Turn 36 text is
reconstructed or quoted. Where a terminal claim would depend on Turn 36's exact wording, that
dependency is flagged rather than assumed.

**Known duplications in corpus, de-duplicated:** `TR-11:10142–10405` and `TR-11:10407–10670`
are the identical GPT Turn 29 ruling; `TR-31:500–568` and `TR-31:1098–1166` are the identical
Claude Turns 33–34. No nonidentical variants were found.

## 1. Object of the experiment

Across the preregistered panel $D_0^{\mathrm{plan}}$, determine what semantic vocabulary and
structural laws are genuinely shared, after representation, translation, resources, semantic
resolution, definability, frames and prior art are made explicit.

Ordering of determination: cell-wise interpretability $W^\ast$ → joint interpretability
$J^\ast$ and all joint profiles → maximal jointly interpretable fragments and first-failure
frontiers → common laws beyond frame-forced laws → content not subsumed by prior art → (only
if content survives) definability, dependency, irreducibility, rank, minimality, alternative
bases.

## 2. Staging

$$\mathfrak{E}_0 = \mathfrak{E}_{0a} \oplus \mathfrak{E}_{0b} \oplus \mathfrak{E}_{0c}$$

- **$\mathfrak{E}_{0a}$** — pre-extraction preregistration shell. **FROZEN** at `TR-11:6864`.
- **$\mathfrak{E}_{0b}$** — source stage. Sub-stages `0b.1` (AR2 evidence — voided, see §3),
  `0b.2` (source profiles / $\mathcal{K}_0$), `0b.3` (exact $\mathfrak{R}_S$, exact $\Pi_0$).
- **$\mathfrak{E}_{0c}$** — blinded extraction of $U_0$ with K4 quotations and $\mathrm{Ax}(u)$.

$W^\ast$ begins only after all three hashes exist (`TR-11:4956`).

## 3. $D_0^{\mathrm{plan}}$ — the panel (`TR-11:6404–6418`)

AR2 (three-taxonomy admission) was **deleted in its entirety** at `TR-11:6398`, because its
predicate is ill-defined across selector structures — not because it excluded wanted targets
(binding provenance, `TR-11:6402`). Recorded as **DF-01**.

$$\mathrm{PAR}(S) \iff S \in D_0^{\mathrm{plan}} = \{S1,\ldots,S11\}$$

$$D_0^{\mathrm{plan}} = D_{\mathrm{dev}} \cup D_{\mathrm{adv}}$$

- $D_{\mathrm{dev}} = \{S1,S2,S3,S7,S8,S9,S10\}$ — heterogeneous working panel. **No claim of
  representativeness, breadth, or frequency.** The word "coverage" is retired.
- $D_{\mathrm{adv}} = \{S4,S5,S6,S11\}$ — outcome-aware selection: included because prior
  analysis predicted they would stress candidate universality.

No target may migrate between labels. This is an **explicit methodological sample**, and any
positive result holds only for the stated panel under the stated profiles (`TR-11:6469`).

### Frozen target tuples

Each target is $S_i = (\mathsf{Inst}_i, \mathsf{Native}_i, \mathfrak{R}_i)$ (`TR-11:4067`).

| | $\mathsf{Inst}_i$ | Native state | Native transformation |
|---|---|---|---|
| S1 | finite sequents over a finite propositional signature; Gentzen **LK**, propositional, backward root-first | finite **multiset of open sequents** | one LK rule application |
| S2 | $(V,\mathrm{dom},\mathcal{C},\mathcal{P})$, $\mathcal{P}=\{(c_j,p_j)\}$ finite | domain store $D:V\to\mathcal{P}(\mathrm{dom})$ | one propagator application $D\to p_j(D)$ |
| S3 | finite $(\Omega,P)$ + positive-probability events | distribution | conditioning |
| S4 | finite $(\Omega,P,\mathcal{E})$ + admissible new marginals | distribution | Jeffrey update |
| S5 | finite acyclic discrete SCM | SCM (mechanisms + exogenous dist.) | observation; intervention |
| S6 | finite **MLL** sequents (multiplicative linear logic, no exponentials) | **sequent with resource context** | one rule application |
| S7 | $(C,A,\alpha,\gamma,\mathcal{F},\nabla)$, $\mathcal{F}=\{(f_C,f_A)\}$ finite | abstract element | one transfer / widening step |
| S8 | finitely-branching LTS over finite alphabet | process term / state | labelled step |
| S9 | propositional STRIPS | world state | grounded action application |
| S10 | finite Dung $(\mathcal{A},R)$ | argument graph + labelling | **not pre-assigned** |
| S11 | $(f,n)$, $f$ $C^1$ with globally Lipschitz $\nabla f$ | $\mathbb{R}^n$ | gradient flow $\{\Phi_t\}_{t\ge0}$, $\Phi_{s+t}=\Phi_s\circ\Phi_t$ |

**Determination invariant** (`TR-11:5424`), a standing validation check:
$$a = a' \implies \mathcal{S}_{i,a} = \mathcal{S}_{i,a'}$$
up to the frozen literal representation equivalence. No analyst choice made after the
instance tuple is supplied may be required to construct the native structure. A target
failing this is **UNDERDETERMINED**, never repaired by analyst convention mid-experiment.

**Universally-quantified target theory** (`TR-11:4084`), binding:
$$\mathrm{Th}_L(S_i,J) = \bigcap_{a\in\mathsf{Inst}_i}\mathrm{Th}_L(\mathcal{S}_{i,a},J_a),
\qquad
\mathcal{T}_{c,\mathbf{J}} = \bigcap_{S_i\in D_c}\ \bigcap_{a\in\mathsf{Inst}_i}\mathrm{Th}_{L_c}(\mathcal{S}_{i,a},J_{i,a})$$

A YES certificate must exhibit an interpretation **schema** uniform over $\mathsf{Inst}_i$.
Instance-specific interpretations are inadmissible. This is a **benchmark-free** experiment;
fixed benchmark instances are prohibited within $\mathfrak{E}_0$.

## 4. Instantiation statuses (`TR-11:6422`)

$$\mathrm{Status}(S_i)\in\{\mathbf{READY},\ \mathbf{SOURCE\text{-}FAIL},\ \mathbf{UNDERDETERMINED},\ \mathbf{OPEN}\}$$

$$\boxed{\mathbf{SOURCE\text{-}FAIL} \neq \text{deletion from } D_0^{\mathrm{plan}}}$$

A non-READY target remains a panel member; its failed instantiation is part of the record,
and any claim requiring it returns **UNRESOLVED / DOMAIN-INSTANTIATION FAILURE**.

## 5. Source selection — K-P1…K-P5 (`TR-11:6435`)

- **K-P1** exact-target match: eligible only if the source explicitly formalizes the exact
  frozen target, or the source-defined ancestor from which it is **directly instantiated**.
- **K-P2** primary-source priority.
- **K-P3** no vocabulary inspection before source selection is hashed.
- **K-P4** ambiguity retained: keep the corpus-profile family $\mathfrak{K}_i$, carry its
  index downstream. Never choose the source yielding favourable vocabulary.
- **K-P5** source failure visible: return SOURCE-FAIL; do not alter the target to fit the
  literature found.

K-P1 **gates** K-P4: eligibility is decided before profiling. Sources may evidence the frozen
target; they may not redefine it (`TR-11:8060`).

### K-P1-DI v1 — direct instantiation (`TR-11:8130`, fixed GPT Turn 23)

$$\text{direct instantiation} = \text{specialization} + \text{source-internal definitional expansion}$$

- **DI1** specialization/restriction only — fixing source parameters, restricting to a
  formally specified subclass, forgetting source structure, renaming. Restrictions must be
  stated independently of FAR's results.
- **DI2** source-internal definitional expansion allowed — a component absent as a primitive
  may be admitted if the source formalism makes it **uniquely definable**,
  $x=\operatorname{Def}_A(\ldots)$, fixed uniformly. No analyst choice may remain.
- **DI3** no new primitive structure — forbidden: analyst-selected scheduler, search
  discipline, orientation, update rule, state aggregation, quotient, completion, resource
  policy, equivalence, intervention, control strategy. **Operative test:** if two inequivalent
  additions $X_1\not\equiv X_2$ are compatible with the same source instance, the source does
  not determine $X$, and direct instantiation fails.
- **DI4** no cross-source assembly — taking $X$ from $K_1$ and $Y$ from $K_2$ and declaring
  $(X,Y)$ a direct instantiation is **synthesis, not instantiation**. A single source-defined
  ancestor must support the target bundle, or one source must explicitly define the other
  structure as an extension of its framework.
- **DI5** conservativity — forgetting the introduced structure recovers the source instance.
- **DI6** uniformity/uniqueness — $a=a'\Rightarrow F(a)\equiv F(a')$.

Boundary (`TR-11:8289`): required is **definitionally forced by the source formalism**, not
**easy for an analyst to build**.

### SRF-v1 — source-recognized family (`TR-11:10166`, fixed GPT Turn 29)

$F'$ counts as a source-recognized variant/extension/restriction of frozen $F$ only if the
source itself supplies enough formal information for one of: **restriction** (source
explicitly identifies a fragment $F'_0\cong F$), **extension** (source explicitly presents
$F'$ as extending $F$ with a stated embedding), **variant** (source explicitly relates $F'$
and $F$ by a formal translation preserving the investigated component). Merely knowing
externally that two formalisms are related is insufficient.

$$\text{mathematical embeddability} \neq \text{direct instantiation}$$
$$\text{source-certified specialization, not analyst-recognized reducibility}$$

Corollary (`TR-11:10331`): list $\to$ multiset is DI2 **only** when permutation-invariance
and operation-invariance are source-defined; otherwise DI3.

### CDE-v1 — canonical definitional expansion (`TR-31:635`, fixed GPT Turn 34)

A component $X$ absent as a named primitive in source formalism $A$ is admissible under DI2 if:

1. $X$ is definable solely from source-defined objects, relations, constructors, equality;
2. its definition contains no free methodological parameter;
3. no choice of scheduler, strategy, ordering convention, equivalence, granularity, or
   auxiliary semantics is required;
4. it is invariant under the frozen representation equivalence;
5. its granularity is **anchored by a primitive source constructor**, not chosen by FAR;
6. if the target quotients/forgets source structure, the induced operation is well-defined on
   the quotient.

$$\text{canonical structural consequence} \neq \text{analyst-designed additional structure}$$

**CDE-v1 provenance risk (`TR-31:1597`, must remain attached to any certificate using it):**
introduced in GPT Turn 34 *after* the Liang–Miller partial-derivation evidence was known and
*after* the direction of its consequence for S1 was disclosed. This does not invalidate the
rule, but later robustness work should attempt to defeat CDE-v1 on unrelated source/target
pairs. The existing over-generation checks are not a proof that the rule is optimally
restrictive.

## 6. SR-B2 v2 — frozen retrieval completion procedure (`TR-11:9484`, GPT Turn 26)

SR-B2 **v1 retired as PROCEDURE-INEXECUTABLE** (`TR-11:9474`); no target verdict derives from
it; its searches are exploratory provenance only and consume no v2 allocation. Recorded as
**DF-05 — SR-B2 v1 procedure inexecutability**, classified as procedure inexecutability, *not*
a result about the theory or the domain.

Applies identically to every target still OPEN after $B_1$.

Let $F_i$ = exact frozen formalism name; $C_i$ = exact disputed component from the frozen
target specification.

**Channel A — fixed query battery, exactly six, not modified after seeing results:**

1. `"<F_i>" "<C_i>"`
2. `"<F_i>" "formal definition" "<C_i>"`
3. `"<F_i>" semantics "<C_i>"`
4. `"<F_i>" "operational semantics" "<C_i>"`
5. `"<F_i>" formalization "<C_i>"`
6. `"<F_i>" definition`

Inspect every result returned by one normal search invocation, capped at 10. The budget unit
is **one executable search invocation**, not an assumed result count. A query returning zero
results is a completed invocation and does not authorize replacement.

**Channel B — deterministic source-name follow-up (no citation indexing):**

Build $N_i$ of near-match named sources under **NM-v1**: a candidate enters iff its
title/abstract/snippet explicitly concerns (**NM1**) the frozen formalism $F_i$ *or* a
source-recognized direct family member under SRF-v1, and (**NM2**) formal definition,
semantics, or formalization of the disputed component $C_i$, with (**NM3**) plausible
provenance path. Membership is decided from title/abstract/snippet **only**, before full-text
evaluation. Same structural role is NM2 and **cannot** substitute for NM1 (`TR-11:10148`).

At most **5** near-matches, ordered by first appearance in the fixed Channel-A query sequence,
then search-result order. No retrospective usefulness ranking; do not manufacture a fifth.
For each selected near-match with title $T$ and first author $A$, run exactly two follow-ups:

7. `"<T>" "<A>"`
8. `"<A>" "<F_i>" "<C_i>"`

**Retrieval/admissibility firewall:** broad retrieval gate, strict evidentiary gate. $N_i$
membership carries **no** implication of K-P1 eligibility.

**Candidate scope (`TR-11:10752`, GPT Turn 30):** a returned candidate is *a top-level
document/result emitted by a prescribed search invocation*. It does **not** recursively
include references, bibliography entries, footnotes, hyperlinks, or works mentioned in prose.
Those are **UNFOLLOWED BIBLIOGRAPHIC LEADS**, logged as $L_i$, with zero stopping or
eligibility authority. No recursive bibliography retrieval in $\mathfrak{E}_0$.

**Evaluation order:** K-P1 → DI1–DI6 → K-P2 → K-P4. Verdicts: EXACT, DIRECT, INELIGIBLE.

**Terminal statuses after all required invocations:**
- **READY** — at least one EXACT or DIRECT source exists.
- **SOURCE-FAIL$_{\mathrm{SR\text{-}B2v2}}$** — all prescribed invocations executed and no
  eligible source found.
- **OPEN$_{\mathrm{retrieval}}$** — a prescribed invocation could not be executed (tool/service
  failure).

**Early stopping (`TR-11:9575`, `TR-11:10085`):** asymmetric and logical, not preferential.
$$\text{positive certificate}\Rightarrow\text{early stop permitted};\qquad
\text{apparent saturation}\Rightarrow\text{early stop forbidden}$$
An EXACT/DIRECT certificate is existentially decisive ⇒ READY, remaining invocations not
required for instantiation status. SOURCE-FAIL requires **all** v2 invocations to complete.
No saturation stopping, no $k$-rule, no cost-based truncation (`TR-11:9959`, `TR-11:10061`).
Saturation is recorded descriptively via the novelty sequence
$\mathrm{Novel}_j = R(Q_j)\setminus\bigcup_{m<j}R(Q_m)$ with **zero stopping authority**.

**RD-01 (`TR-11:10890`):** SOURCE-FAIL under SR-B2 v2 means failure under this bounded
retrieval design, **not** exhaustion of the scholarly citation graph.

## 7. TSI-v1 — targeted source inspection (`TR-31:98`, GPT Turn 31)

Three candidate states: **INELIGIBLE**, **ELIGIBLE**, **REQUIRES INSPECTION**. Absence from a
snippet is almost never evidence of absence from the source.

**SI-CERT — when snippet-level INELIGIBLE suffices.** All three required:
- **SI1** the snippet explicitly identifies the formalism the source defines;
- **SI2** it affirmatively states a defining property incompatible with the frozen target;
- **SI3** the incompatibility is such that specialization or source-internal definitional
  expansion cannot yield the frozen target.

"This paper is focused/polarized" satisfies SI1–SI2 but **not** SI3: it establishes only that
*the focused formalism* is not the frozen target, not that the whole source is ineligible —
the document may still define the ordinary calculus first, as a comparison object
(`TR-31:85`). Uninformative snippet ⇒ **REQUIRES INSPECTION**, never INELIGIBLE.

**TSI-v1 inspection procedure.** Inspect, when accessible: abstract; introduction; the section
containing the formal definition of the calculus/formalism; the section containing
proof-search semantics/algorithm/operational description if present; conclusion only if
needed. Search within the document for mechanically fixed terms derived from the frozen
disputed component. No other exploratory reading is required unless a passage creates a
plausible EXACT/DIRECT route needing verification.

**Terminal rules.** EXACT ⇒ READY. DIRECT (DI1–DI6/SRF-v1) ⇒ READY. INELIGIBLE$_{TSI}$ if the
inspected source positively establishes a different organization *and* no exact/direct
formalization appears in the inspected definitional/search sections.
**INSPECTION-OPEN** if the document is inaccessible or relevant sections cannot be inspected —
such a candidate can never be counted INELIGIBLE, and if any required candidate remains
INSPECTION-OPEN the target cannot receive SOURCE-FAIL.

Full-document exhaustive negative proof is **not** required. EXACT/DIRECT always require
source inspection; never a snippet alone. Applies identically to every OPEN target; do not
inspect S1 more deeply because it controls $R_{\mathrm{primary}}$.

## 8. FDI-v1 / MFDI-v1 — frontier certificates

### FDI-v1 (`TR-31:312`, GPT Turn 32) — for partial-derivation routes

- **FDI1** partial derivations are source-defined (not invented by the analyst).
- **FDI2** open leaves/frontier are source-internal — the closed/open leaf distinction is
  load-bearing and must be source-made.
- **FDI3** frontier multiplicity fixed (set vs sequence vs multiset not left open).
- **FDI4** one-step frontier evolution is source-induced. **Nondeterminism does not trigger
  DI3** — if all applicable expansions are included, no selection policy has been added.
- **FDI5** frontier quotient behaviorally well-defined:
  $\operatorname{Fr}(T_1)=\operatorname{Fr}(T_2)\Rightarrow$ the induced successor-frontier
  sets agree. Fails if tree history, eigenvariable conditions, branch-local annotations, or
  focusing state can alter legal expansion.

Boundary (`TR-31:435`): count a derived component as DI2 only when it is part of the source's
**formal apparatus for the target phenomenon** — explicitly defined, used in its
rules/semantics, or definitionally required by those rules.

### MFDI-v1 (`TR-31:1375`, GPT Turn 35) — S6-specific, applied de novo

**CDE-v1 has zero automatic transfer power** (`TR-31:1282`). No lemma "partial derivations ⇒
frozen search system" has been proved. S6 starts with **no inherited FDI3/4/5 verdicts**, and
therefore remains informative for DF-04-H.

- **MFDI1** source-defined incomplete derivations (pending premises may remain open).
- **MFDI2** resource-sensitive rule instances are source-determined: the source formalism
  itself determines available resources, legal partitions/splits, and resulting premise
  sequents. All admissible splits may be retained ⇒ **resource nondeterminism is harmless**.
- **MFDI3** pending obligations retain multiplicity **and resource content** — may not
  collapse $(\Gamma\vdash A,\ \Delta\vdash B)$ into a representation forgetting which
  resources belong to which obligation.
- **MFDI4** one-step extension preserves premise grouping — $\{P_1,\ldots,P_n\}$ is **one
  jointly generated premise family**. A hyperedge $S\to\{P_1,\ldots,P_n\}$ or a frontier
  update $M\to M-[S]+[P_1]+\cdots+[P_n]$ can do this; independent ordinary edges $S\to P_i$
  generally cannot (AND misread as OR).
- **MFDI5** state sufficiency / quotient well-definedness: $q(D_1)=q(D_2)$ must imply equality
  of induced successor structures including resource partitions and joint premise families.
- **MFDI6** no hidden branch history — legal future expansion may not depend on information
  the frozen state discards (sibling provenance, unrepresented resource allocation, proof-net
  linkage, focusing phase, branch-local annotations).

**Binding constraints (`TR-31:1611`):** resource splitting alone does not imply failure; do
**not** modify the frozen S6 state to help it pass; do **not** make resource sensitivity fail
by definition — $D_{\mathrm{adv}}$ membership is a selection rationale, never an expectation
that S6 must fail. Either outcome is informative.

## 9. Interpretation grammars (`TR-11:5404`, Turn 18 final)

| | $G_1$ literal | $G_2$ parameter-free FO definable | $G_3$ parameter-free FO interpretation |
|---|---|---|---|
| sorts | native carrier as-is | FO-definable $D\subseteq A_{i_1}\times\cdots\times A_{i_n}$ | as $G_2$ + quotient $D/E$, $E$ FO-definable |
| relations | native primitive | FO-definable | as $G_2$, $E$-invariance proved |
| operations | native primitive | FO-definable graph, existence+uniqueness proved | as $G_2$, $E$-invariance proved |
| parameters | none | none | none |
| uniformity | over all $a\in\mathsf{Inst}_i$ | same | same |

$G_1\subseteq G_2\subseteq G_3$ = literal ⊆ definable ⊆ interpretable-up-to-definable-quotient.
Excluded from all three: second-order, recursive, arbitrary computable maps, external
constructions, non-FO-induced functors. Any parameterized grammar is $G_4$, in a separately
versioned experiment.

Cell status is grammar-indexed: $W^\ast_{G_k}(S_i,u)$,
$\mathbf{NO}_{G_k}\iff\mathsf{Int}_{G_k}(S_i,u)=\varnothing$. The **first grammar level
admitting a witness is a reported boundary datum**. No claim may be stated without its
grammar index.

## 10. Witness rules

**YES** (`TR-11:4934`) requires all of: (1) an interpretation schema $I_{i,u}$ in grammar
$G_k$, uniform over $\mathsf{Inst}_i$; (2) the profile $r\in\mathfrak{R}_i$ named; (3) proof of
$E_{i,r}$-factorization; (4) proof of $O_{i,r}$-respect; (5) $I_{i,u}\models\mathrm{Ax}(u)$ —
the interpretation satisfies the item's full constitutive package. No RCCD vocabulary in the
definition.

**NO$_{G_k}$** requires proof that $\mathsf{Int}_{G_k}(S_i,u)=\varnothing$. Admissible forms:
typing/arity obstruction; invariant violation; cardinality obstruction; $E$-factorization
failure at *every* $r\in\mathfrak{R}_i$; countermodel pair; cited impossibility theorem.
**"No source mentions it" is never a NO.**

**OPEN** — everything else, including unreached cells. OPEN never counts as NO. Any claim
depending on an OPEN cell returns UNRESOLVED.

**Dual search streams** (`TR-11:3232`): per reached cell, independent preregistered budgets
$B^{\mathrm{YES}}_{\mathrm{cell}}$ and $B^{\mathrm{NO}}_{\mathrm{cell}}$, run independently, no
adaptive transfer. First success closes the cell. **Both succeeding ⇒ CERTIFICATE
INCONSISTENCY, halt cell for audit, do not choose a verdict.**

Known bias, stated in every report (`TR-11:3350`): NO certificates remain rare, so the measured
boundary is systematically **wider** than the true one. No correction available.

## 11. Joint rules (`TR-11:3252`)

- $\mathfrak{J}_c$ — the mathematical class of all admissible joint profiles. **Possibly
  infinite. No enumeration claim.**
- $\widehat{\mathfrak{J}}_{c,B}$ — certificates actually established under $B$.
- **JOINT-COMPLETE** — a *proof* that $\widehat{\mathfrak{J}}_{c,B}=\mathfrak{J}_c$. Only then
  may exhaustive enumeration be claimed.

Statuses: **JOINT-YES** ($\widehat{\mathfrak{J}}_{c,B}\neq\varnothing$); **JOINT-NO** (proof
that $\mathfrak{J}_c=\varnothing$ — an incompatibility certificate); **JOINT-OPEN**.
Cell status does not imply joint status. $\mathcal{T}^{\mathrm{rob}}_c$ may not be claimed
exact absent JOINT-COMPLETE.

## 12. Frames — interface-only, mechanically generated (`TR-11:4173`)

$$\Gamma_{c,\mathbf{J}} = \underbrace{\bigcup_{u\in L_c}\mathrm{tr}_{\mathbf{J}}(\mathrm{Ax}(u))}_{\text{(i) translated source axioms}} \cup \underbrace{\Sigma_{\mathbf{J}}}_{\text{(ii) sort/typing laws forced by }J} \cup \underbrace{\Xi}_{\text{(iii) host equality/congruence}}$$

Nothing else. **No sentence may enter $\Gamma$ because it holds in the targets**, or because
the interpretation makes it convenient.

$$\mathcal{F}_{c,\mathbf{J}}=\mathrm{Cn}_{L_c}(\Gamma_{c,\mathbf{J}}),\qquad
\mathcal{C}_{c,\mathbf{J}}\neq\varnothing \iff \mathcal{T}_{c,\mathbf{J}}\not\subseteq\mathcal{F}_{c,\mathbf{J}}$$

**Binding ordering:** $\Gamma_{c,\mathbf{J}}$ is generated and hashed from $\mathrm{Ax}$ and
$J$ *before* $\mathcal{T}_{c,\mathbf{J}}$ is computed. Ordering, not just definition, is what
prevents the collapse. Several admissible minimal interface theories ⇒ retain the family
$\mathfrak{F}_{c,\mathbf{J}}$, index results, report per member.

$\mathrm{Ax}(u)$ = axioms/definitional conditions the source states as **constitutive** of
$u$, never downstream propositions involving $u$; each with K4 verbatim quotation.

## 13. $U_0$ registry (`TR-11:2084`, `TR-11:4120`)

- **U-a** extract only items the source itself formally designates as basic in its
  definitional apparatus. Theorems, lemmas, named results excluded.
- **U-b** $m\le 8$ items per source, in the source's own order of first definition.
- **U-c** extraction is per-target and **blind**: the extractor may not see other targets'
  extractions, nor the RCCD vocabulary list.
- **U-d (replaced at `TR-11:4124`) — retention, not exclusion.** No item enters $U_0$ because
  FAR/RCCD supplied it; every item extracted by the frozen rule **stays**, including items
  whose native names resemble Construct, Differentiate, Restrict, Resolve. Registry IDs
  $u_1,u_2,\ldots$ in extraction order; **all downstream work uses IDs only**; source term,
  K4 quotation and citation are provenance metadata **quarantined until Q4**. Symmetric: no
  RCCD insertion, no RCCD-driven deletion.
- **U-e** duplicates retained with distinct identifiers; extensional coincidence is reported
  as *indistinguishable at resolution $|D_0|$*, never as identity.
- **K4** every extracted item carries a verbatim quotation plus page reference.

## 14. Two arms (`TR-11:4136`) and coverage

- **Calibration arm** $\mathcal{G}_0^{\mathrm{cal}}=\{c_0\}\cup\{c_0+u:u\in U_0\}$, with
  $c_0=(\{S1,S2\},L_\to)$. **Explicitly dialogue-derived**; every report carries the label
  *"dialogue-derived preregistered calibration fragment"*; may not be described as unbiased
  discovery.
- **Native-registry arm** $\mathcal{G}_0^{\mathrm{native}}=\{(\{S1,S2\},\{u\}):u\in U_0\}$ —
  source-blind.

Results from the two arms are reported separately and **may never be pooled into a single
discovery rate** (`TR-11:4960`). Pairwise and higher combinations require a separately
versioned $\mathfrak{E}_1$.

**Mandatory (exhaustively attempted) stratum:** all cells $(S,u)$ for $S\in\{S1,S2\}$,
$u\in U_0$, plus joint certificates for every $c$ in both arms. **Secondary (sampled):**
remaining cells under $\sigma$ = lexicographic on
$\mathrm{SHA256}(\texttt{target\_id}\Vert\texttt{item\_id}\Vert\texttt{seed})$, seed published
at freeze. Sampled results characterize $\widehat{W}^\ast_B$ only and **may not support any
maximality claim**.

**Boundary object** (`TR-11:3275`):
$\partial_1(c)=\{u\in U_0\setminus L_c : c+u \text{ is JOINT-NO}\}$, with
$\partial_1^{\mathrm{OPEN}}(c)$ reported separately. **No maximality or complete-boundary
claim while $\partial_1^{\mathrm{OPEN}}\neq\varnothing$.**

## 15. Budgets (`TR-11:3296`)

| | $B_1$ | $B_2$ |
|---|---|---|
| Mandatory stratum | complete | complete |
| Secondary cells | first 100 under $\sigma$ | first 400 under $\sigma$ |
| Per cell | dual YES/NO streams, ≤1 page each | + machine assistance |
| Prior art | $\Pi_0$ only | $\Pi_0+\Pi^{\mathrm{search}}_B$ |

Report $W^\ast_{B_1}\to W^\ast_{B_2}$ movement and $R_B=(N_Y,N_N,N_O)$ globally and per
fragment. Budget monotonicity: $B_1\subsetneq B_2$.

## 16. Prior art (`TR-11:3287`)

**$\Pi_0$** — frozen composite, fixed at $\mathfrak{E}_{0b}$: institutions and
institution-independent model theory; MMT/theory morphisms; FCA/Chu/Barwise–Seligman;
categorical logic and doctrines; Markov and CD categories; effectus theory; restriction
categories; abstract interpretation and Galois connections; Pearl's causal hierarchy;
substructural and monoidal resource theory; universal algebra and coalgebra; rewriting logic.

**$\Pi^{\mathrm{search}}_B$** — prior art found under preregistered external search. May
destroy a provisional novelty claim; may never retroactively redefine $\Pi_0$.

**Three levels, never conflated** (`TR-11:4187`): $\mathcal{C}$ (substantive content);
$\mathcal{N}^{\Pi_0}$ (not subsumed by the frozen baseline);
$\widehat{\mathcal{N}}^{\mathrm{search}}_B$ (no subsumption found under search budget $B$).
The unqualified word "novel" requires human literature review beyond this experiment.
If a $\Pi_0$ translation certificate is OPEN, novelty is **UNRESOLVED, never positive**.

## 17. Obligation ordering (`TR-11:3309`)

$$\text{P2a}\to\text{P2b}\to\text{P1}\to\text{A1}/\partial_1\to\text{P3 (Resolve)}\to\text{P4 (Construct)}\to\text{P6 (Restrict/Cockett–Lack)}\to\text{P5}\to\text{P7}\to\text{P8}\to\text{P9}$$

P2a = joint existence per fragment; P2b = does $\mathcal{T}_{c,\mathbf{J}}$ depend on
$\mathbf{J}$?; P1 = content of the maximal witnessed language. **Rank questions are not opened
until P1 returns.**

## 18. Counterexample registry C1–C12 (`TR-11:2222`)

Append-only, five verdict types (*defeats / narrows / requires revision / exposes assumption /
fails*). Every candidate must be run against all twelve before report.

C1 Galois antitonicity · C2 van Glabbeek spectrum · C3 $(\mathbb{R},\le)$ dense factorization ·
C4 idempotent monoid · C5 NAND vs $\{\neg,\wedge\}$ · C6 Janov–Mučnik · C7 Markov
non-naturality of $\Delta$ · C8 $R_P$ nonconstant · C9 $d_P$ not from $\Delta$ ·
C10 $P(y|x)\neq P(y|do(x))$ · C11 Boolean $d_P=(R_P,R_{\neg P})$ · C12 $\sqsubseteq$ failure.

## 19. Preregistered prediction A2 (`TR-11:3319`)

> $c_0=(\{S1,S2\},L_\to)$: **JOINT-YES**, and
> $\mathcal{T}_{c_0,\mathbf{J}}\subseteq\mathcal{F}_{c_0,\mathbf{J}}=\mathrm{Cn}(\varnothing)$ —
> i.e. $\mathcal{C}_{c_0}=\varnothing$, no non-logical law shared. Interest, if any, lies in
> $\partial_1(c_0)$.
>
> **Falsified by:** any $L_\to$-sentence true in both S1 and S2 that is not logically valid.
> **Registered by:** Claude, Turn 13, before extraction.

Sharpened form (`TR-11:4088`): *every first-order directed-graph sentence true of every
admissible LK proof-search graph and every admissible CSP propagation graph is logically
valid.*

$L_\to$ is dialogue-constructed, has no source, hence no $\mathrm{Ax}$; $\Sigma_{\mathbf{J}}$
is empty; so $\Gamma_{c_0}=\varnothing$ and $\mathcal{F}_{c_0}=\mathrm{Cn}(\varnothing)$.

## 20. Immutability (`TR-11:3333`)

**Immutable after hash:** target tuples; selector schemes; source-selection rule;
$\mathfrak{R}_S$; YES/NO/OPEN, JOINT and JOINT-COMPLETE rules; $\mathcal{G}_0$; $\sigma$ and
seed; $B_1,B_2$; C1–C12; obligation ordering; report formats; the A2 prediction; and — once
produced — $\mathcal{K}_0$, $U_0$, $\Pi_0$, and each $\Gamma_{c,\mathbf{J}}$ once written.

**Never permitted:** target removal; symbol addition; frame weakening; profile selection;
re-specification of $O_{i,r}$ after results; outcome-contingent budget extension; sentences
entering $\Gamma$ because they hold in the targets.

**Permitted:** FRAME FAILURE, JOINT-NO, CERTIFICATE INCONSISTENCY, and negative results of
every type. Any desired change opens a separately versioned $\mathfrak{E}_1$, evaluated from
zero.

## 21. Stop conditions (`TR-11:3327`)

**Experiment terminates** when: mandatory stratum complete; secondary cells reached under $B$
have status; every fragment has a joint status; every JOINT-YES fragment has an R1/R2/R3
verdict. **Termination does not require mathematical resolution.**

**Program level — two outcomes, never conflated:**
- **FALSIFIED** — only where a proof establishes the relevant negative (R1 completeness or
  R2 joint separation).
- **ABANDONED AS UNRESOLVED** — preregistered limits reached without resolution. Three
  experiments returning UNRESOLVED justify stopping; they do **not** falsify.
  (Turn 9: unsupported $\neq$ false.)

## 22. Standing findings ledger

| ID | Statement | Status |
|---|---|---|
| DF-01 | Taxonomy non-comparability: AR2's selectors classify different kinds/granularities of scholarly object, so "top-level presence in two selectors" defined no uniform predicate. A failure of AR2, **not** evidence any target is illegitimate. | Recorded |
| DF-02 | Absent native transformation structure in retrieved primary sources. | Superseded by DF-02b / DF-04-H |
| DF-02b | Revised wording (`TR-31:508`): *No eligible source encountered so far has been certified to determine the frozen frontier-level search structure.* NOT "the calculus does not determine search structure." | Recorded |
| DF-03 | Make every source-native first-class object an explicit native sort; do not add set-sorts to enable later interpretations. Where a source does not treat such objects as first-class in an FO-compatible signature, the limitation stays visible. | Recorded |
| DF-04-H | **Constructed-schema exposure (hypothesis).** Where a target's dynamics is source-native, the schema passes K-P1; where the analyst supplied the dynamics, K-P1 exposes it. **Frozen evaluation point: after terminal source statuses for all eleven.** Wording not to be adjusted to outcomes. Took a direct counter-hit from S1 (`TR-31:1031`) — *dialogue-assembled* ≠ *not source-grounded*. | **Live hypothesis** |
| DF-05 | SR-B2 v1 procedure inexecutability. Classified as procedure inexecutability, not a result about theory or domain. Must not be generalized into "the experiment is inexecutable." | Recorded |
| RD-01 | Unfollowed citation leads: SR-B2 v2 evaluates only top-level results; relevant references inside returned documents are logged ($L_i$) but not retrieved. SOURCE-FAIL under v2 ≠ exhaustion of the citation graph. | Recorded, descriptive |
| N6 | Domain-criterion regress — **OPEN**. "We could not find a suitable taxonomy" is *not* N6. | OPEN |

## 23. Two-stage logic (`TR-11:6471`)

- **Finite panel** — discovery and falsification only.
- **Formal class theorem** — generalization, with Stage-B admission predicate $A$ subject to:
  candidate independence · **native determinacy** (stated in candidate-independent
  native/formal properties, truth value fixed independently of the candidate conclusion,
  whether or not an algorithm decides it) · nontrivial extension · counterexample openness ·
  **proof rather than finite-panel induction**.

*"Broadest independently justified class"* becomes inclusion between provable class theorems,
$\mathcal{C}_{A_1}\subseteq\mathcal{C}_{A_2}$ — not a frequency claim about literature.

Negative results retain full force: one panel member satisfying an independently stated class
predicate and lacking $P$ refutes $\forall S\in C.\,P(S)$, no sample required.

## 24. Panel-sensitivity limitation (`TR-11:6479`)

The panel's composition is a methodological choice of the same kind as $m\le8$ or the choice
of three grammars. Had eleven different schemas been chosen, a different $\partial_1$,
different joint failures, and a different $\mathcal{T}_c$ might result. Panel sensitivity is
untested and, at $|D_0^{\mathrm{plan}}|=11$, **untestable within $\mathfrak{E}_0$**. The
correction is not a bigger panel — it is Stage B.
