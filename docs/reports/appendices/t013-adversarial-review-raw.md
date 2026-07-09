# T-013 Blind Adversarial Review Raw Record

## Execution Metadata

- Artifact: T-013 — Relative Soundness Theorem
- Execution date: 2026-07-09
- Executor: Codex validation session
- Repository branch: codex/validate-t013
- Isolation classification: I1
- Isolation rationale: Verified isolation beyond I1 was not available. The adversarial review was executed inside a repository-aware validation session after the T-013 task, accepted foundation boundary, repository structure, and prior validation sequence were known.
- Scope limitation: T-013 only. T-014, T-015, and downstream artifacts were not validated.

## Prompt

You are performing a blind adversarial review of T-013 only under the accepted Project FAR foundation. Treat AX-001, all accepted canonical definitions, L-001 through L-008, P-001 through P-008, T-001 through T-012, Isolation Classification doctrine, Foundation Consistency Audit, Canonical Mathematics Audit, Definition Audit, and Boundary Repair Report as accepted. Do not validate T-014, T-015, or any downstream artifact. Use only the supplied inputs. Attempt to falsify the theorem, identify hidden assumptions, dependency inflation, circularity, scope errors, and possible counterexamples. Classify declared dependencies as Logically Required, Informative, or Historical. Provide a final recommendation of ACCEPT, REVISE, or REJECT. If revision is needed, state the strongest evidence-supported formulation.

## Supplied Inputs

1. T-013 statement: If a FAR representation marks a transition as admissible only when that transition is admissible under the supplied target calculus, then the FAR representation is sound relative to that calculus.
2. T-013 proof text: Let F be a FAR representation with reasoning calculus C. Assume Mark admissible(t) only if C permits t. Let t be arbitrary and marked admissible in F. By the marking rule, C permits t. Therefore every transition marked admissible in F is admissible under C. By definition, relative soundness means every transition marked admissible is admissible under C. Therefore F is sound relative to C.
3. Declared dependencies: D-CALC; T-005.
4. Derived concept listed in metadata: D-006 Admissibility.
5. Accepted definition: Reasoning Calculus governs admissible reasoning transitions.
6. Accepted derived concept: Admissibility is satisfaction of criteria supplied by a Reasoning Calculus within an Investigation.
7. Model-theory definition: A FAR representation of a reasoning process is sound relative to a target calculus if every transition marked admissible by the FAR representation is admissible under that target calculus.
8. Accepted limitation: T-013 does not prove that a supplied calculus is truth-preserving, empirically reliable, or normatively correct.
9. T-005 accepted summary: Explicitly specified admissible reasoning transitions can be represented in FAR by transition signatures.

## Complete Raw Output

Adversarial target: defeat the claim that the conditional marking rule entails relative soundness.

Attack 1: Vacuity. If F marks no transitions admissible, then every marked transition is admissible under C vacuously. This does not defeat the theorem because the theorem is conditional and the accepted definition of relative soundness is universal over marked transitions.

Attack 2: Unsound calculus. C may be truth-destroying or normatively bad. This does not defeat T-013 because T-013 is explicitly relative to C and does not claim absolute truth preservation, empirical reliability, or normative correctness.

Attack 3: Marking rule ambiguity. The proof uses “C permits t” and concludes “t is admissible under C.” This is valid only if permission by C is identical to or sufficient for admissibility under C. The accepted D-CALC and D-006 definitions supply that bridge. The proof object should cite D-006 rather than relying silently on an informal equivalence.

Attack 4: T-005 dependency. T-005 states transition-signature representability for explicitly specified admissible transitions. T-013 does not construct transition signatures and does not require a representability theorem. It starts from a FAR representation with marked transitions. Therefore T-005 is not logically required. Retaining it as a logical dependency inflates the dependency set.

Attack 5: Missing target calculus. If no supplied target calculus C is fixed, the theorem is ill-scoped. The theorem statement and proof both include a supplied target calculus, so the attack fails inside the stated scope.

Attack 6: Self-validation by labels. Could FAR make a transition admissible by labeling it admissible? No. The condition is one-way: F marks a transition admissible only if C permits it. The theorem preserves calculus-relative admissibility and does not let a label create admissibility.

Attack 7: Circularity. D-CALC and D-006 are accepted definitions or derived concepts. T-005 is accepted but unnecessary. No downstream theorem is required. There is no circular dependence on T-013, T-014, or T-015.

Attack 8: Overclaiming. The statement says “sound relative to that calculus,” not “sound absolutely.” The limitation excludes truth-preservation and normative correctness. No overclaim remains if dependency repair is applied.

Dependency classification:

| Dependency | Classification | Reason |
| --- | --- | --- |
| D-CALC | Logically Required | The theorem's target is a calculus-relative admissibility condition. |
| T-005 | Informative | It may explain that admissible transitions can be represented as signatures elsewhere, but it is not an inferential premise for this conditional soundness result. |
| D-006 | Logically Required | It supplies the needed meaning of admissibility under a reasoning calculus. |

Required revision: repair dependency metadata and proof object by removing T-005 as a logical dependency and citing D-006 as the logical dependency that bridges calculus permission and admissibility. The theorem statement itself need not change.

Strongest evidence-supported final formulation: If a FAR representation marks a transition admissible only when that transition satisfies the admissibility criteria supplied by the target reasoning calculus, then every transition it marks admissible is admissible under that calculus; hence the representation is sound relative to that calculus.

Recommendation: REVISE if the dependency repair has not been applied; ACCEPT IN REVISED FORM if the dependency repair is applied successfully.
