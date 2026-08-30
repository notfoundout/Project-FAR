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
