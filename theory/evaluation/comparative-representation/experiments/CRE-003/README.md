# CRE-003 — Independent Semantic, Investigative, and Calculus Variation Benchmark

## Status

Preregistered and frozen before candidate mapping or evaluation.

## Purpose

CRE-003 addresses the principal limitation identified by AVC-001 and GMA-001: CRE-001 permits several compact graph, state-transition, event-process, and categorical vocabularies to simulate the observable execution while leaving semantic and information preservation unresolved.

CRE-003 therefore uses matched cases that change one commitment while holding the others fixed. A candidate must represent the distinction itself, not merely reproduce one trace.

## Frozen matched cases

| Case | Changed commitment | Held constant | Required distinction |
|---|---|---|---|
| CRE-003-I | Interpretation | Representation, structure, investigation, calculus | Same syntax and inference pattern with different denotation and information content |
| CRE-003-G | Investigation | Representation, structure, interpretation, calculus | Same materials and rules with different objectives and success conditions |
| CRE-003-C | Reasoning calculus | Representation, structure, interpretation, investigation | Same objective with different admissibility rules and permitted conclusions |
| CRE-003-R | Representation and structure | Interpretation, investigation, calculus-level role | Different explicit organization carrying shared interpreted content |

The complete systems and equality constraints are frozen in `preregistration.json`.

## Evaluation design

Each candidate vocabulary receives three independently constructed mappings. No mapping may be discarded because it is inconvenient, divergent, or unfavorable.

Each mapping records:

- preservation vector `P=(p_s,p_m,p_o,p_d,p_i,p_h)`;
- `A_used` and `A_required`;
- derived machinery `D`;
- operations `O`;
- semantic description length `L`;
- hidden or commitment-equivalent reintroduction;
- a case-specific discrimination explanation.

The primary vocabulary result is the least favorable resolved preservation value per dimension, while `Unknown` remains unresolved rather than being mechanically ordered between `Partial` and `Fail`.

Existential sufficiency requires at least one of three mappings to pass all six dimensions on all four cases. Reproducible sufficiency requires all three mappings to do so.

## Candidate set

The first execution should reuse the ten frozen AVC-001 vocabularies without changing their primitive semantics. Any later candidate must be frozen before exposure to the case-specific mapping artifacts.

## Claim boundary

CRE-003 can test whether the frozen candidates preserve independent variation among the targeted commitments. It cannot establish:

- unrestricted primitive necessity;
- closure of the alternative-vocabulary search;
- global minimality;
- unique optimality;
- universal coverage of reasoning.

A favorable FAR result would establish only bounded comparative support on the frozen cases. A successful lower-cost candidate would falsify the corresponding bounded minimality claim and require GMA-001 to be revised.

## Execution status

No candidate mappings or scores are included in this PR. This separation is intentional: the benchmark and decision rules are frozen before evaluation.

## Artifacts

- `preregistration.json` — complete matched-case and decision-rule specification;
- `tests/test_cre003_preregistration.py` — deterministic freeze, orthogonality, and claim-boundary checks.
