from __future__ import annotations

import copy
import json
import unittest
from datetime import datetime
from pathlib import Path

from mechanization.far_mechanization.socratic_epistemic import validate_socratic_record

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests" / "fixtures" / "socratic-epistemic-extensions" / "valid-elenchus-session.json"


def load_fixture() -> dict:
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


def parse_aware(value: str) -> datetime:
    normalized = f"{value[:-1]}+00:00" if value.endswith(("Z", "z")) else value
    parsed = datetime.fromisoformat(normalized)
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        raise ValueError("timestamp is not timezone-aware")
    return parsed


def reference_lifecycle_chronology_accepts(document: dict) -> bool:
    """Independent oracle for lifecycle-event chronology only."""
    record = document["record"]
    response_times = {
        item["id"]: parse_aware(item["timestamp"])
        for item in record["response_events"]
    }
    commitments = {item["id"]: item for item in record["commitments"]}

    for revision in record["revisions"]:
        source = commitments[revision["from_commitment_id"]]
        if response_times[revision["response_event_id"]] < response_times[source["source_event_id"]]:
            return False

    for withdrawal in record["withdrawals"]:
        commitment = commitments[withdrawal["commitment_id"]]
        if response_times[withdrawal["response_event_id"]] < response_times[commitment["source_event_id"]]:
            return False

    return True


def diagnostic_codes(document: dict) -> set[str]:
    return {item.code for item in validate_socratic_record(document).diagnostics}


class ElenchusLifecycleChronologyTests(unittest.TestCase):
    def test_valid_fixture_satisfies_independent_chronology_oracle(self) -> None:
        document = load_fixture()
        self.assertTrue(reference_lifecycle_chronology_accepts(document))
        self.assertTrue(validate_socratic_record(document).success)

    def test_revision_cannot_predate_source_commitment(self) -> None:
        document = load_fixture()
        document["record"]["question_events"][2]["timestamp"] = "2026-09-23T00:00:00Z"
        document["record"]["response_events"][2]["timestamp"] = "2026-09-23T00:00:00Z"

        self.assertFalse(reference_lifecycle_chronology_accepts(document))
        self.assertIn(
            "ELENCHUS_REVISION_PREDATES_SOURCE_COMMITMENT",
            diagnostic_codes(document),
        )

    def test_withdrawal_cannot_predate_commitment(self) -> None:
        document = load_fixture()
        document["record"]["commitments"][1]["status"] = "WITHDRAWN"
        document["record"]["withdrawals"] = [{
            "commitment_id": "c2",
            "response_event_id": "r1",
            "reason": "Artificial chronology mutation.",
        }]

        self.assertFalse(reference_lifecycle_chronology_accepts(document))
        self.assertIn(
            "ELENCHUS_WITHDRAWAL_PREDATES_COMMITMENT",
            diagnostic_codes(document),
        )

    def test_lifecycle_event_at_same_time_as_source_is_allowed(self) -> None:
        document = load_fixture()
        document["record"]["question_events"][2]["timestamp"] = "2026-09-23T00:00:02Z"
        document["record"]["response_events"][2]["timestamp"] = "2026-09-23T00:00:02Z"

        self.assertTrue(reference_lifecycle_chronology_accepts(document))
        self.assertNotIn(
            "ELENCHUS_REVISION_PREDATES_SOURCE_COMMITMENT",
            diagnostic_codes(document),
        )


if __name__ == "__main__":
    unittest.main()
