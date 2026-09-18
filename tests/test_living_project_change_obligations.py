from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tools import promote_living_research as promoter
from tools import reconcile_living_repo as living_reconcile
from tools.check_living_project_change_obligations import (
    CHANGE_DISPOSITION,
    REQUIRED_REVIEW_FIELDS,
    check,
)

ROOT = Path(__file__).resolve().parents[1]
CID = "FAR-LIT-0123456789ABCDEF"
PID = "FAR-LIVING-PROP-CRITICAL-001"
CANDIDATE_RAW = b'{"candidate_id":"FAR-LIT-0123456789ABCDEF"}\n'
PAYLOAD_RAW = b"corrected bytes\n"


def put(root: Path, rel: str, value: object) -> None:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value) + "\n", encoding="utf-8")


def fixture(root: Path, *, promotion: bool = True, snapshot: bool = True) -> dict[str, object]:
    put(root, "research/living/project-change-policy-v1.0.json", {
        "program_id": "FAR-LIVING-PROJECT-CHANGE-001",
        "authority": "Research",
        "disposition": CHANGE_DISPOSITION,
        "source_pr": 490,
        "source_branch": "automation/living-research-inbox",
        "required_review_fields": sorted(REQUIRED_REVIEW_FIELDS),
    })
    put(root, "research/living/promotion-policy-v1.0.json", {
        "snapshot_review_dispositions": [CHANGE_DISPOSITION],
    })
    review = {
        "candidate_id": CID,
        "source_key": "doi:10.0000/example",
        "disposition": CHANGE_DISPOSITION,
        "reviewed_on": "2026-09-13",
        "review_basis": "docs/audits/example.md",
        "proposal_id": PID,
        "suppress_from_core_claim_review_queue": True,
    }
    put(root, "research/living/review-dispositions-v1.0.json", {
        "allowed_dispositions": [CHANGE_DISPOSITION],
        "reviewed_candidates": [review],
    })
    basis = root / "docs/audits/example.md"
    basis.parent.mkdir(parents=True, exist_ok=True)
    basis.write_text("accepted review\n", encoding="utf-8")

    provenance: dict[str, dict[str, str]] = {}
    for key in promoter.PROV_KEYS:
        path = root / f"docs/{key}.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f"{key}\n", encoding="utf-8")
        provenance[key] = {
            "path": f"docs/{key}.md",
            "sha256": promoter.h(path.read_bytes()),
        }

    operation = {
        "op": "write_file",
        "path": "docs/project-status.md",
        "source_path": f"research/living/inbox/promotion-payloads/{PID}/docs/project-status.md",
        "expected_main_sha256": "ABSENT",
        "result_sha256": promoter.h(PAYLOAD_RAW),
    }
    operations = [operation]
    candidate_sha = promoter.h(CANDIDATE_RAW)
    proposal = {
        "proposal_id": PID,
        "candidate_id": CID,
        "candidate_sha256": candidate_sha,
        "lifecycle_stage": "PROMOTION_PROPOSED",
        "provenance": provenance,
        "operations": operations,
    }
    proposal_raw = (json.dumps(proposal) + "\n").encode()
    promotion_auth = {
        "proposal_id": PID,
        "candidate_id": CID,
        "proposal_sha256": promoter.h(proposal_raw),
        "candidate_sha256": candidate_sha,
        "operations_sha256": promoter.canonical_json_sha(operations),
        "lifecycle_stage": "PROMOTION_PROPOSED",
        "authorization_status": "ACCEPTED_FOR_MECHANICAL_PROMOTION",
        "provenance_sha256": {key: value["sha256"] for key, value in provenance.items()},
    }
    put(root, "research/living/promotion-authorizations-v1.0.json", {
        "authorizations": [] if not promotion else [promotion_auth],
    })
    snapshot_auth = {
        "candidate_id": CID,
        "candidate_sha256": candidate_sha,
        "source_key": review["source_key"],
        "disposition": CHANGE_DISPOSITION,
        "review_basis": review["review_basis"],
        "review_basis_sha256": promoter.h(basis.read_bytes()),
        "review_record_sha256": promoter.canonical_json_sha(review),
        "authorization_status": "ACCEPTED_FOR_MECHANICAL_SNAPSHOT",
    }
    put(root, "research/living/snapshot-authorizations-v1.0.json", {
        "authorizations": [] if not snapshot else [snapshot_auth],
    })
    return {"proposal": proposal, "proposal_raw": proposal_raw, "operation": operation}


def source_reader(proposal_raw: bytes):
    def read(_root: Path, _ref: str, path: str) -> bytes | None:
        if path.endswith(f"candidates/{CID}.json"):
            return CANDIDATE_RAW
        if path.endswith(f"promotion-proposals/{PID}.json"):
            return proposal_raw
        if path.startswith(f"research/living/inbox/promotion-payloads/{PID}/"):
            return PAYLOAD_RAW
        return None

    return read


class ProjectChangeObligationTests(unittest.TestCase):
    def test_current_repository_is_complete(self) -> None:
        self.assertEqual([], check(ROOT))

    def test_reconciler_and_registry_share_project_change_disposition(self) -> None:
        registry = json.loads(
            (ROOT / "research/living/review-dispositions-v1.0.json").read_text(encoding="utf-8")
        )
        self.assertIn(CHANGE_DISPOSITION, living_reconcile.ALLOWED_REVIEW_DISPOSITIONS)
        self.assertEqual(
            set(registry["allowed_dispositions"]),
            living_reconcile.ALLOWED_REVIEW_DISPOSITIONS,
        )

    def test_complete_local_obligation_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fixture(root)
            self.assertEqual([], check(root))

    def test_missing_promotion_authorization_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fixture(root, promotion=False)
            self.assertIn("missing promotion authorization", check(root)[0])

    def test_missing_snapshot_authorization_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fixture(root, snapshot=False)
            self.assertIn("missing snapshot authorization", check(root)[0])

    def test_stale_snapshot_candidate_hash_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            data = fixture(root)
            auth_path = root / "research/living/snapshot-authorizations-v1.0.json"
            auths = json.loads(auth_path.read_text())
            auths["authorizations"][0]["candidate_sha256"] = "0" * 64
            put(root, "research/living/snapshot-authorizations-v1.0.json", auths)
            with patch(
                "tools.check_living_project_change_obligations.git_show",
                side_effect=source_reader(data["proposal_raw"]),
            ):
                errors = check(root, "source")
            self.assertIn("snapshot authorization candidate hash mismatch", errors[0])

    def test_project_change_without_repository_operations_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            data = fixture(root)
            proposal = dict(data["proposal"])
            proposal["operations"] = []
            raw = (json.dumps(proposal) + "\n").encode()
            promotion_path = root / "research/living/promotion-authorizations-v1.0.json"
            auths = json.loads(promotion_path.read_text())
            auths["authorizations"][0]["proposal_sha256"] = promoter.h(raw)
            auths["authorizations"][0]["operations_sha256"] = promoter.canonical_json_sha([])
            put(root, "research/living/promotion-authorizations-v1.0.json", auths)
            with patch(
                "tools.check_living_project_change_obligations.git_show",
                side_effect=source_reader(raw),
            ):
                errors = check(root, "source")
            self.assertEqual(1, len(errors))
            self.assertIn("requires nonempty operations", errors[0])

    def test_complete_source_correction_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            data = fixture(root)
            with patch(
                "tools.check_living_project_change_obligations.git_show",
                side_effect=source_reader(data["proposal_raw"]),
            ):
                self.assertEqual([], check(root, "source"))


if __name__ == "__main__":
    unittest.main()
