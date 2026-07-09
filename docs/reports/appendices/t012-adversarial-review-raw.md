# T-012 Blind Adversarial Review Raw Appendix

## Execution Metadata

- Artifact: T-012 — FAR Model Equivalence Theorem
- Date: 2026-07-09
- Executor: Codex research executor
- Repository branch: codex/validate-t012
- Method: blind adversarial review from supplied accepted-foundation inputs and T-012 text only
- Isolation classification: I1

## Isolation Classification

I1. The exercise was performed within the repository workspace and used supplied accepted foundation summaries plus the T-012 repository text. No verified isolation stronger than I1 was available.

## Prompt

You are performing a blind adversarial review of T-012 only under the accepted Project FAR foundation. Treat AX-001, accepted L-001 through L-007, accepted P-001 through P-008, accepted T-001 through T-011, Isolation Classification doctrine, and Foundation Validation Consolidation as accepted evidence. Do not validate T-013 or any downstream theorem. Use only the supplied inputs. Attempt to defeat the theorem, identify dependency inflation, classify supplied dependencies as Logically Required, Informative, or Historical, identify whether revision can repair defects, and provide a recommendation of ACCEPT, REVISE, or REJECT. If revision is needed, state the strongest evidence-supported formulation.

## Supplied Inputs

Accepted foundation supplied:

- AX-001 is accepted.
- L-001 through L-007 are accepted.
- P-001 through P-008 are accepted.
- T-001 through T-011 are accepted.
- Isolation Classification doctrine is accepted.
- Foundation Validation Consolidation is accepted.
- Prior results are consumed as accepted evidence and are not reopened.

T-012 repository statement supplied:

> Two FAR models are equivalent relative to a preservation profile `Q` if and only if every property in `Q` is preserved between them.

T-012 definitions supplied:

> A preservation profile `Q` is a finite set of properties selected from structural, semantic, calculative, trace, and investigation-relative properties.
>
> Two models `A` and `B` are `Q`-equivalent when `A ≡Q B`, meaning every property in `Q` holds in `A` exactly when the corresponding property holds in `B`.

Declared dependencies supplied:

- FAR model theory
- T-004

Proof-object premises supplied:

1. Let `A` and `B` be FAR models and let `Q` be a specified preservation profile.
2. A preservation profile `Q` is a finite set of selected structural, semantic, calculative, trace, and investigation-relative properties.
3. `A` and `B` are `Q`-equivalent exactly when every property in `Q` holds in `A` exactly when the corresponding property holds in `B`.
4. T-004: Semantic content is preserved under interpretation-preserving mappings.

## Complete Raw Output

### Adversarial Attacks

1. Absolute-equivalence attack. If T-012 claims that FAR models are equivalent simpliciter, it is false: models can preserve selected properties while differing in properties outside the selected profile. The statement avoids this by making equivalence relative to `Q`.

2. Empty-profile attack. If `Q` is empty, every pair of FAR models is vacuously `Q`-equivalent. This is not a contradiction; it is a consequence of profile-relative equivalence. If nonempty equivalence is desired, that would be a stronger theorem requiring an explicit nonempty-profile premise. T-012 does not require it.

3. Corresponding-property attack. The supplied definition says every property in `Q` holds in `A` exactly when the corresponding property holds in `B`. If properties are not well-formed predicates on both models, the biconditional is ill-typed. FAR model theory or the preservation-profile definition must ensure that `Q` contains properties applicable to both models. This is a well-formedness obligation rather than a defeat if `Q` is specified.

4. Semantic-content dependency attack. T-004 is not needed to prove the biconditional. The biconditional is true by definition of `Q`-equivalence. T-004 may justify one class of semantic preservation property when a profile includes semantic content under interpretation-preserving mappings, but that does not make T-004 a logical dependency of T-012.

5. Nontrivial mapping attack. T-012 does not prove that a mapping exists between arbitrary models or that any nontrivial preservation property is actually preserved. It only equates a definition with its unfolded condition. The limitation correctly states that stronger equivalence theorems require specified profiles and nontrivial mappings.

6. Downstream contamination attack. T-013 and later soundness/completeness results are not required. The theorem must not cite or rely on downstream results. The supplied dependency set does not include downstream theorems.

### Dependency Classification

| Dependency | Classification | Justification |
| --- | --- | --- |
| FAR model theory | Logically Required | It defines FAR models and model equivalence relative to a property set or preservation profile. The proof is definition unfolding/folding from this source. |
| T-004 | Informative | Useful example or semantic case for properties that may appear in `Q`, but not needed for the definitional equivalence. |
| AX-001 | Historical | Accepted root background, not directly used in the biconditional proof. |
| Accepted L-001 through L-007 | Historical | Accepted earlier foundation; no individual lemma is required for the definition-unfolding proof. |
| Accepted P-001 through P-008 | Historical | Accepted earlier foundation; no proposition is required for the T-012 inference. |
| Accepted T-001 through T-003 and T-005 through T-011 | Historical | Accepted chain context, not direct proof premises. |
| Isolation Classification doctrine | Historical | Governs validation isolation but not the theorem inference. |
| Foundation Validation Consolidation | Historical | Governs use of accepted evidence but not the theorem inference. |

### Defect Assessment

The theorem statement is repairable and does not require substantive revision if it remains explicitly relative to a specified preservation profile. The repository dependency declarations overstate T-004 as a logical dependency. The proof object also includes a T-004 premise and a semantic-preservation step that are not used to derive the final biconditional. Those should be removed to keep dependency discipline minimal.

### Strongest Evidence-Supported Formulation

Keep the theorem in its current relative form. Strengthen neither the theorem nor the corollary. Revise only dependency-bearing artifacts by removing T-004 as a declared logical dependency and deleting the unused T-004 proof-object premise/step.

### Recommendation

REVISE dependency metadata/proof object only. If this PR applies that repair, final recommendation should be ACCEPT IN REVISED FORM.
