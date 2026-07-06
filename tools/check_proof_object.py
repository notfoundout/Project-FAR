#!/usr/bin/env python3
"""Strict structural and rule-pattern checker for Project FAR YAML proof objects."""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Any, Dict, Iterable, List, Set, Tuple

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
DEFINITIONAL_BASE_SOURCES = BASE_DEPENDENCIES | SPECIAL_CONTEXT_SOURCES

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
SEMANTIC_TERMS = {"semantic", "semantics", "meaning", "interpretation", "interpreted", "equivalence", "content"}
CONDITIONAL_TERMS = {"if", "then", "implies", "imply", "whenever", "condition", "conditional", "=>", "->", "→"}
ANTECEDENT_TERMS = {"is", "are", "holds", "given", "let", "for", "every", "condition", "satisfying"}
ALLOWED_STATEMENT_KINDS = {
    "universal", "existential", "definitional", "definition", "conditional",
    "equivalence", "preservation", "construction", "validation",
    "classification", "meta", "claim", "semantic", "registry",
    "conjunction", "theorem", "proposition", "lemma", "axiom",
}


def contains_term(text: str, term: str) -> bool:
    lowered = text.lower()
    lowered_term = term.lower()
    if lowered_term in {"=>", "->", "→"}:
        return lowered_term in lowered
    return re.search(rf"\b{re.escape(lowered_term)}\b", lowered) is not None


def statement_text(value: Any) -> str:
    if isinstance(value, str):
        return value
    if isinstance(value, dict):
        parts = [value.get(field, "") for field in ("kind", "subject", "predicate", "scope", "claim")]
        return " ".join(str(part) for part in parts if part)
    return ""


def validate_statement_value(value: Any, location: str, errors: List[str]) -> str:
    if isinstance(value, str):
        if not value.strip():
            errors.append(f"{location} statement must be nonempty")
        return value
    if not isinstance(value, dict):
        errors.append(f"{location} statement must be prose or a mapping")
        return ""
    kind = str(value.get("kind", "")).strip()
    claim = str(value.get("claim", "")).strip()
    if not kind:
        errors.append(f"{location} statement missing kind")
    elif kind not in ALLOWED_STATEMENT_KINDS:
        errors.append(f"{location} statement has invalid kind: {kind}")
    if not claim:
        errors.append(f"{location} statement missing claim")
    for field in ("subject", "predicate", "scope"):
        if field in value and not isinstance(value[field], str):
            errors.append(f"{location} statement {field} must be a string when present")
    return statement_text(value)


def metadata_statement_text(item: Dict[str, Any]) -> str:
    return statement_text(item.get("statement"))


def source_items(input_ids: List[str], lineage: Dict[str, Set[str]], index: Dict[str, Dict[str, Any]], pattern: str) -> List[Tuple[str, Dict[str, Any]]]:
    items: List[Tuple[str, Dict[str, Any]]] = []
    for input_id in input_ids:
        for source_id in sorted(lineage.get(input_id, set())):
            if re.fullmatch(pattern, source_id) and source_id in index:
                items.append((source_id, index[source_id]))
    return items


def warn_on_weak_metadata_alignment(step_id: str, rule: str, step_statement: str, sources: List[Tuple[str, Dict[str, Any]]], warnings: List[str]) -> None:
    for source_id, item in sources:
        metadata_statement = metadata_statement_text(item)
        if metadata_statement and not conclusion_aligns_with_statement(step_statement, metadata_statement):
            warnings.append(f"step {step_id} {rule} has weak semantic overlap with {source_id} metadata statement")


def has_vocabulary(input_ids: List[str], statements: Dict[str, str], terms: Set[str]) -> bool:
    return any(contains_term(statements.get(input_id, ""), term) for input_id in input_ids for term in terms)


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
            if source_id.startswith("D-") and (source_id in registered_d or source_id in index):
                continue
            if source_id not in index and source_id not in BASE_DEPENDENCIES:
                errors.append(f"premise {pid} source id does not exist: {source_id}")
                continue
            if re.fullmatch(r"[TPL]-\d{3}", source_id) and source_id not in declared:
                errors.append(f"premise {pid} cites undeclared theorem/proposition/lemma dependency: {source_id}")


