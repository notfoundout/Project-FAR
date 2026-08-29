#!/usr/bin/env python3
"""Validate governed research registries and generate deterministic human/graph views."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import jsonschema  # noqa: E402

DATA_SCHEMAS = {
    "research/registry/opportunities-v1.0.json": "schemas/far-opportunity-registry-v1.schema.json",
    "research/registry/research-questions-v1.0.json": "schemas/far-research-question-registry-v1.schema.json",
    "research/registry/citation-links-v1.0.json": "schemas/far-citation-registry-v1.schema.json",
    "research/registry/research-tools-v1.0.json": "schemas/far-research-tool-registry-v1.schema.json",
    "research/registry/epistemic-threats-v1.0.json": "schemas/far-epistemic-threat-registry-v1.schema.json",
    "theory/evaluation/far-core-assurance-v1.0.json": "schemas/far-assurance-ledger-v1.schema.json",
    "theory/evaluation/far-core-formalization-ledger-v1.0.json": "schemas/far-core-formalization-ledger-v1.schema.json",
    "research/campaigns/pca-w1-replay-capsule-v1.0.json": "schemas/far-research-campaign-v1.schema.json",
}

GENERATED = {
    "docs/planning/opportunity-registry.md": "opportunities",
    "docs/research/research-question-registry.md": "questions",
    "docs/assurance/far-core-assurance.md": "assurance",
    "artifacts/knowledge-graph/project-far-knowledge-graph.json": "graph",
}

REQUIRED_THREATS = {
    "universal sufficiency confused with universal minimality",
    "Gamma frame residue confused with exact common theory",
    "preference orientation silently assumed in Pareto reasoning",
    "finite-panel result universalized",
    "encoding confused with structure",
    "Unknown confused with absence",
    "decoder power silently strengthened",
    "historical provenance status confused with truth status",
    "contract silently changed",
    "scope qualifier dropped",
    "prior-art absence mistaken for novelty",
    "model agreement mistaken for proof",
}

REQUIRED_TOOLS = {
    "GitHub", "Lean", "Wolfram", "Consensus", "SciSpace", "Scite", "Zotero",
    "Acumen/Talarion", "Ordinary web research", "GPT/OpenAI models",
    "Claude or other external reasoners", "Notion", "Linear", "Base44", "Floot",
    "OpenAI Agents SDK", "ChatGPT Apps/MCP",
}

PROMOTED_W1_PATHS = {
    "docs/research/pca-w1-independent-review-protocol-v1.0.md",
    "docs/research/pca-w1-independent-review/00-exposure-environment.md",
    "docs/research/pca-w1-independent-review/01-stage-a-blind-reconstruction.md",
    "docs/research/pca-w1-independent-review/tools/stage_a_finite_checks.py",
    "docs/research/pca-w1-independent-review/tools/stage-a-finite-check-output.md",
    "docs/research/pca-w1-independent-review/02-stage-b-ledger-reconciliation.md",
    "docs/research/pca-w1-independent-review/03-stage-c-independent-research.md",
    "docs/research/pca-w1-independent-review/04-stage-c-hostile-test-ledger.md",
    "docs/research/pca-w1-independent-review/05-stage-d-provisional-verdict-frozen.md",
    "docs/research/pca-w1-independent-review/05-stage-d-freeze-manifest.json",
    "docs/research/pca-w1-independent-review/tools/stage_e_sss_checks.py",
    "docs/research/pca-w1-independent-review/tools/stage-e-sss-check-output.json",
    "docs/research/pca-w1-independent-review/06-stage-e-controlled-unblinding.md",
    "docs/research/pca-w1-independent-review/07-final-independent-review.md",
    "docs/research/pca-w1-independent-review/07-final-independent-review.json",
    "docs/research/pca-w1-independent-review/08-review-artifact-manifest.json",
}
# Independent trust root for the 16 byte-promoted W1 artifacts.
# These values are not derived from the mutable promotion JSON at validation time.
W1_PROMOTED_ARTIFACT_SHA256 = {'docs/research/pca-w1-independent-review-protocol-v1.0.md': '2decf1bcc924101928432143535712bd6fccc4723947d97321fee2d14adea0dc', 'docs/research/pca-w1-independent-review/00-exposure-environment.md': 'f9edff7c8385d49064c1ea92a529bbb5d4f32e38a667531687bc123057c7a73d', 'docs/research/pca-w1-independent-review/01-stage-a-blind-reconstruction.md': 'bbc33980d8b5f68d6c3c9d89857cf5706561b0679781fff9f487aa80654c5662', 'docs/research/pca-w1-independent-review/tools/stage_a_finite_checks.py': 'b5c912eaacb766faecec61a60c997cacb53c5f01741952018e1513a29eafa137', 'docs/research/pca-w1-independent-review/tools/stage-a-finite-check-output.md': '342204f48178c68160f5f700d43ab5cafd6ff5fde327a025129983f368b8832b', 'docs/research/pca-w1-independent-review/02-stage-b-ledger-reconciliation.md': '623838d5ff4daded5a35539ecf558264e70ad10fcf4428165c1ceb46cf55ecd7', 'docs/research/pca-w1-independent-review/03-stage-c-independent-research.md': '413e9f9ac2cacc116188dad511fb0726a952bc15f83b1f44dd88c343057fc9db', 'docs/research/pca-w1-independent-review/04-stage-c-hostile-test-ledger.md': 'bceb586e71800375935902ad5653e8d02d1211de24b13eed572d85228fc9dbd5', 'docs/research/pca-w1-independent-review/05-stage-d-provisional-verdict-frozen.md': 'e27c99c7ff52f5f95e30e6f163b83cacbfa389d61d6f9408966bf983ce66902e', 'docs/research/pca-w1-independent-review/05-stage-d-freeze-manifest.json': 'f48b05d997f1e1ae946072c217265f744bc3131b937118ae0e62fc518cfb3e5c', 'docs/research/pca-w1-independent-review/tools/stage_e_sss_checks.py': '746fa76d097e747bdb1ee3a4742401b0a4a01ffd81fa176148b00d926ca5292e', 'docs/research/pca-w1-independent-review/tools/stage-e-sss-check-output.json': 'a17d5b7549a3b66c1ae450a6fb5a6d2cbe000202a6196cd1247310930354498b', 'docs/research/pca-w1-independent-review/06-stage-e-controlled-unblinding.md': '787229856619ce47fc71107550d5afc2940558d0e1443281ecc008bee0c370b6', 'docs/research/pca-w1-independent-review/07-final-independent-review.md': '03848362e0cbea1151ba3a0e042cf2872f51f0781815eaff17c1128e49589aaa', 'docs/research/pca-w1-independent-review/07-final-independent-review.json': 'f311552b877beece5245f48bbf1cf32f68d4b586fb3d65c18410b0ffe9175c37', 'docs/research/pca-w1-independent-review/08-review-artifact-manifest.json': '1437aeb6c52e7d84958b2cc530a9c5bda71706b96386482b98867df3c4e5d1bc'}

W1_REVIEW_TARGET = {
    "commit": "14105775daf3c5713b134a728db2e1e53673af97",
    "tree": "68f058199b7c94b707fd5fe978f1ef59d695ab00",
    "theory_id": "PROJECT-FAR-CORE-THEORY-1.1",
    "theory_sha256": "91513dce21273364ef8ad24ebd1102e3b5957b513bbd5bc429f2b10917fa8239",
    "ledger_sha256": "66372644e5a2fe65c93f7e893e41eae74211934f92827cadcfe28dd81290ab40",
}
W1_REVIEW_BRANCH = {
    "name": "research/pca-w1-core-v1.1-independent-review",
    "head": "0981697546eba68651bddcd22e67ccdeb98decf4",
    "tree": "3b58ca873c210b62c5ce01f572cb1314b55d95d2",
}
W1_REVIEWED_LEDGER_CONTRACT = {
    "source_path": "theory/terminal/project-far-core-theory-v1.1.json",
    "target_whole_file_sha256": W1_REVIEW_TARGET["ledger_sha256"],
    "canonicalization": "json_sorted_keys_utf8_compact",
    "excluded_post_review_metadata_fields": [
        "assurance",
        "independent_review_status",
        "next_workstream",
    ],
    "reviewed_projection_sha256": "ee852f8ceb968861ebdee48d1b3f6ec85771751b9dd3f80abbde8cef96860ca1",
    "permitted_current_metadata_values": {
        "assurance": (
            "internal_deductive_corrected_then_independently_reviewed_"
            "exact_scopes_w2_complete_novelty_not_established"
        ),
        "independent_review_status": (
            "complete_confirmed_14_proved_exact_scopes_novelty_not_established"
        ),
        "next_workstream": "PCA-W3-CONTRACT-SCHEMA",
    },
}
GRAPH_ADDITIONAL_SOURCES = {
    "theory/terminal/project-far-core-theory-v1.1.json",
    "docs/research/pca-w1-independent-review/07-final-independent-review.json",
    "theory/evaluation/pca-w1-independent-review-promotion-v1.0.json",
}


def load(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _unique(items: Iterable[dict], field: str, label: str, errors: list[str]) -> None:
    values = [item[field] for item in items]
    if len(values) != len(set(values)):
        errors.append(f"duplicate {label} {field}")


def validate_schemas(data: dict[str, dict]) -> list[str]:
    errors: list[str] = []
    for data_path, schema_path in DATA_SCHEMAS.items():
        for exc in jsonschema.Draft202012Validator(load(schema_path)).iter_errors(data[data_path]):
            where = "/".join(str(part) for part in getattr(exc, "absolute_path", exc.path))
            errors.append(f"{data_path}:{where}: {exc.message}")
    return errors


def parse_bib_keys(path: Path) -> list[str]:
    return re.findall(r"(?m)^@[A-Za-z]+\{([^,\s]+),", path.read_text(encoding="utf-8"))


def w1_seal_errors(promotion: dict, root: Path = ROOT) -> list[str]:
    """Require exact SHA-256 coverage of every W1 object promoted into current state."""
    errors: list[str] = []
    artifacts = promotion.get("verified_artifacts")
    if not isinstance(artifacts, list):
        return ["W1 promotion verified_artifacts must be a list"]
    paths = [item.get("path") for item in artifacts if isinstance(item, dict)]
    if len(paths) != len(artifacts) or len(paths) != len(set(paths)):
        errors.append("W1 promotion seal has malformed or duplicate artifact paths")
    actual = {path for path in paths if isinstance(path, str)}
    missing = sorted(PROMOTED_W1_PATHS - actual)
    unexpected = sorted(actual - PROMOTED_W1_PATHS)
    if missing or unexpected:
        errors.append(f"W1 promotion seal coverage drift: missing={missing} unexpected={unexpected}")
    target = promotion.get("review_target")
    if target != W1_REVIEW_TARGET:
        errors.append("W1 promotion review target identity/hash contract drifted")
    branch = promotion.get("review_branch")
    if branch != W1_REVIEW_BRANCH:
        errors.append("W1 promotion sealed review branch identity drifted")
    ledger_contract = promotion.get("reviewed_ledger_contract")
    if ledger_contract != W1_REVIEWED_LEDGER_CONTRACT:
        errors.append("W1 reviewed ledger contract drifted")
    else:
        ledger_path = root / ledger_contract["source_path"]
        try:
            current_ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            errors.append(f"current W1-reviewed ledger unavailable: {exc}")
        else:
            excluded = ledger_contract["excluded_post_review_metadata_fields"]
            if not all(field in current_ledger for field in excluded):
                errors.append("current W1-reviewed ledger is missing permitted metadata fields")
            projection = {
                key: value for key, value in current_ledger.items() if key not in excluded
            }
            projection_sha256 = hashlib.sha256(
                canonical_json(projection).encode("utf-8")
            ).hexdigest()
            if projection_sha256 != ledger_contract["reviewed_projection_sha256"]:
                errors.append(
                    "current theorem-bearing W1 ledger projection differs from reviewed target"
                )
            current_metadata = {
                field: current_ledger.get(field) for field in excluded
            }
            if current_metadata != ledger_contract["permitted_current_metadata_values"]:
                errors.append("current W1 ledger metadata exceeds the permitted promotion changes")
    try:
        terminal = json.loads(
            (root / "docs/research/pca-w1-independent-review/07-final-independent-review.json")
            .read_text(encoding="utf-8")
        )
        capsule = json.loads(
            (root / "research/campaigns/pca-w1-replay-capsule-v1.0.json")
            .read_text(encoding="utf-8")
        )
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"W1 target binding source unavailable: {exc}")
    else:
        terminal_target = terminal.get("target", {})
        terminal_projection = {
            "commit": terminal_target.get("commit"),
            "tree": terminal_target.get("tree"),
            "theory_id": terminal_target.get("theory_id"),
            "theory_sha256": terminal_target.get("monograph_sha256"),
            "ledger_sha256": terminal_target.get("ledger_sha256"),
        }
        capsule_target = capsule.get("target", {})
        capsule_hashes = capsule_target.get("hashes", {})
        capsule_projection = {
            "commit": capsule_target.get("commit"),
            "tree": capsule_target.get("tree"),
            "theory_id": (
                capsule_target.get("theory_or_question", "").split(" / ", 1)[0]
            ),
            "theory_sha256": capsule_hashes.get("theory"),
            "ledger_sha256": capsule_hashes.get("ledger"),
        }
        source_hashes = {
            item.get("path"): item.get("sha256")
            for item in capsule.get("source_manifest", [])
            if isinstance(item, dict)
        }
        if terminal_projection != W1_REVIEW_TARGET:
            errors.append("sealed terminal W1 target identity/hash contract drifted")
        if capsule_projection != W1_REVIEW_TARGET:
            errors.append("W1 replay capsule target identity/hash contract drifted")
        if target != terminal_projection or target != capsule_projection:
            errors.append("W1 promotion target is not cross-bound to sealed review/capsule target")
        if source_hashes.get("theory/theorems/Project-FAR-Theory-Closure-v1.1.md") != target.get("theory_sha256"):
            errors.append("W1 target theory hash is not bound to capsule source manifest")
        if source_hashes.get("theory/terminal/project-far-core-theory-v1.1.json") != target.get("ledger_sha256"):
            errors.append("W1 target ledger hash is not bound to capsule source manifest")
    governing_theory = root / "theory/theorems/Project-FAR-Theory-Closure-v1.1.md"
    if not governing_theory.is_file() or sha256(governing_theory) != W1_REVIEW_TARGET["theory_sha256"]:
        errors.append("current governing v1.1 theory bytes differ from the W1-reviewed target")
    if set(W1_PROMOTED_ARTIFACT_SHA256) != PROMOTED_W1_PATHS:
        errors.append("independent W1 artifact seal coverage drift")
    reported_hashes = {
        item.get("path"): item.get("sha256")
        for item in artifacts
        if isinstance(item, dict) and isinstance(item.get("path"), str)
    }
    for raw_path, expected in W1_PROMOTED_ARTIFACT_SHA256.items():
        if reported_hashes.get(raw_path) != expected:
            errors.append(f"W1 promotion artifact hash contract drift: {raw_path}")
            errors.append(f"W1 sealed artifact missing or changed: {raw_path}")
        path = root / raw_path
        if not path.is_file() or sha256(path) != expected:
            errors.append(f"W1 sealed artifact missing or changed: {raw_path}")
    return sorted(set(errors))


def semantic_errors(data: dict[str, dict]) -> list[str]:
    errors: list[str] = []
    opportunities = data["research/registry/opportunities-v1.0.json"]["opportunities"]
    questions = data["research/registry/research-questions-v1.0.json"]["questions"]
    citations = data["research/registry/citation-links-v1.0.json"]
    tools = data["research/registry/research-tools-v1.0.json"]["tools"]
    threats = data["research/registry/epistemic-threats-v1.0.json"]["threats"]
    assurance = data["theory/evaluation/far-core-assurance-v1.0.json"]["claims"]
    formalization = data["theory/evaluation/far-core-formalization-ledger-v1.0.json"]["claims"]
    _unique(opportunities, "id", "opportunity", errors)
    _unique(questions, "id", "question", errors)
    _unique(citations["sources"], "citation_key", "source", errors)
    _unique(citations["relationships"], "id", "citation relationship", errors)
    _unique(tools, "id", "tool", errors)
    _unique(threats, "id", "threat", errors)
    _unique(assurance, "id", "assurance claim", errors)
    _unique(formalization, "id", "formalization claim", errors)

    opportunity_ids = {item["id"] for item in opportunities}
    for item in opportunities:
        for dependency in item["implementation_dependencies"] + item["theoretical_dependencies"]:
            if dependency.startswith("OPP-") and dependency not in opportunity_ids:
                errors.append(f"{item['id']}: unknown opportunity dependency {dependency}")
        if item["status"] in {"SUPERSEDED", "REJECTED"} and item["priority"] != "prohibited":
            errors.append(f"{item['id']}: superseded/rejected opportunity is not prohibited")
        if item["priority"] == "prohibited" and item["status"] not in {"SUPERSEDED", "REJECTED"}:
            errors.append(f"{item['id']}: active planning status has prohibited priority")

    if {item["name"] for item in threats} != REQUIRED_THREATS:
        errors.append("epistemic threat set differs from the required permanent regression library")
    if {item["name"] for item in tools} != REQUIRED_TOOLS:
        errors.append("research tool authority set is incomplete or contains an ungoverned tool")

    source_keys = {item["citation_key"] for item in citations["sources"]}
    bib_keys = parse_bib_keys(ROOT / citations["bibliography"])
    if len(bib_keys) != len(set(bib_keys)):
        errors.append("duplicate BibTeX citation key")
    if set(bib_keys) != source_keys:
        errors.append(f"BibTeX/source registry drift: bib-only={sorted(set(bib_keys)-source_keys)} registry-only={sorted(source_keys-set(bib_keys))}")
    claim_ids = {f"FAR-CORE-{index:03d}" for index in range(1, 15)} | {"NOVELTY-CORE-MATHEMATICS"}
    for relation in citations["relationships"]:
        if relation["citation_key"] not in source_keys:
            errors.append(f"{relation['id']}: unknown citation key")
        if relation["claim_id"] not in claim_ids:
            errors.append(f"{relation['id']}: unknown claim target {relation['claim_id']}")
        artifact = relation["research_artifact"].split("#", 1)[0]
        if not (ROOT / artifact).is_file():
            errors.append(f"{relation['id']}: missing research artifact {artifact}")

    core = load("theory/terminal/project-far-core-theory-v1.1.json")
    core_by_id = {item["id"]: item for item in core["claims"]}
    review = load("docs/research/pca-w1-independent-review/07-final-independent-review.json")
    review_by_id = {item["id"]: item for item in review["claims"]}
    formalization_by_id = {item["id"]: item for item in formalization}
    expected_ids = [f"FAR-CORE-{index:03d}" for index in range(1, 15)]
    if [item["id"] for item in assurance] != expected_ids:
        errors.append("assurance ledger claim order/coverage must be FAR-CORE-001 through 014")
    for item in assurance:
        identifier = item["id"]
        if identifier not in core_by_id or identifier not in review_by_id:
            errors.append(f"{identifier}: missing core or W1 source")
            continue
        if item["exact_statement"] != core_by_id[identifier]["claim"]:
            errors.append(f"{identifier}: exact assurance statement drifted from governing ledger")
        if item["truth_disposition"] != review_by_id[identifier]["verdict"]:
            errors.append(f"{identifier}: truth disposition drifted from W1 terminal review")
        if item["scope"] != review_by_id[identifier]["scope"]:
            errors.append(f"{identifier}: assurance scope drifted from W1 terminal review")
        if (
            item["governing_ledger_provenance_status"]
            != core_by_id[identifier]["status"]
        ):
            errors.append(
                f"{identifier}: governing-ledger provenance status drifted from core ledger"
            )
        if item["version"] != core["theory_id"]:
            errors.append(f"{identifier}: version drift")
        formal = formalization_by_id.get(identifier)
        if formal is None:
            errors.append(f"{identifier}: missing formalization ledger entry")
            continue
        if formal["canonical_prose_statement"] != item["exact_statement"]:
            errors.append(f"{identifier}: formalization prose drifted from governing statement")
        if formal["lean_declarations"] != item["lean_declarations"]:
            errors.append(f"{identifier}: assurance/formalization Lean declaration drift")
        if formal["formalization_status"].replace("/", "_") != item["formalization_status"]:
            errors.append(f"{identifier}: assurance/formalization outcome drift")
        if formal["kernel_check"] != "PASS":
            errors.append(f"{identifier}: formalization has not passed the pinned Lean kernel")
    if core_by_id["FAR-CORE-014"]["status"] != "supported_derived":
        errors.append("FAR-CORE-014 provenance label was overwritten")
    if next(item for item in assurance if item["id"] == "FAR-CORE-014")["truth_disposition"] != "PROVED":
        errors.append("FAR-CORE-014 W1 truth verdict was lost")
    if review["final"]["claim_counts"] != {"PROVED":14,"REFUTED":0,"OPEN":0,"UNDERDETERMINED":0,"NOT APPLICABLE":0}:
        errors.append("W1 terminal count drift")
    promotion = load("theory/evaluation/pca-w1-independent-review-promotion-v1.0.json")
    errors.extend(w1_seal_errors(promotion))
    return sorted(set(errors))


def render_opportunities(data: dict) -> str:
    rows = []
    for item in data["opportunities"]:
        rows.append(f"| `{item['id']}` | {item['name']} | `{item['status']}` | {item['priority']} | `{item['target_workstream']}` | {item['disposition']} |")
    return """# Project FAR Opportunity Registry

