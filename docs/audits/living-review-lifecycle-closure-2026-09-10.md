# Living-review lifecycle closure — 2026-09-10

Status: **Governance/research audit — no FAR-CORE or EFR status change**

## Problem

PR #493 reviewed the then-current 16 high-attention candidates and repaired a generic `impossibility` routing defect. A later scheduled living-research run showed a separate lifecycle defect: `tools/reconcile_living_repo.py` rebuilt `core_claim_review_queue` from every high-attention, claim-mapped raw candidate without consulting any durable record of completed governed review. The scheduled workflow therefore republished already-reviewed candidates into issue #489 as if review were still required.

A second routing defect was exposed while repairing that lifecycle: historical/foundational prior-art backfill could enter the core-claim contradiction queue merely because its target set included `FAR-RQ-009`, even when its registered candidate relation was historical rather than a direct counterexample/theorem threat.

Raw candidate records are discovery history and must remain preserved. Mutating or deleting those records would lose provenance, while promoting automation-created candidate records beyond `DISCOVERED` would violate the living-repository lifecycle. The repair is therefore a canonical review-disposition registry on protected `main`, plus an explicit routing boundary for the core-claim queue. Reconciliation suppresses only candidates explicitly recorded as reviewed, and fully identified historical/foundational records remain research or prior-art material unless they also enter through the direct governed threat lane. It does not rewrite the source record or alter a claim.

## Three candidates discovered after PR #493

### `FAR-LIT-39EF4FD80D5956BD`

Source: Xiaojian Zeng, *A Counterexample to The 2-4-6-8 Binomial Representation Conjecture*, DOI `10.2139/ssrn.7406858`.

Disposition: `IRRELEVANT_FALSE_POSITIVE`.

The candidate was admitted through the FAR-RQ-009 query `Blackwell sufficiency quotient counterexample` because its title contains `counterexample` and `representation`. Its subject is a specific binomial representation conjecture. The discovered record supplies no contract-relative sufficiency, behavioral factorization, observational quotient, or countermodel satisfying the premises of FAR-CORE-001–014. It therefore supplies no reproducible FAR-core contradiction.

### `FAR-LIT-C566FE21125E277F`

Source: Lars John Lefgren, Frank McIntyre, and David Sims, *Is the Intergenerational Income Elasticity a Sufficient Statistic for Fairness?*, DOI `10.2139/ssrn.2379562`.

Disposition: `IRRELEVANT_FALSE_POSITIVE`.

The paper compares economic models of intergenerational mobility and asks whether an empirical elasticity is normatively informative about fairness. Its abstract presents an alternative economic model yielding similar observable predictions but opposite normative conclusions. The phrase `sufficient statistic` is used inside that economics problem; the paper does not state a general representation-sufficiency theorem, FAR's fixed-contract factorization condition, or a countermodel to the governed finite-explicit theorem. No FAR-core contradiction follows.

### `FAR-LIT-DC526D11098789EF`

Source: Susmit Jha and Sanjit A. Seshia, *A theory of formal synthesis via inductive learning*, Acta Informatica 54(7), 2017, DOI `10.1007/s00236-017-0294-5`.

Disposition: `ADJACENT_NO_CONTRADICTION`.

The paper develops oracle-guided inductive synthesis and analyzes counterexample-guided inductive synthesis, including the relative power of counterexample variants and finite-language convergence. This is genuine adjacent prior art for counterexample-driven formal reasoning and should remain in the research record. It does not assert the negation of FAR's exact fixed-contract factorization theorem, construct a same-representation/different-required-behavior witness under FAR's premises, or refute the canonical observational quotient result. It is therefore relevant background without a surviving FAR-core contradiction.

## Canonical review registry

`research/living/review-dispositions-v1.0.json` records the 16 dispositions from the PR #493 audit plus the three dispositions above. Registry membership means only that the candidate no longer belongs in the active metadata-only review queue under the cited review basis. The raw candidate remains untouched and rediscoverable in provenance history.

The registry cannot establish support, novelty, priority, external validity, independence, or an EFR result. `N1_PRIOR_ART_LEAD` remains a lead for the independently controlled EFR-N1 search and does not become an N1 result through registry membership.

## Required reconciliation behavior

A candidate enters `core_claim_review_queue` only when it is high-attention, claim-mapped, routed through the explicit `FAR-RQ-009` / `POTENTIAL_COUNTEREXAMPLE_OR_RELATED_THEOREM` lane, and lacks a canonical suppressing review disposition. A legacy record whose binding lacks both target and candidate-relation metadata remains review-required conservatively until it is classified; missing routing metadata may not silently suppress a possible threat. Fully identified historical/foundational backfill does not self-escalate into the core-claim queue merely because one of its target IDs is `FAR-RQ-009`.

Reconciliation validates the review registry before using it, rejects duplicate IDs, unknown dispositions, malformed candidate IDs, or non-suppressing rows, and reports direct-core-threat, reviewed, and active-review counts separately.

This closes the queue-memory and route-escalation defects while preserving the lifecycle boundary: unattended automation continues to create only `DISCOVERED` candidate records, and protected canonical review state controls whether an already-reviewed candidate is presented again as requiring review.

## Result

The 19 candidates present in issue #489 at this audit snapshot contain no established reproducible contradiction to FAR-CORE-001–014. One previously reviewed candidate, `FAR-LIT-8698902E49C77D94`, remains a material novelty/prior-art lead for independent EFR-N1. The active core-claim queue should contain only later unreviewed direct threats or ambiguous legacy records after reconciliation under the repaired logic.
