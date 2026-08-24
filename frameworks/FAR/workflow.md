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

## Contract-Relative Conformance Overlay

The stage sequence below is Project FAR's operational profile. Every investigation making an adequacy, preservation, common-content, invariance, or minimality claim must also satisfy these theory-derived gates:

1. **Freeze claim and target class.** State quantifiers, membership, evidence cutoff, and nonclaims.
2. **Freeze the comparison contract.** Declare cases, tests/contexts, typed outcomes, observation semantics, calculus/query/execution parameters, admitted translations/equivalences, profile, frame, and any loss/cost order.
3. **Totalize without collapse.** Keep determinate absence, falsity, inapplicability, failure, unresolvedness, and epistemic Unknown distinct whenever observable.
4. **Construct and charge the representation.** Record the mapping and every analyst-supplied tag, interpreter, sidecar, quotient, or hidden dependency.
5. **Run the factorization audit.** Construct a decoder proving \(\beta_C=d\circ\rho\) and search for a collision \(\rho(x)=\rho(y)\) with \(\beta_C(x)\ne\beta_C(y)\). Decoder proof means \`PROVED\`; collision means \`REFUTED\`; neither means \`OPEN\`.
6. **Minimize relative to the objective.** Use the observational quotient for exact information minimality; declare a preorder for runtime, storage, cognitive, or explanatory cost.
7. **Compute common content only after profiles are fixed.** Fix language, interpretations, frame, and target class; subtract frame consequences.
8. **Attack by re-presentation.** Test reification, tagging, dualization, state/decoder enrichment, alternative bases, and cost reversal.
9. **Issue a typed terminal report.** Preserve scope, contract, evidence, provenance, falsifiers, losses, machinery cost, and unresolved boundaries.

The overlay is mandatory for the affected claim types; stages that are not relevant must be marked \`NOT APPLICABLE\` with a reason.

## Stage 1 — Define the Investigation

Specify the investigation and its objective.

The investigation establishes the context within which reasoning is performed.

---

## Stage 2 — Establish the Representational Structure

Identify the representations relevant to the investigation and organize them within an explicit representational structure.

---

## Stage 3 — Specify the Interpretation

Assign interpretations to the representations.

Changes in interpretation should be represented explicitly.

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
