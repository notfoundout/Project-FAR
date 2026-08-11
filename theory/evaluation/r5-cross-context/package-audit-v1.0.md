# Adversarial package audit

**Performed before the package was declared frozen.** The audit attacks the package. Findings that required repair are recorded with the repair; findings that survive are recorded as residual risk.

---

## 1. Attack surface examined

| Attack | Finding | Disposition |
|---|---|---|
| Programme vocabulary in delivered text | None after repair | Mechanically enforced by `verify_r5_package.py` against 76 watchlist terms |
| Semantic paraphrase leakage | `commitment`, `ground`, `stake`, `admissibility`, `calculus`, `supersession`, `provenance`, `uniform recovery`, `machinery` all banned as bare tokens, not merely as programme identifiers | Enforced |
| Hidden target assumptions in the question | The first draft described the phenomenon as systems that "take in information, hold and change positions in light of it, and arrive at conclusions" — this gestures at three of the five target requirements at once | **Repaired.** Replaced with "work through a question or problem and arrive at conclusions, judgements, or decisions", which asserts no structure about what happens in between |
| Examples that prime a target architecture | The only example corpus available to the packet author is the programme's own | **Repaired by omission.** No examples are given. Item A asks the respondent to fix scope themselves, so scope becomes an output rather than an input |
| Field seeding of the literature search | Naming any of the six fields the prior comparison used would steer the search | **Repaired by omission**, and mechanically enforced: 24 field-seed terms banned from delivered text |
| Outcome asymmetry | **Repaired twice; the first repair was itself a defect.** The original packet listed mostly positive outcomes. The first repair replaced that with six outcomes of which **all six** were negative, pluralistic, or dissolving and **none** positive — which signals that a negative result is wanted just as clearly as the original signalled the opposite. See §5 | **Repaired.** Both packets now carry a balanced set: two unified-positive shapes, two pluralistic, two negative or undecidable, explicitly unranked and explicitly non-exhaustive |
| Evaluator discretion | Role C could choose an outcome after seeing origins | Constrained: outcomes pre-registered with per-outcome evidence requirements; `O1` requires explicit recovery or logical consequence on **every** element at `C0`/`C1` and tier `T4`+; origins anonymized where practical |
| Mapper discretion | Role B could manufacture agreement | Constrained: five-class recovery scale with `FORCED RECONSTRUCTION` carrying **no** weight; auxiliary definitions absent from Role A force that class automatically; reverse direction mandatory; failed mappings preserved; six explicit mapper declarations |
| Post-hoc flexibility | The comparison rubric could be chosen after seeing the answer | Constrained: the primary criterion is Role A's own `comparison_H`; applying a project criterion where Role A supplied one, or supplying one where they did not, **invalidates the adjudication** |
| Contamination loopholes | Questionnaire administered too early would itself disclose the programme | **Repaired.** Administration ordered after the answer is final and hashed, before reveal |
| Contamination used to discard inconvenient results | Wholesale discarding would let contamination filter out divergence | **Repaired by the asymmetry rule**: contamination degrades agreement evidence only, never divergence evidence |
| Architecture leakage | Asking Role A to produce an architecture before their contract is frozen would let the architecture question shape the contract | **Repaired by ordering.** The architecture phase runs only after the contract answer is frozen and hashed, and is separately frozen before reveal |
| Ambiguous stopping conditions | An executor could declare the package frozen while decisions remain | Constrained: seven named decisions that, if left to the executor, mean the package is **not** frozen |
| Tier inflation | Context separation could be reported as independence | Constrained: five tiers with explicit `cannot_establish` lists; `T1`/`T2` may never be called replication; `LIM-031` addressed only from `T4` and **not closed by `T5` alone** (see §6) |
| Verifier vacuity | The blinding check could scan nothing and pass | **Repaired.** The first implementation cut the scanned span at the first non-delivered heading, which in both packets is §1, so it scanned almost nothing and passed vacuously. Now the delivered span is extracted explicitly (§2 through §4) with a 600-character floor that fails closed |
| Verifier false positives masking real leaks | Substring matching on short acronyms fires inside ordinary words | **Repaired.** `UPP` matched inside "supplied" and `FARE` would match inside "welfare". Short acronyms are now word-boundary matched. A check that cries wolf trains its reader to ignore it |

## 2. Negative control on the verifier

The verifier was tested against a deliberately leaked packet containing `commitments`, `grounds`, and `Blackwell`. It reported `FAIL` on all three and returned to `PASS` when the packet was restored. The check is therefore known to be live rather than vacuously passing.

## 3. Clean-room read

> *Could a respondent infer the target answer from the packet?*

