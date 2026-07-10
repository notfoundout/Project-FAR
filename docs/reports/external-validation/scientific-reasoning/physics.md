# External Validation: Physics

## Case Study

Newton's second law relates net force, mass, and acceleration through F = ma for the modeled system and frame. The test case uses the law as a supplied physical model rather than treating it as a theorem of FAR.

## FAR Mapping

| FAR role | Scientific realization |
| --- | --- |
| Representation | force vector, mass value, acceleration vector, uncertainty, observation record |
| Representational structure | vector components, units, time ordering, system boundary, equation relation |
| Interpretation | measured quantities assigned physical meaning in a specified frame |
| Investigation | predict acceleration or assess consistency with F = ma |
| Reasoning calculus | algebra, vector rules, measurement conventions, model assumptions |
| Operation | measurement, decomposition, summation, substitution, prediction, comparison |

## Valid Inference

Given a constant-mass object in a specified inertial frame, a measured net force of 10 N and mass of 2 kg imply a model prediction of 5 m/s² acceleration.

FAR can represent the measurements, units, model assumptions, algebraic operation, and comparison with observed acceleration.

Result: PASS.

## Invalid Inference

A measured acceleration is attributed to one named force without establishing that all other forces have been included.

This confuses net force with a selected component force. FAR can expose the missing system-boundary and force-summation assumptions.

Result: PASS.

## Malformed or Scope-Violating Case

The same scalar equation is applied across incompatible coordinate components or with inconsistent units.

FAR can represent the attempted calculation but classify it as structurally malformed relative to the supplied vector and unit conventions.

Result: PASS.

## Alternative Explanations and Limits

Disagreement between prediction and observation may reflect measurement error, omitted forces, changing mass, non-inertial coordinates, or model misuse. The observation alone does not identify which explanation is correct.

## Source Basis

Newton's second law is a standard physical relation connecting net force, mass, and acceleration. This report uses the canonical model only as a case for reasoning-structure analysis.

## Final Outcome

CONDITIONAL PASS

Condition: the physical model, system boundary, frame, units, and measurement assumptions must be supplied explicitly.
