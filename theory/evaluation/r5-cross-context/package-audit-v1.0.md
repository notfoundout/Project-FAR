# Adversarial package audit

**Performed before the package was declared frozen.** The audit attacks the package. Findings that required repair are recorded with the repair; findings that survive are recorded as residual risk.

---

## 1. Attack surface examined

| Attack | Finding | Disposition |
|---|---|---|
| Programme vocabulary in delivered text | None after repair | Mechanically enforced by `verify_r5_package.py` against the registered lexical watchlist |
| Semantic paraphrase leakage | Registered load-bearing paraphrases are banned from participant-facing text | Lexically enforced; this is not proof of absence of semantic leakage |
| Hidden target assumptions in the question | The first draft described the phenomenon as systems that "take in information, hold and change positions in light of it, and arrive at conclusions" — this gestures at three of the five target requirements at once | **Repaired.** Replaced with "work through a question or problem and arrive at conclusions, judgements, or decisions", which asserts no structure about what happens in between |
| Examples that prime a target architecture | The only example corpus available to the packet author is the programme's own | **Repaired by omission.** No examples are given. Item A asks the respondent to fix scope themselves, so scope becomes an output rather than an input |
| Field seeding of the literature search | Naming any of the six fields the prior comparison used would steer the search | **Repaired by omission**, and mechanically enforced against the registered field-seed watchlist |
| Outcome asymmetry | **Repaired twice; the first repair was itself a defect.** The first repair produced six shapes of which none were unified-positive | **Repaired.** Primary/reword packets now carry a balanced set; B2 is explicitly non-exhaustive and unranked |
| Evaluator discretion | Role C could choose an outcome after seeing origins | Constrained by the frozen two-layer outcome registry and source-anonymization where practical |
| Mapper discretion | Role B could manufacture agreement | Constrained by the five-class recovery scale; `FORCED RECONSTRUCTION` carries no recovery weight; failed mappings are preserved |
| Post-hoc flexibility | The comparison rubric could be chosen after seeing the answer | Constrained: the primary criterion is Role A's own `comparison_H`; supplying a project criterion where Role A did not is prohibited |
| Contamination loopholes | Questionnaire administered too early would itself disclose the programme | **Repaired.** It is administered only after every Role-A evidentiary answer is frozen and hashed |
| Contamination used asymmetrically | Earlier rule degraded agreement but gave divergence full weight | **Withdrawn.** Descriptive value is retained; independence value degrades in both directions |
| Architecture leakage | Architecture phase could be shaped by the questionnaire | **Repaired by ordering.** Contract → freeze → optional architecture → freeze → questionnaire → reveal |
| Ambiguous execution stopping | Executor could make material decisions after freeze | Constrained by the preregistered execution and campaign stopping rules |
| Tier inflation | Context separation could be reported as investigator independence | Constrained by T1–T5 definitions and explicit `cannot_establish` lists |
| Verifier vacuity | Blinding check initially scanned almost nothing | **Repaired.** Participant-facing spans are explicitly extracted and length-checked; registered non-packet messages are also scanned |
| Verifier false positives | Short-acronym substring matching fired inside ordinary words | **Repaired.** Short acronyms are word-boundary matched |

## 2. Negative control on the verifier

The verifier was tested against deliberate leaks and returned `FAIL`, then returned to `PASS` after restoration. The check is known to be live rather than vacuously passing.

## 3. Clean-room read

> *Could a respondent infer the target answer from the packet?*

Read as an uninformed recipient, Packet A supplies a thin description of the phenomenon, one preservation/equivalence question, nine sub-questions, a balanced and explicitly non-exhaustive set of answer shapes, and an instruction that there is no target answer. It supplies no programme vocabulary, examples, field list, reading list, or indication that a prior answer exists.

**Residual inference risk, recorded rather than dismissed:** the A–I decomposition itself tells the respondent which axes are worth separating. Control `B2` removes the axis list entirely. Any A/B2 difference under this package remains **descriptive only** because respondent and packet effects are confounded; the package licenses no causal framing claim.

The optional architecture question itself discloses that a structuring question is of interest. It is therefore asked only after the contract answer is frozen. It cannot contaminate that frozen contract answer, but its disclosure limitation travels with every architecture-phase claim.

## 4. What the audit did not do

It did not test the packet on any respondent. Doing so would consume a run and is outside the authorized scope. A clean-room read is not a participant trial.

---

## 5. Second-round audit: outcome priming

**Finding.** A prior repair overcorrected the answer-shape list to zero unified-positive examples. That was directional priming toward negative/dissolving results.

**Alternatives tested:** retain the negative-heavy list; remove enumeration but single out a negative case; or use a balanced, explicitly unranked and non-exhaustive set. The balanced set was selected. Enumeration itself remains a disclosed limitation because it reveals anticipated answer shapes.

## 6. Second-round audit: T5 against the stopping rule — **SUPERSEDED IN PART BY §7 ROW 12**

The second-round audit correctly distinguished faithful external execution from independent protocol design, but it then **overstated the governance consequence** by treating `LIM-031` as two necessary-and-sufficient halves and saying full closure required `T5 + X1`.

