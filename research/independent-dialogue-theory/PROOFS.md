# PROOFS — theorems, objections, countermodels, dispositions

**Revision 2.** Revision 1's T1–T3 are reopened and corrected below under the audit points
raised against them. Every superseded claim is stated as superseded rather than deleted.

Notation and rule statuses are as in `PROTOCOL.md`. Source locators are exact.

---

## 0. Supplied primary sources

Both were supplied as local files, hashed, bibliographically verified from their own front
matter, and cached. They are **SOURCE-SUPPLIED** evidence. Evidence cutoff **2026-08-15** is
preserved: both are 1992/1994 publications, already eligible at that cutoff; later delivery of
an already-eligible publication does not move the cutoff.

| ID | Document | SHA-256 | Identity verified from |
|---|---|---|---|
| `SS-CC92` | P. Cousot & R. Cousot, *Abstract Interpretation Frameworks*, **J. Logic and Computation 2(4):511–547, 1992** | `19591e44a5584e27547538d3ed553a7b26b78d9fe234f129fbba3c2a735f89bb` | title block p. 511; running heads and page numbers 511–547 present in the document |
| `SS-GP94` | D. Galmiche & G. Perrier, *Foundations of Proof Search Strategies Design in Linear Logic*, **LFCS, St-Petersburg, 1994, pp. 101–113**; HAL `hal-01297758` | `622f2f9ee49f8c8b7201b2937ea88509f4ecac345739fd84c357bbf2193132ee` | HAL cover page; PDF metadata (Title, Author); §1 title block |
| `SS-LM24` | C. Liang & D. Miller, *Focusing Gentzen's LK Proof System*, in Piecha & Wehmeier (eds.), **Peter Schroeder-Heister on Proof-Theoretic Semantics**, Springer 2024, ch. 9, pp. 275ff.; DOI `10.1007/978-3-031-50981-0_9` | `044ac192a6fcdea5425a068a254dea99ca32c3a60f3441bbf1bf4b2bfca465ef` | chapter title and author block p. 275; volume/editor statement p. 275; running heads pp. 276–285 |
| `SS-P19` | J. Pearl, *The Seven Tools of Causal Inference, with Reflections on Machine Learning*, **UCLA Technical Report R-481, February 2019**; DOI `10.1145/3241036` | `6adca12cb7817602ed4557ff67893287ef429bdd30586ddeb23ac4fc7dd3c914` | report banner "TECHNICAL REPORT R-481 / February 2019"; DOI line; byline "BY JUDEA PEARL" |

`SS-CC92` has a text layer. `SS-GP94` is a bitmap-font/scanned body; its body was rendered at
200 dpi and OCR'd. **All `SS-GP94` quotations below are OCR transcriptions** and are marked
`[OCR]`; obvious OCR corruption of symbols is marked `[sic]`. Page references for `SS-GP94`
are to the preprint's own printed page numbers.

**Status of `SS-CC92` within the frozen experiment.** It is **$N_7$ member 5**, frozen into the
candidate set by the original SR-B2 v2 Channel-A ordering *before* it was supplied. Its
inspection is therefore ordinary execution of the original frozen procedure, not a successor.

**Status of `SS-GP94`.** It was **never returned** by any of the 16 prescribed S6 SR-B2 v2
invocations and is **not** in frozen $N_6$. It is **not retrofitted**. It is inspected only
under the separately versioned `E0-supplied-v1` (see `PROTOCOL-SUCCESSOR.md`), and the
difference between the two verdicts is reported as source-supply sensitivity (§5.3).

**Status of `SS-LM24`.** It is frozen **$N_1$ member 2** (`TR-11:10689`), placed in the
near-match set by the original Channel-A ordering long before supply, and it is the source
already carrying S1's DIRECT certificate. Its inspection is therefore **ordinary execution of
the original frozen procedure**. See §4bis.

**Status of `SS-P19`.** Not a target source. It is the assigned document for one label of the
prior-art baseline under the sealed `PI0-BIB-v1`. It grounds **no** target verdict and **no**
novelty verdict; see `PI0-BIB-v1.md` §5.

---

## 1. T1 superseded by T1′ — bounded impossibility over explicit classes

### 1.0 What was wrong with T1

Revision 1's T1 asserted that *no* single-sequent binary transition structure represents MLL
backward search, having tested exactly two decoders (OR and AND) against exactly one relation
($\to_\pi$). That is not an impossibility theorem. Two specific defects:

- **Unrestricted representation class is fatal.** If $\to$ may be *any* binary relation on
  $\mathsf{Seq}$, the claim is **false**: put $S\to S'$ iff $S$ is MLL-provable and $S'$ is a
  fixed axiom. Then "some successor is provable" decides provability exactly. The answer has
  simply been encoded into the relation.
- **Unrestricted decoder class is fatal.** MLL provability is a function of $S$ alone, since
  $S$ determines all its rule instances. Any decoder permitted to inspect $S$ can recompute
  provability and ignore $\to$ entirely.

So an impossibility result exists only relative to an explicit representation class **and** an
explicit decoder class. T1′ supplies both and is exhaustive over them.

### 1.1 The two classes, fixed explicitly

