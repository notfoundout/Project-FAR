from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from tools.check_far_evidence_closure import (
    CONTRACT_ID,
    REQUIREMENT_IDS,
    SURFACES,
    VALIDATION_ANCHORS,
    WORKFLOW_ANCHORS,
    validate,
)

ROOT = Path(__file__).resolve().parents[1]


class FarEvidenceClosurePolicyTests(unittest.TestCase):
    def test_repository_policy_is_aligned(self) -> None:
        self.assertEqual(validate(ROOT), [])

    def _write_minimal_valid_fixture(self, root: Path) -> None:
        for name, relative in SURFACES.items():
            path = root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            body = [CONTRACT_ID]
            if name == "workflow":
                body.extend(REQUIREMENT_IDS)
                body.extend(WORKFLOW_ANCHORS)
                body.append(
                    "A decisive claim-level disposition does not by itself authorize investigation closure."
                )
            if name == "validation":
                body.extend(REQUIREMENT_IDS)
                body.extend(VALIDATION_ANCHORS)
                body.append(
                    "A decisive atomic verdict is not evidence that the closure gate passed."
                )
            path.write_text("\n".join(body) + "\n", encoding="utf-8")

    def test_missing_integration_reference_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._write_minimal_valid_fixture(root)
            target = root / SURFACES["research_quality_gate"]
            target.write_text("quality gate without closure contract\n", encoding="utf-8")
            errors = validate(root)
            self.assertIn(
                f"{SURFACES['research_quality_gate'].as_posix()}: missing {CONTRACT_ID} reference",
                errors,
            )

    def test_missing_requirement_id_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._write_minimal_valid_fixture(root)
            workflow = root / SURFACES["workflow"]
            workflow.write_text(
                workflow.read_text(encoding="utf-8").replace("EC-07\n", ""),
                encoding="utf-8",
            )
            self.assertIn("workflow missing closure requirement EC-07", validate(root))

    def test_missing_terminal_saturation_anchor_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._write_minimal_valid_fixture(root)
            validation = root / SURFACES["validation"]
            validation.write_text(
                validation.read_text(encoding="utf-8").replace(
                    "terminal bounded saturation pass\n", ""
                ),
                encoding="utf-8",
            )
            self.assertIn(
                "investigation validation missing evidence-closure anchor: terminal bounded saturation pass",
                validate(root),
            )


if __name__ == "__main__":
    unittest.main()
