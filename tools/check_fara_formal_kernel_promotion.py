#!/usr/bin/env python3
from __future__ import annotations

import copy
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "docs/governance/fara-formal-kernel-promotion-v1.0.json"

EXPECTED_SCOPE = "Project FAR v1.0 finite explicit auditable representational architecture"
EXPECTED_KERNEL = "identity-bearing-many-sorted-relational"
EXPECTED_GATES = [
    "representation_object_separation",
    "rule_execution_result_separation",
    "interpretation_separation",
    "calculus_independence",
    "architecture_operation_separation",
    "identity_bearing_occurrences",
    "explicit_provenance_and_order",
    "encoding_neutrality",
]
EXPECTED_SORTS = [
    "Object",
    "Representation",
    "Meaning",
    "Interpretation",
    "ReasoningCalculus",
    "Rule",
    "State",
    "Event",
    "Investigation",
    "Objective",
    "Condition",
    "RelationType",
    "RelationOccurrence",
    "Role",
    "Provenance",
]
EXPECTED_RELATIONS = {
    "denotes": ["Representation", "Object"],
    "assigns": ["Interpretation", "Representation", "Meaning"],
    "contains_rule": ["ReasoningCalculus", "Rule"],
    "applies": ["Event", "Rule"],
    "input_state": ["Event", "State"],
    "output_state": ["Event", "State"],
    "occurs_in": ["Event", "Investigation"],
    "uses_calculus": ["Investigation", "ReasoningCalculus"],
    "objective_of": ["Investigation", "Objective"],
    "condition_of": ["Investigation", "Condition"],
    "instance_of": ["RelationOccurrence", "RelationType"],
    "participant": ["RelationOccurrence", "Role", "Object"],
    "precedes": ["Event", "Event"],
    "provenance_of": ["Event", "Provenance"],
    "represents_event": ["Representation", "Event"],
}
EXPECTED_PRIMITIVES = [
    "Object",
    "Property",
    "Relation",
    "Representation",
    "Interpretation",
    "Investigation",
    "Reasoning Calculus",
]
EXPECTED_ROLES = {
    "identity-bearing-many-sorted-relational": "canonical-formal-kernel-within-scope",
    "typed-hypergraph": "admissible-derived-representation",
    "algebraic-state-transition": "admissible-derived-backend-with-explicit-preservation-machinery",
    "many-sorted-extensional-relational": "noncanonical-identity-losing-projection",
}
REQUIRED_AUTHORITY_MARKERS = {
    "frameworks/FARA/README.md": "FARA-FORMAL-KERNEL-001",
    "frameworks/FARA/architecture.md": "FARA-FORMAL-KERNEL-001",
    "frameworks/FARA/document-map.md": "formal-kernel.md",
    "frameworks/FARA/dependency-graph.md": "FARA-FORMAL-KERNEL-001",
    "docs/CANONICAL_MAP.md": "formal-kernel.md",
    "docs/governance/claim-status-matrix.md": "FARA-FORMAL-KERNEL-001",
    "docs/governance/limitations-register.md": "LIM-025",
    "docs/governance/unresolved-questions-register.md": "UQ-T11",
    "docs/governance/open-problems-register.md": "OP-10",
    "docs/project-status.md": "FARA-FORMAL-KERNEL-001",
    "docs/DECISION_LOG.md": "FARA-FORMAL-KERNEL-001",
}
FORBIDDEN_ASSERTIONS = [
    "the kernel is globally unique",
    "the kernel represents every reasoning system",
    "the seven primitives are globally necessary",
    "the seven primitives are globally minimal",
    "external-investigator independence is established",
    "all coherent foundations are globally inferior",
]


