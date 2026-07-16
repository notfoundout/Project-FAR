# CRE-002-EXT-001-REP-001 Preregistration

## Research question

Can isolated implementation teams, using only the frozen CRE-002-EXT-001 scientific package, Vocabulary Semantics Baseline 1.1, and this replication protocol, independently construct vocabulary-native encodings whose lowered bounded behavior matches the registered reference behavior?

## Units

The unit of evaluation is one team-produced candidate implementation for one official vocabulary. A team may implement only one vocabulary unless separate personnel, repositories, credentials, and communication channels are used for each implementation.

## Minimum replication set

A valid replication requires:

- at least two eligible implementation teams;
- at least one implementation for each official vocabulary;
- at least one independently implemented verifier maintained by personnel who did not build any candidate implementation;
- frozen submissions and provenance attestations before reference comparison.

## Materials visible to implementation teams

Teams may access only:

- frozen CRE-002-EXT-001 preregistration files;
- frozen scenario, ambiguity policies, decision rules, and output schema;
- Vocabulary Semantics Baseline 1.1;
- official vocabulary definitions;
- neutral submission schemas and conformance tests that reveal no parent implementation details.

## Prohibited exposure before submission freeze

Teams may not access:

- `tools/cre002_execute.py` or equivalent parent execution source;
- parent native representations, lowering traces, generated models, mutation reports, or comparison outputs;
- candidate-specific construction rules extracted from parent generated artifacts beyond the frozen Baseline 1.1 text;
- parent verifier internals or hidden expected state/edge digests;
- communications from prior implementers describing their encoding choices.

Any material prohibited exposure makes the affected submission contaminated and ineligible for the primary replication result.

## Blinding

Implementation teams receive anonymous vocabulary labels where operationally feasible. They receive no parent candidate outcomes, state counts, edge counts, terminal counts, digests, counterexamples, or ranking claims. The independent verifier team receives frozen candidate submissions only after all submissions are locked.

## Submission freeze

Each submission must include source, dependency lock, build instructions, native artifact, lowering trace, generated execution model, test output, provenance record, and SHA-256 manifest. Once submitted, no scientific file may change. Corrections require a separately labeled corrected submission and cannot silently replace the original.

## Verification

The independent verifier must reconstruct the bounded reference behavior from the frozen scenario and policies without importing the parent reference model or parent verifier code. It must check semantic licensing, native construction completeness, replay, behavior, required outputs, deterministic regeneration, mutation sensitivity, and contamination status.

## Primary decision rule

Replication succeeds only if:

1. every official vocabulary has at least one eligible uncontaminated submission;
2. every counted submission passes all required gates;
3. the independent verifier reproduces the registered bounded reference behavior;
4. no unresolved material discrepancy remains between candidate output, verifier output, and the frozen package;
5. provenance and isolation audits pass.

Otherwise the result is classified according to `decision-rules.json` as partial, failed, contaminated, or inconclusive.

## Analysis policy

Report every submission, including divergent and contaminated submissions. Do not discard inconvenient results. Primary aggregation uses only eligible uncontaminated submissions; all exclusions must be enumerated with reasons.

## Claim boundary

A successful result would establish independent replication only for the registered bounded scenario, Baseline 1.1, explicit derived machinery, frozen policies, and tested implementations. It would not establish universal or primitive-only sufficiency, necessity, minimality, primitive independence, superiority, FAR proof, or universal reasoning structure.