# CRE-002 Prospective Vocabulary Comparison

## Scope

This report records the first prospective execution governed by Vocabulary Semantics Baseline 1.0. It is limited to the frozen bounded CRE-002 scenario and decision rules.

## Results

| Vocabulary | Outcome | States | Edges | Counterexample |
|---|---:|---:|---:|---|
| CRE-001-VOCAB-A-1.0 | complete | 73 | 72 | none |
| CRE-001-VOCAB-B-1.0 | complete | 73 | 72 | none |
| CRE-001-VOCAB-C-1.0 | complete | 73 | 72 | none |

## Vocabulary-level decision

- Existential complete condition: `true`
- Reproducible complete condition: `true`
- Ranking permitted: `false`

## Supported conclusions

- Each reported complete outcome passed all frozen CRE-002 complete gates for the bounded scenario.
- The results are prospective relative to Vocabulary Semantics Baseline 1.0.
- Behavioral equivalence, where reported, is limited to the full bounded CRE-002 state space and registered policies.

## Unsupported conclusions

- universal sufficiency
- primitive-only sufficiency
- necessity
- minimality
- independence
- superiority
- FAR proof
- universal structure of reasoning
- adequacy outside the frozen CRE-002 scenario
- unbounded concurrency
- unbounded higher-order modification
- global vocabulary ranking
