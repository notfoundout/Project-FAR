# `far-ir/2.1` Approximation and Cost Contract

Status: **Accepted for PCA-W5 finite-explicit operational semantics**

`far-ir/2.1` is an additive successor. It does not modify or reinterpret `far-ir/2.0` or `far-ir/1.0`. Its checked scope is finite explicit tables with exact nonnegative rational arithmetic.

## Frozen semantics

A checked approximate record must itself be `FROZEN`, and its source domain, required behavior, and representation tables must be explicitly enumerated rather than merely declared. The frozen contract declares all of the following:

1. a total finite metric table, checked for identity, separation, symmetry, and triangle inequality;
2. a finite probability mass over every source case (the reference semantics), permitting zero mass where explicitly declared;
3. either reference-weighted expected aggregation or worst-case (`maximum`) aggregation;
4. a total decision-loss table over the behavior range and action set, checked here to equal the declared metric on those values;
5. an explicit nonnegative rational tolerance;
6. randomized decoder distributions for each used representation value; and
7. one or more separately named, minimize-only cost coordinates defining a product preorder.

For candidate decoder `d`, case `x`, required behavior `β(x)`, representation `r(x)`, and action `a`, case loss is

`L_d(x) = Σ_a d(a | r(x)) loss(β(x), a)`.

The aggregate is either `Σ_x μ(x)L_d(x)` or `max_x L_d(x)`. A candidate is feasible exactly when its aggregate is at most the frozen tolerance.

## Cost conclusions

Costs are not silently scalarized. Candidate `a` is below `b` exactly when it is no greater on every declared coordinate. A feasible candidate is Pareto-minimal when no other feasible candidate strictly dominates it. A least element must be below every feasible candidate. Consequently, multiple incomparable Pareto minima may exist while no least element exists.

## Exact boundary

The checked loss is a separating metric. Under `maximum` aggregation, exact recovery therefore means zero expected decision loss on every source case. Under reference-weighted `expected` aggregation, exact recovery is defined relative to the positive-mass support of the frozen reference: zero-mass cases do not affect the aggregate and cannot be inferred from a zero aggregate. With these definitions and nonnegative loss, zero tolerance makes the feasible set equal the corresponding exact-recovery set. The registered zero-tolerance fixture uses positive mass on every case, so its support-relative statement is also exact on the full listed domain.

This boundary is finite and operational; it is not a theorem about arbitrary measures, pseudometrics, unrepresented cases, or all representations.

## Governed evidence

Terminal W5 evidence is accepted only when the campaign manifest independently matches the registered record/artifact set and the recorded SHA-256 values match the repository bytes. The manifest must bind the semantic verifier and the campaign checker themselves; removing records or artifacts cannot turn validation loops vacuous.

## Boundaries

The verifier does not establish external-domain correspondence, a universally preferred reference distribution, universal scalar cost, unique optimum, open-domain approximation, computational complexity, novelty, empirical utility, or W6 claims. Different metrics, references, aggregators, tolerances, action sets, candidate universes, or cost coordinates define different contracts.

## Normative diagnostic vocabulary

A rejected record carries one or more diagnostics. Each has a `code`, a human-readable `message`, and an optional JSON `path`. **The code is normative and the message is not.** An independent implementation must emit the same code set for the same record; wording, ordering within a code, and path formatting are implementation detail.

The declaration authority is `FAR_IR_2_1_DIAGNOSTIC_CODES` in [`mechanization/far_mechanization/diagnostic_vocabulary.py`](../../mechanization/far_mechanization/diagnostic_vocabulary.py). It is declared there rather than in the verifier because [`contract_v21.py`](../../mechanization/far_mechanization/contract_v21.py) is SHA-256 pinned by the completed `PCA-W5` campaign manifest. This table, that declaration, and the verifier's actual emission sites are held equal by `tests/test_far_contract_diagnostic_codes.py`.

Two codes are constructed at runtime as `DUPLICATE_{label}` and appear nowhere as source literals: `DUPLICATE_METRIC_VALUE` and `DUPLICATE_LOSS_ACTION`. They are listed below like any other code.

### Intake, mode, and freeze

| Code | Emitted when |
|---|---|
| `UNREADABLE_CONTRACT` | The file cannot be read or is not well-formed JSON. |
| `SCHEMA_CONSTRAINT_VIOLATION` | The document violates `far-contract-v2.1.schema.json`. |
| `W5_MODE_EVIDENCE_REQUIRED` | Contract mode is not `approximate`, or evidence kind is not `approximation_cost`. |
| `CHECKED_EVIDENCE_OUTCOME_MISMATCH` | Checked approximation evidence carries an outcome other than `PROVED`. |
| `CHECK_REQUIRES_FROZEN_CONTRACT` | Freeze status is not `FROZEN`. |
| `FREEZE_HASH_MISMATCH` | Freeze status is `FROZEN` and `contract_sha256` does not equal SHA-256 of the canonical `contract` object. |

