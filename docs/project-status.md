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

Current canonical authority includes the corrected core theory v1.1, machine-readable v1.1 claim ledger, v1.1 acceptance record, W1 independent-review promotion, machine assurance ledger, W2 formalization status, W3 contract-schema status, and W4 domain-contract status. Historical v1.0 remains preserved byte-for-byte at SHA-256 `b7cbd28d54686da33773a66edf9af9480044ffaabfeb83cfa4bfc1a12fe862a5`.

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

## W3 contract-schema disposition

`PCA-W3-CONTRACT-SCHEMA` is complete. `far-ir/2.0` is the versioned comparison-contract successor; `far-ir/1.0` remains unchanged as the legacy reasoning-document interchange format.

The v2 contract explicitly represents source/case domain, required behavior, representation, observation contexts, admitted transformations/equivalences, interpretation profile, target/model class, frame, typed outcomes including `Unknown`, factorization/collision/quotient evidence, failure reporting, provenance/freeze metadata, and optional approximation/loss/cost declarations. Checked finite-explicit evidence is recomputed by the semantic verifier. Loss-explicit migration from v1 preserves the legacy primitive payload and marks semantics absent from v1 `Unknown` rather than fabricating them.

W3 does not establish application correspondence for any external domain and does not establish W5 approximation/cost semantics. Schema reuse is not primitive necessity or universal architecture evidence.

## W4 domain-contract disposition

`PCA-W4-DOMAIN-CONTRACTS` is complete at six finite-explicit domain scopes. Native memos for formal logic, Bayesian/causal reasoning, argumentation, model-based reasoning, type theory, and proof theory were frozen before controlled `far-ir/2.0` mapping.

Each domain has a checked lossy collision and a checked repaired factorization. The generic v2 verifier, domain-specific native recomputation, source/memo hash checks, mutation controls, and a corrected Wolfram finite enumeration all pass. Zotero remained unavailable locally; the failure is retained and the repository bibliography is not represented as Zotero-managed.

W4 does not establish minimal or unique repairs, open-domain completeness, approximation/cost semantics, empirical utility, novelty/priority, or external-investigator independence.

## Current phase

Current program: `POST-CLOSURE-001` — [Post-Closure Assurance and Application Program v1.0](governance/post-closure-assurance-and-application-program-v1.0.md).

| Workstream | Current state | Boundary |
|---|---|---|
| `PCA-W0-REPOSITORY-CONFORMITY` | Complete | Original closure integration completed; v1.1 correction is governed successor maintenance. |
| `PCA-W1-INDEPENDENT-REVIEW` | Complete | Sealed exact-scope review promoted; 14 PROVED, no correction; novelty/priority not established. |
| `PCA-W2-PROOF-ASSISTANT-FORMALIZATION` | Complete | 14 FORMALIZED; exact kernel assumptions audited; no contradiction/reopen condition. |
| `PCA-W3-CONTRACT-SCHEMA` | Complete | `far-ir/2.0` successor, semantic verifier, loss-explicit migration, and conformance fixtures complete; v1 unchanged. |
| `PCA-W4-DOMAIN-CONTRACTS` | Complete | Six frozen native contracts; six checked lossy collisions and six checked scoped repairs; internal mapping only. |
| `PCA-W5-APPROXIMATION-AND-COST` | **Next / Active** | Approximation and implementation minimality require declared metrics, losses, tolerances, or cost orders. |
| `PCA-W6-EMPIRICAL-AUDIT-UTILITY` | Open | Empirical utility evidence does not alter deductive theorem status automatically. |

## W5 entry boundary

W5 must not reinterpret W4's exact repairs as approximate or cost-optimal. Every approximate claim must add a declared metric or divergence, tolerance, decision loss, and cost preorder under a new freeze.

The W4 finite-explicit certificates prove only the encoded table properties. They do not prove that the tables exhaust or faithfully represent their external domains.

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
