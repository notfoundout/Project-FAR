# K4 records — per-target primitive extraction

K4 requires, for every extracted item, a **verbatim quotation** of the passage in which the
source designates it primitive, plus an exact locator (`TR-11:2076`). U-a restricts extraction
to items the source itself formally designates as basic in its definitional apparatus —
signature entries, primitive relations/operations, defined-as-basic notions; theorems, lemmas
and named results are excluded. U-b bounds each source at $m\le 8$ items, taken in the source's
own order of first definition. U-e retains duplicates with distinct identifiers.

The original S1/S6/S7 records below are preserved. Eight additional records were made under
`E1-transparent-source-recovery`. They complete the source-local extraction but do **not**
retroactively satisfy frozen U-c: the present analyst had already seen cross-target material.
The successor replaces cognitive blindness with a logged procedural isolation rule and labels
the resulting registry `U0-E1`. This is a limitation, not a hidden compliance claim.

**Transcription note.** In `SS-CC92` the flat/sharp superscripts distinguishing concrete
$P^\flat$ from abstract $P^\sharp$ are typographic and are lost by text extraction; they are
restored below in square brackets and marked. In `SS-GP94` all quotations are OCR
transcriptions of a bitmap-font body and are marked `[OCR]`.

Registry IDs are assigned only in sealed `U0.json`, in target order and then source order.
Every table has exactly eight entries, so $|U0\text{-}E1|=88$.

---

## K4 / S1 — `SS-LM24`

C. Liang & D. Miller, *Focusing Gentzen's LK Proof System*, in T. Piecha & K. F. Wehmeier
(eds.), *Peter Schroeder-Heister on Proof-Theoretic Semantics*, Springer, 2024, chapter 9,
pp. 275ff.; DOI `10.1007/978-3-031-50981-0_9`. SHA-256
`044ac192a6fcdea5425a068a254dea99ca32c3a60f3441bbf1bf4b2bfca465ef`.

**Procedure: ORIGINAL.** This is frozen $N_1$ **member 2** (`TR-11:10689`), in the frozen
near-match set before supply. Text layer present; no OCR required. Identity verified from the
chapter title block, author block, and the volume statement on printed p. 275.

Corpus profile: $K_{1,\mathrm{L\&M}}$ — the profile already carried by S1's certificate.

| # | Item | Verbatim designation | Locator |
|---|---|---|---|
| 1 | atomic formula | "Atomic formulas are of the form $P(t_1,\ldots,t_n)$, where $n\ge0$, $P$ is a predicate of arity $n$, and $t_1,\ldots,t_n$ is a list of first-order terms." | §2, p. 277 |
| 2 | formula | "Formulas are built from atomic formulas using both the logical connectives $\wedge$, t, $\vee$, f, $\supset$ as well as the two first-order quantifiers $\forall$ and $\exists$." | §2, p. 277 |
| 3 | substitution | "the expression $[s/x]B$ denotes the result of performing a capture-avoiding substitution of term $s$ for all free occurrences of the variable $x$ in the formula $B$." | §2, p. 277 |
| 4 | sequent | "Inference rules are between sequents which are **pairs of multisets of formula**, formally written with an infix $\vdash$." | §2, p. 277 |
| 5 | the LK inference rules | "Figure 1 presents the LK sequent proof calculus of Gentzen (1935). … The rules there are divided into introduction rules, structural rules, and identity rules." | §2 and Fig. 1, p. 277 |
| 6 | structural rules cL, cR, wL, wR | displayed under the heading "**Structural rules**": $\dfrac{\Gamma,B,B\vdash\Delta}{\Gamma,B\vdash\Delta}\,cL$, $\dfrac{\Gamma\vdash\Delta,B,B}{\Gamma\vdash\Delta,B}\,cR$, $\dfrac{\Gamma\vdash\Delta}{\Gamma,B\vdash\Delta}\,wL$, $\dfrac{\Gamma\vdash\Delta}{\Gamma\vdash\Delta,B}\,wR$ | Fig. 1, p. 277 |
| 7 | proof | "By **proof**, we mean a tree structure of inference rules and sequents such that all premises are closed, in the sense that the inference rules at the leaves have zero premises (such as the initial rule)." | §2, p. 278 |
| 8 | derivation | "By **derivation**, we mean a similar tree structure of inference rules and sequents, but we do not assume that all leaves are closed: **derivations can have unproved premises**." | §2, p. 278 |

