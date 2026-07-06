# Primitive Sufficiency Evaluation Framework

Status: Provisional v0.3.0 evaluation framework.

## Scope

This framework begins v0.3.0 primitive-sufficiency evaluation without rewriting the frozen v0.2.0 baseline. The current evidence source is the v0.2.0 reasoning-system fixture set and its recorded candidate-counterexample analysis.

## Primitive sufficiency

Primitive sufficiency means that an analyzed reasoning system can be represented, evaluated, and audited using the five current FAR primitives without introducing an additional primitive:

1. Investigation
2. Representation
3. Representational Structure
4. Interpretation
5. Reasoning Calculus

A case supports primitive sufficiency only when its required reasoning behavior is accounted for by those primitives, including any explicitly stated policies or constraints attached to them.

## Supporting evidence

Supporting evidence includes reproducible repository artifacts that show all of the following:

- the reasoning system has a concrete fixture or comparable explicit artifact;
- the artifact validates under existing FAR tooling;
- each current primitive has an identifiable role in the case;
- the case's distinctive reasoning behavior is represented without changing the primitive set;
- any extension is stated as a policy, calculus, interpretation, structure, or scope boundary rather than as a new primitive;
- the evaluation result is recorded in the evidence registry.

## Conservative extension

A conservative extension is an addition that increases descriptive or operational detail without changing the primitive basis. It may add a specialized policy, semantic convention, calculus rule, fixture pattern, validation check, or registry field when that addition is reducible to existing primitives.

A conservative extension must not:

- introduce a sixth primitive;
- alter accepted v0.2.0 conclusions;
- make a new theorem claim unless separately justified;
- treat convenience, convention, or explanatory usefulness as evidence of necessity.

## Unresolved

A case is unresolved when the available evidence is insufficient to classify primitive sufficiency, falsification, conservative extension, or scope exclusion. Unresolved does not count as support for FAR and does not count as falsification.

Common unresolved conditions include:

- the fixture exists but no primitive-sufficiency analysis has been performed;
- a distinctive reasoning behavior is named but not reduced to existing primitives;
- the result depends on a hidden or unexecuted assumption;
- the case requires additional reproducible evaluation before promotion.

## Falsification

A case falsifies primitive sufficiency only if reproducible evidence shows that a reasoning system within FAR scope cannot be represented or evaluated by the five current primitives, even after all conservative extensions have been attempted and shown insufficient.

A falsification must identify:

- the in-scope reasoning behavior;
- the failed attempted reductions to each current primitive or permitted conservative extension;
- why the failure is not caused by an incomplete fixture, tooling limitation, or scope boundary;
- the minimum new primitive obligation implied by the failure.

## Requirement for a sixth primitive

A sixth primitive would be required only if an in-scope, explicit reasoning system has an indispensable feature that is not reducible to Investigation, Representation, Representational Structure, Interpretation, or Reasoning Calculus, and the feature cannot be handled by a conservative extension.

The burden of proof remains on the proposed primitive. Until that burden is met, the correct registry resolution is unresolved, conservative extension, or outside scope, not primitive expansion.
