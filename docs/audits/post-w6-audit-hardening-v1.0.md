# Post-W6 Audit Hardening v1.0

Status: **REPAIR IN PROGRESS — REPOSITORY REPAIR IMPLEMENTED, CONTROL-PLANE ENFORCEMENT OPEN**

Record: `POST-W6-AUDIT-HARDENING-001`

Audited canonical target: `main@03cda5007ff4ac8ca3ce90585b8c872f091965cf`, tree `90d299b6c4df4824fe512e63f1cead49c90f9b41`.

This is a maintenance/audit-repair record. It is not a new `POST-CLOSURE-001` workstream, does not imply a W7, and has no impact on `PROJECT-FAR-CORE-THEORY-1.1` or FAR-CORE-001–014.

## Question

Does the completed W6/current-main state contain assurance defects that leave the registered W6 result intact but weaken provenance or canonical-repository enforcement?

## Execution

The audit re-read current main, the W6 preregistration, execution/results record, machine result, semantic verifier, W6 tests, W6 status, current open-problem/planning surfaces, and GitHub branch metadata. The audit also cross-checked the W6 literature framing with independent research lanes.

## Observation

Two actionable defects survived hostile review.

### PW6-AUDIT-001 — execution incidents are not machine-separated from scientific deviations

The frozen W6 machine result correctly records `deviations: []` under the preregistered scientific meaning: no corpus, mutation, endpoint, algorithm, analysis rule, or interpretation boundary changed. The execution record separately documents seven execution/assurance incidents. Because that distinction existed only in prose, a machine consumer could incorrectly read the empty deviations list as meaning that no execution incidents occurred.

Repair: preserve the frozen W6 result byte-for-byte and add `governance/post-w6-execution-incidents-v1.0.json`, which records `scientific_deviations: []` separately from the seven documented execution/assurance incidents. This avoids retroactively rewriting the accepted W6 scientific result while making the provenance distinction machine-readable.

### PW6-AUDIT-002 — canonical main is not server-side protected

GitHub branch metadata at the audited main state reported `protected=false` and required-status enforcement disabled. Repository-local CI and validators can detect defects after a push but cannot prevent an authorized direct push from becoming canonical state. Therefore they are not equivalent to branch protection.

Required permanent repair: enforce server-side protection on `main` with pull-request-only integration, required status checks, up-to-date-branch enforcement, force-push/deletion restrictions, and no administrator-equivalent bypass that can silently replace the governed merge path.

The available GitHub integration can read ordinary branch metadata and modify repository contents, but it does not expose branch-protection/ruleset administration. A direct read of the protection endpoint is also denied to the integration. This repair is therefore recorded as an external control-plane blocker rather than falsely represented as implemented by repository files.

## Discovery

1. The W6 scientific result remains valid at its exact registered finite-artifact scope. Neither finding changes the six-domain corpus, mutation, endpoint, semantic result, or theory impact.
2. `deviations: []` is defensible only as a scientific-protocol statement. Complete provenance requires a distinct incident ledger.
3. Fail-closed repository validation is not the same control as fail-closed canonical-branch admission. The latter requires GitHub control-plane enforcement.

## Replication

The repair checker verifies that the accepted W6 machine result and W6 execution record remain at their audited SHA-256 identities, validates the exact incident IDs and their non-scientific classification, and verifies the hardening record retains the control-plane blocker until external protection is independently observed.

The branch-protection finding is reproducible from GitHub branch metadata. Completion requires a fresh post-configuration control-plane read; a repository-local assertion is explicitly insufficient.

## Acceptance

Accepted repair consequences:

- add a machine-readable W6 incident ledger without mutating the frozen W6 result;
- add a fail-closed repair checker and regression tests;
- expose server-side main protection as an explicit pre-OP-28 blocker;
- prohibit relabeling repository-local CI as branch protection.

Not accepted:

- reopening the core theory;
- changing the registered W6 result;
- silently naming this maintenance repair W7;
- treating the W6 machine oracle as external validation;
- using an after-the-fact push workflow as a substitute for branch protection.

## Promotion and repository change

Repository-side provenance hardening is implemented on `repair/post-w6-audit-hardening` and is mergeable only after its tests and the existing repository validation surface pass.

Control-plane protection remains open until GitHub itself reports the required protected state. OP-28 should not begin while that blocker is open, because an externally governed effectiveness campaign should not write canonical evidence into an admission path that remains bypassable.
