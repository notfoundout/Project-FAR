# Primitive Sufficiency Evaluation Report

Status: Regenerated from `theory/evaluation/evidence-registry.yaml`, `theory/falsification/adversarial-test-suite.yaml`, and `theory/falsification/primitive-pressure-registry.yaml` for v0.3.0 synthesis.

## Registry Validation

- No registry validation errors detected.

## Overall Statistics

- Total systems: 23
- Analyzed systems: 13
- Remaining systems: 10
- Fits FAR by registry resolution: 2
- Conservative extensions by registry resolution: 10
- Outside FAR scope: 1
- Candidate counterexamples: 3
- Confirmed primitive counterexamples: 0
- Adversarial tests: 14
- Adversarial unresolved pressures: 1
- Adversarial candidate primitive failures: 0

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

- PS-010: Paradoxical reasoning (`examples/far/reasoning-systems/paradox.far.yaml`) — conservative extension
- PS-011: Inconsistent calculus (`examples/far/reasoning-systems/inconsistent-calculus.far.yaml`) — conservative extension
- PS-013: Opaque intuition or oracle reasoning (`examples/far/reasoning-systems/opaque-oracle-reasoning.far.yaml`) — outside scope

## Current Conclusion

The v0.3.0 evidence strengthens, but does not prove, the provisional primitive-sufficiency hypothesis. Current registries record 23 reasoning systems, 14 adversarial tests, 10 unresolved reasoning-system cases, 1 unresolved adversarial pressure, and 0 candidate primitive failures. No analyzed case currently requires a sixth primitive. Conservative extensions remain domain-specific policies, semantics, structures, or derived concepts expressible through the five primitives.
