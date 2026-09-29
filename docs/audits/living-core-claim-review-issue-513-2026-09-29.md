# Living core-claim review — issue #513 — 2026-09-29

Status: **Governed internal literature review — no FAR-CORE or EFR status change**

Issue: #513 (`Living repository: core-claim review queue`)

Reviewed source snapshot: permanent living-research inbox PR #490, head `6f07cb9d2dd8df2ec98962829190ae2a0946d709`.

This is the successor review to `docs/audits/living-core-claim-review-issue-513-2026-09-20.md`. The earlier review froze seven candidates at PR #490 head `2a2610f98c749e2836d23028f8e1aa8e2707f6e5`; those rows are already preserved in `research/living/review-dispositions-v1.0.json`. This review is limited to the four currently unreviewed candidates listed in issue #513 at the snapshot above.

## Governing question and contradiction threshold

The queue is controlled by `FAR-RQ-009`:

> After the completed independent W1 review, does any later evidence produce a reproducible contradiction to an exact FAR-CORE premise, proof step, or theorem?

The contradiction threshold is exact-premise matching, not keyword, title, or domain resemblance. A qualifying challenge must supply a minimized reproducible witness satisfying the exact canonical premises and negating the exact conclusion.

The canonical comparison target remains `PROJECT-FAR-CORE-THEORY-1.1`. The operative attack conditions are unchanged from the prior governed review:

- `FAR-CORE-001`: require an exact fixed-contract representation that is sufficient while required behavior does not factor through it;
- `FAR-CORE-002`: require an exact representation strictly less informative than the fixed-contract observational quotient, or a non-isomorphic competing least element under the same contract;
- `FAR-CORE-003`: require the declared action/test-closure premises together with a failure of action compatibility;
- `FAR-CORE-004`: require one representation proved least-informative sufficient across every varying observation contract on the governed nontrivial domain;
- `FAR-CORE-005`–`014`: require a witness satisfying the exact registered premises of the attacked claim and negating the exact conclusion.

## Primary-source verification and dispositions

### `FAR-LIT-888AC6B78B1CA0D9`

Source: Frank Vega, *The First Hypothetical Counterexample of Robin's Criterion*, Preprints.org version 5, DOI `10.20944/preprints202409.1972.v5`, posted 2026-09-23.

Primary source checked: Preprints.org version 5.

Source result: the paper concerns Robin's criterion for the Riemann Hypothesis. It treats a hypothetical least counterexample to Robin's inequality, uses properties of superabundant numbers and explicit prime-product bounds, and claims that the hypothetical counterexample cannot exist, yielding the paper's claimed proof of the Riemann Hypothesis. Its `counterexample` language is entirely about a number-theoretic inequality equivalent to RH.

Adversarial FAR reconstruction: the source supplies no FAR observation contract, representation/decoder pair, behavior-factorization relation, observational quotient, action/test closure, `Unknown` semantics, FARA operator-eliminability argument, or bounded Search-State witness. There is no premise-preserving map from the paper's hypothetical integer violating Robin's inequality to a witness satisfying any FAR-CORE premise while negating its conclusion.

Disposition: `IRRELEVANT_FALSE_POSITIVE`.

### `FAR-LIT-CBA889C95AED3381`

Source: J. T. Lewis, C.-E. Pfister, and W. G. Sullivan, *The equivalence of ensembles for lattice systems: Some examples and a counterexample*, *Journal of Statistical Physics* 77 (1994), DOI `10.1007/BF02186849`.

Primary/publication record and author-available full-text metadata checked.

Source result: the paper studies equivalence of microcanonical and grand-canonical ensembles for classical lattice systems at the level of states. It relates vanishing specific information gain to equivalence of ensembles, derives a thermodynamic criterion, shows it in a paramagnet and Ising model, and gives a failure/counterexample in the Curie-Weiss mean-field model.

