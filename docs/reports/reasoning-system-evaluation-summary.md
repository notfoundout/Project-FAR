# Reasoning-System Evaluation Summary

Status: Generated baseline for v0.2.0 falsification harness.

## Classification counts

| Classification | Count |
|---|---:|
| fits FAR | 5 |
| extends FAR | 5 |
| candidate counterexample | 3 |
| fails fixture | 0 |

## Fixture results

| System | Fixture | Classification | Primitive mapping complete | Representations | Relations | Transitions | Cycles | Notes |
|---|---|---|---|---:|---:|---:|---:|---|
| Abductive reasoning | `examples/far/reasoning-systems/abductive-reasoning.far.yaml` | fits FAR | yes | 3 | 2 | 1 | 0 | - |
| Analogical reasoning | `examples/far/reasoning-systems/analogical-reasoning.far.yaml` | fits FAR | yes | 3 | 2 | 1 | 0 | - |
| Bayesian reasoning | `examples/far/reasoning-systems/bayesian-reasoning.far.yaml` | fits FAR | yes | 3 | 2 | 1 | 0 | - |
| Classical logic | `examples/far/reasoning-systems/classical-logic.far.yaml` | fits FAR | yes | 3 | 2 | 1 | 0 | - |
| First-order logic | `examples/far/reasoning-systems/first-order-logic.far.yaml` | fits FAR | yes | 3 | 2 | 1 | 0 | - |
| Infinite reasoning | `examples/far/reasoning-systems/infinite-reasoning.far.yaml` | extends FAR | yes | 3 | 2 | 1 | 0 | - |
| Legal reasoning | `examples/far/reasoning-systems/legal-reasoning.far.yaml` | extends FAR | yes | 3 | 2 | 1 | 0 | - |
| Non-monotonic reasoning | `examples/far/reasoning-systems/non-monotonic-reasoning.far.yaml` | extends FAR | yes | 3 | 2 | 1 | 0 | - |
| Scientific reasoning | `examples/far/reasoning-systems/scientific-reasoning.far.yaml` | extends FAR | yes | 3 | 2 | 1 | 0 | - |
| Self-reference | `examples/far/reasoning-systems/self-reference.far.yaml` | extends FAR | yes | 3 | 3 | 1 | 1 | dependency cycle detected |
| Inconsistent calculus | `examples/far/reasoning-systems/inconsistent-calculus.far.yaml` | candidate counterexample | yes | 4 | 4 | 1 | 0 | - |
| Opaque intuition or oracle reasoning | `examples/far/reasoning-systems/opaque-oracle-reasoning.far.yaml` | candidate counterexample | yes | 3 | 2 | 1 | 0 | - |
| Paradoxical reasoning | `examples/far/reasoning-systems/paradox.far.yaml` | candidate counterexample | yes | 3 | 2 | 1 | 0 | - |
