from __future__ import annotations

import argparse
import hashlib
import json
from fractions import Fraction
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
AMEND = HERE / "failure-arithmetic-amendment-v1.1.json"
README = HERE / "AMENDMENT-v1.1.md"
GATE = HERE / "execution-gate-v1.0.json"
HISTORICAL_AUTHORITY = HERE / "historical-authority-v1.0.json"
HISTORICAL_BASE_HEAD = "83c951aca9be6a09a4517044ae531a3ed1bcc9a9"
EXPECTED_HISTORICAL_PATHS = {
    "research/external-validation/swe-agent-v3/historical-base-83c951/preregistration-v1.0.json":
        "research/external-validation/swe-agent-v3/preregistration-v1.0.json",
    "research/external-validation/swe-agent-v3/historical-base-83c951/evidence-and-analysis-plan-v1.0.md":
        "research/external-validation/swe-agent-v3/evidence-and-analysis-plan-v1.0.md",
}


class AmendmentError(ValueError):
    pass


def _bad(token: str) -> Any:
    raise AmendmentError(f"non-finite JSON: {token}")


def _pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise AmendmentError(f"duplicate key: {key}")
        result[key] = value
    return result


def _decode(raw: bytes, label: str) -> Any:
    if raw.startswith(b"\xef\xbb\xbf"):
        raise AmendmentError(f"BOM: {label}")
    try:
        return json.loads(raw.decode("utf-8"), object_pairs_hook=_pairs, parse_constant=_bad)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise AmendmentError(f"invalid JSON: {label}") from exc


def load(path: Path) -> dict[str, Any]:
    if path.is_symlink() or not path.is_file():
        raise AmendmentError(f"regular file required: {path}")
    value = _decode(path.read_bytes(), str(path))
    if not isinstance(value, dict):
        raise AmendmentError(f"object required: {path}")
    return value


def _git_blob_sha1(raw: bytes) -> str:
    return hashlib.sha1(f"blob {len(raw)}\0".encode("ascii") + raw).hexdigest()


def validate_historical_authority(path: Path = HISTORICAL_AUTHORITY) -> dict[str, Any]:
    authority = load(path)
    expected_keys = {
        "schema_version", "program_id", "artifact_status", "authority_status",
        "current_design_authority", "execution_authorized", "purpose",
        "base_design_head", "snapshots", "verification_rule", "immutability_rule", "nonclaims",
    }
    if set(authority) != expected_keys:
        raise AmendmentError("historical authority shape drifted")
    if (
        authority.get("schema_version"), authority.get("program_id"),
        authority.get("artifact_status"), authority.get("authority_status"),
        authority.get("current_design_authority"), authority.get("execution_authorized"),
        authority.get("base_design_head"),
    ) != (
        "1.0", "FAR-SWE-V3-001", "Archive", "immutable_historical_evidence",
        False, False, HISTORICAL_BASE_HEAD,
    ):
        raise AmendmentError("historical authority identity/boundary drifted")
    if "not current Research design surfaces" not in authority.get("purpose", ""):
        raise AmendmentError("historical/current authority distinction drifted")
    if "Historical Git objects" not in authority.get("verification_rule", "") or "are not required" not in authority.get("verification_rule", ""):
        raise AmendmentError("self-contained historical verification rule drifted")
    if "cannot silently rewrite v1.0 authority" not in authority.get("immutability_rule", ""):
        raise AmendmentError("historical immutability rule drifted")

    snapshots = authority.get("snapshots")
    if not isinstance(snapshots, list) or len(snapshots) != 2:
        raise AmendmentError("exactly two historical snapshots required")
    seen: set[str] = set()
    historical_prereg: dict[str, Any] | None = None
    for entry in snapshots:
        if not isinstance(entry, dict) or set(entry) != {
            "path", "historical_git_blob_sha1", "historical_source_path"
        }:
            raise AmendmentError("historical snapshot entry shape drifted")
        rel = entry.get("path")
        source = entry.get("historical_source_path")
        expected_blob = entry.get("historical_git_blob_sha1")
        if type(rel) is not str or rel in seen or EXPECTED_HISTORICAL_PATHS.get(rel) != source:
            raise AmendmentError("historical snapshot path/source drifted")
        if type(expected_blob) is not str or len(expected_blob) != 40 or any(ch not in "0123456789abcdef" for ch in expected_blob):
            raise AmendmentError("invalid historical snapshot blob identity")
        snapshot = HERE.parents[2] / rel
        if snapshot.is_symlink() or not snapshot.is_file():
            raise AmendmentError(f"historical snapshot missing: {rel}")
        raw = snapshot.read_bytes()
        if _git_blob_sha1(raw) != expected_blob:
            raise AmendmentError(f"historical snapshot bytes drifted: {rel}")
        if source.endswith("preregistration-v1.0.json"):
            decoded = _decode(raw, rel)
            if not isinstance(decoded, dict):
                raise AmendmentError("historical preregistration must be object")
            historical_prereg = decoded
        seen.add(rel)
    if seen != set(EXPECTED_HISTORICAL_PATHS):
        raise AmendmentError("historical snapshot set drifted")
    if historical_prereg is None or historical_prereg.get("execution_authorized") is not False:
        raise AmendmentError("historical base execution boundary drifted")
    return authority


