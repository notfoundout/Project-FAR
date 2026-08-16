# The dialogue-built theory

**Revision 3.** The Revision-1 name and formulation remain withdrawn; see §5. SSS-3's scope is extended to propositional LK, verified from a primary source.

**Name (fixed after the content was fixed): Search-State Sufficiency — SSS.**

Descriptive only. No claim of priority, novelty, generality, or relation to any other
framework. See `FAR-COMPARISON.md`, written last.

---

## 1. What kind of theory this is

Not an operator architecture. Not a shared-vocabulary result. Not a minimal basis. Not a
characterisation.

A small **sufficiency taxonomy** for backward-proof-search representations, consisting of two
positive sufficiency results and one bounded impossibility, together with the use of that
taxonomy as an admissibility filter on frozen target specifications. The closure protocol
admits this outcome shape: *"If the strongest result is a boundary theory rather than an
operator architecture, formalize it as the result — not as failed FAR."*

## 2. The content, with its indices

Every claim is indexed by **state type**, **transition structure**, and — for the negative —
**decoder class**. Nothing is asserted outside those indices.

| | State type | Transition structure | Verdict for MLL |
|---|---|---|---|
| $\mathcal{X}_1$ | individual sequent | rule-induced binary relation | **insufficient**, over $\mathcal{D}_{\mathrm{succ}}$ (SSS-3) |
| $\mathcal{X}_2$ | individual sequent | resource-labelled hyperedges | **sufficient** (SSS-2) |
| $\mathcal{X}_3$ | frontier multiset | binary relation | **sufficient** (SSS-1) |

**SSS-1 (frontier sufficiency).** For any rule system with finitary rules, the frontier
representation admits a purely disjunctive fixpoint characterisation of closability. Holds
uniformly — LK and MLL alike.

**SSS-2 (hyperedge sufficiency).** On individual sequents, one hyperedge per rule instance
(labelled, for MLL, by the resource partition) yields the standard AND/OR characterisation.

**SSS-3 (bounded individual-sequent insufficiency).** Over the state type of individual MLL
sequents, with the **rule-induced projected relation** as the only admissible representation and
**uniform monotone successor-set decoders** $\mathcal{D}_{\mathrm{succ}}$ as the decoder class,
no representation/decoder pair computes MLL provability. The decoder class has exactly four
members and all four are refuted by two explicit finite witnesses.

Proofs: `PROOFS.md` §1–§2.

## 3. What SSS explicitly does not say

- **It is not an "iff" and not a characterisation.** Revision 1 asserted a class-level
  equivalence from two instances. Withdrawn.
- **It is not an impossibility for binary relations as such.** $\mathcal{X}_3$ *is* a binary
  relation and is sufficient. The Revision-1 framing in terms of "arity" was imprecise and is
  withdrawn: a binary relation on a rich enough state encodes conjunction perfectly well.
- **SSS-3 is false without its two class restrictions**, and `PROOFS.md` §1.0 gives the
  counterexamples: an arbitrary binary relation can encode the answer, and a state-inspecting
  decoder can recompute provability from the sequent alone.
- **It is not a claim that LK is better behaved than MLL.** The frozen shell's S1/S6 contrast
  is a contrast of **state typing**, not of logic. Had S6 been given a frontier state it would
  have been sufficient; had S1 been given an individual-sequent state it would have faced
  SSS-3's problem under presentations satisfying the witness conditions.
- **It is not claimed novel.** SSS-1 and SSS-2 are elementary and are very probably folklore —
  goal stacks and AND/OR search are old. What this run contributes is their use as a
  preregistered admissibility filter on target specifications. No novelty verdict is available
  for anything, because $\Pi_0$ is unfixed and the frozen rule returns novelty **UNRESOLVED,
  never positive**, on an uncertified translation.

## 4. Scope and profile sensitivity

SSS-3's witness conditions (W1), (W2) are verified for **MLL**, and — from `SS-LM24` Figure 1,
p. 277 — for **propositional LK under the certified corpus profile $K_{1,\mathrm{L\&M}}$**:
$p\vdash q\wedge p$ witnesses (W1) and $p\vdash p\vee q$ with the $i=2$ instance of $\vee R$
witnesses (W2). That presentation also makes $\supset L$ and $cut$ multiplicative, so the
context-splitting phenomenon driving SSS-3 for MLL is present in LK too. A purely
additive-context presentation with no single-conjunct $\vee R$ remains undecided — a
presentation question, not an open mathematical one. SSS-1 and SSS-2 hold for any finitary rule
system.

Nothing is promoted to a class theorem. Stage-B promotion — a candidate-independent, natively
determinate admission predicate, established by proof rather than finite-panel induction — is
**not attempted**.

## 5. Disposition of the Revision-1 theory

**BIA — "Branching-Internalisation Adequacy" — is withdrawn**, with its "iff", its arity
framing, and its claim that Turn 17's S6 determination check was incorrect. What survives is
SSS above, which is weaker, indexed, and proved.

## 6. Where the theory was applied, and what it decided

Used as an admissibility filter under the frozen MFDI obligations, SSS decided one live
question: $\mathcal{X}_1$ fails MFDI4 and is therefore **not** an admissible competing structure
for frozen S6, so exactly one admissible structure ($\mathcal{X}_2$) remains and S6's
determination invariant **holds**. That is what removed the Revision-1 UNDERDETERMINED verdict
and returned S6 to the ordinary source track, where the supplied primary source then closed it.

## 7. Falsifiers

- **SSS-3** is falsified by a member of $\mathcal{D}_{\mathrm{succ}}$, paired with the
  rule-induced projected relation, that computes MLL provability; or by showing the four-decoder
  lemma incomplete.
- **SSS-1** is falsified by a finitary rule system and a frontier configuration where the
  disjunctive recursion fails.
- **SSS-2** is falsified by a rule instance whose hyperedge fails to preserve the joint premise
  family.
- The **application** in §6 is falsified by an admissible structure over frozen S6's state type,
  inequivalent to $\mathcal{X}_2$, that satisfies MFDI1–MFDI6.

## 8. The separate empirical results

These are results of the experiment, not of SSS:

- **A2 falsified** at $(\mathbf{J}_0, G_1, K_{1,\mathrm{L\&M}})$ by $\forall x\,\neg(x\to x)$ —
  profile-relative, weak, novelty UNRESOLVED. Now **independently verified** from `SS-LM24`:
  irreflexivity checked exhaustively against Figure 1's rule set, and the source states in its
  own words that the exchange rule is not used.
- **DF-04-H refuted** at its frozen evaluation point: all three dialogue-assembled schemas
  (S1, S6, S7) reached READY by direct instantiation. Relative to `E0-supplied-v1`, since S6's
  terminal status came from a supplied source.
- **DF-07 recorded**: the frozen SR-B2 v2 battery never returned a 1994 publication squarely on
  S6's disputed component. The gap between S6's original verdict (OPEN) and its supplied verdict
  (READY) is a property of the retrieval design, not of the literature.
- **DF-08 recorded**: frozen $\Pi_0$ is **UNEXECUTABLE** — its twelve labels are internally
  composite and it fixes neither individuation nor per-label certification. My own earlier count
  of thirteen was wrong and is corrected. The sealed successor `PI0-BIB-v1` repairs this
  prospectively; the frozen verdict is preserved.
