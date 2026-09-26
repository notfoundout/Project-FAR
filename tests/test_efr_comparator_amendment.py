"""EFR-001 comparator amendment v2.0: preserved history, real comparator, fail-closed tooling.

These tests enforce that the v1.0 preregistration stays byte-identical, that the confounded
HD1/U1/C1 tests are superseded rather than executed, that the comparator is genuinely generic
and reaches the same classification as the FAR verifier, and that the v2.0 allocation/analysis
tools reject v1.0 inputs and cannot manufacture a FAR-specific benefit from missing FAR data.
"""
from __future__ import annotations

import ast
import copy
import hashlib
import json
import subprocess
import unittest
from collections import Counter
from itertools import combinations
from pathlib import Path

from mechanization.far_mechanization.contract_v2 import validate_contract as validate_baseline
from mechanization.far_mechanization.contract_v2_strict import (
    canonical_json,
    contract_sha256,
    validate_contract,
)
from tools import efr_generic_collision_checker as checker
from tools.efr_hd2_allocation import ARMS, ARM_ORDERS, CLASSES, DOMAINS, allocate
from tools.efr_hd2_analysis import analyze, contrasts, prepare, rates
from tools import efr_u2_analysis as u2

ROOT = Path(__file__).resolve().parents[1]
AUTHORITY = ROOT / "theory/evaluation/external-falsification-and-replication-comparator-amendment-v2.0.json"
V1_PROGRAM = ROOT / "theory/evaluation/external-falsification-and-replication-program-v1.0.json"
V1_FREEZE = ROOT / "theory/evaluation/external-falsification-and-replication-input-freeze-v1.0.json"
RECORDS = sorted((ROOT / "research/results/pca-w4-domain-contracts").glob("*-lossy.json")) + sorted(
    (ROOT / "research/results/pca-w4-domain-contracts").glob("*-repaired.json")
) + sorted((ROOT / "conformance/far-ir-2.0").glob("valid-*.json"))


def blob(path: str) -> str:
    return subprocess.run(["git", "hash-object", path], cwd=ROOT, check=True, capture_output=True, text=True).stdout.strip()


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def candidate_projection(record: dict) -> dict:
    """The v1.0 U1/H1 uniform candidate: first source case per representation value, checked."""
    document = copy.deepcopy(record)
    contract = document["contract"]
    behavior = {row["case_id"]: row["value"] for row in contract["required_behavior"]["table"]}
    decoder: dict[str, dict] = {}
    for row in sorted(contract["representation"]["table"], key=lambda r: r["case_id"]):
        decoder.setdefault(canonical_json(row["value"]), {"representation_value": row["value"],
                                                          "behavior_value": behavior[row["case_id"]]})
    document["report"] = {"outcome": "PROVED", "failure_report": [], "evidence": {
        "kind": "factorization", "status": "CHECKED_FINITE_EXPLICIT",
        "decoder_table": [decoder[key] for key in sorted(decoder)]}}
    document["freeze"]["contract_sha256"] = contract_sha256(contract)
    return document


def tables(record: dict) -> dict:
    contract = record["contract"]
    return {"representation": contract["representation"]["table"],
            "required_behavior": contract["required_behavior"]["table"]}


class PreservationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.authority = load(AUTHORITY)

    def test_v1_objects_are_byte_identical(self) -> None:
        paths = {item["path"] for item in self.authority["preserved_objects"]}
        for item in load(V1_FREEZE)["artifact_objects"]:
            self.assertIn(item["path"], paths)
        for item in self.authority["preserved_objects"]:
            with self.subTest(path=item["path"]):
                self.assertEqual(blob(item["path"]), item["git_blob_sha"])

    def test_bound_v2_artifacts_are_frozen(self) -> None:
        for item in self.authority["bound_artifacts"]:
            with self.subTest(path=item["path"]):
                self.assertEqual(blob(item["path"]), item["git_blob_sha"])

    def test_v1_program_was_never_executed(self) -> None:
        program = load(V1_PROGRAM)
        self.assertEqual({t["status"] for t in program["tests"]}, {"PREREGISTERED_NOT_EXECUTED"})
        results = load(V1_FREEZE)["current_results"]
        for key in ("tests_executed", "external_cases", "human_participants", "field_sites"):
            self.assertEqual(results[key], 0, key)
        for slot in load(V1_FREEZE)["external_input_slots"]:
            self.assertEqual(slot["state"], "EMPTY_AWAITING_INDEPENDENT_CUSTODIAN_SEAL", slot["test_id"])
        self.assertEqual(self.authority["current_results"],
                         {"tests_executed": 0, "external_cases": 0, "participants": 0, "sites": 0})

    def test_exactly_the_confounded_tests_are_superseded(self) -> None:
        v1_ids = {t["id"] for t in load(V1_PROGRAM)["tests"]}
        superseded = self.authority["superseded_tests"]
        self.assertEqual(superseded, {k: "SUPERSEDED_NOT_EXECUTABLE" for k in ("EFR-HD1", "EFR-U1", "EFR-C1")})
        replacements = {t["id"]: t["replaces"] for t in self.authority["replacement_tests"]}
        self.assertEqual(replacements, {"EFR-HD2": "EFR-HD1", "EFR-U2": "EFR-U1", "EFR-C2": "EFR-C1"})
        self.assertEqual(set(self.authority["unamended_tests"]) | set(superseded), v1_ids)
        for test in self.authority["replacement_tests"]:
            self.assertEqual(test["status"], "PREREGISTERED_NOT_EXECUTED")
        self.assertIn("EFR-HD2", self.authority["aggregate_rule"])
        self.assertNotIn("EFR-HD1", self.authority["aggregate_rule"])

    def test_primary_contrasts_are_far_versus_checker(self) -> None:
        for test in self.authority["replacement_tests"][:2]:
            self.assertIn("checker minus far", test["primary_contrast"])
            self.assertEqual(test["arms"], ["far", "checker", "standard"])


class ComparatorTests(unittest.TestCase):
    FAR_TERMS = ("far", "factoriz", "decoder", "contract", "quotient", "proved", "refuted", "collision",
                 "sufficien", "verifier", "witness", "kernel")

    def test_checker_imports_only_the_standard_library(self) -> None:
        tree = ast.parse((ROOT / "tools/efr_generic_collision_checker.py").read_text(encoding="utf-8"))
        imported = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imported |= {alias.name.split(".")[0] for alias in node.names}
            elif isinstance(node, ast.ImportFrom):
                imported.add((node.module or "").split(".")[0])
        self.assertEqual(imported, {"__future__", "json", "sys", "itertools", "pathlib"})

    def test_rendered_report_uses_no_project_far_terminology(self) -> None:
        for path in RECORDS:
            with self.subTest(record=path.name):
                text = checker.render(checker.check(tables(load(path)))).lower()
                for term in self.FAR_TERMS:
                    self.assertNotIn(term, text)

    def test_checker_matches_far_classification_on_every_record(self) -> None:
        self.assertGreaterEqual(len(RECORDS), 15)
        for path in RECORDS:
            with self.subTest(record=path.name):
                record = load(path)
                consistent = checker.check(tables(record))["result"] == "CONSISTENT"
                projected = candidate_projection(record)
                self.assertEqual(validate_contract(projected).success, consistent)

    def test_checker_lists_every_conflicting_pair(self) -> None:
        result = checker.check({
            "representation": [{"case_id": c, "value": 0} for c in ("a", "b", "c")],
            "required_behavior": [{"case_id": "a", "value": 1}, {"case_id": "b", "value": 2},
                                  {"case_id": "c", "value": 1}],
        })
        self.assertEqual(result["result"], "INCONSISTENT")
        self.assertEqual([(p["case_a"], p["case_b"]) for p in result["conflicting_pairs"]], [("a", "b"), ("b", "c")])

    def test_checker_rejects_malformed_tables(self) -> None:
        bad_inputs = [
            {"representation": [{"case_id": "a", "value": 0}], "required_behavior": [{"case_id": "b", "value": 0}]},
            {"representation": [{"case_id": "a", "value": 0}, {"case_id": "a", "value": 1}],
             "required_behavior": [{"case_id": "a", "value": 0}]},
            {"representation": [], "required_behavior": []},
            {"representation": [{"case_id": "a"}], "required_behavior": [{"case_id": "a", "value": 0}]},
        ]
        for bad in bad_inputs:
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                checker.check(bad)


