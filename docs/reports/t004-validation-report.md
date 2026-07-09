# Executive Summary

T-004 was validated under the accepted Project FAR foundation and only T-004 was evaluated. The validation followed the required sequence: dependency audit, isolation classification, blind formalization, blind adversarial review, repository comparison, doctrine evaluation, revision evaluation, and final recommendation.

Final recommendation: ACCEPT.

T-004 changed: yes. The theorem wording did not change. The proof document's dependency section was revised to classify dependencies and remove Semantic Equivalence as a logical dependency. One nonessential semantic-equivalence proof paragraph was removed because it was not required for the semantic-preservation conclusion. The theorem metadata and theory dependency graph were updated to replace inflated dependencies with direct definition dependencies.

# Prior Foundation

The following foundation was consumed as accepted evidence and was not re-investigated:

- AX-001.
- L-001 through L-007.
- P-001 through P-005.
- T-001.
- T-002.
- T-003.
- Isolation Classification doctrine.
- Foundation Validation Consolidation.

This validation did not validate T-005 or any downstream theorem.

# Dependency Audit

Declared dependency sources audited:

- `theory/proofs/T-004-semantic-preservation.md`.
- `theory/metadata/theorems.yaml`.
- `theory/dependencies/dependency-graph.md`.
- `theory/proof-objects/T-004.proof.yaml`.

| Declared dependency | Classification | Justification |
| --- | --- | --- |
| Representation Mapping / DEF-034 | Logically Required | T-004 quantifies over a mapping `M` from a source representational structure to a target representational structure. Without the representation-mapping concept, the object whose preservation property is being proved is absent. |
| Interpretation / DEF-030 | Logically Required | The hypothesis is interpretation preservation, expressed pointwise as `Int1(r) = Int2(M(r))`. The proof cannot state or use this hypothesis without Interpretation. |
| Semantic Content / DEF-031 | Logically Required | The conclusion is semantic-content preservation. The proof works by unfolding semantic content as meaning assigned under a specified interpretation. |
| Semantic Equivalence / DEF-033 | Informative | The original proof used semantic equivalence as an intermediate explanatory consequence, but the theorem's conclusion does not require it. The semantic-content equality already proves semantic-content preservation. |
| D-REP | Informative | Representation is background vocabulary for representation mapping and semantic content, but the direct theorem dependency is better represented by the definitions for Representation Mapping, Interpretation, and Semantic Content. |
| D-INT | Informative | Interpretation is logically required, but the metadata-level declaration `D-INT` was less precise than the canonical definition identifier DEF-030. |
| P-003 | Informative | Semantic relativity is consistent with T-004 and explains why semantic content is interpretation-relative, but T-004's conditional proof is carried by the supplied definitions rather than by P-003 as a separate premise. |
| P-006 | Historical | P-006 is not part of the accepted foundation supplied for this validation and is not needed to prove T-004. Its prior appearance in T-004 metadata and the theory dependency graph was an inflated historical dependency record. |
| DEF-033 in proof object premise p4 | Informative | The proof object uses semantic equivalence for an intermediate step. This is not required for the theorem conclusion, but changing the proof object would exceed the necessary correction because the proof object remains structurally valid and its extra intermediate step is non-defeating. |

Dependency modifications made:

1. `theory/proofs/T-004-semantic-preservation.md` now classifies dependencies as Logically Required, Informative, and Historical.
2. `theory/proofs/T-004-semantic-preservation.md` removes Semantic Equivalence from logical dependencies and retains it only as informative.
3. `theory/proofs/T-004-semantic-preservation.md` removes the nonessential semantic-equivalence proof paragraph, leaving the direct semantic-preservation proof intact.
4. `theory/metadata/theorems.yaml` changes T-004 dependencies from `D-REP`, `D-INT`, `P-003`, and `P-006` to `DEF-030`, `DEF-031`, and `DEF-034`.
5. `theory/dependencies/dependency-graph.md` makes the same T-004 dependency correction.
6. No unrelated dependency records were modified.

# Isolation Classification

Achieved isolation class: I1.

