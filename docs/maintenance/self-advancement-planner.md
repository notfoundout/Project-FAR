# Maintaining the Self-Advancement Planner

The Project FAR self-advancement planner is an advisory workflow for surfacing bounded historical status, research gaps, and possible next tasks. It must not alter accepted theory or evaluation conclusions and it is not a current-state authority.

## How the Planner Works

1. `tools/project_status_report.py` reads frozen W3.5-era registries and writes `docs/reports/project-status-generated.md` as an explicitly historical bounded-program snapshot.
2. `tools/detect_research_gaps.py` scans registries and documentation for unresolved, provisional, missing, stale, or underrepresented items, then writes `docs/reports/research-gap-report.md`.
3. `tools/generate_next_tasks.py` writes `docs/planning/next-actions.md` from the registered `POST-TERM-EVAL-001` workstreams. It does not infer a new research program from gap counts.
4. `tools/self_advancement_plan.py` runs the advisory generators and prints a concise summary.

Current project state is governed by `README.md`, `docs/project-status.md`, `docs/CANONICAL_MAP.md`, and the applicable governance artifacts. Generated planner output cannot override those sources or resolve a conflict between them.

## Gap Severity

- `critical`: candidate primitive failures or similar findings that require immediate human theory review.
- `high`: unresolved primitive pressure, missing reports referenced by registries, or stale current-release references.
- `medium`: underrepresented domains, low primitive coverage, conservative-extension clusters, unresolved cases, and provisional systems.
- `low`: TODO, TBD, unresolved, or future-work notes unless they block validation.

## Task Ordering

`docs/planning/next-actions.md` reflects the registered post-terminal workstream order. `PTE-W1-INDEPENDENT-REVIEW` is the canonical next workstream. Later post-terminal workstreams may be listed for visibility without being ready for immediate execution.

The planner must not invent a stronger deductive program, reopen the completed UPP queue, or convert a research gap into authorization for execution.

## Reviewing Maintainer Task Briefs

Before using a generated task brief, confirm that:

- the task is authorized by the current program or separately justified under the Research Execution Charter;
- the branch and affected files are appropriate;
- frozen evidence and protected theory remain protected;
- independence requirements are not satisfied by project-authored substitutes;
- validation commands match current repository tooling;
- the stop condition prevents unauthorized theory, evidence, or claim-status changes.

## Advisory Status

Planner output is advisory, not authoritative. It can contain false positives, stale references, or incomplete interpretations of evidence. Reviewers must compare recommendations against current canonical state and governance before execution.

## Avoiding Self-Reinforcing Errors

- Do not treat generated reports as evidence by themselves.
- Do not use the historical bounded-status report as current project status.
- Prefer current canonical registries, governance, and result disclosures over planner summaries.
- If canonical current-state surfaces disagree, surface the conflict instead of letting a generated report choose a winner.
- Review repeated recommendations for drift before copying them into new work.
- Keep generated task briefs constrained, falsifiable, and reversible.

**Warning:** Do not auto-merge planner-generated theory changes. All theory and claim-status changes remain subject to current governance and review requirements.
