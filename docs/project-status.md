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

Assurance: **Accepted internal deductive result; corrected after a non-independent hostile audit; subsequently confirmed by sealed independent review under exact scopes; all 14 governed claims subsequently mechanized under pinned Lean 4.19.0. Novelty/priority not established.**

Current canonical authority includes the corrected core theory v1.1, machine-readable v1.1 claim ledger, v1.1 acceptance record, W1 independent-review promotion, machine assurance ledger, and W2 formalization status. Historical v1.0 remains preserved byte-for-byte at SHA-256 `b7cbd28d54686da33773a66edf9af9480044ffaabfeb83cfa4bfc1a12fe862a5`.

## Historical boundaries

The historical UPP adjudication remains: **Frozen proposition not refuted; frozen derivation defective; theorem not established.** `POST-TERM-EVAL-001` is superseded and `UPP-SR-001` is optional bounded historical work, not a core dependency.

The frozen SWE-agent v2 comparison remains a bounded historical result: v1.0.0 resolved **0/2** preregistered runs and v1.0.1 resolved **0/2** preregistered runs, yielding `no_observed_resolution_difference` and bounded-case decision `REVIEW_REQUIRED`. Those observations do not establish equivalence, superiority, safety, readiness, or general performance for either release.

PR #453 remains noncanonical Research. Its E0 blocked, E1 fragmented, SSS, profile-relative irreflexivity, and open-boundary results retain their recorded scopes and do not supply premises of the accepted core theory except where the governing v1.1 claim explicitly depends on the bounded application record.

## W1 assurance disposition

The sealed staged review completed `PCA-W1-INDEPENDENT-REVIEW`: 14 `PROVED`, 0 `REFUTED`, 0 `OPEN`, and 0 `UNDERDETERMINED`; no theorem correction was required; novelty and priority were not established. `FAR-CORE-014` retains its governing `SUPPORTED/DERIVED` provenance label while its independent-review truth verdict is `PROVED` under the exact application scope. Truth and provenance are separate dimensions.

## W2 formalization disposition

`PCA-W2-PROOF-ASSISTANT-FORMALIZATION` is complete. Pinned Lean 4.19.0 checks all 14 governed claims as `FORMALIZED`, with zero `PARTIAL/OBSTRUCTION` and zero `CONTRADICTION/REOPEN REQUIRED` outcomes.

FAR-CORE-014 now includes the bounded unit-free MLL witness bridge end to end: syntax/sequents, resource-splitting derivability, atom balance, the named `S_or` and `S_and` witness profiles, exhaustive monotone decoder classification, and bounded projected-decoder failure. The runtime `#print axioms` audit pins exact transitive kernel dependencies rather than treating tactic success as premise-free proof.

W2 changes only mechanization assurance. It does not establish novelty, priority, empirical utility, computational efficiency, open-domain universality, or product readiness.

## Current phase

Current program: `POST-CLOSURE-001` — [Post-Closure Assurance and Application Program v1.0](governance/post-closure-assurance-and-application-program-v1.0.md).

| Workstream | Current state | Boundary |
|---|---|---|
| `PCA-W0-REPOSITORY-CONFORMITY` | Complete | Original closure integration completed; v1.1 correction is governed successor maintenance. |
| `PCA-W1-INDEPENDENT-REVIEW` | Complete | Sealed exact-scope review promoted; 14 PROVED, no correction; novelty/priority not established. |
| `PCA-W2-PROOF-ASSISTANT-FORMALIZATION` | Complete | 14 FORMALIZED; exact kernel assumptions audited; no contradiction/reopen condition. |
| `PCA-W3-CONTRACT-SCHEMA` | **Next / Active** | Implement a versioned successor contract/factorization format; `far-ir/1.0` is not silently reinterpreted. |
| `PCA-W4-DOMAIN-CONTRACTS` | Open | Domain contracts remain scoped choices and cannot restore contract-free universality. |
| `PCA-W5-APPROXIMATION-AND-COST` | Open | Approximation and implementation minimality require declared metrics, losses, tolerances, or cost orders. |
| `PCA-W6-EMPIRICAL-AUDIT-UTILITY` | Open | Empirical utility evidence does not alter deductive theorem status automatically. |

## W3 entry boundary

W3 must implement a successor to `far-ir/1.0`, not reinterpret it in place. The successor contract must explicitly represent the case/source domain, required behavior, representation, decoder/factorization or collision evidence, observation contexts, typed outcomes including `Unknown`, observational equivalence/quotient evidence, admitted transformations/equivalences, interpretation profile, target/model class, frame, provenance/freeze metadata, and optional approximation/loss/cost declarations.

## Framework status

| Framework | Terminal role | Current status |
|---|---|---|
| FARA | Selected representation target | Stable; `FARA-FORMAL-KERNEL-001` retained only for finite, explicit, auditable Project FAR v1 records. |
| FAR | Contract-relative methodology | Stable with contract freeze, factorization/collision, minimization, and typed-loss conformance. |
| FARO | Downstream operations | Stable for execution, materialized views, comparison, audit, and reporting. |
| FARE | Mathematical support | Requirement-driven; does not replace the canonical core theory. |
| FARM | Change coordination | Stable; does not reverse the canonical dependency direction. |

The seven formerly named FARA primitive candidates are schema or contract roles, not global primitives. Construct, Differentiate, and Restrict are workflow verbs. Resolve and Ω are derived.

## Reopening rule

The core reopens only for a reproducible contradiction to a stated theorem, proof step, or formal premise. CI success, finite scripts, repository consistency, model agreement, and software conformance are not mathematical proof.

## Current authority navigation

For state-sensitive work, use the root README, this status, `CANONICAL_MAP.md`, the corrected core theory and acceptance record, claim-status matrix and theorem/proof register, framework boundaries and dependency specification, then limitations/open-problems/unresolved-question registers. Historical or generated surfaces do not override that order.
