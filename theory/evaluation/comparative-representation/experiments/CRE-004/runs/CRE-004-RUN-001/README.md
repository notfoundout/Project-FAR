# CRE-004 RUN-001 — Execution Intake

## Status

Execution intake opened after the CRE-004 evaluator package and execution/replay pipeline were merged.

No evaluator response, benchmark score, or scientific result is recorded here yet.

## Frozen scope

RUN-001 uses the four matched cases inherited from CRE-003:

- `CRE-003-I`
- `CRE-003-G`
- `CRE-003-C`
- `CRE-003-R`

It reserves ten opaque candidate labels:

- `CANDIDATE_001` through `CANDIDATE_010`

It reserves three evaluator slots:

- `EVALUATOR_001`
- `EVALUATOR_002`
- `EVALUATOR_003`

The candidate-to-vocabulary key must not be placed in an evaluator-visible artifact. Evaluators must not receive benchmark cases until they pass the unrelated calibration exercise.

## Required gates before response capture

1. Freeze the anonymized candidate translations and vocabulary cards.
2. Freeze the candidate-label key in a non-evaluator-facing provenance artifact.
3. Register three eligible evaluators and preserve their calibration outcomes.
4. Record evaluator independence claims without overstating external independence.
5. Freeze the randomization seed and generated assignment order.
6. Verify the protocol lock against the merged CRE-004 artifacts.
7. Confirm every response channel preserves append-only records and correction links.

## Execution rule

The execution pipeline must reject scoring while any gate remains incomplete. No missing evaluator judgment may be inferred, simulated, backfilled, or replaced with an author-generated answer.

## Expected later artifacts

After all gates are satisfied, this directory may contain:

- `execution_manifest.json`
- anonymized assignment packages
- append-only raw response records
- rejection records, if any
- deterministic `results.csv`
- deterministic `summary.json`
- a bounded execution report

## Claim boundary

Opening this intake does not constitute execution evidence. A later result applies only to the frozen candidates, cases, evaluators, and translations actually recorded for RUN-001.