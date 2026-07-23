from __future__ import annotations

import json
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULES = [
    "Canonicality",
    "RepresentationInvariance",
    "QuotientMinimality",
    "DefinitionalCompleteness",
    "ConservativeExtensibility",
    "MaximalKnowability",
    "CanonicalUniversalityTerminal",
]
REGISTRY = ROOT / "theory" / "terminal" / "canonical-universality-v1.0.json"
WORKFLOW = ROOT / ".github" / "workflows" / "lean.yml"


class CanonicalUniversalityAlignmentTests(unittest.TestCase):
    def setUp(self) -> None:
        self.sources = {
            name: (ROOT / "mechanization" / "lean" / f"{name}.lean").read_text(encoding="utf-8")
            for name in MODULES
        }
        self.registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
        self.workflow = WORKFLOW.read_text(encoding="utf-8")

    def test_no_axioms_or_admissions(self) -> None:
        for name, source in self.sources.items():
            code = re.sub(r"/-.*?-/", "", source, flags=re.DOTALL)
            code = re.sub(r"--.*", "", code)
            for token in (r"\baxiom\b", r"\bsorry\b", r"\badmit\b", r"\bunsafe\b"):
                self.assertIsNone(re.search(token, code), f"{name}: {token}")

    def test_six_independent_modules_registered(self) -> None:
        self.assertEqual(len(self.registry["modules"]), 6)
        for module in self.registry["modules"]:
            self.assertIn(module, self.sources)

    def test_terminal_requires_all_six(self) -> None:
        terminal = self.sources["CanonicalUniversalityTerminal"]
        for field in (
            "canonicality", "representationInvariance", "quotientMinimality",
            "definitionalCompleteness", "conservativeExtensibility", "maximalKnowability",
        ):
            self.assertIn(field, terminal)
        self.assertIn("missing_canonicality_blocks_terminal", terminal)

    def test_claim_boundary(self) -> None:
        claims = self.registry["claims"]
        self.assertFalse(claims["unrestricted_metaphysical_universality"])
        self.assertFalse(claims["unique_physical_ontology"])
        self.assertFalse(claims["inaccessible_systems_classified"])

    def test_workflow_compiles_every_module(self) -> None:
        for name in MODULES:
            self.assertIn(f"lean mechanization/lean/{name}.lean", self.workflow)
        self.assertIn("python -m unittest tests.test_canonical_universality_alignment", self.workflow)


if __name__ == "__main__":
    unittest.main()
