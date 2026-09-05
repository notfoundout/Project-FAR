# Project FAR Status

This file is the canonical project-level status surface identified by [`CANONICAL_MAP.md`](CANONICAL_MAP.md). It records current governance and milestone state and does not upgrade any linked artifact beyond its stated scope or assurance.

## Current release

Current published repository release: [`v1.0.0`](releases/project-far-v1.0.0.md). The installable package version remains a separate surface governed by `pyproject.toml`; post-release theory and assurance work does not silently retag either surface.

## Central result

Current governing theory: `PROJECT-FAR-CORE-THEORY-1.1`.

Terminal verdict, unchanged from historical v1.0:

`NONTRIVIAL CONTRACT-FREE MINIMAL ARCHITECTURE IS IMPOSSIBLE; CONTRACT-RELATIVE SUFFICIENCY AND A UNIQUE MINIMAL OBSERVATIONAL QUOTIENT ARE PROVED.`

For a fixed exact contract, sufficiency is equivalent to factorization through the representation and the induced observational quotient is the unique least-informative exact representation up to isomorphism. On a nontrivial domain, no single representation is simultaneously least-informative sufficient for every observation contract. The identity representation can nevertheless be sufficient for every observation contract on fixed `X`; `FAR-CORE-004` is a minimality impossibility, not a universal-sufficiency impossibility.

`FAR-CORE-010` is corrected in v1.1: exact common theory `T_{L,J,I}` is indexed by language, interpretation profiles/models, and target class. The frame `Γ` additionally indexes the frame-subtracted residue `T_{L,J,I} \ Cn_L(Γ)`; changing `Γ` alone while holding the interpreted models fixed does not change exact `T`.

Assurance: **Accepted internal deductive result; corrected after a non-independent hostile audit; subsequently reviewed under sealed I1 claimed isolation at exact scopes; all 14 governed claims subsequently mechanized under pinned Lean 4.19.0. I2 verified isolation, I3 external independent validation/replication, novelty, and priority are not established.**

Current canonical authority includes the corrected core theory v1.1, machine-readable v1.1 claim ledger, v1.1 acceptance record, W1 independent-review promotion, machine assurance ledger, W2 formalization status, W3 contract-schema status, W4 domain-contract status, W5 approximation-and-cost status, and W6 bounded audit-utility status. Historical v1.0 remains preserved byte-for-byte at SHA-256 `b7cbd28d54686da33773a66edf9af9480044ffaabfeb83cfa4bfc1a12fe862a5`.

## Historical boundaries

The historical UPP adjudication remains: **Frozen proposition not refuted; frozen derivation defective; theorem not established.** `POST-TERM-EVAL-001` is superseded and `UPP-SR-001` is optional bounded historical work, not a core dependency.

The frozen SWE-agent v2 comparison remains a bounded historical result: v1.0.0 resolved **0/2** preregistered runs and v1.0.1 resolved **0/2** preregistered runs, yielding `no_observed_resolution_difference` and bounded-case decision `REVIEW_REQUIRED`. Those observations do not establish equivalence, superiority, safety, readiness, or general performance for either release.

PR #453 remains noncanonical Research. Its E0 blocked, E1 fragmented, SSS, profile-relative irreflexivity, and open-boundary results retain their recorded scopes and do not supply premises of the accepted core theory except where the governing v1.1 claim explicitly depends on the bounded application record.

## W1 assurance disposition

The sealed staged review completed the workstream named `PCA-W1-INDEPENDENT-REVIEW`: 14 `PROVED`, 0 `REFUTED`, 0 `OPEN`, and 0 `UNDERDETERMINED`; no theorem correction was required. The exposure record supports I1 claimed isolation because repository access was prohibited by instruction but not technically prevented. It does not support I2 or I3 external independence/replication, novelty, or priority. `FAR-CORE-014` retains its governing `SUPPORTED/DERIVED` provenance label while the W1 exact-scope truth verdict is `PROVED`. Truth, provenance, and isolation class are separate dimensions.

