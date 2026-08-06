from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

HERE = Path(__file__).resolve().parent
DEFAULT_SPEC = HERE / "compositional-invariant-spec-v1.0.json"
DEFAULT_RESULT = HERE / "compositional-invariant-result-v1.0.json"
DEFAULT_REPORT = HERE / "compositional-invariant-terminal-result-v1.0.md"

EXPECTED_ID = "TCD-COMPOSITIONAL-INVARIANT-001"
EXPECTED_AXIOMS = {
    "TC1": "Every step has a source interface and a target interface.",
    "TC2": "Every interface has an identity step.",
    "TC3": (
        "Whenever the target of one step equals the source of another, "
        "their sequential composite exists."
    ),
    "TC4": (
        "Identity steps are two-sided units and sequential composition is associative."
    ),
}
EXPECTED_THEOREM_IDS = ["TCD-CI-T1", "TCD-CI-T2", "TCD-CI-C1", "TCD-CI-C2"]
EXPECTED_NONCLAIMS = {
    "small categories are the absolute broadest possible class of every conceivable reasoning system",
    "all reasoning is sequential",
    "typed composition is a complete architecture of reasoning",
    "RCCD is false",
    "RCCD is necessary, minimal, unique, or Pareto-optimal",
    "the clean-room target-category study has been executed",
    "the result changes accepted Project FAR theory",
}


class VerificationError(ValueError):
    pass


def _reject_constant(value: str) -> None:
    raise VerificationError(f"non-finite JSON number rejected: {value}")


