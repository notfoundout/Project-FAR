# UPP-W5 machinery-closure audit

## Decision

The admissible representation package is no longer evaluated only by its visible core. It is expanded to the least fixed point of every disclosed, required, effectively available support dependency needed to construct, execute, interpret, query, or identify the representation.

The registered result is:

`transitive_machinery_closure_frozen_with_fixed_point_and_hidden_dependency_failure`

## Closure domain

The closure relation includes decoders, interpreters, schedulers, query interfaces, codebooks, external stores, realized oracles, proof objects, runtimes, configurations, operationally required learned artifacts, randomness sources, and identity registries. The list is extensible by role; no item escapes merely because it is stored outside the visible representation.

## Adjudication

A package is **closed** only when every transitively required edge is disclosed and supported by a present, effectively usable target. It is **open** when a required edge is concealed, absent, ineffective, invalid, or unsupported. It is **unknown** when no failure is established but required support remains unresolved.

Unknown is not weakened into closure, and concealment is not treated as missing evidence. Concealment of machinery required for a registered answer is a positive closure failure.

## Fixed-point properties

For finite packages, traversal terminates because each declared node can enter the reached set at most once. Cycles are permitted and terminate at the same finite fixed point. Closed packages are tested for idempotence. Adding disclosed, effective support is tested for monotonicity of the reached set.

## Adversarial coverage

The regression suite covers transitive decoder-to-store dependencies, concealed decoders, unrealized oracles, unknown schedulers, optional absent telemetry, ineffective present support, undeclared roots, duplicate identifiers, cycles, monotonic extension, and duplicate registered queries.

## Claim boundary

This workstream closes the machinery-accounting loophole. It does not prove that two closed packages are equivalent, that they preserve the same commitments, or that RCCD is necessary or sufficient. Those obligations remain downstream.

Public evaluation remains unauthorized. The sole next action is PR #287, `UPP-W6-EQUIVALENCE`.