class H1A1ExecutionBindingTests(unittest.TestCase):
    def test_strict_equals_baseline_on_every_checked_candidate(self) -> None:
        for path in RECORDS:
            with self.subTest(record=path.name):
                projected = candidate_projection(load(path))
                strict = [(d.code, d.message) for d in validate_contract(projected).diagnostics]
                baseline = [(d.code, d.message) for d in validate_baseline(projected).diagnostics]
                self.assertEqual(strict, baseline)


def hd2_fixture(far_errors: int = 0, checker_errors: int = 0, missing_far: int = 0):
    data = {"test_id": "EFR-HD2", "reviewers": [f"R{i:02}" for i in range(60)], "cases": [
        {"id": f"C{d:02}{k}{i:02}", "domain": domain, "class": label}
        for d, domain in enumerate(DOMAINS) for k, label in enumerate(CLASSES) for i in range(10)]}
    raw = json.dumps(data).encode()
    digest = hashlib.sha256(raw).hexdigest()
    labels = {c["id"]: c["class"] for c in data["cases"]}
    flip = {"material_loss": "preservation", "preservation": "material_loss"}
    counters = Counter()
    ratings = []
    for row in allocate(raw, digest)["allocation"]:
        for arm, tasks in row["tasks"].items():
            for case in tasks:
                answer = labels[case]
                if arm == "far" and counters["far_missing"] < missing_far:
                    counters["far_missing"] += 1
                    answer = None
                elif arm == "far" and counters["far"] < far_errors:
                    counters["far"] += 1
                    answer = flip[answer]
                elif arm == "checker" and counters["checker"] < checker_errors:
                    counters["checker"] += 1
                    answer = flip[answer]
                ratings.append({"reviewer_id": row["reviewer_id"], "case_id": case, "arm": arm, "decision": answer})
    output = json.dumps({"input_manifest_sha256": digest, "ratings": ratings}).encode()
    return raw, digest, output, hashlib.sha256(output).hexdigest()


class HD2Tests(unittest.TestCase):
    def test_allocation_is_balanced_disjoint_and_counterbalanced(self) -> None:
        raw, digest, _, _ = hd2_fixture()
        rows = allocate(raw, digest)["allocation"]
        per_case_arm = Counter()
        for row in rows:
            seen = []
            for arm in ARMS:
                self.assertEqual(len(row["tasks"][arm]), 12)
                seen.extend(row["tasks"][arm])
                per_case_arm.update((case, arm) for case in row["tasks"][arm])
            self.assertEqual(len(seen), 36)
            self.assertEqual(len(set(seen)), 36)
        self.assertEqual(set(per_case_arm.values()), {6})
        self.assertEqual(len(per_case_arm), 360)
        orders = Counter(tuple(row["arm_order"]) for row in rows)
        self.assertEqual(set(orders), set(ARM_ORDERS))
        self.assertEqual(set(orders.values()), {10})

    def test_v1_manifest_and_tampering_are_rejected(self) -> None:
        raw, digest, _, _ = hd2_fixture()
        v1 = json.loads(raw)
        del v1["test_id"]
        v1_raw = json.dumps(v1).encode()
        with self.assertRaisesRegex(ValueError, "EFR-HD2"):
            allocate(v1_raw, hashlib.sha256(v1_raw).hexdigest())
        with self.assertRaisesRegex(ValueError, "digest mismatch"):
            allocate(raw + b" ", digest)

    def test_equal_far_and_checker_performance_fails_even_when_standard_is_worse(self) -> None:
        result = analyze(*hd2_fixture())
        self.assertEqual(result["resamples"], 10000)
        self.assertEqual(result["primary"]["far_specific_disagreement_reduction"], "0")
        self.assertEqual(result["numerical_disposition"], "NUMERICAL_GATES_FAIL")

    def test_far_specific_benefit_is_detectable(self) -> None:
        data, groups, _ = prepare(*hd2_fixture(checker_errors=300))
        observed = contrasts(*rates(groups, {c["id"]: 1 for c in data["cases"]}, {r: 1 for r in data["reviewers"]}))
        self.assertGreater(observed[0], 0)

    def test_missing_far_ratings_cannot_create_a_far_specific_benefit(self) -> None:
        data, groups, missing = prepare(*hd2_fixture(missing_far=60))
        self.assertEqual(missing["far"], 60)
        observed = contrasts(*rates(groups, {c["id"]: 1 for c in data["cases"]}, {r: 1 for r in data["reviewers"]}))
        self.assertLess(observed[0], 0)
        self.assertGreater(observed[1], 0)

    def test_excess_missingness_is_invalid(self) -> None:
        result = analyze(*hd2_fixture(missing_far=200))
        self.assertEqual(result["numerical_disposition"], "INVALID_MISSINGNESS")


