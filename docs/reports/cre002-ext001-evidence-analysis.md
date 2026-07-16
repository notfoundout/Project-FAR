# CRE-002-EXT-001 Evidence Analysis

## Status

CRE-002-EXT-001 is complete as a prospective, checksum-locked, bounded comparative execution under Vocabulary Semantics Baseline 1.1.

This analysis integrates the recorded execution artifacts. It does not alter the frozen preregistration, scenario, ambiguity policies, decision rules, output schema, Baseline 1.1, or the original CRE-002 result.

Integration provenance: this report is derived from the committed comparison and execution artifacts and introduces no new candidate computation or adjudication.

## Recorded result

All three official candidate vocabularies received the preregistered outcome `complete`:

| Vocabulary | Licensing | Native construction | Trace replay | Behavioral verification | Output preservation | Deterministic regeneration | Mutation suite | Outcome |
|---|---|---|---|---|---|---|---|---|
| CRE-001-VOCAB-A-1.0 | pass | complete | pass | pass | pass | pass | pass | complete |
| CRE-001-VOCAB-B-1.0 | pass | complete | pass | pass | pass | pass | pass | complete |
| CRE-001-VOCAB-C-1.0 | pass | complete | pass | pass | pass | pass | pass | complete |

The registered bounded reference graph contains 73 states, 72 edges, and 26 terminal states. Of the terminal states, 20 terminate by containment and 6 by deadlock. No candidate produced a shortest counterexample within the registered state space.

All candidates depended on ambiguity policies AP-001 through AP-009 and used the five Baseline 1.1 derived constructs:

- `D_nondeterminism`;
- `D_concurrency`;
- `D_priority`;
- `D_provenance`;
- `D_rule_modification`.

## Supported conclusion

Under Vocabulary Semantics Baseline 1.1, the frozen CRE-002-EXT-001 scenario, the nine registered ambiguity policies, the bounded state-space definition, and the compiler/verifier implementation recorded in the repository, each official candidate vocabulary supported a licensed vocabulary-native construction whose lowered behavior reproduced the complete registered reference graph and required outputs.

This is a scenario-bounded comparative result for **primitive vocabulary plus explicitly licensed derived machinery**. It is stronger than the original CRE-002 result only in the separately labeled extension because Baseline 1.1 supplied the five capabilities that Baseline 1.0 did not license.

## Relationship to original CRE-002

The original CRE-002 result remains unchanged:

- all three candidates are `unsupported` under Baseline 1.0;
- native compilation was not authorized there;
- the result established a semantic-licensing boundary, not vocabulary incapacity.

CRE-002-EXT-001 does not retroactively convert the original result into success. The two records answer different questions under different frozen semantic baselines.

## What the result does not distinguish

Because all three candidates passed every registered gate and produced the same bounded behavior, CRE-002-EXT-001 provides no ranking among them. It does not show that any vocabulary is simpler, more natural, less costly, more explanatory, or more fundamental.

The result also does not isolate whether success came primarily from the primitive categories or from the five licensed derived constructs. Primitive-only sufficiency remains unsupported.

## Remaining methodological dependencies

The result remains dependent on:

1. the bounded scenario and finite state space;
2. the nine frozen ambiguity policies;
3. Baseline 1.1's compiler-facing construction rules;
4. the correctness and independence of the compiler, lowerers, replay checker, reference explorer, verifier, and mutation suite;
5. compiler-authored native encodings rather than independently produced encodings;
6. the selected output schema and equivalence criteria.

Mutation detection establishes sensitivity to the five registered construct classes. It does not prove sensitivity to every possible semantic defect.

## Exact nonclaims

CRE-002-EXT-001 does not establish:

- universal sufficiency;
- primitive-only sufficiency;
- necessity;
- minimality;
- independence;
- superiority or ranking;
- a proof of FAR;
- a universal structure of reasoning;
- adequacy outside the registered bounded scenario class;
- independent replication;
- human-independent or compiler-independent construction validity.

## Evidence assessment

The correct repository-level interpretation is:

- CRE-001: retrospective deterministic evidence under compiler-authored declared interpretations;
- CRE-002: prospective semantic-licensing failure under Baseline 1.0;
- CRE-002-EXT-001: prospective bounded behavioral success under Baseline 1.1 with explicit derived machinery;
- next evidential requirement: independent replication with isolated encoders or compiler implementations.

No additional same-pipeline scenario can substitute for that independence requirement. Further same-pipeline experiments may test boundaries, but they will not independently replicate the current result.