Adversarial FAR reconstruction: `equivalence` here is a statistical-mechanical relation between sequences of equilibrium ensembles/measures, and the counterexample concerns failure of the paper's ensemble-equivalence criterion/model behavior. It is not the fixed-contract behavioral observational-equivalence relation used by FAR. The source does not provide an exact FAR representation smaller than the canonical quotient, a sufficiency-without-factorization witness, a failure of action compatibility under FAR's closure premises, or a universal least representation across varying FAR observation contracts.

Disposition: `IRRELEVANT_FALSE_POSITIVE`.

### `FAR-LIT-DD283139285EDBA1`

Source: Voin Milevski, *What Would an Empirical Counterexample to Motivational Internalism Require?*, SSRN 7481718, DOI `10.2139/ssrn.7481718`.

Source identity checked against the current Crossref/SSRN record; the paper's full text was not available through the public retrieval path used in this review. The source identity is nevertheless sufficient for the bounded premise-mismatch adjudication below: its declared object is motivational internalism in moral psychology/metaethics. This review does not claim an exhaustive inventory of uninspected full-text arguments.

Source context: Milevski's published work on motivational internalism defines the target family in terms of relations between sincere moral or best-option judgments and motivation, including proposed counterexamples involving amoralism or practical irrationality.

Adversarial FAR reconstruction: a putative empirical counterexample to motivational internalism concerns whether an agent can satisfy the relevant moral-judgment conditions while lacking the motivation that an internalist thesis says must accompany them. That is not a FAR fixed observation contract, representation, decoder, quotient, action/test-closure relation, parameter-omission theorem, `Unknown` result, FARA operator claim, or Search-State Sufficiency result. No inspected source material supplies a witness satisfying any FAR-CORE premise while negating its conclusion.

Disposition: `IRRELEVANT_FALSE_POSITIVE`.

### `FAR-LIT-E16D393262C91DAA`

Source: Edward Meyman, *On the Impossibility of Observability-Based Authorization: A Formal Impossibility Result for Ex-Ante AI Governance*, SSRN 6605120 / Zenodo `10.5281/zenodo.19647542`, posted 2026-04-29 and revised 2026-06-22.

Primary source checked: SSRN paper record and author-posted full-text record.

Source result: under an ex-ante authorization regime requiring a consequential action to be authorized before execution by a decision reproducible and independently verifiable from policy, context, and the proposed action specification, the paper argues that an observability architecture cannot itself produce the required authorization artifact. The argument is organized around causal posteriority of observability signals, failure of independent verification for artifacts derived from observational characterization, and failure of compositions of observational outputs to escape those constraints. The paper uses `observability` in the AI-governance/monitoring sense and contrasts it with a separate pre-execution authorization boundary.

Adversarial FAR reconstruction: this is genuinely adjacent to FAR's broader interest in verifiable reasoning artifacts, but its central objects and theorem are different from FAR's fixed-contract representation theory. Meyman's `observability architecture` is a class of monitoring/governance mechanisms, not FAR's observational-equivalence quotient of a state domain under an exact contract. The impossibility result does not exhibit a FAR representation that is sufficient without factorization, a representation strictly less informative than FAR's fixed-contract quotient while preserving the same exact contract, a failure of FAR action compatibility under its closure premises, or one least representation valid across every varying observation contract. Nor does it address the bounded PR #453 Search-State Sufficiency representation/decoder classes.

The result is therefore relevant adjacent prior art/context for observability-versus-authorization and independently reconstructible governance artifacts, but not a countermodel to `PROJECT-FAR-CORE-THEORY-1.1`.

Disposition: `ADJACENT_NO_CONTRADICTION`.

## Claim-by-claim attack result

No candidate in this four-item snapshot supplies the minimum witness needed to reopen a FAR-CORE claim:

