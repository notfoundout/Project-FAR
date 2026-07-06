#!/usr/bin/env python3
"""Project FAR theory verifier.

This script enforces machine-readable checks for definitions, axioms,
theorems, propositions, lemmas, and phased proof-object adoption.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Set

ROOT = Path(__file__).resolve().parents[1]
METADATA_DIR = ROOT / "theory" / "metadata"
PROOF_OBJECTS_DIR = ROOT / "theory" / "proof-objects"
THEOREM_METADATA = METADATA_DIR / "theorems.yaml"
PROPOSITION_METADATA = METADATA_DIR / "propositions.yaml"
LEMMA_METADATA = METADATA_DIR / "lemmas.yaml"
DEFINITION_METADATA = METADATA_DIR / "definitions.yaml"
AXIOM_METADATA = METADATA_DIR / "axioms.yaml"
THEOREM_CATALOG = ROOT / "theory" / "theorems" / "theorems.md"
PROPOSITION_CATALOG = ROOT / "theory" / "theorems" / "propositions.md"
DERIVED_REGISTRY = ROOT / "theory" / "derivations" / "derived-concept-registry.md"
CANONICAL_NOTATION = ROOT / "theory" / "notation" / "canonical-notation.md"
GENERATED_THEOREM_INDEX = METADATA_DIR / "generated-theorem-index.md"
GENERATED_PROPOSITION_INDEX = METADATA_DIR / "generated-proposition-index.md"
GENERATED_LEMMA_INDEX = METADATA_DIR / "generated-lemma-index.md"
GENERATED_DEFINITION_INDEX = METADATA_DIR / "generated-definition-index.md"
GENERATED_AXIOM_INDEX = METADATA_DIR / "generated-axiom-index.md"

REQUIRED_THEOREM_FIELDS = {"id", "title", "status", "proof", "scope", "dependencies", "derived_concepts"}
REQUIRED_RESULT_FIELDS = {"id", "title", "status", "source", "scope", "dependencies"}
REQUIRED_PROOF_OBJECT_FIELDS = {"id", "theorem", "status", "premises", "steps", "conclusion"}
REQUIRED_PROOF_OBJECT_THEOREMS = {
    "T-001", "T-002", "T-003", "T-004", "T-005", "T-006",
    "T-007", "T-008", "T-009", "T-010",
}
KNOWN_STATUSES = {"Draft", "Proposed", "Verified", "Established", "Deprecated"}
BASE_DEPENDENCIES = {"derived-concept-registry", "canonical-notation", "definition-policy", "FAR-model-theory"}
CANONICAL_SYMBOLS = ["I", "Rep", "S", "Int", "C", "T"]
CANONICAL_SPECIAL_SYMBOLS = ["⊨", "≡sem", "≡str", "≡Q", "NF"]
ALLOWED_PROOF_STEP_RULES = {
    "definition_unfolding",
    "axiom_application",
    "prior_theorem",
    "lemma_application",
    "modus_ponens",
    "conjunction_intro",
    "universal_instantiation",
    "registry_substitution",
    "semantic_preservation",
}


class VerificationError(Exception):
    pass


def read_text(path: Path) -> str:
    if not path.exists():
        raise VerificationError(f"Missing required file: {path.relative_to(ROOT)}")
    return path.read_text(encoding="utf-8")


def load_yaml(path: Path) -> Dict[str, Any]:
    try:
        import yaml  # type: ignore
    except Exception as exc:  # pragma: no cover
        raise VerificationError("PyYAML is required. Install with: pip install pyyaml") from exc
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if not isinstance(data, dict):
        raise VerificationError(f"{path.relative_to(ROOT)} must parse to a mapping.")
    return data


def load_metadata_list(path: Path, key: str) -> List[Dict[str, Any]]:
    data = load_yaml(path)
    items = data.get(key)
    if not isinstance(items, list):
        raise VerificationError(f"{path.relative_to(ROOT)} must contain a '{key}' list.")
    return items


def load_theorems() -> List[Dict[str, Any]]:
    return load_metadata_list(THEOREM_METADATA, "theorems")


def load_propositions() -> List[Dict[str, Any]]:
    return load_metadata_list(PROPOSITION_METADATA, "propositions")


def load_lemmas() -> List[Dict[str, Any]]:
    return load_metadata_list(LEMMA_METADATA, "lemmas")


def load_definitions() -> List[Dict[str, Any]]:
    return load_metadata_list(DEFINITION_METADATA, "definitions")


def load_axioms() -> List[Dict[str, Any]]:
    return load_metadata_list(AXIOM_METADATA, "axioms")


def registered_derived_concepts() -> Set[str]:
    return set(re.findall(r"\bD-\d{3}\b", read_text(DERIVED_REGISTRY)))


def established_catalog_theorem_ids() -> Set[str]:
    text = read_text(THEOREM_CATALOG)
    established_start = text.find("# Established Theorems")
    if established_start == -1:
        raise VerificationError("The theorem catalog is missing '# Established Theorems'.")
    planned_start = text.find("# Planned Theorems", established_start)
    section = text[established_start:] if planned_start == -1 else text[established_start:planned_start]
    return set(re.findall(r"\bT-\d{3}\b", section))


def catalog_proposition_ids() -> Set[str]:
    return set(re.findall(r"\bP-\d{3}\b", read_text(PROPOSITION_CATALOG)))


def source_ids(prefix: str, directory: str) -> Set[str]:
    source_dir = ROOT / directory
    ids: Set[str] = set()
    if not source_dir.exists():
        return ids
    for path in source_dir.glob("*.md"):
        ids.update(re.findall(rf"\b{prefix}-\d{{3}}\b", read_text(path)))
    return ids


def id_pattern(prefix: str) -> str:
    if prefix == "A":
        return r"A\d+"
    return rf"{prefix}-\d{{3}}"


def validate_required_fields(items: List[Dict[str, Any]], required: Set[str], prefix: str) -> None:
    seen: Set[str] = set()
    pattern = id_pattern(prefix)
    for item in items:
        if not isinstance(item, dict):
            raise VerificationError(f"Each {prefix} metadata entry must be a mapping.")
        missing = required - set(item)
        if missing:
            raise VerificationError(f"{prefix} entry missing fields {sorted(missing)}: {item}")
        item_id = str(item["id"])
        if not re.fullmatch(pattern, item_id):
            raise VerificationError(f"Invalid {prefix} id: {item_id}")
        if item_id in seen:
            raise VerificationError(f"Duplicate {prefix} id: {item_id}")
        seen.add(item_id)
        if item["status"] not in KNOWN_STATUSES:
            raise VerificationError(f"Invalid status for {item_id}: {item['status']}")
        if not isinstance(item["dependencies"], list):
            raise VerificationError(f"dependencies must be a list for {item_id}")
        if "aliases" in item and not isinstance(item["aliases"], list):
            raise VerificationError(f"aliases must be a list for {item_id}")


def validate_source_files(items: List[Dict[str, Any]], source_key: str = "source") -> None:
    for item in items:
        path = ROOT / item[source_key]
        if not path.exists():
            raise VerificationError(f"Missing source file for {item['id']}: {item[source_key]}")
        text = read_text(path)
        if item["id"] not in text and str(item["title"]) not in text:
            raise VerificationError(f"Source file for {item['id']} contains neither its id nor title.")


def validate_theorem_proof_files(theorems: List[Dict[str, Any]]) -> None:
    for item in theorems:
        path = ROOT / item["proof"]
        if not path.exists():
            raise VerificationError(f"Missing proof file for {item['id']}: {item['proof']}")
        if item["id"] not in read_text(path):
            raise VerificationError(f"Proof file for {item['id']} does not contain its theorem id.")


def definition_aliases(definitions: List[Dict[str, Any]]) -> Set[str]:
    aliases: Set[str] = set()
    for item in definitions:
        for alias in item.get("aliases", []):
            aliases.add(str(alias))
    return aliases


def validate_catalog_consistency(theorems: List[Dict[str, Any]], propositions: List[Dict[str, Any]], lemmas: List[Dict[str, Any]]) -> None:
    theorem_ids = {item["id"] for item in theorems}
    established_theorem_ids = established_catalog_theorem_ids()
    if sorted(established_theorem_ids - theorem_ids):
        raise VerificationError(f"Established theorem catalog ids missing metadata: {sorted(established_theorem_ids - theorem_ids)}")
    if sorted(theorem_ids - established_theorem_ids):
        raise VerificationError(f"Theorem metadata ids missing from established theorem catalog: {sorted(theorem_ids - established_theorem_ids)}")

    proposition_ids = {item["id"] for item in propositions}
    catalog_props = catalog_proposition_ids()
    if sorted(catalog_props - proposition_ids):
        raise VerificationError(f"Proposition catalog ids missing metadata: {sorted(catalog_props - proposition_ids)}")
    if sorted(proposition_ids - catalog_props):
        raise VerificationError(f"Proposition metadata ids missing from catalog: {sorted(proposition_ids - catalog_props)}")

    lemma_ids = {item["id"] for item in lemmas}
    lemma_source_ids = source_ids("L", "theory/lemmas")
    if sorted(lemma_source_ids - lemma_ids):
        raise VerificationError(f"Lemma source ids missing metadata: {sorted(lemma_source_ids - lemma_ids)}")
    if sorted(lemma_ids - lemma_source_ids):
        raise VerificationError(f"Lemma metadata ids missing from source files: {sorted(lemma_ids - lemma_source_ids)}")


def validate_dependencies(
    theorems: List[Dict[str, Any]],
    propositions: Optional[List[Dict[str, Any]]] = None,
    lemmas: Optional[List[Dict[str, Any]]] = None,
    definitions: Optional[List[Dict[str, Any]]] = None,
    axioms: Optional[List[Dict[str, Any]]] = None,
) -> Dict[str, Set[str]]:
    propositions = load_propositions() if propositions is None else propositions
    lemmas = load_lemmas() if lemmas is None else lemmas
    definitions = load_definitions() if definitions is None else definitions
    axioms = load_axioms() if axioms is None else axioms

    theorem_ids = {item["id"] for item in theorems}
    proposition_ids = {item["id"] for item in propositions}
    lemma_ids = {item["id"] for item in lemmas}
    definition_ids = {item["id"] for item in definitions}
    axiom_ids = {item["id"] for item in axioms}
    known_dependencies = BASE_DEPENDENCIES | proposition_ids | lemma_ids | definition_ids | axiom_ids | definition_aliases(definitions)
    graph: Dict[str, Set[str]] = {item["id"]: set() for item in theorems}

    all_items = list(theorems) + list(propositions) + list(lemmas) + list(definitions) + list(axioms)
    for item in all_items:
        item_id = str(item["id"])
        for dep in item["dependencies"]:
            dep = str(dep)
            if dep == item_id:
                raise VerificationError(f"{item_id} directly depends on itself.")
            if re.fullmatch(r"T-\d{3}", dep):
                if dep not in theorem_ids:
                    raise VerificationError(f"{item_id} depends on unknown theorem {dep}.")
                if item_id in graph:
                    graph[item_id].add(dep)
            elif dep not in known_dependencies:
                raise VerificationError(f"{item_id} has unresolved dependency: {dep}")
    return graph


def validate_no_cycles(graph: Dict[str, Set[str]]) -> None:
    temporary: Set[str] = set()
    permanent: Set[str] = set()
    stack: List[str] = []

    def visit(node: str) -> None:
        if node in permanent:
            return
        if node in temporary:
            cycle_start = stack.index(node) if node in stack else 0
            cycle = stack[cycle_start:] + [node]
            raise VerificationError(f"Circular theorem dependency detected: {' -> '.join(cycle)}")
        temporary.add(node)
        stack.append(node)
        for dep in graph[node]:
            visit(dep)
        stack.pop()
        temporary.remove(node)
        permanent.add(node)

    for node in graph:
        visit(node)


def validate_registry(theorems: List[Dict[str, Any]]) -> None:
    registered = registered_derived_concepts()
    for item in theorems:
        for concept in item["derived_concepts"]:
            concept = str(concept)
            if concept not in registered:
                raise VerificationError(f"{item['id']} uses unregistered derived concept: {concept}")


def validate_notation_file() -> None:
    text = read_text(CANONICAL_NOTATION)
    for symbol in CANONICAL_SYMBOLS:
        if f"`{symbol}`" not in text:
            raise VerificationError(f"Canonical notation is missing symbol: {symbol}")
    for symbol in CANONICAL_SPECIAL_SYMBOLS:
        if symbol not in text:
            raise VerificationError(f"Canonical notation is missing special symbol: {symbol}")


def validate_required_proof_objects(theorems: List[Dict[str, Any]]) -> None:
    theorem_ids = {str(item["id"]) for item in theorems}
    for theorem_id in sorted(REQUIRED_PROOF_OBJECT_THEOREMS):
        if theorem_id not in theorem_ids:
            raise VerificationError(f"Required proof object theorem is not in theorem metadata: {theorem_id}")
        path = PROOF_OBJECTS_DIR / f"{theorem_id}.proof.yaml"
        if not path.exists():
            raise VerificationError(f"Missing required proof object: {path.relative_to(ROOT)}")
        data = load_yaml(path)
        missing = REQUIRED_PROOF_OBJECT_FIELDS - set(data)
        if missing:
            raise VerificationError(f"Proof object {theorem_id} missing fields: {sorted(missing)}")
        if str(data.get("theorem")) != theorem_id:
            raise VerificationError(f"Proof object {theorem_id} has mismatched theorem field: {data.get('theorem')}")
        premises = data.get("premises", [])
        steps = data.get("steps", [])
        if not isinstance(premises, list) or not isinstance(steps, list):
            raise VerificationError(f"Proof object {theorem_id} premises and steps must be lists")
        available = {str(premise.get("id")) for premise in premises if isinstance(premise, dict)}
        if len(available) != len(premises):
            raise VerificationError(f"Proof object {theorem_id} has duplicate or invalid premise ids")
        step_statements: Set[str] = set()
        for step in steps:
            if not isinstance(step, dict):
                raise VerificationError(f"Proof object {theorem_id} contains a non-mapping proof step")
            step_id = str(step.get("id", ""))
            if not step_id:
                raise VerificationError(f"Proof object {theorem_id} has a step without an id")
            if step_id in available:
                raise VerificationError(f"Proof object {theorem_id} reuses proof id: {step_id}")
            rule = str(step.get("rule", ""))
            if rule not in ALLOWED_PROOF_STEP_RULES:
                raise VerificationError(f"Proof object {theorem_id} step {step_id} uses unknown rule: {rule}")
            for input_id in step.get("inputs", []):
                if str(input_id) not in available:
                    raise VerificationError(f"Proof object {theorem_id} step {step_id} references unavailable input: {input_id}")
            statement = str(step.get("statement", ""))
            if not statement:
                raise VerificationError(f"Proof object {theorem_id} step {step_id} has no statement")
            if not step.get("justification"):
                raise VerificationError(f"Proof object {theorem_id} step {step_id} has no justification")
            step_statements.add(statement)
            available.add(step_id)
        if str(data.get("conclusion", "")) not in step_statements:
            raise VerificationError(f"Proof object {theorem_id} conclusion does not match a proof step statement")


def build_index(items: List[Dict[str, Any]], title: str, source_column: str) -> str:
    lines = [
        f"# Generated {title} Index",
        "",
        "This file is generated from machine-readable metadata.",
        "",
        f"| ID | Title | Status | {source_column.title()} | Scope |",
        "|---|---|---|---|---|",
    ]
    for item in sorted(items, key=lambda x: x["id"]):
        source = item.get("proof") or item.get("source")
        lines.append(f"| {item['id']} | {item['title']} | {item['status']} | `{source}` | {item['scope']} |")
    lines.append("")
    return "\n".join(lines)


def write_indexes(theorems: List[Dict[str, Any]], propositions: List[Dict[str, Any]], lemmas: List[Dict[str, Any]], definitions: List[Dict[str, Any]], axioms: List[Dict[str, Any]]) -> None:
    GENERATED_THEOREM_INDEX.write_text(build_index(theorems, "Theorem", "proof"), encoding="utf-8")
    GENERATED_PROPOSITION_INDEX.write_text(build_index(propositions, "Proposition", "source"), encoding="utf-8")
    GENERATED_LEMMA_INDEX.write_text(build_index(lemmas, "Lemma", "source"), encoding="utf-8")
    GENERATED_DEFINITION_INDEX.write_text(build_index(definitions, "Definition", "source"), encoding="utf-8")
    GENERATED_AXIOM_INDEX.write_text(build_index(axioms, "Axiom", "source"), encoding="utf-8")


def run_verification(write_generated_index: bool = False) -> None:
    theorems = load_theorems()
    propositions = load_propositions()
    lemmas = load_lemmas()
    definitions = load_definitions()
    axioms = load_axioms()
    validate_required_fields(theorems, REQUIRED_THEOREM_FIELDS, "T")
    validate_required_fields(propositions, REQUIRED_RESULT_FIELDS, "P")
    validate_required_fields(lemmas, REQUIRED_RESULT_FIELDS, "L")
    validate_required_fields(definitions, REQUIRED_RESULT_FIELDS, "DEF")
    validate_required_fields(axioms, REQUIRED_RESULT_FIELDS, "A")
    validate_theorem_proof_files(theorems)
    validate_source_files(propositions)
    validate_source_files(lemmas)
    validate_source_files(definitions)
    validate_source_files(axioms)
    validate_catalog_consistency(theorems, propositions, lemmas)
    graph = validate_dependencies(theorems, propositions, lemmas, definitions, axioms)
    validate_no_cycles(graph)
    validate_registry(theorems)
    validate_notation_file()
    validate_required_proof_objects(theorems)
    if write_generated_index:
        write_indexes(theorems, propositions, lemmas, definitions, axioms)


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Verify Project FAR theory metadata and proof structure.")
    parser.add_argument("--write-index", action="store_true", help="write generated metadata indexes")
    args = parser.parse_args(list(argv) if argv is not None else None)

    try:
        run_verification(write_generated_index=args.write_index)
    except VerificationError as exc:
        print(f"VERIFY THEORY FAILED: {exc}", file=sys.stderr)
        return 1

    print("VERIFY THEORY PASSED")
    if args.write_index:
        print("Wrote generated metadata indexes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
