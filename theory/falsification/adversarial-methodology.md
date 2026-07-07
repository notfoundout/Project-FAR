# Adversarial Falsification Methodology

Status: Research

## Purpose

This methodology defines the adversarial evaluation phase of Project FAR. Its objective is to discover failures in the five-primitive hypothesis, not to confirm that FAR works.

The five-primitive hypothesis is treated as an explicit research hypothesis under adversarial testing. Positive examples, successful encodings, and familiar reasoning systems are not sufficient evidence of truth. They are only evidence that a specific attempted falsification has not yet succeeded.

Adversarial evaluation therefore gives priority to cases that stress, destabilize, or appear to exceed the current primitive basis.

## Burden of Proof

Evidence against primitive sufficiency is sufficient only when a candidate reasoning process is explicit, reproducible, and cannot be represented without introducing a new primitive.

A candidate failure must identify:

- the reasoning system under evaluation;
- the explicit reasoning process being tested;
- the primitive or primitives under pressure;
- the attempted representation using the existing primitives;
- the specific point of representational failure;
- the reason derived concepts do not resolve the failure;
- the reason interpretation, reasoning-calculus, and representational-structure extensions do not resolve the failure;
- machine-verifiable artifacts sufficient for independent reproduction.

Unsupported intuition, preference, tradition, or perceived elegance is not evidence against primitive sufficiency. A proposed sixth primitive is admissible only after the primitive failure standard below is satisfied.

## Evaluation Principles

### Adversarial Neutrality

Evaluators shall neither protect nor attack FAR as a conclusion. The task is to expose the hypothesis to strong tests and record the result.

### Reproducibility

Every adversarial result must be reproducible from recorded inputs, procedures, observations, and outputs.

### Explicit Reasoning Only

Only explicit reasoning processes are admissible as direct evidence. Opaque behavior may motivate future work, but it does not falsify primitive sufficiency unless the reasoning process is made explicit.

### Machine-Verifiable Evidence

Where practical, adversarial claims should be backed by machine-readable registries, fixtures, validation reports, or other artifacts that can be checked independently.

### Conservative Interpretation of Positive Results

A successful representation is not proof that the five primitives are sufficient in general. It only shows that the specific test has not produced a primitive failure.

### Preference for Falsification Over Confirmation

Evaluation effort should prioritize cases most likely to break primitive sufficiency rather than cases expected to fit.

### Minimality of New Commitments

No new primitive, definition, theorem, proof object, parser behavior, reasoning-engine behavior, or metadata schema should be introduced by adversarial evaluation infrastructure alone.

## Primitive Failure Standard

A primitive fails only if:

1. the reasoning process is explicit;
2. it cannot be represented using the five primitives;
3. no derived concept resolves the problem;
4. no interpretation extension resolves the problem;
5. no reasoning-calculus extension resolves the problem;
6. no representational-structure extension resolves the problem.

Only then may a sixth primitive be proposed.