$m=8$, the U-b bound, reached. Later definitional material (polarized formulas; the LKF
sequents $\vdash\Gamma\Uparrow\Theta$ and $\vdash A\Downarrow\Theta$; storage) falls outside the
bound, and the cut point is the source's own definition order.

### $\mathrm{Ax}(u)$ packages carried

- $\mathrm{Ax}(\text{4})$ — that a sequent is a **pair of multisets**, and the source's own
  statement of what this changes: "In Gentzen's system, contexts are lists of formulas, and the
  exchange rule, which allowed two adjacent formulas to be swapped, was used. In Figure 1,
  contexts ($\Gamma$ and $\Delta$) are multisets of formulas, and **the exchange rule is not
  used**." (§2, p. 277, difference 1). This is the constitutive representation law and is the
  load-bearing $\mathrm{Ax}$ item for T4.
- $\mathrm{Ax}(\text{7,8})$ — the closed/unclosed leaf distinction quoted above, which is what
  makes FDI1 and FDI2 source-satisfied.
- $\mathrm{Ax}(\text{5,6})$ — the displayed rule schemata of Fig. 1, p. 277, with the side
  conditions stated in the caption: "In the $\forall R$ and $\exists L$ rules, the variable $y$
  is not free in the conclusion. In the $\wedge L$ and $\vee R$ rules, $i\in\{1,2\}$. In
  $\forall L$ and $\exists R$, $s$ is a first-order term."

---

## K4 / S7 — `SS-CC92`

P. Cousot & R. Cousot, *Abstract Interpretation Frameworks*, J. Logic and Computation
2(4):511–547, 1992. SHA-256 `19591e44…5f89bb`.

Corpus profile: single eligible profile identified; no K-P4 split recorded at this stage.

| # | Item | Verbatim designation | Locator |
|---|---|---|---|
| 1 | concrete semantic domain $P^\flat$ | "The concrete semantics describes properties of the possible executions of a program represented by means of concrete semantic properties $c$ chosen in a given set $P^{[\flat]}$ called the **concrete semantic domain**." | §3, p. 513 |
| 2 | concrete semantic function $F^\flat$ | "the concrete iteration is often specified by transfinite recursion using a basis $\bot^{[\flat]}\in P^{[\flat]}$, a partial map $F^{[\flat]}\in P^{[\flat]}\mapsto P^{[\flat]}$ called the **concrete semantic function**" | §3, p. 514, in the definition of (4.1) |
| 3 | inductive join $\sqcup^\flat$ | "and an **inductive join** $\sqcup^{[\flat]}\in\wp(P^{[\flat]})\mapsto P^{[\flat]}$ so that:" | §3, p. 514, in the definition of (4.1) |
| 4 | widening $\nabla$ | "we can use extrapolation operators: $\nabla\in\wp(P^{[\sharp]})\mapsto P^{[\sharp]}$ **widening**" | §4, eq. (4.6), p. 517 |
| 5 | narrowing $\Delta$ | "$\Delta\in\wp(P^{[\sharp]})\mapsto P^{[\sharp]}$ **narrowing**" | §4, eq. (4.6), p. 517 |
| 6 | abstraction map $\alpha$ | "The correspondence between concrete and abstract properties is given by a Galois connection … that is an **abstraction map** $\alpha\in P^{[\flat]}\to P^{[\sharp]}$ and a concretization map $\gamma\in P^{[\sharp]}\to P^{[\flat]}$ such that, by definition: $\forall c\in P^{[\flat]}:\forall a\in P^{[\sharp]}:\alpha(c)\sqsubseteq^{[\sharp]}a\Leftrightarrow c\sqsubseteq^{[\flat]}\gamma(a)$." | Example 4.6, eq. (4.12), p. 518 |
| 7 | concretization map $\gamma$ | same passage as #6 ("and a **concretization map** $\gamma\in P^{[\sharp]}\to P^{[\flat]}$") | Example 4.6, eq. (4.12), p. 518 |
| 8 | approximation pre-order $\sqsubseteq$ | "We now examine a framework in which the notion of precision is formalized on the abstract properties using an **approximation relation** $\sqsubseteq$: $\sqsubseteq\in\wp(P^{[\sharp]}\times P^{[\sharp]})$ is a pre-order" | §6 opening, eq. (4.18), p. 520 |

