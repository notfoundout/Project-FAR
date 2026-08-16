# K4 records — per-target primitive extraction from supplied primary sources

K4 requires, for every extracted item, a **verbatim quotation** of the passage in which the
source designates it primitive, plus an exact locator (`TR-11:2076`). U-a restricts extraction
to items the source itself formally designates as basic in its definitional apparatus —
signature entries, primitive relations/operations, defined-as-basic notions; theorems, lemmas
and named results are excluded. U-b bounds each source at $m\le 8$ items, taken in the source's
own order of first definition. U-e retains duplicates with distinct identifiers.

**These are per-target K4 records, not $U_0$.** $U_0$ cannot be constituted, sealed or hashed
until all eleven targets have such records; nine do not. See `MISSING-SOURCE-MANIFEST.md`.
Registry IDs are therefore **withheld**: assigning $u_1,u_2,\ldots$ now would fix an extraction
order that the missing nine must share, and U-c requires the extraction to be blind and the
order to be the global extraction order. These records are held as
`K4/<target>/<n>` and will be numbered only at sealing.

**Blindness declaration (U-c).** The two extractions below were performed per-target against
the source's own definitional sections. They were not conditioned on the other target's
extraction, on the RCCD vocabulary list, or on any downstream use. Provenance metadata is
quarantined until Q4 (`TR-11:4128`).

**Transcription note.** In `SS-CC92` the flat/sharp superscripts distinguishing concrete
$P^\flat$ from abstract $P^\sharp$ are typographic and are lost by text extraction; they are
restored below in square brackets and marked. In `SS-GP94` all quotations are OCR
transcriptions of a bitmap-font body and are marked `[OCR]`.

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

## Sealing status

$$\boxed{U_0\ \textbf{NOT SEALED, NOT HASHED} — 2\ \text{of}\ 11\ \text{targets have K4 records}}$$

Per the frozen staging (`TR-11:4956`), $W^\ast$ begins only after $\mathcal{K}_0$, $U_0$ and
$\Pi_0$ are hashed. It has not begun and, on the evidence available in this session, cannot.

**No Codex-generated $U_0$, witness matrix, rank, or minimality claim has been consulted,
imported, or used anywhere in this run.** Such material lacks the K4 source record these
records exist to supply, and the frozen rule is that it may be revealed only after
independently extracted objects are sealed — which has not occurred. It is therefore not
available even as adversarial comparison material at this stage.
