"""Semantic validation for Project FAR Socratic epistemic extension records.

The JSON Schema checks structural shape. This module checks relationships that can
be decided from one explicit record and exposes resolver-assisted binding checks
for expertise applicability and epistemic-boundary views. It does not infer expertise, factual truth, semantic
completeness, or contradiction from natural-language content.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Mapping, Sequence

from jsonschema import Draft202012Validator

REPO_ROOT = Path(__file__).resolve().parents[2]
SCHEMA_PATH = REPO_ROOT / "schemas" / "socratic-epistemic-extensions-v1.schema.json"
FORMAT_VERSION = "socratic-epistemic-extensions/1.0"


@dataclass(frozen=True, slots=True)
class SocraticDiagnostic:
    code: str
    message: str
    path: tuple[object, ...] = ()


@dataclass(frozen=True, slots=True)
class SocraticValidationResult:
    diagnostics: tuple[SocraticDiagnostic, ...]

    @property
    def success(self) -> bool:
        return not self.diagnostics


def _load_schema() -> Mapping[str, Any]:
    return json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))


def _schema_errors(document: object) -> list[SocraticDiagnostic]:
    schema = _load_schema()
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema)
    return [
        SocraticDiagnostic("SCHEMA_CONSTRAINT_VIOLATION", error.message, tuple(error.path))
        for error in sorted(
            validator.iter_errors(document),
            key=lambda e: (tuple(str(part) for part in e.path), e.message),
        )
    ]


def _parse_aware_datetime(value: object) -> datetime | None:
    if not isinstance(value, str) or not value:
        return None
    normalized = f"{value[:-1]}+00:00" if value.endswith(("Z", "z")) else value
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError:
        return None
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        return None
    return parsed


def _check_unique_ids(
    entries: Sequence[Mapping[str, Any]],
    label: str,
    errors: list[SocraticDiagnostic],
) -> set[str]:
    seen: set[str] = set()
    for index, entry in enumerate(entries):
        value = str(entry["id"])
        if value in seen:
            errors.append(
                SocraticDiagnostic(
                    "DUPLICATE_IDENTIFIER",
                    f"{label} contains duplicate id {value}",
                    ("record", label, index, "id"),
                )
            )
        seen.add(value)
    return seen


def _scope_value(scope: Mapping[str, Any], dimension: str) -> object:
    if dimension == "subdomain":
        return scope.get("subdomain")
    return scope[dimension]


def _check_expertise_assertion(record: Mapping[str, Any], errors: list[SocraticDiagnostic]) -> None:
    valid_from = _parse_aware_datetime(record["valid_from"])
    if valid_from is None:
        errors.append(
            SocraticDiagnostic(
                "EXPERTISE_INVALID_VALID_FROM",
                "valid_from must be a parseable timezone-aware date-time",
                ("record", "valid_from"),
            )
        )

    valid_until_value = record.get("valid_until")
    valid_until: datetime | None = None
    if valid_until_value is not None:
        valid_until = _parse_aware_datetime(valid_until_value)
        if valid_until is None:
            errors.append(
                SocraticDiagnostic(
                    "EXPERTISE_INVALID_VALID_UNTIL",
                    "valid_until must be null or a parseable timezone-aware date-time",
                    ("record", "valid_until"),
                )
            )

    if valid_from is not None and valid_until is not None and valid_until < valid_from:
        errors.append(
            SocraticDiagnostic(
                "EXPERTISE_INVERTED_VALIDITY_INTERVAL",
                "valid_until must not precede valid_from",
                ("record", "valid_until"),
            )
        )


def _check_expertise_applicability(record: Mapping[str, Any], errors: list[SocraticDiagnostic]) -> None:
    if _parse_aware_datetime(record["evaluated_at"]) is None:
        errors.append(SocraticDiagnostic(
            "EXPERTISE_INVALID_EVALUATION_TIME",
            "evaluated_at must be a parseable timezone-aware date-time",
            ("record", "evaluated_at"),
        ))
    expertise_scope = record["expertise_scope"]
    claim_scope = record["claim_scope"]
    dimensions = record["dimensions"]

    nonmatching: list[str] = []
    for dimension in ("domain", "subdomain", "claim_type", "population", "geography", "time", "method"):
        assessment = dimensions[dimension]
        expertise_value = _scope_value(expertise_scope, dimension)
        claim_value = _scope_value(claim_scope, dimension)

        if assessment["expertise_value"] != expertise_value:
            errors.append(
                SocraticDiagnostic(
                    "EXPERTISE_DIMENSION_VALUE_MISMATCH",
                    f"{dimension} expertise_value does not match expertise_scope",
                    ("record", "dimensions", dimension, "expertise_value"),
                )
            )
        if assessment["claim_value"] != claim_value:
            errors.append(
                SocraticDiagnostic(
                    "EXPERTISE_DIMENSION_VALUE_MISMATCH",
                    f"{dimension} claim_value does not match claim_scope",
                    ("record", "dimensions", dimension, "claim_value"),
                )
            )

        status = assessment["status"]
        if status == "MATCH" and expertise_value != claim_value and not (assessment.get("bridge") or "").strip():
            errors.append(
                SocraticDiagnostic(
                    "UNJUSTIFIED_EXPERTISE_MATCH",
                    f"{dimension} is marked MATCH despite different values and no explicit bridge",
                    ("record", "dimensions", dimension),
                )
            )
        if status == "NOT_APPLICABLE" and dimension != "subdomain":
            errors.append(
                SocraticDiagnostic(
                    "EXPERTISE_REQUIRED_DIMENSION_NOT_APPLICABLE",
                    f"{dimension} cannot be skipped when deciding expertise applicability",
                    ("record", "dimensions", dimension, "status"),
                )
            )
        if dimension == "subdomain" and status == "NOT_APPLICABLE":
            if expertise_value is not None or claim_value is not None:
                errors.append(
                    SocraticDiagnostic(
                        "EXPERTISE_SUBDOMAIN_NA_WITH_VALUE",
                        "subdomain may be NOT_APPLICABLE only when both scopes omit it",
                        ("record", "dimensions", dimension, "status"),
                    )
                )
        if status not in {"MATCH", "NOT_APPLICABLE"}:
            nonmatching.append(dimension)

    if record["status"] == "SUPPORTED" and nonmatching:
        errors.append(
            SocraticDiagnostic(
                "EXPERTISE_SCOPE_OVERREACH",
                "SUPPORTED expertise applicability requires every material dimension to match; "
                f"nonmatching={nonmatching}",
                ("record", "status"),
            )
        )


def validate_expertise_applicability_binding(
    applicability_document: Mapping[str, Any],
    expertise_assertion_document: Mapping[str, Any],
    claim_snapshot: Mapping[str, Any],
) -> SocraticValidationResult:
    """Validate an applicability record against resolved source revisions.

    ``claim_snapshot`` is a parent-FAR resolver product with exact ``claim_id``,
    ``claim_version``, and ``scope`` keys. The helper deliberately does not fetch or
    infer those records itself; resolution remains the caller's provenance duty.
    """
    errors: list[SocraticDiagnostic] = []

    applicability_result = validate_socratic_record(applicability_document)
    if not applicability_result.success:
        errors.extend(applicability_result.diagnostics)
        return SocraticValidationResult(tuple(errors))

    assertion_result = validate_socratic_record(expertise_assertion_document)
    if not assertion_result.success:
        errors.extend(assertion_result.diagnostics)
        return SocraticValidationResult(tuple(errors))

    if applicability_document.get("record_type") != "EXPERTISE_APPLICABILITY":
        errors.append(
            SocraticDiagnostic(
                "EXPERTISE_BINDING_WRONG_APPLICABILITY_TYPE",
                "binding check requires an EXPERTISE_APPLICABILITY record",
            )
        )
        return SocraticValidationResult(tuple(errors))
    if expertise_assertion_document.get("record_type") != "EXPERTISE_ASSERTION":
        errors.append(
            SocraticDiagnostic(
                "EXPERTISE_BINDING_WRONG_ASSERTION_TYPE",
                "binding check requires an EXPERTISE_ASSERTION source record",
            )
        )
        return SocraticValidationResult(tuple(errors))

    applicability = applicability_document["record"]
    assertion = expertise_assertion_document["record"]

    if applicability["expertise_assertion_id"] != assertion["expertise_assertion_id"]:
        errors.append(
            SocraticDiagnostic(
                "EXPERTISE_ASSERTION_ID_MISMATCH",
                "applicability record does not reference the resolved expertise assertion id",
                ("record", "expertise_assertion_id"),
            )
        )
    if applicability["expertise_assertion_version"] != assertion["version"]:
        errors.append(
            SocraticDiagnostic(
                "EXPERTISE_ASSERTION_VERSION_MISMATCH",
                "applicability record does not reference the resolved expertise assertion version",
                ("record", "expertise_assertion_version"),
            )
        )
    if applicability["expertise_scope"] != assertion["scope"]:
        errors.append(
            SocraticDiagnostic(
                "EXPERTISE_ASSERTION_SCOPE_MISMATCH",
                "applicability expertise_scope does not match the resolved expertise assertion",
                ("record", "expertise_scope"),
            )
        )

    evaluated_at = _parse_aware_datetime(applicability["evaluated_at"])
    valid_from = _parse_aware_datetime(assertion["valid_from"])
    valid_until = _parse_aware_datetime(assertion.get("valid_until"))
    if evaluated_at is not None and valid_from is not None and (
        evaluated_at < valid_from or (valid_until is not None and evaluated_at > valid_until)
    ):
        errors.append(SocraticDiagnostic(
            "EXPERTISE_EVALUATION_OUTSIDE_VALIDITY",
            "expertise assertion is not valid at the applicability evaluation time",
            ("record", "evaluated_at"),
        ))

    required_claim_keys = ("claim_id", "claim_version", "scope")
    missing_claim_keys = [key for key in required_claim_keys if key not in claim_snapshot]
    if missing_claim_keys:
        errors.append(
            SocraticDiagnostic(
                "EXPERTISE_CLAIM_SNAPSHOT_INCOMPLETE",
                f"resolved claim snapshot is missing {missing_claim_keys}",
            )
        )
        return SocraticValidationResult(tuple(errors))

    if applicability["claim_id"] != claim_snapshot["claim_id"]:
        errors.append(
            SocraticDiagnostic(
                "EXPERTISE_CLAIM_ID_MISMATCH",
                "applicability record does not reference the resolved claim id",
                ("record", "claim_id"),
            )
        )
    if applicability["claim_version"] != claim_snapshot["claim_version"]:
        errors.append(
            SocraticDiagnostic(
                "EXPERTISE_CLAIM_VERSION_MISMATCH",
                "applicability record does not reference the resolved claim version",
                ("record", "claim_version"),
            )
        )
    if applicability["claim_scope"] != claim_snapshot["scope"]:
        errors.append(
            SocraticDiagnostic(
                "EXPERTISE_CLAIM_SCOPE_MISMATCH",
                "applicability claim_scope does not match the resolved claim revision",
                ("record", "claim_scope"),
            )
        )

    return SocraticValidationResult(tuple(errors))


def _check_epistemic_boundary(record: Mapping[str, Any], errors: list[SocraticDiagnostic]) -> None:
    disposition = record["claim_disposition"]
    if _parse_aware_datetime(disposition["decided_at"]) is None:
        errors.append(SocraticDiagnostic(
            "BOUNDARY_INVALID_DISPOSITION_TIME",
            "claim disposition decided_at must be a parseable timezone-aware date-time",
            ("record", "claim_disposition", "decided_at"),
        ))
    if (disposition["status"] == "OTHER") != ("target_status" in disposition):
        errors.append(SocraticDiagnostic(
            "BOUNDARY_INVALID_TARGET_STATUS",
            "target_status is required exactly when the protocol uses OTHER",
            ("record", "claim_disposition", "target_status"),
        ))
    categories = (
        "established",
        "conditionally_established",
        "supported_not_established",
        "unknown",
        "not_investigated",
        "not_identifiable_from_current_evidence",
        "explicit_nonclaims",
    )
    seen: dict[str, str] = {}
    for category in categories:
        for index, entry in enumerate(record[category]):
            statement = entry["statement"]
            previous = seen.get(statement)
            if previous is not None and previous != category:
                errors.append(
                    SocraticDiagnostic(
                        "BOUNDARY_CATEGORY_COLLISION",
                        f"the same statement appears in both {previous} and {category}",
                        ("record", category, index, "statement"),
                    )
                )
            else:
                seen[statement] = category

    if record["closure_status"] in {"Resolved", "Provisionally resolved"} and not record["closure_record_refs"]:
        errors.append(
            SocraticDiagnostic(
                "BOUNDARY_CLOSED_WITHOUT_CLOSURE_RECORD",
                "a closed epistemic boundary must reference the canonical evidence-closure record",
                ("record", "closure_record_refs"),
            )
        )


def validate_epistemic_boundary_binding(
    boundary_document: Mapping[str, Any],
    closure_snapshot: Mapping[str, Any],
) -> SocraticValidationResult:
    """Bind a derived boundary view to a resolved FAR closure snapshot.

    The caller resolves *all* closure_record_refs and constructs the snapshot from
    canonical closure and resolution records. The snapshot contains the same named
    fields as the boundary record, except its provenance and boundary_version.
    This comparison does not determine whether the canonical records are true.
    """
    result = validate_socratic_record(boundary_document)
    if not result.success:
        return result
    if boundary_document.get("record_type") != "EPISTEMIC_BOUNDARY":
        return SocraticValidationResult((SocraticDiagnostic(
            "BOUNDARY_BINDING_WRONG_TYPE", "binding requires an EPISTEMIC_BOUNDARY record",
        ),))
    boundary = boundary_document["record"]
    fields = tuple(key for key in boundary if key not in {"provenance", "boundary_version"})
    errors = []
    for field in fields:
        if field not in closure_snapshot or closure_snapshot[field] != boundary[field]:
            errors.append(SocraticDiagnostic(
                "BOUNDARY_CLOSURE_MISMATCH",
                f"resolved closure snapshot does not match boundary {field}",
                ("record", field),
            ))
    return SocraticValidationResult(tuple(errors))


def _check_commitment_refs(
    entries: Sequence[Mapping[str, Any]],
    label: str,
    code: str,
    commitment_ids: set[str],
    errors: list[SocraticDiagnostic],
) -> None:
    for index, entry in enumerate(entries):
        missing = [str(ref) for ref in entry["commitment_refs"] if str(ref) not in commitment_ids]
        if missing:
            errors.append(
                SocraticDiagnostic(
                    code,
                    f"{label} references unknown commitments {missing}",
                    ("record", label, index, "commitment_refs"),
                )
            )


def _check_elenchus(record: Mapping[str, Any], errors: list[SocraticDiagnostic]) -> None:
    question_ids = _check_unique_ids(record["question_events"], "question_events", errors)
    response_ids = _check_unique_ids(record["response_events"], "response_events", errors)
    commitment_ids = _check_unique_ids(record["commitments"], "commitments", errors)
    _check_unique_ids(record["definitions"], "definitions", errors)
    _check_unique_ids(record["assumptions"], "assumptions", errors)
    _check_unique_ids(record["warrants"], "warrants", errors)
    _check_unique_ids(record["derived_implications"], "derived_implications", errors)
    _check_unique_ids(record["tensions"], "tensions", errors)
    _check_unique_ids(record["contradictions"], "contradictions", errors)

    responses = {str(item["id"]): item for item in record["response_events"]}
    commitments = {str(item["id"]): item for item in record["commitments"]}
    question_times: dict[str, datetime] = {}
    response_times: dict[str, datetime] = {}

    for index, question in enumerate(record["question_events"]):
        question_id = str(question["id"])
        parsed = _parse_aware_datetime(question["timestamp"])
        if parsed is None:
            errors.append(
                SocraticDiagnostic(
                    "ELENCHUS_INVALID_QUESTION_TIMESTAMP",
                    "question timestamp must be a parseable timezone-aware date-time",
                    ("record", "question_events", index, "timestamp"),
                )
            )
        else:
            question_times[question_id] = parsed

    for index, response in enumerate(record["response_events"]):
        response_id = str(response["id"])
        question_id = str(response["question_id"])
        if question_id not in question_ids:
            errors.append(
                SocraticDiagnostic(
                    "ELENCHUS_RESPONSE_UNKNOWN_QUESTION",
                    f"response references unknown question {question_id}",
                    ("record", "response_events", index, "question_id"),
                )
            )

        response_time = _parse_aware_datetime(response["timestamp"])
        if response_time is None:
            errors.append(
                SocraticDiagnostic(
                    "ELENCHUS_INVALID_RESPONSE_TIMESTAMP",
                    "response timestamp must be a parseable timezone-aware date-time",
                    ("record", "response_events", index, "timestamp"),
                )
            )
        else:
            response_times[response_id] = response_time
            if question_id in question_times and response_time < question_times[question_id]:
                errors.append(
                    SocraticDiagnostic(
                        "ELENCHUS_RESPONSE_PREDATES_QUESTION",
                        f"response {response_id} predates its question {question_id}",
                        ("record", "response_events", index, "timestamp"),
                    )
                )

    for index, commitment in enumerate(record["commitments"]):
        if str(commitment["source_event_id"]) not in response_ids:
            errors.append(
                SocraticDiagnostic(
                    "ELENCHUS_COMMITMENT_UNKNOWN_SOURCE",
                    f"commitment references unknown response event {commitment['source_event_id']}",
                    ("record", "commitments", index, "source_event_id"),
                )
            )

    _check_commitment_refs(
        record["definitions"],
        "definitions",
        "ELENCHUS_DEFINITION_UNKNOWN_COMMITMENT",
        commitment_ids,
        errors,
    )
    _check_commitment_refs(
        record["assumptions"],
        "assumptions",
        "ELENCHUS_ASSUMPTION_UNKNOWN_COMMITMENT",
        commitment_ids,
        errors,
    )
    _check_commitment_refs(
        record["warrants"],
        "warrants",
        "ELENCHUS_WARRANT_UNKNOWN_COMMITMENT",
        commitment_ids,
        errors,
    )
    _check_commitment_refs(
        record["tensions"],
        "tensions",
        "ELENCHUS_TENSION_UNKNOWN_COMMITMENT",
        commitment_ids,
        errors,
    )

    for index, implication in enumerate(record["derived_implications"]):
        premise_refs = [str(ref) for ref in implication["premise_refs"]]
        missing = [ref for ref in premise_refs if ref not in commitment_ids]
        if missing:
            errors.append(
                SocraticDiagnostic(
                    "ELENCHUS_IMPLICATION_UNKNOWN_PREMISE",
                    f"derived implication references unknown commitments {missing}",
                    ("record", "derived_implications", index, "premise_refs"),
                )
            )

        bridge_by_premise: dict[str, str] = {}
        for bridge_index, bridge in enumerate(implication["context_bridges"]):
            premise_ref = str(bridge["premise_ref"])
            if premise_ref not in premise_refs:
                errors.append(
                    SocraticDiagnostic(
                        "ELENCHUS_IMPLICATION_BRIDGE_UNKNOWN_PREMISE",
                        f"context bridge references non-premise commitment {premise_ref}",
                        ("record", "derived_implications", index, "context_bridges", bridge_index, "premise_ref"),
                    )
                )
            if premise_ref in bridge_by_premise:
                errors.append(
                    SocraticDiagnostic(
                        "ELENCHUS_IMPLICATION_DUPLICATE_CONTEXT_BRIDGE",
                        f"more than one context bridge is supplied for premise {premise_ref}",
                        ("record", "derived_implications", index, "context_bridges", bridge_index, "premise_ref"),
                    )
                )
            bridge_by_premise[premise_ref] = str(bridge["bridge"])

        implication_context = str(implication["context"])
        for premise_ref in premise_refs:
            if premise_ref not in commitments:
                continue
            premise_context = str(commitments[premise_ref]["context"])
            if premise_context != implication_context and premise_ref not in bridge_by_premise:
                errors.append(
                    SocraticDiagnostic(
                        "ELENCHUS_IMPLICATION_CONTEXT_MISMATCH",
                        f"premise {premise_ref} has context {premise_context!r} but implication context is "
                        f"{implication_context!r} and no explicit bridge is recorded",
                        ("record", "derived_implications", index, "context"),
                    )
                )

    revision_sources: set[str] = set()
    revision_targets: set[str] = set()
    for index, revision in enumerate(record["revisions"]):
        source_id = str(revision["from_commitment_id"])
        target_id = str(revision["to_commitment_id"])
        response_id = str(revision["response_event_id"])

        if source_id in revision_sources:
            errors.append(
                SocraticDiagnostic(
                    "ELENCHUS_REVISION_SOURCE_REUSED",
                    f"commitment {source_id} is the source of more than one revision",
                    ("record", "revisions", index, "from_commitment_id"),
                )
            )
        revision_sources.add(source_id)

        if target_id in revision_targets:
            errors.append(
                SocraticDiagnostic(
                    "ELENCHUS_REVISION_TARGET_REUSED",
                    f"commitment {target_id} is the target of more than one revision",
                    ("record", "revisions", index, "to_commitment_id"),
                )
            )
        revision_targets.add(target_id)

        if source_id not in commitments or target_id not in commitments:
            errors.append(
                SocraticDiagnostic(
                    "ELENCHUS_REVISION_UNKNOWN_COMMITMENT",
                    f"revision references unknown commitment source={source_id} target={target_id}",
                    ("record", "revisions", index),
                )
            )
            continue
        if source_id == target_id:
            errors.append(
                SocraticDiagnostic(
                    "ELENCHUS_REVISION_OVERWRITES_HISTORY",
                    "a revision must create a new commitment id rather than overwrite the prior commitment",
                    ("record", "revisions", index),
                )
            )

        source = commitments[source_id]
        target = commitments[target_id]
        if source["status"] != "REVISED":
            errors.append(
                SocraticDiagnostic(
                    "ELENCHUS_REVISION_SOURCE_STATUS",
                    "the superseded commitment must remain recorded with status REVISED",
                    ("record", "commitments"),
                )
            )
        if int(target["version"]) <= int(source["version"]):
            errors.append(
                SocraticDiagnostic(
                    "ELENCHUS_REVISION_VERSION_ORDER",
                    "the replacement commitment version must be greater than the superseded version",
                    ("record", "revisions", index),
                )
            )
        if response_id not in responses:
            errors.append(
                SocraticDiagnostic(
                    "ELENCHUS_REVISION_UNKNOWN_RESPONSE",
                    f"revision references unknown response event {response_id}",
                    ("record", "revisions", index, "response_event_id"),
                )
            )
        else:
            if str(target["source_event_id"]) != response_id:
                errors.append(
                    SocraticDiagnostic(
                        "ELENCHUS_REVISION_TARGET_SOURCE_MISMATCH",
                        "the revision response event must be the source event of the replacement commitment",
                        ("record", "revisions", index, "response_event_id"),
                    )
                )
            source_response_id = str(source["source_event_id"])
            if (
                response_id in response_times
                and source_response_id in response_times
                and response_times[response_id] < response_times[source_response_id]
            ):
                errors.append(
                    SocraticDiagnostic(
                        "ELENCHUS_REVISION_PREDATES_SOURCE_COMMITMENT",
                        "the revision response event predates the response event that sourced the superseded commitment",
                        ("record", "revisions", index, "response_event_id"),
                    )
                )

    withdrawal_commitments: set[str] = set()
    for index, withdrawal in enumerate(record["withdrawals"]):
        commitment_id = str(withdrawal["commitment_id"])
        response_id = str(withdrawal["response_event_id"])
        if commitment_id in withdrawal_commitments:
            errors.append(
                SocraticDiagnostic(
                    "ELENCHUS_WITHDRAWAL_REPEATED",
                    f"commitment {commitment_id} has more than one withdrawal event",
                    ("record", "withdrawals", index, "commitment_id"),
                )
            )
        withdrawal_commitments.add(commitment_id)

        if commitment_id not in commitments:
            errors.append(
                SocraticDiagnostic(
                    "ELENCHUS_WITHDRAWAL_UNKNOWN_COMMITMENT",
                    f"withdrawal references unknown commitment {commitment_id}",
                    ("record", "withdrawals", index, "commitment_id"),
                )
            )
        else:
            commitment = commitments[commitment_id]
            if commitment["status"] != "WITHDRAWN":
                errors.append(
                    SocraticDiagnostic(
                        "ELENCHUS_WITHDRAWAL_STATUS",
                        "a withdrawn commitment must remain recorded with status WITHDRAWN",
                        ("record", "withdrawals", index, "commitment_id"),
                    )
                )
            source_response_id = str(commitment["source_event_id"])
            if (
                response_id in response_times
                and source_response_id in response_times
                and response_times[response_id] < response_times[source_response_id]
            ):
                errors.append(
                    SocraticDiagnostic(
                        "ELENCHUS_WITHDRAWAL_PREDATES_COMMITMENT",
                        "the withdrawal response event predates the response event that sourced the withdrawn commitment",
                        ("record", "withdrawals", index, "response_event_id"),
                    )
                )
        if response_id not in responses:
            errors.append(
                SocraticDiagnostic(
                    "ELENCHUS_WITHDRAWAL_UNKNOWN_RESPONSE",
                    f"withdrawal references unknown response event {response_id}",
                    ("record", "withdrawals", index, "response_event_id"),
                )
            )

    for index, commitment in enumerate(record["commitments"]):
        commitment_id = str(commitment["id"])
        if commitment["status"] == "REVISED" and commitment_id not in revision_sources:
            errors.append(
                SocraticDiagnostic(
                    "ELENCHUS_REVISED_COMMITMENT_WITHOUT_REVISION",
                    f"commitment {commitment_id} is marked REVISED without a revision event",
                    ("record", "commitments", index, "status"),
                )
            )
        if commitment["status"] == "WITHDRAWN" and commitment_id not in withdrawal_commitments:
            errors.append(
                SocraticDiagnostic(
                    "ELENCHUS_WITHDRAWN_COMMITMENT_WITHOUT_WITHDRAWAL",
                    f"commitment {commitment_id} is marked WITHDRAWN without a withdrawal event",
                    ("record", "commitments", index, "status"),
                )
            )

    for index, contradiction in enumerate(record["contradictions"]):
        missing = [str(ref) for ref in contradiction["commitment_refs"] if str(ref) not in commitments]
        if missing:
            errors.append(
                SocraticDiagnostic(
                    "ELENCHUS_CONTRADICTION_UNKNOWN_COMMITMENT",
                    f"contradiction references unknown commitments {missing}",
                    ("record", "contradictions", index, "commitment_refs"),
                )
            )


def validate_socratic_record(document: object) -> SocraticValidationResult:
    errors = _schema_errors(document)
    if errors or not isinstance(document, Mapping):
        return SocraticValidationResult(tuple(errors))

    record_type = document["record_type"]
    record = document["record"]
    if record_type == "EXPERTISE_ASSERTION":
        _check_expertise_assertion(record, errors)
    elif record_type == "EXPERTISE_APPLICABILITY":
        _check_expertise_applicability(record, errors)
    elif record_type == "EPISTEMIC_BOUNDARY":
        _check_epistemic_boundary(record, errors)
    elif record_type == "ELENCHUS_SESSION":
        _check_elenchus(record, errors)
    return SocraticValidationResult(tuple(errors))


def load_and_validate(path: str | Path) -> SocraticValidationResult:
    try:
        document = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return SocraticValidationResult((SocraticDiagnostic("UNREADABLE_RECORD", str(exc)),))
    return validate_socratic_record(document)


def main(argv: Sequence[str] | None = None) -> int:
    import argparse

    parser = argparse.ArgumentParser(prog="python -m mechanization.far_mechanization.socratic_epistemic")
    parser.add_argument("path")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    result = load_and_validate(args.path)
    if args.json:
        print(json.dumps({
            "success": result.success,
            "diagnostics": [
                {"code": item.code, "message": item.message, "path": list(item.path)}
                for item in result.diagnostics
            ],
        }, indent=2, sort_keys=True))
    else:
        print("PASS" if result.success else "FAIL")
        for diagnostic in result.diagnostics:
            print(f"{diagnostic.code}: {diagnostic.message}")
    return 0 if result.success else 1


if __name__ == "__main__":
    raise SystemExit(main())
