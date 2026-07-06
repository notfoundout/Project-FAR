#!/usr/bin/env python3
"""Strict structural proof-object checker for Project FAR YAML proof objects."""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Any, Dict, Iterable, List, Set

import yaml

ROOT = Path(__file__).resolve().parents[1]
METADATA_DIR = ROOT / "theory" / "metadata"
THEOREM_METADATA = METADATA_DIR / "theorems.yaml"
PROPOSITION_METADATA = METADATA_DIR / "propositions.yaml"
LEMMA_METADATA = METADATA_DIR / "lemmas.yaml"
DEFINITION_METADATA = METADATA_DIR / "definitions.yaml"
AXIOM_METADATA = METADATA_DIR / "axioms.yaml"
DERIVED_REGISTRY = ROOT / "theory" / "derivations" / "derived-concept-registry.md"
BASE_DEPENDENCIES = {"derived-concept-registry", "canonical-notation", "definition-policy", "FAR-model-theory"}
SPECIAL_CONTEXT_SOURCES = {
    "definitions",
    "primitive architecture",
    "induction principle over registry depth",
}

ALLOWED_RULES = {
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

REQUIRED_FIELDS = {"id", "theorem", "status", "premises", "steps", "conclusion"}
SOURCE_ID_PATTERN = re.compile(r"\b(?:T|P|L|DEF)-\d{3}\b|\bA\d+\b|\bD-(?:\d{3}|REP|INT|CALC|INV|STRUCT)\b")
WORD_PATTERN = re.compile(r"[A-Za-z][A-Za-z0-9_-]*")
STOP_WORDS = {
    "a", "an", "and", "are", "as", "be", "by", "for", "from", "if", "in", "is", "it", "its",
    "let", "of", "or", "that", "the", "then", "this", "to", "under", "when", "with",
}


def load_yaml(path: Path) -> Dict[str, Any]:
    data = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"{path} must parse to a mapping")
    return data


def metadata_items(path: Path, key: str) -> List[Dict[str, Any]]:
    data = load_yaml(path)
    items = data.get(key, [])
    if not isinstance(items, list):
        raise ValueError(f"{path} must contain a {key} list")
    return items


def metadata_index() -> Dict[str, Dict[str, Any]]:
    index: Dict[str, Dict[str, Any]] = {}
    for path, key in [
        (THEOREM_METADATA, "theorems"),
        (PROPOSITION_METADATA, "propositions"),
        (LEMMA_METADATA, "lemmas"),
        (DEFINITION_METADATA, "definitions"),
        (AXIOM_METADATA, "axioms"),
    ]:
        for item in metadata_items(path, key):
            item_id = str(item.get("id", ""))
            if item_id:
                index[item_id] = item
            for alias in item.get("aliases", []) or []:
                index[str(alias)] = item
    return index


def registered_derived_concepts() -> Set[str]:
    if not DERIVED_REGISTRY.exists():
        return set()
    return set(re.findall(r"\bD-\d{3}\b", DERIVED_REGISTRY.read_text(encoding="utf-8")))


def source_ids(source: str) -> Set[str]:
    return set(SOURCE_ID_PATTERN.findall(source))


def theorem_statement(theorem_id: str, index: Dict[str, Dict[str, Any]]) -> str:
    theorem = index.get(theorem_id)
    if not theorem:
        return ""
    proof_path = ROOT / str(theorem.get("proof", ""))
    if not proof_path.exists():
        return ""
    text = proof_path.read_text(encoding="utf-8")
    match = re.search(r"## Statement\s+(.*?)(?:\n---\n|\n## )", text, flags=re.DOTALL)
    if not match:
        return ""
    statement = re.sub(r"```.*?```", " ", match.group(1), flags=re.DOTALL)
    return re.sub(r"\s+", " ", statement).strip()


def significant_words(text: str) -> Set[str]:
    return {word.lower() for word in WORD_PATTERN.findall(text) if len(word) > 1 and word.lower() not in STOP_WORDS}


def conclusion_aligns_with_statement(conclusion: str, statement: str) -> bool:
    if not conclusion or not statement:
        return False
    normalized_conclusion = re.sub(r"\s+", " ", conclusion.lower()).strip()
    normalized_statement = re.sub(r"\s+", " ", statement.lower()).strip()
    if normalized_conclusion in normalized_statement or normalized_statement in normalized_conclusion:
        return True
    conclusion_words = significant_words(conclusion)
    statement_words = significant_words(statement)
    if not conclusion_words or not statement_words:
        return False
    overlap = conclusion_words & statement_words
    return len(overlap) / len(conclusion_words) >= 0.35


def declared_dependency_ids(theorem_id: str, index: Dict[str, Dict[str, Any]]) -> Set[str]:
    theorem = index.get(theorem_id, {})
    deps = {str(dep) for dep in theorem.get("dependencies", []) or []}
    deps.add(theorem_id)
    deps |= BASE_DEPENDENCIES
    for dep in list(deps):
        dep_item = index.get(dep)
        if dep_item:
            deps.add(str(dep_item.get("id", dep)))
    return deps


