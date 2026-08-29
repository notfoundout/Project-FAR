# Branch and PR triage

[`branch_pr_triage.py`](../../tools/branch_pr_triage.py) produces a machine-readable,
non-destructive inventory. It classifies each branch as active, merged, superseded, frozen
evidence, unique unmerged evidence, abandoned/divergent, or unknown.

Every input record must carry an exact head and a computed unique-commit count (or explicit
`null` when unavailable). Any unique commits override a nominal superseded classification and
force `unique unmerged evidence`. Unknown evidence remains retained. The report always records
`deletion_authorized: false` and never invokes branch or PR deletion APIs.

Local mode computes commits and paths reachable from each local branch but not the base. A
GitHub snapshot may add PR disposition, explicit frozen-evidence status, and a named successor.
The generated report is a cleanup plan only. Destructive pruning requires a later governed
decision and a fresh evidence-safety check.

For a governed remote snapshot, use `--output` to write the deterministic report and `--check`
to fail on drift. A summary may disclose the full observed branch count while supplying exact
heads/unique-commit comparisons only for the subset the GitHub interface could classify. Every
unclassified branch remains retained; a name or apparent age is never deletion evidence.

## Current governed snapshot

The 2026-08-28 [snapshot](../../artifacts/governance/live-branch-pr-snapshot-v1.0.json)
and generated [triage report](../../artifacts/governance/branch-pr-triage-v1.0.json) observed
415 remote branches. Bulk GitHub branch search did not expose enough head/PR/compare data to
classify 412 of them, so all 412 remain retained. Eighty-two evidence-sensitive names are
signals for review, not deletion or freeze classifications.

Three exact comparisons are classified: the W1 branch is frozen evidence; the active W2
integration branch is retained under PR #458; and PR #452's branch has seven unique unmerged
commits, is retained as evidence, and is superseded by #458. Closing #452 did not delete its
branch or any evidence. No destructive action is authorized by the report.
