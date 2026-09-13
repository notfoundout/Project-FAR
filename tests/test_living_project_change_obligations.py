from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tools import reconcile_living_repo as living_reconcile
from tools.check_living_project_change_obligations import (
    CHANGE_DISPOSITION,
    REQUIRED_REVIEW_FIELDS,
    check,
)

ROOT = Path(__file__).resolve().parents[1]
CID = "FAR-LIT-0123456789ABCDEF"
PID = "FAR-LIVING-PROP-CRITICAL-001"


def put(root: Path, rel: str, value: object) -> None:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value) + "\n", encoding="utf-8")


def fixture(root: Path, *, promotion: bool = True, snapshot: bool = True) -> None:
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
    put(root, "research/living/review-dispositions-v1.0.json", {
        "allowed_dispositions": [CHANGE_DISPOSITION],
        "reviewed_candidates": [{
            "candidate_id": CID,
            "source_key": "doi:10.0000/example",
            "disposition": CHANGE_DISPOSITION,
            "reviewed_on": "2026-09-13",
            "review_basis": "docs/audits/example.md",
            "proposal_id": PID,
            "suppress_from_core_claim_review_queue": True,
        }]
    })
    put(root, "research/living/promotion-authorizations-v1.0.json", {
        "authorizations": [] if not promotion else [{
            "proposal_id": PID,
            "candidate_id": CID,
            "lifecycle_stage": "PROMOTION_PROPOSED",
            "authorization_status": "ACCEPTED_FOR_MECHANICAL_PROMOTION",
        }]
    })
    put(root, "research/living/snapshot-authorizations-v1.0.json", {
        "authorizations": [] if not snapshot else [{
            "candidate_id": CID,
            "source_key": "doi:10.0000/example",
            "disposition": CHANGE_DISPOSITION,
            "review_basis": "docs/audits/example.md",
            "authorization_status": "ACCEPTED_FOR_MECHANICAL_SNAPSHOT",
        }]
    })


def source_reader(*, operations: list[dict[str, str]]):
    proposal = json.dumps({
        "proposal_id": PID,
        "candidate_id": CID,
        "lifecycle_stage": "PROMOTION_PROPOSED",
        "operations": operations,
    }).encode()

    def read(_root: Path, _ref: str, path: str) -> bytes | None:
        if path.endswith(f"candidates/{CID}.json"):
            return b"{}\n"
        if path.endswith(f"promotion-proposals/{PID}.json"):
            return proposal
        if path.startswith(f"research/living/inbox/promotion-payloads/{PID}/"):
            return b"corrected bytes\n"
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

    def test_project_change_without_repository_operations_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fixture(root)
            with patch(
                "tools.check_living_project_change_obligations.git_show",
                side_effect=source_reader(operations=[]),
            ):
                errors = check(root, "source")
            self.assertEqual(1, len(errors))
            self.assertIn("requires nonempty operations", errors[0])

    def test_complete_source_correction_passes(self) -> None:
        operation = {
            "op": "write_file",
            "path": "docs/project-status.md",
            "source_path": f"research/living/inbox/promotion-payloads/{PID}/docs/project-status.md",
        }
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            fixture(root)
            with patch(
                "tools.check_living_project_change_obligations.git_show",
                side_effect=source_reader(operations=[operation]),
            ):
                self.assertEqual([], check(root, "source"))


if __name__ == "__main__":
    unittest.main()
