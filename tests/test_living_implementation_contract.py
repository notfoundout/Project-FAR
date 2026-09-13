from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from tools.living_implementation_contract import ImplementationContractError, build_plan, canonical_json_sha, sha256
from tools.materialize_living_implementation import materialize

CID = "FAR-LIT-0123456789ABCDEF"
PID = "FAR-LIVING-IMPL-TEST1"
SOURCE_SHA = "a" * 40
BASE_SHA = "b" * 40
TARGET = "docs/governance/generated-note.md"


def put_json(root: Path, rel: str, value: object) -> bytes:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    raw = (json.dumps(value, sort_keys=True) + "\n").encode()
    path.write_bytes(raw)
    return raw


def fixture(required: bool = True, target: str = TARGET):
    temp = tempfile.TemporaryDirectory()
    root = Path(temp.name)
    canonical, source = root / "canonical", root / "source"
    canonical.mkdir(); source.mkdir()
    put_json(canonical, "research/living/implementation-policy-v1.0.json", {
        "schema_version": "1.0", "program_id": "FAR-LIVING-IMPLEMENTATION-001", "authority": "Research",
        "source_pr": 490, "source_branch": "automation/living-research-inbox",
        "proposal_stage": "IMPLEMENTATION_PROPOSED", "authorization_status": "ACCEPTED_FOR_PROTECTED_IMPLEMENTATION_PR",
        "write_roots": [".github", "docs/governance", "scripts", "tests", "tools"],
        "write_exact_paths": ["Makefile", "pyproject.toml", "requirements.txt"],
        "manifest_prefix": "research/living/implementation-promotions/", "branch_prefix": "automation/living-implementation-",
    })
    put_json(canonical, "research/living/project-change-policy-v1.0.json", {
        "program_id": "FAR-LIVING-PROJECT-CHANGE-001",
        "implementation_review_fields": ["implementation_required", "implementation_proposal_id"],
    })
    review = {
        "candidate_id": CID, "source_key": "doi:10.0000/test", "disposition": "PROJECT_CHANGE_REQUIRED",
        "reviewed_on": "2026-09-13", "review_basis": "docs/audits/test.md", "proposal_id": "FAR-LIVING-PROP-TEST1",
        "suppress_from_core_claim_review_queue": True, "implementation_required": required,
        "implementation_proposal_id": PID if required else None,
    }
    put_json(canonical, "research/living/review-dispositions-v1.0.json", {"reviewed_candidates": [review]})
    candidate = b'{"candidate_id":"FAR-LIT-0123456789ABCDEF"}\n'
    candidate_path = source / f"research/living/inbox/candidates/{CID}.json"
    candidate_path.parent.mkdir(parents=True, exist_ok=True); candidate_path.write_bytes(candidate)
    payload = b"replacement\n"
    payload_rel = f"research/living/inbox/implementation-payloads/{PID}/{target}"
    payload_path = source / payload_rel
    payload_path.parent.mkdir(parents=True, exist_ok=True); payload_path.write_bytes(payload)
    operation = {"op": "write_file", "path": target, "source_path": payload_rel, "expected_main_sha256": "ABSENT", "result_sha256": sha256(payload)}
    proposal = {"proposal_id": PID, "candidate_id": CID, "candidate_sha256": sha256(candidate), "lifecycle_stage": "IMPLEMENTATION_PROPOSED", "operations": [operation]}
    proposal_raw = put_json(source, f"research/living/inbox/implementation-proposals/{PID}.json", proposal)
    auths = []
    if required:
        auths.append({"proposal_id": PID, "candidate_id": CID, "proposal_sha256": sha256(proposal_raw), "candidate_sha256": sha256(candidate), "operations_sha256": canonical_json_sha([operation]), "review_record_sha256": canonical_json_sha(review), "authorization_status": "ACCEPTED_FOR_PROTECTED_IMPLEMENTATION_PR"})
    put_json(canonical, "research/living/implementation-authorizations-v1.0.json", {"schema_version": "1.0", "program_id": "FAR-LIVING-IMPLEMENTATION-AUTHORIZATIONS-001", "authority": "Research", "authorizations": auths})
    return temp, canonical, source, payload_rel


class LivingImplementationContractTests(unittest.TestCase):
    def test_not_required_is_non_actionable(self):
        tmp, canonical, source, _ = fixture(False)
        try:
            plan = build_plan(canonical, source, source_sha=SOURCE_SHA, base_sha=BASE_SHA)
            self.assertFalse(plan["actionable"])
        finally: tmp.cleanup()

    def test_valid_authorized_package_is_actionable(self):
        tmp, canonical, source, _ = fixture()
        try:
            plan = build_plan(canonical, source, source_sha=SOURCE_SHA, base_sha=BASE_SHA)
            self.assertTrue(plan["actionable"])
            self.assertEqual(TARGET, plan["proposals"][0]["operations"][0]["path"])
        finally: tmp.cleanup()

    def test_missing_authorization_fails(self):
        tmp, canonical, source, _ = fixture()
        try:
            put_json(canonical, "research/living/implementation-authorizations-v1.0.json", {"schema_version": "1.0", "program_id": "FAR-LIVING-IMPLEMENTATION-AUTHORIZATIONS-001", "authority": "Research", "authorizations": []})
            with self.assertRaisesRegex(ImplementationContractError, "missing protected implementation authorization"):
                build_plan(canonical, source, source_sha=SOURCE_SHA, base_sha=BASE_SHA)
        finally: tmp.cleanup()

    def test_tampered_payload_fails(self):
        tmp, canonical, source, payload_rel = fixture()
        try:
            (source / payload_rel).write_bytes(b"changed\n")
            with self.assertRaisesRegex(ImplementationContractError, "payload hash mismatch"):
                build_plan(canonical, source, source_sha=SOURCE_SHA, base_sha=BASE_SHA)
        finally: tmp.cleanup()

    def test_forbidden_target_fails(self):
        tmp, canonical, source, _ = fixture(target="theory/forbidden.md")
        try:
            with self.assertRaisesRegex(ImplementationContractError, "outside implementation surface"):
                build_plan(canonical, source, source_sha=SOURCE_SHA, base_sha=BASE_SHA)
        finally: tmp.cleanup()

    def test_stale_preimage_fails(self):
        tmp, canonical, source, _ = fixture()
        try:
            target = canonical / TARGET
            target.parent.mkdir(parents=True, exist_ok=True); target.write_text("old\n")
            with self.assertRaisesRegex(ImplementationContractError, "stale main preimage"):
                build_plan(canonical, source, source_sha=SOURCE_SHA, base_sha=BASE_SHA)
        finally: tmp.cleanup()

    def test_materializer_writes_exact_payload_and_manifest(self):
        tmp, canonical, source, _ = fixture()
        try:
            plan = build_plan(canonical, source, source_sha=SOURCE_SHA, base_sha=BASE_SHA)
            manifest = materialize(canonical, source, plan)
            self.assertEqual(b"replacement\n", (canonical / TARGET).read_bytes())
            self.assertTrue((canonical / plan["manifest_path"]).is_file())
            self.assertEqual([TARGET], [row["path"] for row in manifest["sealed_files"]])
        finally: tmp.cleanup()


if __name__ == "__main__": unittest.main()
