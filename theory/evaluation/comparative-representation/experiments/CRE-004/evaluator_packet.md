# CRE-004 Evaluator Packet

## Scope

This packet is the frozen evaluator-facing procedure for CRE-004. Evaluators do not construct mappings, assign preservation scores, compare complexity, or decide whether FAR is sufficient.

## Eligibility

An evaluator must:

- be able to read formal or semi-formal system descriptions;
- understand basic state-transition or rule-based reasoning descriptions;
- have had no role in creating the candidate vocabularies or benchmark translations;
- have no access to other evaluator responses or the answer key;
- pass the unrelated calibration exercise before receiving benchmark cases.

## Instructions

For each anonymized case, read:

1. Source System A;
2. Source System B;
3. Candidate Translation A;
4. Candidate Translation B;
5. the anonymized vocabulary card.

Then answer only the fields allowed by `response.schema.json`.

### Question 1

Are Source System A and Source System B different in the stated respect?

- `yes`
- `no`
- `cannot_determine`

### Question 2

After translation, can Candidate Translation A and Candidate Translation B still be distinguished in that respect?

- `yes`
- `no`
- `cannot_determine`

### Question 3

If the translated systems remain distinguishable, what visible function carries the distinction?

- `stores_objects`
- `organizes_objects`
- `assigns_meaning`
- `defines_objective`
- `determines_permitted_steps`
- `other`
- `cannot_determine`

Multiple visible functions may be selected only when each is independently present in the translation.

### Question 4

If `other` is selected, does that mechanism perform one of the five listed functions?

- one of the five function labels;
- `none`;
- `cannot_determine`.

### Question 5

Confidence:

- `certain`
- `likely`
- `unsure`

Confidence is metadata only and never alters scoring.

## Prohibitions

Evaluators must not:

- infer candidate identity;
- use FAR terminology in submitted answers;
- repair or improve a translation;
- consult repository history, author notes, answer keys, or other evaluators;
- choose `pass`, `fail`, `unknown`, sufficiency, dominance, or hidden reintroduction directly.

## Submission

Responses are append-only after submission. Any correction requires a new response record linked to the superseded record; the original remains preserved.