def _object_no_duplicates(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise VerificationError(f"duplicate JSON key rejected: {key}")
        result[key] = value
    return result


def load_json(path: Path) -> dict[str, Any]:
    raw = path.read_bytes()
    if raw.startswith(b"\xef\xbb\xbf"):
        raise VerificationError(f"UTF-8 BOM rejected: {path}")
    try:
        value = json.loads(
            raw.decode("utf-8"),
            object_pairs_hook=_object_no_duplicates,
            parse_constant=_reject_constant,
        )
    except UnicodeDecodeError as exc:
        raise VerificationError(f"invalid UTF-8 in {path}") from exc
    except json.JSONDecodeError as exc:
        raise VerificationError(f"invalid JSON in {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise VerificationError(f"top-level JSON object required: {path}")
    return value


def canonical_json(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")


@dataclass(frozen=True)
class Generator:
    name: str
    source: str
    target: str


@dataclass(frozen=True)
class PathArrow:
    source: str
    edges: tuple[str, ...]

    def render(self) -> str:
        if not self.edges:
            return f"id_{self.source}"
        return "∘".join(reversed(self.edges))


class FreeAcyclicCategory:
    def __init__(self, objects: Iterable[str], generators: Iterable[Generator]) -> None:
        self.objects = tuple(objects)
        if len(set(self.objects)) != len(self.objects):
            raise VerificationError("fixture objects must be unique")
        self.generators = tuple(generators)
        self.by_name = {generator.name: generator for generator in self.generators}
        if len(self.by_name) != len(self.generators):
            raise VerificationError("fixture generator names must be unique")
        object_set = set(self.objects)
        for generator in self.generators:
            if generator.source not in object_set or generator.target not in object_set:
                raise VerificationError("fixture generator references an unknown object")
        self._check_acyclic()
        self.arrows = tuple(self._enumerate_paths())

    def _check_acyclic(self) -> None:
        adjacency = {obj: [] for obj in self.objects}
        for generator in self.generators:
            adjacency[generator.source].append(generator.target)
        visiting: set[str] = set()
        visited: set[str] = set()

        def visit(obj: str) -> None:
            if obj in visiting:
                raise VerificationError("bounded fixture must be acyclic")
            if obj in visited:
                return
            visiting.add(obj)
            for target in adjacency[obj]:
                visit(target)
            visiting.remove(obj)
            visited.add(obj)

        for obj in self.objects:
            visit(obj)

    def target(self, arrow: PathArrow) -> str:
        current = arrow.source
        for edge_name in arrow.edges:
            generator = self.by_name.get(edge_name)
            if generator is None or generator.source != current:
                raise VerificationError(f"ill-typed path: {arrow}")
            current = generator.target
        return current

    def identity(self, obj: str) -> PathArrow:
        if obj not in self.objects:
            raise VerificationError(f"unknown object: {obj}")
        return PathArrow(obj, ())

    def compose(self, first: PathArrow, second: PathArrow) -> PathArrow:
        """Return second after first."""
        if self.target(first) != second.source:
            raise VerificationError("non-composable arrows")
        result = PathArrow(first.source, first.edges + second.edges)
        self.target(result)
        return result

    def _enumerate_paths(self) -> list[PathArrow]:
        outgoing: dict[str, list[Generator]] = {obj: [] for obj in self.objects}
        for generator in self.generators:
            outgoing[generator.source].append(generator)
        paths: list[PathArrow] = []

        def extend(path: PathArrow) -> None:
            paths.append(path)
            current = self.target(path)
            for generator in outgoing[current]:
                extend(PathArrow(path.source, path.edges + (generator.name,)))

        for obj in self.objects:
            extend(self.identity(obj))
        unique = {(path.source, path.edges): path for path in paths}
        return sorted(
            unique.values(),
            key=lambda path: (path.source, len(path.edges), path.edges),
        )

    def paths_between(self, source: str, target: str) -> list[PathArrow]:
        return [
            arrow
            for arrow in self.arrows
            if arrow.source == source and self.target(arrow) == target
        ]

    def verify_category_laws(self) -> dict[str, int]:
        identity_checks = 0
        associativity_checks = 0
        for arrow in self.arrows:
            left = self.compose(self.identity(arrow.source), arrow)
            right = self.compose(arrow, self.identity(self.target(arrow)))
            if left != arrow or right != arrow:
                raise VerificationError("identity law failed")
            identity_checks += 2

        for first in self.arrows:
            for second in self.arrows:
                if self.target(first) != second.source:
                    continue
                for third in self.arrows:
                    if self.target(second) != third.source:
                        continue
                    lhs = self.compose(self.compose(first, second), third)
                    rhs = self.compose(first, self.compose(second, third))
                    if lhs != rhs:
                        raise VerificationError("associativity failed")
                    associativity_checks += 1
        return {
            "identity_law_checks": identity_checks,
            "associativity_checks": associativity_checks,
        }


def _validate_exact_spec(spec: dict[str, Any]) -> None:
    required_top = {
        "id",
        "version",
        "status",
        "base_commit",
        "question",
        "broadness_policy",
        "axioms",
        "input_operation_schema",
        "theorem_claims",
        "fixture",
        "terminal_disposition",
        "nonclaims",
    }
    if set(spec) != required_top:
        raise VerificationError("spec top-level keys drifted")
    if spec["id"] != EXPECTED_ID or spec["version"] != "1.0" or spec["status"] != "Research":
        raise VerificationError("spec identity/version/status drifted")
    base_commit = spec["base_commit"]
    if not isinstance(base_commit, str) or len(base_commit) != 40:
        raise VerificationError("base_commit must be a full 40-character commit SHA")

    policy = spec["broadness_policy"]
    if not isinstance(policy, dict):
        raise VerificationError("broadness_policy must be an object")
    expected_policy = {
        "absolute_maximum_claimed": False,
        "reason": "Broadest is undefined until a comparison order and admissible recodings are fixed.",
        "selected_scope": "all small typed compositional systems",
        "scope_criterion": (
            "A system is included exactly when its typed steps have identities and "
            "associative sequential composition."
        ),
        "recodings": "all functors",
    }
    if policy != expected_policy:
        raise VerificationError("broadness policy drifted")

    axioms = spec["axioms"]
    if not isinstance(axioms, list) or len(axioms) != len(EXPECTED_AXIOMS):
        raise VerificationError("exact four-axiom contract required")
    actual_axioms: dict[str, str] = {}
    for axiom in axioms:
        if not isinstance(axiom, dict) or set(axiom) != {"id", "statement"}:
            raise VerificationError("malformed axiom")
        if not isinstance(axiom["id"], str) or not isinstance(axiom["statement"], str):
            raise VerificationError("axiom fields must be strings")
        actual_axioms[axiom["id"]] = axiom["statement"]
    if actual_axioms != EXPECTED_AXIOMS:
        raise VerificationError("typed-composition axioms drifted")

    claims = spec["theorem_claims"]
    if not isinstance(claims, list):
        raise VerificationError("theorem_claims must be a list")
    claim_ids = [claim.get("id") for claim in claims if isinstance(claim, dict)]
    if claim_ids != EXPECTED_THEOREM_IDS:
        raise VerificationError("theorem claim registry drifted")
    if any(set(claim) != {"id", "statement", "status"} for claim in claims):
        raise VerificationError("malformed theorem claim")

    disposition = spec["terminal_disposition"]
    expected_disposition = {
        "classification": "scoped_theoretical_question_closed",
        "strongest_claim": (
            "Across all small typed compositional systems and all functorial recodings, "
            "the complete finitary arrow-valued invariant operations are path terms "
            "generated by identities and sequential composition."
        ),
        "empirical_program_status": "not_executed",
        "rccd_status": "not_derived",
        "remaining_question": (
            "Whether RCCD or another richer basis is necessary, economical, or "
            "Pareto-optimal for the separately chosen explicitly auditable-artifact "
            "class remains empirical and open."
        ),
    }
    if disposition != expected_disposition:
        raise VerificationError("terminal disposition or claim boundary drifted")

    nonclaims = spec["nonclaims"]
    if not isinstance(nonclaims, list) or set(nonclaims) != EXPECTED_NONCLAIMS:
        raise VerificationError("nonclaim set drifted")


def _fixture_category(spec: dict[str, Any]) -> tuple[FreeAcyclicCategory, str, str]:
    fixture = spec["fixture"]
    if not isinstance(fixture, dict):
        raise VerificationError("fixture must be an object")
    expected_keys = {
        "objects",
        "generators",
        "distinguished_source",
        "distinguished_target",
        "expected_paths_from_source_to_target",
        "expected_new_nonidentity_paths_after_free_completion",
    }
    if set(fixture) != expected_keys:
        raise VerificationError("fixture keys drifted")
    objects = fixture["objects"]
    generators_raw = fixture["generators"]
    if not isinstance(objects, list) or not all(isinstance(obj, str) for obj in objects):
        raise VerificationError("fixture objects must be strings")
    if not isinstance(generators_raw, list):
        raise VerificationError("fixture generators must be a list")
    generators: list[Generator] = []
    for entry in generators_raw:
        if not isinstance(entry, dict) or set(entry) != {"name", "source", "target"}:
            raise VerificationError("malformed fixture generator")
        if not all(isinstance(entry[key], str) for key in ("name", "source", "target")):
            raise VerificationError("generator fields must be strings")
        generators.append(Generator(entry["name"], entry["source"], entry["target"]))
    source = fixture["distinguished_source"]
    target = fixture["distinguished_target"]
    if not isinstance(source, str) or not isinstance(target, str):
        raise VerificationError("distinguished endpoints must be strings")
    return FreeAcyclicCategory(objects, generators), source, target


def _evaluate_word_functor(path: PathArrow, generator_words: dict[str, str]) -> str:
    return "".join(generator_words[name] for name in path.edges)


def build_result(spec: dict[str, Any]) -> dict[str, Any]:
    _validate_exact_spec(spec)
    category, source, target = _fixture_category(spec)
    laws = category.verify_category_laws()

    distinguished = category.paths_between(source, target)
    rendered = [path.render() for path in distinguished]
    expected_rendered = spec["fixture"]["expected_paths_from_source_to_target"]
    if rendered != expected_rendered:
        raise VerificationError(
            f"distinguished path set mismatch: expected {expected_rendered}, got {rendered}"
        )

    generator_paths = {
        generator.name: PathArrow(generator.source, (generator.name,))
        for generator in category.generators
    }
    composite = category.compose(generator_paths["a"], generator_paths["b"])
    if composite.render() != "b∘a":
        raise VerificationError("nontrivial composite witness changed")
    if composite in generator_paths.values() or not composite.edges:
        raise VerificationError("composite witness is not genuinely new")

    original_nonidentity = {generator.name for generator in category.generators}
    completed_nonidentity = {
        arrow.render() for arrow in category.arrows if arrow.edges
    }
    new_nonidentity = sorted(completed_nonidentity - original_nonidentity)
    if new_nonidentity != spec["fixture"]["expected_new_nonidentity_paths_after_free_completion"]:
        raise VerificationError("free-completion witness set drifted")

    # Bounded executable corroboration of functorial invariance. A graph presentation
    # is interpreted in the one-object category of words under concatenation, then
    # recoded by word length into the additive monoid of natural numbers.
    generator_words = {"a": "x", "b": "yz", "c": "q"}
    word_value = _evaluate_word_functor(composite, generator_words)
    direct_word = generator_words["a"] + generator_words["b"]
    if word_value != direct_word:
        raise VerificationError("word-category functor failed to preserve composition")
    length_value = len(word_value)
    recoded_composite = len(generator_words["a"]) + len(generator_words["b"])
    if length_value != recoded_composite:
        raise VerificationError("length recoding failed functorial invariance")

    evidence = {
        "fixture_object_count": len(category.objects),
        "fixture_generator_count": len(category.generators),
        "free_category_arrow_count": len(category.arrows),
        "free_category_nonidentity_arrow_count": len(completed_nonidentity),
        "new_nonidentity_path_count": len(new_nonidentity),
        "new_nonidentity_paths": new_nonidentity,
        "distinguished_path_count": len(distinguished),
        "distinguished_paths": rendered,
        "nontrivial_composite": composite.render(),
        "graph_only_has_composite": False,
        "free_category_has_composite": True,
        "identity_law_checks": laws["identity_law_checks"],
        "associativity_checks": laws["associativity_checks"],
        "word_functor_composite": word_value,
        "length_recoding_composite": length_value,
        "path_term_classification_witness": (
            "The operation's value on the identity presentation in the free category "
            "selects one path; naturality forces every other value to be that path's image."
        ),
    }
    result_core = {
        "id": EXPECTED_ID,
        "version": "1.0",
        "status": "Research",
        "classification": "scoped_theoretical_question_closed",
        "theorem_status": "hand_proof_with_bounded_executable_corroboration",
        "strongest_claim": spec["terminal_disposition"]["strongest_claim"],
        "rccd_status": "not_derived",
        "empirical_program_status": "not_executed",
        "evidence": evidence,
        "nonclaims": sorted(EXPECTED_NONCLAIMS),
    }
    result_core["evidence_sha256"] = hashlib.sha256(canonical_json(evidence)).hexdigest()
    return result_core


def _validate_report(report_path: Path) -> None:
    text = report_path.read_text(encoding="utf-8")
    required_phrases = [
        "# Compositional Invariant Terminal Result v1.0",
        "TCD-COMPOSITIONAL-INVARIANT-001",
        "## 5. Theorem 2: path-term classification",
        "No RCCD-specific operation follows",
        "The clean-room empirical program is not complete",
        "Small categories are the absolute broadest possible class",
    ]
    missing = [phrase for phrase in required_phrases if phrase not in text]
    if missing:
        raise VerificationError(f"report is missing required claim-boundary text: {missing}")


def verify(
    spec_path: Path = DEFAULT_SPEC,
    result_path: Path = DEFAULT_RESULT,
    report_path: Path = DEFAULT_REPORT,
) -> dict[str, Any]:
    spec = load_json(spec_path)
    actual = build_result(spec)
    expected = load_json(result_path)
    if actual != expected:
        raise VerificationError("committed result does not match a fresh rebuild")
    _validate_report(report_path)
    return actual


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--spec", type=Path, default=DEFAULT_SPEC)
    parser.add_argument("--result", type=Path, default=DEFAULT_RESULT)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()

    spec = load_json(args.spec)
    actual = build_result(spec)
    if args.write:
        args.result.write_text(
            json.dumps(actual, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    else:
        expected = load_json(args.result)
        if actual != expected:
            raise VerificationError("committed result does not match a fresh rebuild")
    _validate_report(args.report)
    print(
        "PASS: typed-compositional invariant result; "
        f"{actual['evidence']['free_category_arrow_count']} arrows; "
        f"paths={actual['evidence']['distinguished_paths']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
