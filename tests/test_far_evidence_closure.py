from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from tools.check_far_evidence_closure import (
    ACCEPTANCE_LIFECYCLE_ANCHORS,
    AUDIT_PASSING_POLARITY,
    CANONICAL_MAP_ANCHORS,
    CONTRACT_ID,
    REPLICATION_PATH,
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
            if name == "canonical_map":
                body.extend(CANONICAL_MAP_ANCHORS)
            if name == "acceptance":
                body.extend(
                    [
                        "## Question",
                        "## Execution",
                        "## Observation",
                        "## Discovery",
                        "## Replication",
                        REPLICATION_PATH.as_posix(),
                        "## Acceptance",
                        "## Promotion",
                    ]
                )
            if name == "methodology_audit":
                body.append(AUDIT_PASSING_POLARITY)
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

    def test_empty_required_surface_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._write_minimal_valid_fixture(root)
            target = root / SURFACES["research_quality_gate"]
            target.write_text("\n", encoding="utf-8")
            errors = validate(root)
            self.assertIn(
                f"empty required evidence-closure surface: {SURFACES['research_quality_gate'].as_posix()}",
                errors,
            )
            self.assertIn(
                f"{SURFACES['research_quality_gate'].as_posix()}: missing {CONTRACT_ID} reference",
                errors,
            )

    def test_all_empty_surfaces_cannot_self_certify(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._write_minimal_valid_fixture(root)
            for relative in SURFACES.values():
                (root / relative).write_text("", encoding="utf-8")
            errors = validate(root)
            self.assertGreaterEqual(
                sum(error.startswith("empty required evidence-closure surface:") for error in errors),
                len(SURFACES),
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

    def test_canonical_map_must_register_closure_authorities(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._write_minimal_valid_fixture(root)
            canonical_map = root / SURFACES["canonical_map"]
            canonical_map.write_text(
                canonical_map.read_text(encoding="utf-8").replace(
                    "FAR Evidence-Closure Contract\n", ""
                ),
                encoding="utf-8",
            )
            self.assertIn(
                "canonical map missing evidence-closure authority anchor: FAR Evidence-Closure Contract",
                validate(root),
            )

    def test_acceptance_requires_replication_before_acceptance(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._write_minimal_valid_fixture(root)
            acceptance = root / SURFACES["acceptance"]
            text = acceptance.read_text(encoding="utf-8")
            text = text.replace("## Replication\n", "")
            acceptance.write_text(text, encoding="utf-8")
            self.assertIn(
                "evidence-closure acceptance missing lifecycle anchor: ## Replication",
                validate(root),
            )

    def test_acceptance_rejects_out_of_order_lifecycle(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._write_minimal_valid_fixture(root)
            acceptance = root / SURFACES["acceptance"]
            acceptance.write_text(
                "\n".join(
                    [
                        CONTRACT_ID,
                        "## Question",
                        "## Execution",
                        "## Observation",
                        "## Discovery",
                        "## Acceptance",
                        "## Replication",
                        REPLICATION_PATH.as_posix(),
                        "## Promotion",
                    ]
                )
                + "\n",
                encoding="utf-8",
            )
            self.assertIn(
                "evidence-closure acceptance lifecycle stages are out of order",
                validate(root),
            )

    def test_methodology_audit_requires_affirmative_passing_polarity(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self._write_minimal_valid_fixture(root)
            audit = root / SURFACES["methodology_audit"]
            audit.write_text(
                f"{CONTRACT_ID}\nDid a decisive witness, counterexample, proof, or authoritative record cause the investigation to stop before the gate was satisfied?\n",
                encoding="utf-8",
            )
            errors = validate(root)
            self.assertIn(
                "methodology audit does not encode affirmative passing polarity for post-decisive continuation",
                errors,
            )
            self.assertIn(
                "methodology audit retains the inverted premature-stopping closure question",
                errors,
            )


if __name__ == "__main__":
    unittest.main()