**Representation class $\mathcal{R}_{\mathrm{bin}}^{\mathsf{Seq}}$.** The state type is
$\mathsf{Seq}$ = individual MLL sequents (frozen S6's stated state type). The transition
structure is the **rule-induced projected relation**
$$S\to_\pi P \iff P \text{ is a premise of some backward MLL rule instance with conclusion } S.$$
This is the *unique* member of the class: any other binary relation on $\mathsf{Seq}$ requires
an analyst-supplied selection, orientation, or encoding, which DI3 forbids.

**Decoder class $\mathcal{D}_{\mathrm{succ}}$ — uniform monotone successor-set decoders.**
$\mathrm{Prov}$ is the least fixpoint of
$$\Phi(X)(S)\ =\ T(S)\ \vee\ g\big(\{X(P) : S\to P\}\big)$$
where $T(S)$ holds iff $S$ is the conclusion of a zero-premise rule instance, and
$g:\wp(\{0,1\})\to\{0,1\}$ is monotone with $g(\varnothing)=0$. **Uniform** means one $g$ for
all $S$: $g$ may not inspect $S$. This is exactly the information a binary relation carries —
a *set* of successors, hence a *set* of successor truth values.

### 1.2 Lemma (four decoders)

$\mathcal{D}_{\mathrm{succ}}$ has exactly four members.

*Proof.* As $X$ increases pointwise, the value set $V(S)=\{X(P):S\to P\}$ moves along
$\{0\}\to\{0,1\}\to\{1\}$. Monotonicity of $\Phi$ therefore requires
$g(\{0\})\le g(\{0,1\})\le g(\{1\})$, and $g(\varnothing)=0$ is fixed. A monotone chain of
three Booleans has exactly four solutions:

| $g(\{0\}),g(\{0,1\}),g(\{1\})$ | decoder | meaning |
|---|---|---|
| $0,0,0$ | $\mathbf{TERM}$ | provable iff terminal |
| $0,0,1$ | $\mathbf{AND}$ | all successors provable |
| $0,1,1$ | $\mathbf{OR}$ | some successor provable |
| $1,1,1$ | $\mathbf{NONEMPTY}$ | some successor exists |
∎

### 1.3 Lemma (atom balance)

If $\vdash\Gamma$ is MLL-provable then every atom $p$ occurs in $\Gamma$ as often as
$p^{\perp}$. *Proof.* Induction: $(\mathrm{ax})$ is balanced; $(⅋)$ preserves the atom
multiset; $(\otimes)$ takes the union of two balanced multisets. ∎

### 1.4 The two witnesses

$$S_\vee := \ \vdash a^{\perp},\,a^{\perp},\,a\otimes b
\qquad\qquad
S_\wedge := \ \vdash a^{\perp},\,b^{\perp},\,a\otimes b$$

- $S_\vee$ is **not** provable ($a$ occurs twice negatively, once positively; $b$ never
  negatively — Lemma 1.3), is **not** terminal, and **has** a provable successor: the
  $(\otimes)$ instance with partition $\Gamma=\{a^{\perp}\},\Delta=\{a^{\perp}\}$ has premises
  $\vdash a^{\perp},a$ (an axiom) and $\vdash a^{\perp},b$.
- $S_\wedge$ **is** provable (partition $\Gamma=\{a^{\perp}\},\Delta=\{b^{\perp}\}$ gives the
  axioms $\vdash a^{\perp},a$ and $\vdash b^{\perp},b$), is **not** terminal, and **has** an
  unprovable successor: the partition $\Gamma=\varnothing,\Delta=\{a^{\perp},b^{\perp}\}$ gives
  the premise $\vdash a$, unprovable by Lemma 1.3.

### 1.5 Theorem T1′

No pair in
$\mathcal{R}_{\mathrm{bin}}^{\mathsf{Seq}}\times\mathcal{D}_{\mathrm{succ}}$ computes MLL
provability.

*Proof.* By Lemma 1.2 there are four decoders. $\mathbf{TERM}$ is refuted by $S_\wedge$
(provable, non-terminal). $\mathbf{NONEMPTY}$ is refuted by $S_\vee$ (unprovable, has
successors). $\mathbf{OR}$ is refuted by $S_\vee$ (unprovable, has a provable successor).
$\mathbf{AND}$ is refuted by $S_\wedge$ (provable, has an unprovable successor). ∎

### 1.6 Exactly what T1′ does and does not establish

**Does:** over the individual-sequent state type, with the rule-induced relation and uniform
successor-set decoding, MLL provability is not computable — and the reason is identifiable:
the projected relation destroys the pairing between premises arising from the *same* resource
partition.

**Does not:** it does not show MLL provability is undefinable (it is definable from $S$ alone);
it does not show that binary relations on *richer* state types fail (§2 proves one succeeds);
it does not show that resource nondeterminism is a defect (GPT Turn 35 §2 stands — retaining
all admissible partitions is ordinary nondeterminism); and it is **not** a characterisation.

---

## 2. State-type taxonomy, replacing the arity framing

Revision 1 phrased the result as being about **arity**. That was imprecise: a binary relation
on a rich enough state encodes conjunction perfectly well. Every claim is now indexed by
**state type**.

| | State type | Transition structure | Adequate for MLL? |
|---|---|---|---|
| $\mathcal{X}_1$ | individual sequent $\mathsf{Seq}$ | rule-induced **binary relation** | **No** — T1′, over $\mathcal{D}_{\mathrm{succ}}$ |
| $\mathcal{X}_2$ | individual sequent $\mathsf{Seq}$ | resource-labelled **hyperedges** $S\to_{\rho,\text{split}}\{P_1,\ldots,P_k\}$ | **Yes** — Prop. 2.2 |
| $\mathcal{X}_3$ | frontier $\mathsf{MSet}(\mathsf{Seq})$ | **binary relation** | **Yes** — Prop. 2.1 |

$\mathcal{X}_3$ is a *binary relation* and is adequate. This is the direct refutation of the
Revision-1 arity framing, and it is retained as the correction.

### Proposition 2.1 (frontier sufficiency — any finitary rule system)

Let $R$ be any rule system with finitary rules $\frac{P_1\cdots P_k}{S}$, $k\ge0$. Define
$M\to M'$ iff $M'=M-[S]+[P_1]+\cdots+[P_k]$ for some $S\in M$ and some instance. Call $M$
*closable* iff every sequent occurring in $M$ is derivable. Then

$$M \text{ closable} \iff M=[\,]\ \text{ or }\ \exists M'.\, M\to M' \wedge M' \text{ closable.}$$

*Proof.* ($\Leftarrow$) All members of $M'$ derivable ⇒ each $P_i$ derivable ⇒ $S$ derivable by
the instance; the other members of $M$ occur in $M'$. ($\Rightarrow$) $M$ closable, $M\neq[\,]$;
pick $S\in M$, take the last rule of a derivation of $S$; its premises are derivable, so the
resulting $M'$ is closable. ∎

**This holds for MLL exactly as for LK.** The conjunction is absorbed into multiset union.

### Proposition 2.2 (hyperedge sufficiency on individual sequents)

Define $S\rightarrowtail\{P_1,\ldots,P_k\}$ iff $\frac{P_1\cdots P_k}{S}$ is a rule instance
(for MLL, the label carries the resource partition). Then
$$S \text{ derivable} \iff \exists\, S\rightarrowtail\{P_1,\ldots,P_k\}\ \text{with every } P_i \text{ derivable.}$$
*Proof.* Immediate from the definition of derivability by rule application. ∎

This is the standard AND/OR characterisation; the hyperedge retains the joint premise family
that $\to_\pi$ discards.

### Proposition 2.3 (individual-sequent insufficiency is not MLL-specific)

Proposition 2.1's proof uses nothing about MLL, and T1′'s proof uses only the two witness
conditions:

- **(W1)** some non-terminal underivable $S$ has an instance with a derivable premise;
- **(W2)** some non-terminal derivable $S$ has an instance with an underivable premise.

MLL satisfies both (§1.4).

**Classical LK satisfies both, verified against `SS-LM24` Figure 1 (p. 277).** Revision 2 left
this "not decided here"; the supplied source decides it for the certified corpus profile
$K_{1,\mathrm{L\&M}}$.

- **(W1).** $S=\ p\vdash q\wedge p$ is not derivable. The $\wedge R$ instance
  $\dfrac{\Gamma\vdash\Delta,B\quad\Gamma\vdash\Delta,C}{\Gamma\vdash\Delta,B\wedge C}$ with
  $\Gamma=\{p\},\Delta=\varnothing,B=q,C=p$ has the premise $p\vdash p$, which is derivable by
  $init$. ✓
- **(W2).** $S=\ p\vdash p\vee q$ is derivable, via $\vee R$ with $i=1$. Figure 1's $\vee R$ is
  $\dfrac{\Gamma\vdash\Delta,B_i}{\Gamma\vdash\Delta,B_1\vee B_2}$ with $i\in\{1,2\}$ (caption,
  p. 277), so the instance with $i=2$ is a legitimate rule instance at the same conclusion and
  has the premise $p\vdash q$, which is not derivable. ✓

Figure 1 also makes $\supset L$ and $cut$ **multiplicative**, with the context split between
premises — "the cut rule and the implication-left rule are multiplicative" (`SS-LM24`, p. 281) —
so the context-splitting phenomenon that drives T1′ for MLL is present in this LK presentation
too.

$$\boxed{\text{SSS-3's hypotheses hold for propositional LK under } K_{1,\mathrm{L\&M}}, \text{ as well as for MLL.}}$$

A purely additive-context presentation with only single-premise left rules and no
single-conjunct $\vee R$ remains undecided, and that residue is a presentation question, not an
open mathematical one.

$$\boxed{\text{The S1/S6 contrast in the frozen shell is a contrast of \emph{state typing}, not of logic.}}$$

Had the shell given S6 a frontier state it would have been adequate; had it given S1 an
individual-sequent state, S1 would have faced T1′'s problem. Revision 1's suggestion that LK
is intrinsically better behaved than MLL here is **withdrawn**.

---

## 3. T3 superseded by T3′ — S6 is **not** UNDERDETERMINED

### 3.0 What was wrong with T3

Revision 1 classified S6 UNDERDETERMINED because $\mathcal{X}_1$ and $\mathcal{X}_2$ are both
compatible with the frozen text and are inequivalent. That misapplies DI3. **DI3's test ranges
over *admissible* additions.** A structure that fails a frozen obligation is not a competing
witness merely because it is mathematically definable.

### 3.1 Correct application

Frozen S6's state type is fixed by the shell: *sequent with resource context* — an individual
sequent (`TR-11:2145`). Candidate structures over that state type:

- $\mathcal{X}_1$ **fails MFDI4**: by T1′ the projected relation does not preserve the jointly
  generated premise family, and the AND/OR distinction is lost. **Inadmissible.**
- $\mathcal{X}_2$ satisfies MFDI3 (each premise $\vdash\Gamma,A$, $\vdash\Delta,B$ carries its
  own allocated linear context), MFDI4 (Prop. 2.2 — one hyperedge per rule instance, grouping
  preserved), MFDI5 (the hyperedges out of $S$ are a function of $S$ alone, so the root-sequent
  quotient is well defined on successors), and MFDI6 (in exponential-free, quantifier-free MLL,
  applicability at $S$ depends only on $S$; no branch history, proof-net linkage, focusing
  phase, or unrepresented allocation can affect it). **Admissible.**

$\mathcal{X}_3$ is not a candidate: it has a *different state type* and so is not a reading of
frozen S6 at all.

Exactly **one** admissible structure survives. The determination invariant therefore **holds**:

$$\boxed{\text{S6 is NOT UNDERDETERMINED. Its native structure is } \mathcal{X}_2.}$$

### 3.2 Consequences

- Revision 1's claim that **Turn 17's determination check for S6 was incorrect** is
  **withdrawn**. Turn 17's ✓ is correct once inadmissible readings are excluded.
- Revision 1's two-branch disjunction for S6 is **withdrawn**.
- S6 reverts to the ordinary source question: does an eligible source supply MFDI1–MFDI2 for
  $\mathcal{X}_2$ restricted to MLL? Answered in §5.

---

## 4. S7 = **READY** — original procedure, frozen candidate `SS-CC92`

TSI-v1 executed on $N_7$ member 5. Sections inspected: abstract; §1; §3; §4 (extrapolation
operators); Example 4.6; §6 (approximation, Prop. 6.14, Prop. 6.17, Prop. 6.20); §9. Fixed
terms searched: *Galois connection, widening, narrowing, transfer, soundness, complete lattice,
abstraction, concretization, framework*.

### 4.1 The frozen target

$\mathsf{Inst}_7=\{(C,A,\alpha,\gamma,\mathcal{F},\nabla)\}$ with $C,A$ complete lattices,
$(\alpha,\gamma)$ a Galois connection, $\mathcal{F}=\{(f_C,f_A)\}$ finite with
$\alpha\circ f_C\sqsubseteq_A f_A\circ\alpha$, and $\nabla:A\times A\to A$ satisfying
$x\sqsubseteq x\nabla y$, $y\sqsubseteq x\nabla y$, and stabilisation of $\nabla$-iterated
chains (`TR-11:5382`).

### 4.2 Component-by-component certificate

**(a) The bundle is ONE source-defined framework.** This is the DI4 question, and the source
settles it in its own abstract, p. 511:

> "We introduce abstract interpretation frameworks which are variations on the archetypal
> framework using Galois connections between concrete and abstract semantics, widenings and
> narrowings and are obtained by relaxation of the original hypotheses."

and §1, p. 512:

> "The abstract interpretation framework that we introduced in [6, 8, 7, 9, 10, 12, 18, 19] is
> based on the use of Galois connections … However, in some practical cases, this might lead to
> a combinatorial explosion … In this case and more generally, when the abstract domain is
> large or infinite, widening and narrowing operators [6, 7] should be used to tune the
> cost/precision compromise."

The archetypal framework **is** the Galois-connection framework **with** widening and
narrowing. **DI4 is satisfied**, and the Turn-21 worry (`TR-11:6890`) that a Galois connection
and a widening are "distinct approaches" that no primary source presents as a unit is
**refuted by the primary source**.

**(b) Complete lattices and the Galois connection.** Example 4.6, p. 518:

> "In the classical framework of [7, 10, 12], the concrete properties $P^\flat;\sqsubseteq^\flat,
> \sqcup^\flat,\bot^\flat,\top^\flat$ and abstract properties $P^\sharp;\sqsubseteq^\sharp,
> \sqcup^\sharp,\bot^\sharp,\top^\sharp$ are complete lattices. The correspondence between
> concrete and abstract properties is given by a Galois connection … that is an abstraction map
> $\alpha\in P^\flat\to P^\sharp$ and a concretization map $\gamma\in P^\sharp\to P^\flat$ such
> that, by definition: $\forall c\in P^\flat:\forall a\in P^\sharp:\alpha(c)\sqsubseteq^\sharp a
> \Leftrightarrow c\sqsubseteq^\flat\gamma(a)$." — eq. (4.12), p. 518

Gives $C,A$ complete lattices and $(\alpha,\gamma)$ exactly. **DI1**, verbatim.

**(c) The soundness condition, verbatim.** Proposition 6.14, p. 531:

> "the concrete $F^\flat\in P^\flat\to P^\flat$ and abstract $F^\sharp\in P^\sharp\to P^\sharp$
> semantic functions such that $\forall c\in P^\flat:\forall a\in P^\sharp:\alpha(c)\sqsubseteq a
> \Rightarrow\alpha(F^\flat(c))\sqsubseteq F^\sharp(a)$ (… holds in particular when $F^\sharp$ is
> monotonic for $\sqsubseteq$ and $\alpha\circ F^\flat\sqsubseteq F^\sharp\circ\alpha$)"

The frozen soundness condition $\alpha\circ f_C\sqsubseteq f_A\circ\alpha$ appears **verbatim**
in the source. **DI1**.

**(d) The widening's upper-bound conditions.** Eq. (4.39), p. 531:

> "$\nabla A$ exists $\wedge\ a\in A\ \Rightarrow\ a\sqsubseteq\nabla A$"
>
> "which holds when the widening is a partially defined upper bound in $P^\sharp$ (but not
> necessarily the least one)."

For $A=\{x,y\}$ this yields **both** $x\sqsubseteq x\nabla y$ and $y\sqsubseteq x\nabla y$ — the
frozen conditions. The source's $\nabla\in\wp(P^\sharp)\to P^\sharp$ is set-indexed; the frozen
binary $\nabla:A\times A\to A$ is its **restriction to two-element argument sets**, which is the
form the source itself iterates (Prop. 6.20's chain $y_{i+1}=y_i\nabla x_i$). **DI1**, correct
direction: frozen is narrower.

**(e) The chain-stabilisation condition.** Proposition 6.20, condition list (4.46), p. 537:

> "For every $\mathbb{N}$-termed sequence $x_0,\ldots,x_i,\ldots$ in $P^\sharp$, the chain
> $y_0=x_0\ \ldots\ y_{i+1}=y_i\nabla x_i\ \ldots$ is not strictly increasing"

Together with (4.39) — which makes the chain increasing — "not strictly increasing" is exactly
"stabilises". Frozen condition matched. **DI1**.

**(f) The finite family $\mathcal{F}$.** The source's framework carries one pair
$(F^\flat,F^\sharp)$. A finite indexed family of sound pairs over a shared
$(C,A,\alpha,\gamma,\nabla)$ is admitted under **DI2/CDE-v1**: it is definable solely from the
source's own primitive "sound concrete/abstract semantic function pair" (Prop. 6.14); it has no
free methodological parameter, since $\mathcal{F}$ is supplied as *instance data*, not
constructed by the analyst after the instance is given; no scheduler, ordering, strategy or
granularity is chosen; and its granularity is anchored by that source primitive. It is part of
the source's formal apparatus rather than an arbitrary derived object — the source lifts Galois
connections to monotonic function spaces precisely to support families, eq. (4.17), p. 519, and
works with systems of abstract equations over vectors of abstract functions in Example 6.15,
p. 532.

**(g) DI3.** Frozen S7 imposes **no transition graph** (`TR-11:5394`); $\mathcal{S}_{7,a}$ is a
static algebraic structure. No scheduler, search discipline, orientation, update rule,
aggregation, quotient, completion, resource policy, equivalence, intervention or control
strategy is supplied by the analyst. **DI3 satisfied vacuously on the dynamics**, which is
exactly the component that made S1 and S6 hard.

**(h) DI5, DI6.** Forgetting $\gamma$, the family structure, and the completeness of the
lattices recovers the source's framework (**DI5**). The instance tuple determines
$\mathcal{S}_{7,a}=(C,A,\alpha,\gamma,\{f_C\},\{f_A\},\nabla,\sqsubseteq_C,\sqsubseteq_A)$
componentwise (**DI6**, and the determination invariant).

**(i) K-P2.** Cousot & Cousot originated abstract interpretation; this is an authoritative
formalization by the framework's originators. **Primary-source priority satisfied.**

### 4.3 Verdict

$$\boxed{\mathrm{Status}(S7)=\mathbf{READY}\quad\text{(DIRECT: DI1 + DI2/CDE-v1, source }
\texttt{SS-CC92}\text{)}}$$

Established by the **original** frozen procedure on the **original** frozen candidate set. The
existential early-stop fires; the remaining $N_7$ inspections are not required for
instantiation status.

**Recorded against interest:** this outcome is the opposite of the direction S7 had been
trending since Turn 21, and it refutes a conjecture the dialogue had held for fourteen turns.

---

## 4bis. S1 — certificate and A2 witness **independently verified** from `SS-LM24`

TSI-v1 executed on frozen $N_1$ member 2, original procedure. Sections inspected: abstract
p. 275; §1 pp. 276–277; **Figure 1 p. 277**; §2 pp. 277–278; §2.1 p. 278; §3 p. 281. Fixed terms
searched: *proof search, search state, open sequent(s), goal(s), multiset, frontier, backward,
transition, unproved, exchange, derivation*.

Revision 2 recorded S1's certificate and the whole A2 result as **transcript-attested, not
independently verified**. That caveat is now **discharged**.

### 4bis.1 FDI1–FDI2 confirmed verbatim

The Turn-34 quotation is exact. `SS-LM24` §2, p. 278:

> "For this paper, we shall make the following distinction between proof and derivation. By
> proof, we mean a tree structure of inference rules and sequents such that all premises are
> closed, in the sense that the inference rules at the leaves have zero premises (such as the
> initial rule). By derivation, we mean a similar tree structure of inference rules and
> sequents, but we do not assume that all leaves are closed: derivations can have unproved
> premises."

**FDI1** (partial derivations source-defined) and **FDI2** (the open/closed leaf distinction
source-made and load-bearing) are satisfied by the source's own words. FDI3–FDI5 follow from
this plus the rule set, as certified at GPT Turn 34; the propositional restriction that FDI5
needs is examined in §4bis.3.

### 4bis.2 The A2 witness, now verified against the actual rule set

T4's S1 half requires: *no LK rule instance has a single premise identical to its conclusion.*
Figure 1's complete rule set is now visible and can be checked exhaustively.

| Group | Rules | Single-premise instance with premise $=$ conclusion? |
|---|---|---|
| Structural | $cL\ \frac{\Gamma,B,B\vdash\Delta}{\Gamma,B\vdash\Delta}$, $cR\ \frac{\Gamma\vdash\Delta,B,B}{\Gamma\vdash\Delta,B}$ | no — premise multiset strictly larger |
| Structural | $wL\ \frac{\Gamma\vdash\Delta}{\Gamma,B\vdash\Delta}$, $wR\ \frac{\Gamma\vdash\Delta}{\Gamma\vdash\Delta,B}$ | no — premise strictly smaller |
| Identity | $init$ | $k=0$ |
| Identity | $cut$ | $k=2$ |
| Introduction, 1 premise | $\wedge L$, $\vee R$, $\supset R$ | no — conclusion carries one more connective occurrence |
| Introduction, 0 premises | $tR$, $fL$ | $k=0$ |
| Introduction, 2 premises | $\wedge R$, $\vee L$, $\supset L$ | $k=2$ |
| Quantifier | $\forall L,\forall R,\exists L,\exists R$ | outside the frozen propositional fragment |
| **Exchange** | **absent** | — |

The decisive fact is stated by the source itself, §2, p. 277, difference 1:

> "In Gentzen's system, contexts are lists of formulas, and the exchange rule, which allowed two
> adjacent formulas to be swapped, was used. In Figure 1, contexts ($\Gamma$ and $\Delta$) are
> multisets of formulas, and the exchange rule is not used."

and §2, p. 277: "Inference rules are between sequents which are pairs of multisets of formula".

For $M\to M$ we need $k=1$ and $P_1=S$; the table shows no such instance exists. Hence every
$\mathcal{S}_{1,a}$ is irreflexive.

$$\boxed{\varphi_{\mathrm{irr}}\text{ holds in every admissible LK proof-search graph — verified from the primary source.}}$$

The exchange-rule escape route that made T4 profile-relative is confirmed to be **exactly** the
route the source describes as *Gentzen's* presentation and *not* its own. T4's profile
sensitivity is therefore real and correctly stated, and the certified profile
$K_{1,\mathrm{L\&M}}$ is confirmed to be the multiset/no-exchange one.

### 4bis.3 The residual restriction, re-examined and unchanged

Figure 1 is **first-order**: formulas are built "using both the logical connectives $\wedge$, t,
$\vee$, f, $\supset$ as well as the two first-order quantifiers $\forall$ and $\exists$" (§2,
p. 277), and the caption carries the eigenvariable condition "In the $\forall R$ and $\exists L$
rules, the variable $y$ is not free in the conclusion."

Frozen S1 is propositional. The source does **not** formally carve out the quantifier-free
fragment. The restriction remains **analyst-performed under DI1**, exactly as Claude flagged at
Turn 35 (`TR-31:1193`) — and inspection confirms the flag was accurate rather than
over-cautious. It is licensed by DI1 (restriction to a formally specified subclass, stated
independently of any result) and it is what makes FDI5 hold, since the eigenvariable side
condition — the only source-stated constraint that could couple a leaf's expansion to material
outside it — lives exactly on the four rules the restriction removes.

$$\boxed{\mathrm{Status}(S1)=\mathbf{READY}\ \text{— certificate independently verified; the DI1 propositional restriction remains the thinnest point, and is now confirmed as such rather than inferred.}}$$

---

## 5. S6 = **READY** under `E0-supplied-v1`; **OPEN** under original $\mathfrak{E}_0$

### 5.1 Procedure separation, stated first

`SS-GP94` is **not** in frozen $N_6$ and is **not** retrofitted. Under the original frozen
$\mathfrak{E}_0$, S6's status is unchanged: **OPEN**, because all sixteen prescribed SR-B2 v2
invocations were executed and none returned an inspectable eligible source. The verdict below
belongs to `E0-supplied-v1` only.

### 5.2 MFDI1–MFDI6 against `SS-GP94`

The source treats **CLL**; frozen S6 is **MLL without exponentials**. The restriction is
**source-recognised** (SRF-v1): §4.3, p. 5 names the fragment —

> "In the multiplicative fragment MLL (extended with $\otimes$ [sic, OCR]) we have only
> non-determinism in the way to associate literals in the axioms." `[OCR]`

— and Appendix A, p. 12 sets out the calculus with **"Multiplicative rules"** as a separately
displayed group, including the $\otimes$ rule with split contexts
$\dfrac{\vdash F_1,\Gamma_1\quad \vdash F_2,\Gamma_2}{\vdash F_1\otimes F_2,\Gamma_1,\Gamma_2}$.
Direction is correct: MLL is **narrower** than CLL, so frozen S6 is a restriction of the
source's formalism, not a generalisation of it.

**MFDI1 — source-defined incomplete derivations. SATISFIED.** §5, p. 6 `[OCR]`:

> "a bottom-up proof strategy consists in starting from the final conclusion $\vdash\Delta$ and
> applying step by step inference rules to construct a proof tree, the nodes of which
> constitute subgoals to prove at each step and that is closed by axioms."

and §5.3, p. 7 `[OCR]`: "At this step, we have the following **partial proof tree** with
$\Delta=\ldots$"; §6, p. 8 `[OCR]`: "A top-down strategy will consist in building a set of
**partial proofs**, the conclusions of which being multi-sets of subformulas of the final
conclusion." Open-versus-closed is load-bearing and source-made: the tree "is closed by
axioms", so nodes not yet closed are the open subgoals.

**MFDI2 — resource-sensitive rule instances source-determined. SATISFIED.** §5.1(c), p. 6
`[OCR]`:

> "(ii) when the principal formula has the form $F_1\otimes F_2$. The goal to prove has the form
> $\vdash F_1\otimes F_2,\Delta'$ and can be replaced by $2^n$ possibilities ($n$ being the
> number of formulas in $\Delta'$) of the subgoals $\vdash F_1,\Delta_1$ and $\vdash F_2,\Delta_2$
> where $\{\Delta_1,\Delta_2\}$ is a partition of $\Delta'$."

The source itself enumerates **all** $2^n$ admissible splits as the complete choice set. No
heuristic split is introduced; retaining all of them is the source's own base non-determinism.

**MFDI3 — pending obligations retain multiplicity and resource content. SATISFIED.** The same
passage writes the two subgoals as $\vdash F_1,\Delta_1$ **and** $\vdash F_2,\Delta_2$ with
$\{\Delta_1,\Delta_2\}$ a partition: each pending sequent carries its own allocated linear
context, and which resources belong to which obligation is explicit in the source's notation.

**MFDI4 — one-step extension preserves premise grouping. SATISFIED, and the source makes the
AND/OR distinction itself.** Immediately preceding the $\otimes$ clause, §5.1(c)(i), p. 6
`[OCR]`:

> "(i) when the principal formula has the form $F_1\oplus F_2$ [sic, OCR] … can be replaced
> **either** by $\vdash F_1,\Delta'$ **or** $\vdash F_2,\Delta'$"

against the $\otimes$ clause's "the subgoals $\vdash F_1,\Delta_1$ **and** $\vdash F_2,\Delta_2$".
The source distinguishes the disjunctive replacement from the conjunctive one in its own
words. That is precisely the joint premise family MFDI4 requires, and it is source-supplied
rather than analyst-imposed.

**MFDI5 — state sufficiency. SATISFIED.** Quotient: a partial proof tree maps to the sequent
labelling the node under consideration. The admissible replacements at that node are, by the
source's §5.1(b)–(c), a function of the goal sequent's principal formula and context alone.
Hence equal states induce equal successor structures, including partitions and joint families.

**MFDI6 — no hidden branch history. SATISFIED for the frozen fragment.** The source's
non-determinism factors (§5.1) that depend on more than the goal — the exponential rules
$w?,c?,?$ (§5.1(b)) and the $\forall$ eigenvariable side condition ("In $\forall$ rule, $y$ is
not free in $\vdash\forall F,\Gamma$", Appendix A, p. 12) — are **all outside MLL without
exponentials and without quantifiers**. Within the frozen fragment nothing below or beside a
node constrains its expansion.

### 5.3 Verdict and the sensitivity finding

$$\boxed{\mathrm{Status}(S6)=\mathbf{READY}\ \text{under \texttt{E0-supplied-v1}};\quad
\mathbf{OPEN}\ \text{under original }\mathfrak{E}_0}$$

Certificate: DI1 (source-recognised restriction of CLL to its multiplicative fragment, plus
forgetting the source's strategy layer to retain the unrestricted relation) + DI2/CDE-v1
($\mathcal{X}_2$'s hyperedge structure is the source's own goal-replacement formulation, with
the partition as label) + MFDI1–MFDI6.

**Finding DF-07 — source-supply / search-provider sensitivity.** `SS-GP94` is a 1994
publication squarely on the frozen disputed component, well inside the evidence cutoff, and
directly decisive for S6. **The frozen SR-B2 v2 query battery never returned it** across all
sixteen prescribed invocations on the available search provider. The gap between S6's original
verdict (OPEN) and its supplied verdict (READY) is therefore attributable to **retrieval
design and provider coverage**, not to the state of the literature. RD-01's warning is
confirmed concretely: SOURCE-FAIL or OPEN under SR-B2 v2 measures the bounded retrieval design,
not the scholarly record. This is a defect of the retrieval procedure, and it is recorded
against the procedure rather than absorbed into any target verdict.

---

## 6. DF-04-H — evaluated at its frozen evaluation point and **REFUTED**

DF-04-H's frozen evaluation point is *after terminal source statuses for all eleven*
(`TR-11:9620`). With S7 READY (original procedure) and S6 READY (`E0-supplied-v1`), all eleven
targets now hold terminal statuses. The hypothesis is evaluated **as frozen**, without
rewording.

> **DF-04-H.** Where a target's dynamics is source-native, the schema passes K-P1; where the
> analyst supplied the dynamics, K-P1 exposes it.

The three dialogue-assembled schemas were **S1, S6, S7** — precisely the three where the
analyst supplied operational content. Outcomes:

| Target | Assembled? | Verdict | Route |
|---|---|---|---|
| S1 | yes | READY | DIRECT, DI1+FDI1–5+CDE-v1 |
| S6 | yes | READY (`E0-supplied-v1`) | DIRECT, DI1+DI2/CDE-v1+MFDI1–6 |
| S7 | yes | READY | DIRECT, DI1+DI2/CDE-v1 |

$$\boxed{\textbf{DF-04-H is REFUTED.}}$$

All three assembled schemas were directly instantiable from source-defined ancestors by
specialization plus canonical definitional expansion. The predicted split between "found" and
"constructed" schemas did not occur. The correct generalisation is the one GPT Turn 34 stated
after S1 and which now holds for all three: **dialogue-assembled ≠ not source-grounded**.

Recorded as a refutation of a hypothesis this programme itself registered and expected to
confirm.

---

## 7. T4 — retained, profile-relative only

Unchanged from Revision 1 in substance; scope restated as required.

At $c_0=(\{S1,S2\},L_\to)$ with $\Gamma_{c_0}=\varnothing$ fixed in $\mathfrak{E}_{0a}$
(`TR-11:4179`), under `E0-c0-only-v1`: $\mathrm{Status}(c_0)=$ **JOINT-YES** at the literal
profile $\mathbf{J}_0$; and $\varphi_{\mathrm{irr}}=\forall x\,\neg(x\to x)$ lies in
$\mathcal{T}_{c_0,\mathbf{J}_0}\setminus\mathrm{Cn}(\varnothing)$, so
$\mathcal{C}_{c_0,\mathbf{J}_0}\neq\varnothing$.

$$\boxed{\textbf{A2 is falsified at }(\mathbf{J}_0,\ G_1,\ K_{1,\mathrm{L\&M}})\textbf{ — and only there.}}$$

**Not profile-invariant.** Under an LK corpus profile with list contexts and an explicit
exchange rule, the instance with two equal adjacent context formulas has premise identical to
conclusion, the graphs are reflexive, $\varphi_{\mathrm{irr}}$ fails, and
$\mathcal{C}_{c_0}$ under that profile is **UNRESOLVED**, not empty.

**Evidence provenance — caveat DISCHARGED.** Revision 2 marked the S1 half transcript-attested.
`SS-LM24` has since been supplied and inspected, and §4bis.2 verifies the claim exhaustively
against Figure 1's actual rule set, including the source's own statement that the exchange rule
is not used. **T4 is now independently verified at $K_{1,\mathrm{L\&M}}$.** Its profile
sensitivity is unchanged and is confirmed rather than weakened: the source itself identifies the
list-plus-exchange presentation as Gentzen's, which is the profile under which
$\varphi_{\mathrm{irr}}$ fails.

**Novelty: UNRESOLVED**, never positive — frozen $\Pi_0$ is unfixed; E1 later tested the full
successor bibliography but retained OPEN translations. Author's own assessment,
recorded so it cannot later read as a novelty claim: irreflexivity of a one-step reduction
relation with trivial steps excluded is standard in rewriting theory, which lies inside
$\Pi_0$. **No novelty is claimed.**

---

## 8. Historical Revision-3 blocked obligations — superseded in E1 only

This table records the state before the 2026-08-21 source recovery. It remains the correct
frozen-E0 history; it is **not** the current E1 status. Current results are in §11 and
`JOINT-RESULTS.md`.

| Obligation | Requires | Status |
|---|---|---|
| $U_0$ extraction ($\mathfrak{E}_{0c}$) | K4 verbatim quotation + exact locator from the eligible primary source of **each of the eleven** targets | **BLOCKED — 8 of 11 primary documents not supplied.** K4 complete for S1, S6, S7: `K4-RECORDS.md`. See `MISSING-SOURCE-MANIFEST.md`. |
| exact $\mathcal{K}_0$, exact $\mathfrak{R}_S$ | full-text inspection per target | **BLOCKED**, same cause |
| exact $\Pi_0$ + certified translations | one authoritative primary source per frozen $\Pi_0$ label | **DOUBLY BLOCKED.** (i) **DF-08** — frozen $\Pi_0$ is UNEXECUTABLE: its twelve labels are internally composite and the frozen text fixes neither individuation nor per-label certification. (ii) The sealed successor `PI0-BIB-v1` fixes both, but 10 of its 12 labels have no supplied document. |
| $W^\ast$ over $U_0$; both arms; $\partial_1$; maximal fragments; common theories; mechanically generated frames; substantive-content test; prior-art tests; P2a→P2b→P1 | a sealed $U_0$ | **BLOCKED**, downstream of the above |
| definability, dependency, irreducibility, rank, minimality, alternative bases | P1 to return; frozen ordering opens rank only then | **BLOCKED**, gate not passed |
| C1–C12 registry | a candidate architecture to run against | **NOT APPLICABLE** — none produced, because P1 never returned |

At Revision 3, every entry was blocked by a **missing primary document**, not by an incomplete search. The
distinction matters: OPEN never counts as NO, and every claim depending on these returns
UNRESOLVED.

---

## 9. Hostile closure audit — Revision 2

### A1 — against T1′: "the countermodels are degenerate"
**Fails.** $\mathsf{Inst}_6$ is *finite MLL sequents* with no balance restriction, and a search
relation is by definition defined on sequents of unknown provability. $S_\wedge$ is balanced
and provable, so the $\mathbf{AND}$ and $\mathbf{TERM}$ refutations do not use degeneracy.

### A2 — against T1′: "the decoder class is gerrymandered to exclude what works"
**Partially succeeds; already conceded in §1.6.** $\mathcal{D}_{\mathrm{succ}}$ deliberately
excludes state-inspecting decoders, and §1.0 states plainly that without that exclusion the
theorem is false. T1′ is explicitly a **bounded** impossibility, not a characterisation, and
BIA's former "iff" is withdrawn (§10).

### A3 — against T3′: "excluding $\mathcal{X}_1$ by MFDI4 is circular"
**Fails.** MFDI1–6 were fixed by GPT Turn 35 *before* S6 retrieval and before any of this
analysis, specifically to be applied de novo to S6. Applying a preregistered admissibility
condition is not circular. The circularity would lie in the *opposite* move — Revision 1's —
which let a structure that fails a preregistered obligation count as a competing witness.

### A4 — against S7 READY: "the finite family $\mathcal{F}$ is analyst-supplied, so DI3 fires"
**Live, and the thinnest point of the S7 certificate.** The source carries one
$(F^\flat,F^\sharp)$ pair; the frozen tuple carries a finite set. The defence is CDE-v1 clauses
1–5 plus the source's own function-space lifting (4.17, p. 519) and systems of abstract
equations (Example 6.15, p. 532). An auditor who reads CDE-v1 more strictly would return S7 to
OPEN pending a source that carries an explicit family. Recorded, not suppressed. It does not
affect the S7 **DI4** finding, which is independent and verbatim.

### A5 — against S6 READY: "Galmiche–Perrier is about *strategies*, so DI3 fires"
**Fails, but narrowly.** The paper's contribution is strategy design, which would indeed be an
analyst-forbidden discipline if imported. Frozen S6 takes the **unrestricted** relation, which
the source presents in §5.1 as the base non-determinism *prior to* strategy application; taking
it is DI1 *forgetting*, the licensed direction. Had frozen S6 required a focused or normalized
search, the verdict would be INELIGIBLE.

### A6 — against S6 READY: "OCR is not full-text inspection"
**Partially succeeds; disclosed.** `SS-GP94`'s body is bitmap-font/scanned and was OCR'd. All
quotations are marked `[OCR]` and symbol corruption is marked `[sic]`. The load-bearing
passages — §5 p. 6, §5.1(c) p. 6, §5.3 p. 7, Appendix A p. 12 — were read as rendered images at
200 dpi and their content is unambiguous in the prose, but a verbatim-fidelity auditor should
re-verify against a clean copy. This is a **transcription-fidelity** limitation, not an access
limitation: the document is present and was inspected.

### A7 — against T4: profile sensitivity, and unverified S1 provenance
**Half succeeds, half now discharged.** The profile-sensitivity half stands and is incorporated:
T4 carries its corpus-profile index and is explicitly not profile-invariant. The provenance half
is **discharged** — `SS-LM24` was supplied and inspected, and §4bis.2 verifies the claim against
Figure 1's actual rule set.

### A10 — against §4bis: "the propositional restriction is analyst-supplied, so DI3 fires on S1"
**Live, and now confirmed as the certificate's thinnest point rather than merely suspected.**
Figure 1 is first-order and the source does not carve out the quantifier-free fragment.
Inspection settles that this is a real gap, not an artefact of incomplete reading. The defence
is unchanged and is DI1's, not DI2's: restriction to a formally specified subclass, stated
independently of any result. An auditor reading SRF-v1 rather than DI1 as governing
within-formalism restriction would return S1 to OPEN, and with it $c_0$, A2, and the mandatory
stratum. Recorded prominently, as Turn 35 required.

### A11 — against `PI0-BIB-v1`: "fixing $\Pi_0$'s individuation is a repair of a frozen object"
**Fails as stated, but the concern is honoured.** Frozen $\Pi_0$ is **not** modified: it is
recorded as UNEXECUTABLE with its defect (DF-08) preserved, and its verdict is kept separate.
The successor is versioned, its selection rule was fixed before assignment, and it was hashed
before any $W^\ast$ candidate or $U_0$ item existed. The continuation packet's proposed
re-individuation into thirteen bodies was **declined**, because the thirteen-count originated in
an error of mine rather than in the frozen text; declining it keeps the successor strictly less
invasive than proposed.

### A12 — against the whole run: "each round of supplied documents flips a verdict, so the
verdicts track supply rather than evidence"
**Partially succeeds, and is the single most important limitation of this programme.** Three
targets have now changed status on document supply (S7, S6, and S1's verification), and DF-07
records that the frozen retrieval battery missed a decisive in-cutoff source. The honest reading
is that SR-B2 v2's *negative* verdicts carry very little evidential weight, exactly as RD-01
warned; its *positive* verdicts, which require a source-level certificate, are unaffected. No
terminal negative in this run rests on a failed search: every negative is either a proof
(SSS-3, T1′) or a preregistered hypothesis refuted by positive certificates (DF-04-H).

### A8 — against DF-04-H's refutation: "S6's READY comes from a successor procedure, so the
evaluation point was reached by changing the rules"
**Live and material.** Under the original $\mathfrak{E}_0$ alone, S6 is OPEN and DF-04-H's
evaluation point is **not** reached. The refutation is therefore relative to
`E0-supplied-v1`. Recorded in the terminal report as such. Note the direction: the successor
procedure was executed on a source supplied by the user, was preregistered outcome-independently,
and produced the verdict *least* favourable to the hypothesis being defended — DF-04-H was the
programme's own prediction.

### A9 — against everything: "CDE-v1 over-permissiveness"
**Live, and now heavier.** CDE-v1 carries `TR-31:1597`'s provenance risk and is now
load-bearing in **three** certificates (S1, S6, S7). Over-generation checks re-run: it does not
rescue $N_1$ member 1 (no partial-derivation notion); it does not admit the HOL goal-stack
(blocked at NM1/SRF-v1); it does not manufacture transformations for S10 (Dung supplies no
stepwise constructor); and by T1′ it does **not** rescue $\mathcal{X}_1$ for S6, which is the
sharpest available test since $\mathcal{X}_1$ is definable from the source yet still fails.
That last check is new and is the strongest evidence so far that CDE-v1 is not unboundedly
wide. It remains short of a proof of optimal restrictiveness, and the owed robustness
programme on unrelated source/target pairs is **still owed**.

---

## 10. Disposition of the Revision-1 theory name

**BIA — "Branching-Internalisation Adequacy" — is withdrawn**, together with its "iff"
formulation, which was a class-level characterisation asserted from two instances. The
surviving content is renamed and downgraded in `DIALOGUE-THEORY.md`.

---

## 11. Revision 4: E1 hostile closure audit

Sections 1–10 are retained as the historical proof ledger. The former missing-source stop is
superseded only in `E1-transparent-source-recovery`; frozen E0 is unchanged.

| ID | Hostile challenge | Disposition | Consequence |
|---|---|---|---|
| A13 | U-c blindness cannot be asserted after cross-target exposure | **succeeds against E0** | U0-E0 is not certified; E1 uses logged source-local isolation |
| A14 | Jeffrey 1965 was never inspected | **succeeds against E0** | S4 remains INSPECTION-OPEN in E0; same-author successor evidence counts only in E1 |
| A15 | frozen $\sigma$ says a seed was published but supplies no value | **succeeds** | secondary E0 order is unexecutable; E1 publishes a versioned seed before its matrix |
| A16 | URL-only sources may disappear | **partially succeeds** | exact hashes, byte/page counts, and locators permit copy verification; third-party PDFs are not redistributed |
| A17 | source recovery after seeing targets is outcome-directed | **narrows** | selection answers frozen target definitions, not matrix outcomes; it is successor evidence and no source is retrofitted into E0 |
| A18 | `u058`/`u059` are trivial aliases, not discoveries | **succeeds** | reported as extensional coincidence; native and calibration rates are never pooled |
| A19 | zero NO certificates makes the observed boundary too wide | **succeeds** | $\partial_1=\varnothing$ but OPEN frontier has 86 items; no complete maximality claim |
| A20 | non-stuttering may belong in the frame, collapsing “content” | **live and material** | frozen frame rule excludes target truths; under an alternative interface convention irreflexivity would be frame-forced, so content is frame-sensitive |
| A21 | LK list/exchange profiles can create self-loops | **succeeds as a scope objection** | irreflexivity remains indexed to `K1-LM-frontier-multiset`; P2b is OPEN |
| A22 | a lower bound is being sold as the common theory | **fails after correction** | only $Cn(\Gamma\cup\{\varphi_{irr}\})\subseteq\mathcal T$ is claimed; exact $\mathcal T$ is UNRESOLVED |
| A23 | rank 1 overstates an unknown theory | **fails after correction** | rank/minimality apply only to the certified irreflexivity kernel |
| A24 | recovered PI0 documents prove novelty | **fails** | several translations remain OPEN; verdict is NOVELTY UNRESOLVED, never positive |
| A25 | secondary sampling can support maximality | **fails** | all 792 secondary cells are recorded, but sampled results are excluded from maximality |
| A26 | “all joint profiles” implies exhaustive mathematics | **fails after qualification** | all four certified profiles are listed; JOINT-COMPLETE is false and the mathematical class is not enumerated |
| A27 | S10 READY smuggles in a transformation | **fails** | only AF/evaluation semantics are READY; native transformation remains unassigned |
| A28 | S5 assembles probability, acyclicity, and intervention from different sources | **fails** | Beckers–Halpern supplies all components in one source |
| A29 | S11 assembles ODE and semigroup facts across sources | **fails narrowly** | Mielke states the gradient equation, globally-Lipschitz ODE uniqueness on arbitrary horizons, global flow assumption, and semigroup in one source |
| A30 | one-step irreflexivity is prior-art commonplace | **succeeds as a novelty warning** | the result is weak and likely familiar; no priority or novelty claim survives |

### 11.1 Exact closure effects

- **Original E0:** blocked at non-repairable assurance/source/seed conditions. No U0-E0 or E0
  W-star result is claimed.
- **E1:** internally terminates: 968 cells have B1/B2 status, 177 frozen-arm fragments have
  joint status, every JOINT-YES fragment has frame/content disposition, and prior art has a
  certificate status.
- **Mathematics:** one profile-relative non-frame sentence survives; 86 extension questions,
  exact common theory, profile robustness, mathematical maximality, and novelty remain OPEN.

### 11.2 Terminal countermodel for the content test

For each witnessed relation-language frame, take a one-element State carrier $\{a\}$ and
$\to=\{(a,a)\}$. It satisfies equality, congruence, relation typing, and the `u058`/`u059`
aliases, while falsifying $\forall x\neg(x\to x)$. Therefore irreflexivity is not frame-forced.
Removing it from the one-generator kernel leaves a model of the frame, establishing rank 1,
irredundancy, and inclusion minimality for that kernel only.
