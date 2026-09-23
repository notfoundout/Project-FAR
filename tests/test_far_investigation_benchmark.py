import importlib.util
import json
import math
import pathlib
import subprocess
import sys
import tempfile
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools" / "far_investigation_benchmark.py"
MANIFEST = ROOT / "research/comparisons/far-investigation-benchmark-v0.1/manifest.prepared.json"

SPEC = importlib.util.spec_from_file_location("far_investigation_benchmark", TOOL)
BENCH = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BENCH)


class BenchmarkManifestTests(unittest.TestCase):
    def run_tool(self, *args):
        return subprocess.run(
            [sys.executable, str(TOOL), *args],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )

    def temporary_manifest(self, data, *, allow_nan=False):
        f = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False)
        json.dump(data, f, allow_nan=allow_nan)
        f.close()
        self.addCleanup(lambda: pathlib.Path(f.name).unlink(missing_ok=True))
        return f.name

    def prepared(self):
        return json.loads(MANIFEST.read_text(encoding="utf-8"))

    def test_prepared_manifest_validates(self):
        r = self.run_tool("validate", "--manifest", str(MANIFEST.relative_to(ROOT)))
        self.assertEqual(r.returncode, 0, r.stderr)

    def test_prepared_manifest_cannot_analyze(self):
        r = self.run_tool("analyze", "--manifest", str(MANIFEST.relative_to(ROOT)))
        self.assertEqual(r.returncode, 2)
        self.assertIn("BLOCKED", r.stderr)

    def test_extra_top_level_field_fails_closed(self):
        data = self.prepared()
        data["unexpected"] = True
        r = self.run_tool("validate", "--manifest", self.temporary_manifest(data))
        self.assertEqual(r.returncode, 1)
        self.assertIn("additional property", r.stderr)

    def test_nested_schema_violation_fails_closed(self):
        data = self.prepared()
        data["evaluators"] = [{}]
        data["stages"] = "invalid"
        r = self.run_tool("validate", "--manifest", self.temporary_manifest(data))
        self.assertEqual(r.returncode, 1)
        self.assertIn("schema", r.stderr)

    def test_nonfinite_json_fails_closed(self):
        data = self.prepared()
        data["environment"]["bad_numeric"] = math.nan
        r = self.run_tool("validate", "--manifest", self.temporary_manifest(data, allow_nan=True))
        self.assertEqual(r.returncode, 1)
        self.assertIn("non-finite JSON", r.stderr)

    def test_schema_pattern_violation_fails_closed(self):
        data = self.prepared()
        data["target"]["commit"] = "not-a-commit"
        data["artifacts"][0]["sha256"] = "xyz"
        r = self.run_tool("validate", "--manifest", self.temporary_manifest(data))
        self.assertEqual(r.returncode, 1)
        self.assertIn("pattern", r.stderr)

    def test_duplicate_unique_schema_values_fail_closed(self):
        data = self.prepared()
        data["limitations"] = ["duplicate", "duplicate"]
        r = self.run_tool("validate", "--manifest", self.temporary_manifest(data))
        self.assertEqual(r.returncode, 1)
        self.assertIn("unique", r.stderr)

    def test_unsafe_artifact_path_fails_closed(self):
        data = self.prepared()
        data["artifacts"][0]["path"] = "../outside.md"
        r = self.run_tool("validate", "--manifest", self.temporary_manifest(data))
        self.assertEqual(r.returncode, 1)
        self.assertIn("unsafe repository path", r.stderr)

    def test_nonzero_prepared_artifact_hash_is_verified(self):
        data = self.prepared()
        data["artifacts"][0]["sha256"] = "1" * 64
        r = self.run_tool("validate", "--manifest", self.temporary_manifest(data))
        self.assertEqual(r.returncode, 1)
        self.assertIn("hash mismatch", r.stderr)

    def test_frozen_record_cannot_opt_out_of_current_path_verification(self):
        errors = []
        BENCH._verify_records(
            [{"path": "README.md", "sha256": "1" * 64, "role": "x", "verify_current_path": False}],
            "artifacts",
            "frozen",
            errors,
        )
        self.assertTrue(any("verify_current_path=true" in e for e in errors), errors)

    def test_fake_frozen_manifest_fails_completeness_gate(self):
        data = self.prepared()
        data["status"] = "frozen"
        for artifact in data["artifacts"]:
            artifact["sha256"] = "1" * 64
            artifact["verify_current_path"] = False
        data["protocol"]["sha256"] = "1" * 64
        r = self.run_tool("validate", "--manifest", self.temporary_manifest(data))
        self.assertEqual(r.returncode, 1)
        self.assertIn("freeze_time", r.stderr)
        self.assertIn("required artifact", r.stderr)
        self.assertIn("verify_current_path=true", r.stderr)

    def test_unblinding_time_cannot_precede_freeze(self):
        data = self.prepared()
        data["status"] = "unblinded"
        data["times"] = {
            "freeze_time": "2026-09-22T20:00:00-04:00",
            "unblinding_time": "2026-09-22T19:00:00-04:00",
        }
        r = self.run_tool("validate", "--manifest", self.temporary_manifest(data))
        self.assertEqual(r.returncode, 1)
        self.assertIn("unblinding_time cannot precede freeze_time", r.stderr)