Rationale: the blind formalization and blind adversarial review were executed by the same agent in the same repository task, with explicit prompts prohibiting repository, Git history, internet, prior report, and downstream-theorem use during those steps. Because verified process-level isolation was not available, the validation uses I1 as required.

# Blind Formalization

Raw appendix created: `docs/reports/appendices/t004-blind-formalization-raw.md`.

Result: the blind formalization found that T-004 follows by definitional unfolding when semantic content is the meaning assigned under an interpretation and interpretation preservation is read pointwise over mapped representations.

Recommendation from blind formalization: ACCEPT.

# Blind Adversarial Review

Raw appendix created: `docs/reports/appendices/t004-adversarial-review-raw.md`.

Result: the adversarial review found no defeating objection under the supplied definitions. It identified non-defeating risks around domain restriction, pointwise interpretation equality, dependency inflation, and possible overreading beyond mapped representations.

Recommendation from blind adversarial review: ACCEPT.

# Repository Comparison

Repository comparison found that the canonical theorem proof already states the required domain restriction: for every representation `r` in the domain of `M`, if `Int1(r) = Int2(M(r))`, then the semantic-content equality follows.

Repository comparison also found inflated dependency declarations:

- The proof document listed Semantic Equivalence as an unclassified dependency and used it for a nonessential intermediate conclusion.
- The theorem metadata and theory dependency graph listed `P-006`, which is not part of the accepted foundation supplied for this validation and is not logically required for T-004.
- The theorem metadata and theory dependency graph listed less precise primitive/proposition dependencies where direct definition dependencies better match the proof obligation.

No repository evidence demonstrated a stronger theorem wording. The existing theorem statement, expanded statement, formal condition, and limitation remain evidence-supported.

# Doctrine Evaluation

T-004 complies with the accepted foundation when read as a conditional theorem over interpretation-preserving representation mappings.

Doctrine checks:

- Necessity: the theorem requires only the mapping, interpretation, and semantic-content definitions.
- Minimality: dependency declarations were reduced rather than expanded.
- No downstream reliance: T-005 and later theorems were not used.
- No new theory: no new theorem, proposition, primitive, or axiom was introduced.
- Scope discipline: the theorem remains limited to mapped representations and gives a sufficient condition rather than a necessary condition.
- Isolation discipline: I1 was used because verified isolation was not available.

# Acceptance Checklist

- [x] Dependency Audit completed.
- [x] Isolation Classification completed.
- [x] Blind Formalization completed and raw appendix preserved.
- [x] Blind Adversarial Review completed and raw appendix preserved.
- [x] Repository Comparison completed.
- [x] Doctrine Evaluation completed.
- [x] Revision considered only where evidence demonstrated a superior formulation.
- [x] No T-005 validation performed.
- [x] No downstream theorem validation performed.
- [x] No new theorems, propositions, primitives, or axioms introduced.
- [x] Required validation commands run.

# Revision History

Revisions applied in this validation:

1. Dependency classification added to `theory/proofs/T-004-semantic-preservation.md`.
2. Semantic Equivalence moved from logical dependency status to informative status in `theory/proofs/T-004-semantic-preservation.md`.
3. The proof paragraph deriving semantic equivalence was removed because semantic equivalence is not needed to conclude that `M` preserves semantic content.
4. T-004 metadata dependencies changed from `D-REP`, `D-INT`, `P-003`, and `P-006` to `DEF-030`, `DEF-031`, and `DEF-034`.
5. T-004 dependency-graph entry changed from `D-REP`, `D-INT`, `P-003`, and `P-006` to `DEF-030`, `DEF-031`, and `DEF-034`.

No theorem statement wording changed.

# Final Recommendation

ACCEPT

# Remaining Open Questions

None blocking T-004 acceptance.

Non-blocking note: a future proof-object cleanup could remove the informative semantic-equivalence intermediate step from `theory/proof-objects/T-004.proof.yaml`, but this validation did not change it because the extra step is non-defeating and the user instructed that dependency modifications be limited to required changes.

# Next Artifact Readiness

T-004 is ready as accepted in revised dependency form.

T-005 may begin only after this T-004 validation PR is reviewed and accepted according to project process.