Status: **Generated canonical planning view; not theory authority**

Source: [`research/registry/opportunities-v1.0.json`](../../research/registry/opportunities-v1.0.json).

The registry captures useful ideas, dependencies, risks, falsifiers, commercial hypotheses,
and permanent rejected/superseded directions. `canonical` means governed planning record, not
mathematical authority. Edit the JSON and regenerate this view.

| ID | Opportunity | Status | Priority | Workstream | Disposition |
|---|---|---|---|---|---|
""" + "\n".join(rows) + "\n"


def render_questions(data: dict) -> str:
    sections = []
    for item in data["questions"]:
        sections.extend([
            f"## {item['id']}: {item['exact_question']}", "",
            f"- Legacy/register links: {', '.join(f'`{value}`' for value in item['legacy_ids'])}",
            f"- Disposition: `{item['current_disposition']}`", f"- Scope: {item['governing_scope']}",
            f"- Why it matters: {item['why_it_matters']}", f"- Resolution/falsifier: {item['falsifier_resolution_criterion']}",
            f"- Allowed next action: {item['allowed_next_action']}", f"- Workstream: `{item['relevant_workstream']}`", "",
        ])
    return """# Project FAR Research-Question Registry

Status: **Generated index over existing question/problem authorities**

Source: [`research/registry/research-questions-v1.0.json`](../../research/registry/research-questions-v1.0.json).

