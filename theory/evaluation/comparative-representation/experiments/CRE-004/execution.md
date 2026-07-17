# CRE-004 Execution and Replay Pipeline

## Status

Infrastructure only. This document does not report an execution or scientific result.

## Purpose

The pipeline validates preserved evaluator responses against the frozen CRE-004 protocol, applies the registered scorer, and generates deterministic machine-readable outputs. It refuses to operate when a pinned protocol artifact differs from the version merged in PR #205.

## Separation of stages

1. PR #205 froze the evaluator-facing protocol.
2. This PR implements response validation, scoring, aggregation, and replay.
3. A later execution PR may add actual evaluator records and generated outputs.

No benchmark response belongs in this infrastructure PR.

## Frozen inputs

`protocol_lock.json` pins the following files by Git blob SHA-1:

- `preregistration.json`
- `response.schema.json`
- `scoring.py`
- `evaluator_packet.md`

A mismatch is fatal. Changing any pinned artifact requires a new protocol version rather than silently updating the lock during an active execution.

## Execution manifest

Create an execution-specific manifest from `execution_manifest.template.json`. Before evaluator exposure, replace all placeholders and freeze:

- execution identifier;
- protocol version;
- randomization seed;
- complete allowed case-label set;
- complete allowed candidate-label set;
- complete evaluator registry;
- calibration status for every evaluator;
- independence claim for each evaluator.

The pipeline rejects evaluators whose calibration status is not exactly `true`.

## Raw responses

Store one append-only JSON object per file. Each object must conform to the frozen response fields. A response is uniquely identified for execution purposes by:

`(evaluator_id, case_label, candidate_label)`

Duplicate tuples are rejected. Corrections must be preserved as separate superseding records under a later, explicitly versioned procedure; raw files must never be overwritten or deleted.

## Replay command

From the repository root:

```bash
python theory/evaluation/comparative-representation/experiments/CRE-004/execution_pipeline.py \
  path/to/execution_manifest.json \
  path/to/raw_responses \
  path/to/generated_outputs
```

The output directory contains:

- `results.csv` — one deterministic scored row per validated response;
- `summary.json` — aggregate classifications and hidden-reintroduction counts.

Running the same code against byte-identical inputs must produce byte-identical outputs.

## Rejection conditions

Execution stops on:

- a protocol-lock mismatch;
- missing, extra, or invalid response fields;
- an ineligible or uncalibrated evaluator;
- an unregistered case or candidate label;
- a duplicate evaluator/case/candidate response;
- an invalid frozen scoring response;
- malformed execution-manifest data.

Rejected records are not silently discarded. A later execution report must preserve and disclose every rejected input and the reason for rejection.

## Claim boundary

This pipeline creates no evidence by itself. It does not establish successful discrimination, primitive necessity, minimality, universality, or external replication. Those claims depend on later preserved responses, deterministic outputs, and the actual independence of the evaluators and adjudication process.
