# PIE-001 — Bounded Primitive Independence Execution

## Status

Completed bounded internal execution. Scientific conclusion: unresolved.

## Purpose

PIE-001 applies every mandatory reduction test in the Primitive Independence Framework to each of the five current Project FAR primitives:

- Investigation
- Representation
- Representational Structure
- Interpretation
- Reasoning Calculus

The execution records 25 attempts: five tests for each primitive.

## Execution boundary

This is a repository-internal analytic challenge run. It is not a blinded or independent evaluator study.

The run uses:

- the canonical definitions in `theory/definitions/definitions.md`;
- the current axioms in `theory/axioms/axioms.md`;
- the preservation commitments defined by the Primitive Independence Framework;
- existing explicit state-transition and representation-preservation examples as the bounded benchmark basis.

It does not use independent evaluators, independently proposed substitute vocabularies, or a completed global alternative-vocabulary search.

## Results

| Result | Count |
|---|---:|
| Mandatory attempts recorded | 25 |
| Reduction attempts that exposed a preservation failure or hidden reintroduction | 15 |
| Derivability or substitution attempts not completed | 10 |
| Successful admissible reductions | 0 |
| Primitive independence failures established | 0 |
| Primitive independence claims established | 0 |

The elimination, merger, and recovery attempts produced bounded negative results for every primitive. In each case, at least one required commitment was lost or the removed primitive was reconstructed through commitment-equivalent machinery.

The derivability and substitution tests remain incomplete because no total non-circular derivation or independently specified non-equivalent substitute was constructed and frozen before mapping.

## Per-primitive decisions

| Primitive | Decision | Reason |
|---|---|---|
| Investigation | Unresolved | Elimination, merger, and recovery failed; derivability and substitution remain incomplete. |
| Representation | Unresolved | Elimination, merger, and recovery failed; derivability and substitution remain incomplete. |
| Representational Structure | Unresolved | Elimination, merger, and recovery failed; derivability and substitution remain incomplete. |
| Interpretation | Unresolved | Elimination, merger, and recovery failed; derivability and substitution remain incomplete. |
| Reasoning Calculus | Unresolved | Elimination, merger, and recovery failed; derivability and substitution remain incomplete. |

Architecture-level decision: **unresolved**.

## Interpretation

PIE-001 provides evidence that simple deletion, packaging mergers, and unrestricted reconstruction do not reduce the current five-primitive vocabulary on the bounded benchmark basis.

It does not establish local independence under the framework because every mandatory test must be completed and adjudicated. It also does not establish tested-space independence because no external substitute search was executed.

A failure to find a reduction in this internal run is not a proof that no reduction exists.

## Falsification status

No admissible reduction was found. The independence hypothesis was therefore not falsified by PIE-001.

This statement must not be rewritten as "independence established." The correct result is:

> No successful reduction was identified in the completed subset of PIE-001, while derivability and substitution remain unresolved.

## Required next work

A follow-up execution must:

1. freeze explicit candidate derivations for every primitive;
2. freeze at least one non-equivalent substitute for every primitive;
3. use evaluator calibration and independent mappings;
4. retain all failed and divergent mappings;
5. adjudicate commitment-equivalence before aggregation;
6. compare vocabulary and representation costs using the preregistered Pareto rule.

## Artifacts

- `attempts.csv` — all 25 mandatory attempts;
- `tests/test_primitive_independence_execution.py` — deterministic coverage and claim-boundary checks.
