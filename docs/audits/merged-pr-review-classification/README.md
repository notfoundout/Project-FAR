# Merged-PR review classification

This directory contains the deterministic classification layer applied to the frozen authenticated review inventory in `docs/audits/merged-pr-review-audit/`.

## Decision rule

The classifier is fail-closed:

- an open GitHub review thread is classified `unresolved`;
- an empty review comment is classified `non_actionable`;
- a resolved or outdated thread is classified `uncertain_manual_review_required` unless a manual evidence decision establishes a stronger disposition;
- GitHub's resolved flag is never treated as proof that a concern was fixed correctly;
- GitHub's outdated flag is never treated as proof that a concern became obsolete.

Definitive dispositions—`resolved_correctly`, `resolved_incorrectly`, and `obsolete_after_later_changes`—require a decision in `manual-decisions.json` containing concrete evidence and a rationale. Overrides that omit those fields fail validation.

## Outputs

`findings.json` is the machine-readable audit record. `FINDINGS.md` is the human-readable rendering. Both are generated from the same source inventory and decision registry.

Each finding records the PR number, thread and comment identifiers, path and line where available, original reviewer claim, GitHub metadata, disposition, confidence, rationale, and evidence.

The JSON preserves the original reviewer body exactly. The Markdown report renders that body as inert single-line text: embedded images, links, HTML tags, and code delimiters are removed before truncation so untrusted review syntax cannot create broken report links.

## Reproduction

```bash
python tools/classify_merged_pr_review_findings.py \
  --threads docs/audits/merged-pr-review-audit/raw-review-threads.json \
  --overrides docs/audits/merged-pr-review-classification/manual-decisions.json \
  --json-output docs/audits/merged-pr-review-classification/findings.json \
  --markdown-output docs/audits/merged-pr-review-classification/FINDINGS.md
```

Run tests with:

```bash
python -m unittest tests/test_classify_merged_pr_review_findings.py
```

Classification and remediation remain separate. This stage records evidence and triage only; it does not edit the files implicated by review findings.
