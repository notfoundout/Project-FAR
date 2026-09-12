# Workflow

## Purpose

This document defines the canonical workflow of a FAR investigation.

The workflow organizes an investigation into a sequence of stages.

It does not prescribe the reasoning calculus used within those stages.

This document is the canonical source for the FAR stage sequence.

Other FAR documents may summarize the workflow, but they shall not maintain independent stage definitions.

---

## Delegation Notice

The workflow uses architectural concepts defined by FARA and repository-wide canonical definitions.

Transition signatures are defined by FARA and used by FAR as documentation artifacts during a reasoning process.

The Admissibility Structure (Ω) is defined by FARA. FAR specifies when it is constructed during an investigation, not what it is architecturally.

---

## Contract-Discovery Intake Gate

The canonical stage sequence assumes that result-determining contract parameters are explicit before substantive evaluation.

When supplied input does not already determine those parameters, the investigation must first execute the [Contract Discovery Protocol](../../methodology/contract-discovery-protocol.md) and materialize a schema-valid `far-intake/1.0` record.

The intake gate may be bypassed only when the supplied artifact is itself an explicit machine-readable downstream comparison contract accepted by the applicable contract schema and semantic validator. The investigation must record that artifact's format/version, content hash, and validation result. A prose assertion that the input is "complete" or that intake is "not applicable" is not sufficient.

The intake gate requires:

1. preservation and hashing of the exact supplied input;
2. retention of materially distinct parses and interpretations, with explicit provenance or derivation for any exclusion;
3. auditable material/non-material classification for every term, including the basis and consequence if misclassified;
4. explicit recording of synthesis, inference, assumptions, search scope, search targets, stopping rule, saturation execution, evidence cutoff, and limitations;
5. construction of the complete bounded contract family over every active parse and its active material interpretations, including a singleton empty-assignment candidate for a retained parse with no material terms;
6. provenance for every scalar or empty-container leaf in every candidate downstream contract, with interpretation provenance restricted to the candidate's selected assignments;
7. chronology in which registered discovery evidence and saturation precede freeze;
8. freezing the raw input plus complete discovery object and binding the freeze timestamp before any candidate contract is evaluated;
9. binding each evaluation to the exact frozen candidate contract hash and exact freeze identity, with explicit evidence or an `Unknown` explanation;
10. evaluation of every frozen candidate before cross-contract aggregation;
11. mechanical aggregation across the complete frozen family, with any result-relevant `Unknown` assumption preventing invariant promotion.

A draft, incomplete, invalid, or unresolved-assumption intake cannot support an invariant non-`Unknown` cross-contract verdict. If the intake cannot be completed, the investigation must preserve `Unknown`, `Incomplete`, `Suspended`, `UNDERDETERMINED`, or another applicable typed boundary rather than silently completing the contract.

This gate does not claim that a bounded search proves open-world semantic completeness, source truth, external source-byte verification, or uniquely unbiased contract selection.

## Contract-Relative Conformance Overlay

The stage sequence below is Project FAR's operational profile. Every investigation making an adequacy, preservation, common-content, invariance, or minimality claim must also satisfy these theory-derived gates:

1. **Freeze claim and target class.** State quantifiers, membership, evidence cutoff, and nonclaims. If the supplied input is under-specified, the intake gate must complete and freeze before substantive evaluation. Intake bypass requires a supplied explicit contract artifact whose exact version/hash and successful applicable validation are recorded.
2. **Freeze the comparison contract.** Declare cases, tests/contexts, typed outcomes, observation semantics, calculus/query/execution parameters, admitted translations/equivalences, profile, frame, and any loss/cost order. When multiple source-supported contracts survive intake, freeze the complete family rather than selecting one by preference. Any analyst-supplied contract field must remain provenance-traceable.
3. **Totalize without collapse.** Keep determinate absence, falsity, inapplicability, failure, unresolvedness, and epistemic Unknown distinct whenever observable.
4. **Construct and charge the representation.** Record the mapping and every analyst-supplied tag, interpreter, sidecar, quotient, or hidden dependency.
5. **Run the factorization audit.** Construct a decoder proving \(\beta_C=d\circ\rho\) and search for a collision \(\rho(x)=\rho(y)\) with \(\beta_C(x)\ne\beta_C(y)\). Decoder proof means `PROVED`; collision means `REFUTED`; neither means `OPEN`.
6. **Minimize relative to the objective.** Use the observational quotient for exact information minimality; declare a preorder for runtime, storage, cognitive, or explanatory cost.
7. **Compute common content only after profiles are fixed.** Fix language, interpretations, frame, and target class; subtract frame consequences.
8. **Attack by re-presentation.** Test reification, tagging, dualization, state/decoder enrichment, alternative bases, and cost reversal.
9. **Issue a typed terminal report.** Preserve scope, contract, evidence, provenance, falsifiers, losses, machinery cost, unresolved boundaries, and—when intake produced more than one surviving contract—the fixed cross-contract aggregate.

