"""Recompute PCA-W4 native witnesses and verify their frozen far-ir/2.0 records."""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from copy import deepcopy
from fractions import Fraction
from pathlib import Path
from typing import Any, Mapping

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from mechanization.far_mechanization.contract_v2 import canonical_json, validate_contract

RESULTS = ROOT / "research" / "results" / "pca-w4-domain-contracts"
DOCS = ROOT / "docs" / "research" / "pca-w4-domain-contracts"

DOMAINS = {
    "formal-logic": ("formal_logic", "formal-logic.md", {"feitosa2001conservative"}),
    "bayesian-causal": (
        "bayesian_causal_reasoning",
        "bayesian-causal.md",
        {"blackwell1953equivalent", "beckers2019abstracting"},
    ),
    "argumentation": (
        "argumentation",
        "argumentation.md",
        {"prakken2010abstract", "modgil2014aspic"},
    ),
    "model-based-reasoning": (
        "model_based_reasoning",
        "model-based-reasoning.md",
        {"vanderschaft2004equivalence"},
    ),
    "type-theory": (
        "type_theory",
        "type-theory.md",
        {"pientka2020contextual", "angiuli2026principles"},
    ),
    "proof-theory": ("proof_theory", "proof-theory.md", {"dosen2003identity"}),
}
VARIANTS = {"lossy", "repaired"}


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def indexed(entries: list[Mapping[str, Any]]) -> dict[str, Any]:
    return {str(item["case_id"]): item["value"] for item in entries}


def probability_text(value: Fraction) -> str:
    return str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"


def distribution(rows: list[tuple[int, int, Fraction]]) -> list[dict[str, Any]]:
    masses: dict[tuple[int, int], Fraction] = {}
    for x, y, probability in rows:
        masses[(x, y)] = masses.get((x, y), Fraction(0)) + probability
    return [
        {"x": x, "y": y, "probability": probability_text(probability)}
        for (x, y), probability in sorted(masses.items())
        if probability != 0
    ]


def formal_logic(cases: list[Mapping[str, Any]]) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    behavior, lossy, repaired = {}, {}, {}
    valuations = [{"p": p, "q": q} for p in (False, True) for q in (False, True)]
    for case in cases:
        cid, theory = str(case["id"]), case["value"]["theory"]
        models = [v for v in valuations if all(v[atom] for atom in theory)]
        behavior[cid] = all(v["q"] for v in models)
        lossy[cid] = {"satisfiable": bool(models)}
        repaired[cid] = {"models": models}
    return behavior, lossy, repaired


def causal(cases: list[Mapping[str, Any]]) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    behavior, lossy, repaired = {}, {}, {}
    for case in cases:
        cid = str(case["id"])
        value = case["value"]
        equations = value["equations"]
        u_distribution: list[tuple[int, Fraction]] = []
        total_probability = Fraction(0)
        for row in value["u_distribution"]:
            u = int(row["u"])
            probability = Fraction(str(row["probability"]))
            if probability < 0:
                raise ValueError(f"{cid}: negative u_distribution probability")
            total_probability += probability
            u_distribution.append((u, probability))
        if total_probability != 1:
            raise ValueError(f"{cid}: u_distribution probabilities sum to {probability_text(total_probability)}, not 1")

        observational: list[tuple[int, int, Fraction]] = []
        intervened: list[tuple[int, int, Fraction]] = []
        for u, probability in u_distribution:
            if equations["X"] == "U":
                x, y = u, u
            else:
                y, x = u, u
            observational.append((x, y, probability))
            x_do = 0
            y_do = x_do if equations["Y"] == "X" else u
            intervened.append((x_do, y_do, probability))
        p_y1 = sum((probability for _, y, probability in intervened if y == 1), Fraction(0))
        behavior[cid] = {"numerator": p_y1.numerator, "denominator": p_y1.denominator}
        obs = distribution(observational)
        lossy[cid] = {"observational": obs}
        repaired[cid] = {"observational": obs, "do_X_0": distribution(intervened)}
    return behavior, lossy, repaired


