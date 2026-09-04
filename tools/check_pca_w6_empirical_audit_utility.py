"""Recompute and verify the governed PCA-W6 bounded audit-utility experiment."""
from __future__ import annotations

import copy
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any, Mapping

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from jsonschema import Draft202012Validator  # noqa: E402
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
VERIFIER_PATH = ROOT / "mechanization/far_mechanization/contract_v2.py"

EXPECTED_DOMAINS = (
    "argumentation",
    "bayesian-causal",
    "formal-logic",
    "model-based-reasoning",
    "proof-theory",
    "type-theory",
)

EXPECTED_W4_MANIFEST_METADATA = {
    "schema_version": "1.0",
    "campaign_id": "PCA-W4-DOMAIN-CONTRACTS-1.0",
    "base_commit": "3923fd88bb1549d816edcbdff66ce3412b7e80bc",
    "protocol_commit": "9638185b2f92913b3ce13ee2aaae5289e93945b1",
    "native_freeze_commit": "f823c4daf08b61241483bc1cc50d88d22746fa83",
    "mapping_commit": "8f8ad0a9b18f704a892c8bdb1b5fe304e18aae17",
}

EXPECTED_W4_RECORDS = (
    {"sha256": "4d2079d21a8ef9d94999ba4fda7100d10145c3512699e94fa6251bb07b543aec", "path": "research/results/pca-w4-domain-contracts/argumentation-lossy.json", "variant": "lossy", "expected_outcome": "REFUTED", "expected_evidence": "collision"},
    {"sha256": "1ac74ce88366e1e2f3e502831e98b2cd232116357e223f20e5f1d8f2297245b4", "path": "research/results/pca-w4-domain-contracts/argumentation-repaired.json", "variant": "repaired", "expected_outcome": "PROVED", "expected_evidence": "factorization"},
    {"sha256": "9828c6a72b9f999186636d6e9569f89a186689e44e4b087f12adc77994247a42", "path": "research/results/pca-w4-domain-contracts/bayesian-causal-lossy.json", "variant": "lossy", "expected_outcome": "REFUTED", "expected_evidence": "collision"},
    {"sha256": "68fdd6d206ec9d0aca8d7d32afccf671026dcd5c0f1554154e9bd35c5b25b8c8", "path": "research/results/pca-w4-domain-contracts/bayesian-causal-repaired.json", "variant": "repaired", "expected_outcome": "PROVED", "expected_evidence": "factorization"},
    {"sha256": "8071cdef4f44d069168735239190eedb743062321f223f24ad106790a7b5d4ad", "path": "research/results/pca-w4-domain-contracts/formal-logic-lossy.json", "variant": "lossy", "expected_outcome": "REFUTED", "expected_evidence": "collision"},
    {"sha256": "bb4451477becb1b4b8479a411290cad2489424907ccd88e17218b140804dc80f", "path": "research/results/pca-w4-domain-contracts/formal-logic-repaired.json", "variant": "repaired", "expected_outcome": "PROVED", "expected_evidence": "factorization"},
    {"sha256": "f8c919330a7620e6ac749a0b3437affcb11ad3a74d54e9de29bbba69552520da", "path": "research/results/pca-w4-domain-contracts/model-based-reasoning-lossy.json", "variant": "lossy", "expected_outcome": "REFUTED", "expected_evidence": "collision"},
    {"sha256": "e147f2b577a7340e8dd3bc582e250d9b4f5a1b1a16180ddb07858ada854b5c46", "path": "research/results/pca-w4-domain-contracts/model-based-reasoning-repaired.json", "variant": "repaired", "expected_outcome": "PROVED", "expected_evidence": "factorization"},
    {"sha256": "9cb7114370fbf7b561b308c5fdf31bfcb4107461483d9f1dfdeb2174d921bfd3", "path": "research/results/pca-w4-domain-contracts/proof-theory-lossy.json", "variant": "lossy", "expected_outcome": "REFUTED", "expected_evidence": "collision"},
    {"sha256": "4122b0d63007f62f2b24e49312589836e4f17364c1904b6d3068c455cb4734da", "path": "research/results/pca-w4-domain-contracts/proof-theory-repaired.json", "variant": "repaired", "expected_outcome": "PROVED", "expected_evidence": "factorization"},
    {"sha256": "4ca97cc26b14f2cae0c43486bfd4979ea4d024382db5e0418ef15f4ef17880fe", "path": "research/results/pca-w4-domain-contracts/type-theory-lossy.json", "variant": "lossy", "expected_outcome": "REFUTED", "expected_evidence": "collision"},
    {"sha256": "458eee9a3cbfac5688dd3c6d0105c3d2235f2c7feb5b65f65000e3e600caeab2", "path": "research/results/pca-w4-domain-contracts/type-theory-repaired.json", "variant": "repaired", "expected_outcome": "PROVED", "expected_evidence": "factorization"},
)

