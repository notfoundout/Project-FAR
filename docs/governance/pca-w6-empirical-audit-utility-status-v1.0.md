# PCA-W6 Empirical Audit Utility Status v1.0

Status: **COMPLETE AT THE REGISTERED BOUNDED INTERNAL CONTROL SCOPE**

Evidence-class label: **bounded internal controlled-artifact semantic-detection conformance**

Program: `POST-CLOSURE-001`

Workstream: `PCA-W6-EMPIRICAL-AUDIT-UTILITY`

The historical workstream identifier is retained for provenance. The evidence-class label above is the preferred summary description because this experiment is not evidence of external real-world utility or human-review benefit.

## Disposition

PCA-W6 preregistered and executed a controlled artifact experiment over the six frozen W4 finite-explicit domains. The experiment compared JSON-Schema-only conformance with the FAR finite-explicit semantic audit on six unmodified repaired controls and six deterministic representation-collision mutants. It also replayed the six native W4 lossy collision records as secondary positive controls.

The registered mutation remained schema-valid in every domain. The schema-only baseline detected `0/6` mutants and accepted `6/6` clean controls. The FAR semantic audit detected `6/6` mutants and accepted `6/6` clean controls. A separate table-only collision oracle agreed with the FAR loss/no-loss classification on `12/12` primary items. All six native W4 lossy controls were separately recomputed by Project FAR.

Bounded material-loss-detection verdict: **PROVED for the registered corpus and defect class.**

Operational interpretation: **the registered semantic verifier detects the preregistered factorization-collision defect on this internally authored finite corpus where JSON-Schema-only validation does not.** The registered mutation directly targets a condition the semantic verifier is designed to check, so this result is best treated as controlled semantic-detection/conformance evidence rather than an estimate of general audit effectiveness.

## Evidence integrity

The exact W6 manifest binds the preregistration, result, independent-oracle implementation, frozen W4 corpus and protocol-base dependencies, dedicated workflow, tests, and every canonical propagation surface changed by W6. The final tree contains no branch-mutating finalizer; the W6 checker and regression suite fail if the temporary remediation workflow returns.

The provenance ledger separately records **zero scientific deviations** and **seven resolved execution incidents**. The result record is hash-bound to that ledger and states that none of the incidents changed the frozen scientific protocol or result. This preserves the real execution history without misclassifying harness, CI, governance, or packaging failures as scientific deviations.

## What W6 does not establish

The experiment used Project-FAR-authored records, Project-FAR-authored mutations, and Project-FAR-authored implementations. It had no human participants and no external investigator. Therefore:

- human disagreement reduction is `UNDERDETERMINED`;
- external real-world audit utility remains `OPEN`;
- no population sensitivity/specificity is estimated;
- no superiority over alternative audit methods is established;
- no domain-completeness, novelty, or priority claim is established;
- no commercial value, deployment readiness, or product-market evidence is established.

The schema-only baseline is a syntactic machine baseline, not a proxy for unaided human review.

## Theory impact

None. W6 is empirical/post-closure assurance. It does not alter `PROJECT-FAR-CORE-THEORY-1.1`, FAR-CORE-001–014, the W1 independent review, W2 formalization, W3 contract semantics, W4 domain results, or W5 approximation/cost semantics.

## Program consequence

The six registered `POST-CLOSURE-001` workstreams are complete at their governed scopes. This closes the currently registered post-closure workstream sequence without closing downstream external-effectiveness questions. OP-28 remains open for external/human evaluation. The separately governed `EXTERNAL-FALSIFICATION-AND-REPLICATION-001` successor is preregistered but not executed; it is not W7 and supplies no external/human result by registration alone.

For cross-claim calibration, see [`far-core-epistemic-calibration-v1.0.md`](../audits/far-core-epistemic-calibration-v1.0.md).
