# FAR Phase 3 — Methodology Audit

## Status

Initial methodology audit complete.

---

## Scope

This audit reviews whether FAR's methodology functions coherently after Phase 1 canonical cleanup and Phase 2 structural completion.

Reviewed files:

- `frameworks/FAR/workflow.md`
- `frameworks/FAR/methodology.md`
- `frameworks/FAR/application.md`
- `frameworks/FAR/example-standard.md`
- `frameworks/FAR/investigation-validation.md`
- `frameworks/FAR/design-principles.md`
- `frameworks/FAR/dependency-graph.md`
- `frameworks/FAR/faro-boundary.md`
- `frameworks/FAR/FAR-v1.0-criteria.md`

This audit asks:

1. Is every workflow stage necessary?
2. Does every workflow stage have a single responsibility?
3. Can any stage be merged or removed without loss of methodological power?
4. Does FAR remain neutral with respect to logic, mathematics, epistemology, and domain?
5. Are required artifacts sufficiently specified for independent execution?
6. Are iteration and revision handled consistently?
7. Are termination and validation sufficiently defined?
8. Does the methodology satisfy its own stated principles?
9. Are edge cases adequately handled?
10. Is FAR ready for Phase 4 consistency audit?

---

## Methodological Verdict

FAR's methodology is coherent, general, and mostly implementable.

It should proceed toward Phase 4 after correcting several methodology-level gaps.

The current methodology is not yet ready for FAR v1.0 Stable because termination conditions, optional-stage handling, edge-case behavior, and reproducibility standards need sharper specification.

---

## Finding 1 — The nine-stage workflow is methodologically coherent

The workflow currently contains nine stages:

1. define the investigation;
2. establish the representational structure;
3. specify the interpretation;
4. select the reasoning calculus;
5. construct the initial reasoning state;
6. perform reasoning;
7. construct Ω;
8. apply the resolution rule;
9. record the resolution.

Assessment: pass.

The sequence is coherent because each stage performs a distinct methodological function.

No stage is obviously redundant.

---

## Finding 2 — Each stage has a mostly distinct responsibility

The current single-responsibility analysis is:

| Stage | Responsibility | Assessment |
|---|---|---|
| Stage 1 | Establish investigation objective and context | Pass |
| Stage 2 | Establish representation inventory and relations | Pass |
| Stage 3 | Assign meaning through interpretation | Pass |
| Stage 4 | Identify governing rules or criteria | Pass |
| Stage 5 | Establish starting state | Pass |
| Stage 6 | Conduct reasoning and generate candidates | Pass with clarification |
| Stage 7 | Classify candidate admissibility through Ω | Pass |
| Stage 8 | Select by resolution rule | Pass |
| Stage 9 | Record final resolution and process | Pass |

Assessment: pass with minor clarification needed.

Stage 6 should explicitly state that candidate generation belongs there when candidates arise.

This is already recorded in the example standard and validation documents, but should also be reflected directly in `workflow.md`.

---

## Finding 3 — No workflow stage should be removed at this time

Potential removals were evaluated:

- removing Stage 3 would collapse representation with interpretation;
- removing Stage 4 would hide the governing calculus or criteria;
- removing Stage 5 would obscure the starting point of reasoning;
- removing Stage 7 would collapse candidate generation with candidate admissibility;
- removing Stage 8 would collapse admissibility with selection;
- removing Stage 9 would weaken auditability and reconstructibility.

Assessment: pass.

The stages should remain separate.

---

## Finding 4 — Candidate generation should remain inside Stage 6

Candidate generation is not a universal separate stage.

In many investigations, candidates arise iteratively during reasoning rather than in a single discrete step.

Assessment: pass.

The Phase 2 decision is methodologically sound.

Candidate generation should remain within Stage 6.

Stage 7 should classify admissibility for candidates produced by reasoning.

---

## Finding 5 — FAR remains reasoning-calculus neutral

FAR requires a reasoning calculus to be specified but does not prescribe which calculus must be used.

This preserves neutrality across formal, informal, mathematical, empirical, legal, historical, philosophical, and AI-assisted investigations.

Assessment: pass.

No current FAR document forces a particular logic, mathematics, epistemology, or domain-specific standard.

---

## Finding 6 — Required artifacts are mostly specified

