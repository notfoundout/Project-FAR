# Executive Summary

This PR validates only T-013 — Relative Soundness Theorem. T-014, T-015, and downstream artifacts were not validated.

Original finding: the theorem statement is conditionally sound under the accepted Project FAR foundation, but its dependency declaration was inflated because T-005 is not logically required for the relative soundness inference.

Revision applied: T-005 was removed from T-013 logical dependency metadata, proof-object support, and dependency graph. D-006 Admissibility remains recorded as the relevant derived concept and was added to the proof object as the admissibility bridge. The theorem statement was not changed.

Final accepted state: T-013 is accepted in revised dependency form under Isolation Class I1.

# Prior Foundation

The validation treated AX-001, all accepted canonical definitions, L-001 through L-008, P-001 through P-008, T-001 through T-012, Isolation Classification doctrine, Foundation Consistency Audit, Canonical Mathematics Audit, Definition Audit, and Boundary Repair Report as accepted foundation.

Prior accepted work was consumed as foundation only. Completed investigations were not repeated.

# Dependency Audit

Declared original dependencies audited from T-013 metadata, proof object, and dependency graph were D-CALC and T-005.

| Dependency | Classification | Finding | Action |
| --- | --- | --- | --- |
| D-CALC | Logically Required | T-013 is relative to a supplied target reasoning calculus and requires the accepted role of a reasoning calculus in governing admissible transitions. | Retained. |
| T-005 | Informative | T-005 concerns representation of explicitly specified admissible transitions by transition signatures. T-013 begins from an already supplied FAR representation with marked transitions and does not construct transition signatures. | Removed from T-013 logical dependency metadata, proof object, and dependency graph. |
| D-006 | Logically Required derived-concept support | D-006 supplies the accepted meaning of admissibility as satisfaction of criteria supplied by a Reasoning Calculus within an Investigation. It bridges C permitting a transition to admissibility under C. | Retained as a T-013 derived concept and cited in the proof object. |

The dependency repair synchronized theorem metadata, proof object, dependency graph, and generated theorem index. The generated index changed only through normal regeneration from metadata.

# Isolation Classification

Achieved isolation class: I1.

Verified isolation beyond I1 was not available because the validation occurred inside a repository-aware session after the task, accepted foundation boundary, repository structure, and prior validation sequence were known.

# Blind Formalization

The blind formalization raw record is preserved in `docs/reports/appendices/t013-blind-formalization-raw.md`.

It formalized T-013 as a conditional universal claim: if every transition marked admissible by F is permitted by C, and admissibility under C is satisfaction of criteria supplied by C, then every transition marked admissible by F is admissible under C; therefore F is sound relative to C.

The formalization classified D-CALC and D-006 as logically required support and T-005 as informative.

# Blind Adversarial Review

The blind adversarial review raw record is preserved in `docs/reports/appendices/t013-adversarial-review-raw.md`.

The review tested vacuity, unsound target calculi, marking-rule ambiguity, inflated T-005 dependency, missing target calculus, self-validation by labels, circularity, and overclaiming.

No defeating counterexample remained after the dependency repair. The review found that the statement does not prove absolute truth preservation, empirical reliability, or normative correctness.

# Repository Comparison

Repository comparison found that the canonical theorem statement already states a conditional relative soundness claim. The proof text also includes the correct limitation: T-013 proves conditional soundness only and does not certify any supplied calculus as truth-preserving, empirically reliable, or normatively correct.

The proof object, however, used T-005 as a proof step for representability by transition signatures. That step was not used by the theorem statement's relative soundness inference and inflated the logical dependency set.

The repository after revision records T-013 dependency as D-CALC in theorem metadata and dependency graph, with D-006 retained as a derived concept. The proof object now cites D-006 instead of T-005 and no longer depends on transition-signature construction.

# Doctrine Evaluation

- Scope discipline: PASS. This validation covers T-013 only and does not validate T-014, T-015, or downstream artifacts.
- Dependency discipline: PASS after revision. D-CALC is the required declared logical dependency; D-006 is the required derived-concept support; T-005 is not retained as a logical dependency.
- Isolation discipline: PASS as I1. No unverified higher isolation class is claimed.
- Minimality: PASS. No theorem statement edit was made because the accepted evidence supports the existing conditional claim.
- Revision rule: PASS. Revision was limited to the evidence-supported dependency repair.
- Non-overclaiming: PASS. T-013 remains relative to a supplied calculus and does not assert absolute soundness.

# Acceptance Checklist

- [x] Validates only T-013.
- [x] Does not validate T-014.
- [x] Does not validate T-015.
- [x] Uses Isolation Class I1.
- [x] Performs dependency audit.
- [x] Performs isolation classification.
- [x] Preserves blind formalization raw record.
- [x] Preserves blind adversarial review raw record.
- [x] Performs repository comparison.
- [x] Performs doctrine evaluation.
- [x] Revises only where evidence demonstrates a stronger formulation.
- [x] Distinguishes original finding, revision applied, and final accepted state.
- [x] Provides final recommendation as ACCEPT IN REVISED FORM because the revision was applied.

# Revision History

Original finding: T-013's theorem statement was valid as a conditional relative soundness claim, but T-005 was an inflated logical dependency and D-006 was the relevant derived-concept support for admissibility.

Revision applied:

1. Removed T-005 from T-013 theorem metadata dependencies.
2. Retained D-006 in T-013 theorem metadata as a derived concept rather than an unresolved dependency identifier.
3. Replaced the T-005 proof-object premise and prior-theorem step with a D-006 admissibility premise and definition-unfolding step.
4. Updated the T-013 entry in the dependency graph from D-CALC, T-005 to D-CALC.
5. Regenerated theorem indexes from metadata.

Final accepted state: T-013 is accepted in revised dependency form with statement unchanged, declared dependency D-CALC, and derived-concept support D-006.

# Final Recommendation

ACCEPT IN REVISED FORM

# Remaining Open Questions

None blocking T-013 acceptance.

This validation does not decide whether T-014 or T-015 should be accepted, revised, or rejected.

# T-013 Readiness

T-013 is ready to serve as accepted evidence after review and acceptance of this PR.

T-014 may begin only after this T-013 validation PR is reviewed and accepted according to project process, and only as a separate scoped validation effort.
