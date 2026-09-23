# FAR Epistemic Learning Interchange 1.0

Version: 1.0

Status: Provisional implementation contract

Namespace: `far-epistemic/1.0`

## Scope and architectural boundary

This specification defines an **additive application record layer** around a FAR investigation. It does not add a FAR Core primitive, alter `PROJECT-FAR-CORE-THEORY-1.1`, or change the canonical FAR workflow. A document identifies the compatible `far-ir/1.0`, `far-ir/2.0`, or `far-ir/2.1` surface and connects to existing claims, evidence, reasoning steps, proof obligations, and certificates only through provenance references and immutable hashes.

Probability, confidence, utility, expected utility, opportunity cost, value of information, tail risk, and regret are typed epistemic/decision quantities in this namespace. They are not `far-ir/2.1` approximation loss, provenance cost, construction cost, or a comparison-contract cost coordinate. Implementations must reject attempts to put those cost fields into these records. Conversely, this layer cannot be used to scalarize or rank a FAR comparison cost order.

The JSON Schema is [`schemas/far-epistemic-v1.schema.json`](../../schemas/far-epistemic-v1.schema.json). The executable API is `mechanization.far_mechanization.epistemic`. Schema validation supplies structural validation; the API additionally checks cross-record, arithmetic, temporal, graph, and scoring invariants.

## Record contracts

Every record has a unique `id`, one closed `kind`, and provenance containing a source, content hash, and zero or more FAR identifiers. Evidence references point to the existing evidence graph rather than copying or silently adjudicating evidence.

### BeliefRecord / HypothesisSet

A `belief` contains at least two competing hypotheses. Each hypothesis declares a prior probability, current confidence, base/reference classes, falsifiers, and typed uncertainty. Both prior and current distributions are explicit. Every evidence update identifies an evidence reference, timestamp, update rule, and complete posterior over exactly the hypothesis set. The current distribution must equal the final posterior. Revision history is chronological and append-oriented.

The record does not claim that the declared update rule is correct. FAR evidence closure and proof obligations remain separate from numeric belief bookkeeping.

### PredictionRecord

A `prediction` freezes its proposition, timestamp, strict interior probability, resolution window, objective criterion, and evidence-snapshot hash. The snapshot hash must equal its provenance commitment. Resolution is binary. Unresolved records cannot carry scores; resolved records carry a resolution time and recomputed Brier score `(p-o)^2` and natural-log loss `-log(p)` or `-log(1-p)`. Lower scores are better.

`calibration()` groups resolved predictions into deterministic equal-width bins and reports count, mean probability, observed frequency, and overall mean Brier score. Comparable reference classes and selection rules remain the caller's declared methodological responsibility.

### DecisionRecord

A `decision` declares mutually named uncertain states whose probabilities sum to one, available actions, a complete state-contingent utility table, expected utility, worst (`downside_utility`) outcome, a textual tail-risk account, value of information, selected action, rationale, and opportunity cost. Expected utility and opportunity cost are recomputed. When an actual state is known, the outcome and counterfactual action regret are recorded and regret is recomputed.

Utility is necessarily decision-context specific. It neither certifies a moral objective nor inherits any FAR representation-cost meaning. Value of information is a separately declared non-negative decision quantity; the schema does not invent an information-acquisition model.

### DialecticRecord

A `dialectic` preserves the clarified claim, definitions, commitments, assumptions, strongest opposing case, burdens of proof, counterexamples, contradictions, disagreement cruxes, falsifiers, evidence that would change the positions, and revision/result. Required non-empty fields prevent an apparent dialogue record from omitting the opposing case or change conditions.

### CausalModelRecord

A `causal_model` is a first-class, provenance-bound directed acyclic graph with mechanisms, interventions, confounders, counterfactuals, assumptions, and identification limits. Node references and acyclicity are checked. A graph is a declared causal model, not proof that causal effects are identified; identification limitations cannot be omitted.

### ErrorRecord

An `error` links beliefs, predictions, decisions, reasoning/evidence references, and outcomes. It records classifications, root cause, corrective rule, recurring prior failure identifiers, a prospective retest criterion, and one of `improved`, `unchanged`, `worse`, `inconclusive`, or unresolved `null`. Corrective-rule success therefore requires later comparable evidence and cannot be inferred from writing the rule.

`recurring_failure_modes()` deterministically groups two or more ErrorRecords only when their declared root cause and classification set match. It reports the contributing identifiers and never infers an undeclared causal diagnosis.

## Lifecycle and replay

The supported lifecycle is:

```text
BeliefRecord (competing hypotheses and priors)
  -> evidence update and current confidence
  -> PredictionRecord (frozen evidence snapshot)
  -> DecisionRecord (separate probabilities and utilities)
  -> objective outcome / resolution
  -> scoring and longitudinal calibration
  -> ErrorRecord / recurring-mode linkage / prospective retest
  -> BeliefRecord revision history and later posterior
```

`EpistemicDocument` canonicalizes JSON for stable SHA-256 commitments, performs defensive serialization round trips, and emits a deterministic `far_epistemic_validation` audit event. That event can be stored beside existing replay/certificate artifacts; it is a content commitment and validation result, not a FAR theorem or signed certificate by itself.

## API and CLI

```python
from mechanization.far_mechanization.epistemic import EpistemicDocument, calibration

document = EpistemicDocument.load("loop.json")
print(document.digest)
print(document.audit_event())
```

CLI hooks are:

```text
far epistemic validate FILE
far epistemic calibration FILE --bins 10
far epistemic migrate FILE
```

All output is deterministic JSON. Validation failures return a nonzero status with stable path-addressed errors.

## Versioning and migration

`far-epistemic/1.0` is independent of FAR IR versioning. The loss-explicit `0.9` migration renames a legacy `resolution_date` to a point resolution window and adds `far-ir/1.0` only when the compatibility field was absent. It does not manufacture provenance, uncertainty, hypotheses, utilities, causal assumptions, or scoring. The migrated record must pass every 1.0 invariant or migration fails.

## Example and nonclaims

[`examples/epistemic/complete-learning-loop.json`](../../examples/epistemic/complete-learning-loop.json) executes the complete loop, including an explicit no-error/calibration observation so a correct prediction is not relabeled as a failure in hindsight.

Conformance establishes only that a record obeys this interchange contract. It does not establish truth, rationality of priors, causal identification, utility validity, decision optimality outside the declared table, external calibration, learning effectiveness, or any strengthening of FAR Core.