def validate(amend: Path = AMEND, readme: Path = README, gate: Path = GATE) -> dict[str, Any]:
    amendment = load(amend)
    if (
        amendment.get("schema_version"), amendment.get("program_id"),
        amendment.get("artifact_status"), amendment.get("amendment_status"),
    ) != ("1.2", "FAR-SWE-V3-001", "Research", "prospective_pre_execution_correction"):
        raise AmendmentError("identity drifted")
    authority = amendment.get("authority")
    expected_authority = {
        "historical_authority": "historical-authority-v1.0.json",
        "superseded_paths": [
            "/analysis/invalid_run_and_cell_policy/replacement rule",
            "/analysis/bootstrap_interval_spec/arithmetic representation",
        ],
        "precedence": "For the two superseded subjects, this amendment controls over the historical v1.0 design identified by historical-authority-v1.0.json; every other subject is governed by the current prospectively amended design artifacts.",
        "outcome_exposure_status": "none",
        "model_calls_authorized": False,
        "benchmark_execution_authorized": False,
        "execution_authorized": False,
    }
    if authority != expected_authority:
        raise AmendmentError("authority or precedence drifted")
    validate_historical_authority(HERE / authority["historical_authority"])

    gate_data = load(gate)
    if any(gate_data.get(key) is not False for key in (
        "execution_authorized", "model_calls_authorized", "benchmark_execution_authorized",
        "pilot_execution_authorized", "confirmatory_execution_authorized",
    )):
        raise AmendmentError("gate open")

    replacement = amendment.get("replacement_contract")
    if not isinstance(replacement, dict) or set(replacement) != {
        "decision_order", "replacement_attempts_per_eligible_slot", "same_slot_and_conditions_required",
        "replacement_before_any_outcome_reveal_required", "operator_discretion_permitted",
        "eligibility_facts_required_all_true", "terminal_reason_classes", "unlisted_terminal_reason_rule",
        "grader_failure_rule", "cell_rule",
    }:
        raise AmendmentError("replacement contract shape drifted")
    if replacement.get("decision_order") != [
        "protocol_or_evidence_violation_invalid_nonreplaceable",
        "exact_pre_exposure_infrastructure_reason_with_all_eligibility_facts_true",
        "post_exposure_nonresolution_unresolved_nonreplaceable",
        "unlisted_reason_invalid_nonreplaceable",
    ]:
        raise AmendmentError("replacement decision order drifted")
    if (
        replacement.get("replacement_attempts_per_eligible_slot") != 1
        or replacement.get("same_slot_and_conditions_required") is not True
        or replacement.get("replacement_before_any_outcome_reveal_required") is not True
        or replacement.get("operator_discretion_permitted") is not False
    ):
        raise AmendmentError("replacement eligibility boundary drifted")
    eligibility = replacement.get("eligibility_facts_required_all_true")
    if not isinstance(eligibility, list) or len(eligibility) != 5 or len(set(eligibility)) != 5:
        raise AmendmentError("eligibility facts drifted")
    classes = replacement.get("terminal_reason_classes")
    expected_class_keys = {
        "infrastructure_invalid_replacement_eligible", "unresolved_nonreplaceable", "invalid_nonreplaceable"
    }
    if not isinstance(classes, dict) or set(classes) != expected_class_keys:
        raise AmendmentError("taxonomy keys")
    if any(not isinstance(v, list) or any(type(x) is not str for x in v) for v in classes.values()):
        raise AmendmentError("taxonomy values")
    flat = [reason for reasons in classes.values() for reason in reasons]
    if len(flat) != len(set(flat)):
        raise AmendmentError("taxonomy overlap")
    if len(classes["infrastructure_invalid_replacement_eligible"]) != 5 or any(
        "timeout" in reason for reason in classes["infrastructure_invalid_replacement_eligible"]
    ):
        raise AmendmentError("replacement-eligible taxonomy drifted")
    if "provider_timeout_or_failure_after_request_acceptance" not in classes["unresolved_nonreplaceable"]:
        raise AmendmentError("provider post-acceptance rule drifted")
    if "unclassified_terminal_reason" not in classes["invalid_nonreplaceable"]:
        raise AmendmentError("unlisted fallback drifted")
    if "never retroactively reclassify" not in replacement.get("unlisted_terminal_reason_rule", ""):
        raise AmendmentError("unlisted reason preservation drifted")
    if "never rerun the agent" not in replacement.get("grader_failure_rule", ""):
        raise AmendmentError("grader failure rule drifted")
    if replacement.get("cell_rule") != (
        "a retained invalid repetition makes the entire task-arm cell missing; unresolved repetitions remain valid binary zero outcomes and are never replaced"
    ):
        raise AmendmentError("cell rule drifted")

    arithmetic = amendment.get("exact_arithmetic_contract")
    if not isinstance(arithmetic, dict) or set(arithmetic) != {
        "number_system", "canonical_representation", "binary_outcome_encoding", "task_arm_probability",
        "task_contrast", "primary_estimate", "bootstrap_estimate", "sorting_rule", "tail_probabilities",
        "quantile_rule", "classification_thresholds", "classification_comparison_rule", "display_rule",
    }:
        raise AmendmentError("exact arithmetic contract shape drifted")
    if "exact reduced rational" not in arithmetic.get("number_system", "") or "arbitrary-precision" not in arithmetic.get("number_system", ""):
        raise AmendmentError("number system")
    if "denominator > 0" not in arithmetic.get("canonical_representation", "") or "gcd" not in arithmetic.get("canonical_representation", ""):
        raise AmendmentError("rational canonicalization drifted")
    if arithmetic.get("binary_outcome_encoding") != {"resolved": 1, "unresolved": 0}:
        raise AmendmentError("binary encoding")
    for key in ("task_arm_probability", "task_contrast", "primary_estimate", "bootstrap_estimate", "quantile_rule"):
        if "exact" not in arithmetic.get(key, "").lower():
            raise AmendmentError(f"exact arithmetic rule drifted: {key}")
    if "no floating point" not in arithmetic.get("sorting_rule", ""):
        raise AmendmentError("floating point sorting")
    if arithmetic.get("tail_probabilities") != {
        "lower": {"numerator": 1, "denominator": 40},
        "upper": {"numerator": 39, "denominator": 40},
    }:
        raise AmendmentError("tails")
    if arithmetic.get("classification_thresholds") != {
        "zero": {"numerator": 0, "denominator": 1},
        "minimum_practical_difference": {"numerator": 1, "denominator": 10},
    }:
        raise AmendmentError("thresholds")
    if "never decision inputs" not in arithmetic.get("classification_comparison_rule", ""):
        raise AmendmentError("classification comparison drifted")
    if "classification is fixed" not in arithmetic.get("display_rule", ""):
        raise AmendmentError("display rule drifted")

    narrative = readme.read_text(encoding="utf-8")
    for phrase in (
        "Execution authorized: **No**",
        "It supersedes only:",
        "Any unlisted reason is invalid and nonreplaceable",
        "Floating-point values and displayed decimals never determine a classification",
    ):
        if phrase not in narrative:
            raise AmendmentError("amendment narrative boundary drifted")
    return amendment


