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

Current review target: `PROJECT-FAR-CORE-THEORY-1.1`.

The core theory is closed after the governed v1.1 correction. These tasks change assurance, implementation, applicability, or utility; they do not reopen the core without a genuine contradiction.

The hostile W1 audit that found the v1.1 defects is internal/non-independent evidence. It does not satisfy `PCA-W1-INDEPENDENT-REVIEW`.

Canonical next workstream: `PCA-W1-INDEPENDENT-REVIEW`.

## Ranked Next Actions

### STRATEGIC-010: Review the corrected core independently

- Registered workstream: `PCA-W1-INDEPENDENT-REVIEW`
- Review target: `PROJECT-FAR-CORE-THEORY-1.1`
- Source: [docs/governance/post-closure-assurance-and-application-program-v1.0.md](../governance/post-closure-assurance-and-application-program-v1.0.md)
- Priority: high
- Why it matters: The corrected core is accepted internal deductive work but has no genuinely independent premise-by-premise review.
- Required provenance: disclose reviewer prior exposure, conflicts, tools, assumptions, checked obligations, unresolved objections, and source corpus.
- Expected outcome: An immutable review record that confirms, narrows, refutes, or leaves each obligation OPEN without changing its wording by convention.
- Suggested branch name: `research/pca-w1-core-v1.1-independent-review`
- Suggested PR title: `Execute PCA-W1 independent review of core theory v1.1`

### STRATEGIC-011: Formalize the corrected factorization core

- Registered workstream: `PCA-W2-PROOF-ASSISTANT-FORMALIZATION`
- Source: [docs/governance/post-closure-assurance-and-application-program-v1.0.md](../governance/post-closure-assurance-and-application-program-v1.0.md)
- Priority: queued
- Why it matters: The core has explicit narrative proofs but no single proof-assistant-checked artifact.
- Expected outcome: A checked formalization or an exact obstruction report with external assumptions exposed.
- Suggested branch name: `research/pca-w2-core-formalization`
- Suggested PR title: `Formalize Project FAR core theorems`

### STRATEGIC-012: Implement the contract schema

- Registered workstream: `PCA-W3-CONTRACT-SCHEMA`
- Source: [docs/governance/post-closure-assurance-and-application-program-v1.0.md](../governance/post-closure-assurance-and-application-program-v1.0.md)
- Priority: queued
- Why it matters: `far-ir/1.0` cannot natively certify contracts, decoders, collisions, quotients, profiles, frames, or cost orders.
- Expected outcome: A new versioned schema, deterministic implementation, migration boundary, and conformance suite.
- Suggested branch name: `feat/pca-w3-contract-schema`
- Suggested PR title: `Implement contract-relative FAR IR`

### STRATEGIC-013: Develop domain comparison contracts

- Registered workstream: `PCA-W4-DOMAIN-CONTRACTS`
- Source: [docs/governance/post-closure-assurance-and-application-program-v1.0.md](../governance/post-closure-assurance-and-application-program-v1.0.md)
- Priority: queued
- Why it matters: The core theorem does not select tests, outcome types, or normative objectives for a domain.
- Expected outcome: Independently motivated, versioned contracts with explicit nonclaims and collision tests.
- Suggested branch name: `research/pca-w4-domain-contracts`
- Suggested PR title: `Develop scoped domain contracts`

### STRATEGIC-014: Specify approximation and cost orders

- Registered workstream: `PCA-W5-APPROXIMATION-AND-COST`
- Source: [docs/governance/post-closure-assurance-and-application-program-v1.0.md](../governance/post-closure-assurance-and-application-program-v1.0.md)
- Priority: queued
- Why it matters: Exact information minimality does not choose metrics, decision losses, tolerances, runtime, storage, or explanatory cost.
- Expected outcome: Scoped approximate adequacy and cost-minimality specifications without a universal optimum claim.
- Suggested branch name: `research/pca-w5-approximation-cost`
- Suggested PR title: `Specify approximate and cost-relative adequacy`

### STRATEGIC-015: Test audit utility

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
