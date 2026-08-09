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


def _type_exact_equal(actual: Any, expected: Any) -> bool:
    if type(actual) is not type(expected):
        return False
    if isinstance(expected, dict):
        return set(actual) == set(expected) and all(_type_exact_equal(actual[key], expected[key]) for key in expected)
    if isinstance(expected, list):
        return len(actual) == len(expected) and all(_type_exact_equal(a, b) for a, b in zip(actual, expected))
    return actual == expected


def _require_type_exact(actual: Any, expected: Any, label: str) -> None:
    if not _type_exact_equal(actual, expected):
        raise AmendmentError(f"type-exact contract mismatch: {label}")


def _git_blob_sha1(raw: bytes) -> str:
    return hashlib.sha1(f"blob {len(raw)}\0".encode("ascii") + raw).hexdigest()


def validate_historical_authority(path: Path = HISTORICAL_AUTHORITY) -> dict[str, Any]:
    authority = load(path)
    expected_keys = {
        "schema_version", "program_id", "artifact_status", "authority_status",
        "current_design_authority", "execution_authorized", "purpose",
        "claimed_historical_design_head", "provenance_status", "snapshots",
        "verification_rule", "external_provenance_rule", "immutability_rule", "nonclaims",
    }
    if set(authority) != expected_keys:
        raise AmendmentError("historical authority shape drifted")
    expected_identity = {
        "schema_version": "1.1",
        "program_id": "FAR-SWE-V3-001",
        "artifact_status": "Archive",
        "authority_status": "archival_context_not_live_authority",
        "current_design_authority": False,
        "execution_authorized": False,
        "claimed_historical_design_head": HISTORICAL_BASE_HEAD,
        "provenance_status": "not_self_proving",
    }
    for key, expected in expected_identity.items():
        if not _type_exact_equal(authority.get(key), expected):
            raise AmendmentError(f"historical archive identity/boundary drifted: {key}")
    expected_text = {
        "purpose": "Self-contained archival copies of two artifacts associated with the historical design reference 83c951aca9be6a09a4517044ae531a3ed1bcc9a9. They preserve review context only and are not an authority dependency for the current FAR-SWE-V3-001 design.",
        "verification_rule": "Verification proves only that the current archive bytes match the archived_git_blob_sha1 values recorded in this archive record. It does not prove that those bytes occurred at claimed_historical_design_head.",
        "external_provenance_rule": "Proving that an archived snapshot occurred at the claimed historical commit requires an independent external Git object/history or equivalent trusted provenance source. That proof is deliberately outside this self-contained archive and is not required for current experiment validity.",
        "immutability_rule": "Any archive-byte, archive-path, archived-blob-identity, or claimed historical-reference change creates a new archive version and cannot silently rewrite v1.1 archival context.",
    }
    for key, expected in expected_text.items():
        if authority.get(key) != expected:
            raise AmendmentError(f"historical archive semantic drift: {key}")
    _require_type_exact(authority.get("nonclaims"), [
        "This archive does not cryptographically prove that the snapshots came from claimed_historical_design_head.",
        "These snapshots do not restore historical files as current design authority.",
        "Current failure and arithmetic rules are validated independently of this archive.",
        "This archive does not authorize model calls, pilot execution, benchmark execution, confirmatory execution, grading, or outcome reveal.",
        "This archive does not establish that FAR improves software engineering.",
    ], "historical archive nonclaims")

    snapshots = authority.get("snapshots")
    if not isinstance(snapshots, list) or len(snapshots) != 2:
        raise AmendmentError("exactly two historical snapshots required")
    seen: set[str] = set()
    for entry in snapshots:
        if not isinstance(entry, dict) or set(entry) != {"path", "archived_git_blob_sha1", "claimed_historical_source_path"}:
            raise AmendmentError("historical snapshot entry shape drifted")
        rel = entry["path"]
        source = entry["claimed_historical_source_path"]
        expected_blob = entry["archived_git_blob_sha1"]
        if type(rel) is not str or rel in seen or EXPECTED_HISTORICAL_PATHS.get(rel) != source:
            raise AmendmentError("historical snapshot path/source drifted")
        if type(expected_blob) is not str or len(expected_blob) != 40 or any(ch not in "0123456789abcdef" for ch in expected_blob):
            raise AmendmentError("invalid archived snapshot blob identity")
        snapshot = HERE.parents[2] / rel
        if snapshot.is_symlink() or not snapshot.is_file():
            raise AmendmentError(f"historical snapshot missing: {rel}")
        if _git_blob_sha1(snapshot.read_bytes()) != expected_blob:
            raise AmendmentError(f"historical snapshot bytes drifted: {rel}")
        seen.add(rel)
    if seen != set(EXPECTED_HISTORICAL_PATHS):
        raise AmendmentError("historical snapshot set drifted")
    return authority

