# CRE-003 — Independent Semantic, Investigative, and Calculus Variation Benchmark

## Status

Preregistered and frozen before candidate mapping or evaluation. The frozen benchmark has now received a bounded internal execution recorded separately from the preregistration.

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

The complete systems and equality constraints remain frozen in `preregistration.json`.

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

The first execution reused the ten frozen AVC-001 vocabularies without changing their primitive semantics. Any later candidate must be frozen before exposure to the case-specific mapping artifacts.

## Claim boundary

CRE-003 can test whether the frozen candidates preserve independent variation among the targeted commitments. It cannot establish:

- unrestricted primitive necessity;
- closure of the alternative-vocabulary search;
- global minimality;
- unique optimality;
- universal coverage of reasoning.

A favorable FAR result establishes only bounded comparative support on the frozen cases. A successful lower-cost candidate would falsify the corresponding bounded minimality claim and require GMA-001 to be revised.

## Execution status

The preregistration was merged before any candidate mappings or scores were added. The later internal execution is preserved as a separate artifact so the frozen design remains distinguishable from its results.

The execution is internal implementation evidence, not independent external replication. Its bounded conclusions and unresolved judgments are recorded in `execution.md`.

## Artifacts

- `preregistration.json` — frozen matched-case and decision-rule specification;
- `execution.md` — bounded internal execution report and exact claim limits;
- `results.csv` — all 30 retained mapping records;
- `tests/test_cre003_preregistration.py` — deterministic freeze, orthogonality, and claim-boundary checks;
- `tests/test_cre003_execution.py` — deterministic execution-integrity and result-boundary checks.
