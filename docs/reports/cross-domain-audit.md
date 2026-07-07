# Cross-Domain Audit Report

Status: Provisional v0.3.0 report.

Source evaluation artifact: `theory/evaluation/cross-domain-consistency.md`.

## Summary

This report compares current classifications across related reasoning-system domains. It records consistency results without revising fixture classifications or hiding unresolved evidence.

| Domain/System | Classification | Analysis Status | Pressure Point | Consistency Result |
|---|---|---|---|---|
| Modal logic | conservative extension | analyzed | World-indexed semantics and accessibility structure | Consistent with temporal, dynamic, and hybrid logic as indexed or transition semantics. |
| Temporal logic | conservative extension | analyzed | Ordered temporal positions and path semantics | Consistent with modal and dynamic transition/index policies. |
| Dynamic logic | conservative extension | adversarial analysis | Program-transition semantics | Consistent with modal/temporal treatment as conservative transition discipline. |
| Hybrid logic | conservative extension | adversarial analysis | Named worlds and satisfaction operators | Consistent with modal indexed-interpretation pressure. |
| SAT solving | fits FAR | analyzed | Formula valuation, clauses, assignments, certificates | Consistent with theorem provers as explicit machine-checkable reasoning artifacts. |
| Theorem provers | fits FAR | analyzed | Kernel-checked proof traces and proof states | Consistent with SAT solving as explicit auditable artifacts. |
| Type theory | conservative extension | analyzed | Judgments, contexts, derivations, typing calculus | Consistent with intuitionistic logic as proof/admissibility discipline. |
| Intuitionistic logic | conservative extension | analyzed | Constructive proof standards | Consistent with type theory as specialized proof calculus discipline. |
| Paradoxical reasoning | candidate counterexample resolved as conservative extension | conservative extension | Semantic instability and guarded self-reference | Consistent with reflective/meta-reasoning as policy-based interpretation pressure. |
| Self-reference | extends FAR | not analyzed | Dependency cycle and cycle semantics | Borderline: related to paradox/reflection, but remains unresolved due to missing targeted analysis. |
| Reflective reasoning | conservative extension | adversarial analysis | Interpreting reasoning about reasoning | Consistent with meta-reasoning; adjacent to unresolved self-reference. |
| Meta-reasoning | conservative extension | adversarial analysis | Object/meta-level interpretation discipline | Consistent with reflective reasoning. |
| Fuzzy logic | conservative extension | analyzed | Degree-valued interpretation and threshold/t-norm calculus | Consistent with probabilistic programming as policy-based uncertainty handling. |
| Bayesian reasoning | fits FAR | not analyzed | Probabilistic update sufficiency | Borderline: fixture fits FAR, but registry keeps update analysis unresolved. |
| Probabilistic programming | conservative extension | adversarial analysis | Stochastic traces, conditioning, probability kernels | Consistent with fuzzy logic as domain-specific interpretation/calculus pressure. |
| Deontic logic | conservative extension | analyzed | Normative interpretation and conflict calculus | Consistent with legal reasoning's unresolved normative pressure. |
| Legal reasoning | extends FAR | not analyzed | Authority, precedent, and norm handling | Borderline: broader than deontic logic and remains unresolved. |

## Current Result

No direct classification contradiction is established. Borderline cases are preserved as unresolved where the repository lacks targeted analysis. Current analyzed cases do not establish the need for a sixth primitive.
