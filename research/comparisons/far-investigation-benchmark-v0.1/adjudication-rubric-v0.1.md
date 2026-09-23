# FAR Investigation Benchmark — Blinded Adjudication Rubric v0.1

Status: PREPARED / must be frozen before output scoring

## Canonical M1 unitization

Condition packets are normalized and condition-blinded before unitization. M1 inferential-step boundaries are fixed before any support/evidence label is assigned.

Two independent blinded evaluators in the `unitizer` lane each mark material-inference boundaries and proposed immutable unit IDs. They receive no support/unsupported labels, reference-evidence recovery labels, condition identities, or one another's work. A distinct `unitization_adjudicator` resolves boundary disagreements while still blinded to condition identity and support labels. The resulting `canonical-unitization.jsonl` is locked before primary scoring.

Primary scorers receive the immutable canonical M1 unit IDs. They may not split, merge, add, delete, or renumber M1 units. Any defect discovered after canonical unitization is recorded as an integrity deviation; primary scoring does not silently rewrite the unitization.

A material inferential step is a conclusion whose removal or weakening could change the investigation's bottom-line resolution, confidence, causal explanation, or treatment of a material alternative.

A non-missing condition packet must yield at least one ratable material inferential step. If canonical unitization yields no ratable material inference for a packet, treat the case-condition packet as a scoring failure under the case-level missingness rule; do not define M1 as zero and do not divide by zero.

## Frozen packet-presentation schedule

Before S1, `adjudication-schedule.json` is generated from the frozen 60-case corpus, frozen `execution-schedule.json`, and the four independent packet evaluators: two `unitizer` evaluators and two `primary_scorer` evaluators. It is hash-bound in the campaign manifest.

For each of those four evaluators independently:

1. Sort the 60 final `case_id` values by lowercase hexadecimal `SHA256(UTF8("20260922|adjudication-case-order|" + evaluator_id + "|" + case_id))`, breaking a hash tie by ascending Unicode-code-point order of `case_id`. This is the evaluator's fixed base case order.
2. Number the base positions `j = 0..59`. Let `rotation = j mod 4` and let the condition vector be exactly `[F, B0, B1, B2]`.
3. Present four rounds. In round `r = 0..3`, traverse the same 60-case base order and present the run whose condition is `conditions[(r + rotation) mod 4]` for that case.
4. Concatenate the four rounds to obtain exactly 240 packet assignments with `presentation_index = 1..240`.

This construction gives every evaluator exactly 60 packets from each condition, exactly 15 packets from each condition in every 60-packet round, and places the four versions of any one case exactly 60 presentation positions apart. The validator must reproduce this schedule exactly; arbitrary reordering is invalid.

The artifact is exactly `{"status":"FROZEN","schedules":[...]}`. Each schedule has exactly `evaluator_id`, `lane`, and `packets`; it names one frozen `unitizer` or `primary_scorer`. Each packet has exactly `presentation_index`, `round`, `round_position`, `case_id`, `run_id`, `fresh_context`, `condition_label_visible`, `same_case_packet_visible`, and `other_evaluator_scores_visible`. Indices are one-based. `run_id` must equal the unique frozen execution-schedule run for the derived case-condition pair. The four isolation fields must respectively be `true`, `false`, `false`, and `false`; they are normative execution constraints, not descriptive metadata.

Each evaluator receives one normalized packet at a time in a fresh scoring context with no condition label, no other condition packet for the same case, and no access to another evaluator's scores. Packet presentation order may not be altered after any scoring output exists.

The `unitization_adjudicator` receives only locked unit-boundary disputes after both unitizers finish. The `scoring_adjudicator` receives only locked scoring disputes after both primary scorers finish. For either adjudicator, dispute IDs are sorted before the first adjudication by lowercase hexadecimal `SHA256(UTF8("20260922|adjudication-dispute-order|" + evaluator_id + "|" + dispute_id))`; the adjudicator receives one blinded dispute at a time and never receives prior-vote identities or condition identity.

## M1 unsupported inference

For every canonical material inference, assign one:

- SUPPORTED: cited evidence plus explicit assumptions warrants the conclusion at the stated strength;
- UNSUPPORTED: evidence/assumptions do not warrant the conclusion at the stated strength;
- NOT-RATABLE: required evidence is inaccessible or the normalized packet is corrupt.

An inference is UNSUPPORTED when any necessary bridge is hidden, contradicted, materially weaker than the conclusion, or dependent on an uncited factual premise.

M1 denominator = SUPPORTED + UNSUPPORTED material inferences.  
M1 numerator = UNSUPPORTED material inferences.  
NOT-RATABLE units never silently disappear; they trigger the missingness rule.

## M2 evidence coverage

The reference-evidence panel assigns stable IDs to valid material evidence items and freezes the denominator before any condition execution.

For each frozen reference item, primary scorers assign:

- RECOVERED-CORRECTLY-CONNECTED;
- RECOVERED-WRONG-CONNECTION;
- NOT-RECOVERED.

