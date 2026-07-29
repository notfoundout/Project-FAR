#!/usr/bin/env python3
"""Execute FAR-THEORY-DEPENDENCY-AUDIT-001 from hash-locked accepted sources."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
SPEC_PATH = ROOT / "research/theory-dependency-audit/execution-spec-v1.0.json"
RESULT_PATH = ROOT / "research/theory-dependency-audit/result-v1.0.json"


def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_candidate_primitives(text: str) -> list[str]:
    match = re.search(
        r"# Current Candidate Primitives\s+The current candidate primitive concepts are:\s+(.*?)\s+These concepts presently serve",
        text,
        flags=re.DOTALL,
    )
    if not match:
        return []
    return re.findall(r"^- (.+)$", match.group(1), flags=re.MULTILINE)


def contains_all(text: str, markers: list[str]) -> bool:
    lowered = text.lower()
    return all(marker.lower() in lowered for marker in markers)


def execute(spec: dict[str, Any] | None = None, *, root: Path = ROOT) -> dict[str, Any]:
    spec = spec or load_json(root / SPEC_PATH.relative_to(ROOT))
    source_locks = spec["source_locks"]
    sources: dict[str, str] = {}
    lock_results: dict[str, dict[str, Any]] = {}

    for relative, expected_sha in source_locks.items():
        path = root / relative
        if not path.is_file():
            raise FileNotFoundError(f"locked source missing: {relative}")
        data = path.read_bytes()
        actual_sha = git_blob_sha(data)
        lock_results[relative] = {
            "expected_git_blob_sha": expected_sha,
            "actual_git_blob_sha": actual_sha,
            "verified": actual_sha == expected_sha,
        }
        if actual_sha != expected_sha:
            raise ValueError(f"locked source drift: {relative}")
        sources[relative] = data.decode("utf-8")

    primitives = spec["candidate_primitives"]
    definitions = sources["theory/definitions/definitions.md"]
    primitive_registry = sources["frameworks/FARA/primitives.md"]
    formal_kernel = sources["frameworks/FARA/formal-kernel.md"]
    semantic_registry = json.loads(
        sources["docs/governance/semantic-consistency.json"]
    )
    framework_boundaries = sources["docs/governance/framework-boundaries.md"]
    derivation_matrix = sources["docs/governance/derivation-status-matrix.md"]
    far_dependency = sources["frameworks/FAR/dependency-graph.md"]
    faro_dependency = sources["frameworks/FARO/dependency-graph.md"]

    definition_headings = {
        primitive: f"## {primitive}" in definitions for primitive in primitives
    }
    c1_pass = contains_all(
        definitions,
        [
            "establishes the canonical terminology used throughout Project FAR",
            "The definitions contained in this document are canonical",
        ],
    ) and all(definition_headings.values())

    parsed_primitives = parse_candidate_primitives(primitive_registry)
    c2_pass = (
        parsed_primitives == primitives
        and "theory/definitions/definitions.md" in primitive_registry
        and "candidate primitive status is not evidence of irreducibility"
        in primitive_registry.lower()
    )

    semantic_candidates = {
        row["term"]: row
        for row in semantic_registry.get("canonical_terms", [])
        if row.get("status") == "candidate-primitive"
    }
    expected_terms = {primitive.lower() for primitive in primitives}
    registered_terms = set(semantic_candidates)
    all_registered = registered_terms == expected_terms
    split_fields_present = all(
        "definition_owner" in row and "classification_owner" in row
        for row in semantic_candidates.values()
    ) if semantic_candidates else False
    c3_pass = all_registered and split_fields_present

    c4_pass = contains_all(
        formal_kernel,
        [
            "Status: **Accepted**",
            "finite, explicit, auditable representational architectures in Project FAR v1.0",
            "The formal carrier names do not reclassify FARA's seven candidate primitives.",
            "This kernel selection does not establish their global independence, necessity, minimality, or irreducibility.",
        ],
    )

    far_contract_markers = contains_all(
        far_dependency,
        [
            "FARA provides the architecture used by FAR",
            "FAR applies these architectural concepts methodologically",
            "It does not modify their definitions",
        ],
    )
    far_non_derivation_markers = contains_all(
        framework_boundaries,
        ["that its procedural choices are FARA theorems"],
    ) and contains_all(
        derivation_matrix,
        ["FAR staged/multi-pass workflow", "compatible independent methodology"],
    )
    c5_pass = far_contract_markers and far_non_derivation_markers

    faro_contract_markers = contains_all(
        faro_dependency,
        [
            "Supplies representational architecture",
            "Supplies stable investigation methodology",
        ],
    )
    faro_non_derivation_markers = contains_all(
        framework_boundaries,
        ["that operational choices follow necessarily from FARA/FAR"],
    ) and contains_all(
        derivation_matrix,
        ["operational audit/comparison/reporting", "compatible independent operations"],
    )
    c6_pass = faro_contract_markers and faro_non_derivation_markers

    c7_pass = contains_all(
        derivation_matrix,
        [
            "canonicalization and CIR",
            "independent design choice",
            "Pareto comparison / CIR cost metrics",
            "independent decision rule",
            "preregistration and frozen evidence",
            "governance rule",
            "fail reports and uncertainty outputs",
            "governance/usability choice",
        ],
    )

    checks = [
        {
            "id": "C1",
            "name": "canonical_definition_authority",
            "status": "Pass" if c1_pass else "Fail",
            "measurements": {
                "authority_markers_present": contains_all(
                    definitions,
                    [
                        "establishes the canonical terminology used throughout Project FAR",
                        "The definitions contained in this document are canonical",
                    ],
                ),
                "definition_headings": definition_headings,
            },
        },
        {
            "id": "C2",
            "name": "fara_candidate_classification",
            "status": "Pass" if c2_pass else "Fail",
            "measurements": {
                "parsed_candidate_primitives": parsed_primitives,
                "definitions_pointer_present": "theory/definitions/definitions.md"
                in primitive_registry,
                "irreducibility_nonclaim_present": "candidate primitive status is not evidence of irreducibility"
                in primitive_registry.lower(),
            },
        },
        {
            "id": "C3",
            "name": "undifferentiated_registry_adequacy",
            "status": "Pass" if c3_pass else "Fail",
            "measurements": {
                "expected_candidate_primitive_terms": sorted(expected_terms),
                "registered_candidate_primitive_terms": sorted(registered_terms),
                "all_seven_registered": all_registered,
                "separate_definition_and_classification_fields_present": split_fields_present,
            },
        },
        {
            "id": "C4",
            "name": "formal_kernel_role_boundary",
            "status": "Pass" if c4_pass else "Fail",
            "measurements": {
                "accepted_scope_marker": contains_all(
                    formal_kernel,
                    [
                        "Status: **Accepted**",
                        "finite, explicit, auditable representational architectures in Project FAR v1.0",
                    ],
                ),
                "primitive_reclassification_nonclaim": contains_all(
                    formal_kernel,
                    ["The formal carrier names do not reclassify FARA's seven candidate primitives."],
                ),
                "global_primitive_nonclaim": contains_all(
                    formal_kernel,
                    ["does not establish their global independence, necessity, minimality, or irreducibility"],
                ),
            },
        },
        {
            "id": "C5",
            "name": "far_dependency_kind",
            "status": "Pass" if c5_pass else "Fail",
            "measurements": {
                "artifact_use_markers": far_contract_markers,
                "non_derivation_markers": far_non_derivation_markers,
                "accepted_derivation_proof_recorded": False,
            },
        },
        {
            "id": "C6",
            "name": "faro_dependency_kind",
            "status": "Pass" if c6_pass else "Fail",
            "measurements": {
                "artifact_and_workflow_markers": faro_contract_markers,
                "non_derivation_markers": faro_non_derivation_markers,
                "accepted_derivation_proof_recorded": False,
            },
        },
        {
            "id": "C7",
            "name": "protocol_derivation_boundary",
            "status": "Pass" if c7_pass else "Fail",
            "measurements": {
                "independent_method_and_governance_classifications_present": c7_pass
            },
        },
    ]

    authority_classifications = {
        "undifferentiated_owner": "Fail" if not c3_pass else "Pass",
        "split_authority": "Pass" if c1_pass and c2_pass and c4_pass and not c3_pass else "Fail",
    }
    dependency_classifications = {
        "logical_derivation": "Fail" if c5_pass and c6_pass and c7_pass else "Unknown",
        "artifact_workflow_contract": "Pass" if c5_pass and c6_pass and c7_pass else "Fail",
        "unclassified_dependency": "Fail" if c5_pass and c6_pass and c7_pass else "Unknown",
    }

    discovery_supported = (
        authority_classifications == {
            "undifferentiated_owner": "Fail",
            "split_authority": "Pass",
        }
        and dependency_classifications
        == {
            "logical_derivation": "Fail",
            "artifact_workflow_contract": "Pass",
            "unclassified_dependency": "Fail",
        }
    )

    return {
        "schema_version": "1.0",
        "investigation_id": spec["investigation_id"],
        "status": "Research",
        "base_commit": spec["base_commit"],
        "source_lock_results": lock_results,
        "checks": checks,
        "candidate_adjudication": {
            "authority_models": authority_classifications,
            "dependency_models": dependency_classifications,
        },
        "observations": [
            "Shared theory explicitly owns repository-wide canonical definitions for all seven FARA candidate-primitive terms.",
            "FARA separately lists and classifies the same seven terms as candidate primitives while pointing definitions to shared theory.",
            "The accepted semantic owner registry covers only a subset of the seven candidate primitives and exposes no distinct definition-owner and classification-owner relations.",
            "The accepted FARA formal kernel is a scoped formalization and explicitly does not reclassify the candidate primitives or establish their global primitive properties.",
            "Accepted FAR, FARO, framework-boundary, and derivation records support upstream artifact/workflow consumption while rejecting necessary downstream procedural derivation.",
            "Accepted protocol classifications keep canonicalization, CIR, evaluator controls, Pareto comparison, preregistration, and fail reporting outside canonical theory.",
        ],
        "discovery": {
            "supported": discovery_supported,
            "finding": "split_authority_and_artifact_contract_model_supported_at_frozen_repository_scope"
            if discovery_supported
            else "no_reconciliation_discovery_supported",
            "proposed_authority_relations": {
                "canonical_definition": "shared-theory",
                "candidate_primitive_classification": "FARA",
                "formal_representation_kernel": "FARA",
                "investigation_methodology": "FAR",
                "operational_interface": "FARO",
                "experiment_protocol_and_decision_rules": "CRP/methodology",
                "acceptance_promotion_and_freeze": "governance",
            },
            "proposed_dependency_kinds": {
                "FARA_to_FAR": "representation-artifact-contract",
                "FARA_to_FARO": "representation-artifact-contract",
                "FAR_to_FARO": "investigation-artifact-and-workflow-contract",
            },
        },
        "failures": [
            "The undifferentiated owner model does not preserve both shared-theory definition authority and FARA candidate classification.",
            "The current semantic owner registry does not register all seven FARA candidate primitives.",
            "No accepted derivation proof supports treating FAR methodology or FARO operations as logical consequences of FARA.",
        ],
        "lifecycle": {
            "question": "complete",
            "execution": "complete",
            "observation": "complete",
            "discovery": "Research finding",
            "replication": "pending separate implementation",
            "acceptance": "prohibited",
            "promotion": "prohibited",
            "repository_change": "prohibited except Research evidence",
        },
        "nonclaims": spec["nonclaims"],
    }


def canonical_json(value: Any) -> str:
    return json.dumps(value, indent=2, sort_keys=True) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    try:
        result = execute()
    except (FileNotFoundError, ValueError, json.JSONDecodeError) as exc:
        print(f"theory/dependency audit: FAIL: {exc}")
        return 1

    rendered = canonical_json(result)
    if args.write:
        RESULT_PATH.write_text(rendered, encoding="utf-8")
        print(f"wrote {RESULT_PATH.relative_to(ROOT)}")
        return 0

    if not RESULT_PATH.is_file():
        print("theory/dependency audit: FAIL: committed result missing")
        return 1
    committed = RESULT_PATH.read_text(encoding="utf-8")
    if committed != rendered:
        print("theory/dependency audit: FAIL: committed result drift")
        return 1
    print("theory/dependency audit: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
