"""Semantic validation for Project FAR Socratic epistemic extension records.

The JSON Schema checks structural shape. This module checks only relationships that
can be decided from one explicit record. It does not infer expertise, factual truth,
semantic completeness, or contradiction from natural-language content.
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
        if status == "MATCH" and expertise_value != claim_value and not assessment.get("bridge"):
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


def _check_epistemic_boundary(record: Mapping[str, Any], errors: list[SocraticDiagnostic]) -> None:
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

    questions = {str(item["id"]): item for item in record["question_events"]}
    responses = {str(item["id"]): item for item in record["response_events"]}
    commitments = {str(item["id"]): item for item in record["commitments"]}
    question_times: dict[str, datetime] = {}

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
        elif question_id in question_times and response_time < question_times[question_id]:
            errors.append(
                SocraticDiagnostic(
                    "ELENCHUS_RESPONSE_PREDATES_QUESTION",
                    f"response {response['id']} predates its question {question_id}",
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
        missing = [str(ref) for ref in implication["premise_refs"] if str(ref) not in commitment_ids]
        if missing:
            errors.append(
                SocraticDiagnostic(
                    "ELENCHUS_IMPLICATION_UNKNOWN_PREMISE",
                    f"derived implication references unknown commitments {missing}",
                    ("record", "derived_implications", index, "premise_refs"),
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
        elif str(target["source_event_id"]) != response_id:
            errors.append(
                SocraticDiagnostic(
                    "ELENCHUS_REVISION_TARGET_SOURCE_MISMATCH",
                    "the revision response event must be the source event of the replacement commitment",
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
        elif commitments[commitment_id]["status"] != "WITHDRAWN":
            errors.append(
                SocraticDiagnostic(
                    "ELENCHUS_WITHDRAWAL_STATUS",
                    "a withdrawn commitment must remain recorded with status WITHDRAWN",
                    ("record", "withdrawals", index, "commitment_id"),
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