This index connects serious active questions to the accepted unresolved-question,
open-problem, limitation, and workstream structures. It does not replace those authorities and
does not authorize execution by itself.

""" + "\n".join(sections)


def render_assurance(data: dict) -> str:
    rows = []
    for item in data["claims"]:
        rows.append(f"| `{item['id']}` | `{item['truth_disposition']}` | `{item['governing_ledger_provenance_status']}` | `{item['proof_status']}` | `{item['independent_review_status']}` | `{item['formalization_status']}` | `{item['empirical_status']}` | `{item['novelty_prior_art_status']}` |")
    return """# FAR-CORE assurance ledger

Status: **Generated assurance view; governing statements remain in theory v1.1**

Source: [`theory/evaluation/far-core-assurance-v1.0.json`](../../theory/evaluation/far-core-assurance-v1.0.json).

Truth, narrative proof, independent review, proof-assistant formalization, empirical evidence,
novelty/prior art, governance, version, and scope are independent dimensions. No column may be
used as a substitute for another. In particular, FAR-CORE-014's W1 truth verdict is `PROVED`
under its exact application scope while its governing-ledger provenance label remains
`supported_derived`.

| Claim | Truth | Governing provenance | Proof | Independent review | Lean | Empirical | Novelty/prior art |
|---|---|---|---|---|---|---|---|
""" + "\n".join(rows) + "\n"


def _slug(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()[:16]


def build_graph(data: dict[str, dict]) -> dict:
    source_paths = sorted(set(DATA_SCHEMAS) | GRAPH_ADDITIONAL_SOURCES)
    generated_from = {path: sha256(ROOT / path) for path in source_paths}
    nodes: dict[str, dict] = {}
    raw_edges: set[tuple[str, str, str, str]] = set()

    def node(
        identifier: str,
        kind: str,
        label: str,
        status: str,
        source: str,
        **metadata: Any,
    ) -> None:
        candidate = {
            "id": identifier,
            "type": kind,
            "label": label,
            "status": status,
            "source": source,
            **metadata,
        }
        if identifier in nodes and nodes[identifier] != candidate:
            raise ValueError(f"contradictory node mapping: {identifier}")
        nodes[identifier] = candidate

    def edge(kind: str, source: str, target: str, provenance: str) -> None:
        raw_edges.add((kind, source, target, provenance))

    version_id = "version:PROJECT-FAR-CORE-THEORY-1.1"
    node(version_id, "version", "Project FAR Core Theory v1.1", "governing", "theory/terminal/project-far-core-theory-v1.1.json")
    contract_id = "contract:local-exact-comparison"
    node(contract_id, "contract", "Local exact comparison contract C=(X,T,V,obs)", "governing-definition", "theory/theorems/Project-FAR-Theory-Closure-v1.0.md#21-local-comparison-contract")
    node("domain:set-based-exact", "domain", "Set-based exact contract domain", "declared-scope", "theory/terminal/project-far-core-theory-v1.1.json")
    node("representation:finite-playground", "representation", "Finite exact playground representation", "experimental-noncanonical", "tools/exact_contract_playground.py")
    node("test-context:declared-tests", "test_context", "Declared tests/contexts T", "contract-relative", "theory/theorems/Project-FAR-Theory-Closure-v1.0.md#21-local-comparison-contract")
    edge("APPLIES_TO", contract_id, "domain:set-based-exact", "canonical contract scope")
    edge("IMPLEMENTS", "representation:finite-playground", contract_id, "experimental finite demonstrator")
    edge("APPLIES_TO", contract_id, "test-context:declared-tests", "contract definition")

    assurance = data["theory/evaluation/far-core-assurance-v1.0.json"]["claims"]
    formalization_by_id = {
        item["id"]: item
        for item in data["theory/evaluation/far-core-formalization-ledger-v1.0.json"]["claims"]
    }
    core_ids = {item["id"] for item in assurance}
    for item in assurance:
        claim_id = f"claim:{item['id']}"
        node(
            claim_id,
            "claim",
            item["exact_statement"],
            "multidimensional_assurance",
            "theory/evaluation/far-core-assurance-v1.0.json",
            scope=item["scope"],
            status_dimensions={
                "truth_disposition": item["truth_disposition"],
                "governing_ledger_provenance_status": item[
                    "governing_ledger_provenance_status"
                ],
                "proof_status": item["proof_status"],
                "independent_review_status": item["independent_review_status"],
                "formalization_status": item["formalization_status"],
                "empirical_status": item["empirical_status"],
                "novelty_prior_art_status": item["novelty_prior_art_status"],
                "governance_status": item["governance_status"],
                "version": item["version"],
            },
        )
        edge("DEPENDS_ON", claim_id, version_id, "assurance version")
        edge("APPLIES_TO", claim_id, contract_id, "assurance scope")
        for dependency in item["dependencies"]:
            if dependency in core_ids:
                target = f"claim:{dependency}"
                edge("DEPENDS_ON", claim_id, target, "assurance dependencies")
            else:
                target = f"premise:{dependency}"
                node(target, "premise", dependency.replace("_", " "), "declared", "theory/evaluation/far-core-assurance-v1.0.json")
                edge("ASSUMES", claim_id, target, "assurance dependencies")
        formal = formalization_by_id[item["id"]]
        for declaration in formal["lean_declarations"]:
            theorem_id = f"theorem:{declaration}"
            node(theorem_id, "theorem", declaration, formal["formalization_status"], formal["intended_lean_module"])
            edge("FORMALIZES", theorem_id, claim_id, "assurance Lean mapping")
        for premise in formal["premises"]:
            premise_id = f"premise:{_slug(item['id'] + premise)}"
            node(premise_id, "premise", premise, "encoded", "theory/evaluation/far-core-formalization-ledger-v1.0.json")
            edge("ASSUMES", f"theorem:{formal['lean_declarations'][0]}", premise_id, "formalization ledger premise")
        for artifact in item["internal_proof_artifacts"]:
            proof_id = f"proof:{_slug(artifact)}"
            node(proof_id, "proof", artifact, item["proof_status"], artifact)
            edge("PROVES", proof_id, claim_id, "assurance internal proof")
        for artifact in item["independent_review_artifacts"]:
            evidence_id = f"evidence:{_slug(artifact)}"
            node(evidence_id, "evidence_artifact", artifact, item["independent_review_status"], artifact)
            edge("SUPPORTS", evidence_id, claim_id, "independent review")
        for limitation in item["limitations"]:
            limitation_id = f"limitation:{_slug(item['id'] + limitation)}"
            node(limitation_id, "limitation", limitation, "binding", "theory/evaluation/far-core-assurance-v1.0.json")
            edge("LIMITS", limitation_id, claim_id, "assurance limitation")
        for counterexample in item["known_counterexamples_to_stronger_variants"]:
            counter_id = f"counterexample:{_slug(item['id'] + counterexample)}"
            node(counter_id, "counterexample", counterexample, "retained", "theory/evaluation/far-core-assurance-v1.0.json")
            edge("LIMITS", counter_id, claim_id, "counterexample to stronger variant")

    opportunities = data["research/registry/opportunities-v1.0.json"]["opportunities"]
    opportunity_ids = {item["id"] for item in opportunities}
    for item in opportunities:
        identifier = f"open-problem:{item['id']}"
        node(identifier, "open_problem", item["name"], item["status"], "research/registry/opportunities-v1.0.json")
        target = f"workstream:{item['target_workstream']}"
        node(target, "workstream", item["target_workstream"], "registered", "theory/evaluation/post-closure-assurance-and-application-program-v1.0.json")
        edge("APPLIES_TO", identifier, target, "opportunity target workstream")
        for dependency in item["implementation_dependencies"] + item["theoretical_dependencies"]:
            if dependency in opportunity_ids:
                edge("DEPENDS_ON", identifier, f"open-problem:{dependency}", "opportunity dependency")
            elif dependency in core_ids:
                edge("DEPENDS_ON", identifier, f"claim:{dependency}", "opportunity theory dependency")

    questions = data["research/registry/research-questions-v1.0.json"]["questions"]
    for item in questions:
        identifier = f"research-question:{item['id']}"
        node(identifier, "research_question", item["exact_question"], item["current_disposition"], "research/registry/research-questions-v1.0.json")
        target = f"workstream:{item['relevant_workstream']}"
        node(target, "workstream", item["relevant_workstream"], "registered", "theory/evaluation/post-closure-assurance-and-application-program-v1.0.json")
        edge("APPLIES_TO", identifier, target, "research question workstream")
        for dependency in item["dependencies"]:
            if dependency in core_ids:
                edge("DEPENDS_ON", identifier, f"claim:{dependency}", "research question dependency")
            elif dependency in opportunity_ids:
                edge("DEPENDS_ON", identifier, f"open-problem:{dependency}", "research question dependency")

    citations = data["research/registry/citation-links-v1.0.json"]
    for item in citations["sources"]:
        node(f"source:{item['citation_key']}", "source", item["identity"], item["identity_status"], item["canonical_locator"])
    for relation in citations["relationships"]:
        source = f"source:{relation['citation_key']}"
        if relation["claim_id"] in core_ids:
            target = f"claim:{relation['claim_id']}"
            edge("CITES", target, source, relation["id"])
            mapped = {"SUPPORTS":"SUPPORTS","DISPUTES":"CONFLICTS_WITH","CONTEXT":"APPLIES_TO","ANTICIPATES":"SUPPORTS","LIMITS":"LIMITS","DOES_NOT_ESTABLISH":"LIMITS"}[relation["relationship"]]
            edge(mapped, source, target, relation["id"])

    for item in data["research/registry/research-tools-v1.0.json"]["tools"]:
        node(f"tool:{item['id']}", "tool", item["name"], item["authority"], "research/registry/research-tools-v1.0.json")

    promotion_path = "theory/evaluation/pca-w1-independent-review-promotion-v1.0.json"
    promotion = load(promotion_path)
    review_target = promotion["review_target"]
    review_branch = promotion["review_branch"]
    node(
        "pr-commit:W1-target",
        "pr_commit",
        (
            f"W1 immutable target {review_target['commit'][:8]} / "
            f"{review_target['tree'][:8]}"
        ),
        "sealed",
        promotion_path,
    )
    node(
        "pr-commit:W1-review",
        "pr_commit",
        (
            f"W1 review {review_branch['head'][:8]} / "
            f"{review_branch['tree'][:8]}"
        ),
        "accepted-evidence",
        promotion_path,
    )
    edge("TESTS", "pr-commit:W1-review", "pr-commit:W1-target", "W1 promotion record")
    edge("SUPPORTS", "pr-commit:W1-review", version_id, "W1 promotion record")

    for node_item in list(nodes.values()):
        if node_item["type"] == "theorem":
            definition_id = f"definition:{node_item['id'].split(':',1)[1].split('.')[-1]}"
            node(definition_id, "definition", f"encoded definition for {node_item['label']}", "formalization-mapped", node_item["source"])
            edge("DERIVES", definition_id, node_item["id"], "formalization mapping")

    ordered_edges = []
    for index, (kind, source, target, provenance) in enumerate(sorted(raw_edges), 1):
        if source not in nodes or target not in nodes:
            raise ValueError(f"dangling graph edge: {source} -> {target}")
        ordered_edges.append({"id":f"EDGE-{index:05d}","type":kind,"source":source,"target":target,"provenance":provenance})
    return {"schema_version":"1.0","graph_id":"PROJECT-FAR-KNOWLEDGE-GRAPH-1.0","authority":"generated_view_not_independent_truth_system","generated_from":generated_from,"nodes":[nodes[key] for key in sorted(nodes)],"edges":ordered_edges}


def graph_errors(graph: dict) -> list[str]:
    errors: list[str] = []
    ids = [item["id"] for item in graph["nodes"]]
    if len(ids) != len(set(ids)):
        errors.append("duplicate graph node")
    node_ids = set(ids)
    for edge in graph["edges"]:
        if edge["source"] not in node_ids or edge["target"] not in node_ids:
            errors.append(f"dangling graph edge {edge['id']}")
    adjacency: dict[str, list[str]] = {}
    for edge in graph["edges"]:
        if edge["type"] == "DEPENDS_ON":
            adjacency.setdefault(edge["source"], []).append(edge["target"])
    visiting: set[str] = set()
    visited: set[str] = set()
    def visit(current: str) -> None:
        if current in visiting:
            errors.append(f"prohibited DEPENDS_ON cycle at {current}")
            return
        if current in visited:
            return
        visiting.add(current)
        for target in adjacency.get(current, []):
            visit(target)
        visiting.remove(current)
        visited.add(current)
    for identifier in sorted(adjacency):
        visit(identifier)
    return sorted(set(errors))


def expected_outputs(data: dict[str, dict]) -> dict[str, str]:
    graph = build_graph(data)
    return {
        "docs/planning/opportunity-registry.md": render_opportunities(data["research/registry/opportunities-v1.0.json"]),
        "docs/research/research-question-registry.md": render_questions(data["research/registry/research-questions-v1.0.json"]),
        "docs/assurance/far-core-assurance.md": render_assurance(data["theory/evaluation/far-core-assurance-v1.0.json"]),
        "artifacts/knowledge-graph/project-far-knowledge-graph.json": json.dumps(graph, indent=2, sort_keys=True, ensure_ascii=False) + "\n",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    try:
        data = {path: load(path) for path in DATA_SCHEMAS}
        errors = validate_schemas(data) + semantic_errors(data)
        outputs = expected_outputs(data)
        graph = json.loads(outputs["artifacts/knowledge-graph/project-far-knowledge-graph.json"])
        errors += graph_errors(graph)
    except (OSError, json.JSONDecodeError, jsonschema.ValidationError, ValueError) as exc:
        print(f"FAIL: {exc}")
        return 1
    if errors:
        print("FAIL: " + "; ".join(sorted(set(errors))))
        return 1
    if args.write:
        for path, content in outputs.items():
            target = ROOT / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8")
        print(f"wrote {len(outputs)} generated registry/knowledge-graph views")
        return 0
    stale = [path for path, content in outputs.items() if not (ROOT / path).is_file() or (ROOT / path).read_text(encoding="utf-8") != content]
    if stale:
        print("FAIL: stale generated outputs: " + ", ".join(stale))
        return 1
    print(f"FAR research registries and knowledge graph: PASS (nodes={len(graph['nodes'])}, edges={len(graph['edges'])})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
