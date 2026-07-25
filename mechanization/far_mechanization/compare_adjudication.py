"""Bounded deterministic comparison and separately auditable adjudication.

This module does not determine truth. It validates two FAR evidence packages,
produces a mechanical comparison, and validates a distinct adjudication record.
All serialized artifacts are canonical JSON with stable content-derived IDs.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

PACKAGE_SCHEMA = "far-evidence-package/1.0"
COMPARISON_SCHEMA = "far-evidence-comparison/1.0"
ADJUDICATION_SCHEMA = "far-evidence-adjudication/1.0"

CLAIM_STATUSES = {
    "observed",
    "derived",
    "inferred",
    "declared",
    "unknown",
    "contradicted",
    "unverifiable",
}
DISPOSITIONS = {
    "accept_left",
    "accept_right",
    "combine",
    "unresolved",
    "out_of_scope",
}

_PACKAGE_KEYS = {"schema", "package_id", "subject_id", "claims", "boundaries", "metadata"}
_CLAIM_KEYS = {
    "claim_id",
    "statement",
    "status",
    "support",
    "assumptions",
    "contradicts",
    "boundaries",
}
_ADJUDICATION_KEYS = {
    "schema",
    "adjudication_id",
    "comparison_sha256",
    "adjudicator",
    "decisions",
    "dissent",
    "metadata",
}
_DECISION_KEYS = {"finding_id", "disposition", "rationale", "support", "limitations"}


class InterfaceError(ValueError):
    """Fail-closed validation error for the v1.0 interface."""


def canonical_json_bytes(value: object) -> bytes:
    return (
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True, separators=(",", ": "))
        + "\n"
    ).encode("utf-8")


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def artifact_sha256(value: object) -> str:
    return sha256_bytes(canonical_json_bytes(value))


def _require_mapping(value: Any, path: str) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise InterfaceError(f"{path} must be an object")
    return value


def _require_list(value: Any, path: str) -> list[Any]:
    if not isinstance(value, list):
        raise InterfaceError(f"{path} must be an array")
    return value


def _require_string(value: Any, path: str, *, nonempty: bool = True) -> str:
    if not isinstance(value, str):
        raise InterfaceError(f"{path} must be a string")
    if nonempty and not value.strip():
        raise InterfaceError(f"{path} must not be empty")
    return value


def _reject_unknown_keys(value: Mapping[str, Any], allowed: set[str], path: str) -> None:
    unknown = sorted(set(value) - allowed)
    if unknown:
        raise InterfaceError(f"{path} contains unsupported fields: {', '.join(unknown)}")


def _string_list(value: Any, path: str) -> list[str]:
    items = _require_list(value, path)
    result = [_require_string(item, f"{path}[{index}]") for index, item in enumerate(items)]
    if len(result) != len(set(result)):
        raise InterfaceError(f"{path} contains duplicates")
    return sorted(result)


def _metadata(value: Any, path: str) -> dict[str, Any]:
    mapping = dict(_require_mapping(value, path))
    # Metadata is intentionally bounded to JSON scalar values. Nested structures
    # become an uncontrolled extension channel and are rejected in v1.0.
    for key, item in mapping.items():
        _require_string(key, f"{path} key")
        if not isinstance(item, (str, int, float, bool)) and item is not None:
            raise InterfaceError(f"{path}.{key} must be a JSON scalar")
    return dict(sorted(mapping.items()))


def normalize_package(value: Any) -> dict[str, Any]:
    package = dict(_require_mapping(value, "package"))
    _reject_unknown_keys(package, _PACKAGE_KEYS, "package")
    required = {"schema", "package_id", "subject_id", "claims", "boundaries"}
    missing = sorted(required - set(package))
    if missing:
        raise InterfaceError(f"package missing required fields: {', '.join(missing)}")
    if package["schema"] != PACKAGE_SCHEMA:
        raise InterfaceError(f"package.schema must equal {PACKAGE_SCHEMA}")

    package_id = _require_string(package["package_id"], "package.package_id")
    subject_id = _require_string(package["subject_id"], "package.subject_id")
    boundaries = _string_list(package["boundaries"], "package.boundaries")
    claims_raw = _require_list(package["claims"], "package.claims")
    if not claims_raw:
        raise InterfaceError("package.claims must contain at least one claim")

    claims: list[dict[str, Any]] = []
    seen: set[str] = set()
    for index, raw in enumerate(claims_raw):
        path = f"package.claims[{index}]"
        claim = dict(_require_mapping(raw, path))
        _reject_unknown_keys(claim, _CLAIM_KEYS, path)
        required_claim = {"claim_id", "statement", "status", "support", "assumptions", "contradicts", "boundaries"}
        missing_claim = sorted(required_claim - set(claim))
        if missing_claim:
            raise InterfaceError(f"{path} missing required fields: {', '.join(missing_claim)}")
        claim_id = _require_string(claim["claim_id"], f"{path}.claim_id")
        if claim_id in seen:
            raise InterfaceError(f"duplicate claim_id: {claim_id}")
        seen.add(claim_id)
        status = _require_string(claim["status"], f"{path}.status")
        if status not in CLAIM_STATUSES:
            raise InterfaceError(f"{path}.status is unsupported: {status}")
        claims.append(
            {
                "claim_id": claim_id,
                "statement": _require_string(claim["statement"], f"{path}.statement"),
                "status": status,
                "support": _string_list(claim["support"], f"{path}.support"),
                "assumptions": _string_list(claim["assumptions"], f"{path}.assumptions"),
                "contradicts": _string_list(claim["contradicts"], f"{path}.contradicts"),
                "boundaries": _string_list(claim["boundaries"], f"{path}.boundaries"),
            }
        )

    claim_ids = {claim["claim_id"] for claim in claims}
    for claim in claims:
        invalid = sorted(set(claim["contradicts"]) - claim_ids)
        if invalid:
            raise InterfaceError(
                f"claim {claim['claim_id']} contradicts unknown claim IDs: {', '.join(invalid)}"
            )

    normalized = {
        "schema": PACKAGE_SCHEMA,
        "package_id": package_id,
        "subject_id": subject_id,
        "claims": sorted(claims, key=lambda item: item["claim_id"]),
        "boundaries": boundaries,
        "metadata": _metadata(package.get("metadata", {}), "package.metadata"),
    }
    return normalized


def _finding_id(left_hash: str, right_hash: str, claim_id: str) -> str:
    material = f"{COMPARISON_SCHEMA}\0{left_hash}\0{right_hash}\0{claim_id}".encode("utf-8")
    return "finding-" + sha256_bytes(material)[:24]


def _comparison_id(left_hash: str, right_hash: str) -> str:
    material = f"{COMPARISON_SCHEMA}\0{left_hash}\0{right_hash}".encode("utf-8")
    return "comparison-" + sha256_bytes(material)[:24]


def _classify(left: Mapping[str, Any] | None, right: Mapping[str, Any] | None) -> str:
    if left is None:
        return "right_only"
    if right is None:
        return "left_only"
    if left["statement"] == right["statement"] and left["status"] == right["status"]:
        return "agreement"
    if (
        left["status"] == "contradicted"
        or right["status"] == "contradicted"
        or left["statement"] != right["statement"]
    ):
        return "contradiction"
    return "unresolved"


def compare_packages(left_value: Any, right_value: Any) -> dict[str, Any]:
    left = normalize_package(left_value)
    right = normalize_package(right_value)
    left_hash = artifact_sha256(left)
    right_hash = artifact_sha256(right)
    if left_hash == right_hash:
        raise InterfaceError("comparison requires two distinct canonical packages")

    left_claims = {claim["claim_id"]: claim for claim in left["claims"]}
    right_claims = {claim["claim_id"]: claim for claim in right["claims"]}
    findings: list[dict[str, Any]] = []
    for claim_id in sorted(set(left_claims) | set(right_claims)):
        left_claim = left_claims.get(claim_id)
        right_claim = right_claims.get(claim_id)
        findings.append(
            {
                "finding_id": _finding_id(left_hash, right_hash, claim_id),
                "claim_id": claim_id,
                "classification": _classify(left_claim, right_claim),
                "left": left_claim,
                "right": right_claim,
                "mechanical_differences": {
                    "statement_equal": bool(left_claim and right_claim and left_claim["statement"] == right_claim["statement"]),
                    "status_equal": bool(left_claim and right_claim and left_claim["status"] == right_claim["status"]),
                    "support_only_left": sorted(set((left_claim or {}).get("support", [])) - set((right_claim or {}).get("support", []))),
                    "support_only_right": sorted(set((right_claim or {}).get("support", [])) - set((left_claim or {}).get("support", []))),
                    "assumptions_only_left": sorted(set((left_claim or {}).get("assumptions", [])) - set((right_claim or {}).get("assumptions", []))),
                    "assumptions_only_right": sorted(set((right_claim or {}).get("assumptions", [])) - set((left_claim or {}).get("assumptions", []))),
                    "boundaries_only_left": sorted(set((left_claim or {}).get("boundaries", [])) - set((right_claim or {}).get("boundaries", []))),
                    "boundaries_only_right": sorted(set((right_claim or {}).get("boundaries", [])) - set((left_claim or {}).get("boundaries", []))),
                },
            }
        )

    counts: dict[str, int] = {}
    for finding in findings:
        key = finding["classification"]
        counts[key] = counts.get(key, 0) + 1

    return {
        "schema": COMPARISON_SCHEMA,
        "comparison_id": _comparison_id(left_hash, right_hash),
        "subject_match": left["subject_id"] == right["subject_id"],
        "left": {"package_id": left["package_id"], "sha256": left_hash},
        "right": {"package_id": right["package_id"], "sha256": right_hash},
        "boundary_differences": {
            "only_left": sorted(set(left["boundaries"]) - set(right["boundaries"])),
            "only_right": sorted(set(right["boundaries"]) - set(left["boundaries"])),
        },
        "findings": findings,
        "summary": dict(sorted(counts.items())),
        "claim_boundary": "Mechanical comparison only; no truth, policy, or normative determination.",
    }


def normalize_comparison(value: Any) -> dict[str, Any]:
    comparison = dict(_require_mapping(value, "comparison"))
    expected = {
        "schema", "comparison_id", "subject_match", "left", "right",
        "boundary_differences", "findings", "summary", "claim_boundary",
    }
    _reject_unknown_keys(comparison, expected, "comparison")
    if set(comparison) != expected:
        missing = sorted(expected - set(comparison))
        raise InterfaceError(f"comparison missing required fields: {', '.join(missing)}")
    if comparison["schema"] != COMPARISON_SCHEMA:
        raise InterfaceError(f"comparison.schema must equal {COMPARISON_SCHEMA}")
    _require_string(comparison["comparison_id"], "comparison.comparison_id")
    if not isinstance(comparison["subject_match"], bool):
        raise InterfaceError("comparison.subject_match must be boolean")
    _require_string(comparison["claim_boundary"], "comparison.claim_boundary")
    findings = _require_list(comparison["findings"], "comparison.findings")
    ids: list[str] = []
    for index, finding_raw in enumerate(findings):
        finding = _require_mapping(finding_raw, f"comparison.findings[{index}]")
        finding_id = _require_string(finding.get("finding_id"), f"comparison.findings[{index}].finding_id")
        ids.append(finding_id)
    if len(ids) != len(set(ids)):
        raise InterfaceError("comparison contains duplicate finding IDs")
    # The producer emits canonical ordering. Refuse reordered artifacts because
    # stable byte identity is part of the v1.0 contract.
    if ids != sorted(ids, key=lambda item: next(
        str(f["claim_id"]) for f in findings if f["finding_id"] == item
    )):
        raise InterfaceError("comparison findings are not in canonical claim order")
    return comparison


def adjudicate(comparison_value: Any, adjudication_value: Any) -> dict[str, Any]:
    comparison = normalize_comparison(comparison_value)
    comparison_hash = artifact_sha256(comparison)
    adjudication = dict(_require_mapping(adjudication_value, "adjudication"))
    _reject_unknown_keys(adjudication, _ADJUDICATION_KEYS, "adjudication")
    required = {"schema", "comparison_sha256", "adjudicator", "decisions", "dissent"}
    missing = sorted(required - set(adjudication))
    if missing:
        raise InterfaceError(f"adjudication missing required fields: {', '.join(missing)}")
    if adjudication["schema"] != ADJUDICATION_SCHEMA:
        raise InterfaceError(f"adjudication.schema must equal {ADJUDICATION_SCHEMA}")
    if adjudication["comparison_sha256"] != comparison_hash:
        raise InterfaceError("adjudication comparison_sha256 does not match comparison artifact")
    adjudicator = _require_string(adjudication["adjudicator"], "adjudication.adjudicator")
    dissent = _string_list(adjudication["dissent"], "adjudication.dissent")
    known_findings = {finding["finding_id"] for finding in comparison["findings"]}

    decisions_raw = _require_list(adjudication["decisions"], "adjudication.decisions")
    decisions: list[dict[str, Any]] = []
    seen: set[str] = set()
    for index, raw in enumerate(decisions_raw):
        path = f"adjudication.decisions[{index}]"
        decision = dict(_require_mapping(raw, path))
        _reject_unknown_keys(decision, _DECISION_KEYS, path)
        if set(decision) != _DECISION_KEYS:
            missing_decision = sorted(_DECISION_KEYS - set(decision))
            raise InterfaceError(f"{path} missing required fields: {', '.join(missing_decision)}")
        finding_id = _require_string(decision["finding_id"], f"{path}.finding_id")
        if finding_id not in known_findings:
            raise InterfaceError(f"{path} references unknown finding: {finding_id}")
        if finding_id in seen:
            raise InterfaceError(f"duplicate adjudication decision for finding: {finding_id}")
        seen.add(finding_id)
        disposition = _require_string(decision["disposition"], f"{path}.disposition")
        if disposition not in DISPOSITIONS:
            raise InterfaceError(f"{path}.disposition is unsupported: {disposition}")
        rationale = _require_string(decision["rationale"], f"{path}.rationale")
        if disposition == "unresolved" and not rationale:
            raise InterfaceError(f"{path}.rationale is required for unresolved disposition")
        decisions.append(
            {
                "finding_id": finding_id,
                "disposition": disposition,
                "rationale": rationale,
                "support": _string_list(decision["support"], f"{path}.support"),
                "limitations": _string_list(decision["limitations"], f"{path}.limitations"),
            }
        )

    missing_findings = sorted(known_findings - seen)
    if missing_findings:
        raise InterfaceError(
            "adjudication must explicitly decide every finding, including unresolved findings: "
            + ", ".join(missing_findings)
        )

    normalized = {
        "schema": ADJUDICATION_SCHEMA,
        "adjudication_id": "",
        "comparison_sha256": comparison_hash,
        "adjudicator": adjudicator,
        "decisions": sorted(decisions, key=lambda item: item["finding_id"]),
        "dissent": dissent,
        "metadata": _metadata(adjudication.get("metadata", {}), "adjudication.metadata"),
        "claim_boundary": "Human or policy adjudication record; not a truth certificate.",
    }
    id_material = dict(normalized)
    id_material.pop("adjudication_id")
    normalized["adjudication_id"] = "adjudication-" + artifact_sha256(id_material)[:24]

    supplied_id = adjudication.get("adjudication_id")
    if supplied_id not in (None, "", normalized["adjudication_id"]):
        raise InterfaceError("supplied adjudication_id does not match canonical content-derived ID")
    return normalized


def read_json(path: str | Path) -> Any:
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except OSError as exc:
        raise InterfaceError(f"unable to read {path}: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise InterfaceError(f"invalid JSON in {path}: {exc}") from exc


def write_json(path: str | Path, value: object, *, force: bool = False) -> None:
    target = Path(path)
    if target.exists() and not force:
        raise InterfaceError(f"refusing to overwrite existing file: {target}")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(canonical_json_bytes(value))


def _emit(value: object, output: str | None, force: bool) -> None:
    if output:
        write_json(output, value, force=force)
    else:
        sys.stdout.buffer.write(canonical_json_bytes(value))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="far-evidence", description="Bounded FAR evidence compare/adjudicate interface v1.0")
    sub = parser.add_subparsers(dest="command", required=True)

    validate = sub.add_parser("validate-package", help="validate and canonicalize one evidence package")
    validate.add_argument("package")
    validate.add_argument("--output-file")
    validate.add_argument("--force", action="store_true")

    compare = sub.add_parser("compare", help="mechanically compare two evidence packages")
    compare.add_argument("left")
    compare.add_argument("right")
    compare.add_argument("--output-file")
    compare.add_argument("--force", action="store_true")

    adjudicate_cmd = sub.add_parser("adjudicate", help="validate a separate adjudication record")
    adjudicate_cmd.add_argument("comparison")
    adjudicate_cmd.add_argument("adjudication")
    adjudicate_cmd.add_argument("--output-file")
    adjudicate_cmd.add_argument("--force", action="store_true")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        if args.command == "validate-package":
            result = normalize_package(read_json(args.package))
        elif args.command == "compare":
            result = compare_packages(read_json(args.left), read_json(args.right))
        else:
            result = adjudicate(read_json(args.comparison), read_json(args.adjudication))
        _emit(result, args.output_file, args.force)
        return 0
    except InterfaceError as exc:
        sys.stderr.write(f"far-evidence: {exc}\n")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
