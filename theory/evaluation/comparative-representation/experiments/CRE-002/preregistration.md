# CRE-002 Preregistration

Version: CRE-002-PREREGISTRATION-1.0
Status: Frozen upon merge; not executed

## Research question

Under Vocabulary Semantics Baseline 1.0, can each official candidate vocabulary produce a fully traceable representation and executable lowering of CRE-002-SCENARIO-1.0 without introducing undeclared semantic commitments or an unrestricted hidden metalanguage?

## Primary hypotheses

- H-SCOPE: At least one vocabulary completes construction, trace replay, and behavioral verification under the frozen semantics baseline.
- H-REPRO: A vocabulary-level reproducibility claim requires three independently regenerated compiler runs with identical canonical outputs and source digests.
- H-BOUNDARY: Unsupported scenario commitments must produce explicit partial or unsupported results rather than silent wrapping or invented semantics.

No necessity, minimality, independence, or superiority hypothesis is tested by CRE-002.

## Inputs frozen before execution

1. Vocabulary Semantics Baseline 1.0 as merged before this package.
2. Official Vocabulary A, B, and C source definitions.
3. CRE-002 scenario and ambiguity policies.
4. Decision rules in `decision-rules.json`.
5. Compiler interface and trace requirements, but not vocabulary-specific CRE-002 encodings.

## Independence rule

Vocabulary-specific native constructs, lowering rules, and mappings must be authored only after this package is locked. The scenario and decision rules may not be edited in response to compiler failures. Any correction requires a new scenario version and invalidates prior execution attempts for confirmatory use.

## Required candidate artifacts

Each vocabulary must emit:

- source and semantic-baseline checksums;
- vocabulary-native representation;
- declared derived machinery and payload types;
- executable lowering rules;
- atomic lowering trace;
- trace-replay report;
- generated execution model;
- verifier report;
- compiler-boundary report;
- mutation-test report;
- limitation and unsupported-element report.

## Primary outcomes

For each vocabulary:

- construction status: complete, partial, unsupported, or error;
- semantic-licensing status for every native role;
- embedded-metalanguage classification;
- trace replay status;
- behavioral verification status;
- shortest counterexample if verification fails;
- unsupported commitment list;
- ambiguity-policy dependence;
- deterministic regeneration status.

## Analysis rule

Results are reported per vocabulary. No ranking is produced unless all compared encodings satisfy the same preservation requirements and a separately frozen complexity policy exists. Passing behavioral verification is insufficient if semantic licensing or trace replay fails.

## Stopping rule

Execution stops for a vocabulary when a required scenario commitment cannot be represented under the frozen baseline without adding undeclared semantics. The result must be `partial` or `unsupported`; the package must not be weakened to force completion.

## Nonclaims

No result from CRE-002 alone establishes universal sufficiency, primitive-only sufficiency, necessity, minimality, independence, superiority, FAR, or universal reasoning structure.