### Domain and table preconditions

| Code | Emitted when |
|---|---|
| `CHECK_REQUIRES_FINITE_EXPLICIT_DOMAIN` | `source_domain` is not `finite_explicit` with status `EXPLICIT`. |
| `CHECK_REQUIRES_EXPLICIT_BEHAVIOR` | `required_behavior` does not have status `EXPLICIT`. |
| `CHECK_REQUIRES_EXPLICIT_REPRESENTATION` | `representation` does not have status `EXPLICIT`. |
| `DUPLICATE_DOMAIN_CASE` | `source_domain.cases` contains a repeated case identifier. |
| `DUPLICATE_CASE_VALUE` | A behavior or representation table assigns two rows to one `case_id`. |
| `CASE_TABLE_COVERAGE_MISMATCH` | Behavior or representation does not cover the declared cases exactly. |

### Reference measure

| Code | Emitted when |
|---|---|
| `DUPLICATE_REFERENCE_CASE` | A case appears twice in `reference.weights`. |
| `REFERENCE_COVERAGE_MISMATCH` | Reference weights do not cover every case exactly. |
| `REFERENCE_NOT_PROBABILITY` | A weight is negative, or the weights do not sum to exactly one. |

### Metric

| Code | Emitted when |
|---|---|
| `DUPLICATE_METRIC_VALUE` | `metric.values` contains a repeated canonical value. |
| `DUPLICATE_METRIC_ENTRY` | `metric.entries` contains a repeated ordered pair. |
| `METRIC_NOT_TOTAL` | Entries do not cover the full product of declared values. Suppresses the four metric-axiom checks below. |
| `METRIC_IDENTITY_FAILURE` | `d(v, v) != 0` for a declared value. |
| `METRIC_SYMMETRY_FAILURE` | `d(l, r) != d(r, l)` for a declared pair. |
| `METRIC_SEPARATION_FAILURE` | `d(l, r) == 0` for distinct declared values. |
| `METRIC_TRIANGLE_FAILURE` | `d(l, r) > d(l, m) + d(m, r)` for a declared triple. |

### Loss

| Code | Emitted when |
|---|---|
| `DUPLICATE_LOSS_ACTION` | `loss.actions` contains a repeated canonical action. |
| `DUPLICATE_LOSS_ENTRY` | `loss.entries` contains a repeated (truth, action) pair. |
| `LOSS_NOT_TOTAL` | Entries do not cover the behavior range crossed with the action set exactly. |
| `METRIC_LOSS_DOMAIN_MISMATCH` | A (truth, action) pair required by the loss table has no metric entry. |
| `LOSS_METRIC_MISMATCH` | A declared loss value differs from the metric distance on the same pair. |

### Cost preorder and candidates

| Code | Emitted when |
|---|---|
| `DUPLICATE_COST_DIMENSION` | `cost_preorder.dimensions` contains a repeated identifier. |
| `DUPLICATE_CANDIDATE` | Two candidates share an identifier. The later candidate is skipped. |
| `DUPLICATE_CANDIDATE_COST` | One candidate declares a dimension twice. |
| `COST_COVERAGE_MISMATCH` | A candidate's costs do not cover the declared dimensions exactly. |
| `DUPLICATE_DECODER_ENTRY` | A candidate decoder repeats a representation value. |
| `DUPLICATE_DECODER_ACTION` | One decoder row repeats an action. |
| `DECODER_UNKNOWN_ACTION` | A decoder row assigns probability to an action outside the declared action set. |
| `DECODER_NOT_PROBABILITY` | A decoder distribution has a negative entry or does not sum to exactly one. |
| `DECODER_COVERAGE_MISMATCH` | A candidate decoder does not cover exactly the representation values used by the domain. |

### Frontier claims

| Code | Emitted when |
|---|---|
| `FEASIBLE_SET_MISMATCH` | `claimed_feasible` differs from the recomputed feasible set. |
| `PARETO_SET_MISMATCH` | `claimed_pareto_minimal` differs from the recomputed Pareto-minimal set. |
| `LEAST_SET_MISMATCH` | `claimed_least_elements` differs from the recomputed least-element set. |
| `EXACT_RECOVERY_SET_MISMATCH` | `exact_recovery_claims` differs from the recomputed exact-recovery set. |
| `ZERO_TOLERANCE_EXACT_BOUNDARY_FAILURE` | Tolerance is zero and the feasible set differs from the exact-recovery set. |

### Evaluation order

Schema errors are terminal. Otherwise the verifier fails closed in stages: intake/freeze/domain conditions are collected first and, if any fired, the record is rejected before any approximation semantics run; metric, loss, and cost-dimension conditions are collected next and, if any fired, no candidate frontier is computed; a candidate that produced any diagnostic is excluded from the frontier calculation entirely. Independent implementations must reproduce this staging, because it determines which codes a record yields.

Publishing this vocabulary is a specification-completeness obligation, not a claim that the code set is minimal, complete for future versions, or externally validated.
