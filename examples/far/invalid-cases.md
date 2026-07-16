# Invalid FAR Grammar Cases

These fragments are intentionally invalid and are covered by `tests/test_formal_semantics_and_grammar.py`.

1. Unknown top-level field: a conforming parser rejects `extra: true`.
2. Empty representation set: `representations: []` is invalid because a FAR object must contain at least one representation.
3. Unknown record field: misspelled or undeclared fields inside representations, relations, interpretations, rules, or transitions are rejected.
4. Noninteger transition order: quoted numbers and booleans are rejected.
5. Dangling references: relation endpoints, interpretation targets, rule inputs/outputs, and transition rules must resolve.
6. Duplicate IDs or transition orders are invalid.
7. Empty investigation, IDs, kinds, meanings, rule outputs, and transition endpoints are invalid.

The negative cases are generated in temporary files so repository-wide discovery can continue treating every checked-in `*.far.yaml` file as expected-valid input.
