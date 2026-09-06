# EFR-U1 deterministic contract projection v1.0

Status: **Provisional preregistration material; frozen by protected promotion of PR #470 before execution**

This procedure supplies each prospective U1 contract and automated report before its arm is revealed. It does not permit choosing a behavior, representation, context, or frame after allocation. It narrows the eligible native-record format; correspondence to other domain records is not claimed.

## Native input and independent transcription

Before site enrollment, two independent custodians outside Project FAR and the site execution team inspect the existing SOP. It must uniquely identify the native source-case ID, source-case value, required-behavior value, and candidate-representation value in its routine records. Seal that source-field map, verbatim SOP, and source-format description with hashes. The field map only names pre-existing SOP fields; it may not introduce a new behavior, representation, equivalence, repair, or aggregation. If the SOP does not uniquely specify these fields and literal JSON-value equality, the site is ineligible. No later field-map revision is allowed.

For each consecutively screened investigation, seal the complete native evidence first. The two custodians separately transcribe every native row into `{id, value, required_behavior, representation}` using that field map, without running FAR or seeing the pending arm. Values must already be well-defined JSON values in the native format; preserve types, strings, array order, and every row. No inferred value, case omission, rounding, tolerance, normalization, or new source case is allowed. IDs must already be unique and satisfy the baseline v2 identifier schema. Empty tables, nonfinite numbers, duplicate IDs, missing fields, or non-unique extraction are ineligible before enrollment and remain in the screening log.

Sort transcribed rows by source-case ID. The two canonical JSON transcriptions must be identical. A third independent custodian resolves only a demonstrated transcription error by reference to the sealed source/SOP; unresolved disagreement makes the investigation ineligible before its arm is revealed. Retain both originals, the corrected transcription if any, exact source references, and every adjudication. A separate pair of blinded domain judges seals the native preservation/loss label and witness from the native source and SOP before FAR execution; a third judge resolves disagreement by the program's witness/majority rule. Unresolved native labels are ineligible. Projection constructors cannot use the FAR result to choose a native label.

## Fixed contract construction

Use the exact evidence baseline from the program freeze. Set record and contract IDs to `efr.u1.` followed by the enrolled investigation ID, `format_version` to `far-ir/2.0`, `contract_version` to `1.0`, and `mode` to `exact`. The following construction is normative; `rows` is the sorted, agreed transcription, and all strings below are literal:

```python
contract = {
    "id": "efr.u1." + investigation_id,
    "contract_version": "1.0", "mode": "exact",
    "source_domain": {
        "status": "EXPLICIT", "kind": "finite_explicit",
        "description": "All sealed native source cases.",
        "cases": [{"id": x["id"], "value": x["value"]} for x in rows],
    },
    "required_behavior": {
        "status": "EXPLICIT", "description": "Required behavior in the sealed SOP.",
        "table": [{"case_id": x["id"], "value": x["required_behavior"]} for x in rows],
    },
    "representation": {
        "status": "EXPLICIT", "description": "Recorded candidate representation.",
        "table": [{"case_id": x["id"], "value": x["representation"]} for x in rows],
    },
    "observation_contexts": [{"id": "obs.literal", "status": "EXPLICIT",
        "description": "Compare every listed row under literal canonical-JSON equality."}],
    "admitted_transformations": [{"id": "eq.literal", "kind": "equivalence", "status": "EXPLICIT",
        "description": "Literal canonical-JSON equality only."}],
    "interpretation_profile": {"id": "interp.literal", "status": "EXPLICIT",
        "description": "Literal canonical-JSON values; no inferred equivalences."},
    "target_model_class": {"id": "target.finite", "status": "EXPLICIT",
        "description": "Exactly the listed native source cases."},
    "frame": {"id": "frame.sealed", "status": "EXPLICIT",
        "description": "Only the sealed native evidence and SOP; no unstated premises."},
}
```

Do not add optional contract fields. For each distinct representation value, select the required-behavior value of its lexically first source-case ID. Sort these entries by the baseline verifier's `canonical_json(representation_value)`. Use this decoder table in a candidate report with `outcome=PROVED` and evidence `{kind: factorization, status: CHECKED_FINITE_EXPLICIT, decoder_table: entries}`; `failure_report` is `[]` and notes are omitted. This is a uniform candidate preservation claim for the verifier to check, not a preaccepted result. A collision causes the candidate decoder to fail on at least one row; do not replace the report with a different witness after seeing that result.

Record provenance producer `EFR-U1`, the RFC3339 transcription-seal time, and hashes of native evidence, SOP, field map, and agreed transcription. Freeze the contract with that same time and the baseline verifier's `contract_sha256(contract)`. Validate the resulting full record against the baseline v2 schema. Serialize frozen JSON with Python 3.12 `json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)` and UTF-8. No new field values or serialization choices are supplied at intake.

## Report and pre-arm seal

Run the baseline command `python -m mechanization.far_mechanization.contract_v2 RECORD --json` exactly once on the schema-valid record. Preserve its complete JSON stdout, stderr, exit code, runtime identity, and record hash. A semantic rejection (exit 1 with its diagnostic JSON) is an expected adverse output, not a reason to exclude or repair a valid record. A missing or malformed report is retained as a failed machine output; it cannot be replaced by a favorable rerun. The FAR form's report box displays the complete JSON stdout verbatim, or the literal text `AUTOMATED REPORT UNAVAILABLE` if no valid JSON stdout exists. Record every such failure and apply the program's missing-output/failure rules.

Append-only seal the native evidence, independent native label/witness, both transcriptions and adjudication, exact contract record, report bytes and execution log, assigned worker, and all hashes before revealing that investigation's arm. These projections/reports are generated for all forty investigations per site. Only FAR-assigned workers receive them; standard workers receive the common native evidence/SOP and outcome-capture form. Constructors and label custodians do not participate in the audit. No post-arm correction, projection substitution, selective omission, or case replacement is permitted. A later discovered source/projection breach remains visible and invalidates the affected test under the original rule.