The example standard and investigation validation documents specify the required artifacts for completed FAR investigations.

Required artifacts now include:

- investigation;
- representational structure;
- interpretation;
- reasoning calculus;
- initial reasoning state;
- reasoning trace or equivalent artifact;
- candidates where they arise;
- Ω when candidate admissibility is relevant;
- resolution rule;
- resolution;
- audit notes.

Assessment: pass with one gap.

The methodology still needs explicit handling for stages that are not applicable.

For example, an exploratory investigation may not have a final resolution, and a descriptive investigation may not require candidate admissibility classification.

Recommended addition:

Add an optional-stage policy explaining that a stage may be marked `Not applicable` only when the reason is explicitly recorded.

---

## Finding 7 — Iteration is acknowledged but underspecified

The workflow states that an investigation may return to earlier stages when new representations, revised interpretations, modified criteria, or additional reasoning require further analysis.

Assessment: partial pass.

Iteration is permitted, but the methodology does not yet specify how revisions are recorded.

Recommended addition:

Add a revision rule requiring that any return to an earlier stage record:

- the stage revisited;
- the reason for revision;
- the changed artifact;
- the effect on later stages.

Without this, auditability weakens in iterative investigations.

---

## Finding 8 — Termination conditions are insufficiently specified

The workflow ends with recording the resolution.

However, FAR does not yet specify when an investigation is allowed to terminate.

Assessment: gap.

Recommended addition:

Add an investigation closure policy distinguishing:

- resolved investigations;
- provisionally resolved investigations;
- unresolved investigations;
- suspended investigations;
- invalid or incomplete investigations.

This should not force every investigation to produce a final true conclusion.

It should only define how closure status is recorded.

---

## Finding 9 — Reproducibility is stated but not operationally specified

The methodology states that equivalent investigators following the same methodology should be capable of reproducing equivalent investigations.

Assessment: partial pass.

The idea is sound, but `equivalent investigators` and `equivalent investigations` are not operationally specified enough to function as validation standards.

Recommended correction:

Reframe reproducibility as artifact-based reconstructibility:

> A FAR investigation is reproducible to the extent that another investigator can reconstruct the reasoning process from the recorded artifacts under the stated interpretation and reasoning calculus.

This is cleaner and avoids unnecessary assumptions about investigator equivalence.

---

## Finding 10 — Edge cases need explicit methodological handling

The current methodology can probably handle edge cases, but not all are explicit.

Edge cases requiring explicit policy:

- no admissible candidates;
- multiple admissible candidates;
- changing interpretations;
- changing reasoning calculi;
- open-ended investigations;
- suspended investigations;
- investigations with incomplete records;
- investigations with conflicting resolutions.

Assessment: gap.

Recommended addition:

Add an edge-case policy to `investigation-validation.md` or a dedicated `edge-cases.md` file.

---

## Finding 11 — FAR does not drift into FARA, FARO, or FARE

The methodology delegates architectural concepts to FARA, preserves FARO as downstream, and does not require new FARE mathematics.

Assessment: pass.

No methodology document currently requires FARE expansion.

---

## Finding 12 — Methodology satisfies explicitness and auditability only if revision and closure policies are added

The explicitness and auditability principles are strong.

However, in iterative investigations, auditability requires explicit revision records.

In unresolved or open-ended investigations, auditability requires explicit closure status.

Assessment: partial pass.

The methodology is close, but still underspecified for complex investigations.

---

## Required Corrections Before Phase 3 Completion

1. Update `workflow.md` to state that candidate generation belongs in Stage 6 when candidates arise.
2. Add an optional-stage policy.
3. Add a revision-record rule for iteration.
4. Add an investigation closure policy.
5. Reframe reproducibility around artifact-based reconstructibility.
6. Add edge-case handling.
7. Update `investigation-validation.md` to include optional stages, revision records, closure status, and edge cases.
8. Update `example-standard.md` to include revision records and closure status.
9. Update `FAR-v1.0-criteria.md` to require these methodology policies before FAR v1.0 Stable.

---

## Recommendation

Open a focused FAR Phase 3 cleanup PR implementing the corrections above.

Do not begin FARO.

Do not modify FARE.

After the corrections are merged, proceed to Phase 4 — Consistency Audit.
