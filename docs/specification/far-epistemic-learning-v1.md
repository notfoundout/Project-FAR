# FAR Epistemic Learning Interchange 1.0

Version: 1.0

Status: Provisional application contract

Namespace: `far-epistemic/1.0`

## Boundary and authority

This is an additive application interchange around governed FAR investigations. It does not add a FAR Core primitive, alter `PROJECT-FAR-CORE-THEORY-1.1`, replace evidence closure or proof obligations, change the FAR workflow, or reinterpret any `far-ir/2.1` approximation, loss, provenance, construction, or product-cost coordinate. Probability, utility, expected utility, opportunity cost, expected value of perfect information (EVPI), tail risk, scores, and regret are distinct typed quantities in this namespace.

Interactive dialectic is not independently redefined here. Every embedded dialogue must be an exact, successfully validated `FAR-ELENCHUS-1.0` `ELENCHUS_SESSION` from the canonical [Socratic Epistemic Extensions specification](socratic-epistemic-extensions-v1.0.md). The epistemic document may reference those session identifiers from record provenance. This strict composition preserves the elenchus contract's typed question/response events, commitments, definitions, assumptions, warrants, implications, tensions, contradictions, revisions, withdrawals, chronology, provenance, and FAR Intake obligations. There is one elenchus architecture, not a parallel `DialecticRecord`.

The structural contract is [`schemas/far-epistemic-v1.schema.json`](../../schemas/far-epistemic-v1.schema.json). `EpistemicDocument.from_dict()` always executes that schema before semantic checks. The executable contract is `mechanization.far_mechanization.epistemic`; an object is conforming only if both structural and semantic validation succeed.

## Deterministic data and commitment semantics

Semantic probabilities and utilities are JSON strings, never binary JSON numbers:

- probabilities have exactly six fractional decimal places and lie in `[0,1]`;
- scored prediction probabilities lie strictly inside `(0,1)`;
- utilities have exactly six fractional decimal places;
- Brier and log scores have exactly twelve fractional decimal places;
- booleans, binary floats, `NaN`, and infinities are rejected in numeric positions.

Arithmetic uses local decimal context, precision 50, and `ROUND_HALF_EVEN`; it does not inherit the caller's ambient Decimal context. Natural-log loss uses `Decimal.ln()` and is quantized to twelve places. Brier score is `(p-o)^2`, also quantized to twelve places. Lower scores are better.

`FAR-CJ/1` canonicalization is UTF-8 JSON with exact unnormalized strings, keys ordered by Unicode code point, no insignificant whitespace, no duplicate keys, no non-finite values, and no surrogate replacement. Snapshot `sha256` is the lowercase SHA-256 digest of the `FAR-CJ/1` object after removing only its `sha256` member. Evidence commitments hash the exact UTF-8 bytes of the recorded evidence statement, and the `byte_target` declares that target. Other provenance artifact digests are declared external byte commitments: validation enforces real lowercase SHA-256 syntax but does not claim to retrieve an external URI.

## Records and lifecycle

### Evidence and snapshots

Evidence has a stable ID, observation time, statement, source URI, exact byte target, and verified statement digest. Every evidence ID used by a belief revision, causal assumption, outcome, or record provenance must exist. A belief revision's evidence must also occur in that belief's provenance.

A snapshot commits to one belief revision, its exact probability distribution, and its exact evidence reference set. The digest, revision identity, values, and chronology are recomputed. Predictions and decisions cannot substitute another snapshot.

### BeliefRecord / HypothesisSet

A belief contains at least two hypotheses with explicit priors, base/reference classes, falsifiers, and typed uncertainty. Its first revision equals the priors and supersedes nothing. Later revisions are strictly chronological, supersede exactly the immediately preceding revision, cite evidence, declare their update rule and rationale, and provide a complete distribution summing exactly to `1.000000`. `current_revision_ref` is the final revision.

The contract records a declared update; it does not establish that an update rule is rational, externally calibrated, or evidentially sufficient.

### PredictionRecord