$m=8$, the U-b bound, reached. Items defined later in the source (soundness relation $\sigma$;
computational ordering $\preceq$; abstract basis $\bot^\sharp$) are **excluded by the bound**,
not by judgement, and the cut point is the source's own definition order.

### $\mathrm{Ax}(u)$ packages carried

- $\mathrm{Ax}(\text{6,7})$ — the adjunction (4.12), quoted above, is stated by the source as
  the *definition* of the Galois connection and is therefore constitutive.
- $\mathrm{Ax}(\text{4})$ — "$\nabla A$ exists $\wedge\ a\in A\Rightarrow a\sqsubseteq\nabla A$"
  (eq. (4.39), p. 531), glossed by the source as "which holds when the widening is a partially
  defined upper bound in $P^{[\sharp]}$ (but not necessarily the least one)"; and the
  stabilisation condition "For every $\mathbb{N}$-termed sequence $x_0,\ldots,x_i,\ldots$ in
  $P^{[\sharp]}$, the chain $y_0=x_0\ \ldots\ y_{i+1}=y_i\nabla x_i\ \ldots$ is not strictly
  increasing" (Prop. 6.20, condition list (4.46), p. 537).
- $\mathrm{Ax}(\text{1,2,3})$ — the iteration scheme (4.1), p. 514.
- $\mathrm{Ax}(\text{8})$ — "is a pre-order", (4.18), p. 520.

Downstream propositions *involving* these items (Prop. 6.14, 6.17, 6.20 as results) are
**not** $\mathrm{Ax}$ material; only the constitutive conditions are (`TR-11:4944`).

---

## K4 / S6 — `SS-GP94`

D. Galmiche & G. Perrier, *Foundations of Proof Search Strategies Design in Linear Logic*,
LFCS 1994, pp. 101–113; HAL `hal-01297758`. SHA-256 `622f2f9e…3132ee`.

**Procedure attribution:** extracted under `E0-supplied-v1`, not under original
$\mathfrak{E}_0$. Under the original procedure S6 has no eligible inspected source and hence no
K4 record. All quotations `[OCR]`.

| # | Item | Verbatim designation | Locator |
|---|---|---|---|
| 1 | sequent $\vdash\Gamma$ (one-sided, multiset context) | displayed in the calculus; the rule group is introduced as "**Multiplicative rules**" with $\dfrac{\vdash F_1,\Gamma_1\quad\vdash F_2,\Gamma_2}{\vdash F_1\otimes F_2,\Gamma_1,\Gamma_2}$ | Appendix A, p. 12 |
| 2 | inference rule (identity/structural, multiplicative, additive, exponential/quantifier groups) | "1) Identity and structural rules … 3) Logical rules — Multiplicative rules … Additive rules … Exponential and quantifier rules" | Appendix A, p. 12 |
| 3 | proof tree | "a bottom-up proof strategy consists in starting from the final conclusion $\vdash\Delta$ and applying step by step inference rules to construct a **proof tree**, the nodes of which constitute subgoals to prove at each step and that is closed by axioms." | §5, p. 6 |
| 4 | subgoal | same passage as #3 ("the nodes of which constitute **subgoals** to prove at each step") | §5, p. 6 |
| 5 | partition $\{\Delta_1,\Delta_2\}$ of the context | "The goal to prove has the form $\vdash F_1\otimes F_2,\Delta'$ and can be replaced by $2^n$ possibilities ($n$ being the number of formulas in $\Delta'$) of the subgoals $\vdash F_1,\Delta_1$ and $\vdash F_2,\Delta_2$ where $\{\Delta_1,\Delta_2\}$ is a **partition** of $\Delta'$." | §5.1(c)(ii), p. 6 |
| 6 | partial proof tree | "At this step, we have the following **partial proof tree** with $\Delta=\ldots$" | §5.3, p. 7 |
| 7 | partial proof | "A top-down strategy will consist in building a set of **partial proofs**, the conclusions of which being multi-sets of subformulas of the final conclusion." | §6, p. 8 |
| 8 | permutation position | "we say that $I_1$ and $I_2$ two inferences of $\Pi$ are in **permutation position** iff they verify the conditions: (i) $I_1$ follows directly $I_2$ in $\Pi$, (ii) the principal part in $I_1$ is disjoint of the active part of $I_2$'s $j$-th premise" | Definition B.1, Appendix B, p. 12 |

$m=8$, the U-b bound, reached. `Permutability` (Definition B.2) falls outside the bound.

### $\mathrm{Ax}(u)$ packages carried

