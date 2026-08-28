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
