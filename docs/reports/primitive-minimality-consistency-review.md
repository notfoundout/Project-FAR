# Primitive Minimality and Independence Consistency Review

## 1. Documents Reviewed

- `research/validation/investigations/VI-002-primitive-minimality.md`
- `research/validation/investigations/VI-003-primitive-independence.md`
- `theory/proofs/T-001-primitive-minimality.md`
- `theory/proof-objects/T-001.proof.yaml`
- `theory/proofs/T-002-primitive-independence.md`
- `theory/proof-objects/T-002.proof.yaml`
- `theory/theorems/theorems.md`
- `research/open-problems/open-questions.md`

The actual T-002 proof-object path located during review is `theory/proof-objects/T-002.proof.yaml`.

## 2. Current Status Values

| Source | Record | Current status value |
|---|---|---|
| `theory/theorems/theorems.md` | T-001 — Conditional Primitive Minimality | Established, conditional. |
| `theory/theorems/theorems.md` | T-002 — Conditional Primitive Independence | Established, conditional. |
| `theory/proofs/T-001-primitive-minimality.md` | T-001 proof | Established relative to the current Project FAR scope, definitions, axioms, and deletion-only compression standard. |
| `theory/proofs/T-002-primitive-independence.md` | T-002 proof | Established relative to the current Project FAR definitions and reduction standard. |
| `theory/proof-objects/T-001.proof.yaml` | PO-T-001 | accepted |
| `theory/proof-objects/T-002.proof.yaml` | PO-T-002 | accepted |
| `research/validation/investigations/VI-002-primitive-minimality.md` | top status | Research |
| `research/validation/investigations/VI-002-primitive-minimality.md` | Research Status section | Completed; PASS (Provisional) |
| `research/validation/investigations/VI-003-primitive-independence.md` | top status / Research Status | Research |
| `research/open-problems/open-questions.md` | Primitive Independence | Active |
| `research/open-problems/open-questions.md` | Primitive Minimality | Active |

## 3. VI-002 Criterion-by-Criterion Assessment

VI-002 states that each primitive shall be classified as Reducible, Independent, or Undetermined. Its methodology also requires removing each primitive, defining it from the remaining primitives, reconstructing affected architecture and dependent FARA documents, verifying VI-001 remains executable, and recording loss of expressive power and hidden assumptions.

| Criterion | Relevant proof section or artifact | Assessment | Justification |
|---|---|---|---|
| Remove each primitive from the candidate basis. | VI-002 reduction investigations 1–7; T-001 proof and PO-T-001 deletion steps. | Satisfied | VI-002 contains separate reduction investigations for Object, Property, Relation, Representation, Interpretation, Investigation, and Reasoning Calculus. T-001/PO-T-001 covers a five-primitive theorem basis using deletion-only removal for Investigation, Representation, Representational Structure, Interpretation, and Reasoning Calculus. |
| Attempt to define the primitive using remaining candidate primitives. | VI-002 attempt sections under each reduction investigation. | Satisfied | VI-002 records multiple attempted reductions for each candidate primitive and gives evaluations. |
| Reconstruct every affected architectural definition. | VI-002 methodology; reduction evaluations; T-001 proof object. | Partially satisfied | VI-002 discusses architectural effects and failed reductions, but the reviewed proof object establishes deletion-only minimality from lemmas rather than documenting full reconstruction of every affected definition for the seven-candidate VI-002 basis. |
| Reconstruct every dependent FARA document. | VI-002 methodology and limitations. | Not addressed | The reviewed proof artifacts do not enumerate reconstructed dependent FARA documents for each primitive-removal attempt. |
| Verify VI-001 remains executable. | VI-002 conclusion and overall evaluation. | Partially satisfied | VI-002 says attempted reductions failed to preserve expressive capabilities demonstrated by VI-001, but the reviewed proof object does not contain a direct VI-001 execution artifact for each attempted reduction. |
| Record loss of expressive power. | T-001 proof; PO-T-001 steps s1–s10; VI-002 evaluations. | Satisfied for the five-theorem primitive basis; partially satisfied for the seven-candidate VI basis | T-001/PO-T-001 explicitly records expressive-power loss for each of the five theorem primitives. VI-002 records losses or circularity for all seven candidates, but the theorem proof does not cover Object and Property as theorem primitives. |
| Record hidden assumptions introduced by reduction. | VI-002 attempt evaluations and limitations. | Partially satisfied | VI-002 records circularity and lost distinctions; however, the proof artifacts do not provide a separate hidden-assumption ledger for every criterion. |
| Classify each primitive as Reducible, Independent, or Undetermined. | VI-002 summary matrix. | Satisfied, with provisional qualification | VI-002 classifies all seven candidate primitives as Independent (Provisional). |

## 4. VI-003 Criterion-by-Criterion Assessment

VI-003 requires a stricter independence showing: remove each primitive, replace every occurrence using the others, reconstruct definitions, execute VI-001 and VI-002, find and minimize a counterexample, and verify no equivalent reconstruction exists.

