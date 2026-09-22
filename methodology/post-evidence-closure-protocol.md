# FAR Post-Evidence Closure Protocol v1.0

Status: **Accepted internal methodology protocol when promoted by its governance record**

Identifier: `FAR-POST-EVIDENCE-CLOSURE-1.0`

## Purpose

This protocol prevents a decisive result about one frozen proposition from being mistaken for completion of the surrounding investigation.

FAR distinguishes two questions:

1. **Logical disposition:** what does the admitted evidence establish about the exact frozen proposition?
2. **Investigation closure:** has the bounded investigation completed the evidence, interpretation, and uncertainty checks required to stop?

A proposition may be proved, supported, falsified, left open, or otherwise dispositioned before the investigation is ready to close. Logical disposition is therefore necessary evidence for closure, not a substitute for closure.

## Bounded completeness only

This protocol never claims open-world or metaphysical completeness. Closure is relative to an explicit search frame, evidence cutoff, evidence classes, stopping rule, and terminal saturation pass.

A `Resolved` investigation means that the declared bounded closure obligations were satisfied. It does not mean that no undiscovered source, interpretation, counterexample, measurement defect, or future evidence exists.

## Closure contract

Before an investigation may close as `Resolved`, it must record all four closure dimensions below.

### 1. Logical disposition

Record the exact outcome for the frozen proposition and the evidence that licenses it. A decisive counterexample, proof, or other terminal atomic result may be recorded immediately.

Recording that result does not by itself close the investigation.

### 2. Evidence saturation

Freeze and execute a bounded search frame containing:

- scope;
- sources, corpora, databases, formal spaces, or other search locations;
- evidence cutoff;
- stopping rule.

Every investigation must then cover, or explicitly mark `NOT APPLICABLE` with a reason, these evidence classes:

1. direct or primary evidence bearing on the exact claim;
2. strongest opposing or disconfirming evidence;
3. measurement, classification, source-quality, or data-quality limitations;
4. denominator, base-rate, directness, and construct-alignment checks for empirical, statistical, causal, or comparative claims;
5. material alternative explanations or rival hypotheses;
6. narrower propositions that survive the atomic disposition;
7. residual uncertainty that remains after the result.

Coverage means the class was actually examined under the declared frame and has traceable evidence. A label such as `checked`, `complete`, or `none found` is not evidence that the search occurred.

### 3. Interpretive closure

Test materially plausible alternative formulations, interpretations, causal stories, comparison classes, or mechanisms that could change what the result means.

An atomic proposition can be false while a narrower proposition remains supported, or true while a broader interpretation remains unsupported. The terminal report must preserve those distinctions rather than collapsing them into the first decisive verdict.

### 4. Residual uncertainty and terminal saturation

Record surviving limitations, unresolved propositions, and uncertainty explicitly.

Then run a final pass over the declared search frame using the frozen stopping rule. Full `Resolved` closure requires that this terminal pass produce **zero new material findings**. If it produces a new material source, interpretation, alternative, limitation, or surviving proposition, incorporate the finding and repeat the closure analysis before attempting another terminal pass.

`Not found` remains bounded by the declared search frame. It does not become `does not exist` without a separate exhaustive or formal-completeness argument.

## Closure statuses

### `Resolved`

Use only when:

- the logical disposition is recorded with evidence;
- every mandatory evidence class is covered or justified as not applicable;
- the strongest opposition and material alternatives are recorded;
- measurement/data limitations and applicable denominator/directness/construct checks are recorded;
- surviving narrower propositions are recorded;
- residual uncertainty is recorded;
- interpretive closure is complete; and
- the terminal bounded saturation pass yields zero new material findings.

### `Provisionally resolved`

Use when the frozen proposition has a defensible disposition but one or more closure dimensions remain incomplete, constrained, or unsaturated.

The record must identify the unfinished dimension. A provisionally resolved investigation must not be represented as closure-complete and must not satisfy a machine `PASS` that requires full closure.

### Other statuses

`Unresolved`, `Suspended`, `Incomplete`, and `Invalid` retain their canonical meanings. They do not require fabrication of a closure contract that was never completed.

## Machine-readable execution boundary

For execution manifests governed after this protocol, `result: pass` requires a `closure` mapping with:

- `status: resolved`;
- `logical_disposition.outcome` plus repository evidence references;
- a populated `search_frame` with scope, search spaces, stopping rule, and evidence cutoff;
- all mandatory `evidence_classes`, each `covered` with evidence or `not_applicable` with a reason;
- finding inventories for strongest opposition, measurement/classification limits, alternatives, surviving narrower propositions, and residual uncertainty; empty inventories require a non-empty `none_found_basis`;
- `interpretive_closure.status: complete` plus evidence; and
- `terminal_saturation.status: complete`, `new_material_findings: 0`, plus evidence.

The validator rejects self-certifying labels that lack the required structural basis.

## Historical records

A pre-protocol historical PASS may remain valid at its historical scope without inventing closure evidence after the fact. Any compatibility exception must be pinned to the exact immutable historical bytes. Editing the record removes the exception and subjects the modified artifact to this protocol.

## Nonclaims

This protocol does not establish:

- open-world evidence completeness;
- factual correctness of admitted sources;
- independence or external replication;
- freedom from all hidden assumptions;
- a universal list of domain-specific evidence classes;
- that a zero-new terminal pass proves no future material evidence exists;
- novelty, priority, empirical utility, or commercial value.

It changes the stopping discipline of FAR investigations. It changes no FAR-CORE theorem or `far-ir/2.x` representation semantics.
