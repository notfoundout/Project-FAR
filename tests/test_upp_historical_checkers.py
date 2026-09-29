"""Historical POST-TUE-UPP-001 checkers stay executable against the frozen queue history.

Eleven of these checkers asserted the live queue tip and silently broke when the queue
advanced and was migrated to terminal fields; nothing ran them. This module runs every UPP
checker and pins the history semantics they now share through tools/upp_queue_history.py.
"""
from __future__ import annotations

import copy
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import upp_queue_history as history  # noqa: E402

QUEUE = json.loads((ROOT / "theory/evaluation/post-tue-universal-proof-queue-checkpoint-v1.0.json").read_text(encoding="utf-8"))
CHECKERS = sorted((ROOT / "tools").glob("check_upp_w*.py"))


class UppHistoricalCheckerTest(unittest.TestCase):
    def test_all_fifteen_workstream_checkers_are_present(self):
        self.assertEqual(15, len(CHECKERS))

    def test_every_upp_checker_passes_on_the_frozen_queue(self):
        failures = {}
        for path in CHECKERS:
            completed = subprocess.run([sys.executable, str(path.relative_to(ROOT))], cwd=ROOT, capture_output=True, text=True, timeout=300)
            if completed.returncode != 0:
                failures[path.name] = (completed.stdout + completed.stderr)[-400:]
        self.assertEqual({}, failures)


class QueueHistoryTest(unittest.TestCase):
    def test_frozen_queue_is_contiguous_and_terminally_closed(self):
        self.assertTrue(history.history_contiguous(QUEUE))
        self.assertTrue(history.terminally_closed(QUEUE))
        self.assertIs(True, history.public_evaluation_authorized(QUEUE))

    def test_successor_is_read_from_history(self):
        self.assertTrue(history.successor_recorded(QUEUE, 290, "UPP-W9-DEPENDENCY-STRUCTURE"))
        self.assertFalse(history.successor_recorded(QUEUE, 290, "UPP-W10-SEMANTIC-INTERPRETATION"))

    def test_successor_falls_back_to_live_next_action(self):
        live = {"completed_workstreams": QUEUE["completed_workstreams"][:3], "next_action": {"target_pr": 284, "workstream": "UPP-W3-CONTRACT"}}
        self.assertTrue(history.successor_recorded(live, 284, "UPP-W3-CONTRACT"))
        self.assertFalse(history.successor_recorded(live, 285, "UPP-W4-REPRESENTATIONS"))

    def test_gap_in_history_is_rejected(self):
        queue = copy.deepcopy(QUEUE)
        del queue["completed_workstreams"][8]
        self.assertFalse(history.history_contiguous(queue))

    def test_followup_before_completed_history_is_rejected(self):
        queue = copy.deepcopy(QUEUE)
        queue["ordered_followups"] = [290]
        self.assertFalse(history.history_contiguous(queue))

    def test_reopened_terminal_queue_is_not_closed(self):
        for field, value in (("terminal_next_action", {"target_pr": 297, "workstream": "UPP-W16"}), ("terminal_ordered_followups", [297]), ("status", "active")):
            queue = copy.deepcopy(QUEUE)
            queue[field] = value
            self.assertFalse(history.terminally_closed(queue), field)

    def test_pre_migration_queue_uses_legacy_fields(self):
        legacy = {"status": "complete", "next_action": None, "ordered_followups": [], "public_evaluation_authorized": True}
        self.assertTrue(history.terminally_closed(legacy))
        self.assertIs(True, history.public_evaluation_authorized(legacy))


if __name__ == "__main__":
    unittest.main()
