from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
DEFAULT_SPEC = HERE / "compositional-invariant-spec-v1.0.json"
DEFAULT_RESULT = HERE / "compositional-invariant-result-v1.0.json"
DEFAULT_REPORT = HERE / "compositional-invariant-terminal-result-v1.0.md"
DEFAULT_README = HERE / "README.md"
DEFAULT_CHARTER = HERE / "scope-and-universality-charter-v1.2.md"
DEFAULT_GATES = ROOT / "theory/evaluation/research-gates.json"

EXPECTED_BASE = "d1fc8053e1459a7829f6f24b8d187f7887375cf0"
EXPECTED_SPEC_SHA256 = "d402f13377b89a54fa32346bb542283850cc4dc4d196ffbe37cad97b086342f3"
EXPECTED_PUBLIC_SHA256 = {
    "README": "e170173af98e194cbfccc52f9970499c43dcba40c3494f3c7b09299becd83ecd",
    "Charter": "29be2d7d7b5f65a871323126cd3e181c22db7b062957a414aac7576549e94c01",
    "Report": "b3b4d03bc80b235f17b2ca25846b5142a9584e287cf8cbe9c9c0e31eeb9f0473",
}
PUBLIC_NONCLAIMS = ['No weakest invariant-supporting structure has been proved.', 'No first invariant-supporting structure has been proved.', 'No minimal invariant-supporting structure has been proved.', 'No globally optimal invariant-supporting structure has been proved.', 'Small categories are not claimed to be broader than bare sets under a common comparison order.', 'No complete architecture of reasoning is established.', 'RCCD is not derived.', 'The empirical clean-room program has not been executed.', 'Accepted Project FAR theory is unchanged.', 'This result is not released while RG-07 remains unsatisfied.']
EXPECTED_SPEC = {'id': 'TCD-COMPOSITIONAL-INVARIANT-001', 'version': '1.1', 'status': 'Research', 'base_commit': 'd1fc8053e1459a7829f6f24b8d187f7887375cf0', 'question': 'Within an independently stated typed-compositional scope, which finitary arrow-valued operations are invariant under every admissible recoding, without assuming RCCD components?', 'broadness_policy': {'absolute_maximum_claimed': False, 'reason': 'Broadest is undefined until a comparison order and admissible recodings are fixed.', 'selected_scope': 'all small categories', 'scope_criterion': 'A system is included exactly when it supplies the set-sized category data and laws in TC1-TC4.', 'recodings': 'all functors'}, 'axioms': [{'id': 'TC1', 'statement': 'Objects and arrows are sets, with total source and target functions from arrows to objects.'}, {'id': 'TC2', 'statement': 'A total designated identity assignment maps every object X to one arrow id_X:X->X.'}, {'id': 'TC3', 'statement': 'A single-valued composition operation is defined exactly on composable ordered pairs (f,g) with target(f)=source(g), and returns g∘f with source(g∘f)=source(f) and target(g∘f)=target(g).'}, {'id': 'TC4', 'statement': 'For every well-typed arrow and composable triple, identities are two-sided units and composition is associative.'}], 'input_operation_schema': {'input': 'a finite directed graph G with distinguished vertices s and t', 'presentation': 'a graph map x:G->U(C) into the underlying graph of a small category C', 'output': 'an arrow alpha_C(x):x(s)->x(t)', 'invariance': 'for every functor H:C->D, H(alpha_C(x))=alpha_D(H composed with x)'}, 'theorem_claims': [{'id': 'TCD-CI-T1', 'statement': 'TC1-TC4 specify exactly a small category, and structure-preserving recodings are exactly functors.', 'status': 'proved_in_internal_research_report'}, {'id': 'TCD-CI-T2', 'statement': 'Every finitary arrow-valued operation invariant under all functors is evaluation of one unique fixed path in the free category on its input graph; conversely every fixed path defines such an invariant operation.', 'status': 'proved_in_internal_research_report'}, {'id': 'TCD-CI-C1', 'statement': 'For an input graph with a composable chain from s to t, sequential composition can supply a nonidentity invariant path such as b∘a. Identity paths remain structural path terms only when s=t and are not classified as nontrivial.', 'status': 'corollary'}, {'id': 'TCD-CI-C2', 'statement': 'No RCCD-specific generator, operator, observation, objective, decomposition, or policy follows from typed composition alone.', 'status': 'corollary'}], 'fixture': {'objects': ['A', 'B', 'C'], 'generators': [{'name': 'a', 'source': 'A', 'target': 'B'}, {'name': 'b', 'source': 'B', 'target': 'C'}, {'name': 'c', 'source': 'A', 'target': 'C'}], 'distinguished_source': 'A', 'distinguished_target': 'C', 'expected_paths_from_source_to_target': ['c', 'b∘a'], 'expected_new_nonidentity_paths_after_free_completion': ['b∘a'], 'identity_is_nontrivial_for_distinguished_shape': False}, 'disposition': {'classification': 'scoped_theorem_established_internal_release_blocked', 'scope_status': 'resolved_within_declared_small_category_scope', 'release_status': 'blocked_by_rg_07_nonclaim_audit', 'empirical_program_status': 'not_executed', 'rccd_status': 'not_derived', 'accepted_theory_change': False, 'strongest_internal_claim': 'Across all small categories and functors, the complete finitary arrow-valued invariant operations for a fixed finite input graph are evaluations of unique path terms generated by identities and typed sequential composition.', 'next_release_condition': 'A separately evidenced RG-07 nonclaim audit and a new reviewed version are required before theorem release.'}, 'nonclaims': ['No weakest invariant-supporting structure has been proved.', 'No first invariant-supporting structure has been proved.', 'No minimal invariant-supporting structure has been proved.', 'No globally optimal invariant-supporting structure has been proved.', 'Small categories are not claimed to be broader than bare sets under a common comparison order.', 'No complete architecture of reasoning is established.', 'RCCD is not derived.', 'The empirical clean-room program has not been executed.', 'Accepted Project FAR theory is unchanged.', 'This result is not released while RG-07 remains unsatisfied.']}