def u2_fixture(outcome):
    sites = {}
    for site in u2.SITES:
        workers = [f"{site}-W{i:03d}" for i in range(1, 21)]
        sites[site] = {"workers": workers, "assignments": {
            f"{site}-{i:03d}": workers[(i - 1) % len(workers)] for i in range(1, 61)}}
    raw = json.dumps({"test_id": "EFR-U2", "sites": sites}).encode()
    digest = hashlib.sha256(raw).hexdigest()
    allocation = u2.allocate(raw, digest)["allocation"]
    rows = [{"id": case, "escaped_defect": outcome(arm, case)} for site in u2.SITES for case, arm in allocation[site].items()]
    out = json.dumps({"roster_manifest_sha256": digest, "investigations": rows}).encode()
    return raw, digest, out, hashlib.sha256(out).hexdigest()


class U2Tests(unittest.TestCase):
    def test_allocation_is_twenty_per_arm_per_site(self) -> None:
        raw, digest, _, _ = u2_fixture(lambda arm, case: False)
        allocation = u2.allocate(raw, digest)["allocation"]
        for site in u2.SITES:
            self.assertEqual(Counter(allocation[site].values()), {arm: 20 for arm in u2.ARMS})

    def test_v1_roster_and_bad_assignment_are_rejected(self) -> None:
        raw, digest, _, _ = u2_fixture(lambda arm, case: False)
        data = json.loads(raw)
        data["test_id"] = "EFR-U1"
        changed = json.dumps(data).encode()
        with self.assertRaisesRegex(ValueError, "EFR-U2"):
            u2.allocate(changed, hashlib.sha256(changed).hexdigest())
        data["test_id"] = "EFR-U2"
        data["sites"]["S01"]["assignments"]["S01-001"] = "S01-W002"
        changed = json.dumps(data).encode()
        with self.assertRaisesRegex(ValueError, "cyclic"):
            u2.allocate(changed, hashlib.sha256(changed).hexdigest())

    def test_zero_denominator_resolves_against_far_not_invalid(self) -> None:
        self.assertEqual(u2._conservative(None, "far"), 1)
        self.assertEqual(u2._conservative(None, "checker"), 0)
        self.assertEqual(u2._conservative(None, "standard"), 0)
        few = {}
        for site in u2.SITES:
            workers = [f"{site}-W{i:03d}" for i in range(1, 3)]
            few[site] = {"workers": workers, "assignments": {
                f"{site}-{i:03d}": workers[(i - 1) % 2] for i in range(1, 61)}}
        raw = json.dumps({"test_id": "EFR-U2", "sites": few}).encode()
        digest = hashlib.sha256(raw).hexdigest()
        allocation = u2.allocate(raw, digest)["allocation"]
        rows = [{"id": c, "escaped_defect": False} for s in u2.SITES for c in allocation[s]]
        out = json.dumps({"roster_manifest_sha256": digest, "investigations": rows}).encode()
        result = u2.analyze(raw, digest, out, hashlib.sha256(out).hexdigest())
        self.assertIn(result["numerical_disposition"], ("NUMERICAL_GATES_FAIL",))
        self.assertIn("zero_denominator_resamples", result)

    def test_equal_far_and_checker_fails_and_missing_far_counts_against_far(self) -> None:
        equal = u2.analyze(*u2_fixture(lambda arm, case: arm == "standard"))
        self.assertEqual(equal["primary"]["far_specific_escaped_defect_reduction"], "0")
        self.assertEqual(equal["numerical_disposition"], "NUMERICAL_GATES_FAIL")
        missing = u2.analyze(*u2_fixture(lambda arm, case: None))
        self.assertEqual(missing["primary"]["far_specific_escaped_defect_reduction"], "-1")
        self.assertEqual(missing["numerical_disposition"], "NUMERICAL_GATES_FAIL")


if __name__ == "__main__":
    unittest.main()