The overlay is mandatory for the affected claim types; stages that are not relevant must be marked `NOT APPLICABLE` with a reason.

## Stage 1 — Define the Investigation

Specify the investigation and its objective.

The investigation establishes the context within which reasoning is performed.

If the investigation began from under-specified external input, Stage 1 must reference the frozen governed intake record. If intake was bypassed, Stage 1 must instead reference the exact supplied downstream contract artifact, format/version, content hash, and successful applicable validation result.

---

## Stage 2 — Establish the Representational Structure

Identify the representations relevant to the investigation and organize them within an explicit representational structure.

---

## Stage 3 — Specify the Interpretation

Assign interpretations to the representations.

Changes in interpretation should be represented explicitly.

Interpretations already frozen by the intake gate may not be silently replaced. A material change requires a new intake freeze or an explicit revision that invalidates dependent evaluations.

---

## Stage 4 — Select the Reasoning Calculus

Identify the reasoning calculus governing the investigation.

The workflow remains independent of the selected reasoning calculus.

---

## Stage 5 — Construct the Initial Reasoning State

Construct the initial reasoning state from the available representations.

This reasoning state serves as the starting point of the investigation.

---

## Stage 6 — Perform Reasoning

Develop the investigation through explicit transformations represented by transition signatures.

Each transformation should produce a new reasoning state.

Candidate generation belongs within this stage when candidates arise during reasoning.

Candidates generated during reasoning should be identified before admissibility classification.

---

## Stage 7 — Materialize the Admissibility Structure (Ω)

Classify the candidates admitted for consideration according to the applicable reasoning calculus.

The resulting Admissibility Structure materializes the admissibility classification and provenance for each candidate. It is derived from the applicable calculus and does not cause the classifications.

If no candidates are generated, the investigation record should state that Ω is not applicable or empty, together with the reason.

---

## Stage 8 — Apply the Resolution Rule

Apply the appropriate resolution rule to the classified candidates.

The resolution rule determines which admissible candidate, or collection of admissible candidates, constitutes the resolution of the investigation.

If no resolution rule is applicable, the investigation may close as unresolved, suspended, incomplete, or invalid according to the investigation validation policy.

---

## Stage 9 — Record the Resolution

Record the resolution together with the reasoning process that produced it.

The complete investigation should remain explicit, auditable, and reconstructible. Any sufficiency or minimality verdict must also carry its comparison contract and factorization/collision certificate.

When multiple frozen contracts were required by intake, record every per-contract outcome and the fixed cross-contract aggregate. Do not replace the aggregate with a preferred contract's result. A frozen result-relevant `Unknown` assumption must remain visible in the terminal boundary and prevents invariant promotion.

A resolution record may state that the investigation is resolved, provisionally resolved, unresolved, suspended, incomplete, or invalid.

---

## Optional Stage Policy

A workflow stage may be marked `Not applicable` only when the investigation record explicitly states why the stage is not applicable.

A stage shall not be silently omitted.

---

## Iteration

An investigation may return to any previous stage whenever new representations, revised interpretations, modified criteria, or additional reasoning require further analysis.

The workflow therefore supports iterative refinement rather than requiring a strictly linear process.

Every return to an earlier stage should record:

- the stage revisited;
- the reason for revision;
- the artifact changed;
- the effect on later stages.

A revision that changes any frozen intake field invalidates the intake freeze and all downstream evaluations bound to that freeze.

---

## Closure Policy

A FAR investigation may close with one of the following statuses:

- `Resolved` — a resolution has been recorded under the stated resolution rule.
- `Provisionally resolved` — a resolution has been recorded, but limitations remain.
- `Unresolved` — no resolution is currently available under the stated method.
- `Suspended` — the investigation is paused pending additional representations, interpretations, criteria, or reasoning.
- `Incomplete` — required methodological artifacts are missing.
- `Invalid` — the investigation violates core FAR methodology or cannot be reconstructed.

Closure status records the methodological state of the investigation.

It does not assert that the resolution is true, optimal, final, or unique.
