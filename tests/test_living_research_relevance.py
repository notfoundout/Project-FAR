from __future__ import annotations

from pathlib import Path
import unittest

from tools import run_living_research as lr


class LivingResearchRelevanceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        root = Path(__file__).resolve().parents[1]
        config = lr.read_json(root / lr.CONFIG_PATH)
        cls.target = next(
            target for target in config["targets"] if target["target_id"] == "FAR-RQ-009"
        )

    def test_generic_impossibility_is_not_a_core_threat_signal(self) -> None:
        terms = self.target["signal_terms"]
        self.assertNotIn("impossibility", terms)
        self.assertEqual(
            lr.hits("an impossibility theorem for spontaneously rotating time crystals", terms),
            [],
        )

    def test_specific_representation_threats_remain_discoverable(self) -> None:
        terms = self.target["signal_terms"]
        self.assertIn("minimal sufficient", terms)
        self.assertIn(
            "minimal sufficient",
            lr.hits("minimal sufficient algebraic projections of proof certificates", terms),
        )
        hits = lr.hits("observational quotient impossibility theorem", terms)
        self.assertIn("observational", hits)
        self.assertIn("quotient", hits)


if __name__ == "__main__":
    unittest.main()