def has_source_kind(input_ids: List[str], lineage: Dict[str, Set[str]], pattern: str) -> bool:
    return any(any(re.fullmatch(pattern, source_id) for source_id in lineage.get(input_id, set())) for input_id in input_ids)


def has_source_id(input_ids: List[str], lineage: Dict[str, Set[str]], allowed: Set[str]) -> bool:
    return any(bool(lineage.get(input_id, set()) & allowed) for input_id in input_ids)


def has_rule(input_ids: List[str], rule_lineage: Dict[str, Set[str]], rule: str) -> bool:
    return any(rule in rule_lineage.get(input_id, set()) for input_id in input_ids)


def input_text(input_ids: List[str], statements: Dict[str, str]) -> str:
    return " ".join(statements.get(input_id, "") for input_id in input_ids).lower()


def validate_rule_pattern(
    step_id: str,
    rule: str,
    input_ids: List[str],
    lineage: Dict[str, Set[str]],
    rule_lineage: Dict[str, Set[str]],
    statements: Dict[str, str],
    errors: List[str],
    warnings: List[str],
    index: Dict[str, Dict[str, Any]],
    step_statement: str,
) -> None:
    if rule == "definition_unfolding":
        if not input_ids:
            errors.append(f"step {step_id} definition_unfolding requires at least one input")
            return
        if not (
            has_source_kind(input_ids, lineage, r"DEF-\d{3}")
            or has_source_kind(input_ids, lineage, r"D-(?:\d{3}|REP|INT|CALC|INV|STRUCT)")
            or has_source_kind(input_ids, lineage, r"T-\d{3}")
            or has_source_id(input_ids, lineage, DEFINITIONAL_BASE_SOURCES)
            or has_rule(input_ids, rule_lineage, "definition_unfolding")
        ):
            errors.append(f"step {step_id} definition_unfolding requires a definition, definition alias, theorem statement/context, definitional base source, or prior definitional step")

    elif rule == "axiom_application":
        sources = source_items(input_ids, lineage, index, r"A\d+")
        if not sources:
            errors.append(f"step {step_id} axiom_application requires an axiom-bearing input")
        warn_on_weak_metadata_alignment(step_id, rule, step_statement, sources, warnings)

    elif rule == "prior_theorem":
        sources = source_items(input_ids, lineage, index, r"T-\d{3}")
        if not sources:
            errors.append(f"step {step_id} prior_theorem requires a theorem-bearing input")
        warn_on_weak_metadata_alignment(step_id, rule, step_statement, sources, warnings)

    elif rule == "lemma_application":
        sources = source_items(input_ids, lineage, index, r"L-\d{3}")
        if not sources:
            errors.append(f"step {step_id} lemma_application requires a lemma-bearing input")
        warn_on_weak_metadata_alignment(step_id, rule, step_statement, sources, warnings)

    elif rule == "conjunction_intro":
        if len(input_ids) < 2:
            errors.append(f"step {step_id} conjunction_intro requires at least two inputs")

    elif rule == "universal_instantiation":
        if not input_ids:
            errors.append(f"step {step_id} universal_instantiation requires at least one scoped or universal input")

    elif rule == "semantic_preservation":
        semantic_text = input_text(input_ids, statements)
        if not (
            has_source_id(input_ids, lineage, {"T-004", "DEF-031", "DEF-033", "D-INT"})
            or has_rule(input_ids, rule_lineage, "semantic_preservation")
            or any(contains_term(semantic_text, term) for term in SEMANTIC_TERMS)
        ):
            errors.append(f"step {step_id} semantic_preservation requires semantic content, interpretation, equivalence, or T-004/DEF-031/DEF-033 input")

    elif rule == "registry_substitution":
        if not (
            has_source_id(input_ids, lineage, {"derived-concept-registry", "T-006"})
            or has_source_kind(input_ids, lineage, r"D-\d{3}")
            or has_rule(input_ids, rule_lineage, "registry_substitution")
        ):
            errors.append(f"step {step_id} registry_substitution requires registry, registered derived concept, T-006, or prior registry-substitution input")

    elif rule == "modus_ponens":
        if len(input_ids) < 2:
            errors.append(f"step {step_id} modus_ponens requires at least two inputs")
        elif not has_vocabulary(input_ids, statements, CONDITIONAL_TERMS):
            errors.append(f"step {step_id} modus_ponens requires at least one conditional-like input")
        elif not has_vocabulary(input_ids, statements, ANTECEDENT_TERMS):
            errors.append(f"step {step_id} modus_ponens requires at least one antecedent-like input")


