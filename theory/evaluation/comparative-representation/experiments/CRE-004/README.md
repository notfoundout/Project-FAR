# CRE-004 — Blind Discrimination Protocol

## Status

Preregistered and frozen before evaluator execution.

## Purpose

CRE-004 tests whether a frozen candidate translation preserves a preregistered difference between two reasoning systems. It replaces open-ended mapping construction with a minimal, plain-language discrimination task that can be completed by a qualified human or AI evaluator.

The evaluator does not select preservation scores, count representation complexity, or decide whether a candidate is sufficient. The evaluator answers observable multiple-choice questions. Deterministic rules derive the protocol result.

## Core question

> Two systems differ in one frozen commitment. After translation into a candidate vocabulary, can the evaluator still distinguish them?

## Evaluator workflow

For each randomized and anonymized case, the evaluator receives:

1. System A and System B;
2. a statement that the source pair contains exactly one intended difference;
3. the candidate translation of each system;
4. the frozen candidate vocabulary card.

The evaluator answers:

1. **Are the source systems different?** — `yes`, `no`, or `cannot_determine`.
2. **Can the translated systems still be distinguished?** — `yes`, `no`, or `cannot_determine`.
3. If distinguishable, **what observable function carries the difference?** — one or more plain-language function labels.
4. If `other` is selected, **does that mechanism perform one of the five registered functions?**
5. **How certain is the evaluator?** — `certain`, `likely`, or `unsure`.

The interface does not expose the terms FAR, Representation, Representational Structure, Interpretation, Investigation, or Reasoning Calculus.

## Plain-language function labels

- `stores_objects` — stores the explicit objects being reasoned about;
- `organizes_objects` — determines how those objects are arranged or related;
- `assigns_meaning` — assigns denotation or meaning;
- `defines_objective` — defines the question, objective, or success condition;
- `determines_permitted_steps` — determines which inferences or transitions are allowed;
- `other` — another visible mechanism;
- `cannot_determine` — the evaluator cannot identify the mechanism.

These labels are mapped internally to the registered FAR commitments only after response capture.

## Deterministic scoring

- Source difference `yes` and translated distinction `yes` produces `pass`.
- Source difference `yes` and translated distinction `no` produces `fail`.
- Any required `cannot_determine` produces `unknown`.
- Source difference `no` produces `invalid_case_response`, because benchmark validity is frozen independently of candidate performance.
- Selecting `other` and then identifying one of the five registered functions produces `hidden_reintroduction = true`.
- Confidence never changes the score.

The evaluator cannot directly choose `pass`, `fail`, `unknown`, hidden reintroduction, sufficiency, dominance, or complexity values.

## Complexity

`A_used`, `A_required`, `D`, `O`, and `L` are computed from the frozen candidate translations by a separate mechanical representation audit. They are not estimated by the discrimination evaluator.

## Blinding and execution controls

- candidate identities use randomized opaque labels;
- case and candidate order are randomized from a recorded seed;
- vocabulary cards contain no candidate names, FAR terminology, repository paths, or author-identifying metadata;
- evaluators cannot access answer keys or other evaluator responses;
- responses are append-only after submission;
- the same JSON response schema is used for humans and AI agents;
- no candidate vocabulary or translation may be repaired after exposure to benchmark cases.

## Use with CRE-003

CRE-004 does not replace or revise CRE-003. CRE-003 established the frozen matched cases and the richer construction-based evaluation. CRE-004 defines a lower-discretion external verification layer for already frozen translations.

The first execution should use blinded translations derived from CRE-003 and must be frozen in a separate PR before evaluator recruitment or agent execution.

## Claim boundary

A successful CRE-004 execution demonstrates only that the tested candidate translations preserved the preregistered distinctions in the tested cases under this decision protocol.

It does not establish:

- unrestricted primitive necessity;
- closure of the alternative-vocabulary search;
- global minimality;
- unique optimality;
- universal reasoning coverage;
- external replication unless the evaluators and adjudication process are genuinely independent of Project FAR development.

## Artifacts

- `preregistration.json` — frozen decision tree, response choices, blinding rules, and claim boundary;
- `response.schema.json` — shared machine-readable response format for humans and AI agents;
- `scoring.py` — deterministic response scorer;
- `evaluator_packet.md` — frozen plain-language evaluator instructions and eligibility rules;
- `decision_tree.md` — human-readable normative classification tree;
- `automatic_scoring.md` — input, output, aggregation, and immutability rules;
- `hidden_reintroduction.md` — frozen functional-equivalence test;
- `calibration_cases.json` — unrelated evaluator eligibility calibration;
- `tests/test_cre004_protocol.py` — protocol, scoring, blinding, and claim-boundary tests;
- `tests/test_cre004_evaluator_package.py` — evaluator-package, calibration, and immutability tests.
