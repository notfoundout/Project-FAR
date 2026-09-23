from __future__ import annotations

from datetime import datetime
from typing import Any, Iterable


class EpistemicAssuranceError(ValueError):
    """Raised when an epistemic-assurance record violates semantic constraints."""


DEPENDENT_RELATIONSHIPS = {"syndicated", "copied", "derived", "quoted", "mixed_derivation"}
INDEPENDENT_RELATIONSHIPS = {"origin", "independent"}


def _parse_time(value: str) -> datetime:
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except (TypeError, ValueError) as exc:
        raise EpistemicAssuranceError(f"invalid date-time: {value!r}") from exc


def validate_source_lineage(record: dict[str, Any]) -> dict[str, Any]:
    relationship = record.get("relationship")
    upstream = record.get("upstream_source_ids")
    roots = record.get("root_lineage_ids")
    if not isinstance(upstream, list):
        raise EpistemicAssuranceError("upstream_source_ids must be a list")
    if not isinstance(roots, list) or not roots:
        raise EpistemicAssuranceError("root_lineage_ids must be a non-empty list")
    if len(roots) != len(set(roots)):
        raise EpistemicAssuranceError("root_lineage_ids must be unique")
    if record.get("source_id") in upstream:
        raise EpistemicAssuranceError("source cannot be upstream of itself")
    if relationship in DEPENDENT_RELATIONSHIPS and not upstream:
        raise EpistemicAssuranceError("dependent relationship requires upstream source")
    if relationship in INDEPENDENT_RELATIONSHIPS and upstream:
        raise EpistemicAssuranceError("origin/independent relationship cannot declare upstream sources")
    if relationship in INDEPENDENT_RELATIONSHIPS and len(roots) != 1:
        raise EpistemicAssuranceError("origin/independent relationship requires exactly one root lineage")
    return record


def validate_source_lineage_set(records: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    items = [validate_source_lineage(record) for record in records]
    by_id: dict[str, dict[str, Any]] = {}
    for record in items:
        source_id = record.get("source_id")
        if not source_id:
            raise EpistemicAssuranceError("source_id is required")
        if source_id in by_id:
            raise EpistemicAssuranceError(f"duplicate source_id: {source_id}")
        by_id[source_id] = record

    for record in items:
        for upstream_id in record["upstream_source_ids"]:
            if upstream_id not in by_id:
                raise EpistemicAssuranceError(
                    f"unresolved upstream source {upstream_id!r} for {record['source_id']!r}"
                )

    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(source_id: str) -> None:
        if source_id in visiting:
            raise EpistemicAssuranceError(f"source-lineage cycle detected at {source_id}")
        if source_id in visited:
            return
        visiting.add(source_id)
        for upstream_id in by_id[source_id]["upstream_source_ids"]:
            visit(upstream_id)
        visiting.remove(source_id)
        visited.add(source_id)

    for source_id in by_id:
        visit(source_id)

    for record in items:
        if record["relationship"] in DEPENDENT_RELATIONSHIPS:
            expected: set[str] = set()
            for upstream_id in record["upstream_source_ids"]:
                expected.update(by_id[upstream_id]["root_lineage_ids"])
            actual = set(record["root_lineage_ids"])
            if actual != expected:
                raise EpistemicAssuranceError(
                    f"root_lineage_ids for {record['source_id']!r} must equal upstream lineage union"
                )
    return items


def validate_temporal_state(record: dict[str, Any]) -> dict[str, Any]:
    for field in ("valid_time", "known_time"):
        interval = record.get(field)
        if not isinstance(interval, dict) or not interval.get("start"):
            raise EpistemicAssuranceError(f"{field}.start is required")
        start = _parse_time(interval["start"])
        end_raw = interval.get("end")
        if end_raw is not None:
            end = _parse_time(end_raw)
            if end < start:
                raise EpistemicAssuranceError(f"{field}.end precedes start")
    if record.get("state") == "superseded" and not record.get("superseded_by_subject_ids"):
        raise EpistemicAssuranceError("superseded state requires superseded_by_subject_ids")
    return record


def validate_abstention(record: dict[str, Any]) -> dict[str, Any]:
    if not record.get("blocking_dimensions"):
        raise EpistemicAssuranceError("abstention requires at least one blocking dimension")
    if not record.get("reopen_conditions"):
        raise EpistemicAssuranceError("abstention requires at least one reopen condition")
    if not record.get("rationale"):
        raise EpistemicAssuranceError("abstention requires rationale")
    calibration = record.get("calibration")
    if calibration:
        target = calibration.get("coverage_target")
        observed = calibration.get("observed_coverage")
        if target is not None and not (0 < target <= 1):
            raise EpistemicAssuranceError("coverage_target must lie in (0,1]")
        if observed is not None and not (0 <= observed <= 1):
            raise EpistemicAssuranceError("observed_coverage must lie in [0,1]")
    return record


def validate_audit_assurance(record: dict[str, Any]) -> dict[str, Any]:
    checks = record.get("checks")
    required = {
        "source_integrity",
        "interpretation_fidelity",
        "search_coverage",
        "evidence_adjudication",
        "inference_adjudication",
        "reproducibility",
        "hostile_source_isolation",
    }
    if not isinstance(checks, dict):
        raise EpistemicAssuranceError("checks must be an object")
    missing = required - set(checks)
    if missing:
        raise EpistemicAssuranceError(f"missing assurance checks: {sorted(missing)}")

    statuses: dict[str, str | None] = {}
    any_limitations = False
    for name in required:
        check = checks[name]
        status = check.get("status")
        statuses[name] = status
        if status == "pass" and not check.get("evidence"):
            raise EpistemicAssuranceError(f"passed check {name!r} requires evidence")
        if check.get("limitations"):
            any_limitations = True

    overall = record.get("overall_status")
    if overall not in {"assured", "bounded", "not_assured", "abstain"}:
        raise EpistemicAssuranceError("overall_status must be assured, bounded, not_assured, or abstain")
    defeaters = bool(record.get("unresolved_defeaters"))
    if overall == "assured":
        bad = {k: v for k, v in statuses.items() if v not in {"pass", "not_applicable"}}
        if bad:
            raise EpistemicAssuranceError(f"assured status incompatible with checks: {bad}")
        if defeaters:
            raise EpistemicAssuranceError("assured status cannot retain unresolved defeaters")
    elif overall == "bounded":
        if "fail" in statuses.values():
            raise EpistemicAssuranceError("bounded status cannot contain a failed check")
        if not ({"unknown"} & set(statuses.values()) or defeaters or any_limitations):
            raise EpistemicAssuranceError("bounded status requires an unknown, defeater, or limitation")
    elif overall == "not_assured":
        if "fail" not in statuses.values():
            raise EpistemicAssuranceError("not_assured requires at least one failed check")
    elif overall == "abstain":
        if not ({"unknown", "fail"} & set(statuses.values()) or defeaters):
            raise EpistemicAssuranceError(
                "abstain requires an unknown/failed check or unresolved defeater"
            )
    return record
