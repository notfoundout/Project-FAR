# Reveal packet — RESTRICTED

> **RESTRICTED ARTIFACT.** This file must never be delivered, shown, quoted, summarised, or linked to Role A, before or during elicitation. It is released to Role B only after every freeze step in `freeze-procedure-v1.0.md` §3 steps 1–8 is complete and recorded. Releasing it earlier destroys the run.

---

## 1. Release gate

Role B may open this file only when all of the following are recorded for the run:

- [ ] Role A declared the answer final.
- [ ] Raw output preserved byte-for-byte and SHA-256 recorded.
- [ ] Timestamp recorded.
- [ ] Sources recorded and classified.
- [ ] Contamination questionnaire administered and level assigned.
- [ ] Optional architecture phase, if run, separately frozen and hashed.
- [ ] Reveal timestamp about to be recorded.

If any box is unchecked, stop. The run is a procedural failure and is preserved as such.

---

## 2. The programme's formulation, stated for mapping

The programme's target formulation is the pair `C*`/`P*` over the admissible representation family `E*`, as registered on `main`. Role B reads it from the canonical records rather than from any paraphrase:

- Source class `C*` and preservation contract `P*`: `docs/research/ikd-w7-lower-bounds-v1.0.md`, `docs/research/tue-w4-final-question-answer-v1.0.md`
- Admissible representation family `E*` and machinery closure: same records
- The derived architecture, for the **separate** architecture-phase comparison only: `docs/research/ikd-w3-common-factor-v1.0.md`, `docs/research/ikd-w9-terminal-adjudication-v1.0.md`
- Current claim scope and what is **not** established: `docs/research/contract-frontier-discovery-v1.0.md` §0, `theory/evaluation/far-canonical-universality-decision-v1.0.json`

**Role B must read `contract-frontier-discovery-v1.0.md` §0 before mapping.** It records which prior comparison claims were withdrawn, so that Role B does not reintroduce a withdrawn rubric.

---

## 3. Ordering rule

The **contract-to-contract** comparison is performed and recorded first, and completely, before the architecture material in §2 is opened. If the architecture phase was run, its comparison is a second, separately recorded exercise.

Collapsing the two into a single agreement judgement invalidates both.

---

## 4. Prohibitions on Role B

- Do not alter, strengthen, weaken, reinterpret, or repair Role A's formulation.
- Do not introduce any auxiliary definition absent from Role A in order to produce agreement. Any mapping requiring one is `FORCED RECONSTRUCTION`.
- Do not apply the withdrawn seven-dimension rubric, or any project-supplied comparison criterion, where Role A supplied one or declined to supply one.
- Do not classify the outcome. That is Role C's function.
- Do not discard failed mappings. Preserve each with its reason.
- Do not feed anything from this packet back to Role A, in this run or any later one. A respondent who has seen it is permanently at contamination level `C4` for this programme.

---

## 5. Post-reveal corrections

If Role A offers corrections after reveal, they are recorded as a separate artifact with its own hash and the label `post_reveal_correction`. They do not overwrite the frozen pre-reveal answer and do not count as independent evidence.
