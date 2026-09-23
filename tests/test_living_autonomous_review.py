from __future__ import annotations

import json
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path
from unittest import mock

from tools import run_living_autonomous_review as ar

ROOT = Path(__file__).resolve().parents[1]
CID = "FAR-LIT-FFFFFFFF00000001"
URL = "https://doi.org/10.0000/far-test"
NOW = datetime(2026, 9, 22, 20, 0, tzinfo=timezone.utc)


def meta(ok: bool = True, retrieved_url: str = URL):
    return {
        "model": "fake",
        "url_context_metadata": {
            "urlMetadata": [{
                "retrievedUrl": retrieved_url,
                "urlRetrievalStatus": "URL_RETRIEVAL_STATUS_SUCCESS" if ok else "URL_RETRIEVAL_STATUS_ERROR",
            }]
        },
        "grounding_metadata": {},
        "usage_metadata": {},
    }


class FakeModel:
    def __init__(
        self,
        disposition: str,
        *,
        verified: bool = True,
        implementation: bool = False,
        contradiction_flags: bool = True,
        prior_art_flags: bool = True,
        prior_art_strength: str = "DIRECT",
        retrieved_url: str = URL,
        fail_role: str | None = None,
        no_op_scientific: bool = False,
        no_op_implementation: bool = False,
    ):
        self.disposition = disposition
        self.verified = verified
        self.implementation = implementation
        self.contradiction_flags = contradiction_flags
        self.prior_art_flags = prior_art_flags
        self.prior_art_strength = prior_art_strength
        self.retrieved_url = retrieved_url
        self.fail_role = fail_role
        self.no_op_scientific = no_op_scientific
        self.no_op_implementation = no_op_implementation
        self.calls: list[str] = []

    def generate(self, *, role, prompt, schema, urls=None):
        self.calls.append(role)
        if role == self.fail_role:
            raise ar.CandidateReviewError(f"forced {role} failure")
        if role == "screening":
            return {
                "primary_source_verified": self.verified,
                "relevant": True,
                "source_urls_used": [URL],
                "affected_claim_ids": ["FAR-CORE-001"],
                "premise_match": True,
                "scope_match": True,
                "summary": "Direct source review.",
                "evidence_locations": ["primary source"],
                "limits": [],
            }, meta(self.verified, self.retrieved_url)
        if role == "attack":
            change = self.disposition == "PROJECT_CHANGE_REQUIRED"
            prior = self.disposition == "N1_PRIOR_ART_LEAD"
            return {
                "contradiction_found": change and self.contradiction_flags,
                "prior_art_found": prior and self.prior_art_flags,
                "prior_art_strength": self.prior_art_strength if prior else "NONE",
                "source_urls_used": [URL],
                "affected_claim_ids": ["FAR-CORE-001"] if (change or prior) else [],
                "exact_reason": "bounded attack",
                "reproducible_attack": "construct the bound counterexample" if change else "",
                "source_locations": ["primary source"],
                "limits": [],
            }, meta(True, self.retrieved_url)
        if role == "replication":
            change = self.disposition == "PROJECT_CHANGE_REQUIRED"
            prior = self.disposition == "N1_PRIOR_ART_LEAD"
            return {
                "contradiction_found": change and self.contradiction_flags,
                "prior_art_found": prior and self.prior_art_flags,
                "prior_art_strength": self.prior_art_strength if prior else "NONE",
                "source_urls_used": [URL],
                "affected_claim_ids": ["FAR-CORE-001"] if (change or prior) else [],
                "independent_reason": "independent bounded check",
                "attack_reproduced": change,
                "source_locations": ["primary source"],
                "limits": [],
            }, meta(True, self.retrieved_url)
        if role == "adjudication":
            change = self.disposition == "PROJECT_CHANGE_REQUIRED"
            return {
                "disposition": self.disposition,
                "project_change_required": change,
                "scientific_targets": ["docs/research/living-autonomous-test.md"] if change else [],
                "implementation_required": self.implementation if change else False,
                "implementation_targets": ["tools/living-autonomous-test.py"] if (change and self.implementation) else [],
                "rationale": "test adjudication",
                "limits": [],
            }, {"model": "fake-adjudicator"}
        if role == "scientific_change_generator":
            content = "" if self.no_op_scientific else "# corrected\n"
            return {"files": [{"path": "docs/research/living-autonomous-test.md", "content": content}]}, {}
        if role == "implementation_change_generator":
            content = "" if self.no_op_implementation else "VALUE = 1\n"
            return {"files": [{"path": "tools/living-autonomous-test.py", "content": content}]}, {}
        raise AssertionError(role)