- $\mathrm{Ax}(\text{5})$ — that $\{\Delta_1,\Delta_2\}$ is a **partition** of $\Delta'$, and
  that the admissible replacements are exactly the $2^n$ such partitions (§5.1(c)(ii), p. 6).
  This is the constitutive resource-accounting law and is the load-bearing $\mathrm{Ax}$ item
  for MFDI2/MFDI3.
- $\mathrm{Ax}(\text{3,4})$ — that the tree "is closed by axioms", which is what makes the
  open/closed distinction on nodes source-defined (§5, p. 6) and hence MFDI1/MFDI2 satisfiable.
- $\mathrm{Ax}(\text{1,2})$ — the displayed rule schemata, Appendix A, p. 12.

**Contrast preserved as source-made:** §5.1(c)(i), p. 6 `[OCR]` gives the disjunctive case —
the goal "can be replaced **either** by $\vdash F_1,\Delta'$ **or** $\vdash F_2,\Delta'$" —
against #5's conjunctive "**and**". The AND/OR distinction that MFDI4 requires is stated by the
source in its own words, not imposed by the analyst.

---

## K4 / S2 — Schulte–Stuckey

*Efficient Constraint Propagation Engines*, PDF pp. 3–4; SHA-256
`1e46a8c47750c1783b11d9915dc36eadd4ae312687b3d32cd6d669cf1d2d920e`.

| local # | Item | Short verbatim designation | Locator | Constitutive package |
|---:|---|---|---|---|
| 1 | domain store | “Domains” | §2, p. 3 | $D:V\to\mathcal P_{fin}(\mathbb Z)$ |
| 2 | strength order | “stronger” | §2, p. 3 | $D_1\sqsubseteq D_2\iff\forall x\ D_1(x)\subseteq D_2(x)$ |
| 3 | valuation | “valuation” | §2, pp. 3–4 | integer assignment and membership in a domain |
| 4 | constraint | “constraint” | §2, p. 4 | set of valuations over its variables |
| 5 | propagator | “Propagators” | §2, p. 4 | monotone contracting map on domains |
| 6 | correctness | “correct” | §2, p. 4 | $D\cap c=f(D)\cap c$ at valuation level |
| 7 | checking family | “checking” | §2, p. 4 | valuation is a solution iff all propagators fix its singleton domain |
| 8 | output variables | “output variables” | §2, p. 4 | variables changed by some application |

The same section supplies every frozen S2 component, including propagator-to-constraint
association as data. Certificate: **DIRECT**, E1.

## K4 / S3 — Kolmogorov

*Foundations of the Theory of Probability*, English translation, Chapter I §§1–4, printed
pp. 1–7 (PDF pp. 13–18); SHA-256
`427e0fd315c5bec6c123838ed9510acb7ac354755dd7ac5ddc34b236d9891674`.

| local # | Item | Short verbatim designation | Locator | Constitutive package |
|---:|---|---|---|---|
| 1 | elementary event | “elementary events” | Ch. I §1, p. 2 | elements of $E$ |
| 2 | random event | “random events” | Ch. I §1, p. 2 | members of a field of subsets of $E$ |
| 3 | field of sets | “field of sets” | Ch. I §1, pp. 2–3 | closure under finite set operations |
| 4 | probability | “probability” | Ch. I §1, p. 3 | set function satisfying axioms III–V |
| 5 | probability field | “field of probability” | Ch. I §2, p. 3 | $(E,\mathcal F,P)$ package |
| 6 | incompatibility | “incompatible” | Ch. I §3, p. 5 | empty intersection |
| 7 | complement | “opposite event” | Ch. I §3, p. 5 | $\bar A=E-A$ |
| 8 | conditional probability | “conditional probability” | Ch. I §4, pp. 6–7 | $P_A(B)=P(AB)/P(A)$ and fixed-$A$ probability field |

Restriction to finite $E$ and $P(A)>0$ is DI1. Certificate: **DIRECT**, E1.

## K4 / S4 — Jeffrey successor evidence

Richard C. Jeffrey, *After Logical Empiricism / Radical Probabilism*, §2.3, printed pp. 18–19
(PDF pp. 19–20); SHA-256
`21c778ee0d64f2e97531c0f878c80a4063ce873ddc3e8788ea22d8a3da52cbc6`.

