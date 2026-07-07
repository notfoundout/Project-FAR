# Maintaining the Self-Advancement Planner

The Project FAR self-advancement planner is an advisory workflow for surfacing repository status, research gaps, and possible next tasks. It must not alter accepted theory or evaluation conclusions.

## How the Planner Works

1. `tools/project_status_report.py` reads selected registries and reports, then writes `docs/reports/project-status-generated.md`.
2. `tools/detect_research_gaps.py` scans registries and documentation for unresolved, provisional, missing, stale, or underrepresented items, then writes `docs/reports/research-gap-report.md`.
3. `tools/generate_next_tasks.py` turns the gap report into ranked advisory tasks and ready-to-copy Codex prompts in `docs/planning/next-actions.md`.
4. `tools/self_advancement_plan.py` runs all three tools and prints a concise summary.

## Gap Severity

- `critical`: candidate primitive failures or similar findings that require immediate human theory review.
- `high`: unresolved primitive pressure, missing reports referenced by registries, or stale latest-release references.
- `medium`: underrepresented domains, low primitive coverage, conservative-extension clusters, unresolved cases, and provisional systems.
- `low`: TODO, TBD, unresolved, or future-work notes unless they block validation.

## Task Ranking

Tasks are ranked by severity first, then by gap identifier. The generator intentionally keeps recommendations cautious and scoped to review, documentation, or planning unless a human authorizes more.

## Reviewing Codex Prompts

Before using a generated prompt, confirm that:

- The branch and allowed files are appropriate.
- Forbidden theory files remain protected.
- Validation commands match current repository tooling.
- The stop condition prevents unauthorized theory changes.

## Advisory Status

Planner output is advisory, not authoritative. It can contain false positives, stale references, or incomplete interpretations of evidence. Human reviewers must compare recommendations against the registries, reports, and governance charter.

## Avoiding Self-Reinforcing Errors

- Do not treat generated reports as evidence by themselves.
- Prefer registry and report sources over planner summaries.
- Review repeated recommendations for drift before copying them into new work.
- Keep generated prompts constrained and reversible.

**Warning:** Do not auto-merge planner-generated theory changes. All theory changes require human review.
