from __future__ import annotations

import argparse
import json
import subprocess
from fractions import Fraction
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
AMEND = HERE / "failure-arithmetic-amendment-v1.1.json"
README = HERE / "AMENDMENT-v1.1.md"
GATE = HERE / "execution-gate-v1.0.json"
BASE_HEAD = "83c951aca9be6a09a4517044ae531a3ed1bcc9a9"
PREREG_REL = "research/external-validation/swe-agent-v3/preregistration-v1.0.json"
PLAN_REL = "research/external-validation/swe-agent-v3/evidence-and-analysis-plan-v1.0.md"
PREREG_BLOB = "7147f6814f76eb0f73fd0741b17b2501e38e6f57"
PLAN_BLOB = "15b352d54a524d9caf827018b608028c004f8f13"
EXPECTED_AUTHORITY = {
    "base_design_head": BASE_HEAD,
    "base_preregistration_git_blob_sha1": PREREG_BLOB,
    "base_evidence_plan_git_blob_sha1": PLAN_BLOB,
    "superseded_paths": [
        "/analysis/invalid_run_and_cell_policy/replacement rule",
        "/analysis/bootstrap_interval_spec/arithmetic representation",
    ],
    "precedence": "For the two superseded subjects, this amendment controls over v1.0; every other v1.0 field remains unchanged.",
    "outcome_exposure_status": "none",
    "model_calls_authorized": False,
    "benchmark_execution_authorized": False,
    "execution_authorized": False,
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


def _decode(raw: bytes, label: str) -> dict[str, Any]:
    if raw.startswith(b"\xef\xbb\xbf"):
        raise AmendmentError(f"BOM: {label}")
    try:
        value = json.loads(raw.decode("utf-8"), object_pairs_hook=_pairs, parse_constant=_bad)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise AmendmentError(f"invalid JSON: {label}") from exc
    if not isinstance(value, dict):
        raise AmendmentError(f"object required: {label}")
    return value


def load(path: Path) -> dict[str, Any]:
    return _decode(path.read_bytes(), str(path))


def _git(*args: str) -> bytes:
    try:
        return subprocess.run(["git", "-C", str(ROOT), *args], check=True, capture_output=True).stdout
    except (OSError, subprocess.CalledProcessError) as exc:
        raise AmendmentError(
            "required historical Git object is unavailable; fetch full history with "
            "`git fetch --unshallow` (or explicitly fetch the named historical commit), "
            f"then retry: {' '.join(args)}"
        ) from exc


def historical_blob_id(head: str, relative: str) -> str:
    value = _git("rev-parse", f"{head}:{relative}").decode("ascii").strip()
    if len(value) != 40 or any(ch not in "0123456789abcdef" for ch in value):
        raise AmendmentError(f"invalid historical blob id: {relative}")
    return value


def historical_blob_bytes(head: str, relative: str) -> bytes:
    return _git("cat-file", "blob", f"{head}:{relative}")


def validate(amend: Path = AMEND, readme: Path = README, gate: Path = GATE) -> dict[str, Any]:
    amendment = load(amend)
    if (amendment.get("schema_version"), amendment.get("program_id"), amendment.get("artifact_status"), amendment.get("amendment_status")) != (
        "1.1", "FAR-SWE-V3-001", "Research", "prospective_pre_execution_correction"
    ):
        raise AmendmentError("identity drifted")
    if amendment.get("authority") != EXPECTED_AUTHORITY:
        raise AmendmentError("authority or precedence drifted")

    if historical_blob_id(BASE_HEAD, PREREG_REL) != PREREG_BLOB:
        raise AmendmentError("historical preregistration identity drifted")
    if historical_blob_id(BASE_HEAD, PLAN_REL) != PLAN_BLOB:
        raise AmendmentError("historical evidence-plan identity drifted")
    historical_prereg = _decode(historical_blob_bytes(BASE_HEAD, PREREG_REL), f"{BASE_HEAD}:{PREREG_REL}")
    if historical_prereg.get("execution_authorized") is not False:
        raise AmendmentError("historical base execution authorized")

    gate_data = load(gate)
    if any(gate_data.get(key) is not False for key in ("execution_authorized", "model_calls_authorized", "benchmark_execution_authorized")):
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
    if replacement.get("replacement_attempts_per_eligible_slot") != 1 or replacement.get("same_slot_and_conditions_required") is not True or replacement.get("replacement_before_any_outcome_reveal_required") is not True or replacement.get("operator_discretion_permitted") is not False:
        raise AmendmentError("replacement eligibility boundary drifted")
    eligibility = replacement.get("eligibility_facts_required_all_true")
    if not isinstance(eligibility, list) or len(eligibility) != 5 or len(set(eligibility)) != 5:
        raise AmendmentError("eligibility facts drifted")
    classes = replacement.get("terminal_reason_classes")
    expected_class_keys = {"infrastructure_invalid_replacement_eligible", "unresolved_nonreplaceable", "invalid_nonreplaceable"}
    if not isinstance(classes, dict) or set(classes) != expected_class_keys:
        raise AmendmentError("taxonomy keys")
    flat = [reason for reasons in classes.values() for reason in reasons]
    if len(flat) != len(set(flat)):
        raise AmendmentError("taxonomy overlap")
    if len(classes["infrastructure_invalid_replacement_eligible"]) != 5 or any("timeout" in reason for reason in classes["infrastructure_invalid_replacement_eligible"]):
        raise AmendmentError("replacement-eligible taxonomy drifted")
    if "provider_timeout_or_failure_after_request_acceptance" not in classes["unresolved_nonreplaceable"]:
        raise AmendmentError("provider post-acceptance rule drifted")
    if "unclassified_terminal_reason" not in classes["invalid_nonreplaceable"]:
        raise AmendmentError("unlisted fallback drifted")
    if "never retroactively reclassify" not in replacement.get("unlisted_terminal_reason_rule", ""):
        raise AmendmentError("unlisted reason preservation drifted")
    if "never rerun the agent" not in replacement.get("grader_failure_rule", ""):
        raise AmendmentError("grader failure rule drifted")
    if replacement.get("cell_rule") != "a retained invalid repetition makes the entire task-arm cell missing; unresolved repetitions remain valid binary zero outcomes and are never replaced":
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
    if arithmetic.get("tail_probabilities") != {"lower": {"numerator": 1, "denominator": 40}, "upper": {"numerator": 39, "denominator": 40}}:
        raise AmendmentError("tails")
    if arithmetic.get("classification_thresholds") != {"zero": {"numerator": 0, "denominator": 1}, "minimum_practical_difference": {"numerator": 1, "denominator": 10}}:
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


def classify(estimate: Fraction, lower: Fraction, upper: Fraction, missing: bool = False, critical_harm: bool = False) -> str:
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
    print("PASS: amendment v1.1 validated against immutable historical authority; execution blocked.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