# Git blob identities read from the preregistered protocol base. This prevents
# the schema-only and FAR-semantic lanes from silently changing after freeze.
EXPECTED_PROTOCOL_BASE_BLOBS = {
    "schemas/far-contract-v2.schema.json": "e424359f804d268210e0f65fdf2fd28efc7e616b",
    "mechanization/far_mechanization/contract_v2.py": "31a4c00dcbee9adfe9e7c19fcacb4c04578e3b61",
}

EXPECTED_ARTIFACTS = (
    ".github/workflows/pca-w6.yml",
    "docs/governance/pca-w6-empirical-audit-utility-status-v1.0.md",
    "docs/research/pca-w6-empirical-audit-utility/00-preregistration.md",
    "docs/research/pca-w6-empirical-audit-utility/01-literature-and-design.md",
    "docs/research/pca-w6-empirical-audit-utility/02-execution-and-results.md",
    "docs/research/pca-w6-empirical-audit-utility/references.bib",
    "mechanization/far_mechanization/contract_v2.py",
    "research/results/pca-w4-domain-contracts/argumentation-lossy.json",
    "research/results/pca-w4-domain-contracts/argumentation-repaired.json",
    "research/results/pca-w4-domain-contracts/bayesian-causal-lossy.json",
    "research/results/pca-w4-domain-contracts/bayesian-causal-repaired.json",
    "research/results/pca-w4-domain-contracts/formal-logic-lossy.json",
    "research/results/pca-w4-domain-contracts/formal-logic-repaired.json",
    "research/results/pca-w4-domain-contracts/model-based-reasoning-lossy.json",
    "research/results/pca-w4-domain-contracts/model-based-reasoning-repaired.json",
    "research/results/pca-w4-domain-contracts/proof-theory-lossy.json",
    "research/results/pca-w4-domain-contracts/proof-theory-repaired.json",
    "research/results/pca-w4-domain-contracts/type-theory-lossy.json",
    "research/results/pca-w4-domain-contracts/type-theory-repaired.json",
    "research/results/pca-w4-domain-contracts/manifest.json",
    "research/results/pca-w6-empirical-audit-utility/results.json",
    "schemas/far-contract-v2.schema.json",
    "tests/test_cre001_semantics.py",
    "tests/test_pca_w6_empirical_audit_utility.py",
    "theory/evaluation/pca-w6-empirical-audit-utility-v1.0.json",
    "tools/check_pca_w4_domain_contracts.py",
    "tools/check_pca_w6_empirical_audit_utility.py",
    "tools/generate_next_tasks.py",
)


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_blob_sha1(path: Path) -> str:
    data = path.read_bytes()
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


def verify_protocol_base_dependencies() -> list[str]:
    errors: list[str] = []
    for rel, expected_blob in EXPECTED_PROTOCOL_BASE_BLOBS.items():
        path = ROOT / rel
        if not path.is_file():
            errors.append(f"missing protocol-base dependency: {rel}")
            continue
        actual_blob = git_blob_sha1(path)
        if actual_blob != expected_blob:
            errors.append(
                f"protocol-base dependency drift: {rel}: expected_blob={expected_blob} actual_blob={actual_blob}"
            )
    return errors


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
    """Identify pairwise material collisions without calling the FAR verifier."""
    contract = document["contract"]
    case_ids = [str(case["id"]) for case in contract["source_domain"]["cases"]]
    if len(case_ids) != len(set(case_ids)):
        raise ValueError("oracle source_domain contains duplicate case ids")
    behavior = _indexed_table(contract["required_behavior"]["table"])
    representation = _indexed_table(contract["representation"]["table"])
    if set(case_ids) != set(behavior) or set(case_ids) != set(representation):
        raise ValueError("oracle input tables do not cover the registered cases")
    for index, left in enumerate(case_ids):
        for right in case_ids[index + 1 :]:
            same_representation = canonical_json(representation[left]) == canonical_json(representation[right])
            different_behavior = canonical_json(behavior[left]) != canonical_json(behavior[right])
            if same_representation and different_behavior:
                return True
    return False


