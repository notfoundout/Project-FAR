#!/usr/bin/env python3
"""Project FAR theory verifier.

This script enforces the first machine-readable theory checks:

- every theorem in metadata has required fields;
- every theorem proof file exists;
- every established theorem listed in the catalog has a proof file;
- every established theorem has metadata;
- dependencies resolve to known identifiers or known canonical resources;
- theorem dependency graph has no cycles;
- no theorem depends on itself;
- derived concepts listed in metadata are registered;
- proof files use canonical notation references when required;
- a generated theorem index can be written from metadata.

The checks are intentionally conservative. A failing check means the repository
needs correction or the verifier needs an explicit whitelist entry.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List, Set

ROOT = Path(__file__).resolve().parents[1]
THEOREM_METADATA = ROOT / "theory" / "metadata" / "theorems.yaml"
THEOREM_CATALOG = ROOT / "theory" / "theorems" / "theorems.md"
DERIVED_REGISTRY = ROOT / "theory" / "derivations" / "derived-concept-registry.md"
CANONICAL_NOTATION = ROOT / "theory" / "notation" / "canonical-notation.md"
GENERATED_INDEX = ROOT / "theory" / "metadata" / "generated-theorem-index.md"

REQUIRED_THEOREM_FIELDS = {"id", "title", "status", "proof", "scope", "dependencies", "derived_concepts"}
KNOWN_STATUSES = {"Draft", "Proposed", "Verified", "Established", "Deprecated"}

# Canonical non-file dependencies. These are intentionally explicit; adding to
# this list is a theory-governance decision, not a shortcut.
KNOWN_DEPENDENCIES = {
    "A1", "A2", "A3", "A4", "A5",
    "D-REP", "D-INT", "D-CALC", "D-INV", "D-STRUCT",
    "P-001", "P-002", "P-003", "P-004", "P-005", "P-006", "P-007", "P-008",
    "L-001", "L-002", "L-003", "L-004", "L-005", "L-006", "L-007", "L-008",
    "derived-concept-registry",
    "canonical-notation",
    "definition-policy",
    "FAR-model-theory",
}

CANONICAL_SYMBOLS = ["I", "Rep", "S", "Int", "C", "T"]
CANONICAL_SPECIAL_SYMBOLS = ["⊨", "≡sem", "≡str", "≡Q", "NF"]


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
        raise VerificationError("Theorem metadata must parse to a mapping.")
    return data


def load_theorems() -> List[Dict[str, Any]]:
    data = load_yaml(THEOREM_METADATA)
    theorems = data.get("theorems")
    if not isinstance(theorems, list):
        raise VerificationError("theory/metadata/theorems.yaml must contain a 'theorems' list.")
    return theorems


def registered_derived_concepts() -> Set[str]:
    text = read_text(DERIVED_REGISTRY)
    return set(re.findall(r"\bD-\d{3}\b", text))


def established_catalog_theorem_ids() -> Set[str]:
    """Return theorem IDs only from the Established Theorems section.

    The theorem catalog also contains planned research targets, such as T-016.
    Planned theorem IDs should not be required to have proof files or established
    metadata. This parser intentionally ignores everything after the Planned
    Theorems heading.
    """

    text = read_text(THEOREM_CATALOG)
    established_start = text.find("# Established Theorems")
    if established_start == -1:
        raise VerificationError("The theorem catalog is missing '# Established Theorems'.")

    planned_start = text.find("# Planned Theorems", established_start)
    if planned_start == -1:
        section = text[established_start:]
    else:
        section = text[established_start:planned_start]

    return set(re.findall(r"\bT-\d{3}\b", section))


def proof_theorem_ids() -> Set[str]:
    proof_dir = ROOT / "theory" / "proofs"
    ids: Set[str] = set()
    if not proof_dir.exists():
        return ids
    for path in proof_dir.glob("T-*.md"):
        match = re.match(r"(T-\d{3})", path.name)
        if match:
            ids.add(match.group(1))
    return ids


def validate_required_fields(theorems: List[Dict[str, Any]]) -> None:
    seen: Set[str] = set()
    for item in theorems:
        if not isinstance(item, dict):
            raise VerificationError("Each theorem metadata entry must be a mapping.")
        missing = REQUIRED_THEOREM_FIELDS - set(item)
        if missing:
            raise VerificationError(f"Theorem entry missing fields {sorted(missing)}: {item}")
        theorem_id = item["id"]
        if not re.fullmatch(r"T-\d{3}", str(theorem_id)):
            raise VerificationError(f"Invalid theorem id: {theorem_id}")
        if theorem_id in seen:
            raise VerificationError(f"Duplicate theorem id: {theorem_id}")
        seen.add(theorem_id)
        if item["status"] not in KNOWN_STATUSES:
            raise VerificationError(f"Invalid status for {theorem_id}: {item['status']}")
        if not isinstance(item["dependencies"], list):
            raise VerificationError(f"dependencies must be a list for {theorem_id}")
        if not isinstance(item["derived_concepts"], list):
            raise VerificationError(f"derived_concepts must be a list for {theorem_id}")


def validate_proof_files(theorems: List[Dict[str, Any]]) -> None:
    for item in theorems:
        proof_path = ROOT / item["proof"]
        if not proof_path.exists():
            raise VerificationError(f"Missing proof file for {item['id']}: {item['proof']}")
        proof_text = read_text(proof_path)
        if item["id"] not in proof_text:
            raise VerificationError(f"Proof file for {item['id']} does not contain its theorem id.")


def validate_catalog_consistency(theorems: List[Dict[str, Any]]) -> None:
    metadata_ids = {item["id"] for item in theorems}
    established_catalog_ids = established_catalog_theorem_ids()
    proof_ids = proof_theorem_ids()

    missing_metadata = sorted(established_catalog_ids - metadata_ids)
    if missing_metadata:
        raise VerificationError(f"Established theorem catalog ids missing metadata: {missing_metadata}")

    missing_proofs = sorted(established_catalog_ids - proof_ids)
    if missing_proofs:
        raise VerificationError(f"Established theorem catalog ids missing proof files: {missing_proofs}")

    metadata_without_catalog = sorted(metadata_ids - established_catalog_ids)
    if metadata_without_catalog:
        raise VerificationError(f"Metadata theorem ids missing from established theorem catalog: {metadata_without_catalog}")


def validate_dependencies(theorems: List[Dict[str, Any]]) -> Dict[str, Set[str]]:
    theorem_ids = {item["id"] for item in theorems}
    graph: Dict[str, Set[str]] = {item["id"]: set() for item in theorems}

    for item in theorems:
        theorem_id = item["id"]
        for dep in item["dependencies"]:
            dep = str(dep)
            if dep == theorem_id:
                raise VerificationError(f"{theorem_id} directly depends on itself.")
            if re.fullmatch(r"T-\d{3}", dep):
                if dep not in theorem_ids:
                    raise VerificationError(f"{theorem_id} depends on unknown theorem {dep}.")
                graph[theorem_id].add(dep)
            elif dep not in KNOWN_DEPENDENCIES:
                raise VerificationError(f"{theorem_id} has unresolved dependency: {dep}")
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


def build_index(theorems: List[Dict[str, Any]]) -> str:
    lines = [
        "# Generated Theorem Index",
        "",
        "This file is generated from `theory/metadata/theorems.yaml`.",
        "",
        "| ID | Title | Status | Proof | Scope |",
        "|---|---|---|---|---|",
    ]
    for item in sorted(theorems, key=lambda x: x["id"]):
        lines.append(
            f"| {item['id']} | {item['title']} | {item['status']} | `{item['proof']}` | {item['scope']} |"
        )
    lines.append("")
    return "\n".join(lines)


def write_index(theorems: List[Dict[str, Any]]) -> None:
    GENERATED_INDEX.write_text(build_index(theorems), encoding="utf-8")


def run_verification(write_generated_index: bool = False) -> None:
    theorems = load_theorems()
    validate_required_fields(theorems)
    validate_proof_files(theorems)
    validate_catalog_consistency(theorems)
    graph = validate_dependencies(theorems)
    validate_no_cycles(graph)
    validate_registry(theorems)
    validate_notation_file()
    if write_generated_index:
        write_index(theorems)


def main(argv: Iterable[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Verify Project FAR theory metadata and proof structure.")
    parser.add_argument("--write-index", action="store_true", help="write generated theorem index")
    args = parser.parse_args(list(argv) if argv is not None else None)

    try:
        run_verification(write_generated_index=args.write_index)
    except VerificationError as exc:
        print(f"VERIFY THEORY FAILED: {exc}", file=sys.stderr)
        return 1

    print("VERIFY THEORY PASSED")
    if args.write_index:
        print(f"Wrote {GENERATED_INDEX.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
