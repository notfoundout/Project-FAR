# CRE-001 Deterministic Verifier

Status: Deterministic CRE-001 implementation merged at registered CRE-001 scope.

This directory contains the merged executable deterministic CRE-001 implementation: vocabulary-native compilation outputs, executable lowering, deterministic verification, replayable lowering traces, mutation testing, and adversarial compiler audit artifacts.

## Purpose

The verifier compares two machine-readable execution models:

1. `reference-model.json`, the registered CRE-001 reference behavior under explicit ambiguity policies;
2. a candidate model expressed in the same execution format.

It checks declarative structure and then explores paired reachable behavior. When enabled transitions or post-transition states diverge, it reports a shortest breadth-first counterexample trace within the configured depth bound.

## Files

- `reference-model.json`: Phase 1 reference execution model.
- `model-schema.json`: JSON Schema for the execution-model envelope.
- `fixtures/valid-candidate.json`: known-equivalent candidate fixture.
- `tools/cre001_verifier.py`: validator, executor, comparator, CLI, and report generator.
- `tests/test_cre001_deterministic_verifier.py`: valid and adversarial regression cases.

## Run

```bash
python tools/cre001_verifier.py \
  theory/evaluation/comparative-representation/experiments/CRE-001/deterministic-verifier/reference-model.json \
  theory/evaluation/comparative-representation/experiments/CRE-001/deterministic-verifier/fixtures/valid-candidate.json
```

Exit code `0` means the candidate matched every Phase 1 check. Exit code `1` means the report contains one or more diagnostics.

## Phase 1 checks

The verifier checks:

- variable and transition coverage;
- initial-value equality;
- transition guards, including disjunctive guards;
- transition updates;
- enabled-transition equality across reachable paired states;
- exact post-state and ordered-history equality;
- terminal condition and post-halt blocking policy;
- declared invariants;
- required output definitions;
- registered ambiguity-policy equality;
- shortest reachable counterexample traces for behavioral divergence.

## Registered ambiguity policies

The English scenario contains unresolved choices. Phase 1 does not conceal them. The reference model registers one policy for each so candidate results are conditional on the same policy:

- `disable_reject_repeatability = require_r_reject_active_before`;
- `prohibited_transition_output = executed_only`;
- `unterminated_output = finite_nonterminal_snapshot`.

Alternative policies require separate reference-model runs. A candidate cannot pass by silently selecting another interpretation.

## Nonclaims

A passing result establishes equivalence only to this finite CRE-001 execution model under the registered policies and verifier depth.

It does not establish:

- vocabulary sufficiency beyond the submitted compiled candidate;
- primitive necessity or minimality;
- evaluator reproducibility;
- comparative superiority;
- universality of FAR or any vocabulary.

The remaining limitation is semantic licensing: compiler-local compatibility checks and generated artifacts do not constitute independently frozen formal vocabulary semantics. Passing results do not establish universal sufficiency, primitive-only sufficiency, necessity, minimality, independence, superiority, a FAR proof, universal reasoning structure, or formally licensed vocabulary semantics.
