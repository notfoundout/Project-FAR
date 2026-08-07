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
PREREG = HERE / "preregistration-v1.0.json"
PLAN = HERE / "evidence-and-analysis-plan-v1.0.md"
GATE = HERE / "execution-gate-v1.0.json"
AMEND_SHA = "08065ca4b4878f77732e2a86c3beb99a18312bcf892c669ff1795eae172016c2"
README_SHA = "5f95525e501d8e86700f66a2d6a48d0bb6386bfc36b68f8ee7085f1323d1e355"
PREREG_BLOB = "7147f6814f76eb0f73fd0741b17b2501e38e6f57"
PLAN_BLOB = "15b352d54a524d9caf827018b608028c004f8f13"
REPL_DIGEST = "18babea600927a00669682937b0da60e5b4689f69e9c98e7e39ebe2a53f1ce2e"
ARITH_DIGEST = "df99660ed73f71757013a2cae39f2cb53b4ce3f9ec97bc7e6cf7557dfc70f653"
EXPECTED_AUTHORITY = {
    "base_design_head": "83c951aca9be6a09a4517044ae531a3ed1bcc9a9",
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


def load(path: Path) -> dict[str, Any]:
    raw = path.read_bytes()
    if raw.startswith(b"\xef\xbb\xbf"):
        raise AmendmentError("BOM")
    try:
        value = json.loads(
            raw.decode("utf-8"),
            object_pairs_hook=_pairs,
            parse_constant=_bad,
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise AmendmentError(f"invalid JSON: {path}") from exc
    if not isinstance(value, dict):
        raise AmendmentError("object required")
    return value


def digest(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            ensure_ascii=False,
            allow_nan=False,
        ).encode("utf-8")
    ).hexdigest()


def blob(raw: bytes) -> str:
    header = b"blob " + str(len(raw)).encode("ascii") + b"\x00"
    return hashlib.sha1(header + raw).hexdigest()


def validate(
    amend: Path = AMEND,
    readme: Path = README,
    prereg: Path = PREREG,
    plan: Path = PLAN,
    gate: Path = GATE,
) -> dict[str, Any]:
    if hashlib.sha256(amend.read_bytes()).hexdigest() != AMEND_SHA:
        raise AmendmentError("amendment bytes drifted")
    if hashlib.sha256(readme.read_bytes()).hexdigest() != README_SHA:
        raise AmendmentError("README bytes drifted")

    amendment = load(amend)
    authority = amendment.get("authority")
    identity = (
        amendment.get("schema_version"),
        amendment.get("program_id"),
        amendment.get("artifact_status"),
        amendment.get("amendment_status"),
    )
    if identity != (
        "1.1",
        "FAR-SWE-V3-001",
        "Research",
        "prospective_pre_execution_correction",
    ):
        raise AmendmentError("identity drifted")
    if authority != EXPECTED_AUTHORITY:
        raise AmendmentError("authority or precedence drifted")
    if blob(prereg.read_bytes()) != PREREG_BLOB or blob(plan.read_bytes()) != PLAN_BLOB:
        raise AmendmentError("base design identity drifted")
    if load(prereg).get("execution_authorized") is not False:
        raise AmendmentError("base execution authorized")
    gate_data = load(gate)
    if any(
        gate_data.get(key) is not False
        for key in (
            "execution_authorized",
            "model_calls_authorized",
            "benchmark_execution_authorized",
        )
    ):
        raise AmendmentError("gate open")

    replacement = amendment.get("replacement_contract", {})
    arithmetic = amendment.get("exact_arithmetic_contract", {})
    if digest(replacement) != REPL_DIGEST or digest(arithmetic) != ARITH_DIGEST:
        raise AmendmentError("contract drifted")

    classes = replacement.get("terminal_reason_classes", {})
    keys = {
        "infrastructure_invalid_replacement_eligible",
        "unresolved_nonreplaceable",
        "invalid_nonreplaceable",
    }
    if set(classes) != keys:
        raise AmendmentError("taxonomy keys")
    flat = [reason for reasons in classes.values() for reason in reasons]
    if len(flat) != len(set(flat)):
        raise AmendmentError("taxonomy overlap")
    if any("timeout" in reason for reason in classes["infrastructure_invalid_replacement_eligible"]):
        raise AmendmentError("timeout retry")
    if "provider_timeout_or_failure_after_request_acceptance" not in classes["unresolved_nonreplaceable"]:
        raise AmendmentError("provider rule")
    if "unclassified_terminal_reason" not in classes["invalid_nonreplaceable"]:
        raise AmendmentError("fallback")
    if (
        replacement.get("operator_discretion_permitted") is not False
        or replacement.get("replacement_attempts_per_eligible_slot") != 1
    ):
        raise AmendmentError("replacement discretion")
    if len(replacement.get("eligibility_facts_required_all_true", [])) != 5:
        raise AmendmentError("eligibility facts")
    if (
        "never retroactively reclassify"
        not in replacement.get("unlisted_terminal_reason_rule", "")
        or "never rerun the agent" not in replacement.get("grader_failure_rule", "")
    ):
        raise AmendmentError("preservation rules")

    if (
        "exact reduced rational" not in arithmetic.get("number_system", "")
        or "arbitrary-precision" not in arithmetic.get("number_system", "")
    ):
        raise AmendmentError("number system")
    if arithmetic.get("binary_outcome_encoding") != {"resolved": 1, "unresolved": 0}:
        raise AmendmentError("binary encoding")
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
    if (
        "no floating point" not in arithmetic.get("sorting_rule", "")
        or "never decision inputs"
        not in arithmetic.get("classification_comparison_rule", "")
    ):
        raise AmendmentError("floating point")
    return amendment


def probability(resolved: int, repetitions: int) -> Fraction:
    if (
        type(resolved) is not int
        or type(repetitions) is not int
        or repetitions <= 0
        or not 0 <= resolved <= repetitions
    ):
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
    print("PASS: amendment v1.1 exact-locked; execution blocked.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