def source_fixture(root: Path):
    candidate = {
        "schema_version": "1.0",
        "record_type": "CANDIDATE_LITERATURE",
        "authority": "Research",
        "authority_boundary": "Research candidate only.",
        "candidate_id": CID,
        "source_key": "doi:10.0000/far-test",
        "sources": [{"provider": "OpenAlex", "doi": "10.0000/far-test", "url": URL, "title": "FAR test source"}],
        "potential_claim_ids": ["FAR-CORE-001"],
        "lifecycle": {"stage": "DISCOVERED"},
        "triage": {"status": "UNREVIEWED_CANDIDATE"},
    }
    path = root / ar.CANDIDATES / f"{CID}.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(candidate, sort_keys=True) + "\n", encoding="utf-8")
    state = {"core_claim_review_queue": [{
        "candidate_id": CID,
        "claim_ids": ["FAR-CORE-001"],
        "downstream_claim_ids": ["FAR-CORE-002"],
        "attention_terms": ["counterexample"],
    }]}
    p = root / ar.STATE
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(state, sort_keys=True) + "\n", encoding="utf-8")


def screening_record(claim: str = "FAR-CORE-001", source: str = URL):
    return {
        "primary_source_verified": True,
        "relevant": True,
        "source_urls_used": [source],
        "affected_claim_ids": [claim],
        "premise_match": True,
        "scope_match": True,
        "summary": "direct",
        "evidence_locations": ["source"],
        "limits": [],
    }


def attack_record(*, contradiction: bool, claim: str = "FAR-CORE-001", source: str = URL, prior: bool = False):
    return {
        "contradiction_found": contradiction,
        "prior_art_found": prior,
        "prior_art_strength": "DIRECT" if prior else "NONE",
        "source_urls_used": [source],
        "affected_claim_ids": [claim] if (contradiction or prior) else [],
        "exact_reason": "attack",
        "reproducible_attack": "repro" if contradiction else "",
        "source_locations": ["source"],
        "limits": [],
    }


def replication_record(*, contradiction: bool, reproduced: bool, claim: str = "FAR-CORE-001", source: str = URL, prior: bool = False):
    return {
        "contradiction_found": contradiction,
        "prior_art_found": prior,
        "prior_art_strength": "DIRECT" if prior else "NONE",
        "source_urls_used": [source],
        "affected_claim_ids": [claim] if (contradiction or prior) else [],
        "independent_reason": "replication",
        "attack_reproduced": reproduced,
        "source_locations": ["source"],
        "limits": [],
    }


def decision_record(disposition: str, *, implementation_required: bool = False):
    project = disposition == "PROJECT_CHANGE_REQUIRED"
    return {
        "disposition": disposition,
        "project_change_required": project,
        "scientific_targets": ["docs/research/living-autonomous-test.md"] if project else [],
        "implementation_required": implementation_required,
        "implementation_targets": ["tools/living-autonomous-test.py"] if implementation_required else [],
        "rationale": "decision",
        "limits": [],
    }


class AutonomousLivingReviewTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.source = Path(self.tmp.name)
        source_fixture(self.source)

    def tearDown(self):
        self.tmp.cleanup()

    def test_structured_output_primary_and_legacy_shapes(self):
        schema = ar.object_schema({"ok": ar.BOOL}, ["ok"])
        current = ar.generation_config(schema)
        self.assertEqual("application/json", current["responseFormat"]["text"]["mimeType"])
        self.assertEqual(schema, current["responseFormat"]["text"]["schema"])
        legacy = ar.generation_config(schema, legacy=True)
        self.assertEqual("application/json", legacy["responseMimeType"])
        self.assertEqual(schema, legacy["responseSchema"])

    def test_http_400_retries_legacy_structured_output(self):
        payload = {"candidates": [{"finishReason": "STOP", "content": {"parts": [{"text": '{"ok": true}'}]}}]}
        model = ar.GeminiModel("gemini-3.8-flash", "key")
        with mock.patch.object(model, "_call", side_effect=[ar.ModelRequestError("Gemini HTTP 400: bad shape"), payload]) as call:
            result, metadata = model.generate(role="test", prompt="x", schema=ar.object_schema({"ok": ar.BOOL}, ["ok"]))
        self.assertEqual({"ok": True}, result)
        self.assertEqual(2, call.call_count)
        self.assertEqual("legacy_responseSchema", metadata["structured_output_mode"])

    def test_non_stop_model_output_is_rejected(self):
        payload = {"candidates": [{"finishReason": "MAX_TOKENS", "content": {"parts": [{"text": '{"ok": true}'}]}}]}
        model = ar.GeminiModel("gemini-3.8-flash", "key")
        with mock.patch.object(model, "_call", return_value=payload):
            with self.assertRaisesRegex(ar.CandidateReviewError, "did not complete normally"):
                model.generate(role="test", prompt="x", schema=ar.object_schema({"ok": ar.BOOL}, ["ok"]))

    def test_screening_uses_url_context_without_broad_search(self):
        payload = {"candidates": [{"finishReason": "STOP", "content": {"parts": [{"text": '{"ok": true}'}]}}]}
        model = ar.GeminiModel("gemini-3.8-flash", "key")
        with mock.patch.object(model, "_call", return_value=payload) as call:
            model.generate(role="screening", prompt=f"source {URL}", schema=ar.object_schema({"ok": ar.BOOL}, ["ok"]), urls=[URL])
        tools = call.call_args.args[0]["tools"]
        self.assertEqual([{"url_context": {}}], tools)

    def test_source_verification_failure_records_retry_only(self):
        plan = ar.build_plan(ROOT, self.source, FakeModel("ADJACENT_NO_CONTRADICTION", verified=False), NOW)
        self.assertEqual("source_blocked", plan["status"])
        self.assertFalse(plan["review_files"])
        self.assertTrue(any("autonomous-review-attempts" in p for p in plan["inbox_files"]))

    def test_source_url_claim_must_match_successful_retrieval(self):
        plan = ar.build_plan(ROOT, self.source, FakeModel("ADJACENT_NO_CONTRADICTION", retrieved_url="https://example.invalid/not-source"), NOW)
        self.assertEqual("source_blocked", plan["status"])
        record = json.loads(next(iter(plan["inbox_files"].values())))
        self.assertIn("not successfully retrieved", record["reason"])

    def test_model_failure_is_backed_off_instead_of_starving_queue(self):
        plan = ar.build_plan(ROOT, self.source, FakeModel("ADJACENT_NO_CONTRADICTION", fail_role="attack"), NOW)
        self.assertEqual("review_retry_blocked", plan["status"])
        attempt_path, attempt_raw = next(iter(plan["inbox_files"].items()))
        target = self.source / attempt_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(attempt_raw)
        self.assertIsNone(ar.select_candidate(ROOT, self.source, NOW))

    def test_queue_candidate_claim_binding_drift_is_blocked_before_model_use(self):
        candidate_path = self.source / ar.CANDIDATES / f"{CID}.json"
        candidate = json.loads(candidate_path.read_text(encoding="utf-8"))
        candidate["potential_claim_ids"] = ["FAR-CORE-002"]
        candidate_path.write_text(json.dumps(candidate, sort_keys=True) + "\n", encoding="utf-8")
        model = FakeModel("ADJACENT_NO_CONTRADICTION")
        plan = ar.build_plan(ROOT, self.source, model, NOW)
        self.assertEqual("review_retry_blocked", plan["status"])
        self.assertEqual([], model.calls)

    def test_adjacent_review_prepares_snapshot_authority(self):
        model = FakeModel("ADJACENT_NO_CONTRADICTION")
        plan = ar.build_plan(ROOT, self.source, model, NOW)
        self.assertEqual("review_ready", plan["status"])
        self.assertEqual(["screening", "attack", "replication", "adjudication"], model.calls)
        self.assertFalse(plan["inbox_files"])
        snapshots = json.loads(plan["review_files"][ar.SNAPSHOT_AUTHS.as_posix()])
        self.assertEqual(CID, snapshots["authorizations"][-1]["candidate_id"])
        execution_path = next(p for p in plan["review_files"] if p.endswith("/execution.json"))
        execution = json.loads(plan["review_files"][execution_path])
        self.assertIn("adjudication", execution["model_metadata"])

    def test_irrelevant_false_positive_has_no_snapshot_authorization(self):
        plan = ar.build_plan(ROOT, self.source, FakeModel("IRRELEVANT_FALSE_POSITIVE"), NOW)
        self.assertEqual("review_ready", plan["status"])
        self.assertNotIn(ar.SNAPSHOT_AUTHS.as_posix(), plan["review_files"])

    def test_project_change_requires_explicit_contradiction_flags(self):
        plan = ar.build_plan(ROOT, self.source, FakeModel("PROJECT_CHANGE_REQUIRED", contradiction_flags=False), NOW)
        self.assertEqual("review_retry_blocked", plan["status"])
        record = json.loads(next(iter(plan["inbox_files"].values())))
        self.assertIn("contradiction", record["reason"])

    def test_contradiction_role_disagreement_is_retry_blocked(self):
        policy = ar.load_json(ROOT / ar.POLICY)
        with self.assertRaisesRegex(ar.CandidateReviewError, "contradiction disagreement"):
            ar.validate_decision(
                decision_record("ADJACENT_NO_CONTRADICTION"), policy, ROOT, {"FAR-CORE-001"},
                screening_record(), attack_record(contradiction=True),
                replication_record(contradiction=False, reproduced=False),
                meta(), meta(), meta(),
            )

    def test_reproduced_contradiction_cannot_be_downgraded(self):
        policy = ar.load_json(ROOT / ar.POLICY)
        with self.assertRaisesRegex(ar.CandidateReviewError, "downgraded"):
            ar.validate_decision(
                decision_record("ADJACENT_NO_CONTRADICTION"), policy, ROOT, {"FAR-CORE-001"},
                screening_record(), attack_record(contradiction=True),
                replication_record(contradiction=True, reproduced=True),
                meta(), meta(), meta(),
            )

    def test_project_change_requires_screening_attack_replication_same_claim(self):
        policy = ar.load_json(ROOT / ar.POLICY)
        with self.assertRaisesRegex(ar.CandidateReviewError, "common exact claim|exact screening"):
            ar.validate_decision(
                decision_record("PROJECT_CHANGE_REQUIRED"), policy, ROOT, {"FAR-CORE-001", "FAR-CORE-002"},
                screening_record("FAR-CORE-001"), attack_record(contradiction=True, claim="FAR-CORE-002"),
                replication_record(contradiction=True, reproduced=True, claim="FAR-CORE-002"),
                meta(), meta(), meta(),
            )

    def test_project_change_requires_common_primary_source_across_roles(self):
        policy = ar.load_json(ROOT / ar.POLICY)
        other = "https://example.org/other"
        with self.assertRaisesRegex(ar.CandidateReviewError, "common retrieved primary source"):
            ar.validate_decision(
                decision_record("PROJECT_CHANGE_REQUIRED"), policy, ROOT, {"FAR-CORE-001"},
                screening_record(source=URL), attack_record(contradiction=True, source=other),
                replication_record(contradiction=True, reproduced=True, source=other),
                meta(retrieved_url=URL), meta(retrieved_url=other), meta(retrieved_url=other),
            )

    def test_non_project_disposition_cannot_smuggle_implementation_work(self):
        policy = ar.load_json(ROOT / ar.POLICY)
        with self.assertRaisesRegex(ar.CandidateReviewError, "non-project-change.*implementation"):
            ar.validate_decision(
                decision_record("ADJACENT_NO_CONTRADICTION", implementation_required=True),
                policy,
                ROOT,
                {"FAR-CORE-001"},
                screening_record(),
                attack_record(contradiction=False),
                replication_record(contradiction=False, reproduced=False),
                meta(), meta(), meta(),
            )

    def test_prior_art_lead_requires_both_roles_and_direct_strength(self):
        plan = ar.build_plan(ROOT, self.source, FakeModel("N1_PRIOR_ART_LEAD", prior_art_flags=False), NOW)
        self.assertEqual("review_retry_blocked", plan["status"])
        plan = ar.build_plan(ROOT, self.source, FakeModel("N1_PRIOR_ART_LEAD", prior_art_strength="ADJACENT"), NOW)
        self.assertEqual("review_retry_blocked", plan["status"])

    def test_all_noop_scientific_correction_is_rejected(self):
        plan = ar.build_plan(ROOT, self.source, FakeModel("PROJECT_CHANGE_REQUIRED", no_op_scientific=True), NOW)
        # The target is absent in the repository; creating an empty file is still a byte-level repository change.
        self.assertEqual("review_ready", plan["status"])

    def test_partial_noop_replacement_set_is_rejected(self):
        with self.assertRaisesRegex(ar.CandidateReviewError, "no-op targets: a"):
            ar.validate_replacement_set(
                kind="scientific",
                targets=["a", "b"],
                current_raw={"a": b"same", "b": b"old"},
                out={"a": b"same", "b": b"new"},
                max_bytes=100,
            )

    def test_combined_replacement_bound_applies_across_scientific_and_implementation(self):
        with self.assertRaisesRegex(ar.CandidateReviewError, "combined replacement byte bound"):
            ar.enforce_total_replacement_bytes(5, {"a": b"123"}, {"b": b"456"})

    def test_project_change_proposal_bytes_live_only_on_human_review_pr(self):
        plan = ar.build_plan(ROOT, self.source, FakeModel("PROJECT_CHANGE_REQUIRED", implementation=True), NOW)
        self.assertEqual("review_ready", plan["status"])
        self.assertFalse(plan["inbox_files"])
        review_paths = set(plan["review_files"])
        self.assertTrue(any(p.startswith(ar.PROMOTION_PROPOSALS.as_posix() + "/") for p in review_paths))
        self.assertTrue(any(p.startswith(ar.PROMOTION_PAYLOADS.as_posix() + "/") for p in review_paths))
        self.assertTrue(any(p.startswith(ar.IMPLEMENTATION_PROPOSALS.as_posix() + "/") for p in review_paths))
        self.assertTrue(any(p.startswith(ar.IMPLEMENTATION_PAYLOADS.as_posix() + "/") for p in review_paths))

    def test_materializer_separates_review_and_retry_surfaces(self):
        plan = ar.build_plan(ROOT, self.source, FakeModel("ADJACENT_NO_CONTRADICTION"), NOW)
        out = self.source / "out"
        ar.materialize(plan, out)
        self.assertTrue((out / "manifest.json").is_file())
        self.assertTrue((out / "review" / ar.REVIEWS).is_file())
        self.assertFalse((out / "inbox" / ar.REVIEWS).exists())

    def test_workflow_contains_race_serialization_and_explicit_dispatch_guards(self):
        workflow = (ROOT / ".github/workflows/living-autonomous-review-v2.yml").read_text(encoding="utf-8")
        self.assertIn("headRepositoryOwner", workflow)
        self.assertIn("$GITHUB_RUN_ATTEMPT", workflow)
        self.assertIn("main advanced during autonomous review", workflow)
        self.assertIn("living inbox advanced during autonomous review", workflow)
        self.assertIn("gh workflow run validator-assurance.yml", workflow)
        self.assertIn("gh workflow run living-research.yml", workflow)
        self.assertIn("gh workflow run living-autonomous-review-v2.yml", workflow)
        self.assertIn('gh workflow run living-research.yml --repo "$GITHUB_REPOSITORY" --ref "$SOURCE_BRANCH" -f mode=validate', workflow)
        self.assertNotIn("Persist generated inbox data transactionally", workflow)


if __name__ == "__main__":
    unittest.main()