def grounded_extension(arguments: list[str], defeats: list[list[str]]) -> list[str]:
    accepted: set[str] = set()
    while True:
        next_set = {
            arg
            for arg in arguments
            if all(
                any([defender, attacker] in defeats for defender in accepted)
                for attacker, target in defeats
                if target == arg
            )
        }
        if next_set == accepted:
            return sorted(accepted)
        accepted = next_set


def argumentation(cases: list[Mapping[str, Any]]) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    behavior, lossy, repaired = {}, {}, {}
    for case in cases:
        cid, value = str(case["id"]), case["value"]
        attacks, preference = value["attacks"], value["strict_preference"]
        defeats = [edge for edge in attacks if [edge[1], edge[0]] not in preference]
        behavior[cid] = grounded_extension(value["arguments"], defeats)
        lossy[cid] = {"arguments": value["arguments"], "attacks": attacks}
        repaired[cid] = {
            "arguments": value["arguments"],
            "attacks": attacks,
            "strict_preference": preference,
            "defeats": defeats,
        }
    return behavior, lossy, repaired


def model_based(cases: list[Mapping[str, Any]]) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    behavior, lossy, repaired = {}, {}, {}
    for case in cases:
        cid, value = str(case["id"]), case["value"]
        initial = value["initial"]
        step = next(t for t in value["transitions"] if t["from"] == initial and t["action"] == "a")
        behavior[cid] = [value["outputs"][initial], value["outputs"][step["to"]]]
        lossy[cid] = {"initial_output": value["outputs"][initial]}
        repaired[cid] = {
            "initial": initial,
            "transitions": value["transitions"],
            "outputs": value["outputs"],
        }
    return behavior, lossy, repaired


def type_theory(cases: list[Mapping[str, Any]]) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    behavior, lossy, repaired = {}, {}, {}
    for case in cases:
        cid, value = str(case["id"]), case["value"]
        behavior[cid] = value["context"].get(value["raw_term"]) == "Nat"
        lossy[cid] = {"raw_term": value["raw_term"]}
        repaired[cid] = {"raw_term": value["raw_term"], "context": value["context"]}
    return behavior, lossy, repaired


def contains_cut(tree: Mapping[str, Any]) -> bool:
    return tree["rule"] == "Cut" or any(contains_cut(premise) for premise in tree.get("premises", []))


def proof_theory(cases: list[Mapping[str, Any]]) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    behavior, lossy, repaired = {}, {}, {}
    for case in cases:
        cid, value = str(case["id"]), case["value"]
        behavior[cid] = not contains_cut(value)
        lossy[cid] = {"end_sequent": value["conclusion"]}
        repaired[cid] = deepcopy(value)
    return behavior, lossy, repaired


RECOMPUTERS = {
    "formal_logic": formal_logic,
    "bayesian_causal_reasoning": causal,
    "argumentation": argumentation,
    "model_based_reasoning": model_based,
    "type_theory": type_theory,
    "proof_theory": proof_theory,
}


def audit_document(document: Mapping[str, Any], root: Path = ROOT) -> list[dict[str, str]]:
    errors: list[dict[str, str]] = []
    for diagnostic in validate_contract(document).diagnostics:
        errors.append({"code": diagnostic.code, "message": diagnostic.message})

    contract = document.get("contract", {})
    domain = contract.get("extensions", {}).get("w4.domain")
    variant = contract.get("extensions", {}).get("w4.variant")
    if domain not in RECOMPUTERS:
        return errors + [{"code": "W4_UNKNOWN_DOMAIN", "message": str(domain)}]
    if variant not in VARIANTS:
        errors.append({"code": "W4_UNKNOWN_VARIANT", "message": str(variant)})

    cases = contract["source_domain"]["cases"]
    try:
        expected_behavior, expected_lossy, expected_repaired = RECOMPUTERS[domain](cases)
    except (KeyError, TypeError, ValueError, ZeroDivisionError) as exc:
        errors.append({"code": "W4_NATIVE_CASE_INVALID", "message": f"{domain}: {exc}"})
        return errors
    actual_behavior = indexed(contract["required_behavior"]["table"])
    if canonical_json(actual_behavior) != canonical_json(expected_behavior):
        errors.append({"code": "W4_NATIVE_BEHAVIOR_MISMATCH", "message": domain})

    actual_representation = indexed(contract["representation"]["table"])
    expected_representation = expected_lossy if variant == "lossy" else expected_repaired
    if canonical_json(actual_representation) != canonical_json(expected_representation):
        errors.append({"code": "W4_NATIVE_REPRESENTATION_MISMATCH", "message": domain})

    for source in document.get("provenance", {}).get("sources", []):
        source_path = root / source["path"]
        if not source_path.is_file():
            errors.append({"code": "W4_SOURCE_MISSING", "message": source["path"]})
        elif sha256_path(source_path) != source["sha256"]:
            errors.append({"code": "W4_SOURCE_HASH_MISMATCH", "message": source["path"]})
    return errors


