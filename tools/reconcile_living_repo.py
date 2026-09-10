#!/usr/bin/env python3
"""Reconcile Project FAR's living repository state against canonical governed surfaces.

The reconciler is deliberately non-authoritative. It derives hashes, claim/RQ inventories,
dependency impact, and candidate review queues. It can detect that a canonical claim may need
review or reopening, but cannot itself promote a correction.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any

SURFACES_PATH = Path("research/living/repository-surfaces-v1.0.json")
STATE_PATH = Path("research/living/repository-state-v1.0.json")
CANDIDATE_DIR = Path("research/living/inbox/candidates")
REVIEW_DISPOSITIONS_PATH = Path("research/living/review-dispositions-v1.0.json")
STATUS_PATH = Path("docs/research/living-repository-status.md")
CLAIM_LEDGER = Path("theory/terminal/project-far-core-theory-v1.1.json")
ASSURANCE_LEDGER = Path("theory/evaluation/far-core-assurance-v1.0.json")
RQ_LEDGER = Path("research/registry/research-questions-v1.0.json")

AUTHORITY_BOUNDARY = (
    "Research candidate only. Discovery or triage does not establish support, dispute, "
    "novelty, priority, external validity, utility, independence, theorem status, EFR result, "
    "or any other Project FAR claim/evidence disposition."
)
ALLOWED_REVIEW_DISPOSITIONS = {
    "IRRELEVANT_FALSE_POSITIVE",
    "ADJACENT_NO_CONTRADICTION",
    "N1_PRIOR_ART_LEAD",
}
CORE_THREAT_TARGET = "FAR-RQ-009"
CORE_THREAT_RELATION = "POTENTIAL_COUNTEREXAMPLE_OR_RELATED_THEOREM"


class ReconciliationError(RuntimeError):
    pass


def read_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        value = json.load(handle)
    if not isinstance(value, dict):
        raise ReconciliationError(f"expected object: {path}")
    return value


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_review_dispositions(root: Path) -> dict[str, dict[str, Any]]:
    """Load protected review memory without mutating raw discovery records.

    The file is optional for synthetic/legacy fixtures; canonical main carries it and tests
    require the shipped registry. Any present registry fails closed on malformed rows.
    """
    path = root / REVIEW_DISPOSITIONS_PATH
    if not path.exists():
        return {}
    registry = read_json(path)
    if registry.get("program_id") != "FAR-LIVING-REVIEW-DISPOSITIONS-001":
        raise ReconciliationError("unexpected living review-disposition program_id")
    if registry.get("authority") != "Research":
        raise ReconciliationError("review-disposition authority drift")
    if registry.get("authority_boundary") != AUTHORITY_BOUNDARY:
        raise ReconciliationError("review-disposition authority boundary drift")
    declared = registry.get("allowed_dispositions")
    if not isinstance(declared, list) or set(declared) != ALLOWED_REVIEW_DISPOSITIONS:
        raise ReconciliationError("review-disposition allowed set drift")
    rows = registry.get("reviewed_candidates")
    if not isinstance(rows, list):
        raise ReconciliationError("reviewed_candidates must be an array")
    result: dict[str, dict[str, Any]] = {}
    for row in rows:
        if not isinstance(row, dict):
            raise ReconciliationError("review-disposition row must be an object")
        candidate_id = row.get("candidate_id")
        if not isinstance(candidate_id, str) or re.fullmatch(r"FAR-LIT-[0-9A-F]{16}", candidate_id) is None:
            raise ReconciliationError(f"invalid reviewed candidate id: {candidate_id!r}")
        if candidate_id in result:
            raise ReconciliationError(f"duplicate reviewed candidate id: {candidate_id}")
        if row.get("disposition") not in ALLOWED_REVIEW_DISPOSITIONS:
            raise ReconciliationError(f"{candidate_id}: unknown review disposition")
        if row.get("suppress_from_core_claim_review_queue") is not True:
            raise ReconciliationError(f"{candidate_id}: reviewed row must explicitly suppress active queue")
        if not isinstance(row.get("source_key"), str) or not row["source_key"].strip():
            raise ReconciliationError(f"{candidate_id}: source_key required")
        if not isinstance(row.get("review_basis"), str) or not row["review_basis"].strip():
            raise ReconciliationError(f"{candidate_id}: review_basis required")
        result[candidate_id] = row
    return result


def exact_claim_inventory(claim_ledger: dict[str, Any], assurance: dict[str, Any]) -> tuple[list[dict[str, Any]], dict[str, list[str]]]:
    claims = claim_ledger.get("claims")
    assured = assurance.get("claims")
    if not isinstance(claims, list) or not isinstance(assured, list):
        raise ReconciliationError("claim ledgers malformed")
    by_id = {x.get("id"): x for x in assured if isinstance(x, dict) and isinstance(x.get("id"), str)}
    expected = [f"FAR-CORE-{n:03d}" for n in range(1, 15)]
    if [x.get("id") for x in claims] != expected:
        raise ReconciliationError("governing ledger must contain exact ordered FAR-CORE-001..014")
    inventory = []
    dependencies: dict[str, list[str]] = {}
    for claim in claims:
        cid = claim["id"]
        other = by_id.get(cid)
        if not other:
            raise ReconciliationError(f"assurance ledger missing {cid}")
        if claim.get("claim") != other.get("exact_statement"):
            raise ReconciliationError(f"{cid}: exact statement drift between governing and assurance ledgers")
        if claim.get("scope") not in str(other.get("scope", "")) and other.get("scope") not in str(claim.get("scope", "")):
            scope_relation = "TEXT_DIFF_REVIEWED_SEPARATELY"
        else:
            scope_relation = "TEXT_COMPATIBLE"
        deps = [d for d in other.get("dependencies", []) if isinstance(d, str)]
        dependencies[cid] = [d for d in deps if re.fullmatch(r"FAR-CORE-\d{3}", d)]
        inventory.append({
            "id": cid,
            "status": claim.get("status"),
            "scope": claim.get("scope"),
            "exact_statement": claim.get("claim"),
            "truth_disposition": other.get("truth_disposition"),
            "formalization_status": other.get("formalization_status"),
            "novelty_prior_art_status": other.get("novelty_prior_art_status"),
            "governance_status": other.get("governance_status"),
            "dependencies": deps,
            "scope_relation": scope_relation,
        })
    return inventory, dependencies


def reverse_graph(edges: dict[str, list[str]]) -> dict[str, list[str]]:
    result = {node: [] for node in edges}
    for node, deps in edges.items():
        for dep in deps:
            result.setdefault(dep, []).append(node)
    for node in result:
        result[node] = sorted(set(result[node]))
    return result


def transitive_dependents(start: str, reverse: dict[str, list[str]]) -> list[str]:
    seen: set[str] = set()
    stack = list(reverse.get(start, []))
    while stack:
        node = stack.pop()
        if node in seen:
            continue
        seen.add(node)
        stack.extend(reverse.get(node, []))
    return sorted(seen)


def rq_inventory(registry: dict[str, Any]) -> list[dict[str, Any]]:
    questions = registry.get("questions")
    if not isinstance(questions, list):
        raise ReconciliationError("RQ registry malformed")
    return [{
        "id": q.get("id"),
        "current_disposition": q.get("current_disposition"),
        "exact_question": q.get("exact_question"),
        "dependencies": q.get("dependencies", []),
        "relevant_workstream": q.get("relevant_workstream"),
    } for q in questions if isinstance(q, dict)]


def is_direct_core_threat_candidate(record: dict[str, Any]) -> bool:
    """Route exact counterexample alerts without silently dropping legacy ambiguity.

    Fully identified historical/foundational backfill remains research and prior-art material,
    but does not become a claim-reopening alert merely because its target set includes RQ-009.
    Older records or synthetic fixtures that lack both target and relation metadata are retained
    conservatively in the review queue until they can be classified.
    """
    bindings = record.get("discovery", {}).get("query_bindings", [])
    for binding in bindings:
        if not isinstance(binding, dict):
            continue
        if (
            binding.get("target_id") == CORE_THREAT_TARGET
            and binding.get("candidate_relation") == CORE_THREAT_RELATION
        ):
            return True
        if "target_id" not in binding and "candidate_relation" not in binding:
            return True
    return False


def candidate_queue(
    root: Path,
    reverse: dict[str, list[str]],
    review_dispositions: dict[str, dict[str, Any]] | None = None,
) -> tuple[list[dict[str, Any]], dict[str, int]]:
    queue: list[dict[str, Any]] = []
    reviewed = review_dispositions or {}
    counts = {
        "candidates": 0,
        "high_attention": 0,
        "claim_mapped": 0,
        "historical": 0,
        "philosophy_metaphysics_history": 0,
        "direct_core_threat": 0,
        "reviewed": 0,
        "review_required": 0,
    }
    for path in sorted((root / CANDIDATE_DIR).glob("FAR-LIT-*.json")):
        record = read_json(path)
        counts["candidates"] += 1
        candidate_id = record.get("candidate_id")
        triage = record.get("triage", {})
        attention = triage.get("attention_terms", []) if isinstance(triage, dict) else []
        claims = record.get("potential_claim_ids", [])
        lenses = set(triage.get("lenses", [])) if isinstance(triage, dict) else set()
        direct_core_threat = is_direct_core_threat_candidate(record)
        if attention:
            counts["high_attention"] += 1
        if claims:
            counts["claim_mapped"] += 1
        if direct_core_threat:
            counts["direct_core_threat"] += 1
        if candidate_id in reviewed:
            counts["reviewed"] += 1
        if any(
            isinstance(b, dict) and b.get("mode") == "historical_backfill"
            for b in record.get("discovery", {}).get("query_bindings", [])
        ):
            counts["historical"] += 1
        if lenses & {"philosophy_of_science", "formal_metaphysics", "history_of_logic", "historical_foundations"}:
            counts["philosophy_metaphysics_history"] += 1
        if attention and claims and direct_core_threat and candidate_id not in reviewed:
            fallout = sorted({
                dep for cid in claims if isinstance(cid, str)
                for dep in transitive_dependents(cid, reverse)
            })
            queue.append({
                "candidate_id": candidate_id,
                "claim_ids": claims,
                "downstream_claim_ids": fallout,
                "attention_terms": attention,
                "stage": "REVIEW_REQUIRED",
                "epistemic_status": "METADATA_SIGNAL_ONLY",
                "required_next_step": (
                    "Obtain and verify the primary source where available; reconstruct the exact "
                    "claim under the canonical FAR premises; attempt a reproducible counterexample "
                    "or derivation; if an exact contradiction survives, open the smallest governed "
                    "reopening/correction path. Do not infer contradiction from metadata."
                ),
            })
            counts["review_required"] += 1
    return queue, counts


def reconcile(root: Path) -> dict[str, Any]:
    surfaces = read_json(root / SURFACES_PATH)
    if surfaces.get("authority_boundary") != AUTHORITY_BOUNDARY:
        raise ReconciliationError("surface authority boundary drift")
    surface_rows = surfaces.get("surfaces")
    if not isinstance(surface_rows, list) or not surface_rows:
        raise ReconciliationError("repository-surfaces list missing")

    prior = read_json(root / STATE_PATH) if (root / STATE_PATH).exists() else {}
    prior_hashes = {
        row.get("path"): row.get("sha256")
        for row in prior.get("surfaces", [])
        if isinstance(row, dict) and isinstance(row.get("path"), str)
    }
    hashed = []
    missing = []
    changed = []
    for row in surface_rows:
        if not isinstance(row, dict) or not isinstance(row.get("path"), str):
            raise ReconciliationError("invalid surface record")
        path = root / row["path"]
        if not path.exists():
            missing.append(row["path"])
            continue
        digest = sha256_file(path)
        item = dict(row)
        item["sha256"] = digest
        item["changed_since_last_reconciliation"] = (
            row["path"] in prior_hashes and prior_hashes[row["path"]] != digest
        )
        if item["changed_since_last_reconciliation"]:
            changed.append(row["path"])
        hashed.append(item)
    if missing:
        raise ReconciliationError("missing canonical surfaces: " + ", ".join(missing))

    claim_ledger = read_json(root / CLAIM_LEDGER)
    assurance = read_json(root / ASSURANCE_LEDGER)
    rq = read_json(root / RQ_LEDGER)
    review_dispositions = load_review_dispositions(root)
    claims, deps = exact_claim_inventory(claim_ledger, assurance)
    reverse = reverse_graph(deps)
    impacts = {
        claim["id"]: {
            "direct_dependencies": deps.get(claim["id"], []),
            "downstream_claim_ids": transitive_dependents(claim["id"], reverse),
        }
        for claim in claims
    }
    queue, counts = candidate_queue(root, reverse, review_dispositions)
    state = {
        "schema_version": "1.0",
        "program_id": "FAR-LIVING-REPOSITORY-001",
        "authority": "Research",
        "authority_boundary": AUTHORITY_BOUNDARY,
        "canonical_theory_id": claim_ledger.get("theory_id"),
        "surface_count": len(hashed),
        "changed_surfaces": changed,
        "surfaces": hashed,
        "claims": claims,
        "claim_dependency_impact": impacts,
        "research_questions": rq_inventory(rq),
        "candidate_counts": counts,
        "review_disposition_count": len(review_dispositions),
        "core_claim_review_queue": queue,
        "rules": {
            "candidate_metadata_may_reopen_claim": False,
            "reproducible_exact_contradiction_may_trigger_reopening": True,
            "canonical_claim_change_requires_governed_lifecycle_and_protected_merge": True,
            "external_research_never_executes_efr_implicitly": True,
            "negative_search_never_establishes_novelty": True,
            "reviewed_candidates_remain_preserved_but_leave_active_queue": True,
            "historical_backfill_does_not_self_escalate_to_core_reopening_queue": True,
        },
    }
    write_json(root / STATE_PATH, state)

    lines = [
        "# Living Repository Status",
        "",
        "Status: **Research-derived reconciliation; never theory or evidence authority**",
        "",
        AUTHORITY_BOUNDARY,
        "",
        f"- Canonical theory: `{state['canonical_theory_id']}`",
        f"- Canonical surfaces tracked: **{state['surface_count']}**",
        f"- FAR-CORE claims reconciled: **{len(claims)}/14**",
        f"- Governed research questions indexed: **{len(state['research_questions'])}**",
        f"- Research candidates: **{counts['candidates']}**",
        f"- Historical-backfill candidates: **{counts['historical']}**",
        f"- Philosophy/metaphysics/history-lens candidates: **{counts['philosophy_metaphysics_history']}**",
        f"- High-attention metadata candidates: **{counts['high_attention']}**",
        f"- Direct core-threat candidates: **{counts['direct_core_threat']}**",
        f"- Canonically reviewed candidates present: **{counts['reviewed']}**",
        f"- Canonical review dispositions recorded: **{len(review_dispositions)}**",
        f"- Core-claim review queue: **{len(queue)}**",
        f"- Canonical surfaces changed since prior reconciliation: **{len(changed)}**",
        "",
        "## Claim-change rule",
        "",
        "The automation may identify a candidate that could affect a core claim and compute its downstream",
        "claim fallout. It may not rewrite the claim from metadata or model judgment. A canonical correction",
        "requires an exact reproducible contradiction (or another governance-authorized basis), replication,",
        "acceptance, promotion, and the protected merge path. Historical claim text remains recoverable in Git.",
        "Reviewed raw candidates remain preserved but are omitted from the active metadata review queue when",
        "their protected review disposition is recorded in the canonical review registry. Historical/foundational",
        "backfill remains research and prior-art material unless it also entered through the governed direct",
        "core-counterexample/theorem-threat lane.",
        "",
    ]
    (root / STATUS_PATH).parent.mkdir(parents=True, exist_ok=True)
    (root / STATUS_PATH).write_text("\n".join(lines), encoding="utf-8")
    return state


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    args = parser.parse_args()
    state = reconcile(Path(args.root))
    print(json.dumps({
        "surface_count": state["surface_count"],
        "claims": len(state["claims"]),
        "candidate_counts": state["candidate_counts"],
        "review_disposition_count": state["review_disposition_count"],
        "claim_review_queue": len(state["core_claim_review_queue"]),
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