def probability(resolved: int, repetitions: int) -> Fraction:
    if type(resolved) is not int or type(repetitions) is not int or repetitions <= 0 or not 0 <= resolved <= repetitions:
        raise AmendmentError("counts")
    return Fraction(resolved, repetitions)


def type7(values: list[Fraction], p: Fraction) -> Fraction:
    if not values or values != sorted(values) or not 0 <= p <= 1:
        raise AmendmentError("quantile input")
    h = Fraction(len(values) - 1) * p
    k = h.numerator // h.denominator
    f = h - k
    upper = min(k + 1, len(values) - 1)
    return (1 - f) * values[k] + f * values[upper]


def classify(
    estimate: Fraction,
    lower: Fraction,
    upper: Fraction,
    missing: bool = False,
    critical_harm: bool = False,
) -> str:
    if missing:
        return "inconclusive_due_to_missingness"
    if upper < 0:
        return "bounded_harm"
    if estimate >= Fraction(1, 10) and lower > 0 and not critical_harm:
        return "bounded_positive"
    if 0 <= upper < Fraction(1, 10):
        return "no_practical_advantage"
    return "inconclusive"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--amendment", type=Path, default=AMEND)
    parser.add_argument("--readme", type=Path, default=README)
    args = parser.parse_args()
    try:
        validate(args.amendment, args.readme)
    except AmendmentError as exc:
        print(f"FAIL: {exc}")
        return 1
    print("PASS: amendment v1.1 validates against self-contained historical authority; execution blocked.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