def manifest_record_set_errors(artifact_manifest: Mapping[str, Any]) -> list[dict[str, str]]:
    expected_paths = {
        f"research/results/pca-w4-domain-contracts/{slug}-{variant}.json"
        for slug in DOMAINS
        for variant in VARIANTS
    }
    actual_paths = {str(item.get("path")) for item in artifact_manifest.get("records", [])}
    if actual_paths == expected_paths:
        return []
    return [{
        "code": "W4_MANIFEST_RECORD_SET_MISMATCH",
        "message": f"missing={sorted(expected_paths-actual_paths)} extra={sorted(actual_paths-expected_paths)}",
    }]


def validate_campaign(root: Path = ROOT) -> list[dict[str, str]]:
    errors: list[dict[str, str]] = []
    results = root / RESULTS.relative_to(ROOT)
    docs = root / DOCS.relative_to(ROOT)
    expected_files = {
        f"{slug}-{variant}.json" for slug in DOMAINS for variant in VARIANTS
    }
    actual_files = {path.name for path in results.glob("*.json") if path.name != "manifest.json"}
    if actual_files != expected_files:
        errors.append({
            "code": "W4_RECORD_SET_MISMATCH",
            "message": f"missing={sorted(expected_files-actual_files)} extra={sorted(actual_files-expected_files)}",
        })

    source_manifest = load_json(docs / "01-source-manifest.json")
    sources = source_manifest.get("sources", [])
    source_keys = [item["key"] for item in sources]
    if len(source_keys) != len(set(source_keys)):
        errors.append({"code": "W4_DUPLICATE_SOURCE_KEY", "message": "source keys must be unique"})
    dois = [item["doi"].lower() for item in sources if item.get("doi")]
    if len(dois) != len(set(dois)):
        errors.append({"code": "W4_DUPLICATE_DOI", "message": "DOIs must be unique"})
    bibliography = (docs / "references.bib").read_text(encoding="utf-8")
    for key in source_keys:
        if f"{{{key}," not in bibliography:
            errors.append({"code": "W4_BIBLIOGRAPHY_KEY_MISSING", "message": key})

    artifact_manifest = load_json(results / "manifest.json")
    errors.extend(manifest_record_set_errors(artifact_manifest))
    manifest_items = artifact_manifest.get("records", []) + artifact_manifest.get(
        "supporting_artifacts", []
    )
    manifest_paths = [item["path"] for item in manifest_items]
    if len(manifest_paths) != len(set(manifest_paths)):
        errors.append({"code": "W4_MANIFEST_DUPLICATE_PATH", "message": "artifact paths"})
    for item in manifest_items:
        path = root / item["path"]
        if not path.is_file():
            errors.append({"code": "W4_MANIFEST_ARTIFACT_MISSING", "message": item["path"]})
        elif sha256_path(path) != item["sha256"]:
            errors.append({"code": "W4_MANIFEST_HASH_MISMATCH", "message": item["path"]})

    for slug, (domain, memo_name, required_keys) in DOMAINS.items():
        memo = docs / "native" / memo_name
        if "FROZEN BEFORE CONTROLLED MAPPING" not in memo.read_text(encoding="utf-8"):
            errors.append({"code": "W4_NATIVE_MEMO_NOT_FROZEN", "message": memo.as_posix()})
        if not required_keys.issubset(set(source_keys)):
            errors.append({"code": "W4_REQUIRED_SOURCE_MISSING", "message": slug})

        pair = {}
        for variant in VARIANTS:
            path = results / f"{slug}-{variant}.json"
            if not path.is_file():
                continue
            document = load_json(path)
            pair[variant] = document
            errors.extend(
                {"code": item["code"], "message": f"{path.name}: {item['message']}"}
                for item in audit_document(document, root)
            )
            if document["contract"]["extensions"]["w4.domain"] != domain:
                errors.append({"code": "W4_DOMAIN_SLUG_MISMATCH", "message": path.name})

        if pair.keys() == VARIANTS:
            left, right = pair["lossy"]["contract"], pair["repaired"]["contract"]
            for key in (
                "source_domain",
                "required_behavior",
                "observation_contexts",
                "admitted_transformations",
                "interpretation_profile",
                "target_model_class",
                "frame",
            ):
                if canonical_json(left[key]) != canonical_json(right[key]):
                    errors.append({"code": "W4_PAIR_CONTRACT_DRIFT", "message": f"{slug}:{key}"})

    campaign = load_json(root / "research" / "campaigns" / "pca-w4-domain-contracts-v1.0.json")
    if campaign.get("status") != "COMPLETE_FINITE_EXPLICIT":
        errors.append({"code": "W4_CAMPAIGN_NOT_COMPLETE", "message": str(campaign.get("status"))})
    if campaign.get("results", {}).get("checked_lossy_collisions") != 6:
        errors.append({"code": "W4_CAMPAIGN_COUNT_MISMATCH", "message": "lossy collisions"})
    if campaign.get("results", {}).get("checked_repaired_factorizations") != 6:
        errors.append({"code": "W4_CAMPAIGN_COUNT_MISMATCH", "message": "repaired factorizations"})

    program = load_json(
        root
        / "theory"
        / "evaluation"
        / "post-closure-assurance-and-application-program-v1.0.json"
    )
    workstreams = {item["id"]: item for item in program["workstreams"]}
    if workstreams["PCA-W4-DOMAIN-CONTRACTS"]["state"] != "complete":
        errors.append({"code": "W4_PROGRAM_STATUS_DRIFT", "message": "W4 is not complete"})
    if workstreams["PCA-W5-APPROXIMATION-AND-COST"]["state"] == "complete":
        if program["next_action"]["workstream"] != "PCA-W6-EMPIRICAL-AUDIT-UTILITY":
            errors.append({"code": "W4_PROGRAM_STATUS_DRIFT", "message": "completed W5 does not advance to W6"})
    elif program["next_action"]["workstream"] != "PCA-W5-APPROXIMATION-AND-COST":
        errors.append({"code": "W4_PROGRAM_STATUS_DRIFT", "message": "incomplete W5 is not next"})

    current_authority = {
        "docs/CANONICAL_MAP.md": ["Records 13 formalized claims"],
        "docs/governance/claim-status-matrix.md": [
            "W2: 13 FORMALIZED",
            "PCA-W2-PROOF-ASSISTANT-FORMALIZATION` is active",
        ],
        "docs/governance/theorem-proof-status-register.md": [
            "13 claims are formalized",
            "PARTIAL/OBSTRUCTION in Lean",
        ],
        "docs/governance/limitations-register.md": [
            "has not been independently reviewed",
        ],
        "docs/governance/open-problems-register.md": [
            "| OP-23 | Independently review",
            "| OP-24 | Formalize the core",
            "| OP-25 | Implement a versioned",
            "| OP-26 | Develop independently",
        ],
    }
    for relative, stale_fragments in current_authority.items():
        text = (root / relative).read_text(encoding="utf-8")
        for fragment in stale_fragments:
            if fragment in text:
                errors.append({"code": "W4_STALE_AUTHORITY_TEXT", "message": f"{relative}: {fragment}"})
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    errors = validate_campaign()
    result = {
        "success": not errors,
        "records": len([path for path in RESULTS.glob("*.json") if path.name != "manifest.json"]),
        "diagnostics": errors,
    }
    if args.json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print("PASS" if not errors else "FAIL")
        for error in errors:
            print(f"{error['code']}: {error['message']}")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