That closure analysis is retained only as provenance. **It is withdrawn.** The current adjudication is in §7 row 12 and in `evidence-tier-rules-v1.0.json`: `LIM-031` remains its original external-selection/evaluation deficit; programme-authored framing is separately registered as `LIM-032`; no necessity or sufficiency relation between T5 and X1 is claimed.

---

## 7. Third-round adversarial review (2026-08-11) — findings and repairs

Twenty-one defect classes were raised externally; all were verified against the text. Further defects were found during verification.

| # | Defect | Repair |
|---|---|---|
| 1 | Verifier modelled only packet §§2–3 as participant-facing, leaving fallback text unchecked | `participant-surface-v1.1.json` registers the complete authorized pre-reveal surface; unregistered text fails closed |
| 2 | Packet A provenance still claimed deliberate negative overrepresentation | Corrected; failed 6:0 repair preserved only as provenance |
| 3 | Contamination asymmetry invalid | Replaced by descriptive-value vs independence-value model; independence degrades in both directions |
| 4 | Architecture phase ordered after the questionnaire; procedure/schema also disagreed | Reordered contract → freeze → architecture → freeze → questionnaire → reveal; contradiction removed |
| 5 | Packet B reproduced A–I while adding a pragmatic criterion | Replaced by B1 semantic-preserving reword and B2 decomposition ablation |
| 6 | Target read "as registered on main" | Pinned to evidence-base commit `3ba4986` with target-source hashes |
| 7 | `repository_base` overloaded | Split into explicit evidence-base/protocol revision fields |
| 8 | T4/T5 eligibility underdefined | Capability-based T4 criteria and explicit organizational T5 criteria |
| 9 | Only favorable O1 carried an independence bar | Two-layer outcome model with direction-neutral warrant gates |
| 10 | F1–F6 not operationalized | F2/F3/F4 single-run testable; F1/F5/F6 multi-run cumulative and not operationalized for aggregate claims |
| 11 | No campaign policy; optional stopping open | Frozen as single-run descriptive pilot; repeated-run claims blocked pending a future aggregation protocol |
| 12 | `LIM-031` silently redefined into two halves | `LIM-031` left unchanged; separate framing deficit registered as `LIM-032`; no necessity/sufficiency claim |
| 13 | File-count ambiguous and earlier counts named different sets | **18 tracked files = 17 frozen payload artifacts + 1 verifier; 17 files are hashed by the manifest, which cannot self-hash** |
| 14 | "No semantic paraphrases" overclaimed from finite lexical scanning | Narrowed to lexical absence of registered watchlist terms; semantic clean-room read kept separate |
| 15 | No separate review gate | Added as a process-quality gate, not an independence claim |

**Found during verification:**

- the manifest originally hashed a directory scan, permitting stray files to enter the freeze; now it hashes a declared list;
- procedure and Role-A schema contradicted on architecture/questionnaire ordering; corrected;
- the original B1/B2 delivered-span extractor needed end-of-file termination; corrected fail-safe.

## 8. Negative controls, third round

Six controls were required to fail and to return to `PASS` after restoration:

| Control | Required result |
|---|---|
| banned programme identifier in packet body | FAIL |
| banned registered paraphrase in packet body | FAIL |
| banned field seed in packet body | FAIL |
| contamination inserted into fallback string | FAIL |
| contamination inserted into architecture-phase wording | FAIL |
| unregistered participant-facing string | FAIL |

## 9. Separate adversarial review pass (2026-08-11)

A separate post-repair pass found that B2 lacked an explicit non-exhaustiveness clause. That defect was repaired and hashes were regenerated. The pass is a **process-quality review, not independent evidence**.

## 10. Final consistency repair and bounded review-loop rule

A later full-state audit found additional cross-surface defects that did not require a new research campaign: the README still placed the contamination questionnaire before the optional architecture phase; the architecture-phase fallback named particular nonpositive answer shapes; the package audit contained a stale file count; the active X1 tier text still called framing the "remaining half" of `LIM-031`; and provenance text referenced the wrong manifest filename. Those are corrected in the current package.

**Review-loop stop condition:**

**Counter initialization:** this rule applies prospectively from its registration. The failure counter starts at zero here. Review rounds completed before this rule existed are historical provenance and do not count toward the three-cycle failure stop.

- **Success:** after the latest substantive repair, one complete logically separate adversarial review finds zero new substantive defects, all required checks and the semantic sweep pass, and no substantive file changes occur afterward. Review stops; re-reviewing the unchanged state is prohibited.
- **Reset:** any substantive repair resets the clean-pass count to zero and requires exactly one new separate adversarial review. Editorial-only changes that cannot affect participant exposure, methodology, warrant, target identity, role separation, contamination, campaign interpretation, governance scope, or hash integrity require validation but do not reset the loop.
- **Failure:** if three consecutive post-completion adversarial review cycles after this rule's registration each discover at least one new substantive defect, stop without merge and mark `REVIEW_EXHAUSTED_NOT_MERGE_READY`. Further repair requires a different model/provider or qualified human reviewer and explicit authorization.

This rule prevents both endless review of an unchanged clean state and endless same-reviewer repair loops.
