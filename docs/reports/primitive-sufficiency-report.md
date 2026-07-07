# Primitive Sufficiency Evaluation Report

Status: Regenerated from `theory/evaluation/evidence-registry.yaml` after v0.3.0 expanded fixture analysis.

## Registry Validation

- No registry validation errors detected.

## Overall Statistics

- Total systems: 23
- Analyzed systems: 13
- Remaining systems: 10
- Fits FAR: 9
- Conservative extensions: 10
- Outside FAR scope: 1
- Candidate counterexamples: 3
- Confirmed primitive counterexamples: 0

## Classification Counts

| Classification | Count |
|---|---:|
| candidate counterexample | 3 |
| conservative extension | 8 |
| extends FAR | 5 |
| fits FAR | 7 |

## Analysis Outcome Counts

| Analysis outcome | Count |
|---|---:|
| analyzed | 10 |
| conservative extension | 2 |
| not analyzed | 10 |
| outside FAR scope | 1 |

## Current Evidence

### Strongest evidence supporting primitive sufficiency

- Theorem provers and SAT solving fit FAR directly because they expose goals, formulas, proof states, assignments, certificates, structures, interpretations, and rule-governed transitions.
- Modal, temporal, deontic, intuitionistic, and fuzzy logics all pressure semantic status, but each pressure point reduces to indexed interpretation and mode-relative admissibility rather than a sixth primitive.
- Causal reasoning, type theory, and category-theoretic reasoning pressure structural complexity, but the relevant graph, context, diagram, and universal-property content is representational structure governed by calculi.
- No analyzed v0.3.0 fixture demonstrates explicit reasoning that cannot be represented by the five primitives, a derived concept, or a conservative extension of Interpretation, Reasoning Calculus, or Representational Structure.

### Strongest unresolved cases

- The frozen v0.2.0 carried-forward systems remain unresolved in this report: Classical logic, First-order logic, Bayesian reasoning, Scientific reasoning, Legal reasoning, Abductive reasoning, Analogical reasoning, Non-monotonic reasoning, Self-reference, and Infinite reasoning.
- These cases are not reclassified here because v0.2.0 is treated as the frozen baseline.

### Strongest remaining challenges

- Opaque automation remains a scope-boundary challenge: without an accessible trace or certificate, FAR has an assertion rather than explicit reasoning evidence.
- Infinite or fairness-sensitive temporal/path reasoning may need additional analysis against existing trace and infinite-reasoning concepts.
- Norm conflicts, dependent type universes, and higher categorical coherence may require more specialized derived concepts, but current fixtures do not show primitive failure.

## Unresolved Cases

- PS-001: Classical logic (`examples/far/reasoning-systems/classical-logic.far.yaml`)
- PS-002: First-order logic (`examples/far/reasoning-systems/first-order-logic.far.yaml`)
- PS-003: Bayesian reasoning (`examples/far/reasoning-systems/bayesian-reasoning.far.yaml`)
- PS-004: Scientific reasoning (`examples/far/reasoning-systems/scientific-reasoning.far.yaml`)
- PS-005: Legal reasoning (`examples/far/reasoning-systems/legal-reasoning.far.yaml`)
- PS-006: Abductive reasoning (`examples/far/reasoning-systems/abductive-reasoning.far.yaml`)
- PS-007: Analogical reasoning (`examples/far/reasoning-systems/analogical-reasoning.far.yaml`)
- PS-008: Non-monotonic reasoning (`examples/far/reasoning-systems/non-monotonic-reasoning.far.yaml`)
- PS-009: Self-reference (`examples/far/reasoning-systems/self-reference.far.yaml`)
- PS-012: Infinite reasoning (`examples/far/reasoning-systems/infinite-reasoning.far.yaml`)

## Candidate Counterexamples

- PS-010: Paradoxical reasoning (`examples/far/reasoning-systems/paradox.far.yaml`)
- PS-011: Inconsistent calculus (`examples/far/reasoning-systems/inconsistent-calculus.far.yaml`)
- PS-013: Opaque intuition or oracle reasoning (`examples/far/reasoning-systems/opaque-oracle-reasoning.far.yaml`)

## Current Conclusion

The expanded v0.3.0 fixture analysis strengthens provisional evidence for primitive sufficiency. No genuine primitive counterexamples were found. The current evidence supports conservative extension through derived concepts D-033 through D-035 rather than adding a sixth primitive.
