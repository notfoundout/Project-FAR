"""Synthetic scheduling fixtures, not EFR study participants or observations."""
import collections
import copy
import hashlib
import json
import unittest

from tools.efr_hd1_allocation import allocate, DOMAINS, CLASSES


class EfrHD1AllocationTests(unittest.TestCase):
    def inputs(self):
        reviewers = [f"synthetic-reviewer-{i:02}" for i in range(24)]
        cases = [{"id": f"synthetic-{d}-{c}-{i:02}", "domain": d, "class": c}
                 for d in DOMAINS for c in CLASSES for i in range(10)]
        return reviewers, cases

    def seal(self, reviewers, cases):
        raw = json.dumps({"reviewers": reviewers, "cases": cases}, sort_keys=True).encode()
        return raw, hashlib.sha256(raw).hexdigest()

    def test_every_case_has_six_ratings_per_arm_without_reviewer_repeats(self):
        reviewers, cases = self.inputs()
        result = allocate(*self.seal(reviewers, cases))
        counts = {arm: collections.Counter() for arm in ("far", "standard")}
        first = collections.Counter()
        for row in result["allocation"]:
            tasks = row["tasks"]
            self.assertEqual(len(tasks["far"]), 30)
            self.assertEqual(len(tasks["standard"]), 30)
            self.assertTrue(set(tasks["far"]).isdisjoint(tasks["standard"]))
            first[row["arm_order"][0]] += 1
            for arm in counts:
                counts[arm].update(tasks[arm])
        self.assertEqual(first, {"far": 12, "standard": 12})
        expected = {case["id"]: 6 for case in cases}
        self.assertEqual(dict(counts["far"]), expected)
        self.assertEqual(dict(counts["standard"]), expected)

    def test_input_order_cannot_change_roster_or_task_sequence(self):
        reviewers, cases = self.inputs()
        raw, digest = self.seal(reviewers, cases)
        self.assertEqual(allocate(raw, digest), allocate(raw, digest))
        reordered, _ = self.seal(list(reversed(reviewers)), list(reversed(cases)))
        with self.assertRaisesRegex(ValueError, "digest mismatch"):
            allocate(reordered, digest)

    def test_equal_count_metadata_swap_cannot_reuse_sealed_identity(self):
        reviewers, cases = self.inputs()
        raw, digest = self.seal(reviewers, cases)
        changed = copy.deepcopy(cases)
        changed[0]["class"], changed[10]["class"] = changed[10]["class"], changed[0]["class"]
        tampered, _ = self.seal(reviewers, changed)
        with self.assertRaisesRegex(ValueError, "digest mismatch"):
            allocate(tampered, digest)
        self.assertEqual(allocate(raw, digest)["input_manifest_sha256"], digest)

    def test_bad_seal_duplicates_and_stratum_changes_fail_closed(self):
        reviewers, cases = self.inputs()
        variants = [
            (self.seal(reviewers, cases)[0], "bad"),
            self.seal(reviewers[:-1] + [reviewers[0]], cases),
            self.seal(reviewers, cases[:-1] + [cases[0]]),
        ]
        changed = copy.deepcopy(cases)
        changed[0]["class"] = "preservation"
        variants.append(self.seal(reviewers, changed))
        for variant in variants:
            with self.assertRaises(ValueError):
                allocate(*variant)


if __name__ == "__main__":
    unittest.main()