| local # | Item | Short verbatim designation | Locator | Constitutive package |
|---:|---|---|---|---|
| 1 | old credence | “old” | §2.3, p. 18 | prior probability function |
| 2 | new credence | “new” | §2.3, p. 18 | posterior probability function |
| 3 | evidence cells | “partition” | §2.3, p. 18 | disjoint exhaustive $D_1,\ldots,D_n$ under old and new |
| 4 | new marginals | “new($D_i$)” | §2.3, pp. 18–19 | admissible cell weights |
| 5 | old conditionals | “old($H\mid D_i$)” | §2.3, p. 19 | conditional terms held fixed |
| 6 | Jeffrey update | “probability kinematics” | §2.3, p. 19, eq. (1) | $new(H)=\sum_i new(D_i)old(H\mid D_i)$ |
| 7 | rigidity | “rigidity” | §2.3, p. 19, eq. (2) | $new(H\mid D_i)=old(H\mid D_i)$ |
| 8 | odds multiplier | “bayes factor” | §2.3, p. 19, eq. (3) | posterior-odds/prior-odds ratio |

This is **not** the frozen 1965 edition. The located 1965 scan is access-restricted and was
not inspected. Certificate: **DIRECT in E1 only; E0 remains INSPECTION-OPEN**.

## K4 / S5 — Beckers–Halpern

*Abstracting Causal Models*, §2, PDF pp. 2–3; SHA-256
`49ebd3238aaf589071eaafe95164cea08d6f7b4d38febe7d168f4dbfe53a87c3`.

| local # | Item | Short verbatim designation | Locator | Constitutive package |
|---:|---|---|---|---|
| 1 | signature | “signature” | Def. 2.1, p. 2 | $\mathcal S=(U,V,R)$ |
| 2 | exogenous variables | “exogenous variables” | Def. 2.1, p. 2 | $U$ |
| 3 | endogenous variables | “endogenous variables” | Def. 2.1, p. 2 | $V$ |
| 4 | ranges | “possible values” | Def. 2.1, p. 2 | nonempty $R(Y)$ |
| 5 | deterministic model | “basic causal model” | Def. 2.2, p. 2 | $(\mathcal S,F)$ |
| 6 | mechanism | “structural equation” | Def. 2.2, p. 2 | one $F_X$ per endogenous variable |
| 7 | intervention set | “allowed interventions” | Def. 2.2, p. 2 | $I$ in $(\mathcal S,F,I)$ |
| 8 | intervention semantics | “replaced” | §2, p. 2 | intervened equations are replaced by constants |

The same source restricts to recursive/acyclic models, proves context-wise determination, and
defines $Pr$ on contexts for probabilistic causal models. Certificate: **DIRECT**, E1; no DI4
assembly.

## K4 / S8 — Plotkin

*A Structural Approach to Operational Semantics*, §§1.2–1.4, printed pp. 4–10 (PDF pp. 5–11);
SHA-256 `7479be4ee1786caec996796e5fcaff7c972d8290e5c553944f34d7899ce7288e`.

| local # | Item | Short verbatim designation | Locator | Constitutive package |
|---:|---|---|---|---|
| 1 | transition system | “Transition System” | Def. 1.2.1, p. 4 | configuration set plus binary relation |
| 2 | configuration | “configurations” | Def. 1.2.1, p. 4 | elements of the state carrier |
| 3 | step | “transition relation” | Def. 1.2.1, p. 4 | binary relation on configurations |
| 4 | terminality | “terminal” | §1.2, p. 5 | absence of an outgoing transition |
| 5 | terminal set | “terminal configurations” | §1.2, p. 5 | distinguished subset $T$ |
| 6 | labelled system | “Labeled Transition System” | Def. 1.4, p. 9 | configurations, labels, labelled relation |
| 7 | labels | “labels” | Def. 1.4, p. 9 | members of $A$ |
| 8 | labelled step | “transition relation” | Def. 1.4, p. 9 | subset of $\Gamma\times A\times\Gamma$ |

Finite alphabet and finite branching are uniform DI1 restrictions. Certificate: **DIRECT**,
E1.

## K4 / S9 — Suda

*Duality in STRIPS Planning*, §2, PDF p. 2; SHA-256
`75e320d8c52f8c58df913c63a060da890d8b057a0fd5c5c73a6679bbbbef5c07`.