def validate(amend: Path = AMEND, readme: Path = README, gate: Path = GATE) -> dict[str, Any]:
    amendment = load(amend)
    if (
        amendment.get("schema_version"), amendment.get("program_id"),
        amendment.get("artifact_status"), amendment.get("amendment_status"),
    ) != ("1.3", "FAR-SWE-V3-001", "Research", "current_prospective_failure_and_arithmetic_contract"):
        raise AmendmentError("identity drifted")
    expected_authority = {
        "contract_role": "standalone_current_prospective_authority",
        "historical_context": "historical-authority-v1.0.json",
        "historical_provenance_required_for_current_validity": False,
        "governed_subjects": [
            "replacement eligibility and terminal-reason classification",
            "exact arithmetic for primary and bootstrap calculations and classification comparisons",
        ],
        "precedence": "For its governed subjects, this contract controls the current FAR-SWE-V3-001 design prospectively. The historical archive is explanatory context only and is not an authority dependency.",
        "outcome_exposure_status": "none",
        "model_calls_authorized": False,
        "benchmark_execution_authorized": False,
        "execution_authorized": False,
    }
    _require_type_exact(amendment.get("authority"), expected_authority, "current standalone failure/arithmetic authority")

    gate_data = load(gate)
    for key in ("execution_authorized", "model_calls_authorized", "benchmark_execution_authorized", "pilot_execution_authorized", "confirmatory_execution_authorized"):
        if type(gate_data.get(key)) is not bool or gate_data.get(key) is not False:
            raise AmendmentError(f"gate open or type drifted: {key}")

    replacement = amendment.get("replacement_contract")
    expected_replacement_keys = {
        "decision_order", "replacement_attempts_per_eligible_slot", "same_slot_and_conditions_required",
        "replacement_before_any_outcome_reveal_required", "operator_discretion_permitted",
        "eligibility_facts_required_all_true", "terminal_reason_classes", "unlisted_terminal_reason_rule",
        "grader_failure_rule", "cell_rule",
    }
    if not isinstance(replacement, dict) or set(replacement) != expected_replacement_keys:
        raise AmendmentError("replacement contract shape drifted")
    _require_type_exact(replacement.get("decision_order"), [
        "protocol_or_evidence_violation_invalid_nonreplaceable",
        "exact_pre_exposure_infrastructure_reason_with_all_eligibility_facts_true",
        "post_exposure_nonresolution_unresolved_nonreplaceable",
        "unlisted_reason_invalid_nonreplaceable",
    ], "replacement decision order")
    if type(replacement.get("replacement_attempts_per_eligible_slot")) is not int or replacement.get("replacement_attempts_per_eligible_slot") != 1:
        raise AmendmentError("replacement count drifted")
    for key, expected in (
        ("same_slot_and_conditions_required", True),
        ("replacement_before_any_outcome_reveal_required", True),
        ("operator_discretion_permitted", False),
    ):
        if type(replacement.get(key)) is not bool or replacement.get(key) is not expected:
            raise AmendmentError(f"replacement boolean drifted: {key}")
    _require_type_exact(replacement.get("eligibility_facts_required_all_true"), [
        "capsule_or_placebo_bytes_not_mounted_or_read",
        "no_model_request_accepted_by_provider",
        "no_repository_command_executed",
        "no_task_arm_output_or_grade_revealed",
        "failure_cause_is_indepent_of_task_arm_and_capsule_content",
    ], "replacement eligibility facts")
    expected_classes = {
        "infrastructure_invalid_replacement_eligible": [
            "pre_arm_workspace_provisioning_failure", "pre_arm_environment_image_start_failure",
            "pre_arm_provider_connection_refused", "pre_arm_provider_rate_limited", "pre_arm_evidence_store_unavailable",
        ],
        "unresolved_nonreplaceable": [
            "target_or_regression_test_failure", "patch_does_not_apply", "budget_exhausted",
            "agent_timeout_after_exposure", "provider_timeout_or_failure_after_request_acceptance",
            "harness_or_container_failure_after_exposure_with_complete_evidence", "no_patch_or_submission_failure",
            "other_agent_or_repository_failure_with_complete_evidence",
        ],
        "invalid_nonreplaceable": [
            "configuration_or_arm_access_mismatch", "information_barrier_or_task_leakage", "unauthorized_action",
            "required_evidence_missing_or_corrupt", "grader_integrity_failure",
            "harness_or_container_failure_after_exposure_with_incomplete_evidence", "unclassified_terminal_reason",
        ],
    }
    _require_type_exact(replacement.get("terminal_reason_classes"), expected_classes, "replacement terminal taxonomy")
    if replacement.get("unlisted_terminal_reason_rule") != "classify as invalid_nonreplaceable/unclassified_terminal_reason; preserve the run; stop further execution until a prospective amendment is frozen; never retroactively reclassify the run":
        raise AmendmentError("unlisted reason preservation drifted")
    if replacement.get("grader_failure_rule") != "retry grading against the same frozen evidence bundle; never rerun the agent solely because grading infrastructure failed":
        raise AmendmentError("grader preservation drifted")
    if replacement.get("cell_rule") != "a retained invalid repetition makes the entire task-arm cell missing; unresolved repetitions remain valid binary zero outcomes and are never replaced":
        raise AmendmentError("cell rule drifted")

    arithmetic = amendment.get("exact_arithmetic_contract")
    expected_arithmetic = {
        "number_system": "exact reduced rational arithmetic over arbitrary-precision signed integers",
        "canonical_representation": "numerator/denominator with denominator > 0, gcd(abs(numerator), denominator)=1, and zero represented as 0/1",
        "binary_outcome_encoding": {"resolved": 1, "unresolved": 0},
        "task_arm_probability": "sum of binary outcomes divided by the exact frozen repetition count, reduced exactly",
        "task_contrast": "p_i(far) - p_i(placebo) using exact rational subtraction",
        "primary_estimate": "sum of D_i divided by the exact number of complete primary tasks",
        "bootstrap_estimate": "for each resample, sum selected D_i values and divide by N using exact rational arithmetic",
        "sorting_rule": "compare a/b and c/d by arbitrary-precision cross multiplication a*d versus c*b; no floating point",
        "tail_probabilities": {"lower": {"numerator": 1, "denominator": 40}, "upper": {"numerator": 39, "denominator": 40}},
        "quantile_rule": "Hyndman-Fan type 7 with h=(m-1)*p computed as an exact rational; k=floor(h); f=h-k; q=(1-f)*x[k]+f*x[k+1], all exactly reduced",
        "classification_thresholds": {"zero": {"numerator": 0, "denominator": 1}, "minimum_practical_difference": {"numerator": 1, "denominator": 10}},
        "classification_comparison_rule": "all <, <=, >, and >= decisions use exact rational cross multiplication against 0/1 and 1/10; displayed decimals are never decision inputs",
        "display_rule": "decimal renderings are secondary, labeled approximations and rounded half-even to six places after the exact classification is fixed",
    }
    _require_type_exact(arithmetic, expected_arithmetic, "exact arithmetic contract")
    _require_type_exact(amendment.get("nonclaims"), [
        "This contract does not require the historical archive to prove its current validity.",
        "This contract does not authorize model calls, pilot execution, benchmark execution, or outcome reveal.",
        "This contract does not change the FAR treatment, task population, estimand, or decision categories.",
        "This contract does not establish that FAR improves software engineering.",
    ], "current contract nonclaims")

    narrative = readme.read_text(encoding="utf-8")
    for phrase in (
        "Execution authorized: **No**",
        "current machine-readable authority is now standalone",
        "`historical-authority-v1.0.json` is archival context only",
        "current failure/arithmetic validity does not depend on that claim",
        "Current authority for unrelated subjects comes from the current integrity-rooted design artifacts",
        "Any unlisted reason is invalid and nonreplaceable",
        "Floating-point values and displayed decimals never determine a classification",
    ):
        if phrase not in narrative:
            raise AmendmentError(f"amendment narrative boundary drifted: {phrase}")
    if "All other v1.0 design fields remain unchanged" in narrative:
        raise AmendmentError("stale amendment precedence claim survived")
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
    print("PASS: standalone failure/arithmetic authority validates; archival context is non-authoritative; execution blocked.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