A prediction references an existing belief and a cryptographically verified belief snapshot. Its hypothesis and probability must equal that snapshot. It freezes its proposition, creation time, resolution window, objective criterion, and explicit calibration reference class. Creation cannot predate the snapshot or follow the start of the resolution window.

### DecisionRecord

A decision references the same belief snapshot and prediction, and occurs after prediction creation but before resolution begins. Every uncertain state maps to exactly one snapshot hypothesis with the identical probability, and each hypothesis has exactly one state, including zero-weight hypotheses. Every action supplies a complete state-utility table, expected utility, downside utility, and typed tail-risk threshold/probability. The validator recomputes all four quantities, chosen-action opportunity cost, and **expected value of perfect information**:

`EVPI = sum_s p(s) max_a U(a,s) - max_a sum_s p(s) U(a,s)`.

This is deliberately named EVPI, not generic value of information. No information-acquisition/test model is represented.

### OutcomeRecord

An outcome binds one linked prediction and decision, objective evidence, resolution time, binary resolution, realized state, deterministic scores, and realized regret. The binary result must be one exactly when the realized state's hypothesis equals the predicted hypothesis. The validator checks lifecycle consistency, evidence provenance and observation time, resolution chronology, scores, state identity, and regret.

### ErrorRecord and RetestRecord

An error binds the prediction, decision, and outcome. Recurrence uses normalized `failure_mode_code` plus stable corrective-rule ID, never root-cause prose. A corrective rule declares which codes it applies to.

`retest_ref` may be null. Any asserted retest is a separate `RetestRecord` that must reference the error, a later non-empty set of resolved outcomes, one shared prediction reference class, the baseline outcome score, the deterministic comparison mean Brier score, and an evaluation time after the baseline and all comparison outcomes. `IMPROVED`, `UNCHANGED`, or `WORSE` is derived from those numbers. Even a valid `IMPROVED` record means only lower score on its exact declared comparison set; it does not establish general learning effectiveness, causal effectiveness of the rule, or external calibration.

### CausalModelRecord

A causal model contains typed variables/domains; mechanism-bearing directed edges; typed interventions with targets and assigned values; explicit confounder relations; counterfactual queries tied to interventions and outcome variables; identified assumptions with evidence references; and an identification object with estimand, treatment, outcome, status, adjustment set, assumptions, and limits. References, provenance, and DAG acyclicity are checked. `IDENTIFIED`, `PARTIALLY_IDENTIFIED`, and `NOT_IDENTIFIED` remain declared bounded statuses; conformance does not prove causal identification or model truth.

## Calibration

`calibration()` accepts only resolved outcomes selected by the caller under one identical explicit reference class and explicit strictly increasing bin edges from zero to one. Outcome probabilities are strict interior six-place decimal strings. Empty sets, mixed classes, invalid outcomes, probabilities outside the bins, nonfinite numbers, and duplicate/inverted edges fail. Bins are left-closed/right-open except the final right endpoint. Results report the declared class and edges, counts, mean probability, observed frequency, and overall mean Brier score. Selection, censoring, exchangeability, and population generalization remain external methodological assumptions and must not be inferred from a successful aggregate.

## API, CLI, replay, and versioning

```python
from mechanization.far_mechanization.epistemic import EpistemicDocument

document = EpistemicDocument.load("loop.json")
print(document.digest)
print(document.audit_event())
```

```text
far epistemic validate FILE
far epistemic calibration FILE --bin-edges 0,0.5,1
```

CLI failures produce deterministic JSON and nonzero status. The audit event is a deterministic content commitment suitable for adjacent replay/certificate storage; it is not itself a FAR proof or signed certificate. There is no historical `far-epistemic/0.9`, so 1.0 defines no synthetic predecessor migration. Future versions must introduce migrations only from real, frozen predecessor contracts and fixtures.

The complete fixture is [`examples/epistemic/complete-learning-loop.json`](../../examples/epistemic/complete-learning-loop.json). It includes the canonical elenchus session, typed causal model, two belief snapshots, two predictions/decisions/outcomes, deterministic scoring, a normalized error/corrective rule, a later comparable retest, and explicit nonclaims preventing a bounded lower score from being reported as general learning.
