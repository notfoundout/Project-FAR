# FAR IR 2.0 comparison-contract specification

Status: **PCA-W3 governed successor specification**

Format identifier: `far-ir/2.0`

Schema: [`schemas/far-contract-v2.schema.json`](../../schemas/far-contract-v2.schema.json)

Semantic verifier: [`mechanization/far_mechanization/contract_v2.py`](../../mechanization/far_mechanization/contract_v2.py)

## 1. Version boundary

`far-ir/2.0` is a versioned successor for comparison contracts. It does not replace or reinterpret `far-ir/1.0`. Version 1 remains the reasoning-document interchange format accepted at its historical Phase 3 scope. A v1 document contains representations, claims, evidence, operations, reasoning steps, dependencies, proofs, and graph material, but it does not by itself state the complete contract needed by `PROJECT-FAR-CORE-THEORY-1.1`.

The v1-to-v2 migrator therefore validates the v1 document, embeds its primitive payload unchanged, and materializes every missing comparison-contract dimension as `Unknown`. Migration is not semantic completion.

## 2. Contract tuple represented by v2

A v2 record makes the following dimensions explicit rather than inferring them from surrounding prose:

- contract identity and contract version;
- exact, approximate, or `Unknown` comparison mode;
- source/case domain `X`;
- required behavior `beta`;
- candidate representation `r`;
- observation contexts;
- admitted transformations/equivalences;
- interpretation profile;
- target/model class;
- frame;
- optional approximation, metric, loss, tolerance, and cost declarations;
- typed report outcome, including `Unknown`;
- factorization, collision, quotient, or unknown evidence;
- failure report;
- provenance and freeze metadata.

These fields are contract parameters. Their presence in a schema is not evidence that any one choice is universally privileged.

## 3. Checkable finite-explicit semantics

When `source_domain.kind = finite_explicit`, source, required-behavior, and representation tables are `EXPLICIT`, and an evidence object declares `CHECKED_FINITE_EXPLICIT`, the verifier recomputes the asserted property.

### 3.1 Factorization

For every listed case `x`, the verifier requires a functional decoder table and checks

`d(r(x)) = beta(x)`.

Missing decoder entries, nonfunctional decoder assignments, incomplete case coverage, or a mismatching decoded value fail validation. A checked factorization report must have outcome `PROVED`.

### 3.2 Collision

A checked collision witness names distinct cases `x1` and `x2`. The verifier requires

`r(x1) = r(x2)` and `beta(x1) != beta(x2)`.

A checked collision report must have outcome `REFUTED` because it refutes exact sufficiency of the recorded representation for the frozen contract.

### 3.3 Exact observational quotient

A checked quotient witness must partition the explicit case domain. Every class must be constant in required behavior. If `claims_exact_observational_quotient = true`, the verifier additionally checks both directions of the behavior-kernel condition:

`x ~ y` exactly when `beta(x) = beta(y)`.

This certifies the quotient represented by the fixture as the finite explicit observational quotient for that exact recorded beta table. It does not establish a domain-independent primitive architecture.

## 4. `Unknown` is a value, not missing data

`Unknown` is an explicit typed outcome and semantic status. Unknown evidence must have outcome `Unknown`, and outcome `Unknown` must use unknown evidence. An `Unknown` contract mode cannot certify a non-Unknown outcome.

This prevents migration, omitted fields, or inability to decide an application question from being silently recoded as absence, falsehood, proof, or conformance.

## 5. Freeze semantics

A `FROZEN` record contains an RFC3339 freeze time and `contract_sha256`. The hash is SHA-256 of canonical JSON for the `contract` object only. This avoids self-reference while binding every contract parameter that controls the comparison. Changing a frame, target class, observation context, transformation set, source table, behavior table, representation table, or approximation declaration invalidates the freeze hash.

Provenance source hashes are independent inputs and do not substitute for the contract freeze.

## 6. Approximation boundary

W3 permits optional metric/loss/cost declarations so a future W5 record need not break the interchange format. The schema fixes `w5_semantics_established` to `false`. The W3 verifier rejects `CHECKED_FINITE_EXPLICIT` evidence under `mode = approximate` with `W5_SEMANTICS_NOT_ESTABLISHED`.

Therefore W3 records approximation metadata without claiming that an approximation order, tolerance semantics, loss aggregation rule, or implementation cost order has been justified. Those obligations remain `PCA-W5-APPROXIMATION-AND-COST`.

## 7. Application-correspondence boundary

W3 verifies only what is encoded in a record. It does not prove that a chosen finite case list represents a real domain, that an interpretation profile is correct, that a target/model class is complete, or that observation contexts capture all material behavior. Those are domain-contract and collision-audit obligations for W4.

The six W4 target domains remain formal logic, Bayesian/causal reasoning, argumentation, model-based reasoning, type theory, and proof theory.

## 8. Conformance suite

The registered `conformance/far-ir-2.0/manifest.json` contains positive factorization, collision, and quotient witnesses plus an adversarial false-factorization fixture. Unit tests additionally mutate collision, quotient, freeze, Unknown, and approximation conditions and require the verifier to reject them for the correct reason.

Conformance success means the software enforces these encoded W3 semantics. It is not a substitute for the mathematical status of the governing core theory.

## 9. Normative diagnostic vocabulary

