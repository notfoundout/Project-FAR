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

Program: `POST-CLOSURE-001` — complete at its six registered workstream scopes.

Current governing theory: `PROJECT-FAR-CORE-THEORY-1.1`.

The core theory is closed after the governed v1.1 correction. The sealed W1 independent review, W2 proof-assistant formalization, W3 contract schema, W4 domain contracts, W5 approximation/cost semantics, and W6 bounded internal audit-utility control are complete at their exact governed scopes.

There is **no registered next `POST-CLOSURE-001` workstream**. External/human audit-effectiveness evidence remains an open downstream obligation under OP-28 and requires separate governance before execution; it is not silently named W7.

A post-W6 hostile audit found two maintenance defects that do not change the W6 scientific result or the core theory. Machine-readable separation of scientific deviations from execution incidents is repaired on `repair/post-w6-audit-hardening`. Server-side protection of canonical `main` remains an external control-plane blocker and must be completed before OP-28 execution.

## Ranked Next Actions

### POST-W6-AUDIT-HARDENING-001: Close assurance defects before external evaluation

- Kind: maintenance/audit repair; not a `POST-CLOSURE-001` workstream and not W7.
- Repository-side status: machine-readable W6 execution-incident provenance implemented on the repair branch with fail-closed checks.
- Open blocker: GitHub `main` must be server-side protected with pull-request-only admission, required status checks, up-to-date enforcement, force-push/deletion restrictions, and no silent administrator-equivalent bypass.
- Completion evidence: a fresh GitHub control-plane read showing the required protected state. Repository-local files, CI, or after-the-fact push failures are not substitutes.
- Authority: [`post-w6-audit-hardening-v1.0.md`](../audits/post-w6-audit-hardening-v1.0.md) and `governance/post-w6-audit-hardening-v1.0.json`.

### STRATEGIC-012: Develop domain comparison contracts

- Registered workstream: `PCA-W4-DOMAIN-CONTRACTS`
- Priority: complete
- Outcome: Six source-motivated native contracts, twelve `far-ir/2.0` records, six checked collisions, and six checked scoped repairs with explicit nonclaims.

### STRATEGIC-013: Specify approximation and cost orders

- Registered workstream: `PCA-W5-APPROXIMATION-AND-COST`
- Priority: complete
- Outcome: Checked finite-explicit `far-ir/2.1` approximation and product-cost semantics without a universal optimum claim.

### STRATEGIC-014: Test audit utility

- Registered workstream: `PCA-W6-EMPIRICAL-AUDIT-UTILITY`
- Priority: complete at bounded internal controlled-artifact scope
- Outcome: Preregistered six-domain control found schema-only mutation detection `0/6`, FAR semantic mutation detection `6/6`, clean-control acceptance `6/6`, FAR/oracle agreement `12/12`, and native lossy-control confirmation `6/6`.
- Boundary: human disagreement reduction remains `UNDERDETERMINED`; external real-world utility remains `OPEN`.

### OPEN-EXTERNAL-OP-28: Independently test human/external audit effectiveness

- Registered post-closure workstream: none
- Authority: OP-28 in the open-problems register
- Priority: open / external-dependency
- Precondition: `POST-W6-AUDIT-HARDENING-001` must close its GitHub control-plane protection blocker before execution begins.
- Why it matters: W6 establishes only a project-authored machine controlled-artifact result. It does not show that human reviewers catch more consequential loss, disagree less, work faster, or make better real-world decisions.
- Required before execution: a separately governed protocol defining participant population or external evaluator, comparator, blinded/randomized procedure where appropriate, outcome measures, analysis plan, independence disclosure, data governance/ethics requirements, falsifiers, and promotion boundaries.
- Prohibited shortcut: do not relabel W6's schema baseline, machine oracle, or internal replication as human or external evidence.

## Maintainer Boundaries

- Read `AGENTS.md` and the Research Execution Charter before execution.
- Preserve historical v1.0 bytes/hash and the corrected v1.1 authority.
- Preserve the v1.1 FAR-CORE-004 minimality/sufficiency distinction and FAR-CORE-010 exact-theory/frame-residue distinction.
- Reopen the core only for a reproducible contradiction to a premise, proof step, theorem, or derivation.
- Keep determinate absence, failure, inapplicability, unresolvedness, and epistemic Unknown distinct when the contract does.
- Do not infer mathematical proof from CI, schema conformance, finite panels, successful encoding, or W6 controlled-artifact performance.

Validation commands:

- `python tools/check_post_w6_audit_hardening.py`
- `python -m unittest tests.test_post_w6_audit_hardening -v`
- `python tools/check_project_far_theory_closure.py`
- `make pca-w6-check`
- `make semantic-check`
- `make docs-check`
- `make health-fast`
