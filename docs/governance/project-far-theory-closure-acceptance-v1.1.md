# Project FAR Core Theory v1.1 — Correction Acceptance and Promotion Record

Status: **Accepted governance authority upon merge**

Date: 2026-08-27

Theory identity: `PROJECT-FAR-CORE-THEORY-1.1`

Corrected successor: [Project FAR Core Theory v1.1](../../theory/theorems/Project-FAR-Theory-Closure-v1.1.md)

Machine ledger: [project-far-core-theory-v1.1.json](../../theory/terminal/project-far-core-theory-v1.1.json)

## Trigger

A hostile W1 audit identified reproducible defects satisfying the v1.0 reopening rule. The audit was not independent under the project's evaluator-independence standard, so it supplies internal counterevidence and correction obligations but no assurance upgrade.

## Preservation

The original v1.0 monograph remains immutable at SHA-256 `b7cbd28d54686da33773a66edf9af9480044ffaabfeb83cfa4bfc1a12fe862a5`. Its machine ledger and acceptance record remain historical evidence. No v1.0 byte is rewritten.

## Governed reopening

Only the following surfaces are substantively reopened:

1. `FAR-CORE-004` wording/scope, because the v1.0 machine wording could be read as denying universal sufficiency even though the identity representation is sufficient for every contract on fixed `X`.
2. `FAR-CORE-010` dependency statement, because `Γ` was incorrectly listed as a direct determinant of `T_{L,J,I}` while absent from its definition.
3. The Blackwell prior-art characterization, because the v1.0 wording understated the classical decision-problem-uniform Blackwell partial order.

`FAR-CORE-014` remains `SUPPORTED/DERIVED`. No other core claim is reopened. The terminal verdict and surviving terminal kernel are unchanged.

## Accepted corrections

### FAR-CORE-004

Accepted wording:

> On every nontrivial domain, no single representation is simultaneously a least-informative sufficient representation for every observation contract.

The identity representation may be sufficient for all contracts; it is not least-informative for nondiscriminating contracts. The negative theorem is about simultaneous minimality, not existence of a universally sufficient encoding.

### FAR-CORE-010

Accepted dependency split:

- exact common theory `T_{L,J,I}=∩_i Th_L(M_i)` depends directly on `L`, the interpretation profiles/models `J`, and target class/index `I`;
- frame-subtracted residue `R_{L,J,I,Γ}=T_{L,J,I}\Cn_L(Γ)` additionally depends on `Γ`;
- changing `Γ` while holding `L,J,I,M_i` fixed cannot change `T` itself.

### Prior art

Blackwell's classical comparison of experiments is recognized as stronger prior art than v1.0's wording implied: under the standard setup, dominance over all decision problems is equivalent to a garbling relation. Project FAR makes no novelty claim for that mathematical pattern.

## Regression requirement

`theory/evaluation/project-far-core-theory-v1.1-regressions.json` is permanent regression evidence. Validation must fail if:

- the identity countermodel is again interpreted as refuting universal sufficiency rather than universal minimality; or
- `Γ` is again treated as an independent index of exact `T_{L,J,I}` while `L,J,I,M_i` remain fixed.

## Assurance

Current assurance remains: **internal deductive; corrected after non-independent hostile audit; not independently reviewed**.

`PCA-W1-INDEPENDENT-REVIEW` remains open and is the next assurance workstream. Any future reviewer must review v1.1 while retaining access to v1.0 and this correction record.

## Promotion

Upon merge:

- `PROJECT-FAR-CORE-THEORY-1.1` becomes current core authority;
- `PROJECT-FAR-CORE-THEORY-1.0` remains preserved historical authority at its original evidence cutoff;
- current status, claim, theorem, planning, and repository-truth surfaces must point to v1.1;
- post-closure program `POST-CLOSURE-001` remains active and W1 remains open;
- no software conformance or CI result is treated as mathematical proof.
