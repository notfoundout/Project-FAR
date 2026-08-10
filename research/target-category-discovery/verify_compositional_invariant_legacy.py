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
DEFAULT_EMPIRICAL_CHARTER = HERE / "scope-and-universality-charter-v1.1.md"
DEFAULT_EMPIRICAL_MANIFEST = HERE / "audit-manifest-v1.0.json"
DEFAULT_CHAT_AUDIT = HERE / "chat-audit-2026-08-05.md"
DEFAULT_GATES = ROOT / "theory/evaluation/research-gates.json"

EXPECTED_BASE = "d1fc8053e1459a7829f6f24b8d187f7887375cf0"
EXPECTED_SPEC_SHA256 = "2b6ede05f7d5e3525070e1a5893ea599613a64eb114b12ed43606fb114e14128"
EXPECTED_PUBLIC_SHA256 = {
    "README": "248598257d4f1ac23f4156a209fc6088439abdfd5d9f7bb6bb90638ac149b35f",
    "Charter": "6252fbef6c49886f6c8516ebc8f23237b7d2908bdca10230789174daad7c3b53",
    "Report": "426b48e0b1a8724bd718bb3ffb5491f2f97b79860c90f4d1f57c35d78434c991",
}
EXPECTED_EMPIRICAL_BLOBS = {
    "scope-and-universality-charter-v1.1.md": "a4f7074c10c92863fc5a37edfd65aa3178b71dba",
    "audit-manifest-v1.0.json": "bda494ad389f31cb88306adcdf3401ca816ef350",
    "chat-audit-2026-08-05.md": "85ca5089824962ddee5e43b7ef0abb46d602c981",
}
PUBLIC_NONCLAIMS = [
    "No weakest invariant-supporting structure has been proved.",
    "No first invariant-supporting structure has been proved.",
    "No minimal invariant-supporting structure has been proved.",
    "No globally optimal invariant-supporting structure has been proved.",
    "Small categories are not claimed to be broader than bare sets under a common comparison order.",
    "No complete architecture of reasoning is established.",
    "RCCD is not derived.",
    "The empirical clean-room program has not been executed.",
    "Accepted Project FAR theory is unchanged.",
    "This derivation is exploratory and is not a registered theorem.",
]
EXPECTED_SPEC = {
    "id": "TCD-COMPOSITIONAL-INVARIANT-001",
    "version": "1.0",
    "status": "Research",
    "base_commit": "d1fc8053e1459a7829f6f24b8d187f7887375cf0",
    "question": "Within an independently stated typed-compositional scope, which finitary arrow-valued operations are invariant under every admissible recoding, without assuming RCCD components?",
    "broadness_policy": {
        "absolute_maximum_claimed": False,
        "reason": "Broadest is undefined until a comparison order and admissible recodings are fixed.",
        "selected_scope": "all small categories",
        "scope_criterion": "A system is included exactly when it supplies the set-sized category data and laws in TC1-TC4.",
        "recodings": "all functors",
    },
    "axioms": [
        {"id": "TC1", "statement": "Objects and arrows are sets, with total source and target functions from arrows to objects."},
        {"id": "TC2", "statement": "A total designated identity assignment maps every object X to one arrow id_X:X->X."},
        {"id": "TC3", "statement": "A single-valued composition operation is defined exactly on composable ordered pairs (f,g) with target(f)=source(g), and returns g∘f with source(g∘f)=source(f) and target(g∘f)=target(g)."},
        {"id": "TC4", "statement": "For every well-typed arrow and composable triple, identities are two-sided units and composition is associative."},
    ],
    "input_operation_schema": {
        "input": "a finite directed graph G with distinguished vertices s and t",
        "presentation": "a graph map x:G->U(C) into the underlying graph of a small category C",
        "output": "an arrow alpha_C(x):x(s)->x(t)",
        "invariance": "for every functor H:C->D, H(alpha_C(x))=alpha_D(H composed with x)",
    },
    "theorem_claims": [
        {"id": "TCD-CI-T1", "statement": "TC1-TC4 specify exactly a small category, and structure-preserving recodings are exactly functors.", "status": "exploratory_unregistered_argument"},
        {"id": "TCD-CI-T2", "statement": "Every finitary arrow-valued operation invariant under all functors is evaluation of one unique fixed path in the free category on its input graph; conversely every fixed path defines such an invariant operation.", "status": "exploratory_unregistered_argument"},
        {"id": "TCD-CI-C1", "statement": "For an input graph with a composable chain from s to t, sequential composition can supply a nonidentity invariant path such as b∘a. Identity paths remain structural path terms only when s=t and are not classified as nontrivial.", "status": "exploratory_consequence"},
        {"id": "TCD-CI-C2", "statement": "No RCCD-specific generator, operator, observation, objective, decomposition, or policy follows from typed composition alone.", "status": "exploratory_consequence"},
    ],
    "fixture": {
        "objects": ["A", "B", "C"],
        "generators": [
            {"name": "a", "source": "A", "target": "B"},
            {"name": "b", "source": "B", "target": "C"},
            {"name": "c", "source": "A", "target": "C"},
        ],
        "distinguished_source": "A",
        "distinguished_target": "C",
        "expected_paths_from_source_to_target": ["c", "b∘a"],
        "expected_new_nonidentity_paths_after_free_completion": ["b∘a"],
        "identity_is_nontrivial_for_distinguished_shape": False,
    },
    "disposition": {
        "classification": "exploratory_unregistered_derivation",
        "scope_status": "exploratory_candidate_within_declared_small_category_scope",
        "release_status": "not_eligible_unregistered_deductive_program",
        "empirical_program_status": "not_executed",
        "rccd_status": "not_derived",
        "accepted_theory_change": False,
        "strongest_internal_claim": "Exploratory candidate argument: under TC1-TC4, functor-invariant finitary arrow-valued operations for a fixed finite input graph appear to be evaluations of unique path terms generated by identities and typed sequential composition.",
        "next_release_condition": "Before any theorem claim or execution, register a new prospective deductive program with independently frozen definitions, explicit terminal outcomes, a finite stopping rule, and a claim-impact policy; theorem release would additionally require all controlling release gates.",
    },
    "nonclaims": PUBLIC_NONCLAIMS,
}


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


