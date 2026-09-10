"""Bounded deterministic comparison and separately auditable adjudication.

This module does not determine truth. It validates two FAR evidence packages,
produces a mechanical comparison, and validates a distinct adjudication record.
All serialized artifacts are canonical JSON with stable content-derived IDs.
"""
from __future__ import annotations

import argparse
import hashlib
import math
import json
import re
import sys
from pathlib import Path
from typing import Any, Mapping, Sequence

PACKAGE_SCHEMA = "far-evidence-package/1.0"
COMPARISON_SCHEMA = "far-evidence-comparison/1.0"
ADJUDICATION_SCHEMA = "far-evidence-adjudication/1.0"

PACKAGE_CLAIM_BOUNDARY = "Mechanical comparison only; no truth, policy, or normative determination."
ADJUDICATION_CLAIM_BOUNDARY = "Human or policy adjudication record; not a truth certificate."

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
CLASSIFICATIONS = {"agreement", "contradiction", "left_only", "right_only", "unresolved"}

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
    "claim_boundary",
}
_DECISION_KEYS = {"finding_id", "disposition", "rationale", "support", "limitations"}
_COMPARISON_KEYS = {
    "schema",
    "comparison_id",
    "subject_match",
    "left",
    "right",
    "boundary_differences",
    "findings",
    "summary",
    "claim_boundary",
}
_FINDING_KEYS = {"finding_id", "claim_id", "classification", "left", "right", "mechanical_differences"}
_DIFF_KEYS = {
    "statement_equal",
    "status_equal",
    "support_only_left",
    "support_only_right",
    "assumptions_only_left",
    "assumptions_only_right",
    "boundaries_only_left",
    "boundaries_only_right",
}
_HEX64 = re.compile(r"^[0-9a-f]{64}$")


class InterfaceError(ValueError):
    """Fail-closed validation error for the v1.0 interface."""


def canonical_json_bytes(value: object) -> bytes:
    return (
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True, separators=(",", ": "), allow_nan=False)
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


def _require_sha256(value: Any, path: str) -> str:
    digest = _require_string(value, path)
    if _HEX64.fullmatch(digest) is None:
        raise InterfaceError(f"{path} must be a lowercase SHA-256 digest")
    return digest


def _reject_unknown_keys(value: Mapping[str, Any], allowed: set[str], path: str) -> None:
    unknown = sorted(set(value) - allowed)
    if unknown:
        raise InterfaceError(f"{path} contains unsupported fields: {', '.join(unknown)}")


def _require_exact_keys(value: Mapping[str, Any], expected: set[str], path: str) -> None:
    _reject_unknown_keys(value, expected, path)
    missing = sorted(expected - set(value))
    if missing:
        raise InterfaceError(f"{path} missing required fields: {', '.join(missing)}")


def _string_list(value: Any, path: str) -> list[str]:
    items = _require_list(value, path)
    result = [_require_string(item, f"{path}[{index}]") for index, item in enumerate(items)]
    if len(result) != len(set(result)):
        raise InterfaceError(f"{path} contains duplicates")
    return sorted(result)


def _metadata(value: Any, path: str) -> dict[str, Any]:
    mapping = dict(_require_mapping(value, path))
    for key, item in mapping.items():
        _require_string(key, f"{path} key")
        if not isinstance(item, (str, int, float, bool)) and item is not None:
            raise InterfaceError(f"{path}.{key} must be a JSON scalar")
        if isinstance(item, float) and not math.isfinite(item):
            raise InterfaceError(f"{path}.{key} must be a finite JSON scalar")
    return dict(sorted(mapping.items()))


