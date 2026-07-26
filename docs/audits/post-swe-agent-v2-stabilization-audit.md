# Post–SWE-agent v2 Stabilization Audit

Status: **Accepted repository audit; not canonical theory**
Date: 2026-07-26

## Scope and method

The audit inspected tracked repository content by domain; canonical architecture, status, map, terminology, decisions, methodology and validation protocols; FAR/FARA/FARO entry points and dependency maps; the v2 preregistration, locks, packages, reveal and reports; relevant Python tests; and all GitHub workflows. Automated checks then compared hashes, derived reports, links, dependency direction, workflow controls and claim language. Historical evidence under `primary-freeze/` and `post-freeze-reveal/` was not edited.

## Ground truth

The only demonstrated outcome is one task and four budget-limited runs: v1.0.0 resolved **0/2**, v1.0.1 resolved **0/2**, so there was `no_observed_resolution_difference`. The outcome-blind integrity decision and final bounded decision are `REVIEW_REQUIRED`. This does not demonstrate equivalence, superiority, safety, commercial or enterprise readiness, or general performance.

## Defects found and fixed

| Defect | Correction |
|---|---|
| Mutable execution status still instructed readers to reveal outcomes after the reveal was committed. | Reconciled it with the frozen final bundle and bounded decision. |
| Completed model execution remained manually dispatchable. | Added a fail-closed completed-bundle guard. |
| Controller exit 75 (internal retryable failure) became workflow success. | Propagated exit 75 while retaining `always()` artifact upload. |
| Final-report verification silently skipped when the reveal was absent. | Made the committed reveal mandatory. |
| No single post-experiment limitations/threat/claim register existed. | Added canonical governance registers and navigation. |
| Evidence and bounded wording relied on scattered tests. | Added a mutation-tested stabilization checker. |

## Historically unfixable defects and limitations

- The completed source artifact is external to Git and its continued availability cannot be proven by this repository; the committed source lock authenticates a retrieved tree but does not preserve that tree.
- Both systems lack a verifiable SWE-ReX commit hash. This provenance gap is frozen evidence and cannot honestly be repaired retrospectively.
- GitHub-hosted actions are referenced by mutable major tags, and the execution installed version-pinned but not hash-locked Python material plus exact Git commits from external hosts. Those historical executions cannot be re-created as hermetic supply-chain proofs.
- The preview model endpoint, API behavior, GitHub runner image and artifact service were externally administered. A digest-pinned task image narrows, but does not remove, infrastructure dependence.
- Runs were sequential and workspace-isolated, but used one provider account, workflow/controller and temporal execution series; statistical independence was neither demonstrated nor measurable from two repetitions.
- All four runs stopped at the call budget. The evidence cannot separate release behavior from budget, model variation, harness behavior, provider behavior or task difficulty.

## Unsupported claims removed or downgraded

No frozen report made an equivalence or superiority claim. Mutable entry points now explicitly reject the tempting inference that equal observed counts establish equivalence. The broad “stable” framework labels remain project maturity labels, not evidence of universality; the claim-status matrix makes that boundary explicit.

## Unresolved theoretical questions

Universality, primitive necessity and independence, global minimality, application correspondence, the FAR/FARA/FARO boundary under all admissible representations, and end-to-end kernel-checked proof remain unresolved or scoped as recorded in the claim matrix.

## Unresolved empirical questions

Whether either release differs across a preregistered task population; how sensitive results are to model, budget and harness; whether the provenance-field changes are operational; and whether an independent evaluator reproduces the case remain unresolved.

## Additional experiments needed

Any follow-up must be a new preregistered case with multiple tasks, enough repetitions for a declared analysis, immutable dependency identities, explicit infrastructure/provider failure classes, independently administered evaluation, and a noninferiority/equivalence design if equivalence is actually the question. The frozen v2 runs must not be silently pooled into it.
