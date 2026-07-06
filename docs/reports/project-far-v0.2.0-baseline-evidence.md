# Project FAR v0.2.0 Baseline Evidence Report

Status: Provisional v0.2.0 baseline evidence report.

## Purpose

This report records the evidence baseline for Project FAR v0.2.0. It summarizes the reasoning-system fixture corpus, falsification-harness classifications, candidate-counterexample analysis, hard-case derived concepts, current evidence status, and known limitations.

This report is not a claim of universal coverage. It records the finite evidence currently available for v0.2.0 and fixes that evidence as a baseline for future comparison.

## Systems Tested

The v0.2.0 baseline fixture corpus tests the following reasoning systems:

| System | Fixture | v0.2.0 classification | Analysis status |
|---|---|---|---|
| Abductive reasoning | `examples/far/reasoning-systems/abductive-reasoning.far.yaml` | fits FAR | not analyzed |
| Analogical reasoning | `examples/far/reasoning-systems/analogical-reasoning.far.yaml` | fits FAR | not analyzed |
| Bayesian reasoning | `examples/far/reasoning-systems/bayesian-reasoning.far.yaml` | fits FAR | not analyzed |
| Classical logic | `examples/far/reasoning-systems/classical-logic.far.yaml` | fits FAR | not analyzed |
| First-order logic | `examples/far/reasoning-systems/first-order-logic.far.yaml` | fits FAR | not analyzed |
| Infinite reasoning | `examples/far/reasoning-systems/infinite-reasoning.far.yaml` | extends FAR | not analyzed |
| Legal reasoning | `examples/far/reasoning-systems/legal-reasoning.far.yaml` | extends FAR | not analyzed |
| Non-monotonic reasoning | `examples/far/reasoning-systems/non-monotonic-reasoning.far.yaml` | extends FAR | not analyzed |
| Scientific reasoning | `examples/far/reasoning-systems/scientific-reasoning.far.yaml` | extends FAR | not analyzed |
| Self-reference | `examples/far/reasoning-systems/self-reference.far.yaml` | extends FAR | not analyzed |
| Inconsistent calculus | `examples/far/reasoning-systems/inconsistent-calculus.far.yaml` | candidate counterexample | conservative extension |
| Opaque intuition or oracle reasoning | `examples/far/reasoning-systems/opaque-oracle-reasoning.far.yaml` | candidate counterexample | outside FAR scope |
| Paradoxical reasoning | `examples/far/reasoning-systems/paradox.far.yaml` | candidate counterexample | conservative extension |

## Fixture Classifications

The v0.2.0 falsification harness records the following classification counts:

| Classification | Count |
|---|---:|
| fits FAR | 5 |
| extends FAR | 5 |
| candidate counterexample | 3 |
| fails fixture | 0 |

The analysis-decision counts are:

| Analysis decision | Count |
|---|---:|
| conservative extension | 2 |
| outside FAR scope | 1 |
| real counterexample | 0 |
| not analyzed | 10 |

## Counterexample Fixtures

The v0.2.0 baseline contains three fixtures classified as candidate counterexamples:

1. `examples/far/reasoning-systems/paradox.far.yaml`
2. `examples/far/reasoning-systems/inconsistent-calculus.far.yaml`
3. `examples/far/reasoning-systems/opaque-oracle-reasoning.far.yaml`

Candidate-counterexample status means the fixture stresses the current primitive architecture and requires analysis. It does not by itself establish that the primitive basis has failed.

## Candidate-Counterexample Analysis Results

The v0.2.0 analysis results are provisional:

- **Paradoxical reasoning** is currently treated as a conservative extension. The analyzed pressure point is semantic instability in paradoxical self-reference. The current result is that the case requires explicit semantic and calculus policies, not a new primitive.
- **Inconsistent calculus** is currently treated as a conservative extension. The analyzed pressure point is contradiction without automatic explosion. The current result is that non-explosive behavior can be represented as a calculus-level policy.
- **Opaque intuition or oracle reasoning** is currently treated as outside FAR's present scope of explicit reasoning. The analyzed pressure point is inaccessible derivation. The current result is that FAR can represent an opaque assertion, but cannot evaluate the hidden process as explicit reasoning unless its representations, structures, interpretations, calculus, transitions, or trace become inspectable.

No analyzed candidate-counterexample fixture is currently classified as a real primitive failure.

## Hard-Case Derived Concepts

The hard-case analysis uses the following derived concepts to record pressure points without adding a sixth primitive:

- Semantic Instability
- Guarded Self-Reference
- Paraconsistent Calculus
- Non-Explosive Inference
- Explicit-Reasoning Scope Boundary
- Opaque Assertion

These are derived concepts for auditability and comparison. They are not new v0.2.0 primitives.

## Current Evidence Status

The current v0.2.0 evidence status is:

- multiple reasoning-system fixtures parse as machine-readable FAR examples;
- the reasoning engine runs over the fixture corpus;
- the falsification harness classifies all current reasoning-system fixtures;
- current candidate-counterexample fixtures have provisional analysis decisions;
- current analyzed hard cases do not establish a real primitive failure;
- no analyzed case currently requires introducing a sixth primitive.

## Limitations

The v0.2.0 evidence remains limited:

- the fixture corpus is finite;
- classification depends on the current fixture schema and evaluator behavior;
- not all fixture classes have received candidate-counterexample analysis;
- mechanization does not yet amount to a complete theorem prover;
- successful representation of current fixtures does not prove universality;
- future fixtures may expose missing structure, reduction failures, or primitive inadequacy;
- future tooling may strengthen, revise, or falsify current classifications.

## Provisional Conclusion

Project FAR v0.2.0 is the first evidence-bearing milestone for the current machine-readable fixture and falsification workflow. The current analyzed evidence does not require a sixth primitive. This conclusion is provisional and subject to future falsification.
