# Next Actions

## Navigation

- README Command Center: [README.md](../../README.md)
- Current Project Status: [docs/project-status.md](../project-status.md)
- Core Theory: [theory/theorems/Project-FAR-Theory-Closure-v1.1.md](../../theory/theorems/Project-FAR-Theory-Closure-v1.1.md)
- Historical v1.0 Core: [theory/theorems/Project-FAR-Theory-Closure-v1.0.md](../../theory/theorems/Project-FAR-Theory-Closure-v1.0.md)
- Post-Closure Program: [docs/governance/post-closure-assurance-and-application-program-v1.0.md](../governance/post-closure-assurance-and-application-program-v1.0.md)
- Historical Bounded Status: [docs/reports/project-status-generated.md](../reports/project-status-generated.md)
- Next Actions: [docs/planning/next-actions.md](next-actions.md)

Generated from the registered post-closure program.

Program: `POST-CLOSURE-001`.

Current governing theory: `PROJECT-FAR-CORE-THEORY-1.1`.

The core theory is closed after the governed v1.1 correction. These tasks change assurance, implementation, applicability, or utility; they do not reopen the core without a genuine contradiction.

The hostile correction audit remains non-independent. The separately sealed `PCA-W1-INDEPENDENT-REVIEW` is complete: 14 PROVED, no correction, novelty/priority not established.

Canonical next workstream: `PCA-W2-PROOF-ASSISTANT-FORMALIZATION`.

## Ranked Next Actions

### STRATEGIC-010: Close the bounded MLL formalization bridge

- Registered workstream: `PCA-W2-PROOF-ASSISTANT-FORMALIZATION`
- Source: [docs/governance/post-closure-assurance-and-application-program-v1.0.md](../governance/post-closure-assurance-and-application-program-v1.0.md)
- Priority: active
- Why it matters: FAR-CORE-001 through 013 are formalized, but FAR-CORE-014 still lacks Lean proofs of the actual PR #453 MLL witness profiles.
- Expected outcome: An end-to-end certified MLL application module or preservation of the exact reproducible obstruction without added premises.
- Suggested branch name: `research/pca-w2-core-formalization`
- Suggested PR title: `Complete Project FAR core v1.1 formalization`

### STRATEGIC-011: Implement the contract schema

- Registered workstream: `PCA-W3-CONTRACT-SCHEMA`
- Source: [docs/governance/post-closure-assurance-and-application-program-v1.0.md](../governance/post-closure-assurance-and-application-program-v1.0.md)
- Priority: queued
- Why it matters: `far-ir/1.0` cannot natively certify contracts, decoders, collisions, quotients, profiles, frames, or cost orders.
- Expected outcome: A new versioned schema, deterministic implementation, migration boundary, and conformance suite.
- Suggested branch name: `feat/pca-w3-contract-schema`
- Suggested PR title: `Implement contract-relative FAR IR`

### STRATEGIC-012: Develop domain comparison contracts

- Registered workstream: `PCA-W4-DOMAIN-CONTRACTS`
- Source: [docs/governance/post-closure-assurance-and-application-program-v1.0.md](../governance/post-closure-assurance-and-application-program-v1.0.md)
- Priority: queued
- Why it matters: The core theorem does not select tests, outcome types, or normative objectives for a domain.
- Expected outcome: Independently motivated, versioned contracts with explicit nonclaims and collision tests.
- Suggested branch name: `research/pca-w4-domain-contracts`
- Suggested PR title: `Develop scoped domain contracts`

### STRATEGIC-013: Specify approximation and cost orders

- Registered workstream: `PCA-W5-APPROXIMATION-AND-COST`
- Source: [docs/governance/post-closure-assurance-and-application-program-v1.0.md](../governance/post-closure-assurance-and-application-program-v1.0.md)
- Priority: queued
- Why it matters: Exact information minimality does not choose metrics, decision losses, tolerances, runtime, storage, or explanatory cost.
- Expected outcome: Scoped approximate adequacy and cost-minimality specifications without a universal optimum claim.
- Suggested branch name: `research/pca-w5-approximation-cost`
- Suggested PR title: `Specify approximate and cost-relative adequacy`

### STRATEGIC-014: Test audit utility

- Registered workstream: `PCA-W6-EMPIRICAL-AUDIT-UTILITY`
- Source: [docs/governance/post-closure-assurance-and-application-program-v1.0.md](../governance/post-closure-assurance-and-application-program-v1.0.md)
- Priority: external-dependency
- Why it matters: No preregistered external study shows that contract/factorization auditing catches material loss or reduces disagreement.
- Expected outcome: Bounded empirical evidence with negative results, protocol deviations, and independence disclosed.
- Suggested branch name: `research/pca-w6-audit-utility`
- Suggested PR title: `Prepare PCA-W6 audit-utility study`

## Maintainer Boundaries

- Read `AGENTS.md` and the Research Execution Charter before execution.
- Preserve historical v1.0 bytes/hash and the corrected v1.1 authority.
- Preserve the v1.1 FAR-CORE-004 minimality/sufficiency distinction and FAR-CORE-010 exact-theory/frame-residue distinction.
- Reopen the core only for a reproducible contradiction to a premise, proof step, theorem, or derivation.
- Keep determinate absence, failure, inapplicability, unresolvedness, and epistemic Unknown distinct when the contract does.
- Do not infer mathematical proof from CI, schema conformance, finite panels, or successful encoding.

Validation commands:

- `python tools/check_project_far_theory_closure.py`
- `make semantic-check`
- `make docs-check`
- `make health-fast`

## Navigation

- README Command Center: [README.md](../../README.md)
- Current Project Status: [docs/project-status.md](../project-status.md)
- Core Theory: [theory/theorems/Project-FAR-Theory-Closure-v1.1.md](../../theory/theorems/Project-FAR-Theory-Closure-v1.1.md)
- Historical v1.0 Core: [theory/theorems/Project-FAR-Theory-Closure-v1.0.md](../../theory/theorems/Project-FAR-Theory-Closure-v1.0.md)
- Post-Closure Program: [docs/governance/post-closure-assurance-and-application-program-v1.0.md](../governance/post-closure-assurance-and-application-program-v1.0.md)
- Historical Bounded Status: [docs/reports/project-status-generated.md](../reports/project-status-generated.md)
- Next Actions: [docs/planning/next-actions.md](next-actions.md)