def _read_utf8(path: Path) -> tuple[bytes, str]:
    if path.is_symlink() or not path.is_file():
        raise VerificationError(f"required artifact must be a regular non-symlink file: {path}")
    try:
        raw = path.read_bytes()
    except OSError as exc:
        raise VerificationError(f"required artifact missing or unreadable: {path}") from exc
    if raw.startswith(b"\xef\xbb\xbf"):
        raise VerificationError(f"UTF-8 BOM rejected: {path}")
    try:
        return raw, raw.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise VerificationError(f"invalid UTF-8 in {path}") from exc


def load_json(path: Path) -> dict[str, Any]:
    raw, text = _read_utf8(path)
    try:
        value = json.loads(text, object_pairs_hook=_no_duplicate_keys, parse_constant=_reject_constant)
    except json.JSONDecodeError as exc:
        raise VerificationError(f"invalid JSON in {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise VerificationError(f"top-level JSON object required: {path}")
    return value


def canonical_json(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")


def _git_blob_sha1(raw: bytes) -> str:
    return hashlib.sha1(f"blob {len(raw)}\0".encode("ascii") + raw).hexdigest()


def validate_spec(spec: dict[str, Any]) -> None:
    if spec != EXPECTED_SPEC:
        raise VerificationError("frozen specification or claim boundary drifted")
    base = spec.get("base_commit")
    if not isinstance(base, str) or re.fullmatch(r"[0-9a-f]{40}", base) is None or base != EXPECTED_BASE:
        raise VerificationError("base_commit does not match the frozen lowercase hexadecimal repository base")
    if hashlib.sha256(canonical_json(spec)).hexdigest() != EXPECTED_SPEC_SHA256:
        raise VerificationError("canonical specification digest drifted")
    statuses = {item["status"] for item in spec["theorem_claims"]}
    if any("proved" in status or "established" in status for status in statuses):
        raise VerificationError("unregistered derivation cannot carry proved or established theorem status")
    disposition = spec["disposition"]
    if disposition["classification"] != "exploratory_unregistered_derivation":
        raise VerificationError("unregistered derivation must remain exploratory")
    if disposition["release_status"] != "not_eligible_unregistered_deductive_program":
        raise VerificationError("unregistered derivation cannot be release-eligible")
    if disposition["accepted_theory_change"] is not False:
        raise VerificationError("exploratory derivation cannot change accepted theory")


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
            if target(first) != second[0]: continue
            for third in arrows:
                if target(second) != third[0]: continue
                if compose(compose(first, second), third) != compose(first, compose(second, third)):
                    raise VerificationError("associativity failed")
                associativity_checks += 1
    distinguished = [_render(path) for path in arrows if path[0] == "A" and target(path) == "C"]
    if distinguished != ["c", "b∘a"]: raise VerificationError("distinguished path set drifted")
    if any(path.startswith("id_") for path in distinguished): raise VerificationError("identity cannot inhabit the distinct-endpoint A->C operation shape")
    composite = compose(("A", ("a",)), ("B", ("b",)))
    if _render(composite) != "b∘a": raise VerificationError("nontrivial composite witness changed")
    nonidentity = {_render(path) for path in arrows if path[1]}
    new_paths = sorted(nonidentity - set(generators))
    if new_paths != ["b∘a"]: raise VerificationError("free-completion witness set drifted")
    words = {"a": "x", "b": "yz", "c": "q"}
    word = "".join(words[edge] for edge in composite[1])
    if word != "xyz": raise VerificationError("functorial recoding witness failed")
    evidence = {"fixture_object_count":3,"fixture_generator_count":3,"free_category_arrow_count":len(arrows),"free_category_nonidentity_arrow_count":len(nonidentity),"new_nonidentity_paths":new_paths,"distinguished_paths":distinguished,"nontrivial_invariant_witness":"b∘a","identity_is_nontrivial_witness":False,"identity_is_admissible_for_distinguished_A_to_C_shape":False,"identity_law_checks":identity_checks,"associativity_checks":associativity_checks,"word_functor_composite":word,"path_classification_argument":"Evaluation on the identity presentation in the free category selects one path; naturality forces every other value to be its image."}
    result = {"id":EXPECTED_SPEC["id"],"version":EXPECTED_SPEC["version"],"status":"Research",**EXPECTED_SPEC["disposition"],"theorem_status":"not_established_exploratory_argument_with_bounded_executable_corroboration","evidence":evidence,"nonclaims":PUBLIC_NONCLAIMS}
    result["evidence_sha256"] = hashlib.sha256(canonical_json(evidence)).hexdigest()
    return result


def validate_public_surface(name: str, path: Path) -> None:
    raw, text = _read_utf8(path)
    if hashlib.sha256(raw).hexdigest() != EXPECTED_PUBLIC_SHA256[name]: raise VerificationError(f"{name} public claim surface drifted")
    for line in PUBLIC_NONCLAIMS:
        if text.count(line) != 1: raise VerificationError(f"{name} must preserve each public nonclaim exactly once: {line}")
    forbidden = ("proved theorem", "theorem established", "question is closed", "scoped theorem")
    lowered = text.lower()
    if any(term in lowered for term in forbidden): raise VerificationError(f"{name} overstates the exploratory derivation")
    if name == "README":
        empirical_artifacts = ("audit-manifest-v1.0.json","chat-audit-2026-08-05.md","scope-and-universality-charter-v1.1.md","clean-room-derivation-protocol-v1.2.md","sampling-design-v1.1.md","covering-array-v1.0.csv","pairwise-coverage-report-v1.0.csv","restricted-artifacts-policy.md","protocol-amendment-001.md","verify_sampling_design.py")
        if any(text.count(item) != 1 for item in empirical_artifacts): raise VerificationError("README must preserve complete empirical-track navigation")
    if name == "Charter":
        required_authority = ("does not supersede, amend, or control the registered empirical clean-room program","scope-and-universality-charter-v1.1.md","remains controlling for `TCD-CLEANROOM-001` empirical execution","this v1.2 document adds no empirical authority")
        if any(fragment not in text for fragment in required_authority): raise VerificationError("Charter must preserve the empirical/compositional authority boundary")


def validate_empirical_authority(charter_path: Path, manifest_path: Path, audit_path: Path = DEFAULT_CHAT_AUDIT) -> None:
    for path, label in ((charter_path,"controlling empirical charter"),(manifest_path,"registered empirical manifest"),(audit_path,"registered chat audit")):
        raw, _ = _read_utf8(path)
        expected = EXPECTED_EMPIRICAL_BLOBS.get(path.name)
        if expected is None or _git_blob_sha1(raw) != expected: raise VerificationError(f"{label} identity drifted")
    manifest = load_json(manifest_path)
    if manifest.get("program_id") != "TCD-CLEANROOM-001" or manifest.get("decision") != "research_program_registered_execution_not_authorized": raise VerificationError("registered empirical program disposition drifted")
    execution_gate = manifest.get("execution_gate")
    if not isinstance(execution_gate, dict) or execution_gate.get("authorized") is not False: raise VerificationError("empirical execution gate must remain closed")
    blockers = execution_gate.get("blockers")
    if not isinstance(blockers, list) or not blockers or any(type(item) is not str or not item for item in blockers): raise VerificationError("empirical execution blockers must remain explicit")
    committed = manifest.get("committed_artifacts")
    if not isinstance(committed, list) or not committed: raise VerificationError("registered empirical artifact ledger missing")
    seen_paths: set[str] = set(); ledger: dict[str, str] = {}
    for item in committed:
        if not isinstance(item, dict) or set(item) != {"path","git_blob_sha1"}: raise VerificationError("empirical artifact ledger entries require exact path/blob fields")
        rel = item.get("path"); expected_blob = item.get("git_blob_sha1")
        if not isinstance(rel, str) or not rel or rel.startswith("/") or ".." in Path(rel).parts: raise VerificationError("unsafe empirical artifact ledger path")
        if rel in seen_paths: raise VerificationError("duplicate empirical artifact ledger path")
        if not isinstance(expected_blob, str) or re.fullmatch(r"[0-9a-f]{40}", expected_blob) is None: raise VerificationError("invalid empirical artifact blob identity")
        seen_paths.add(rel); ledger[rel] = expected_blob
        raw, _ = _read_utf8(ROOT / rel)
        if _git_blob_sha1(raw) != expected_blob: raise VerificationError(f"registered empirical artifact identity drifted: {rel}")
    expected_charter_path = "research/target-category-discovery/scope-and-universality-charter-v1.1.md"
    expected_audit_path = "research/target-category-discovery/chat-audit-2026-08-05.md"
    if ledger.get(expected_charter_path) != EXPECTED_EMPIRICAL_BLOBS["scope-and-universality-charter-v1.1.md"]: raise VerificationError("empirical manifest no longer registers the controlling charter identity")
    if ledger.get(expected_audit_path) != EXPECTED_EMPIRICAL_BLOBS["chat-audit-2026-08-05.md"]: raise VerificationError("empirical manifest no longer registers the chat-audit identity")


def validate_gate(gates_path: Path) -> None:
    gates = load_json(gates_path); entries = gates.get("gates")
    if not isinstance(entries, list): raise VerificationError("research gate registry missing gates list")
    rg07 = [item for item in entries if isinstance(item, dict) and item.get("id") == "RG-07"]
    if len(rg07) != 1: raise VerificationError("exactly one RG-07 gate required")
    gate = rg07[0]
    if gate.get("name") != "nonclaim-audit" or gate.get("status") != "not_satisfied" or gate.get("evidence") != []: raise VerificationError("RG-07 state changed; this exploratory artifact requires a new reviewed version")
    required = gate.get("required_before")
    if required != ["evidence_release", "theorem_release"]: raise VerificationError("RG-07 must remain required before evidence_release and theorem_release exactly")


def verify(spec_path: Path = DEFAULT_SPEC, result_path: Path = DEFAULT_RESULT, report_path: Path = DEFAULT_REPORT, readme_path: Path = DEFAULT_README, charter_path: Path = DEFAULT_CHARTER, gates_path: Path = DEFAULT_GATES, empirical_charter_path: Path = DEFAULT_EMPIRICAL_CHARTER, empirical_manifest_path: Path = DEFAULT_EMPIRICAL_MANIFEST, audit_path: Path = DEFAULT_CHAT_AUDIT) -> dict[str, Any]:
    validate_empirical_authority(empirical_charter_path, empirical_manifest_path, audit_path)
    validate_gate(gates_path)
    actual = build_result(load_json(spec_path))
    if actual != load_json(result_path): raise VerificationError("committed result does not match a fresh rebuild")
    validate_public_surface("README", readme_path); validate_public_surface("Charter", charter_path); validate_public_surface("Report", report_path)
    if actual["classification"] != "exploratory_unregistered_derivation": raise VerificationError("classification must remain exploratory")
    if actual["release_status"] != "not_eligible_unregistered_deductive_program": raise VerificationError("unregistered derivation cannot be release-eligible")
    return actual


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--spec", type=Path, default=DEFAULT_SPEC); parser.add_argument("--result", type=Path, default=DEFAULT_RESULT); parser.add_argument("--report", type=Path, default=DEFAULT_REPORT); parser.add_argument("--readme", type=Path, default=DEFAULT_README); parser.add_argument("--charter", type=Path, default=DEFAULT_CHARTER); parser.add_argument("--empirical-charter", type=Path, default=DEFAULT_EMPIRICAL_CHARTER); parser.add_argument("--empirical-manifest", type=Path, default=DEFAULT_EMPIRICAL_MANIFEST); parser.add_argument("--chat-audit", type=Path, default=DEFAULT_CHAT_AUDIT); parser.add_argument("--gates", type=Path, default=DEFAULT_GATES)
    args = parser.parse_args()
    try: result = verify(args.spec,args.result,args.report,args.readme,args.charter,args.gates,args.empirical_charter,args.empirical_manifest,args.chat_audit)
    except VerificationError as exc:
        print(f"FAIL: {exc}"); return 1
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True)); return 0


if __name__ == "__main__":
    raise SystemExit(main())
