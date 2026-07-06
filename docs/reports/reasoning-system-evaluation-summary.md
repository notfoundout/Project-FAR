# Reasoning-System Evaluation Summary

Status: Generated baseline for v0.2.0 falsification harness with provisional candidate-counterexample analysis.

## Classification counts

| Classification | Count |
|---|---:|
| fits FAR | 5 |
| extends FAR | 5 |
| candidate counterexample | 3 |
| fails fixture | 0 |

## Analysis counts

| Analysis decision | Count |
|---|---:|
| conservative extension | 2 |
| outside FAR scope | 1 |
| real counterexample | 0 |
| not analyzed | 10 |

## Fixture results

| System | Fixture | Classification | Primitive mapping complete | Representations | Relations | Transitions | Cycles | Analysis status | Notes |
|---|---|---|---|---:|---:|---:|---:|---|---|
| Abductive reasoning | `examples/far/reasoning-systems/abductive-reasoning.far.yaml` | fits FAR | yes | 3 | 2 | 1 | 0 | not analyzed | - |
| Analogical reasoning | `examples/far/reasoning-systems/analogical-reasoning.far.yaml` | fits FAR | yes | 3 | 2 | 1 | 0 | not analyzed | - |
| Bayesian reasoning | `examples/far/reasoning-systems/bayesian-reasoning.far.yaml` | fits FAR | yes | 3 | 2 | 1 | 0 | not analyzed | - |
| Classical logic | `examples/far/reasoning-systems/classical-logic.far.yaml` | fits FAR | yes | 3 | 2 | 1 | 0 | not analyzed | - |
| First-order logic | `examples/far/reasoning-systems/first-order-logic.far.yaml` | fits FAR | yes | 3 | 2 | 1 | 0 | not analyzed | - |
| Infinite reasoning | `examples/far/reasoning-systems/infinite-reasoning.far.yaml` | extends FAR | yes | 3 | 2 | 1 | 0 | not analyzed | - |
| Legal reasoning | `examples/far/reasoning-systems/legal-reasoning.far.yaml` | extends FAR | yes | 3 | 2 | 1 | 0 | not analyzed | - |
| Non-monotonic reasoning | `examples/far/reasoning-systems/non-monotonic-reasoning.far.yaml` | extends FAR | yes | 3 | 2 | 1 | 0 | not analyzed | - |
| Scientific reasoning | `examples/far/reasoning-systems/scientific-reasoning.far.yaml` | extends FAR | yes | 3 | 2 | 1 | 0 | not analyzed | - |
| Self-reference | `examples/far/reasoning-systems/self-reference.far.yaml` | extends FAR | yes | 3 | 3 | 1 | 1 | not analyzed | dependency cycle detected |
| Inconsistent calculus | `examples/far/reasoning-systems/inconsistent-calculus.far.yaml` | candidate counterexample | yes | 4 | 4 | 1 | 0 | conservative extension | non-explosive inconsistency can be represented as a calculus policy |
| Opaque intuition or oracle reasoning | `examples/far/reasoning-systems/opaque-oracle-reasoning.far.yaml` | candidate counterexample | yes | 3 | 2 | 1 | 0 | outside FAR scope | inaccessible process is not explicit reasoning under current FAR scope |
| Paradoxical reasoning | `examples/far/reasoning-systems/paradox.far.yaml` | candidate counterexample | yes | 3 | 2 | 1 | 0 | conservative extension | paradox requires a specialized semantic policy, not a new primitive |

## Provisional conclusion

The current analyzed candidate counterexamples do not yet establish a real primitive failure. Paradox and inconsistent calculi require conservative extensions. Opaque oracle reasoning is outside FAR scope unless the hidden process is made explicit.
