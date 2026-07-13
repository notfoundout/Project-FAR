# CRE-001 Calibration Exercise v1.0

Status: Frozen calibration package; not experimental data
Calibration identifier: CRE-001-CALIBRATION-1.0
Experiment: CRE-001
Protocol: CRP-1.0

## Separation from Experimental Dataset

This calibration is unrelated to Project FAR and uses a different scenario. Calibration responses and scores are evaluator-eligibility records only. They must never be included in the CRE-001 mapping dataset, CIR dataset, adjudication dataset, ablation dataset, or comparative-result dataset.

## Calibration Scenario: Library Hold Queue

A library has patrons, books, holds, checkout status, and queue rules. The system begins with two patrons (`Patron-1`, `Patron-2`) and one book (`Book-X`). `Patron-1` has priority hold position 1. `Patron-2` has priority hold position 2. `Book-X` is available, not checked out, and has an empty checkout history.

Rules:

1. If a book is available and the hold queue is nonempty, the first patron in the queue may check out the book.
2. Checking out the book sets `available=false`, sets `checked_out_to` to the patron, removes that patron from the queue, and appends a checkout event to history.
3. If the book is checked out, no other patron may check it out.
4. A queue-adjustment rule may move a patron one position forward only if the preceding patron has become ineligible.
5. A return transition sets `available=true`, clears `checked_out_to`, and appends a return event to history.
6. The process stops after one successful checkout followed by one return.

## Calibration Task

Produce a compact structured representation that identifies entities, relations, state variables, permitted transitions, prohibited transitions, rule modification or queue adjustment behavior, dependency history, and fixed output format.

## Required Output Format

The response must contain these sections:

1. entities;
2. relations;
3. state variables;
4. permitted transitions;
5. prohibited transitions;
6. rule modification or queue adjustment behavior;
7. dependency history;
8. final observable output.

## Scoring Rubric

Score each dimension as `Pass` or `Fail`:

- entities identified correctly;
- relations identified correctly;
- state variables identified correctly;
- transitions identified correctly;
- prohibited transitions identified correctly;
- queue-adjustment behavior represented correctly;
- dependency history preserved;
- fixed output format followed.

## Passing Criteria

An evaluator passes calibration only if all eight rubric dimensions receive `Pass`. Calibration failure excludes evaluator participation before assignment. Calibration scoring does not rank evaluators and does not become experimental evidence.
