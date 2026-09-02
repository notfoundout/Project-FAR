"""Recompute and verify the governed PCA-W6 bounded audit-utility experiment."""
from __future__ import annotations

import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any, Mapping

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from mechanization.far_mechanization.contract_v2 import (  # noqa: E402
    contract_sha256,
    validate_contract,
)

PROTOCOL_FREEZE_COMMIT = "3813b9e3eb49562bd8b9f4d3179c3d9536831de6"
PROTOCOL_BASE_COMMIT = "2cecf2e21cc27208f606dcd38337af4369e66af2"
W4_MANIFEST = ROOT / "research/results/pca-w4-domain-contracts/manifest.json"
RESULT_PATH = ROOT / "research/results/pca-w6-empirical-audit-utility/results.json"
MANIFEST_PATH = ROOT / "research/results/pca-w6-empirical-audit-utility/manifest.json"
SCHEMA_PATH = ROOT / "schemas/far-contract-v2.schema.json"
EXPECTED_DOMAINS = (
    "argumentation",
    "bayesian-causal",
    "formal-logic",
    "model-based-reasoning",
    "proof-theory",
    "type-theory",
)
EXPECTED_ARTIFACTS = (
    ".github/workflows/pca-w6.yml",
    "docs/governance/pca-w6-empirical-audit-utility-status-v1.0.md",
    "docs/research/pca-w6-empirical-audit-utility/00-preregistration.md",
    "docs/research/pca-w6-empirical-audit-utility/01-literature-and-design.md",
    "docs/research/pca-w6-empirical-audit-utility/02-execution-and-results.md",
    "docs/research/pca-w6-empirical-audit-utility/references.bib",
    "research/results/pca-w4-domain-contracts/manifest.json",
    "research/results/pca-w6-empirical-audit-utility/results.json",
    "tests/test_pca_w6_empirical_audit_utility.py",
    "theory/evaluation/pca-w6-empirical-audit-utility-v1.0.json",
    "tools/check_pca_w6_empirical_audit_utility.py",
)


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _schema_valid(document: object) -> bool:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    return not list(Draft202012Validator(schema).iter_errors(document))


