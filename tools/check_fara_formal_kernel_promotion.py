#!/usr/bin/env python3
from __future__ import annotations

import copy
import hashlib
import importlib.util
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
EXPECTED_IDENTITY_CRITERIA = {
    "typed_identity": True,
    "cross_sort_identity_collision_allowed": False,
    "event_occurrences_identity_bearing": True,
    "relation_occurrences_identity_bearing": True,
    "literal_identifier_spelling_semantic": False,
    "renaming_may_merge_split_create_or_delete_identities": False,
}
EXPECTED_MODEL_EQUIVALENCE = {
    "name": "kernel-equivalence",
    "relation": "sort-preserving relational isomorphism",
    "requires_bijection_per_sort": True,
    "preserves_and_reflects_every_relation": True,
    "preserves_occurrence_multiplicity": True,
    "preserves_event_cardinality": True,
    "preserves_provenance": True,
    "preserves_precedence": True,
    "exact_normalized_equality": "identity-map special case",
    "behavioral_or_commitment_equivalence_substitutable": False,
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
EXPECTED_TERMINAL_RECLASSIFICATION = {
    "authority": "PROJECT-FAR-CORE-THEORY-1.0/FAR-CORE-007",
    "status": "superseded-as-global-primitives",
    "current_classification": "schema-and-contract-roles",
    "kernel_scope_unchanged": True,
}
EXPECTED_ROLES = {
    "identity-bearing-many-sorted-relational": "canonical-formal-kernel-within-scope",
    "typed-hypergraph": "admissible-derived-representation",
    "algebraic-state-transition": (
        "admissible-derived-backend-with-explicit-preservation-machinery"
    ),
    "many-sorted-extensional-relational": "noncanonical-identity-losing-projection",
}
REQUIRED_AUTHORITY_MARKERS = {
    "README.md": "FARA-FORMAL-KERNEL-001",
    "frameworks/FARA/README.md": "FARA-FORMAL-KERNEL-001",
    "frameworks/FARA/architecture.md": "FARA-FORMAL-KERNEL-001",
    "frameworks/FARA/design-principles.md": "sort-preserving relational isomorphism",
    "frameworks/FARA/document-map.md": "formal-kernel.md",
    "frameworks/FARA/dependency-graph.md": "FARA-FORMAL-KERNEL-001",
    "docs/CANONICAL_MAP.md": "formal-kernel.md",
    "docs/governance/framework-boundaries.md": "FARA-FORMAL-KERNEL-001",
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
    stages = (
        "question",
        "execution",
        "observation",
        "discovery",
        "replication",
        "acceptance",
        "promotion",
    )
    for stage in stages:
        if lifecycle.get(stage) != "complete":
            errors.append(f"lifecycle stage not complete: {stage}")
    expected_change = "authorized; effective when this pull request merges"
    if lifecycle.get("repository_change") != expected_change:
        errors.append("repository-change lifecycle boundary mismatch")

    if manifest.get("mandatory_gates") != EXPECTED_GATES:
        errors.append("mandatory gate registry mismatch")
    if manifest.get("sorts") != EXPECTED_SORTS:
        errors.append("canonical sort registry mismatch")
    if manifest.get("relations") != EXPECTED_RELATIONS:
        errors.append("canonical relation signature mismatch")
    if manifest.get("identity_criteria") != EXPECTED_IDENTITY_CRITERIA:
        errors.append("identity criteria mismatch")
    if manifest.get("model_equivalence") != EXPECTED_MODEL_EQUIVALENCE:
        errors.append("model equivalence relation mismatch")
    if manifest.get("candidate_roles") != EXPECTED_ROLES:
        errors.append("candidate role adjudication mismatch")
    if manifest.get("primitive_registry_unchanged") != EXPECTED_PRIMITIVES:
        errors.append("historical seven-role registry changed")
    if manifest.get("terminal_reclassification") != EXPECTED_TERMINAL_RECLASSIFICATION:
        errors.append("terminal schema-role reclassification mismatch")

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
    lock_names = (
        "source_spec",
        "source_proof",
        "source_implementation",
        "replication_result",
        "replication_adjudication",
        "acceptance_record",
        "promotion_record",
    )
    records.extend(
        manifest.get("evidence_locks", {}).get(key, {}) for key in lock_names
    )
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


def validate_evidence_content(
    manifest: dict[str, Any], root: Path = ROOT
) -> list[str]:
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

    source_rows = {
        row["id"]: row for row in source_proof.get("candidate_adjudication", [])
    }
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
    agreement = adjudication.get("agreement", {})
    if not agreement.get("matches_source_classifications_and_failed_gates"):
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


def validate_model_isomorphism(
    left: dict[str, Any],
    right: dict[str, Any],
    mapping: dict[str, dict[str, str]],
) -> list[str]:
    errors: list[str] = []
    left_sorts = left.get("sorts", {})
    right_sorts = right.get("sorts", {})
    left_relations = left.get("relations", {})
    right_relations = right.get("relations", {})

    for sort_name in EXPECTED_SORTS:
        left_members = set(left_sorts.get(sort_name, []))
        right_members = set(right_sorts.get(sort_name, []))
        sort_mapping = mapping.get(sort_name, {})
        if set(sort_mapping) != left_members:
            errors.append(f"isomorphism domain mismatch: {sort_name}")
            continue
        images = list(sort_mapping.values())
        if len(images) != len(set(images)):
            errors.append(f"isomorphism is not injective: {sort_name}")
        if set(images) != right_members:
            errors.append(f"isomorphism codomain mismatch: {sort_name}")

    for relation_name, signature in EXPECTED_RELATIONS.items():
        mapped_rows: set[tuple[str, ...]] = set()
        for row in left_relations.get(relation_name, []):
            if len(row) != len(signature):
                errors.append(f"left relation arity mismatch: {relation_name}")
                continue
            try:
                mapped = tuple(
                    mapping[sort_name][value]
                    for value, sort_name in zip(row, signature)
                )
            except KeyError:
                errors.append(f"unmapped relation member: {relation_name}")
                continue
            mapped_rows.add(mapped)
        right_rows = {
            tuple(row) for row in right_relations.get(relation_name, [])
        }
        if mapped_rows != right_rows:
            errors.append(f"relation not preserved and reflected: {relation_name}")
    return sorted(set(errors))


def rename_model(
    model: dict[str, Any], mapping: dict[str, dict[str, str]]
) -> dict[str, Any]:
    renamed = copy.deepcopy(model)
    renamed["sorts"] = {
        sort_name: [mapping[sort_name][member] for member in members]
        for sort_name, members in model["sorts"].items()
    }
    renamed["relations"] = {}
    for relation_name, signature in EXPECTED_RELATIONS.items():
        renamed["relations"][relation_name] = [
            [
                mapping[sort_name][value]
                for value, sort_name in zip(row, signature)
            ]
            for row in model["relations"][relation_name]
        ]
    return renamed


def load_source_kernel(
    manifest: dict[str, Any], root: Path = ROOT
) -> Any:
    path = root / manifest["evidence_locks"]["source_implementation"]["path"]
    spec = importlib.util.spec_from_file_location("fara_source_kernel", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load source kernel")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def validate_equivalence_witness(
    manifest: dict[str, Any], root: Path = ROOT
) -> list[str]:
    errors: list[str] = []
    try:
        kernel = load_source_kernel(manifest, root)
        model = kernel.sample_model()
    except Exception as exc:  # pragma: no cover - converted to fail-closed output
        return [f"equivalence witness setup failed: {exc}"]

    mapping = {
        sort_name: {
            member: f"{sort_name.lower()}::{index}"
            for index, member in enumerate(model["sorts"][sort_name])
        }
        for sort_name in EXPECTED_SORTS
    }
    renamed = rename_model(model, mapping)
    if kernel.validate_model(renamed):
        errors.append("renamed equivalence witness is not an admitted model")
    if validate_model_isomorphism(model, renamed, mapping):
        errors.append("sort-preserving renaming failed kernel equivalence")

    occurrence_members = model["sorts"]["RelationOccurrence"]
    if len(occurrence_members) >= 2:
        noninjective = copy.deepcopy(mapping)
        first, second = occurrence_members[:2]
        noninjective["RelationOccurrence"][second] = noninjective[
            "RelationOccurrence"
        ][first]
        noninjective_errors = validate_model_isomorphism(
            model, renamed, noninjective
        )
        if not any(
            "not injective: RelationOccurrence" in item
            for item in noninjective_errors
        ):
            errors.append("occurrence-identity collapse was not rejected")

    without_provenance = copy.deepcopy(renamed)
    without_provenance["relations"]["provenance_of"] = without_provenance[
        "relations"
    ]["provenance_of"][:-1]
    provenance_errors = validate_model_isomorphism(
        model, without_provenance, mapping
    )
    if "relation not preserved and reflected: provenance_of" not in provenance_errors:
        errors.append("provenance-loss equivalence was not rejected")
    return errors


def extract_formal_carriers(text: str) -> tuple[list[str], list[str]]:
    match = re.search(
        r"## Formal carriers\s+"
        r"The kernel contains the following disjoint carriers:\s+"
        r"(.*?)\s+These are formal carrier names\.",
        text,
        flags=re.DOTALL,
    )
    if not match:
        return [], ["canonical formal-carrier registry not found"]
    found = re.findall(r"^- `([^`]+)`$", match.group(1), flags=re.MULTILINE)
    errors: list[str] = []
    for sort_name in EXPECTED_SORTS:
        if sort_name not in found:
            errors.append(f"canonical kernel sort missing: {sort_name}")
    extras = [sort_name for sort_name in found if sort_name not in EXPECTED_SORTS]
    if extras or found != EXPECTED_SORTS:
        errors.append("canonical formal-carrier registry mismatch")
    return found, errors


def extract_relation_signature(
    text: str,
) -> tuple[dict[str, list[str]], list[str]]:
    match = re.search(
        r"## Relation signature\s+"
        r"The canonical relation signature is:\s+"
        r"\| Relation \| Signature \|\s+"
        r"\|---\|---\|\s+"
        r"(.*?)\s+## Admission constraints",
        text,
        flags=re.DOTALL,
    )
    if not match:
        return {}, ["canonical relation-signature table not found"]
    found: dict[str, list[str]] = {}
    errors: list[str] = []
    for name, signature_text in re.findall(
        r"^\| `([^`]+)` \| `([^`]+)` \|$",
        match.group(1),
        flags=re.MULTILINE,
    ):
        if name in found:
            errors.append(f"duplicate canonical relation declaration: {name}")
        found[name] = signature_text.split(" × ")
    for relation_name in EXPECTED_RELATIONS:
        if relation_name not in found:
            errors.append(f"canonical kernel relation missing: {relation_name}")
    if found != EXPECTED_RELATIONS:
        errors.append("canonical relation-signature table mismatch")
    return found, errors


def validate_canonical_text(
    manifest: dict[str, Any], text: str
) -> list[str]:
    errors: list[str] = []
    required = [
        "Status: **Accepted**",
        "FARA-FORMAL-KERNEL-001",
        "identity-bearing many-sorted relational structure",
        "finite, explicit, auditable representational architectures in Project FAR v1.0",
        "The formal carrier names instantiate FARA's seven schema roles and do not confer global primitive status.",
        "Literal token spelling is not semantic by itself.",
        "sort-preserving relational isomorphism",
        "external-investigator independence",
    ]
    for marker in required:
        if marker not in text:
            errors.append(f"canonical kernel marker missing: {marker}")
    _, carrier_errors = extract_formal_carriers(text)
    errors.extend(carrier_errors)
    _, relation_errors = extract_relation_signature(text)
    errors.extend(relation_errors)
    lowered = text.lower()
    for assertion in FORBIDDEN_ASSERTIONS:
        if assertion in lowered:
            errors.append(f"forbidden scope inflation: {assertion}")
    return errors


def validate_primitive_text(
    manifest: dict[str, Any], text: str
) -> list[str]:
    errors: list[str] = []
    match = re.search(
        r"## Current schema and contract roles\s+"
        r"\| Role \| Terminal classification \|\s+"
        r"\|---\|---\|\s+"
        r"(.*?)\s+## Derived architectural concepts",
        text,
        flags=re.DOTALL,
    )
    if not match:
        return ["schema-role section not found"]
    found = re.findall(
        r"^\| ([^|]+?) \| [^|]+ \|$",
        match.group(1),
        flags=re.MULTILINE,
    )
    found = [value.strip() for value in found]
    if found != manifest.get("primitive_registry_unchanged"):
        errors.append("canonical schema-role list changed")
    if "not global primitives" not in text:
        errors.append("schema-role nonprimitive boundary missing")
    if "global primitive-independence and primitive-minimality search is closed" not in text:
        errors.append("global primitive-search closure missing")
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
    manifest_path = root / MANIFEST.relative_to(ROOT)
    manifest = copy.deepcopy(
        manifest if manifest is not None else load_json(manifest_path)
    )
    errors = validate_manifest(manifest)
    if check_files:
        errors.extend(validate_blob_locks(manifest, root))
        errors.extend(validate_evidence_content(manifest, root))
        errors.extend(validate_equivalence_witness(manifest, root))
        canonical_path = root / manifest.get("canonical_document", {}).get(
            "path", ""
        )
        canonical_text = (
            canonical_path.read_text() if canonical_path.is_file() else ""
        )
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
