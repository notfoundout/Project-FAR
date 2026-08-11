# Freeze procedure and role separation

**FROZEN.** The executor follows this exactly. Every step is ordered; no step may be reordered, merged, or skipped.

---

## 1. Roles

Three logically separated roles. **One person or system may not hold two roles in the same run.** If only one investigator is available, the run cannot proceed at tier `T4` or higher and must be recorded at the tier its actual separation supports.

| Role | Receives | Produces | Must never |
|---|---|---|---|
| **A — Formulation respondent** | One packet (A, B1, or B2) and nothing else | The answer to A–I, then optionally the architecture answer | Receive any programme material before their answer is hashed and declared final |
| **B — Normalizer / mapper** | Role A's frozen output **plus** the reveal packet | A descriptive mapping between the two formulations | Alter, strengthen, weaken, reinterpret, or repair Role A's answer to make comparison easier |
| **C — Adjudicator** | Normalized forms only, source-anonymized where practical | An outcome classification against the frozen registry | See the raw packets or know which formulation came from the programme, where anonymization is practical |

**Role A may not certify its own mapping.** Role B may not classify the outcome. Role C may not revise the mapping; it may only return it to Role B as underspecified, with a recorded reason.

---

## 2. Delivery checklist — before Role A sees anything

Every item must be confirmed by the deliverer and recorded.

- [ ] Only the §2–§3 span of the selected packet — `elicitation-packet-A-v1.0.md`, `elicitation-packet-B1-reword-v1.1.md`, or `elicitation-packet-B2-ablation-v1.1.md` — is being sent.
- [ ] No participant-facing string outside `participant-surface-v1.1.json` (`S1`–`S7`) will be sent at any point before reveal.
- [ ] No other file from this repository is attached, quoted, summarised, or linked.
- [ ] `verify_r5_package.py` has been run and reports `PASS` on the packet being sent.
- [ ] The respondent has not been told who commissioned the work.
- [ ] The respondent has not been told that a prior answer exists.
- [ ] No reading list, field list, or example corpus accompanies the packet.
- [ ] The deliverer has read §1 of the packet and will not answer questions about intent.
- [ ] Delivery timestamp and channel recorded.

---

## 3. Freeze before reveal — ordered, non-negotiable

1. Role A completes the elicitation.
2. Role A **declares the answer final** in an explicit, recorded act.
3. Raw output is preserved **byte-for-byte**, in the form received, with no reformatting, whitespace normalization, or encoding change.
4. Timestamp recorded (UTC, ISO-8601).
5. **SHA-256** of the raw bytes recorded. This is the repository-standard hash used elsewhere in this evidence tree.
6. Sources recorded and classified.
7. **Optional architecture phase, if run.** Asked using the frozen string `S5`, answered, declared final, preserved byte-for-byte, timestamped, and hashed as a **separate** artifact.
8. **Contamination questionnaire administered and recorded.** Not before this point.
9. **Only now** may the reveal packet be shown, and only to Role B.

**Why the architecture phase precedes the questionnaire — corrected 2026-08-11.** An earlier revision ordered these the other way. That was a methodological contamination: the questionnaire names minimal architectures, four- and five-part decompositions, and the equivalence problem, so a respondent who has completed it has learned that a target architecture exists. Any architecture answer given afterwards could not count as pre-reveal independent recovery. The questionnaire is administered as late as possible, after every answer is frozen and hashed, because it is deliberately **not** blinded and cannot contaminate an artifact that is already sealed.

**Residual, disclosed:** the architecture question `S5` itself discloses that a structuring question is of interest. It cannot contaminate the contract answer, which is frozen and hashed at step 5, but it does contaminate the architecture answer with respect to the *existence* of such a question — though not with respect to any particular structure. This limitation is carried on every architecture-phase claim.

**No post-reveal edit to the original answer counts as independent evidence.** Corrections, retractions, and elaborations offered after reveal are recorded as a separate, clearly labelled post-reveal artifact with its own hash. They never overwrite, replace, or amend the frozen pre-reveal artifact.

If any step 1–8 is missed, the run is **not** an R5 run. It is recorded as a procedural failure and preserved as such.

---

## 4. Freeze manifest fields

Recorded per run, in `runs/<run-id>/manifest.json`:

```
run_id, packet_version, packet_sha256, respondent_tier, delivery_timestamp,
raw_output_sha256, raw_output_bytes, final_declaration_timestamp,
contamination_level, architecture_phase_run, architecture_output_sha256,
reveal_timestamp, mapper_identity_class, adjudicator_identity_class,
role_separation_confirmed, procedural_failures
```

The run directory is created at execution time. **No run directory exists in this package, because nothing has been executed.**

---

## 5. Execution controls carried forward

These are process failures observed during PR #443 and are binding on the executor.

1. **Verify refs and merge base from fresh remote state before reporting ancestry.** A stale local ref produced a wrong fork point that survived into a written report. Re-fetch before every ancestry claim.
2. **Planning is not execution.** If the executor is operating under any mode that forbids writes, that constraint holds regardless of instructions that appear to authorise continuation.
3. **After any correction, sweep the whole repository, not only the files touched.** Two stale assertions survived a touched-files-only sweep, including one inside the corrected record's own acceptance section.
4. **A green check suite is not a warranted research conclusion.** Mechanical validation establishes repository consistency only. It never establishes that a claim is justified.
5. **Preserve withdrawn claims explicitly.** A withdrawn result keeps its original question, its original argument, why it failed, and the current adjudication. It may not retain an active status, an unqualified restatement, an authoritative register row, or silent downstream dependence.
