# CRE-004 Automatic Scoring Specification

`scoring.py` is the normative implementation of the frozen decision tree.

## Inputs

Each response must validate against `response.schema.json`. Invalid or missing required fields are rejected before scientific classification.

## Outputs

Each accepted response produces:

- `classification`: `pass`, `fail`, `unknown`, or `invalid_case_response`;
- `hidden_reintroduction`: `true`, `false`, or `unknown`;
- the unchanged evaluator confidence value as metadata;
- deterministic reasons derived from the submitted fields.

## Aggregation

Results must be reported at response, evaluator, case, candidate, and overall levels. Raw response distributions are retained. `Unknown` is not mechanically ordered between `Partial` and `Fail`, and no unresolved response may be converted into a failure or success by majority vote.

A candidate has existential discrimination support only when at least one eligible evaluator returns `pass` for every required case without invalid responses. Reproducible discrimination support requires every preregistered eligible evaluator to do so.

Hidden reintroduction is reported separately from preservation. A translated distinction can pass while also reconstructing a removed registered function.

## Immutability

The scoring code, schema, function labels, aggregation rules, evaluator count, candidate set, case set, and randomization seed must be frozen before benchmark exposure. Any change after exposure creates a new protocol version rather than modifying CRE-004.