def check_proof_object(path: Path) -> List[str]:
    errors: List[str] = []
    warnings: List[str] = []
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
    lineage: Dict[str, Set[str]] = {}
    rule_lineage: Dict[str, Set[str]] = {}
    statements: Dict[str, str] = {}

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
        statement = validate_statement_value(premise.get("statement", ""), f"premise {pid}", errors)
        source = str(premise.get("source", "")).strip()
        ids = source_ids(source)
        if source in BASE_DEPENDENCIES or source in SPECIAL_CONTEXT_SOURCES:
            ids.add(source)
        lineage[pid] = ids
        rule_lineage[pid] = set()
        statements[pid] = statement

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

        raw_inputs = step.get("inputs", [])
        if not isinstance(raw_inputs, list):
            errors.append(f"step {sid} inputs must be a list")
            raw_inputs = []
        inputs = [str(inp) for inp in raw_inputs]
        for inp in inputs:
            if inp not in available:
                errors.append(f"step {sid} references unavailable input: {inp}")

        if rule in ALLOWED_RULES and all(inp in available for inp in inputs):
            validate_rule_pattern(sid, rule, inputs, lineage, rule_lineage, statements, errors, warnings, index, statement_text(step.get("statement", "")))

        statement = validate_statement_value(step.get("statement", ""), f"step {sid}", errors)
        if statement:
            step_statements.add(statement)
        if not step.get("justification"):
            errors.append(f"step {sid} missing justification")

        step_source_ids: Set[str] = set()
        step_rules: Set[str] = {rule} if rule in ALLOWED_RULES else set()
        for inp in inputs:
            step_source_ids |= lineage.get(inp, set())
            step_rules |= rule_lineage.get(inp, set())
        lineage[sid] = step_source_ids
        rule_lineage[sid] = step_rules
        statements[sid] = statement
        available.add(sid)

    conclusion = statement_text(data.get("conclusion", ""))
    if conclusion and conclusion not in step_statements:
        errors.append("conclusion does not match any proof step statement")
    if theorem_id and conclusion:
        statement = theorem_statement(theorem_id, index)
        if not statement:
            errors.append(f"theorem {theorem_id} proof file has no parsable Statement section")
        elif not conclusion_aligns_with_statement(conclusion, statement):
            errors.append(f"conclusion does not align with theorem {theorem_id} Statement section")

    return errors + [f"WARNING: {warning}" for warning in warnings]


def main() -> int:
    parser = argparse.ArgumentParser(description="Check a Project FAR proof object")
    parser.add_argument("path", type=Path)
    args = parser.parse_args()

    errors = check_proof_object(args.path)
    hard_errors = [error for error in errors if not error.startswith("WARNING:")]
    warnings = [error for error in errors if error.startswith("WARNING:")]
    if hard_errors:
        print("PROOF OBJECT CHECK FAILED")
        for error in hard_errors:
            print(f"- {error}")
        for warning in warnings:
            print(f"- {warning}")
        return 1
    print("PROOF OBJECT CHECK PASSED")
    for warning in warnings:
        print(f"- {warning}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
