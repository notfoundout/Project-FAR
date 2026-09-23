import unittest
from pathlib import Path

from tests.test_far_investigation_benchmark import BENCH, FrozenSemanticTests


ROOT = Path(__file__).resolve().parents[1]
BENCH_ROOT = ROOT / "research/comparisons/far-investigation-benchmark-v0.1"


class AdjudicationTieBreakTests(unittest.TestCase):
    def test_equal_schedule_hashes_break_by_case_id(self):
        helper = FrozenSemanticTests()
        _, cases, _ = helper.valid_case_bundle()
        execution = helper.valid_schedule(cases)
        evaluators = helper.valid_evaluators()

        case_ids = sorted((case["case_id"] for case in cases), reverse=True)
        run_by_pair = {
            (run["case_id"], run["condition"]): run["run_id"]
            for run in execution["runs"]
        }
        eligible = sorted(
            (evaluator["id"], evaluator["lane"])
            for evaluator in evaluators
            if evaluator["lane"] in {"unitizer", "primary_scorer"}
        )

        schedules = []
        for evaluator_id, lane in eligible:
            assignments = []
            presentation_index = 1
            for round_index in range(4):
                for base_position, case_id in enumerate(sorted(case_ids)):
                    condition = BENCH.CONDITIONS[(round_index + (base_position % 4)) % 4]
                    assignments.append(
                        {
                            "presentation_index": presentation_index,
                            "round": round_index,
                            "base_position": base_position,
                            "case_id": case_id,
                            "condition": condition,
                            "run_id": run_by_pair[(case_id, condition)],
                        }
                    )
                    presentation_index += 1
            schedules.append(
                {
                    "evaluator_id": evaluator_id,
                    "lane": lane,
                    "assignments": assignments,
                }
            )

        schedule = {
            "status": "FROZEN",
            "algorithm": "sha256-four-round-counterbalance-v1",
            "isolation": {
                "fresh_context_per_packet": True,
                "condition_label_visible": False,
                "same_case_other_condition_visible": False,
                "other_evaluator_scores_visible": False,
            },
            "evaluators": schedules,
        }

        original_sha256_text = BENCH.sha256_text

        def forced_tie(text):
            if text.startswith("20260922|adjudication-case-order|"):
                return "0" * 64
            return original_sha256_text(text)

        BENCH.sha256_text = forced_tie
        try:
            errors = []
            BENCH._validate_adjudication_schedule(
                schedule,
                case_ids,
                execution,
                evaluators,
                errors,
            )
        finally:
            BENCH.sha256_text = original_sha256_text

        self.assertEqual(errors, [])

    def test_controlling_normative_surfaces_require_case_id_tie_break(self):
        amendment = (BENCH_ROOT / "hardening-amendment-v0.1.md").read_text(encoding="utf-8")
        rubric = (BENCH_ROOT / "adjudication-rubric-v0.1.md").read_text(encoding="utf-8")

        self.assertIn(
            'sort the 60 final cases by the ascending tuple `(SHA256(UTF8("20260922|adjudication-case-order|" + evaluator_id + "|" + case_id)), case_id)`',
            amendment,
        )
        self.assertIn(
            "using Unicode code-point ordering for the `case_id` tie-break when schedule hashes are equal",
            amendment,
        )
        self.assertIn(
            'Sort the 60 final `case_id` values by the tuple `(lowercase hexadecimal SHA256(UTF8("20260922|adjudication-case-order|" + evaluator_id + "|" + case_id)), case_id)`, ascending in both components.',
            rubric,
        )
        self.assertIn(
            "The secondary `case_id` comparison uses Unicode code-point order and is mandatory",
            rubric,
        )


if __name__ == "__main__":
    unittest.main()