## W2 formalization disposition

`PCA-W2-PROOF-ASSISTANT-FORMALIZATION` is complete. Pinned Lean 4.19.0 checks all 14 governed claims as `FORMALIZED`, with zero `PARTIAL/OBSTRUCTION` and zero `CONTRADICTION/REOPEN REQUIRED` outcomes.

FAR-CORE-014 now includes the bounded unit-free MLL witness bridge end to end: syntax/sequents, resource-splitting derivability, atom balance, the named `S_or` and `S_and` witness profiles, exhaustive monotone decoder classification, and bounded projected-decoder failure. The runtime `#print axioms` audit pins exact transitive kernel dependencies rather than treating tactic success as premise-free proof.

W2 changes only mechanization assurance. It does not establish novelty, priority, empirical utility, computational efficiency, open-domain universality, or product readiness.

## W3 contract-schema disposition

`PCA-W3-CONTRACT-SCHEMA` is complete. `far-ir/2.0` is the versioned comparison-contract successor; `far-ir/1.0` remains unchanged as the legacy reasoning-document interchange format.

The v2 contract explicitly represents source/case domain, required behavior, representation, observation contexts, admitted transformations/equivalences, interpretation profile, target/model class, frame, typed outcomes including `Unknown`, factorization/collision/quotient evidence, failure reporting, provenance/freeze metadata, and optional approximation/loss/cost declarations. Checked finite-explicit evidence is recomputed by the semantic verifier. Loss-explicit migration from v1 preserves the legacy primitive payload and marks semantics absent from v1 `Unknown` rather than fabricating them.

W3 does not establish application correspondence for any external domain and does not establish W5 approximation/cost semantics. Schema reuse is not primitive necessity or universal architecture evidence.

## W4 domain-contract disposition

`PCA-W4-DOMAIN-CONTRACTS` is complete at six finite-explicit domain scopes. Native memos for formal logic, Bayesian/causal reasoning, argumentation, model-based reasoning, type theory, and proof theory were frozen before controlled `far-ir/2.0` mapping.

Each domain has a checked lossy collision and a checked repaired factorization. The generic v2 verifier, domain-specific native recomputation, source/memo hash checks, mutation controls, and a corrected Wolfram finite enumeration all pass. Zotero remained unavailable locally; the failure is retained and the repository bibliography is not represented as Zotero-managed.

W4 does not establish minimal or unique repairs, open-domain completeness, approximation/cost semantics, empirical utility, novelty/priority, or external-investigator independence.

## W5 approximation-and-cost disposition

`PCA-W5-APPROXIMATION-AND-COST` is complete at the frozen finite-explicit operational scope. W5 did not reinterpret W4's exact repairs as approximate or cost-optimal. Its additive `far-ir/2.1` controls separately freeze a metric, reference and aggregation rule, decision loss, tolerance, randomized decoder, and multidimensional cost preorder. Checked finite results distinguish Pareto minima from least elements and enforce the zero-loss recovery boundary.

W5 does not establish a universal metric, reference, tolerance, scalar cost, unique optimum, external-domain correspondence, open-domain approximation result, empirical utility, or novelty.

## W6 empirical audit-utility disposition

`PCA-W6-EMPIRICAL-AUDIT-UTILITY` is complete at the preregistered bounded internal controlled-artifact scope. The protocol was frozen before execution at `3813b9e3eb49562bd8b9f4d3179c3d9536831de6` from canonical base `2cecf2e21cc27208f606dcd38337af4369e66af2`.

The primary experiment used six unmodified W4 repaired controls and six deterministic representation-collision mutants. All twelve remained JSON-Schema-valid. The schema-only baseline detected `0/6` mutants and accepted `6/6` clean controls. The FAR finite-explicit semantic audit detected `6/6` mutants with `FACTORIZATION_FAILURE` and accepted `6/6` clean controls. A separate table-only collision oracle agreed with the FAR loss/no-loss classification on `12/12` primary records. All six frozen native W4 lossy controls were also separately recomputed.