def _normalize_claim(raw: Any, path: str) -> dict[str, Any]:
    claim = dict(_require_mapping(raw, path))
    _require_exact_keys(claim, _CLAIM_KEYS, path)
    claim_id = _require_string(claim["claim_id"], f"{path}.claim_id")
    status = _require_string(claim["status"], f"{path}.status")
    if status not in CLAIM_STATUSES:
        raise InterfaceError(f"{path}.status is unsupported: {status}")
    return {
        "claim_id": claim_id,
        "statement": _require_string(claim["statement"], f"{path}.statement"),
        "status": status,
        "support": _string_list(claim["support"], f"{path}.support"),
        "assumptions": _string_list(claim["assumptions"], f"{path}.assumptions"),
        "contradicts": _string_list(claim["contradicts"], f"{path}.contradicts"),
        "boundaries": _string_list(claim["boundaries"], f"{path}.boundaries"),
    }


def normalize_package(value: Any) -> dict[str, Any]:
    package = dict(_require_mapping(value, "package"))
    _reject_unknown_keys(package, _PACKAGE_KEYS, "package")
    required = {"schema", "package_id", "subject_id", "claims", "boundaries"}
    missing = sorted(required - set(package))
    if missing:
        raise InterfaceError(f"package missing required fields: {', '.join(missing)}")
    if package["schema"] != PACKAGE_SCHEMA:
        raise InterfaceError(f"package.schema must equal {PACKAGE_SCHEMA}")

    claims_raw = _require_list(package["claims"], "package.claims")
    if not claims_raw:
        raise InterfaceError("package.claims must contain at least one claim")
    claims = [_normalize_claim(raw, f"package.claims[{index}]") for index, raw in enumerate(claims_raw)]
    claim_ids = [claim["claim_id"] for claim in claims]
    if len(claim_ids) != len(set(claim_ids)):
        duplicate = next(item for item in claim_ids if claim_ids.count(item) > 1)
        raise InterfaceError(f"duplicate claim_id: {duplicate}")
    known = set(claim_ids)
    for claim in claims:
        invalid = sorted(set(claim["contradicts"]) - known)
        if invalid:
            raise InterfaceError(
                f"claim {claim['claim_id']} contradicts unknown claim IDs: {', '.join(invalid)}"
            )

    return {
        "schema": PACKAGE_SCHEMA,
        "package_id": _require_string(package["package_id"], "package.package_id"),
        "subject_id": _require_string(package["subject_id"], "package.subject_id"),
        "claims": sorted(claims, key=lambda item: item["claim_id"]),
        "boundaries": _string_list(package["boundaries"], "package.boundaries"),
        "metadata": _metadata(package.get("metadata", {}), "package.metadata"),
    }


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
    if left["status"] == "contradicted" or right["status"] == "contradicted" or left["statement"] != right["statement"]:
        return "contradiction"
    return "unresolved"


def _mechanical_differences(left: Mapping[str, Any] | None, right: Mapping[str, Any] | None) -> dict[str, Any]:
    return {
        "statement_equal": bool(left and right and left["statement"] == right["statement"]),
        "status_equal": bool(left and right and left["status"] == right["status"]),
        "support_only_left": sorted(set((left or {}).get("support", [])) - set((right or {}).get("support", []))),
        "support_only_right": sorted(set((right or {}).get("support", [])) - set((left or {}).get("support", []))),
        "assumptions_only_left": sorted(set((left or {}).get("assumptions", [])) - set((right or {}).get("assumptions", []))),
        "assumptions_only_right": sorted(set((right or {}).get("assumptions", [])) - set((left or {}).get("assumptions", []))),
        "boundaries_only_left": sorted(set((left or {}).get("boundaries", [])) - set((right or {}).get("boundaries", []))),
        "boundaries_only_right": sorted(set((right or {}).get("boundaries", [])) - set((left or {}).get("boundaries", []))),
    }


def compare_packages(left_value: Any, right_value: Any) -> dict[str, Any]:
    left = normalize_package(left_value)
    right = normalize_package(right_value)
    left_hash = artifact_sha256(left)
    right_hash = artifact_sha256(right)
    if left_hash == right_hash:
        raise InterfaceError("comparison requires two distinct canonical packages")

    left_claims = {claim["claim_id"]: claim for claim in left["claims"]}
    right_claims = {claim["claim_id"]: claim for claim in right["claims"]}
    findings = []
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
                "mechanical_differences": _mechanical_differences(left_claim, right_claim),
            }
        )

    counts: dict[str, int] = {}
    for finding in findings:
        classification = finding["classification"]
        counts[classification] = counts.get(classification, 0) + 1
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
        "claim_boundary": PACKAGE_CLAIM_BOUNDARY,
    }


