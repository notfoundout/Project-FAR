# Stage A Adjudication Codebook v1.0

Status: **Research**  
Program ID: `TCD-CLEANROOM-001`  
Applies to: Stage A1/A2 outputs under protocol v1.3

## 1. Immutable inputs

Adjudication receives only hashed raw A1 outputs, hashed A2 outputs, the sealed curator failure ledger, packet versions, contamination records, and this codebook. The adjudicator cannot edit a raw output.

## 2. Atomic question normalization

A submitted question is split only when it contains independently answerable clauses joined by `and`, `or`, semicolons, numbered subquestions, or separate failure predicates. Splitting must preserve the original text and a parent pointer.

Normalization may correct whitespace, capitalization, punctuation, and exact source-native synonyms. It may not replace a source-native concept with a target-architecture term.

## 3. Equivalence rule

Two atomic questions are equivalent only when all five fields match after normalization:

1. object of inquiry;
2. requested property;
3. answer space;
4. permitted evidence/access;
5. failure predicate.

Lexical similarity alone is insufficient. If any field differs materially, preserve separate questions.

## 4. Merge rule

Equivalent questions may be represented by one canonical wording plus all source pointers. A merge is prohibited when it broadens or narrows the object, property, evidence, Unknown meaning, or failure predicate. Prohibited merges are recorded as attempted and rejected.

## 5. Evidence linkage

Every question must cite at least one source-native review objective or one independently derived concrete failure mode. A question without linkage is `rejected_unlinked`.

## 6. Status algorithm

For each normalized atomic question:

- `accepted_convergent`: independently present in at least two uncontaminated A1 runs for the same case and passes all acceptance fields.
- `accepted_witness`: present in one uncontaminated A1 run and supported by a concrete admissible paired outcome or source-native rule showing different correct review results.
- `provisional_singleton`: present in one uncontaminated A1 run, passes acceptance fields, but lacks an independent witness.
- `curator_prompted`: absent from all uncontaminated A1 runs and introduced in A2 after curator-led disclosure.
- `disputed`: adjudicators disagree on equivalence, linkage, answer space, or failure predicate after one written challenge and response.
- `rejected_duplicate`: exactly equivalent to a retained question.
- `rejected_unlinked`: lacks objective/failure linkage.
- `rejected_target_shaped`: requests a target field or architecture without source-native necessity.
- `rejected_incomplete`: lacks answer space, evidence rule, Unknown meaning, or failure predicate.
- `excluded_contaminated`: appears only in contaminated runs.

No majority vote can convert `curator_prompted`, `provisional_singleton`, or `disputed` into `accepted_convergent`.

## 7. Adjudicator procedure

Two adjudicators independently code every atomic question. They then exchange only their coded records, not private deliberation. One challenge-response round is permitted. Remaining disagreement becomes `disputed`; a third adjudicator may select between the two written codings but may not introduce a third interpretation.

## 8. Cross-case synthesis

Cross-case equivalence uses the same five-field rule. Recurrence is reported as counts by case and source stratum. Frequency is not necessity. Curator-prompted questions are reported separately and excluded from primary convergence totals.

## 9. Reproducibility record

Every decision record contains:

- raw question hash and pointer;
- normalized wording;
- split/merge lineage;
- five equivalence fields;
- objective/failure linkage;
- A1 recurrence count;
- A2/curator provenance;
- adjudicator codes;
- challenge and response;
- final status;
- reason code.

Any decision not reconstructible from these fields fails adjudication.
