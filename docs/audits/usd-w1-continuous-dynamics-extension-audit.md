# Audit — USD-W1 continuous-dynamics extension

## Scope integrity

The source class is frozen independently of the candidate vocabulary. Admission depends on effective finite-dimensional presentation, a computable Lipschitz bound, declared compact horizon, effectively decidable isolated guards, and finite reasoning annotations. No FARA primitive appears in the admission rule.

## Construction audit

The construction is uniform across `S_cd_lip_eff`. It uses the source-declared evaluation interfaces and certified bounds; it does not use a source-instance-specific decoder, future-trajectory oracle, exact-real equality oracle, or new target primitive.

The continuum is represented intensionally by a coherent refinement family. This differs materially from asserting that one finite grid is the trajectory. Every rational query time and positive rational tolerance is handled under one interface.

## Preservation audit

The proof separately checks:

- flow observations and refinement coherence;
- real-time and event ordering;
- guard and reset effects;
- commitments, grounds, and dependencies;
- history and revision;
- rejection of discretization collapse and oracle smuggling.

No preservation dimension is converted from Unknown to Pass merely because no counterexample was found.

## Negative-control audit

The fixed-grid negative control is rejected because it loses a guard crossing. The oracle-smuggling control is rejected because it imports undeclared power. Nonunique and Zeno examples are recorded as frozen scope boundaries rather than repaired after execution.

## Classification audit

`extension_proved` would be false because the result excludes major continuous families. `countermodel` would also be false because all admitted fixtures satisfy the construction. The correct terminal outcome is `proper_subclass_only`.

## Claim-boundary audit

The result advances one feature subclass only. It does not establish all continuous dynamics, general `S_IRD` representation, universal structure, necessity, minimality, uniqueness, actual-process correspondence, mechanization, or independent review.