- `FAR-CORE-001`: no exact-sufficiency/non-factorization witness.
- `FAR-CORE-002`: no exact representation strictly less informative than the fixed-contract observational quotient, and no non-isomorphic competing least element under the same contract.
- `FAR-CORE-003`: no declared action/test-closed observational relation that fails compatibility.
- `FAR-CORE-004`: no single representation proved least-informative sufficient across every varying observation contract on the governed nontrivial domain.
- `FAR-CORE-005`–`010`: no counterexample to the stated invariance, encoding, vocabulary/operator-count, finite-panel, or indexed-common-theory statements.
- `FAR-CORE-011`: no representation shown exact after omitting a parameter that changes required consequences.
- `FAR-CORE-012`: no contradiction involving determinate absence versus `Unknown`.
- `FAR-CORE-013`: no argument that canonical FARA `Ω` is semantically non-eliminable.
- `FAR-CORE-014`: no result about the bounded PR #453 Search-State Sufficiency representation/decoder classes.

## Replication and adjudication

The four dispositions were independently re-run as a second internal premise-matching pass after the first source reconstruction. The second pass did not use discovery keywords as evidence. It attempted the strongest available mapping from each source result into the exact FAR witness tests above and required the mapping to preserve the source's actual premises rather than replacing them with FAR premises by analogy.

| Candidate | Replicated premise-match result | Adjudication |
|---|---|---|
| `FAR-LIT-888AC6B78B1CA0D9` | No FAR-CORE witness; Robin counterexample is an analytic-number-theory integer violating Robin's inequality. | `IRRELEVANT_FALSE_POSITIVE` |
| `FAR-LIT-CBA889C95AED3381` | No FAR-CORE witness; equivalence/counterexample concerns statistical-mechanical ensembles and specific information gain. | `IRRELEVANT_FALSE_POSITIVE` |
| `FAR-LIT-DD283139285EDBA1` | No FAR-CORE witness; target is motivational internalism in metaethics/moral psychology. | `IRRELEVANT_FALSE_POSITIVE` |
| `FAR-LIT-E16D393262C91DAA` | No FAR-CORE witness; theorem concerns monitoring/observability architectures versus ex-ante authorization artifacts, not fixed-contract observational-quotient minimality. | `ADJACENT_NO_CONTRADICTION` |

Adjudication result: the second pass reproduces all four first-pass dispositions and finds zero surviving exact-claim contradiction witnesses.

## Smallest governed correction analysis

No FAR-CORE correction is warranted.

The three irrelevant candidates demonstrate the expected cost of a deliberately high-recall literature lane: generic `counterexample`/`equivalence` vocabulary can admit unrelated domains. The existing review-disposition registry is specifically designed to preserve raw discovery while suppressing reviewed false positives from the active core-claim queue. Tightening the search solely to remove these three records would risk suppressing genuine cross-domain threats and is not justified by this snapshot alone.

`FAR-LIT-E16D393262C91DAA` should be preserved as adjacent research context, not promoted to `N1_PRIOR_ART_LEAD`: the reviewed theorem does not teach the fixed-contract least-informative quotient, the four-element registered EFR-N1 anticipation target, or another result close enough to warrant an N1 novelty disposition on this evidence alone.

Accordingly the smallest governed action is only to append these four review dispositions to `research/living/review-dispositions-v1.0.json`, preserving raw candidate records and suppressing repeated metadata-only review.

## Final disposition set

| Candidate | Disposition |
|---|---|
| `FAR-LIT-888AC6B78B1CA0D9` | `IRRELEVANT_FALSE_POSITIVE` |
| `FAR-LIT-CBA889C95AED3381` | `IRRELEVANT_FALSE_POSITIVE` |
| `FAR-LIT-DD283139285EDBA1` | `IRRELEVANT_FALSE_POSITIVE` |
| `FAR-LIT-E16D393262C91DAA` | `ADJACENT_NO_CONTRADICTION` |

## Claim/status impact

None. This review does not reopen or alter any FAR-CORE claim, premise, proof, theorem, W1-W6 result, EFR gate, novelty status, external-validity status, independence status, or commercial-readiness status. The review is internally authored and does not execute or substitute for EFR-R1, EFR-R2, or EFR-N1.