Read as an uninformed recipient, the delivered text supplies: a thin description of a phenomenon, one question about what carries over between two descriptions of one episode, nine sub-questions, a balanced and explicitly non-exhaustive list of six answer shapes, and an instruction that there is no target answer. It supplies no vocabulary, no examples, no fields, no reading list, no structure of the expected answer beyond the A–I headings, and no indication that a prior answer exists.

**Residual inference risk, recorded rather than dismissed:** the A–I decomposition itself tells the respondent that scope, observables, droppable distinctions, carry-over, sameness, legitimate rewritings, assumptions, and comparability are the axes worth separating. That is a structural hint. It is retained because the protocol requires answers along those axes to be comparable at all, and removing it would make the output unmappable without the mapper supplying structure — which is a worse contamination. Packet B mitigates it by asking the same question without that decomposition and with a different primitive object, so any artefact of the A–I structure should show up as A/B divergence.

This residual risk is a **known limitation of the instrument**, disclosed here and carried on every claim the package eventually supports.

## 4. What the audit did not do

It did not test the packet on any respondent. It could not: doing so would consume a run and is outside the authorised scope. The clean-room read is a read, not a trial. The first genuine test of the packet's blinding is the first `C0` run's answer to questionnaire item `Q12`, which asks whether the respondent formed a belief about the wanted answer — and a `C5` result there triggers a re-audit before further runs.

---

## 5. Second-round audit: outcome priming

**Finding.** The first repair of the outcome list overcorrected. Counting the delivered list in the original Packet A: *ill-posed*, *several equally defensible*, *domain-relative*, *no non-trivial answer*, *additional structure required*, *unable to reach a stable answer* — **zero of six** describe a unified positive answer. §1 of this audit previously recorded that imbalance as a repair, on the reasoning that it counters positive-result bias. That reasoning is wrong. A respondent reading the list for cues learns that a negative or dissolving result is anticipated, which is directional information of exactly the kind the packet is supposed to withhold. Packet B carried the same defect in a single sentence: four acceptable outcomes, none positive.

**Alternatives tested.**

| Option | Directional information | Other cost | Verdict |
|---|---|---|---|
| **A** retain the current list | High, toward negative. Zero of six shapes are positive | — | **Rejected.** The imbalance is the defect |
| **B** drop the enumeration; say only that any conclusion including no stable answer is acceptable | Reduced but non-zero. Naming only the negative case foregrounds it, so the residual signal still points one way | Lowest enumeration cost | **Rejected.** Better than A, still directional |
| **C** balanced set: positive, pluralistic, negative, undecidable, no numerical imbalance | Near zero. No shape is over- or under-represented | Enumeration signals which shapes were anticipated, which may suppress an unlisted shape | **Selected**, with the enumeration cost mitigated |

**Repair.** Option C, refined. Both packets now carry two unified-positive shapes, two pluralistic, two negative or undecidable, and both state explicitly that the list is **neither exhaustive nor ranked** and that an unlisted shape is equally acceptable. The heading changed from "Outcomes that are equally acceptable" to "Shapes an answer may take", which does not presuppose that the answer is an outcome of a decision procedure.

**Residual, disclosed:** any enumeration tells the respondent which shapes were anticipated. This is non-directional and is mitigated by the explicit non-exhaustiveness clause, but it is not eliminated. It is a known limitation of the instrument.

## 6. Second-round audit: T5 against the stopping rule

**Finding.** T5 read *"executing under their own preregistration"*, which is ambiguous between (A) independently preregistering faithful execution of this frozen protocol and (B) independently designing a different protocol. Under reading B, T5 is not an execution tier of this package at all, and the stopping rule — which requires the executor to make no methodological decision — does not govern it. The ambiguity therefore put the tier table and the stopping rule in conflict.

**Resolution: interpretation A, stated explicitly.** T5 is an execution tier of this package. The executing organization supplies procedural and organizational independence while making no methodological decision, because every such decision is fixed here. Seven administrative additions are enumerated as permitted; nine alterations are enumerated as creating a new protocol version and therefore not being T5 at all. Procedural independence and methodological alteration are now distinguished rather than blurred.

**Interpretation B is reclassified** as class `X1 — independent protocol design`, explicitly **not** an execution tier, which this package cannot produce.

**Consequential correction to a claim this package previously made.** The package asserted that `LIM-031` is *"closed only at T5"*. That is **withdrawn as overstated**. `LIM-031` has two halves: no external party has *evaluated* a preservation contract, and no external party has *chosen* the question or comparison procedure. A faithful T5 execution supplies an externally authored **answer** but not an externally chosen **question** — the wording, the A–I decomposition, and the comparison procedure remain programme-authored, and the residual structural hint disclosed in §3 survives any faithful execution. T5 therefore **substantially addresses** `LIM-031` without closing it. Full closure requires T5 **and** X1.

This correction makes the package weaker and more honest: it removes a closure claim the instrument cannot support.
