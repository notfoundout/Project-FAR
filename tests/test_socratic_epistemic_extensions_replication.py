from __future__ import annotations

import copy
import json
import unittest
from datetime import datetime
from pathlib import Path

from mechanization.far_mechanization.socratic_epistemic import validate_socratic_record

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures" / "socratic-epistemic-extensions"


def load(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text(encoding="utf-8"))


def parse_aware(value: object) -> datetime | None:
    if not isinstance(value, str) or not value:
        return None
    text = f"{value[:-1]}+00:00" if value.endswith(("Z", "z")) else value
    try:
        parsed = datetime.fromisoformat(text)
    except ValueError:
        return None
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        return None
    return parsed


def reference_expertise_assertion_accepts(document: dict) -> bool:
    record = document["record"]
    start = parse_aware(record["valid_from"])
    if start is None:
        return False
    end_value = record.get("valid_until")
    if end_value is None:
        return True
    end = parse_aware(end_value)
    return end is not None and end >= start


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
    seen: dict[str, str] = {}
    for category in categories:
        for entry in record[category]:
            statement = entry["statement"]
            previous = seen.get(statement)
            if previous is not None and previous != category:
                return False
            seen[statement] = category
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

    questions = {item["id"]: item for item in record["question_events"]}
    responses = {item["id"]: item for item in record["response_events"]}
    commitments = {item["id"]: item for item in record["commitments"]}
    commitment_ids = set(commitments)

    question_times: dict[str, datetime] = {}
    for question_id, question in questions.items():
        parsed = parse_aware(question["timestamp"])
        if parsed is None:
            return False
        question_times[question_id] = parsed

    response_times: dict[str, datetime] = {}
    for response_id, response in responses.items():
        question_id = response["question_id"]
        if question_id not in questions:
            return False
        response_time = parse_aware(response["timestamp"])
        if response_time is None or response_time < question_times[question_id]:
            return False
        response_times[response_id] = response_time

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

    for implication in record["derived_implications"]:
        premise_refs = implication["premise_refs"]
        if any(ref not in commitment_ids for ref in premise_refs):
            return False
        bridges: dict[str, str] = {}
        for bridge in implication["context_bridges"]:
            premise_ref = bridge["premise_ref"]
            if premise_ref not in premise_refs or premise_ref in bridges:
                return False
            bridges[premise_ref] = bridge["bridge"]
        for premise_ref in premise_refs:
            if commitments[premise_ref]["context"] != implication["context"] and premise_ref not in bridges:
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
        source_response_id = source["source_event_id"]
        if response_times[response_id] < response_times[source_response_id]:
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
        source_response_id = commitments[commitment_id]["source_event_id"]
        if response_times[response_id] < response_times[source_response_id]:
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

    def test_expertise_assertion_mutation_matrix(self) -> None:
        base = load("valid-expertise-assertion.json")
        cases = [base]

        malformed = copy.deepcopy(base)
        malformed["record"]["valid_from"] = "not-a-date"
        cases.append(malformed)

        naive = copy.deepcopy(base)
        naive["record"]["valid_from"] = "2026-09-23T00:00:00"
        cases.append(naive)

        inverted = copy.deepcopy(base)
        inverted["record"]["valid_until"] = "2026-09-22T23:59:59Z"
        cases.append(inverted)

        bounded = copy.deepcopy(base)
        bounded["record"]["valid_until"] = "2026-10-23T00:00:00Z"
        cases.append(bounded)

        for index, document in enumerate(cases):
            with self.subTest(case=index):
                self.assert_agreement(document, reference_expertise_assertion_accepts)

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

        same_category_duplicate = copy.deepcopy(base)
        same_category_duplicate["record"]["established"].append(
            copy.deepcopy(base["record"]["established"][0])
        )
        cases.append(same_category_duplicate)

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

        invalid_question_time = copy.deepcopy(base)
        invalid_question_time["record"]["question_events"][0]["timestamp"] = "not-a-date"
        cases.append(invalid_question_time)

        response_predates_question = copy.deepcopy(base)
        response_predates_question["record"]["response_events"][0]["timestamp"] = "2026-09-23T00:00:00Z"
        cases.append(response_predates_question)

        unknown_definition_ref = copy.deepcopy(base)
        unknown_definition_ref["record"]["definitions"][0]["commitment_refs"] = ["missing"]
        cases.append(unknown_definition_ref)

        unknown_tension_ref = copy.deepcopy(base)
        unknown_tension_ref["record"]["tensions"][0]["commitment_refs"] = ["c1", "missing"]
        cases.append(unknown_tension_ref)

        context_collapse = copy.deepcopy(base)
        context_collapse["record"]["commitments"][1]["context"] = "unrelated context"
        cases.append(context_collapse)

        context_bridge = copy.deepcopy(context_collapse)
        context_bridge["record"]["derived_implications"][0]["context_bridges"] = [{
            "premise_ref": "c2",
            "bridge": "Explicit test bridge.",
        }]
        cases.append(context_bridge)

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
