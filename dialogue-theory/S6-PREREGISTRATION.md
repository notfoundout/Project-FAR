# S6 — SR-B2 v2 preregistration, recorded BEFORE execution

Per `PROTOCOL.md` §6. Written and fixed before any S6 search invocation. Queries are not
modified after seeing results.

## Frozen target (unchanged, not repaired)

- **Formalism:** MLL — multiplicative linear logic without exponentials; sequent-calculus
  proof search (`TR-11:3178`).
- $\mathsf{Inst}_6$: finite MLL sequents (`TR-11:4076`).
- **Native state:** *sequent with resource context* (`TR-11:2145`).
- **Native transformation:** *one rule application* (`TR-11:2145`).
- $\mathcal{S}_{6,a}$: backward MLL search graph (`TR-11:4076`).
- $\mathfrak{R}_6$: $r_{\mathrm{syn}}$ = (sequent + context, identity mod α);
  $r_{\mathrm{prov}}$ = (MLL provability, provability equivalence) (`TR-11:3211`).
- Panel label: $D_{\mathrm{adv}}$ — admitted because prior analysis predicted non-cartesian
  $\delta$ would stress candidate universality. **This is a selection rationale, never an
  expectation that S6 must fail** (`TR-31:1519`).

## Fixed retrieval parameters

$$F_6 = \texttt{multiplicative linear logic}$$
$$C_6 = \texttt{sequent with resource context}$$

$C_6$ is taken **verbatim** from the frozen native-state specification, exactly as $C_1$ was
taken verbatim from S1's *"state = finite multiset of open sequents"*.

## Channel A — six fixed queries, preregistered verbatim

1. `"multiplicative linear logic" "sequent with resource context"`
2. `"multiplicative linear logic" "formal definition" "sequent with resource context"`
3. `"multiplicative linear logic" semantics "sequent with resource context"`
4. `"multiplicative linear logic" "operational semantics" "sequent with resource context"`
5. `"multiplicative linear logic" formalization "sequent with resource context"`
6. `"multiplicative linear logic" definition`

All six execute for a negative result. Existential early stop only on a certified
EXACT/DIRECT. No saturation stopping, no cost truncation, no query substitution on a
zero-result invocation.

## Channel B

$N_6$ built under NM-v1 from Channel-A title/abstract/snippet only, max 5, ordered by first
query of appearance then result position. Two follow-ups per member (Q7 `"<T>" "<A>"`,
Q8 `"<A>" "<F_6>" "<C_6>"`). Top-level results only; bibliography entries logged as $L_6$.

## Adjudication order

K-P1 → DI1–DI6 (with SRF-v1, CDE-v1) → **MFDI1–MFDI6 de novo** → K-P2 → K-P4.

**No FDI3/FDI4/FDI5 verdict is inherited from S1** (`TR-31:1282`). MFDI is applied fresh.

## TSI-v1 fixed search terms for S6

Mechanically derived from the frozen disputed component $C_6$ and the MFDI conditions:

*proof search · search state · open premise · open premises · sequent · resource ·
context · multiset · frontier · backward · transition · partial derivation · incomplete ·
splitting · partition · tensor*

## Directional disclosure (recorded before results)

The prior expectation entering S6 is **not** neutral: GPT Turn 35 identified AND-branching
(MFDI4) and resource-content preservation (MFDI3) as the likely failure points for the frozen
single-sequent state, and the resume summary reports that a proposed `S6 = SOURCE-FAIL` was
**rejected as terminal** because MFDI3 ruled out ordinary $\mathsf{Seq}\times\mathsf{Seq}$
while a permitted resource-labelled hyperedge might preserve joint premises. Both directions
are therefore live. The frozen procedure, not this expectation, decides the verdict.