This proves only the registered bounded material-loss-detection result. The corpus, mutation, oracle, and adjudication were Project-FAR-authored; there were no human participants or external investigators. Human disagreement reduction is `UNDERDETERMINED` and external real-world utility remains `OPEN`. No population sensitivity/specificity, superiority over alternative audit methods, or theorem-status change is inferred.

## Current phase

Completed predecessor: `POST-CLOSURE-001` — [Post-Closure Assurance and Application Program v1.0](governance/post-closure-assurance-and-application-program-v1.0.md) — complete at its six registered workstream scopes.

Current program: `EXTERNAL-FALSIFICATION-AND-REPLICATION-001` — [External Falsification and Replication Program v1.0](governance/external-falsification-and-replication-program-v1.0.md) — **preregistered; not executed; not W7**. Its [canonical W1–W6 claim/evidence matrix](governance/w1-w6-claim-evidence-matrix-v1.0.md) fixes the inherited claims and nonclaims.

| Workstream | Current state | Boundary |
|---|---|---|
| `PCA-W0-REPOSITORY-CONFORMITY` | Complete | Original closure integration completed; v1.1 correction is governed successor maintenance. |
| `PCA-W1-INDEPENDENT-REVIEW` | Complete | Sealed I1 claimed-isolation exact-scope review; 14 PROVED, no correction; not I3 external validation; novelty/priority not established. |
| `PCA-W2-PROOF-ASSISTANT-FORMALIZATION` | Complete | 14 FORMALIZED; exact kernel assumptions audited; no contradiction/reopen condition. |
| `PCA-W3-CONTRACT-SCHEMA` | Complete | `far-ir/2.0` successor, semantic verifier, loss-explicit migration, and conformance fixtures complete; v1 unchanged. |
| `PCA-W4-DOMAIN-CONTRACTS` | Complete | Six frozen native contracts; six checked lossy collisions and six checked scoped repairs; internal mapping only. |
| `PCA-W5-APPROXIMATION-AND-COST` | Complete | `far-ir/2.1` checks finite metrics, references/aggregation, losses, tolerances, randomized decoders, product cost preorders, Pareto/least sets, and exact recovery. |
| `PCA-W6-EMPIRICAL-AUDIT-UTILITY` | Complete | Bounded internal controlled-artifact loss detection proved for registered corpus; human disagreement and external utility not established. |

No `POST-CLOSURE-001` W7 is registered. EFR-001 is the separately governed successor and all eight tests remain `PREREGISTERED_NOT_EXECUTED`; OP-28 remains open.

## Framework status

| Framework | Terminal role | Current status |
|---|---|---|
| FARA | Selected representation target | Stable; `FARA-FORMAL-KERNEL-001` retained only for finite, explicit, auditable Project FAR v1 records. |
| FAR | Contract-relative methodology | Stable with contract freeze, factorization/collision, minimization, and typed-loss conformance. |
| FARO | Downstream operations | Role defined; implementation, product, external-validation, and deployment readiness not established. |
| FARE | Mathematical support | Requirement-driven; does not replace the canonical core theory. |
| FARM | Change coordination | Stable; does not reverse the canonical dependency direction. |

The seven formerly named FARA primitive candidates are schema or contract roles, not global primitives. Construct, Differentiate, and Restrict are workflow verbs. Resolve and Ω are derived.

## Reopening rule

The core reopens only for a reproducible contradiction to a stated theorem, proof step, or formal premise. CI success, finite scripts, repository consistency, model agreement, software conformance, and W6 controlled-artifact performance are not mathematical proof.

## Current authority navigation

For state-sensitive work, use the root README, this status, `CANONICAL_MAP.md`, the corrected core theory and acceptance record, the canonical W1–W6 matrix, claim-status matrix and theorem/proof register, framework boundaries and dependency specification, then limitations/open-problems/unresolved-question registers. Historical or generated surfaces do not override that order.
