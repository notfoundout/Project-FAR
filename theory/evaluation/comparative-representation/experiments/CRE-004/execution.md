# CRE-004 Execution and Replay

This package records and replays evaluator responses. It does not generate evaluator judgments and contains no benchmark results.

## Pre-exposure corrections

Before any evaluator response was recorded, two inconsistencies in the merged evaluator package were corrected:

1. `decision_tree.md` now uses the schema field `translated_difference`.
2. `scoring.py` now reports unresolved hidden reintroduction as `unknown`, matching the frozen written rule.

The response schema also permits an optional `supersedes_record_id` so corrections can preserve the original append-only record as required by the evaluator packet.

## Commands

From the repository root:

```bash
python theory/evaluation/comparative-representation/experiments/CRE-004/execution.py manifest
python theory/evaluation/comparative-representation/experiments/CRE-004/execution.py validate path/to/response.json
python theory/evaluation/comparative-representation/experiments/CRE-004/execution.py append path/to/response.json
python theory/evaluation/comparative-representation/experiments/CRE-004/execution.py replay
```

## Controls

- Every record contains hashes of all normative protocol files.
- The record identifier commits to both the response and protocol manifest.
- Exact duplicate submissions are rejected.
- Corrections append a new record linked through `supersedes_record_id`; originals are never deleted.
- Replay rejects altered responses, altered scores, duplicate record identifiers, unknown supersession links, and protocol-manifest drift.
- Generated reports retain response distributions by evaluator, case, candidate, and overall result.
- `unknown` is retained as its own outcome and is never converted by majority vote.

## Generated and execution-only artifacts

The following artifacts must not be populated until genuine evaluator submissions exist:

- `responses.jsonl`
- `results.generated.json`

Their absence means CRE-004 has not been executed.

## Claim boundary

Successful replay establishes deterministic internal implementation reproducibility for the preserved records. It does not establish evaluator independence, external replication, global minimality, unique optimality, or universal reasoning coverage.