| Criterion | Relevant proof section or artifact | Assessment | Justification |
|---|---|---|---|
| Remove the primitive. | T-002 countermodels; PO-T-002 steps s2–s6. | Satisfied for the five-theorem primitive basis | T-002 constructs deletion test cases for Representation, Representational Structure, Interpretation, Investigation, and Reasoning Calculus. |
| Replace every occurrence using only remaining primitives. | T-002 proof method and countermodels. | Partially satisfied | T-002 argues that attempted recovery must reintroduce the omitted primitive or accepted replacement, but it does not document full replacement of every occurrence in all affected documents. |
| Reconstruct affected architectural definitions. | VI-003 methodology; T-002 proof. | Not addressed | The reviewed T-002 proof gives countermodels but does not include reconstructed architectural definitions. |
| Execute VI-001. | VI-003 methodology. | Not addressed | No execution record for VI-001 under each deletion case appears in the reviewed proof object. |
| Execute VI-002. | VI-003 methodology. | Not addressed | No execution record for VI-002 under each deletion case appears in the reviewed proof object. |
| Search for a reasoning situation no longer representable. | T-002 countermodels. | Satisfied | T-002 gives a no-representation, no-structure, no-interpretation, no-investigation, and no-calculus case, each explaining lost representability. |
| Minimize the counterexample. | VI-003 required evidence; T-002 countermodels. | Partially satisfied | The countermodels are minimal in form, but the proof does not present an explicit minimization argument or search procedure. |
| Verify no equivalent reconstruction exists. | T-002 conclusion and limitation. | Partially satisfied | The proof argues any repair must reintroduce the missing primitive or accepted replacement under the deletion-only standard. It does not establish absolute nonexistence under future lower-level theories. |
| Classify each candidate primitive as Independent, Dependent, or Undetermined. | VI-003 primitive evaluation matrix. | Not satisfied | VI-003 remains Pending/Research and does not classify any candidate primitive. |

## 5. Distinctions Required for Status Resolution

- **Proof validity under stated assumptions:** T-001 and T-002 are valid only under their stated current definitions, current axioms, current Project FAR scope, and deletion-only compression/reduction standards.
- **Local or conditional establishment:** The theorem registry and proof documents support conditional establishment of the five-theorem primitive basis: Investigation, Representation, Representational Structure, Interpretation, and Reasoning Calculus.
- **Satisfaction of the validation investigation:** VI-002 appears internally mixed: its top status says Research, while its Research Status section says Completed and PASS (Provisional). VI-003 remains Research and its evaluation matrix is still Pending.
- **Global/project-wide establishment:** The reviewed evidence does not support unqualified global establishment of absolute primitive minimality or absolute primitive independence. Both proof documents explicitly preserve limitations for future lower-level reductions or replacement theories.

## 6. Unresolved Assumptions or Proof Obligations

1. The theorem primitive set contains five primitives, while VI-002/VI-003 use seven candidates including Object and Property instead of Representational Structure.
2. VI-002 has conflicting status markers: top-level Research and later Completed/PASS (Provisional).
3. VI-003 has no completed primitive evaluation matrix.
4. The proof objects establish deletion-only results but do not satisfy all VI-003 methodology requirements for replacement, reconstruction, VI-001 execution, VI-002 execution, minimization, and equivalent-reconstruction exclusion.
5. Open questions still mark Primitive Minimality and Primitive Independence as Active despite conditional theorem establishment.

## 7. Proposed Consistent Statuses After Human Approval

These are recommendations only; no status-bearing sources were edited.

| Source | Proposed status treatment |
|---|---|
| `theory/theorems/theorems.md` T-001 | Keep `Established, conditional.` unless humans decide the theorem/VI primitive-set mismatch requires narrowing wording. |
| `theory/theorems/theorems.md` T-002 | Keep `Established, conditional.` unless humans require narrowing to `Established, conditional, deletion-only.` |
| `VI-002` | Resolve internal inconsistency by choosing either top-level `Completed` with `PASS (Provisional)` retained, or top-level `Research` with the later Completed/PASS section revised. Evidence favors Completed only for provisional reduction-investigation status, not global theorem-level minimality. |
| `VI-003` | Keep `Research` until its own methodology and matrix are completed. |
| `research/open-problems/open-questions.md` Primitive Minimality | Replace broad `Active` only with a more precise split after approval, e.g. conditional/deletion-only theorem resolved; absolute/future lower-level minimality remains open. |
| `research/open-problems/open-questions.md` Primitive Independence | Replace broad `Active` only with a more precise split after approval, e.g. deletion-independence conditionally resolved; full VI-003/global independence remains open. |

## 8. Exact Source Changes Required After Human Approval

1. In `research/validation/investigations/VI-002-primitive-minimality.md`, reconcile `## Status` with the later `# Research Status` section.
2. In `research/validation/investigations/VI-003-primitive-independence.md`, either complete the methodology and primitive evaluation matrix or retain `Research` and add an explicit note distinguishing T-002 deletion-independence from VI-003 completion.
3. In `research/open-problems/open-questions.md`, replace the unqualified Primitive Minimality and Primitive Independence `Active` entries with scoped entries distinguishing conditional deletion-only theorem results from unresolved absolute/future lower-level questions.
4. Optionally in `theory/theorems/theorems.md`, add wording that T-001 and T-002 are established only under the deletion-only standard and theorem primitive basis, if the existing title/status is deemed insufficiently explicit.

## 9. Recommendation

Do not automatically promote or demote any status-bearing source without human sign-off. The theorem registry is not simply wrong: it is supported by proof documents and accepted proof objects under stated assumptions. The VI files are not simply wrong either: VI-003 remains incomplete by its own criteria, and VI-002 contains provisional/internally inconsistent status evidence. The consistent resolution should preserve conditional theorem establishment while keeping broader validation/global questions open unless and until the missing VI criteria are satisfied.
