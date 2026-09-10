# Project FAR Fix Register Control

Status: active governance control
Source: Project FAR Complete Fix Register, 117 original audit IDs, generated from a 2,020-file snapshot.

## Authority boundary

The register is a complete audit backlog, not automatic repository truth. Every original ID is immutable and must be preserved, but each finding must be revalidated against current `main` before it is accepted as a defect or closure obligation.

Allowed validation states:

- `unvalidated`
- `confirmed`
- `partially_resolved`
- `resolved`
- `stale`
- `duplicate`
- `needs_evidence`
- `not_accepted`

A finding may not be marked resolved without evidence satisfying its stated completion condition or a documented, reviewable reason that the condition was superseded.

## Work-in-progress limits

At most three remediation tracks may be active simultaneously:

1. one P0 research/external-validation item;
2. one P0 commercial/product item;
3. one repository-maintenance item.

New frameworks and major product categories remain deferred unless a recorded external-evidence trigger justifies activation.

The research slot follows the current governed successor program. When a later protected governance artifact explicitly replaces the active external-validation program, the older bounded experiment remains in the fix register at its evidence-backed disposition but does not continue occupying the P0 slot merely because its original completion condition remains unmet.

## Current queue

- Research — active: `EXTERNAL-FALSIFICATION-AND-REPLICATION-001` (`EFR-001`), the protected successor program for independent replication, external cases, adversarial falsification, human disagreement, real-world utility/cost, and novelty/prior-art testing. Its registered tests remain `PREREGISTERED_NOT_EXECUTED`; recruitment/logistics do not clear any scientific gate.
- Research — legacy open evidence obligation: original ID 3, the frozen SWE-agent release-assurance case, is `needs_evidence`. Environment construction, immutable image publication, preflight, planning, execution control, and post-execution boundary tooling are implemented. The first live run produced a retryable provider/quota failure rather than an accepted completion. Four accepted live runs, primary freeze verification, outcome reveal, and bounded publication remain incomplete. This case may resume under its frozen controls when execution resources permit, but it no longer occupies the sole P0 external-validation slot and does not block EFR recruitment or sealing.
- Commercial — resolved for the registered item: original ID 2 was completed through the bounded compare/adjudicate interface in PR #369 and issue #368. No replacement commercial remediation item is active under this control.
- Maintenance — resolved for the registered items: original IDs 13 and 23–25 were revalidated and completed in PR #371 and issue #370. No replacement maintenance remediation item is active under this control.

Issue #364 is the operational queue authority. This document must be updated when that issue accepts a new active item or records a closure that changes the queue above.

The 2026-09-10 reconciliation basis is `docs/audits/efr-activation-and-living-threat-triage-2026-09-10.md`. It preserves original ID 3 without allowing the pre-EFR queue state to block the later protected successor program.

## Release gates

The following claims remain blocked until their corresponding evidence exists:

- External research validation: independent reviewers, independent target/countermodel selection, preserved negative results, and exact claim disclosure.
- Formal completion: public kernel/executable/prose gap map and at least one bounded end-to-end kernel-checked theorem matching a public claim.
- Commercial readiness: completed external case, benchmark against ordinary review, two paid pilots, one repeat use, and integration under one working day.
- Security readiness: upload threat model, retention controls, dependency scanning, parser hardening, incident response, and external review before sensitive hosted use.
- Repository readiness: no tracked transient bytecode, one canonical status authority, truthful warnings, reproducible generated artifacts, and a clean release build.

## Issue creation rule

All 117 IDs remain trackable immediately. Separate GitHub issues are created only after revalidation confirms that work is independently closable. Overlapping findings may share one implementation issue, but the issue must list every original audit ID it advances or closes.

## Execution relationship

EFR-001 is the active P0 research/external-validation program. It may proceed only through its frozen independent-seal and role-separation controls; internally authored work cannot fabricate an EFR prerequisite or result.

Original ID 3 remains a bounded legacy experiment. If resumed, it retains its original safeguards: no outcome reveal before the blinded freeze, no inflated claims, no silent negative-result deletion, and no readiness claim before its release gate passes. Completing or abandoning that experiment cannot substitute for any EFR test.
