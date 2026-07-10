# External Validation: Chemistry

## Case Study

The ideal gas law, PV = nRT, relates pressure, volume, amount of substance, and absolute temperature for an idealized gas model.

## FAR Mapping

| FAR role | Scientific realization |
| --- | --- |
| Representation | pressure, volume, amount, temperature, gas constant, uncertainty |
| Representational structure | equation, units, controlled variables, state comparison |
| Interpretation | measurements treated as properties of a specified gas sample |
| Investigation | predict one state variable or test model fit |
| Reasoning calculus | algebra, thermodynamic conventions, measurement rules, model assumptions |
| Operation | measurement, unit conversion, substitution, prediction, residual comparison |

## Valid Inference

For a fixed amount of ideal gas at fixed absolute temperature, decreasing volume predicts increasing pressure because PV remains constant under the stated conditions.

FAR can represent the controlled variables, model equation, transformation, prediction, and observation comparison.

Result: PASS.

## Invalid Inference

A single agreement with PV = nRT is taken to prove that the gas is ideal under all pressures and temperatures.

This overgeneralizes beyond the tested state and ignores known model limits. FAR can separate local model fit from unrestricted theory confirmation.

Result: PASS.

## Malformed or Scope-Violating Case

Temperature in degrees Celsius is substituted directly where the equation requires absolute temperature, or inconsistent pressure-volume units are combined with an incompatible value of R.

FAR can represent the calculation but classify it as malformed relative to the supplied unit and interpretation rules.

Result: PASS.

## Alternative Explanations and Limits

Deviation may reflect non-ideal intermolecular effects, measurement error, leakage, temperature gradients, or incorrect amount estimates. The residual alone does not determine the cause.

## Source Basis

The ideal gas law is the established relation PV = nRT and is exact only for an ideal gas model, while serving as an approximation for many gases under suitable conditions.

## Final Outcome

CONDITIONAL PASS

Condition: the ideal-gas model, absolute-temperature convention, units, controlled variables, and measurement assumptions must be explicit.
