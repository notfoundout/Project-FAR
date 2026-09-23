from __future__ import annotations

import copy
import json
import unittest
from pathlib import Path

from mechanization.far_mechanization.socratic_epistemic import validate_socratic_record

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures" / "socratic-epistemic-extensions"


def load(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def reference_expertise_accepts(document: dict) -> bool:
    """Independent table-only oracle for the scope-transfer invariant."""
    record = document["record"]
    expertise = record["expertise_scope"]
    claim = record["claim_scope"]
    dimensions = record["dimensions"]
    for name in ("domain", "subdomain", "claim_type", "population", "geography", "time", "method"):
        expected_expertise = expertise.get(name)
        expected_claim = claim.get(name)
        item = dimensions[name]
        if item["expertise_value"] != expected_expertise or item["claim_value"] != expected_claim:
            return False
        if item["status"] == "MATCH" and expected_expertise != expected_claim and not item.get("bridge"):
            return False
        if item["status"] == "NOT_APPLICABLE" and name != "subdomain":
            return False
        if name == "subdomain" and item["status"] == "NOT_APPLICABLE" and (
            expected_expertise is not None or expected_claim is not None
        ):
            return False
    if record["status"] == "SUPPORTED":
        return all(item["status"] in {"MATCH", "NOT_APPLICABLE"} for item in dimensions.values())
    return True


def reference_boundary_accepts(document: dict) -> bool:
    """Independent oracle for category exclusivity and closure linkage."""
    record = document["record"]
    categories = (
        "established",
        "conditionally_established",
        "supported_not_established",
        "unknown",
        "not_investigated",
        "not_identifiable_from_current_evidence",
        "explicit_nonclaims",
    )
    seen: set[str] = set()
    for category in categories:
        for entry in record[category]:
            statement = entry["statement"]
            if statement in seen:
                return False
            seen.add(statement)
    if record["closure_status"] in {"Resolved", "Provisionally resolved"} and not record["closure_record_refs"]:
        return False
    return True


def _unique_ids(entries: list[dict]) -> bool:
    ids = [item["id"] for item in entries]
    return len(ids) == len(set(ids))


def _refs_exist(entries: list[dict], field: str, known: set[str]) -> bool:
    return all(all(ref in known for ref in item[field]) for item in entries)


def reference_elenchus_accepts(document: dict) -> bool:
    """Independent oracle for elicited-record provenance and revision history."""
    record = document["record"]
    id_lists = (
        record["question_events"],
        record["response_events"],
        record["commitments"],
        record["definitions"],
        record["assumptions"],
        record["warrants"],
        record["derived_implications"],
        record["tensions"],
        record["contradictions"],
    )
    if any(not _unique_ids(entries) for entries in id_lists):
        return False

    questions = {item["id"] for item in record["question_events"]}
    responses = {item["id"]: item for item in record["response_events"]}
    commitments = {item["id"]: item for item in record["commitments"]}
    commitment_ids = set(commitments)

    if any(item["question_id"] not in questions for item in responses.values()):
        return False
    if any(item["source_event_id"] not in responses for item in commitments.values()):
        return False
    if not _refs_exist(record["definitions"], "commitment_refs", commitment_ids):
        return False
    if not _refs_exist(record["assumptions"], "commitment_refs", commitment_ids):
        return False
    if not _refs_exist(record["warrants"], "commitment_refs", commitment_ids):
        return False
    if not _refs_exist(record["tensions"], "commitment_refs", commitment_ids):
        return False
    if not _refs_exist(record["contradictions"], "commitment_refs", commitment_ids):
        return False
    if any(any(ref not in commitment_ids for ref in item["premise_refs"]) for item in record["derived_implications"]):
        return False

    revision_sources: set[str] = set()
    revision_targets: set[str] = set()
    for revision in record["revisions"]:
        source_id = revision["from_commitment_id"]
        target_id = revision["to_commitment_id"]
        response_id = revision["response_event_id"]
        if source_id in revision_sources or target_id in revision_targets:
            return False
        revision_sources.add(source_id)
        revision_targets.add(target_id)
        if source_id not in commitments or target_id not in commitments or source_id == target_id:
            return False
        source = commitments[source_id]
        target = commitments[target_id]
        if source["status"] != "REVISED" or target["version"] <= source["version"]:
            return False
        if response_id not in responses or target["source_event_id"] != response_id:
            return False

    withdrawal_ids: set[str] = set()
    for withdrawal in record["withdrawals"]:
        commitment_id = withdrawal["commitment_id"]
        response_id = withdrawal["response_event_id"]
        if commitment_id in withdrawal_ids:
            return False
        withdrawal_ids.add(commitment_id)
        if commitment_id not in commitments:
            return False
        if commitments[commitment_id]["status"] != "WITHDRAWN":
            return False
        if response_id not in responses:
            return False

    for commitment_id, commitment in commitments.items():
        if commitment["status"] == "REVISED" and commitment_id not in revision_sources:
            return False
        if commitment["status"] == "WITHDRAWN" and commitment_id not in withdrawal_ids:
            return False

    for contradiction in record["contradictions"]:
        if len(set(contradiction["commitment_refs"])) < 2:
            return False
        if not contradiction.get("interpretation") or not contradiction.get("calculus") or not contradiction.get("basis"):
            return False
    return True


class SocraticEpistemicReplicationTests(unittest.TestCase):
    def assert_agreement(self, document: dict, oracle) -> None:
        expected = oracle(document)
        result = validate_socratic_record(document)
        observed = result.success
        self.assertEqual(observed, expected, result.diagnostics)

    def test_expertise_mutation_matrix(self) -> None:
        base = load("valid-expertise-applicability.json")
        cases = [base]

        cross_domain_match = copy.deepcopy(base)
        cross_domain_match["record"]["claim_scope"]["domain"] = "economics"
        cross_domain_match["record"]["dimensions"]["domain"]["claim_value"] = "economics"
        cases.append(cross_domain_match)

        supported_mismatch = copy.deepcopy(base)
        supported_mismatch["record"]["claim_scope"]["method"] = "survey analysis"
        supported_mismatch["record"]["dimensions"]["method"]["claim_value"] = "survey analysis"
        supported_mismatch["record"]["dimensions"]["method"]["status"] = "MISMATCH"
        cases.append(supported_mismatch)

        stale_dimension = copy.deepcopy(base)
        stale_dimension["record"]["dimensions"]["time"]["claim_value"] = "historical"
        cases.append(stale_dimension)

        for index, document in enumerate(cases):
            with self.subTest(case=index):
                self.assert_agreement(document, reference_expertise_accepts)

    def test_boundary_mutation_matrix(self) -> None:
        base = load("valid-epistemic-boundary.json")
        cases = [base]

        collision = copy.deepcopy(base)
        collision["record"]["unknown"].append({
            "statement": base["record"]["established"][0]["statement"],
            "basis_refs": ["closure.example.1"],
            "reason": "mutation",
        })
        cases.append(collision)

        no_closure = copy.deepcopy(base)
        no_closure["record"]["closure_record_refs"] = []
        cases.append(no_closure)

        for index, document in enumerate(cases):
            with self.subTest(case=index):
                self.assert_agreement(document, reference_boundary_accepts)

    def test_elenchus_mutation_matrix(self) -> None:
        base = load("valid-elenchus-session.json")
        cases = [base]

        unknown_question = copy.deepcopy(base)
        unknown_question["record"]["response_events"][0]["question_id"] = "missing"
        cases.append(unknown_question)

        unknown_definition_ref = copy.deepcopy(base)
        unknown_definition_ref["record"]["definitions"][0]["commitment_refs"] = ["missing"]
        cases.append(unknown_definition_ref)

        unknown_tension_ref = copy.deepcopy(base)
        unknown_tension_ref["record"]["tensions"][0]["commitment_refs"] = ["c1", "missing"]
        cases.append(unknown_tension_ref)

        overwritten_revision = copy.deepcopy(base)
        overwritten_revision["record"]["revisions"][0]["to_commitment_id"] = "c1"
        cases.append(overwritten_revision)

        bad_version = copy.deepcopy(base)
        bad_version["record"]["commitments"][2]["version"] = 1
        cases.append(bad_version)

        missing_revision = copy.deepcopy(base)
        missing_revision["record"]["revisions"] = []
        cases.append(missing_revision)

        mismatched_revision_response = copy.deepcopy(base)
        mismatched_revision_response["record"]["revisions"][0]["response_event_id"] = "r2"
        cases.append(mismatched_revision_response)

        missing_withdrawal = copy.deepcopy(base)
        missing_withdrawal["record"]["commitments"][1]["status"] = "WITHDRAWN"
        cases.append(missing_withdrawal)

        forked_revision = copy.deepcopy(base)
        forked_revision["record"]["commitments"].append({
            "id": "c4",
            "statement": "Alternative replacement definition.",
            "version": 3,
            "status": "ACTIVE",
            "source_event_id": "r3",
            "context": "definition of reliable testimony",
        })
        forked_revision["record"]["revisions"].append({
            "from_commitment_id": "c1",
            "to_commitment_id": "c4",
            "response_event_id": "r3",
            "reason": "Artificial fork mutation.",
        })
        cases.append(forked_revision)

        for index, document in enumerate(cases):
            with self.subTest(case=index):
                self.assert_agreement(document, reference_elenchus_accepts)


if __name__ == "__main__":
    unittest.main()
