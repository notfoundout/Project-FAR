import json
import pathlib
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
BASE = ROOT / "theory" / "scope" / "ISD-001"
REGISTRY = BASE / "scope-registry.json"
REPORT = BASE / "README.md"


class IndependentScopeDefinitionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
        self.report = REPORT.read_text(encoding="utf-8")

    def test_scope_claim_is_bounded(self) -> None:
        self.assertEqual("bounded-current-scope", self.registry["status"])
        self.assertEqual("demonstrated-representational-scope", self.registry["claim_level"])
        self.assertIn("current demonstrated scope is narrow and explicit", self.report)

    def test_included_classes_have_evidence_and_boundaries(self) -> None:
        included = self.registry["included_classes"]
        self.assertEqual(3, len(included), msg=f"expected exactly 3 included classes, observed {len(included)}")
        for entry in included:
            self.assertEqual("included", entry["status"], msg=f"{entry['id']} has status {entry['status']}")
            self.assertTrue(entry["evidence"], msg=f"{entry['id']} has no evidence")
            self.assertTrue(entry["boundary"].strip(), msg=f"{entry['id']} has no boundary")

    def test_unresolved_domains_are_not_promoted(self) -> None:
        observed = {entry["class"]: entry["status"] for entry in self.registry["investigated_but_unresolved_classes"]}
        expected = {
            "large-language-model reasoning": "unresolved",
            "agentic AI reasoning": "unresolved",
            "human expert reasoning": "unresolved",
            "analogical reasoning": "unresolved",
            "legal reasoning": "conservative-extension",
        }
        self.assertEqual(expected, observed, msg=f"scope classification mismatch: expected {expected!r}, observed {observed!r}")

    def test_universal_claims_are_explicitly_excluded(self) -> None:
        exclusions = set(self.registry["excluded_from_current_claims"])
        required = {
            "all human reasoning",
            "all artificial intelligence reasoning",
            "universal necessity, global minimality, or unique optimality",
        }
        self.assertTrue(required.issubset(exclusions), msg=f"missing exclusions: {sorted(required - exclusions)}")
        prohibited_affirmations = (
            "Project FAR covers all reasoning",
            "Project FAR is universal",
            "universal coverage is established",
        )
        for statement in prohibited_affirmations:
            self.assertNotIn(statement, self.report, msg=f"prohibited affirmative scope claim found: {statement!r}")

    def test_scope_expansion_has_required_controls(self) -> None:
        requirements = self.registry["scope_expansion_requirements"]
        joined = "\n".join(requirements)
        for phrase in (
            "freeze a representative benchmark",
            "three independent mappings",
            "all six preservation dimensions",
            "domain-specific extensions",
            "alternative-vocabulary comparison",
        ):
            self.assertIn(phrase, joined, msg=f"scope expansion control missing: {phrase!r}")


if __name__ == "__main__":
    unittest.main()
