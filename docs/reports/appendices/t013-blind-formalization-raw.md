# T-013 Blind Formalization Raw Record

## Execution Metadata

- Artifact: T-013 — Relative Soundness Theorem
- Execution date: 2026-07-09
- Executor: Codex validation session
- Repository branch: codex/validate-t013
- Isolation classification: I1
- Isolation rationale: Verified isolation beyond I1 was not available. The formalization was executed inside a repository-aware validation session after the T-013 task, accepted foundation boundary, repository structure, and prior validation sequence were known.
- Scope limitation: T-013 only. T-014, T-015, and downstream artifacts were not validated.

## Prompt

You are performing a blind formalization of T-013 only under the accepted Project FAR foundation. Treat AX-001, all accepted canonical definitions, L-001 through L-008, P-001 through P-008, T-001 through T-012, Isolation Classification doctrine, Foundation Consistency Audit, Canonical Mathematics Audit, Definition Audit, and Boundary Repair Report as accepted. Do not validate T-014, T-015, or any downstream artifact. Use only the supplied inputs. Formalize the theorem, identify the minimally required premises, classify declared dependencies as Logically Required, Informative, or Historical, and state whether the theorem should be accepted, revised, or rejected.

## Supplied Inputs

1. T-013 statement: If a FAR representation marks a transition as admissible only when that transition is admissible under the supplied target calculus, then the FAR representation is sound relative to that calculus.
2. T-013 proof text: Let F be a FAR representation with reasoning calculus C. Assume the admissibility marking rule for F is: Mark admissible(t) only if C permits t. Let t be arbitrary and marked admissible in F. By the marking rule, C permits t. Therefore every transition marked admissible in F is admissible under C. By definition, a representation is sound relative to C when every transition it marks admissible is admissible under C. Therefore F is sound relative to C.
3. Declared dependencies: D-CALC; T-005.
4. Derived concept listed in metadata: D-006 Admissibility.
5. Accepted definition: Reasoning Calculus governs admissible reasoning transitions.
6. Accepted derived concept: Admissibility is satisfaction of criteria supplied by a Reasoning Calculus within an Investigation.
7. Model-theory definition: A FAR representation of a reasoning process is sound relative to a target calculus if every transition marked admissible by the FAR representation is admissible under that target calculus.
8. T-005 accepted summary: Explicitly specified admissible reasoning transitions can be represented in FAR by transition signatures.

## Complete Raw Output

Formalization target: T-013 is a conditional theorem about a FAR representation F and a supplied target calculus C.

Let Trans(F) be the transitions represented or assessed by F. Let Mark_F(t) mean F marks transition t admissible. Let Perm_C(t) mean C permits t. Let Adm_C(t) mean t is admissible under C. Let SoundRel(F, C) mean F is sound relative to C.

Accepted definitions supply:

1. A reasoning calculus governs admissible reasoning transitions.
2. Admissibility under C is satisfaction of the criteria supplied by C.
3. SoundRel(F, C) means: for every transition t, if Mark_F(t), then Adm_C(t).

T-013's assumption is:

A1. For every transition t, if Mark_F(t), then Perm_C(t).

The bridge supplied by D-CALC and D-006 is:

A2. For every transition t, if Perm_C(t), then Adm_C(t), because permitting a transition under the supplied calculus is the calculus-relative admissibility condition.

From A1 and A2, for arbitrary t:

- Assume Mark_F(t).
- By A1, Perm_C(t).
- By A2, Adm_C(t).
- Therefore Mark_F(t) implies Adm_C(t).

By universal generalization, every transition marked admissible by F is admissible under C.

By the relative soundness definition, SoundRel(F, C).

Dependency classification:

| Dependency | Classification | Reason |
| --- | --- | --- |
| D-CALC | Logically Required | The theorem is relative to a supplied target calculus and requires the accepted role of a reasoning calculus as governing admissible reasoning transitions. |
| D-006 | Logically Required | The proof needs the meaning of admissibility under C as satisfaction of criteria supplied by C. Without this bridge, “C permits t” and “t is admissible under C” are not fixed. |
| T-005 | Informative | T-005 concerns representability of explicitly specified admissible transitions by transition signatures. T-013 does not need transition-signature construction; it begins from a FAR representation that already marks transitions. |

Result: The theorem is valid as a conditional definitional consequence if dependencies are repaired from D-CALC and T-005 to D-CALC and D-006. No stronger substantive formulation is justified. The strongest evidence-supported final state is acceptance in revised dependency form, not a change to the theorem statement.

Recommendation: ACCEPT IN REVISED FORM.
