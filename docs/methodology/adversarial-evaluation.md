# Adversarial Evaluation

Status: Research

## Why Adversarial Evaluation Exists

Adversarial evaluation exists to test the Project FAR five-primitive hypothesis against cases selected because they may fail. The objective is not to collect examples that fit FAR. The objective is to organize explicit attempts to falsify primitive sufficiency.

This phase treats failure as a successful research outcome when the failure is explicit, reproducible, and supported by evidence.

## Why Confirming Examples Are Insufficient

Confirming examples show only that specific reasoning systems can be represented under specific assumptions. They do not establish that all explicit reasoning can be represented by the five primitives.

A theory may survive many examples and still fail under a single well-formed counterexample. For that reason, successful representations must be interpreted conservatively.

## Failed Falsification Attempts and Confidence

Repeated failed attempts to falsify the hypothesis can increase confidence in the hypothesis. They do not prove it true.

Each failed attempt narrows the space of currently known objections only if the attempt is reproducible, explicit, and recorded with enough detail for independent inspection.

## Designing New Adversarial Tests

Future contributors should design tests by:

1. selecting a reasoning system that plausibly stresses at least one primitive;
2. stating the hypothesis under test before analysis begins;
3. recording the primitive under pressure;
4. keeping expected and observed outcomes distinct;
5. avoiding classification until analysis has been performed;
6. preserving machine-readable registry consistency;
7. documenting why derived concepts or conservative extensions do or do not resolve observed pressure;
8. proposing a new primitive only after the primitive failure standard is satisfied.

New tests should prefer explicit, reproducible artifacts over narrative claims. They should not modify primitives, definitions, axioms, theorems, proof objects, parsers, reasoning engines, CI, or metadata schemas.