`REFERENCE-ITEM-INVALID` is not an output-scoring option. Reference-item inclusion, materiality, validity, and denominator membership are resolved by the reference panel before S1. A post-S1 defect is an integrity deviation, not a condition-specific denominator edit.

M2 denominator is the frozen positive set of valid reference items for that case and is identical across conditions.  
M2 numerator includes only RECOVERED-CORRECTLY-CONNECTED.

An item is RECOVERED-CORRECTLY-CONNECTED only when the condition identifies the same substantive evidence represented by the frozen item and visibly connects it to the proposition, inference, material alternative, or uncertainty boundary for which the item was frozen as material. Exact wording is unnecessary; proposition-level correspondence is required. A citation to the source elsewhere in the packet, an unsupported paraphrase, or a link to a different proposition is RECOVERED-WRONG-CONNECTION or NOT-RECOVERED as applicable.

## Critical error classes

Use exactly one primary class per material defect: C1 unsupported factual assertion; C2 citation/evidence mismatch; C3 omitted material counterevidence; C4 hidden assumption; C5 invalid/over-strength inference; C6 interpretation/claim substitution; C7 provenance failure; C8 unresolved contradiction presented as resolved; C9 uncertainty suppression; C10 materially incomplete alternative set; C11 unreplayable evidence/computation; C12 other with mandatory justification.

## Secondary metrics

Contradiction discovery, alternative-hypothesis coverage, assumption explicitness, source-to-claim correspondence, calibrated Unknown use, falsification-condition quality, provenance completeness, and replay completeness are scored only from frozen operational definitions. They cannot alter M1/M2.

## Blinding

Condition names, FAR field names, distinctive headers, filenames, and machine-readable schema labels are removed or mapped to neutral labels. Content is not rewritten merely to conceal substantive differences.

Immediately after scoring each packet and before condition identities are revealed, each primary scorer records exactly one condition guess: `F`, `B0`, `B1`, `B2`, or `UNKNOWN`. `UNKNOWN` counts as incorrect.

Blinding fails if either primary scorer correctly identifies F on at least 30 of the 60 F packets, or has exact four-way condition accuracy of at least 40% across all 240 packets. A blinding failure makes the confirmatory campaign `INDETERMINATE`; it is not merely descriptive.

## Raters, lanes, and disagreement

A frozen confirmatory campaign uses exactly six distinct evaluators with distinct IDs and identities:

- 2 × `unitizer`;
- 1 × `unitization_adjudicator`;
- 2 × `primary_scorer`;
- 1 × `scoring_adjudicator`.

All six must have substantive provider/affiliation, prior-exposure, conflict, and lane declarations. Project-authored adjudication is insufficient for this confirmatory external benchmark.

Two primary scorers independently score every packet from the canonical unitization. They may not see one another's scores. Any M1 label disagreement or M2 item disagreement goes to the `scoring_adjudicator`. The scoring adjudicator receives the blinded packet and disputed immutable unit/item, not the identities or prior votes of the first two scorers.

Raw unitizations and ratings are immutable. Canonical unitization and adjudicated ratings are stored separately with provenance.

## Missingness

A wholly missing condition output is assigned M1 = 1 and M2 = 0 for that case. A non-missing packet with no ratable canonical M1 unit is treated as a packet-level scoring failure, not as zero unsupported inference.

If packet corruption, inaccessible evidence, or a scoring failure prevents valid scoring for any condition, the affected case is non-ratable for that primary metric across all compared conditions; condition-specific deletion is forbidden. If more than 3 of 60 cases are non-ratable for either primary metric, the terminal benchmark status is INDETERMINATE. At 3 or fewer, use complete paired cases for that metric and run the frozen best/worst-case sensitivity analysis defined in `analysis-parameters-v0.1.json`.

Reaching a frozen resource ceiling is an observed condition outcome, not a missingness exclusion. Only a condition-blindly classified exogenous infrastructure/configuration failure that prevents the frozen condition from being executed as specified may make the four-condition case non-ratable.

The confirmatory SURVIVES disposition additionally requires the preregistered worst-case sensitivity result not to reverse either primary gate. If it does, the benchmark is INDETERMINATE rather than promoted from the complete-case analysis alone.

## Score lock and unblinding

Before condition identities are revealed, the campaign must hash-bind and lock `canonical-unitization.jsonl`, `ratings.raw.jsonl`, `ratings.adjudicated.jsonl`, `blinding-guesses.jsonl`, `score-lock.json`, and `metrics.csv`. `score-lock.json` records the exact hashes and a lock time no later than `unblinding_time`.

No scorer, unitizer, or adjudicator may receive condition identities before the score lock is complete.

## Prohibitions

Evaluators do not score writing quality, ideological agreement, preferred policy, persuasiveness, or whether they personally agree with the conclusion. They score evidence-to-claim and evidence-to-inference relations under this rubric.