def validate_premise_sources(
    theorem_id: str,
    premises: Iterable[Dict[str, Any]],
    index: Dict[str, Dict[str, Any]],
    errors: List[str],
) -> None:
    declared = declared_dependency_ids(theorem_id, index)
    registered_d = registered_derived_concepts()
    for premise in premises:
        pid = str(premise.get("id", ""))
        source = str(premise.get("source", "")).strip()
        if not source:
            errors.append(f"premise {pid} missing source")
            continue
        ids = source_ids(source)
        if not ids and source not in SPECIAL_CONTEXT_SOURCES and source not in BASE_DEPENDENCIES:
            errors.append(f"premise {pid} source is not resolvable: {source}")
            continue
        for source_id in ids:
            if source_id.startswith("D-") and source_id in registered_d:
                continue
            if source_id not in index and source_id not in BASE_DEPENDENCIES:
                errors.append(f"premise {pid} source id does not exist: {source_id}")
                continue
            if re.fullmatch(r"[TPL]-\d{3}", source_id) and source_id not in declared:
                errors.append(f"premise {pid} cites undeclared theorem/proposition/lemma dependency: {source_id}")


def check_proof_object(path: Path) -> List[str]:
    errors: List[str] = []
    try:
        data = load_yaml(path)
    except Exception as exc:
        return [f"proof object must be valid YAML mapping: {exc}"]

    missing = REQUIRED_FIELDS - set(data)
    if missing:
        errors.append(f"missing required fields: {sorted(missing)}")

    index = metadata_index()
    theorem_id = str(data.get("theorem", ""))
    if not re.fullmatch(r"T-\d{3}", theorem_id):
        errors.append(f"invalid theorem id: {theorem_id}")
    elif theorem_id not in index:
        errors.append(f"theorem does not exist in metadata: {theorem_id}")

    expected_id = f"PO-{theorem_id}" if theorem_id else ""
    if theorem_id and str(data.get("id", "")) != expected_id:
        errors.append(f"proof object id must be {expected_id}")

    premises = data.get("premises", [])
    steps = data.get("steps", [])
    if not isinstance(premises, list):
        errors.append("premises must be a list")
        premises = []
    if not isinstance(steps, list):
        errors.append("steps must be a list")
        steps = []

    premise_ids: Set[str] = set()
    for premise in premises:
        if not isinstance(premise, dict):
            errors.append("premise must be a mapping")
            continue
        pid = str(premise.get("id", ""))
        if not pid:
            errors.append("premise missing id")
        if pid in premise_ids:
            errors.append(f"duplicate premise id: {pid}")
        premise_ids.add(pid)
        if not premise.get("statement"):
            errors.append(f"premise {pid} missing statement")

    if theorem_id:
        validate_premise_sources(theorem_id, [p for p in premises if isinstance(p, dict)], index, errors)

    available: Set[str] = set(premise_ids)
    step_ids: Set[str] = set()
    step_statements: Set[str] = set()
    for step in steps:
        if not isinstance(step, dict):
            errors.append("step must be a mapping")
            continue
        sid = str(step.get("id", ""))
        if not sid:
            errors.append("step missing id")
            continue
        if sid in step_ids:
            errors.append(f"duplicate step id: {sid}")
        if sid in premise_ids:
            errors.append(f"step id reuses premise id: {sid}")
        step_ids.add(sid)

        rule = str(step.get("rule", ""))
        if rule not in ALLOWED_RULES:
            errors.append(f"step {sid} uses unknown rule: {rule}")

        inputs = step.get("inputs", [])
        if not isinstance(inputs, list):
            errors.append(f"step {sid} inputs must be a list")
            inputs = []
        for inp in inputs:
            inp = str(inp)
            if inp not in available:
                errors.append(f"step {sid} references unavailable input: {inp}")

        statement = str(step.get("statement", ""))
        if not statement:
            errors.append(f"step {sid} missing statement")
        else:
            step_statements.add(statement)
        if not step.get("justification"):
            errors.append(f"step {sid} missing justification")

        available.add(sid)

    conclusion = str(data.get("conclusion", ""))
    if conclusion and conclusion not in step_statements:
        errors.append("conclusion does not match any proof step statement")
    if theorem_id and conclusion:
        statement = theorem_statement(theorem_id, index)
        if not statement:
            errors.append(f"theorem {theorem_id} proof file has no parsable Statement section")
        elif not conclusion_aligns_with_statement(conclusion, statement):
            errors.append(f"conclusion does not align with theorem {theorem_id} Statement section")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Check a Project FAR proof object")
    parser.add_argument("path", type=Path)
    args = parser.parse_args()

    errors = check_proof_object(args.path)
    if errors:
        print("PROOF OBJECT CHECK FAILED")
        for error in errors:
            print(f"- {error}")
        return 1
    print("PROOF OBJECT CHECK PASSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