class VerificationError(ValueError):
    pass


def _reject_constant(value: str) -> None:
    raise VerificationError(f"non-finite JSON number rejected: {value}")


def _no_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in pairs:
        if key in out:
            raise VerificationError(f"duplicate JSON key rejected: {key}")
        out[key] = value
    return out


def load_json(path: Path) -> dict[str, Any]:
    raw = path.read_bytes()
    if raw.startswith(b"\xef\xbb\xbf"):
        raise VerificationError(f"UTF-8 BOM rejected: {path}")
    try:
        value = json.loads(raw.decode("utf-8"), object_pairs_hook=_no_duplicate_keys, parse_constant=_reject_constant)
    except UnicodeDecodeError as exc:
        raise VerificationError(f"invalid UTF-8 in {path}") from exc
    except json.JSONDecodeError as exc:
        raise VerificationError(f"invalid JSON in {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise VerificationError(f"top-level JSON object required: {path}")
    return value


def canonical_json(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")


def validate_spec(spec: dict[str, Any]) -> None:
    if spec != EXPECTED_SPEC:
        raise VerificationError("frozen specification or claim boundary drifted")
    base = spec.get("base_commit")
    if not isinstance(base, str) or re.fullmatch(r"[0-9a-f]{40}", base) is None or base != EXPECTED_BASE:
        raise VerificationError("base_commit does not match the frozen lowercase hexadecimal repository base")
    if hashlib.sha256(canonical_json(spec)).hexdigest() != EXPECTED_SPEC_SHA256:
        raise VerificationError("canonical specification digest drifted")


def _free_category() -> tuple[list[tuple[str, tuple[str, ...]]], dict[str, tuple[str, str]]]:
    fixture = EXPECTED_SPEC["fixture"]
    generators = {g["name"]: (g["source"], g["target"]) for g in fixture["generators"]}
    outgoing: dict[str, list[str]] = {obj: [] for obj in fixture["objects"]}
    for name, (source, _) in generators.items():
        outgoing[source].append(name)

    def target(path: tuple[str, tuple[str, ...]]) -> str:
        current = path[0]
        for edge in path[1]:
            source, destination = generators[edge]
            if source != current:
                raise VerificationError("ill-typed path")
            current = destination
        return current

    paths: list[tuple[str, tuple[str, ...]]] = []
    def extend(path: tuple[str, tuple[str, ...]]) -> None:
        paths.append(path)
        for edge in outgoing[target(path)]:
            extend((path[0], path[1] + (edge,)))
    for obj in fixture["objects"]:
        extend((obj, ()))
    return sorted(set(paths), key=lambda p: (p[0], len(p[1]), p[1])), generators


def _render(path: tuple[str, tuple[str, ...]]) -> str:
    return f"id_{path[0]}" if not path[1] else "∘".join(reversed(path[1]))


def build_result(spec: dict[str, Any]) -> dict[str, Any]:
    validate_spec(spec)
    arrows, generators = _free_category()

    def target(path: tuple[str, tuple[str, ...]]) -> str:
        current = path[0]
        for edge in path[1]:
            source, destination = generators[edge]
            if source != current:
                raise VerificationError("ill-typed path")
            current = destination
        return current

    def compose(first: tuple[str, tuple[str, ...]], second: tuple[str, tuple[str, ...]]) -> tuple[str, tuple[str, ...]]:
        if target(first) != second[0]:
            raise VerificationError("non-composable arrows")
        return first[0], first[1] + second[1]

    identity_checks = 0
    for arrow in arrows:
        if compose((arrow[0], ()), arrow) != arrow or compose(arrow, (target(arrow), ())) != arrow:
            raise VerificationError("identity law failed")
        identity_checks += 2

    associativity_checks = 0
    for first in arrows:
        for second in arrows:
            if target(first) != second[0]:
                continue
            for third in arrows:
                if target(second) != third[0]:
                    continue
                if compose(compose(first, second), third) != compose(first, compose(second, third)):
                    raise VerificationError("associativity failed")
                associativity_checks += 1

    distinguished = [_render(path) for path in arrows if path[0] == "A" and target(path) == "C"]
    if distinguished != ["c", "b∘a"]:
        raise VerificationError("distinguished path set drifted")
    if any(path.startswith("id_") for path in distinguished):
        raise VerificationError("identity cannot inhabit the distinct-endpoint A->C operation shape")

    composite = compose(("A", ("a",)), ("B", ("b",)))
    if _render(composite) != "b∘a":
        raise VerificationError("nontrivial composite witness changed")
    nonidentity = {_render(path) for path in arrows if path[1]}
    new_paths = sorted(nonidentity - set(generators))
    if new_paths != ["b∘a"]:
        raise VerificationError("free-completion witness set drifted")

    words = {"a": "x", "b": "yz", "c": "q"}
    word = "".join(words[edge] for edge in composite[1])
    if word != "xyz":
        raise VerificationError("functorial recoding witness failed")

    evidence = {
        "fixture_object_count": 3,
        "fixture_generator_count": 3,
        "free_category_arrow_count": len(arrows),
        "free_category_nonidentity_arrow_count": len(nonidentity),
        "new_nonidentity_paths": new_paths,
        "distinguished_paths": distinguished,
        "nontrivial_invariant_witness": "b∘a",
        "identity_is_nontrivial_witness": False,
        "identity_is_admissible_for_distinguished_A_to_C_shape": False,
        "identity_law_checks": identity_checks,
        "associativity_checks": associativity_checks,
        "word_functor_composite": word,
        "path_classification_argument": "Evaluation on the identity presentation in the free category selects one path; naturality forces every other value to be its image.",
    }
    result = {
        "id": EXPECTED_SPEC["id"],
        "version": EXPECTED_SPEC["version"],
        "status": "Research",
        **EXPECTED_SPEC["disposition"],
        "theorem_status": "hand_proof_with_bounded_executable_corroboration",
        "evidence": evidence,
        "nonclaims": PUBLIC_NONCLAIMS,
    }
    result["evidence_sha256"] = hashlib.sha256(canonical_json(evidence)).hexdigest()
    return result


def validate_public_surface(name: str, path: Path) -> None:
    raw = path.read_bytes()
    if raw.startswith(b"\xef\xbb\xbf"):
        raise VerificationError(f"UTF-8 BOM rejected: {path}")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise VerificationError(f"invalid UTF-8 in {path}") from exc
    if hashlib.sha256(raw).hexdigest() != EXPECTED_PUBLIC_SHA256[name]:
        raise VerificationError(f"{name} public claim surface drifted")
    for line in PUBLIC_NONCLAIMS:
        if text.count(line) != 1:
            raise VerificationError(f"{name} must preserve each public nonclaim exactly once: {line}")


def validate_gate(gates_path: Path) -> None:
    gates = load_json(gates_path)
    entries = gates.get("gates")
    if not isinstance(entries, list):
        raise VerificationError("research gate registry missing gates list")
    rg07 = [item for item in entries if isinstance(item, dict) and item.get("id") == "RG-07"]
    if len(rg07) != 1:
        raise VerificationError("exactly one RG-07 gate required")
    gate = rg07[0]
    if gate.get("name") != "nonclaim-audit" or gate.get("status") != "not_satisfied" or gate.get("evidence") != []:
        raise VerificationError("RG-07 state changed; this blocked Research artifact requires a new reviewed version")
    required = gate.get("required_before")
    if not isinstance(required, list) or "theorem_release" not in required:
        raise VerificationError("RG-07 must remain required before theorem_release")


def verify(spec_path: Path = DEFAULT_SPEC, result_path: Path = DEFAULT_RESULT, report_path: Path = DEFAULT_REPORT,
           readme_path: Path = DEFAULT_README, charter_path: Path = DEFAULT_CHARTER, gates_path: Path = DEFAULT_GATES) -> dict[str, Any]:
    actual = build_result(load_json(spec_path))
    if actual != load_json(result_path):
        raise VerificationError("committed result does not match a fresh rebuild")
    validate_public_surface("README", readme_path)
    validate_public_surface("Charter", charter_path)
    validate_public_surface("Report", report_path)
    validate_gate(gates_path)
    if actual["release_status"] != "blocked_by_rg_07_nonclaim_audit":
        raise VerificationError("release must remain blocked")
    return actual


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--spec", type=Path, default=DEFAULT_SPEC)
    parser.add_argument("--result", type=Path, default=DEFAULT_RESULT)
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--readme", type=Path, default=DEFAULT_README)
    parser.add_argument("--charter", type=Path, default=DEFAULT_CHARTER)
    parser.add_argument("--gates", type=Path, default=DEFAULT_GATES)
    args = parser.parse_args()
    try:
        result = verify(args.spec, args.result, args.report, args.readme, args.charter, args.gates)
    except VerificationError as exc:
        print(f"FAIL: {exc}")
        return 1
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
