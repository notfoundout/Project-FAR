#!/usr/bin/env python3
"""Execute FAR-THEORY-DEPENDENCY-AUDIT-001 from its frozen base-commit blobs."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
SPEC_PATH = ROOT / "research/theory-dependency-audit/execution-spec-v1.0.json"
RESULT_PATH = ROOT / "research/theory-dependency-audit/result-v1.0.json"
PROOF_INVENTORY_PATH = "docs/governance/theorem-proof-status-register.md"

SOURCE_PATHS = {
    "definitions": "theory/definitions/definitions.md",
    "primitives": "frameworks/FARA/primitives.md",
    "formal_kernel": "frameworks/FARA/formal-kernel.md",
    "terminology": "docs/glossary/canonical-terminology.md",
    "semantic_registry": "docs/governance/semantic-consistency.json",
    "framework_boundaries": "docs/governance/framework-boundaries.md",
    "derivation_matrix": "docs/governance/derivation-status-matrix.md",
    "far_dependency": "frameworks/FAR/dependency-graph.md",
    "faro_dependency": "frameworks/FARO/dependency-graph.md",
}


def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _run_git(root: Path, *args: str) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        ["git", "-C", str(root), *args],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def read_base_blob(root: Path, base_commit: str, relative: str) -> bytes:
    """Read a recorded blob from the frozen base, fetching that commit if shallow."""
    specifier = f"{base_commit}:{relative}"
    result = _run_git(root, "show", specifier)
    if result.returncode == 0:
        return result.stdout

    remote = _run_git(root, "remote", "get-url", "origin")
    if remote.returncode != 0:
        raise ValueError(
            f"frozen base unavailable and no origin remote exists: {base_commit}"
        )
    fetch = _run_git(
        root,
        "fetch",
        "--no-tags",
        "--depth=1",
        "origin",
        base_commit,
    )
    if fetch.returncode != 0:
        raise ValueError(
            "unable to fetch frozen base commit: "
            + fetch.stderr.decode("utf-8", errors="replace").strip()
        )
    result = _run_git(root, "show", specifier)
    if result.returncode != 0:
        raise ValueError(
            f"frozen blob unavailable at {base_commit}:{relative}: "
            + result.stderr.decode("utf-8", errors="replace").strip()
        )
    return result.stdout


def read_source(
    root: Path,
    base_commit: str,
    relative: str,
    *,
    source_mode: str,
) -> bytes:
    if source_mode == "git":
        return read_base_blob(root, base_commit, relative)
    if source_mode == "worktree":
        path = root / relative
        if not path.is_file():
            raise FileNotFoundError(f"locked source missing: {relative}")
        return path.read_bytes()
    raise ValueError(f"unsupported source mode: {source_mode}")


def contains_all(text: str, markers: list[str]) -> bool:
    lowered = text.lower()
    return all(marker.lower() in lowered for marker in markers)


def parse_candidate_primitives(text: str) -> list[str]:
    match = re.search(
        r"# Current Candidate Primitives\s+The current candidate primitive concepts are:\s+(.*?)\s+These concepts presently serve",
        text,
        flags=re.DOTALL,
    )
    if not match:
        return []
    return re.findall(r"^- (.+)$", match.group(1), flags=re.MULTILINE)


def parse_table(
    text: str,
    *,
    first_header: str,
    value_names: tuple[str, ...],
) -> dict[str, dict[str, str]]:
    rows: dict[str, dict[str, str]] = {}
    active = False
    for line in text.splitlines():
        if line.startswith(f"| {first_header} |"):
            active = True
            continue
        if not active:
            continue
        if not line.startswith("|"):
            if rows:
                break
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if not cells or not cells[0] or set(cells[0]) == {"-"}:
            continue
        if len(cells) < len(value_names) + 1:
            continue
        rows[cells[0].lower()] = {
            "label": cells[0],
            **{name: cells[index + 1] for index, name in enumerate(value_names)},
        }
    return rows


def normalize_owner(value: str | None) -> str | None:
    if value is None:
        return None
    return " ".join(value.lower().replace("-", " ").split())


def row_matches(
    rows: dict[str, dict[str, str]],
    label: str,
    *,
    owner: str | None = None,
    status: str | None = None,
    rationale_marker: str | None = None,
) -> bool:
    row = rows.get(label.lower())
    if row is None:
        return False
    if owner is not None and normalize_owner(row.get("owner")) != normalize_owner(owner):
        return False
    if status is not None and row.get("status", "").lower() != status.lower():
        return False
    if rationale_marker is not None and rationale_marker.lower() not in row.get(
        "rationale", ""
    ).lower():
        return False
    return True


def inspect_source_admissibility(sources: dict[str, str]) -> dict[str, Any]:
    artifacts: dict[str, dict[str, Any]] = {}

    def record(path: str, state: str, evidence: str) -> None:
        artifacts[path] = {
            "identity_verified": True,
            "acceptance_state": state,
            "acceptance_verified": state == "Accepted",
            "evidence": evidence,
        }

    definitions = sources[SOURCE_PATHS["definitions"]]
    if "Status: **Accepted" in definitions:
        record(SOURCE_PATHS["definitions"], "Accepted", "explicit Accepted marker")
    else:
        record(
            SOURCE_PATHS["definitions"],
            "Unknown",
            "canonical authority is declared, but Accepted lifecycle status is not",
        )

    primitives = sources[SOURCE_PATHS["primitives"]]
    if "Status: **Accepted" in primitives:
        record(SOURCE_PATHS["primitives"], "Accepted", "explicit Accepted marker")
    elif "Candidate primitive status is provisional" in primitives:
        record(
            SOURCE_PATHS["primitives"],
            "Provisional",
            "artifact explicitly declares candidate primitive status provisional",
        )
    else:
        record(SOURCE_PATHS["primitives"], "Unknown", "Accepted status not declared")

    formal_kernel = sources[SOURCE_PATHS["formal_kernel"]]
    record(
        SOURCE_PATHS["formal_kernel"],
        "Accepted" if "Status: **Accepted**" in formal_kernel else "Unknown",
        "explicit Accepted marker"
        if "Status: **Accepted**" in formal_kernel
        else "Accepted status not declared",
    )

    terminology = sources[SOURCE_PATHS["terminology"]]
    record(
        SOURCE_PATHS["terminology"],
        "Accepted"
        if "Status: **Accepted terminology authority**" in terminology
        else "Unknown",
        "explicit Accepted marker"
        if "Status: **Accepted terminology authority**" in terminology
        else "Accepted status not declared",
    )

    semantic_registry = json.loads(sources[SOURCE_PATHS["semantic_registry"]])
    semantic_accepted = str(semantic_registry.get("status", "")).lower().startswith(
        "accepted"
    )
    record(
        SOURCE_PATHS["semantic_registry"],
        "Accepted" if semantic_accepted else "Unknown",
        "top-level Accepted status field"
        if semantic_accepted
        else "top-level Accepted status is absent",
    )

    boundaries = sources[SOURCE_PATHS["framework_boundaries"]]
    record(
        SOURCE_PATHS["framework_boundaries"],
        "Accepted"
        if "Status: **Accepted architectural specification**" in boundaries
        else "Unknown",
        "explicit Accepted marker"
        if "Status: **Accepted architectural specification**" in boundaries
        else "Accepted status not declared",
    )

    derivation = sources[SOURCE_PATHS["derivation_matrix"]]
    record(
        SOURCE_PATHS["derivation_matrix"],
        "Accepted"
        if "Status: **Accepted classification register**" in derivation
        else "Unknown",
        "explicit Accepted marker"
        if "Status: **Accepted classification register**" in derivation
        else "Accepted status not declared",
    )

    for key in ("far_dependency", "faro_dependency"):
        path = SOURCE_PATHS[key]
        accepted = "Status: **Accepted" in sources[path]
        record(
            path,
            "Accepted" if accepted else "Unknown",
            "explicit Accepted marker" if accepted else "Accepted status not declared",
        )

    counts = {"Accepted": 0, "Provisional": 0, "Unknown": 0}
    for row in artifacts.values():
        counts[row["acceptance_state"]] += 1
    return {
        "all_selected_sources_accepted": all(
            row["acceptance_verified"] for row in artifacts.values()
        ),
        "counts": counts,
        "artifacts": artifacts,
    }


def adjudicate_content(
    content_pass: bool,
    required_sources: list[str],
    admissibility: dict[str, Any],
) -> str:
    if not all(
        admissibility["artifacts"][path]["acceptance_verified"]
        for path in required_sources
    ):
        return "Unknown"
    return "Pass" if content_pass else "Fail"


def execute(
    spec: dict[str, Any] | None = None,
    *,
    root: Path = ROOT,
    source_mode: str = "git",
) -> dict[str, Any]:
    spec = spec or load_json(root / SPEC_PATH.relative_to(ROOT))
    sources: dict[str, str] = {}
    lock_results: dict[str, dict[str, Any]] = {}

    for relative, expected_sha in spec["source_locks"].items():
        data = read_source(
            root,
            spec["base_commit"],
            relative,
            source_mode=source_mode,
        )
        actual_sha = git_blob_sha(data)
        verified = actual_sha == expected_sha
        lock_results[relative] = {
            "expected_git_blob_sha": expected_sha,
            "actual_git_blob_sha": actual_sha,
            "verified": verified,
        }
        if not verified:
            raise ValueError(f"frozen source identity mismatch: {relative}")
        sources[relative] = data.decode("utf-8")

    missing_selected = sorted(set(SOURCE_PATHS.values()) - set(sources))
    if missing_selected:
        raise ValueError(
            f"required frozen source missing from specification: {missing_selected}"
        )

    admissibility = inspect_source_admissibility(sources)
    proof_inventory_in_scope = PROOF_INVENTORY_PATH in sources

    primitives = spec["candidate_primitives"]
    expected_terms = {primitive.lower() for primitive in primitives}
    definitions = sources[SOURCE_PATHS["definitions"]]
    primitive_registry = sources[SOURCE_PATHS["primitives"]]
    formal_kernel = sources[SOURCE_PATHS["formal_kernel"]]
    terminology = sources[SOURCE_PATHS["terminology"]]
    semantic_registry = json.loads(sources[SOURCE_PATHS["semantic_registry"]])
    framework_boundaries = sources[SOURCE_PATHS["framework_boundaries"]]
    derivation_matrix = sources[SOURCE_PATHS["derivation_matrix"]]
    far_dependency = sources[SOURCE_PATHS["far_dependency"]]
    faro_dependency = sources[SOURCE_PATHS["faro_dependency"]]

    terminology_rows = parse_table(
        terminology,
        first_header="Canonical term",
        value_names=("meaning", "owner", "status", "detail"),
    )
    derivation_rows = parse_table(
        derivation_matrix,
        first_header="Procedure",
        value_names=("owner", "status", "rationale"),
    )

    definition_headings = {
        primitive: f"## {primitive}" in definitions for primitive in primitives
    }
    c1_content = contains_all(
        definitions,
        [
            "establishes the canonical terminology used throughout Project FAR",
            "The definitions contained in this document are canonical",
        ],
    ) and all(definition_headings.values())

    parsed_primitives = parse_candidate_primitives(primitive_registry)
    c2_content = (
        parsed_primitives == primitives
        and "theory/definitions/definitions.md" in primitive_registry
        and "candidate primitive status is not evidence of irreducibility"
        in primitive_registry.lower()
    )

    terminology_candidates = {
        term: row
        for term, row in terminology_rows.items()
        if "candidate primitive" in row.get("status", "").lower()
    }
    semantic_candidates = {
        row["term"].lower(): row
        for row in semantic_registry.get("canonical_terms", [])
        if row.get("status", "").lower() == "candidate-primitive"
    }
    terminology_coverage = (
        expected_terms & set(terminology_candidates)
    ) == expected_terms
    semantic_coverage = (expected_terms & set(semantic_candidates)) == expected_terms
    represented_owner_agreement = all(
        normalize_owner(terminology_candidates[term].get("owner"))
        == normalize_owner(semantic_candidates[term].get("owner"))
        for term in expected_terms & set(terminology_candidates) & set(semantic_candidates)
    )
    c3_content = terminology_coverage and semantic_coverage and represented_owner_agreement

    c4_content = contains_all(
        formal_kernel,
        [
            "Status: **Accepted**",
            "finite, explicit, auditable representational architectures in Project FAR v1.0",
            "The formal carrier names do not reclassify FARA's seven candidate primitives.",
            "does not establish their global independence, necessity, minimality, or irreducibility",
        ],
    )

    far_contract_markers = contains_all(
        far_dependency,
        [
            "FARA provides the architecture used by FAR",
            "FAR applies these architectural concepts methodologically",
            "It does not modify their definitions",
        ],
    )
    far_negative_record = row_matches(
        derivation_rows,
        "FAR staged/multi-pass workflow",
        owner="FAR",
        status="compatible independent methodology",
        rationale_marker="no FARA derivation is recorded",
    )
    c5_content = (
        far_contract_markers
        and contains_all(
            framework_boundaries,
            ["that its procedural choices are FARA theorems"],
        )
        and far_negative_record
    )

    faro_contract_markers = contains_all(
        faro_dependency,
        [
            "Supplies representational architecture",
            "Supplies stable investigation methodology",
        ],
    )
    faro_negative_record = row_matches(
        derivation_rows,
        "operational audit/comparison/reporting",
        owner="FARO",
        status="compatible independent operations",
        rationale_marker="no necessity theorem exists",
    )
    c6_content = (
        faro_contract_markers
        and contains_all(
            framework_boundaries,
            ["that operational choices follow necessarily from FARA/FAR"],
        )
        and faro_negative_record
    )

    protocol_rows = {
        "evaluator_mapping": row_matches(
            derivation_rows,
            "evaluator mapping",
            owner="CRP/FARO",
            status="empirical protocol",
        ),
        "evaluator_controls": row_matches(
            derivation_rows,
            "evaluator independence/competence/calibration",
            owner="CRP",
            status="experimental-design choice",
        ),
        "canonicalization_and_cir": row_matches(
            derivation_rows,
            "canonicalization and CIR",
            owner="CRP",
            status="protocol design choice",
        ),
        "pareto": row_matches(
            derivation_rows,
            "Pareto comparison / CIR cost metrics",
            owner="CRP/FARO",
            status="protocol decision rule",
        ),
        "preregistration": row_matches(
            derivation_rows,
            "preregistration and frozen evidence",
            owner="methodology/governance",
            status="governance rule",
        ),
        "fail_reporting": row_matches(
            derivation_rows,
            "fail reports and uncertainty outputs",
            owner="FARO",
            status="governance/usability choice",
        ),
    }
    terminology_protocol_rows = {
        "evaluator_mapping": row_matches(
            terminology_rows,
            "evaluator mapping",
            owner="CRP methodology",
            status="empirical artifact",
        ),
        "canonicalization": row_matches(
            terminology_rows,
            "canonicalization",
            owner="methodology",
            status="independent design choice",
        ),
        "cir": row_matches(
            terminology_rows,
            "CIR",
            owner="CRP methodology",
            status="protocol artifact, not canonical theory",
        ),
        "pareto": row_matches(
            terminology_rows,
            "Pareto dominance",
            owner="CRP methodology",
            status="decision rule",
        ),
        "fail_report": row_matches(
            terminology_rows,
            "fail report",
            owner="FARO",
            status="independent governance/method choice",
        ),
    }
    c7_content = all(protocol_rows.values()) and all(terminology_protocol_rows.values())

    required_sources = {
        "C1": [SOURCE_PATHS["definitions"]],
        "C2": [SOURCE_PATHS["primitives"]],
        "C3": [
            SOURCE_PATHS["definitions"],
            SOURCE_PATHS["primitives"],
            SOURCE_PATHS["terminology"],
            SOURCE_PATHS["semantic_registry"],
        ],
        "C4": [SOURCE_PATHS["formal_kernel"]],
        "C5": [
            SOURCE_PATHS["far_dependency"],
            SOURCE_PATHS["framework_boundaries"],
            SOURCE_PATHS["derivation_matrix"],
        ],
        "C6": [
            SOURCE_PATHS["faro_dependency"],
            SOURCE_PATHS["framework_boundaries"],
            SOURCE_PATHS["derivation_matrix"],
        ],
        "C7": [SOURCE_PATHS["derivation_matrix"], SOURCE_PATHS["terminology"]],
    }
    content_results = {
        "C1": c1_content,
        "C2": c2_content,
        "C3": c3_content,
        "C4": c4_content,
        "C5": c5_content,
        "C6": c6_content,
        "C7": c7_content,
    }
    names = {
        "C1": "canonical_definition_authority",
        "C2": "fara_candidate_classification",
        "C3": "undifferentiated_registry_adequacy",
        "C4": "formal_kernel_role_boundary",
        "C5": "far_dependency_kind",
        "C6": "faro_dependency_kind",
        "C7": "protocol_derivation_boundary",
    }
    measurements = {
        "C1": {
            "definition_headings": definition_headings,
            "content_markers_present": c1_content,
        },
        "C2": {
            "parsed_candidate_primitives": parsed_primitives,
            "content_markers_present": c2_content,
        },
        "C3": {
            "semantic_registry_covers_all_seven": semantic_coverage,
            "terminology_inventory_covers_all_seven": terminology_coverage,
            "represented_owner_values_agree": represented_owner_agreement,
        },
        "C4": {"content_markers_present": c4_content},
        "C5": {
            "artifact_contract_markers_present": far_contract_markers,
            "negative_derivation_record_present": far_negative_record,
            "proof_inventory_in_scope": proof_inventory_in_scope,
            "positive_derivation_proof_verified": False,
        },
        "C6": {
            "artifact_workflow_markers_present": faro_contract_markers,
            "negative_derivation_record_present": faro_negative_record,
            "proof_inventory_in_scope": proof_inventory_in_scope,
            "positive_derivation_proof_verified": False,
        },
        "C7": {
            "derivation_matrix_classifications": protocol_rows,
            "terminology_authority_classifications": terminology_protocol_rows,
        },
    }

    checks = []
    for check_id in ("C1", "C2", "C3", "C4", "C5", "C6", "C7"):
        checks.append(
            {
                "id": check_id,
                "name": names[check_id],
                "status": adjudicate_content(
                    content_results[check_id],
                    required_sources[check_id],
                    admissibility,
                ),
                "content_result": "Pass" if content_results[check_id] else "Fail",
                "required_sources": required_sources[check_id],
                "acceptance_verified": all(
                    admissibility["artifacts"][path]["acceptance_verified"]
                    for path in required_sources[check_id]
                ),
                "measurements": measurements[check_id],
            }
        )

    check_status = {row["id"]: row["status"] for row in checks}
    authority_evidence_complete = all(
        check_status[check_id] in {"Pass", "Fail"}
        for check_id in ("C1", "C2", "C3", "C4")
    )
    dependency_evidence_complete = (
        all(
            check_status[check_id] in {"Pass", "Fail"}
            for check_id in ("C5", "C6", "C7")
        )
        and proof_inventory_in_scope
    )

    return {
        "schema_version": "1.0",
        "investigation_id": spec["investigation_id"],
        "status": "Research",
        "base_commit": spec["base_commit"],
        "source_lock_results": lock_results,
        "source_admissibility": admissibility,
        "proof_scope": {
            "authoritative_proof_inventory_path": PROOF_INVENTORY_PATH,
            "selected_in_frozen_source_set": proof_inventory_in_scope,
            "positive_derivation_proof_verified": False,
            "proof_absence_verified": False,
            "status": "Unknown" if not proof_inventory_in_scope else "In scope",
        },
        "checks": checks,
        "candidate_adjudication": {
            "authority_models": {
                "undifferentiated_owner": "Unknown",
                "split_authority": "Unknown",
            },
            "dependency_models": {
                "logical_derivation": "Unknown",
                "artifact_workflow_contract": "Unknown",
                "unclassified_dependency": "Unknown",
            },
        },
        "observations": [
            "All nine selected files match their preregistered Git blob identities at the frozen base commit.",
            "Four selected files explicitly declare Accepted status, one selected file explicitly declares provisional status, and four selected files do not verify Accepted status within the frozen source set.",
            "The selected source text contains the registered definition, classification, formal-kernel, framework-boundary, dependency, evaluator, and protocol markers measured by C1-C7.",
            "The authoritative theorem/proof-status register was not selected, so proof presence or absence cannot be adjudicated.",
            "Source identity does not establish source Acceptance.",
        ],
        "discovery": {
            "supported": False,
            "finding": "no_reconciliation_discovery_supported",
            "failure_mode": "source_admissibility_and_proof_scope_incomplete",
            "authority_evidence_complete": authority_evidence_complete,
            "dependency_evidence_complete": dependency_evidence_complete,
        },
        "failures": [
            "The frozen design did not include an Accepted-status authority capable of validating every selected source.",
            "The FARA primitive registry explicitly declares its candidate status provisional.",
            "The semantic registry and FAR/FARO dependency graphs do not declare Accepted status within the selected evidence.",
            "The authoritative theorem/proof-status register was omitted, so logical derivation and proof absence remain Unknown.",
            "Post-hoc addition of omitted evidence is prohibited; a separately preregistered campaign is required.",
        ],
        "lifecycle": {
            "question": "complete",
            "execution": "complete",
            "observation": "complete",
            "discovery": "complete",
            "outcome": "failure report",
            "replication": "blocked pending separately preregistered source-complete campaign",
            "acceptance": "prohibited",
            "promotion": "prohibited",
            "repository_change": "prohibited except Research evidence and validation wiring",
        },
        "nonclaims": spec["nonclaims"],
    }


def canonical_json(value: Any) -> str:
    return json.dumps(value, indent=2, sort_keys=True) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    try:
        result = execute()
    except (
        FileNotFoundError,
        ValueError,
        json.JSONDecodeError,
    ) as exc:
        print(f"theory/dependency audit: FAIL: {exc}")
        return 1

    rendered = canonical_json(result)
    if args.write:
        RESULT_PATH.write_text(rendered, encoding="utf-8")
        print(f"wrote {RESULT_PATH.relative_to(ROOT)}")
        return 0

    if not RESULT_PATH.is_file():
        print("theory/dependency audit: FAIL: committed result missing")
        return 1
    committed = RESULT_PATH.read_text(encoding="utf-8")
    if committed != rendered:
        print("theory/dependency audit: FAIL: committed result drift")
        return 1
    print("theory/dependency audit: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
