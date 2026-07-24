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

## Current active queue

- Research: original ID 3, complete the frozen SWE-agent release-assurance case. Environment construction, immutable image publication, preflight, and planning are complete. Four sequential runs, FAR evidence compilation, blinded comparison freeze, outcome reveal, and final publication remain.
- Commercial: original ID 2, define one stable compare/adjudicate CLI/API, initially bounded to the SWE-agent case requirements.
- Maintenance: validate original IDs 13 and 23–25 against current `main`, then remove confirmed repository-truth defects.

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

The register does not block the SWE-agent experiment as a whole because original ID 3 is the experiment itself. It constrains execution: no outcome reveal before the blinded freeze, no inflated claims, no silent negative-result deletion, and no readiness claim before its release gate passes.
