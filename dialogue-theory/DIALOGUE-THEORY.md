# The dialogue-built theory

**Name (fixed only after the content was fixed): Branching-Internalisation Adequacy — BIA.**

The name is descriptive of the content and carries no claim of priority, novelty, generality,
or relation to any other framework. See `FAR-COMPARISON.md`, written last, for the only
relational claim made anywhere in these artifacts.

---

## 1. What kind of theory this is

Not an operator architecture. Not a shared-vocabulary result. Not a minimal basis.

The strongest result this run supports is a **boundary theory about representation typing**:
a statement of when a chosen state representation is adequate to the rule system it is meant
to represent, plus the observation that this adequacy question is *prior to*, and gates, the
entire shared-vocabulary programme — and that the frozen panel itself failed it at one target.

The closure protocol explicitly admits this outcome shape: *"If the strongest result is a
boundary theory rather than an operator architecture, formalize it as the result — not as
failed FAR."* That is what is done here.

## 2. The content

### BIA — the criterion

Let $R$ be a rule system whose rules have the form $\frac{P_1\ \cdots\ P_k}{S}$ with $k\ge 0$,
where deriving $S$ requires deriving **all** of $P_1,\ldots,P_k$. Let a *state representation*
be a map $q$ from the objects of backward search to a set $\mathsf{St}$, together with an
induced successor structure on $\mathsf{St}$.

> **$q$ is BIA-adequate for $R$** iff the derivability predicate on $\mathsf{St}$ admits a
> purely disjunctive fixpoint characterisation — i.e. the conjunction over sibling premises is
> absorbed into the successor states themselves, so that
> *"$s$ succeeds iff $s$ is terminal-successful or some successor of $s$ succeeds."*

Equivalently: a state representation is adequate exactly when it **internalises the rule
system's conjunctive branching**. Where it does not, the conjunction has to live in the
transition structure's arity, and an ordinary binary relation cannot carry it.

### The two theorems that give BIA content

- **Positive instance (T2.1).** The finite-multiset-of-open-sequents representation is
  BIA-adequate for propositional LK. Proved.
- **Negative instance (T1).** The single-sequent representation is **not** BIA-adequate for
  MLL. Proved by two explicit finite countermodels: the disjunctive reading over-generates at
  $\vdash a^{\perp},a^{\perp},a\otimes b$, and the conjunctive reading under-generates at
  $\vdash a^{\perp},b^{\perp},a\otimes b$. The failure is one of **arity**, not of determinacy:
  retaining all admissible resource partitions is ordinary nondeterminism and is harmless.

Full statements and proofs: `PROOFS.md` T1, T2.

### The boundary datum

The frozen panel assigned a BIA-adequate state typing to S1 (frontier multiset) and a
BIA-inadequate — or at best undetermined — one to S6 (single sequent with resource context),
for two structurally analogous sequent-calculus targets. The shell's own determination check
recorded S6 as satisfying the determination invariant; **that check was wrong**, because it
verified that the rules and the root are fixed without verifying that the arity of the
transition structure is fixed (`PROOFS.md` T3).

$$\boxed{\mathrm{Status}(S6)\in\{\mathbf{UNDERDETERMINED},\ \mathbf{OPEN}\rightsquigarrow\mathbf{SOURCE\text{-}FAIL}\}}$$

Both branches of that disjunction agree that S6 is **not READY** and that the frozen
single-sequent state is inadequate. Distinguishing the branches requires exact Turn-36 text
that is not in the supplied corpus. This is preserved as a **terminal defect of the
$\mathfrak{E}_0$ run**, not repaired: selecting the hyperedge reading because it works is
precisely the analyst construction DI3 exists to block.

### The one piece of shared content actually established

At the calibration fragment $c_0=(\{S1,S2\},L_\to)$, computed under separately versioned
`E0-c0-only-v1` because it is the unique fragment independent of the blocked registry $U_0$:

- $\mathrm{Status}(c_0)=$ **JOINT-YES** at the literal profile $\mathbf{J}_0$, as A2 predicted.
- $\varphi_{\mathrm{irr}} = \forall x\,\neg(x\to x)$ holds in every admissible LK proof-search
  graph and every admissible CSP propagation graph, and is not logically valid.
- Hence $\mathcal{C}_{c_0,\mathbf{J}_0}\neq\varnothing$ and the preregistered prediction **A2 is
  falsified** at $(\mathbf{J}_0,\ G_1,\ K_{1,\mathrm{L\&M}})$.

Stated without inflation: $\varphi_{\mathrm{irr}}$ is a weak law, half-conventional on the S2
side, and its novelty verdict is **UNRESOLVED** — with the author's own assessment recorded
that it is almost certainly subsumed by rewriting theory, which lies inside $\Pi_0$. **No
novelty is claimed.**

And it is **not profile-invariant**: under an LK corpus profile using list contexts with an
explicit exchange rule, the exchange instance with two equal adjacent formulas has premise
identical to conclusion, the graphs are reflexive, and $\varphi_{\mathrm{irr}}$ fails. Under
that profile $\mathcal{C}_{c_0}$ is **UNRESOLVED**, not empty. A2's truth value is
corpus-profile-relative — which is the sharpest vindication in this run of the K-P4 decision
to carry corpus-profile indices into every downstream result.

## 3. What is *not* claimed

- No shared vocabulary across the panel. $U_0$ was never populated.
- No maximal jointly interpretable fragment, no first-failure frontier $\partial_1$, no
  common-law theory beyond the single fragment above. All require $U_0$.
- No definability, dependency, irreducibility, rank, minimality, or alternative-basis result.
  The frozen ordering opens rank questions only after P1 returns, and P1 never returned.
- No novelty, for anything.
- No universality, representativeness, or breadth. $D_0^{\mathrm{plan}}$ is an explicit
  methodological panel of eleven schemas chosen by two models during protocol development;
  panel sensitivity is untested and untestable at $|D_0^{\mathrm{plan}}|=11$.
- No evaluation of DF-04-H. Its frozen evaluation point is *after terminal statuses for all
  eleven*, and S7 has none. The partial pattern — of the three dialogue-assembled schemas,
  S1 passed, S6 failed, S7 is unresolved — is recorded and explicitly **not** promoted.
- No claim that BIA is new. It is a criterion made precise and proved in two instances; the
  underlying observation that AND/OR search structure must be represented as such is old.
  What is established here is the *proof pattern* and the *audit consequence*, not priority.

## 4. Scope of BIA

BIA is stated for rule systems with multi-premise conjunctive rules and proved for exactly two:
propositional LK (adequate under the frontier representation) and MLL (inadequate under the
single-sequent representation). It is **not** established for any other target in the panel and
is **not** a class theorem. Promoting it would require Stage-B treatment: a candidate-
independent, natively determinate admission predicate, with proof rather than finite-panel
induction. That work is not done.

## 5. Falsifiers

- **BIA's negative instance (T1)** is falsified by exhibiting a binary relation on MLL
  sequents, derived from the MLL rule instances without added analyst structure, whose induced
  provability predicate agrees with MLL provability everywhere.
- **BIA's positive instance (T2.1)** is falsified by an LK rule system and a frontier
  configuration where the disjunctive recursion fails.
- **T3** is falsified by an exact-text adjudication fixing frozen S6's transition arity, which
  would move S6 from UNDERDETERMINED into the ordinary source-adjudication track.
- **T4** is falsified by showing $\varphi_{\mathrm{irr}}$ fails in some admissible instance of
  S1 or S2 under the certified corpus profile, or by showing $\Gamma_{c_0}\neq\varnothing$.