def _normalize_package_ref(value: Any, path: str) -> dict[str, str]:
    mapping = dict(_require_mapping(value, path))
    _require_exact_keys(mapping, {"package_id", "sha256"}, path)
    return {
        "package_id": _require_string(mapping["package_id"], f"{path}.package_id"),
        "sha256": _require_sha256(mapping["sha256"], f"{path}.sha256"),
    }


def _normalize_string_diff(value: Any, path: str) -> dict[str, list[str]]:
    mapping = dict(_require_mapping(value, path))
    _require_exact_keys(mapping, {"only_left", "only_right"}, path)
    return {
        "only_left": _string_list(mapping["only_left"], f"{path}.only_left"),
        "only_right": _string_list(mapping["only_right"], f"{path}.only_right"),
    }


def normalize_comparison(value: Any) -> dict[str, Any]:
    comparison = dict(_require_mapping(value, "comparison"))
    _require_exact_keys(comparison, _COMPARISON_KEYS, "comparison")
    if comparison["schema"] != COMPARISON_SCHEMA:
        raise InterfaceError(f"comparison.schema must equal {COMPARISON_SCHEMA}")
    if comparison["claim_boundary"] != PACKAGE_CLAIM_BOUNDARY:
        raise InterfaceError("comparison.claim_boundary does not match the v1.0 boundary")
    if not isinstance(comparison["subject_match"], bool):
        raise InterfaceError("comparison.subject_match must be boolean")

    left_ref = _normalize_package_ref(comparison["left"], "comparison.left")
    right_ref = _normalize_package_ref(comparison["right"], "comparison.right")
    expected_comparison_id = _comparison_id(left_ref["sha256"], right_ref["sha256"])
    if comparison["comparison_id"] != expected_comparison_id:
        raise InterfaceError("comparison_id does not match the oriented package hashes")

    findings_raw = _require_list(comparison["findings"], "comparison.findings")
    findings: list[dict[str, Any]] = []
    claim_ids: set[str] = set()
    finding_ids: set[str] = set()
    counts: dict[str, int] = {}
    for index, raw in enumerate(findings_raw):
        path = f"comparison.findings[{index}]"
        finding = dict(_require_mapping(raw, path))
        _require_exact_keys(finding, _FINDING_KEYS, path)
        claim_id = _require_string(finding["claim_id"], f"{path}.claim_id")
        if claim_id in claim_ids:
            raise InterfaceError(f"comparison contains duplicate claim finding: {claim_id}")
        claim_ids.add(claim_id)
        finding_id = _require_string(finding["finding_id"], f"{path}.finding_id")
        if finding_id in finding_ids:
            raise InterfaceError(f"comparison contains duplicate finding ID: {finding_id}")
        finding_ids.add(finding_id)
        expected_finding_id = _finding_id(left_ref["sha256"], right_ref["sha256"], claim_id)
        if finding_id != expected_finding_id:
            raise InterfaceError(f"{path}.finding_id does not match package hashes and claim_id")
        classification = _require_string(finding["classification"], f"{path}.classification")
        if classification not in CLASSIFICATIONS:
            raise InterfaceError(f"{path}.classification is unsupported: {classification}")

        left_claim = None if finding["left"] is None else _normalize_claim(finding["left"], f"{path}.left")
        right_claim = None if finding["right"] is None else _normalize_claim(finding["right"], f"{path}.right")
        if left_claim is not None and left_claim["claim_id"] != claim_id:
            raise InterfaceError(f"{path}.left claim_id does not match finding claim_id")
        if right_claim is not None and right_claim["claim_id"] != claim_id:
            raise InterfaceError(f"{path}.right claim_id does not match finding claim_id")
        expected_classification = _classify(left_claim, right_claim)
        if classification != expected_classification:
            raise InterfaceError(f"{path}.classification does not match bounded claim records")

        differences = dict(_require_mapping(finding["mechanical_differences"], f"{path}.mechanical_differences"))
        _require_exact_keys(differences, _DIFF_KEYS, f"{path}.mechanical_differences")
        expected_differences = _mechanical_differences(left_claim, right_claim)
        if differences != expected_differences:
            raise InterfaceError(f"{path}.mechanical_differences do not match bounded claim records")

        findings.append(
            {
                "finding_id": finding_id,
                "claim_id": claim_id,
                "classification": classification,
                "left": left_claim,
                "right": right_claim,
                "mechanical_differences": expected_differences,
            }
        )
        counts[classification] = counts.get(classification, 0) + 1

    if [item["claim_id"] for item in findings] != sorted(item["claim_id"] for item in findings):
        raise InterfaceError("comparison findings are not in canonical claim order")
    summary = dict(_require_mapping(comparison["summary"], "comparison.summary"))
    for key, amount in summary.items():
        if key not in CLASSIFICATIONS or not isinstance(amount, int) or isinstance(amount, bool) or amount < 0:
            raise InterfaceError("comparison.summary contains an invalid classification count")
    expected_summary = dict(sorted(counts.items()))
    if summary != expected_summary:
        raise InterfaceError("comparison.summary does not match findings")

    return {
        "schema": COMPARISON_SCHEMA,
        "comparison_id": expected_comparison_id,
        "subject_match": comparison["subject_match"],
        "left": left_ref,
        "right": right_ref,
        "boundary_differences": _normalize_string_diff(comparison["boundary_differences"], "comparison.boundary_differences"),
        "findings": findings,
        "summary": expected_summary,
        "claim_boundary": PACKAGE_CLAIM_BOUNDARY,
    }


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
    supplied_boundary = adjudication.get("claim_boundary")
    if supplied_boundary not in (None, ADJUDICATION_CLAIM_BOUNDARY):
        raise InterfaceError("adjudication.claim_boundary does not match the v1.0 boundary")

    known_findings = {finding["finding_id"] for finding in comparison["findings"]}
    decisions_raw = _require_list(adjudication["decisions"], "adjudication.decisions")
    decisions: list[dict[str, Any]] = []
    seen: set[str] = set()
    for index, raw in enumerate(decisions_raw):
        path = f"adjudication.decisions[{index}]"
        decision = dict(_require_mapping(raw, path))
        _require_exact_keys(decision, _DECISION_KEYS, path)
        finding_id = _require_string(decision["finding_id"], f"{path}.finding_id")
        if finding_id not in known_findings:
            raise InterfaceError(f"{path} references unknown finding: {finding_id}")
        if finding_id in seen:
            raise InterfaceError(f"duplicate adjudication decision for finding: {finding_id}")
        seen.add(finding_id)
        disposition = _require_string(decision["disposition"], f"{path}.disposition")
        if disposition not in DISPOSITIONS:
            raise InterfaceError(f"{path}.disposition is unsupported: {disposition}")
        decisions.append(
            {
                "finding_id": finding_id,
                "disposition": disposition,
                "rationale": _require_string(decision["rationale"], f"{path}.rationale"),
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
        "adjudicator": _require_string(adjudication["adjudicator"], "adjudication.adjudicator"),
        "decisions": sorted(decisions, key=lambda item: item["finding_id"]),
        "dissent": _string_list(adjudication["dissent"], "adjudication.dissent"),
        "metadata": _metadata(adjudication.get("metadata", {}), "adjudication.metadata"),
        "claim_boundary": ADJUDICATION_CLAIM_BOUNDARY,
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
    parser = argparse.ArgumentParser(
        prog="far-evidence",
        description="Bounded FAR evidence compare/adjudicate interface v1.0",
    )
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