| local # | Item | Short verbatim designation | Locator | Constitutive package |
|---:|---|---|---|---|
| 1 | planning task | “planning task” | §2, p. 2 | $P=(X,I,G,A)$ |
| 2 | atoms | “atoms” | §2, p. 2 | finite $X$ |
| 3 | initial state | “initial condition” | §2, p. 2 | $I\subseteq X$ |
| 4 | goal | “goal condition” | §2, p. 2 | $G\subseteq X$ |
| 5 | action family | “actions” | §2, p. 2 | finite $A$ |
| 6 | action | “triple” | §2, p. 2 | $(pre_a,add_a,del_a)$, with no disjointness axiom |
| 7 | state carrier | “world states” | §2, p. 2 | $S=2^X$ |
| 8 | action step | “transition relation” | §2, p. 2 | applicability and $s'=(s\cup add_a)\setminus del_a$ |

Certificate: **EXACT**, E1. The paper later discusses overlapping action lists, confirming that
the frozen unconstrained-triple class was not silently narrowed.

## K4 / S10 — Dung

*On the Acceptability of Arguments …*, §2.1, printed pp. 326–327 (PDF pp. 6–7); SHA-256
`8a3139ba974401551f5f762910da8f933e7e23d3efc24a710c9028b198ec327d`.

| local # | Item | Short verbatim designation | Locator | Constitutive package |
|---:|---|---|---|---|
| 1 | AF | “argumentation framework” | Def. 2, p. 326 | $AF=(AR,attacks)$ |
| 2 | argument carrier | “set of arguments” | Def. 2, p. 326 | $AR$ |
| 3 | attack | “attacks” | Def. 2, p. 326 | binary relation on $AR$ |
| 4 | set attack | “attacks B” | Remark 4, p. 326 | existential attack by a member of a set |
| 5 | conflict-free set | “conflict-free” | Def. 5, p. 326 | no internal attack |
| 6 | acceptability | “acceptable” | Def. 6(1), p. 326 | every attacker counterattacked by $S$ |
| 7 | admissibility | “admissible” | Def. 6(2), p. 326 | conflict-free and self-defending |
| 8 | preferred extension | “preferred extension” | Def. 7, p. 327 | inclusion-maximal admissible set |

Stable, grounded, and complete semantics were also inspected later in §2, but fall beyond U-b.
The source makes extensions sets in the metatheory and assigns no native state transformation;
S10 is READY for state/evaluation semantics while its frozen transformation remains unassigned.

## K4 / S11 — Mielke

*An Introduction to the Analysis of Gradient Systems*, §§1.1–1.2, printed pp. 4–5; SHA-256
`f5d39f2977eca3a7cfb764197650fea5147ec41dfa4ca63ba55173af757832b2`.

| local # | Item | Short verbatim designation | Locator | Constitutive package |
|---:|---|---|---|---|
| 1 | metric tensor | “Riemannian structure” | §1.1, p. 4 | symmetric positive $G(u)$ |
| 2 | inverse metric | “Onsager operator” | Def. 1.1, p. 4 | $K(u)=G(u)^{-1}$ |
| 3 | gradient | “gradient” | Def. 1.1, p. 4 | $grad_G F=KDF$ |
| 4 | gradient system | “gradient system” | Def. 1.2, p. 4 | $(M,F,G)$ |
| 5 | evolution equation | “gradient-flow equation” | Def. 1.2, p. 4 | $\dot u=-grad_G F(u)$ |
| 6 | solution | “solution” | Def. 1.2, p. 4 | equation plus initial condition |
| 7 | flow | “gradient flow” | §1.2, p. 5 | $u(t)=S_t(u_0)$ |
| 8 | composition law | “semigroup property” | §1.2, p. 5 | $S_0=id$ and $S_t\circ S_r=S_{t+r}$ |

For $M=\mathbb R^n$, $G=I$, and globally Lipschitz $\nabla f$, the source's globally
Lipschitz ODE statement on arbitrary $[0,T]$ supplies unique global solutions; autonomy gives
the displayed semigroup. Certificate: **DIRECT**, E1, within one source.

## Sealing status

$$\boxed{U0\text{-}E1\ \textbf{SEALED} — 88\ \text{items};\quad U0\text{-}E0\ \textbf{NOT CERTIFIED}}$$

All eleven targets now have eight K4 records. `U0.json` is the immutable successor registry;
`SEALS.json` records its SHA-256 before `W-STAR.json` was generated. Frozen E0 is not
retroactively repaired: S4's exact source is uninspected and U-c cognitive blindness cannot be
re-created after exposure.
