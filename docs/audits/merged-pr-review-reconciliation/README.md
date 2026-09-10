# Merged-PR review residual reconciliation

Status: Audit

This directory reconciles every finding classified `resolved_incorrectly` in the frozen
merged-PR review classification against main commit
`5ca27d5c40281771cf74aa29704c2a06868a16ae`. The reconciliation commit itself changes
only this machinery and its generated audit surfaces; it does not repair residual
findings.

`disposition-ledger.json` is authoritative. `RECONCILIATION_REPORT.md` is its complete
human-readable rendering. `RESIDUAL_REMEDIATION_QUEUE.md` contains only
`still_reproducible` and `cannot_verify` records. `REMEDIATION_BATCHES.md` groups records
only when a decision supplies a demonstrated shared `root_cause_id`; otherwise every
finding retains a unique group and its own remediation boundary.

The policy is fail-closed:

- a finding without current-main reproduction, comparison, fix, obsolescence, or
  supersession evidence is `cannot_verify`;
- baseline evidence is never reused to justify a new definitive disposition;
- `still_reproducible` requires disposition-specific evidence and a verified root-cause
  mechanism;
- a shared file path is not treated as a shared root cause.

Regenerate the artifacts with:

```bash
python tools/reconcile_merged_pr_review_findings.py \
  --baseline docs/audits/merged-pr-review-classification/findings.json \
  --decisions docs/audits/merged-pr-review-reconciliation/reconciliation-decisions.json \
  --output-dir docs/audits/merged-pr-review-reconciliation
```

Use `--check` for a read-only deterministic validation. A nonzero residual count is an
active verification or remediation state and must not be described as a clear queue.

The [2026-09-10 internal assurance audit](../../../research/internal-assurance-2026-09-10/README.md)
records fresh reproductions, unprotected repairs, and the blocked protected-validator
candidate. It does not declare the residual queue clear.