def git_blob_sha(data: bytes) -> str:
    header = f"blob {len(data)}\0".encode()
    return hashlib.sha1(header + data).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def validate_manifest(manifest: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    expected_scalars = {
        "acceptance_id": "FARA-FORMAL-KERNEL-001",
        "promotion_id": "FARA-FORMAL-KERNEL-PROMOTION-001",
        "change_id": "FARA-CCR-001",
        "status": "Accepted",
        "scope": EXPECTED_SCOPE,
        "canonical_kernel": EXPECTED_KERNEL,
        "external_investigator_independence": "not established",
    }
    for key, expected in expected_scalars.items():
        if manifest.get(key) != expected:
            errors.append(f"manifest {key} mismatch")

    lifecycle = manifest.get("lifecycle", {})
    for stage in ("question", "execution", "observation", "discovery", "replication", "acceptance", "promotion"):
        if lifecycle.get(stage) != "complete":
            errors.append(f"lifecycle stage not complete: {stage}")
    if lifecycle.get("repository_change") != "authorized; effective when this pull request merges":
        errors.append("repository-change lifecycle boundary mismatch")

    if manifest.get("mandatory_gates") != EXPECTED_GATES:
        errors.append("mandatory gate registry mismatch")
    if manifest.get("sorts") != EXPECTED_SORTS:
        errors.append("canonical sort registry mismatch")
    if manifest.get("relations") != EXPECTED_RELATIONS:
        errors.append("canonical relation signature mismatch")
    if manifest.get("candidate_roles") != EXPECTED_ROLES:
        errors.append("candidate role adjudication mismatch")
    if manifest.get("primitive_registry_unchanged") != EXPECTED_PRIMITIVES:
        errors.append("candidate primitive registry changed")

    nonclaims = set(manifest.get("nonclaims", []))
    required_nonclaims = {
        "global uniqueness",
        "universal representation of every reasoning system",
        "global primitive necessity",
        "global minimality",
        "completeness",
        "full-signature adequacy",
        "unbounded adequacy",
        "nonfinite continuous semantics",
        "live-oracle semantics",
        "environment-inclusive embodied semantics",
        "external-investigator independence",
        "superiority under every possible comparison criterion",
    }
    if not required_nonclaims.issubset(nonclaims):
        errors.append("required nonclaim missing")
    return errors


def validate_blob_locks(manifest: dict[str, Any], root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    records = [manifest.get("canonical_document", {})]
    records.extend(manifest.get("evidence_locks", {}).get(key, {}) for key in (
        "source_spec",
        "source_proof",
        "replication_result",
        "replication_adjudication",
        "acceptance_record",
        "promotion_record",
    ))
    for record in records:
        path_value = record.get("path")
        expected = record.get("git_blob_sha")
        if not path_value or not expected:
            errors.append("incomplete artifact lock")
            continue
        path = root / path_value
        if not path.is_file():
            errors.append(f"locked artifact missing: {path_value}")
            continue
        actual = git_blob_sha(path.read_bytes())
        if actual != expected:
            errors.append(f"artifact blob lock mismatch: {path_value}")
    return errors


def validate_evidence_content(manifest: dict[str, Any], root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    locks = manifest["evidence_locks"]
    source_spec = load_json(root / locks["source_spec"]["path"])
    source_proof = load_json(root / locks["source_proof"]["path"])
    replication_result = load_json(root / locks["replication_result"]["path"])
    adjudication = load_json(root / locks["replication_adjudication"]["path"])

    if source_spec.get("status") != "Research":
        errors.append("source specification was relabeled")
    if source_spec.get("proposed_foundation") != EXPECTED_KERNEL:
        errors.append("source specification foundation mismatch")
    if source_proof.get("status") != "Research":
        errors.append("source proof was relabeled")
    if source_proof.get("proposed_foundation") != EXPECTED_KERNEL:
        errors.append("source proof foundation mismatch")

    source_rows = {row["id"]: row for row in source_proof.get("candidate_adjudication", [])}
    selected = source_rows.get(EXPECTED_KERNEL, {})
    if selected.get("classification") != "provisional-canonical-candidate":
        errors.append("source candidate classification mismatch")
    if selected.get("failed_gates") != []:
        errors.append("source candidate has failed gates")

    if replication_result.get("candidate_adjudication") is None:
        errors.append("replication raw result missing candidate adjudication")
    if adjudication.get("decision") != "replicated":
        errors.append("replication decision is not replicated")
    if adjudication.get("errors") != []:
        errors.append("replication adjudication contains errors")
    if not adjudication.get("agreement", {}).get("matches_source_classifications_and_failed_gates"):
        errors.append("replication/source agreement missing")
    independence = adjudication.get("independence", {})
    if independence.get("external_investigator_independence") != "not established":
        errors.append("external-investigator independence boundary changed")
    if not independence.get("implementation_language_independent"):
        errors.append("implementation-language independence missing")
    if not independence.get("isolated_directory_execution"):
        errors.append("isolated replication execution missing")
    if not independence.get("neutral_fixture_history", {}).get("verified"):
        errors.append("neutral fixture history is not verified")
    return errors


def validate_canonical_text(manifest: dict[str, Any], text: str) -> list[str]:
    errors: list[str] = []
    required = [
        "Status: **Accepted**",
        "FARA-FORMAL-KERNEL-001",
        "identity-bearing many-sorted relational structure",
        "finite, explicit, auditable representational architectures in Project FAR v1.0",
        "The formal carrier names do not reclassify FARA's seven candidate primitives.",
        "external-investigator independence",
    ]
    for marker in required:
        if marker not in text:
            errors.append(f"canonical kernel marker missing: {marker}")
    for sort_name in EXPECTED_SORTS:
        if f"`{sort_name}`" not in text:
            errors.append(f"canonical kernel sort missing: {sort_name}")
    for relation_name in EXPECTED_RELATIONS:
        if f"`{relation_name}`" not in text:
            errors.append(f"canonical kernel relation missing: {relation_name}")
    lowered = text.lower()
    for assertion in FORBIDDEN_ASSERTIONS:
        if assertion in lowered:
            errors.append(f"forbidden scope inflation: {assertion}")
    return errors


def validate_primitive_text(manifest: dict[str, Any], text: str) -> list[str]:
    errors: list[str] = []
    match = re.search(
        r"# Current Candidate Primitives\s+The current candidate primitive concepts are:\s+(.*?)\s+These concepts presently serve",
        text,
        flags=re.DOTALL,
    )
    if not match:
        return ["candidate primitive section not found"]
    found = re.findall(r"^- (.+)$", match.group(1), flags=re.MULTILINE)
    if found != manifest.get("primitive_registry_unchanged"):
        errors.append("canonical candidate primitive list changed")
    return errors


def validate_authority_markers(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    for relative, marker in REQUIRED_AUTHORITY_MARKERS.items():
        path = root / relative
        if not path.is_file():
            errors.append(f"authority surface missing: {relative}")
            continue
        if marker not in path.read_text():
            errors.append(f"authority surface stale: {relative}")
    return errors


def validate(
    manifest: dict[str, Any] | None = None,
    *,
    root: Path = ROOT,
    check_files: bool = True,
    canonical_text: str | None = None,
    primitive_text: str | None = None,
) -> list[str]:
    manifest = copy.deepcopy(manifest if manifest is not None else load_json(root / MANIFEST.relative_to(ROOT)))
    errors = validate_manifest(manifest)
    if check_files:
        errors.extend(validate_blob_locks(manifest, root))
        errors.extend(validate_evidence_content(manifest, root))
        canonical_path = root / manifest.get("canonical_document", {}).get("path", "")
        canonical_text = canonical_path.read_text() if canonical_path.is_file() else ""
        primitive_text = (root / "frameworks/FARA/primitives.md").read_text()
        errors.extend(validate_authority_markers(root))
    if canonical_text is not None:
        errors.extend(validate_canonical_text(manifest, canonical_text))
    if primitive_text is not None:
        errors.extend(validate_primitive_text(manifest, primitive_text))
    return sorted(set(errors))


def main() -> int:
    errors = validate()
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("FARA formal-kernel Acceptance/Promotion validation: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