def inject_registered_collision(document: Mapping[str, Any]) -> dict[str, Any]:
    mutant = copy.deepcopy(document)
    contract = mutant["contract"]
    cases = [str(case["id"]) for case in contract["source_domain"]["cases"]]
    if len(cases) != 2 or len(set(cases)) != 2:
        raise ValueError(f"registered W6 mutation requires exactly two distinct cases, got {cases}")
    behavior = _indexed_table(contract["required_behavior"]["table"])
    if set(behavior) != set(cases):
        raise ValueError("required-behavior table does not exactly cover registered cases")
    if canonical_json(behavior[cases[0]]) == canonical_json(behavior[cases[1]]):
        raise ValueError("registered W6 mutation requires different required behaviors")
    rows = contract["representation"]["table"]
    by_case: dict[str, dict[str, Any]] = {}
    for row in rows:
        case_id = str(row["case_id"])
        if case_id in by_case:
            raise ValueError(f"duplicate representation case_id: {case_id}")
        by_case[case_id] = row
    if set(by_case) != set(cases):
        raise ValueError("representation table does not exactly cover registered cases")
    by_case[cases[1]]["value"] = copy.deepcopy(by_case[cases[0]]["value"])
    mutant["freeze"]["contract_sha256"] = contract_sha256(contract)
    return mutant


def validate_registered_corpus_manifest(manifest: Mapping[str, Any]) -> None:
    for key, expected in EXPECTED_W4_MANIFEST_METADATA.items():
        if manifest.get(key) != expected:
            raise ValueError(
                f"registered W4 manifest metadata drift: {key}: expected={expected!r} actual={manifest.get(key)!r}"
            )
    if manifest.get("records") != list(EXPECTED_W4_RECORDS):
        raise ValueError("registered W4 record projection drifted from the protocol-base corpus")


def _record_groups() -> dict[str, dict[str, Path]]:
    manifest = json.loads(W4_MANIFEST.read_text(encoding="utf-8"))
    validate_registered_corpus_manifest(manifest)
    groups: dict[str, dict[str, Path]] = {}
    for item in EXPECTED_W4_RECORDS:
        rel = item["path"]
        path = ROOT / rel
        if not path.is_file():
            raise ValueError(f"missing W4 record: {rel}")
        actual_hash = sha256(path)
        if actual_hash != item["sha256"]:
            raise ValueError(
                f"W4 protocol-base record hash mismatch: {rel}: expected={item['sha256']} actual={actual_hash}"
            )
        filename = path.name
        suffix = f"-{item['variant']}.json"
        if not filename.endswith(suffix):
            raise ValueError(f"W4 record filename/variant mismatch: {filename}")
        domain = filename[: -len(suffix)]
        if item["variant"] in groups.setdefault(domain, {}):
            raise ValueError(f"duplicate W4 domain/variant: {domain}/{item['variant']}")
        groups[domain][item["variant"]] = path
    if tuple(sorted(groups)) != EXPECTED_DOMAINS:
        raise ValueError(f"unexpected W4 domain set: {sorted(groups)}")
    for domain, variants in groups.items():
        if set(variants) != {"lossy", "repaired"}:
            raise ValueError(f"domain {domain} lacks exact lossy/repaired pair")
    return groups


def compute_results() -> dict[str, Any]:
    dependency_errors = verify_protocol_base_dependencies()
    if dependency_errors:
        raise ValueError("; ".join(dependency_errors))
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

        primary_items.append({
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
        })

        lossy = json.loads(groups[domain]["lossy"].read_text(encoding="utf-8"))
        lossy_audit = validate_contract(lossy)
        evidence = lossy["report"]["evidence"]
        secondary_items.append({
            "domain": domain,
            "schema_valid": _schema_valid(lossy),
            "audit_valid_checked_refutation": bool(
                lossy_audit.success
                and lossy["report"]["outcome"] == "REFUTED"
                and evidence["kind"] == "collision"
                and evidence["status"] == "CHECKED_FINITE_EXPLICIT"
            ),
            "oracle_material_collision": oracle_has_material_collision(lossy),
        })

    clean_count = len(primary_items)
    mutant_count = len(primary_items)
    baseline_true_positives = sum(1 for item in primary_items if not item["mutant"]["schema_valid"])
    baseline_true_negatives = sum(1 for item in primary_items if item["clean"]["schema_valid"])
    audit_true_positives = sum(
        1 for item in primary_items
        if not item["mutant"]["audit_valid"]
        and "FACTORIZATION_FAILURE" in item["mutant"]["audit_diagnostic_codes"]
    )
    audit_true_negatives = sum(1 for item in primary_items if item["clean"]["audit_valid"])
    primary_agreement = sum(
        1 for item in primary_items
        if (not item["mutant"]["audit_valid"]) == item["mutant"]["oracle_material_collision"]
    ) + sum(
        1 for item in primary_items
        if (not item["clean"]["audit_valid"]) == item["clean"]["oracle_material_collision"]
    )
    secondary_detected = sum(
        1 for item in secondary_items
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
            "population_inference": False,
            "p_values": False,
            "confidence_intervals": False,
            "reason": "finite project-authored exhaustive registered corpus; not a probability sample",
        },
        "independence": {
            "external_investigator": False,
            "human_participants": False,
            "human_disagreement_tested": False,
            "machine_oracle_independent_of_far_verifier": True,
        },
        "deviations": [],
        "terminal": {
            "bounded_material_loss_detection": "PROVED" if primary_pass and secondary_pass else "REFUTED",
            "human_disagreement_reduction": "UNDERDETERMINED",
            "external_real_world_utility": "OPEN",
            "core_theory_impact": "NONE",
        },
    }