def _indexed_table(rows: list[Mapping[str, Any]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for row in rows:
        case_id = str(row["case_id"])
        if case_id in result:
            raise ValueError(f"duplicate case_id in oracle input: {case_id}")
        result[case_id] = row["value"]
    return result


def oracle_has_material_collision(document: Mapping[str, Any]) -> bool:
    """Independent pairwise oracle: no FAR verifier and no report/evidence access."""
    contract = document["contract"]
    case_ids = [str(case["id"]) for case in contract["source_domain"]["cases"]]
    behavior = _indexed_table(contract["required_behavior"]["table"])
    representation = _indexed_table(contract["representation"]["table"])
    if set(case_ids) != set(behavior) or set(case_ids) != set(representation):
        raise ValueError("oracle input tables do not cover the registered cases")
    for index, left in enumerate(case_ids):
        for right in case_ids[index + 1 :]:
            same_representation = canonical_json(representation[left]) == canonical_json(
                representation[right]
            )
            different_behavior = canonical_json(behavior[left]) != canonical_json(
                behavior[right]
            )
            if same_representation and different_behavior:
                return True
    return False


def inject_registered_collision(document: Mapping[str, Any]) -> dict[str, Any]:
    mutant = copy.deepcopy(document)
    contract = mutant["contract"]
    cases = [str(case["id"]) for case in contract["source_domain"]["cases"]]
    if len(cases) != 2:
        raise ValueError(f"registered W6 mutation requires exactly two cases, got {len(cases)}")
    behavior = _indexed_table(contract["required_behavior"]["table"])
    if canonical_json(behavior[cases[0]]) == canonical_json(behavior[cases[1]]):
        raise ValueError("registered W6 mutation requires different required behaviors")
    rows = contract["representation"]["table"]
    by_case = {str(row["case_id"]): row for row in rows}
    if set(by_case) != set(cases):
        raise ValueError("representation table does not exactly cover registered cases")
    by_case[cases[1]]["value"] = copy.deepcopy(by_case[cases[0]]["value"])
    mutant["freeze"]["contract_sha256"] = contract_sha256(contract)
    return mutant


def _record_groups() -> dict[str, dict[str, Path]]:
    manifest = json.loads(W4_MANIFEST.read_text(encoding="utf-8"))
    groups: dict[str, dict[str, Path]] = {}
    for item in manifest["records"]:
        rel = str(item["path"])
        path = ROOT / rel
        if not path.is_file():
            raise ValueError(f"missing W4 record: {rel}")
        actual_hash = sha256(path)
        if actual_hash != item["sha256"]:
            raise ValueError(
                f"W4 record hash mismatch: {rel}: expected={item['sha256']} actual={actual_hash}"
            )
        filename = path.name
        suffix = f"-{item['variant']}.json"
        if not filename.endswith(suffix):
            raise ValueError(f"W4 record filename/variant mismatch: {filename}")
        domain = filename[: -len(suffix)]
        groups.setdefault(domain, {})[str(item["variant"])] = path
    if tuple(sorted(groups)) != EXPECTED_DOMAINS:
        raise ValueError(f"unexpected W4 domain set: {sorted(groups)}")
    for domain, variants in groups.items():
        if set(variants) != {"lossy", "repaired"}:
            raise ValueError(f"domain {domain} lacks exact lossy/repaired pair")
    return groups


def compute_results() -> dict[str, Any]:
    groups = _record_groups()
    primary_items: list[dict[str, Any]] = []
    secondary_items: list[dict[str, Any]] = []

    for domain in EXPECTED_DOMAINS:
        repaired = json.loads(groups[domain]["repaired"].read_text(encoding="utf-8"))
        clean_schema_valid = _schema_valid(repaired)
        clean_audit = validate_contract(repaired)
        clean_oracle_collision = oracle_has_material_collision(repaired)

        mutant = inject_registered_collision(repaired)
        mutant_schema_valid = _schema_valid(mutant)
        mutant_audit = validate_contract(mutant)
        mutant_codes = sorted({diagnostic.code for diagnostic in mutant_audit.diagnostics})
        mutant_oracle_collision = oracle_has_material_collision(mutant)

        primary_items.append(
            {
                "domain": domain,
                "clean": {
                    "schema_valid": clean_schema_valid,
                    "audit_valid": clean_audit.success,
                    "oracle_material_collision": clean_oracle_collision,
                },
                "mutant": {
                    "schema_valid": mutant_schema_valid,
                    "audit_valid": mutant_audit.success,
                    "audit_diagnostic_codes": mutant_codes,
                    "oracle_material_collision": mutant_oracle_collision,
                },
            }
        )

        lossy = json.loads(groups[domain]["lossy"].read_text(encoding="utf-8"))
        lossy_audit = validate_contract(lossy)
        evidence = lossy["report"]["evidence"]
        secondary_items.append(
            {
                "domain": domain,
                "schema_valid": _schema_valid(lossy),
                "audit_valid_checked_refutation": bool(
                    lossy_audit.success
                    and lossy["report"]["outcome"] == "REFUTED"
                    and evidence["kind"] == "collision"
                    and evidence["status"] == "CHECKED_FINITE_EXPLICIT"
                ),
                "oracle_material_collision": oracle_has_material_collision(lossy),
            }
        )

    clean_count = len(primary_items)
    mutant_count = len(primary_items)
    baseline_true_positives = sum(
        1 for item in primary_items if not item["mutant"]["schema_valid"]
    )
    baseline_true_negatives = sum(
        1 for item in primary_items if item["clean"]["schema_valid"]
    )
    audit_true_positives = sum(
        1
        for item in primary_items
        if not item["mutant"]["audit_valid"]
        and "FACTORIZATION_FAILURE" in item["mutant"]["audit_diagnostic_codes"]
    )
    audit_true_negatives = sum(
        1 for item in primary_items if item["clean"]["audit_valid"]
    )
    primary_agreement = sum(
        1
        for item in primary_items
        if (not item["mutant"]["audit_valid"])
        == item["mutant"]["oracle_material_collision"]
    ) + sum(
        1
        for item in primary_items
        if (not item["clean"]["audit_valid"])
        == item["clean"]["oracle_material_collision"]
    )

    secondary_detected = sum(
        1
        for item in secondary_items
        if item["schema_valid"]
        and item["audit_valid_checked_refutation"]
        and item["oracle_material_collision"]
    )

    primary_pass = all(
        item["clean"]["schema_valid"]
        and item["clean"]["audit_valid"]
        and not item["clean"]["oracle_material_collision"]
        and item["mutant"]["schema_valid"]
        and not item["mutant"]["audit_valid"]
        and "FACTORIZATION_FAILURE" in item["mutant"]["audit_diagnostic_codes"]
        and item["mutant"]["oracle_material_collision"]
        for item in primary_items
    )
    secondary_pass = secondary_detected == len(secondary_items)

    return {
        "schema_version": "1.0",
        "campaign": "PCA-W6-EMPIRICAL-AUDIT-UTILITY",
        "protocol_freeze_commit": PROTOCOL_FREEZE_COMMIT,
        "protocol_base_commit": PROTOCOL_BASE_COMMIT,
        "corpus": {
            "domains": list(EXPECTED_DOMAINS),
            "primary_negative_controls": clean_count,
            "primary_collision_mutants": mutant_count,
            "secondary_native_lossy_controls": len(secondary_items),
        },
        "primary": {
            "items": primary_items,
            "schema_only_baseline": {
                "true_positives": baseline_true_positives,
                "false_negatives": mutant_count - baseline_true_positives,
                "true_negatives": baseline_true_negatives,
                "false_positives": clean_count - baseline_true_negatives,
                "sensitivity": f"{baseline_true_positives}/{mutant_count}",
                "specificity": f"{baseline_true_negatives}/{clean_count}",
            },
            "far_semantic_audit": {
                "true_positives": audit_true_positives,
                "false_negatives": mutant_count - audit_true_positives,
                "true_negatives": audit_true_negatives,
                "false_positives": clean_count - audit_true_negatives,
                "sensitivity": f"{audit_true_positives}/{mutant_count}",
                "specificity": f"{audit_true_negatives}/{clean_count}",
            },
            "audit_oracle_agreement": f"{primary_agreement}/{clean_count + mutant_count}",
            "registered_all_items_claim": "PROVED" if primary_pass else "REFUTED",
        },
        "secondary": {
            "items": secondary_items,
            "native_lossy_controls_detected": f"{secondary_detected}/{len(secondary_items)}",
            "registered_control_claim": "PROVED" if secondary_pass else "REFUTED",
        },
        "analysis_policy": {
            "population_inference": false,
            "p_values": false,
            "confidence_intervals": false,
            "reason": "finite project-authored exhaustive registered corpus; not a probability sample",
        },
        "independence": {
            "external_investigator": false,
            "human_participants": false,
            "human_disagreement_tested": false,
            "machine_oracle_independent_of_far_verifier": true,
        },
        "deviations": [],
        "terminal": {
            "bounded_material_loss_detection": "PROVED" if primary_pass and secondary_pass else "REFUTED",
            "human_disagreement_reduction": "UNDERDETERMINED",
            "external_real_world_utility": "OPEN",
            "core_theory_impact": "NONE",
        },
    }


def verify_manifest() -> list[str]:
    errors: list[str] = []
    if not MANIFEST_PATH.is_file():
        return [f"missing W6 manifest: {MANIFEST_PATH.relative_to(ROOT)}"]
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    if manifest.get("campaign") != "PCA-W6-EMPIRICAL-AUDIT-UTILITY":
        errors.append("W6 manifest campaign mismatch")
    if manifest.get("protocol_freeze_commit") != PROTOCOL_FREEZE_COMMIT:
        errors.append("W6 manifest protocol freeze mismatch")
    artifacts = manifest.get("artifacts")
    if not isinstance(artifacts, list):
        return errors + ["W6 manifest artifacts must be a list"]
    paths = [item.get("path") for item in artifacts if isinstance(item, dict)]
    if paths != list(EXPECTED_ARTIFACTS):
        errors.append(
            f"W6 manifest artifact set/order mismatch expected={list(EXPECTED_ARTIFACTS)} actual={paths}"
        )
        return errors
    for item in artifacts:
        rel = str(item["path"])
        path = ROOT / rel
        if not path.is_file():
            errors.append(f"W6 manifest missing artifact: {rel}")
            continue
        actual = sha256(path)
        if actual != item.get("sha256"):
            errors.append(
                f"W6 manifest hash mismatch: {rel}: expected={item.get('sha256')} actual={actual}"
            )
    return errors


def main() -> int:
    errors: list[str] = []
    if not RESULT_PATH.is_file():
        errors.append(f"missing W6 result: {RESULT_PATH.relative_to(ROOT)}")
    else:
        recorded = json.loads(RESULT_PATH.read_text(encoding="utf-8"))
        computed = compute_results()
        if recorded != computed:
            errors.append(
                "W6 result recomputation mismatch\n"
                + json.dumps({"recorded": recorded, "computed": computed}, indent=2, sort_keys=True)
            )
    errors.extend(verify_manifest())
    if errors:
        print("\n".join(errors))
        return 1
    result = compute_results()
    print(
        "PCA-W6 PASS: "
        f"primary={result['primary']['registered_all_items_claim']} "
        f"secondary={result['secondary']['registered_control_claim']} "
        f"bounded_loss_detection={result['terminal']['bounded_material_loss_detection']} "
        f"human_disagreement={result['terminal']['human_disagreement_reduction']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