A rejected record carries one or more diagnostics. Each diagnostic has a `code`, a human-readable `message`, and an optional JSON `path`. **The code is normative and the message is not.** An independent implementation of this specification must emit the same code set for the same record; message wording, ordering within a code, and path formatting are implementation detail.

The declaration authority is `FAR_IR_2_0_DIAGNOSTIC_CODES` in [`mechanization/far_mechanization/diagnostic_vocabulary.py`](../../mechanization/far_mechanization/diagnostic_vocabulary.py). It is declared there rather than in the verifier because [`contract_v2.py`](../../mechanization/far_mechanization/contract_v2.py) is pinned by git blob identity as the preregistered `PCA-W6` protocol base and must not change after that freeze. This table, that declaration, and the verifier's actual emission sites are held equal by `tests/test_far_contract_diagnostic_codes.py`.

### 9.1 Document intake and schema

| Code | Emitted when |
|---|---|
| `UNREADABLE_CONTRACT` | The file cannot be read or is not well-formed JSON. |
| `SCHEMA_CONSTRAINT_VIOLATION` | The document violates `far-contract-v2.schema.json`. Emitted once per schema error, ordered by JSON path then message. |

### 9.2 Finite-explicit check preconditions

| Code | Emitted when |
|---|---|
| `CHECK_REQUIRES_FINITE_EXPLICIT_DOMAIN` | Checked evidence is declared but `source_domain` is not `finite_explicit` with status `EXPLICIT`. |
| `CHECK_REQUIRES_EXPLICIT_TABLES` | Checked evidence is declared but `required_behavior` or `representation` does not have status `EXPLICIT`. |
| `DUPLICATE_DOMAIN_CASE` | `source_domain.cases` contains a repeated case identifier. |
| `DUPLICATE_CASE_VALUE` | A behavior or representation table assigns two rows to one `case_id`. |
| `CASE_TABLE_COVERAGE_MISMATCH` | A behavior or representation table does not cover exactly the declared case identifiers. |

### 9.3 Factorization evidence

| Code | Emitted when |
|---|---|
| `NONFUNCTIONAL_DECODER` | `decoder_table` assigns two distinct behavior values to one canonical representation value. |
| `DECODER_UNDEFINED` | No decoder row matches the representation value of a declared case. |
| `FACTORIZATION_FAILURE` | `d(r(x)) != beta(x)` for a declared case. |

### 9.4 Collision evidence

| Code | Emitted when |
|---|---|
| `COLLISION_CASE_UNKNOWN` | A witness case identifier is not in `source_domain`. |
| `COLLISION_REQUIRES_DISTINCT_CASES` | The witness names the same case twice. |
| `COLLISION_REPRESENTATION_DIFFERS` | The witness cases do not share a canonical representation value. |
| `COLLISION_BEHAVIOR_AGREES` | The witness cases do not differ in required behavior. |

### 9.5 Quotient evidence

| Code | Emitted when |
|---|---|
| `QUOTIENT_OVERLAP` | A case occurs in more than one declared class. |
| `QUOTIENT_NOT_PARTITION` | The declared classes do not partition `source_domain`. |
| `QUOTIENT_CLASS_NOT_BEHAVIOR_CONSTANT` | Two cases share a class but differ in required behavior. |
| `QUOTIENT_NOT_EXACT_BEHAVIOR_KERNEL` | `claims_exact_observational_quotient` is true and the class relation differs from the beta-kernel on some pair. |

### 9.6 Cross-field contract conditions

| Code | Emitted when |
|---|---|
| `UNKNOWN_EVIDENCE_REQUIRES_UNKNOWN_OUTCOME` | Evidence kind is `unknown` but the outcome is not `Unknown`. |
| `UNKNOWN_OUTCOME_REQUIRES_UNKNOWN_EVIDENCE` | The outcome is `Unknown` but the evidence kind is not `unknown`. |
| `UNKNOWN_CONTRACT_MODE_REQUIRES_UNKNOWN_OUTCOME` | Contract mode is `Unknown` but the outcome is not `Unknown`. |
| `W5_SEMANTICS_NOT_ESTABLISHED` | Contract mode is `approximate` and evidence status is `CHECKED_FINITE_EXPLICIT` (see §6). |
| `CHECKED_EVIDENCE_OUTCOME_MISMATCH` | Checked evidence carries an outcome other than `REFUTED` for collision evidence or `PROVED` for any other kind. |
| `DUPLICATE_OBSERVATION_CONTEXT` | `observation_contexts` contains a repeated identifier. |
| `DUPLICATE_TRANSFORMATION` | `admitted_transformations` contains a repeated identifier. |
| `FREEZE_HASH_MISMATCH` | Freeze status is `FROZEN` and `contract_sha256` does not equal SHA-256 of the canonical `contract` object (see §5). |

### 9.7 Evaluation order

Schema errors are terminal: when any `SCHEMA_CONSTRAINT_VIOLATION` is present, no semantic check runs. Otherwise cross-field conditions are evaluated, then the single check selected by `report.evidence.kind`. Within the finite-explicit checks, a precondition failure in §9.2 suppresses the corresponding §9.3–§9.5 check for that record. Independent implementations must reproduce this suppression behavior, because it determines which codes a record yields.

Publishing this vocabulary is a specification-completeness obligation, not a claim that the code set is minimal, complete for future versions, or externally validated.