def manifest_errors(manifest: object) -> list[str]:
    errors: list[str] = []
    if not isinstance(manifest, dict):
        return ["W6 manifest must be an object"]
    expected_top_level = {
        "schema_version", "campaign", "status", "protocol_freeze_commit", "protocol_base_commit", "artifacts"
    }
    if set(manifest) != expected_top_level:
        errors.append(
            f"W6 manifest top-level field mismatch expected={sorted(expected_top_level)} actual={sorted(manifest)}"
        )
    if manifest.get("schema_version") != "1.0":
        errors.append("W6 manifest schema version mismatch")
    if manifest.get("campaign") != "PCA-W6-EMPIRICAL-AUDIT-UTILITY":
        errors.append("W6 manifest campaign mismatch")
    if manifest.get("status") != "COMPLETE_BOUNDED_INTERNAL_CONTROL":
        errors.append("W6 manifest status mismatch")
    if manifest.get("protocol_freeze_commit") != PROTOCOL_FREEZE_COMMIT:
        errors.append("W6 manifest protocol freeze mismatch")
    if manifest.get("protocol_base_commit") != PROTOCOL_BASE_COMMIT:
        errors.append("W6 manifest protocol base mismatch")

    artifacts = manifest.get("artifacts")
    if not isinstance(artifacts, list):
        return errors + ["W6 manifest artifacts must be a list"]

    paths: list[str] = []
    malformed = False
    for index, item in enumerate(artifacts):
        if not isinstance(item, dict) or set(item) != {"path", "sha256"}:
            errors.append(f"W6 manifest artifact {index} must contain only path and sha256")
            malformed = True
            continue
        rel, digest = item["path"], item["sha256"]
        if not isinstance(rel, str) or not isinstance(digest, str):
            errors.append(f"W6 manifest artifact {index} has non-string path/hash")
            malformed = True
            continue
        paths.append(rel)
        if not re.fullmatch(r"[0-9a-f]{64}", digest):
            errors.append(f"W6 manifest artifact {rel} has invalid sha256")
            malformed = True
    if malformed:
        return errors
    if paths != list(EXPECTED_ARTIFACTS):
        errors.append(
            f"W6 manifest artifact set/order mismatch expected={list(EXPECTED_ARTIFACTS)} actual={paths}"
        )
        return errors
    for item in artifacts:
        rel = item["path"]
        path = ROOT / rel
        if not path.is_file():
            errors.append(f"W6 manifest missing artifact: {rel}")
            continue
        actual = sha256(path)
        if actual != item["sha256"]:
            errors.append(f"W6 manifest hash mismatch: {rel}: expected={item['sha256']} actual={actual}")
    return errors


def verify_manifest() -> list[str]:
    if not MANIFEST_PATH.is_file():
        return [f"missing W6 manifest: {MANIFEST_PATH.relative_to(ROOT)}"]
    try:
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return [f"unreadable W6 manifest: {exc}"]
    return manifest_errors(manifest)


def main() -> int:
    errors: list[str] = []
    errors.extend(verify_protocol_base_dependencies())
    if not RESULT_PATH.is_file():
        errors.append(f"missing W6 result: {RESULT_PATH.relative_to(ROOT)}")
    else:
        try:
            recorded = json.loads(RESULT_PATH.read_text(encoding="utf-8"))
            computed = compute_results()
        except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
            errors.append(f"W6 recomputation blocked: {exc}")
        else:
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
