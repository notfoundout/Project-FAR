# AX-001 Wording Revision Report

## Executive Summary

This report records the canonical AX-001 wording revision authorized by the accepted prior AX-001 research reports. The revision retains Operation as the AX-001 candidate primitive and changes only the working characterization needed to remove or clarify operation-adjacent wording.

Final recommendation: **REVISED WORDING READY FOR STABILITY REVIEW**.

## Prior Evidence

This revision uses the following prior evidence:

- `docs/reports/foundation-validation-report.md`
- `docs/reports/ax001-circularity-investigation.md`
- `docs/reports/ax001-primitive-candidate-adjudication.md`
- `docs/reports/appendices/ax001-p1-raw.md`
- `docs/reports/appendices/ax001-c1-raw.md`

The prior evidence supports revision because it found material circularity pressure in the terms `executable act`, `performed`, and `act upon`; unresolved type/token ambiguity; unresolved temporal-versus-functional ambiguity; and insufficiency of bare Operation to supply normativity, semantics, validity, warrant, or the distinction between reasoning and arbitrary manipulation.

The prior evidence does not support replacing Operation. Transition, Rule-Licensed Transition, and Admissible Transition remain live rival candidates only as recorded in the prior adjudication report.

## Exact AX-001 Changes

The prior AX-001 working characterization stated:

```text
An operation is an executable act performed within a reasoning process.
```

The revised AX-001 working characterization states:

```text
Operation is the primitive unit-type for reasoning-relevant transformation, preservation, inspection, relation, constraint, or determination of reasoning conditions.

An operation-token is an instance of such a unit when it participates functionally in a reasoning process, rather than merely occurring during the same time interval.
```

The revision also adds the following clarifications to AX-001:

```text
Operation alone does not supply normativity, semantics, validity, or warrant.

Reasoning is distinguished from arbitrary manipulation by admissibility under reasoning-relevant constraints supplied by the surrounding theory, not by bare Operation alone.
```

AX-001 remains provisional and continues to state that the working characterization is not yet a formal definition.

## Rationale

The revised wording removes `executable act` and `performed` from the characterization because prior evidence showed that those terms belong to an operation-adjacent cluster and cannot serve as independent reducers.

The revised wording does not use `act upon`, avoiding the catch-all phrasing that prior evidence identified as overbroad and circularity-prone.

The revised wording distinguishes operation-types from operation-tokens. The type is the primitive unit-type; the token is an instance participating functionally in reasoning.

The revised wording distinguishes functional participation from mere temporal co-occurrence. An operation-token is not included merely because it happens during a reasoning episode.

The revised wording preserves Operation as the candidate primitive while recording the limits identified by prior evidence: Operation alone does not supply normativity, semantics, validity, or warrant, and bare Operation does not distinguish reasoning from arbitrary manipulation.

## What Was Not Changed

No downstream validation of L-001 through T-001 was performed.

No replacement primitive was introduced. Operation was not replaced by Transition, Rule-Licensed Transition, or Admissible Transition.

No unrelated axioms, lemmas, propositions, theorems, FARO documents, dashboards, automation, tooling, dependency analyzers, impact analyzers, knowledge graphs, GitHub Actions, release tooling, or repository architecture were modified.

The AX-001 status was not promoted. It remains Draft because this wording revision prepares AX-001 for stability review but does not itself complete that review.

## Remaining Open Questions

1. Whether the revised working characterization passes the AX-001 stability review.
2. Whether admissibility can be characterized without reducing it to Operation, rule application, or downstream calculus.
3. Whether reasoning states can be individuated independently enough to support Transition or Admissible Transition as future competitors.
4. Whether future evidence justifies promoting AX-001 beyond Draft.

## Recommendation

REVISED WORDING READY FOR STABILITY REVIEW