class FrozenSemanticTests(unittest.TestCase):
    def valid_evaluators(self):
        lanes = [
            "primary_scorer", "primary_scorer", "scoring_adjudicator",
            "unitizer", "unitizer", "unitization_adjudicator",
        ]
        return [
            {
                "id": f"E{i}", "identity": f"person-{i}", "provider": f"external-provider-{i}",
                "model": "none", "prior_exposure": "none", "conflicts": "none", "lane": lane,
            }
            for i, lane in enumerate(lanes)
        ]

    def candidate(self, n, stratum, cluster=None):
        text = f"claim {stratum} {n}"
        return {
            "candidate_id": f"{stratum}-{n:02d}",
            "stratum_id": stratum,
            "retrieval_rank": n,
            "claim_text": text,
            "normalized_claim_text": text,
            "normalized_source_identity": f"source-{stratum}-{n:02d}",
            "claim_cluster_id": cluster or BENCH.sha256_text(text),
            "cluster_representative": True,
            "eligible": True,
            "contamination_checked": True,
            "contaminated": False,
        }

    def valid_case_bundle(self):
        candidates, cases, reserves = [], [], []
        for stratum in BENCH.STRATA:
            rows = [self.candidate(i, stratum) for i in range(1, 21)]
            candidates.extend(rows)
            for i, c in enumerate(rows[:10], 1):
                prompt = f"Investigate {c['claim_text']}"
                cases.append(
                    {
                        "case_id": f"{stratum}-case-{i:02d}",
                        "candidate_id": c["candidate_id"],
                        "claim_cluster_id": c["claim_cluster_id"],
                        "stratum_id": stratum,
                        "prompt": prompt,
                        "prompt_sha256": BENCH.sha256_text(prompt),
                    }
                )
            for c in rows[10:]:
                reserves.append(
                    {
                        "candidate_id": c["candidate_id"],
                        "claim_cluster_id": c["claim_cluster_id"],
                        "stratum_id": stratum,
                    }
                )
        return candidates, cases, reserves

    def valid_schedule(self, cases):
        rows = []
        for c in cases:
            for condition in BENCH.CONDITIONS:
                run_id = f"{c['case_id']}--{condition}"
                key = BENCH.sha256_text(f"20260922|schedule|{c['case_id']}|{condition}")
                rows.append(
                    {
                        "case_id": c["case_id"],
                        "condition": condition,
                        "run_id": run_id,
                        "schedule_key": key,
                        "cache_nonce": BENCH.sha256_text(f"{BENCH.CAMPAIGN_ID}|cache|{run_id}"),
                    }
                )
        rows.sort(key=lambda r: r["schedule_key"])
        for i, row in enumerate(rows, 1):
            row["execution_index"] = i
        return {"status": "FROZEN", "runs": rows}

    def valid_adjudication_schedule(self, cases, execution_schedule, evaluators):
        run_by_pair = {(r["case_id"], r["condition"]): r["run_id"] for r in execution_schedule["runs"]}
        schedules = []
        case_ids = {c["case_id"] for c in cases}
        for evaluator in evaluators:
            if evaluator["lane"] not in {"unitizer", "primary_scorer"}:
                continue
            evaluator_id = evaluator["id"]
            base_order = sorted(
                case_ids,
                key=lambda cid: BENCH.sha256_text(f"20260922|adjudication-case-order|{evaluator_id}|{cid}"),
            )
            assignments = []
            for round_index in range(4):
                for round_position, case_id in enumerate(base_order, 1):
                    condition = BENCH.CONDITIONS[(round_index + (round_position - 1) % 4) % 4]
                    assignments.append(
                        {
                            "presentation_index": len(assignments) + 1,
                            "round": round_index + 1,
                            "round_position": round_position,
                            "case_id": case_id,
                            "condition": condition,
                            "run_id": run_by_pair[(case_id, condition)],
                            "condition_label_visible": False,
                            "fresh_context": True,
                            "other_case_versions_visible": False,
                            "other_evaluator_outputs_visible": False,
                        }
                    )
            schedules.append({"evaluator_id": evaluator_id, "lane": evaluator["lane"], "assignments": assignments})
        return {"status": "FROZEN", "schedules": schedules}

    def test_empty_case_corpus_rejected(self):
        errors = []
        BENCH._validate_case_bundle([], [], [], errors)
        self.assertTrue(any("cases.jsonl must not be empty" in e for e in errors), errors)

    def test_wrong_case_count_and_duplicate_cluster_rejected(self):
        candidates, cases, reserves = self.valid_case_bundle()
        cases.pop()
        cases[1]["claim_cluster_id"] = cases[0]["claim_cluster_id"]
        errors = []
        BENCH._validate_case_bundle(candidates, cases, reserves, errors)
        self.assertTrue(any("exactly 60" in e for e in errors), errors)
        self.assertTrue(any("duplicate claim_cluster_id" in e for e in errors), errors)

    def test_valid_case_bundle_passes_semantic_checks(self):
        candidates, cases, reserves = self.valid_case_bundle()
        errors = []
        BENCH._validate_case_bundle(candidates, cases, reserves, errors)
        self.assertEqual(errors, [])

    def test_schedule_requires_complete_cartesian_product(self):
        _, cases, _ = self.valid_case_bundle()
        schedule = self.valid_schedule(cases)
        schedule["runs"].pop()
        errors = []
        BENCH._validate_schedule(schedule, {c["case_id"] for c in cases}, errors)
        self.assertTrue(any("exactly 240" in e for e in errors), errors)

    def test_schedule_rejects_wrong_cache_nonce(self):
        _, cases, _ = self.valid_case_bundle()
        schedule = self.valid_schedule(cases)
        schedule["runs"][0]["cache_nonce"] = "0" * 64
        errors = []
        BENCH._validate_schedule(schedule, {c["case_id"] for c in cases}, errors)
        self.assertTrue(any("cache nonce mismatch" in e for e in errors), errors)

    def test_adjudication_schedule_reproduces_all_four_evaluator_orders(self):
        _, cases, _ = self.valid_case_bundle()
        execution = self.valid_schedule(cases)
        evaluators = self.valid_evaluators()
        schedule = self.valid_adjudication_schedule(cases, execution, evaluators)
        errors = []
        BENCH._validate_adjudication_schedule(
            schedule, {c["case_id"] for c in cases}, execution, evaluators, errors
        )
        self.assertEqual(errors, [])
        for evaluator_schedule in schedule["schedules"]:
            assignments = evaluator_schedule["assignments"]
            self.assertEqual({a["presentation_index"] for a in assignments}, set(range(1, 241)))
            for round_number in range(1, 5):
                counts = {
                    condition: sum(a["condition"] == condition and a["round"] == round_number for a in assignments)
                    for condition in BENCH.CONDITIONS
                }
                self.assertEqual(counts, {condition: 15 for condition in BENCH.CONDITIONS})

    def test_adjudication_schedule_rejects_missing_evaluator(self):
        _, cases, _ = self.valid_case_bundle()
        execution = self.valid_schedule(cases)
        evaluators = self.valid_evaluators()
        schedule = self.valid_adjudication_schedule(cases, execution, evaluators)
        schedule["schedules"].pop()
        errors = []
        BENCH._validate_adjudication_schedule(
            schedule, {c["case_id"] for c in cases}, execution, evaluators, errors
        )
        self.assertTrue(any("exactly four" in e for e in errors), errors)

    def test_adjudication_schedule_rejects_order_binding_and_isolation_changes(self):
        _, cases, _ = self.valid_case_bundle()
        execution = self.valid_schedule(cases)
        evaluators = self.valid_evaluators()
        schedule = self.valid_adjudication_schedule(cases, execution, evaluators)
        first = schedule["schedules"][0]["assignments"][0]
        first["run_id"] = "wrong-run"
        first["fresh_context"] = False
        first["other_evaluator_outputs_visible"] = True
        errors = []
        BENCH._validate_adjudication_schedule(
            schedule, {c["case_id"] for c in cases}, execution, evaluators, errors
        )
        self.assertTrue(any("frozen order/run binding" in e for e in errors), errors)
        self.assertTrue(any("fresh context" in e for e in errors), errors)
        self.assertTrue(any("another evaluator output" in e for e in errors), errors)

    def test_adjudication_schedule_rejects_undeclared_assignment_field(self):
        _, cases, _ = self.valid_case_bundle()
        execution = self.valid_schedule(cases)
        evaluators = self.valid_evaluators()
        schedule = self.valid_adjudication_schedule(cases, execution, evaluators)
        schedule["schedules"][0]["assignments"][0]["hidden_hint"] = "F"
        errors = []
        BENCH._validate_adjudication_schedule(
            schedule, {c["case_id"] for c in cases}, execution, evaluators, errors
        )
        self.assertTrue(any("invalid fields" in e for e in errors), errors)

    def test_adjudication_schedule_is_a_required_frozen_artifact(self):
        path = f"{BENCH.BENCHMARK_DIR}/adjudication-schedule.json"
        self.assertIn(path, BENCH.REQUIRED_FROZEN_ARTIFACTS)
        self.assertIn(path, BENCH.FROZEN_CONFIG_JSON)

    def test_resource_budget_rejects_infinity(self):
        data = {
            "status": "FROZEN",
            "budgets": {
                "wall_clock_seconds": float("inf"),
                "model_output_token_ceiling": 1000,
                "retrieval_tool_call_ceiling": 20,
                "output_size_ceiling": 1000,
                "retry_rounds": 0,
                "model_family": "m",
                "model_version": "v",
                "source_cutoff": "2026-09-22",
                "retrieval_tools": ["web"],
            },
            "confirmatory_exclusion_rule": "Ceiling hits are not exclusions; only exogenous failures are nonratable.",
        }
        errors = []
        BENCH._validate_resource_budget(data, errors)
        self.assertTrue(any("finite positive" in e for e in errors), errors)

    def test_evaluator_lane_counts_are_exact(self):
        evaluators = self.valid_evaluators()
        errors = []
        BENCH._validate_evaluators(evaluators, errors)
        self.assertEqual(errors, [])
        evaluators[-1]["lane"] = "unitizer"
        errors = []
        BENCH._validate_evaluators(evaluators, errors)
        self.assertTrue(any("lanes must equal" in e for e in errors), errors)

    def test_analysis_parameters_require_familywise_m2_falsification(self):
        data = {
            "case_count": 60,
            "domains": 6,
            "cases_per_domain": 10,
            "confirmatory_baselines": ["B0", "B1", "B2"],
            "m2": {
                "bootstrap_resamples": 10000,
                "seed": 20260922,
                "directional_falsification_familywise": {
                    "one_sided_upper_confidence": 1 - 0.05 / 3,
                    "zero_based_index_n10000": 9833,
                    "strictly_less_than": -0.05,
                },
            },
        }
        errors = []
        BENCH._validate_analysis_parameters(data, errors)
        self.assertEqual(errors, [])
        data["m2"]["directional_falsification_familywise"]["zero_based_index_n10000"] = 9499
        errors = []
        BENCH._validate_analysis_parameters(data, errors)
        self.assertTrue(any("9833" in e for e in errors), errors)

    def test_treatment_manifest_requires_all_transitive_sources(self):
        records = []
        for path in sorted(BENCH.TREATMENT_SOURCE_PATHS):
            fp = ROOT / path
            self.assertTrue(fp.exists(), path)
            records.append({"path": path, "sha256": BENCH.sha256(fp), "verify_current_path": True})
        errors = []
        BENCH._validate_treatment_manifest({"status": "FROZEN", "sources": records}, errors)
        self.assertEqual(errors, [])
        errors = []
        BENCH._validate_treatment_manifest({"status": "FROZEN", "sources": records[:-1]}, errors)
        self.assertTrue(any("missing mandatory transitive" in e for e in errors), errors)


if __name__ == "__main__":
    unittest.main()
