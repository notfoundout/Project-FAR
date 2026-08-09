from __future__ import annotations

import importlib.util
import json
import shutil
import sys
import tempfile
import unittest
from fractions import Fraction
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
DIR = ROOT / "research/external-validation/swe-agent-v3"
PATH = DIR / "verify_amendment_v1_1.py"
SPEC = importlib.util.spec_from_file_location("swe_v3_amendment", PATH)
assert SPEC and SPEC.loader
module = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = module
SPEC.loader.exec_module(module)


class AmendmentTests(unittest.TestCase):
    def test_canonical(self) -> None:
        amendment = module.validate()
        self.assertEqual(amendment["authority"]["outcome_exposure_status"], "none")
        self.assertFalse(amendment["authority"]["execution_authorized"])
        self.assertEqual(amendment["authority"]["contract_role"], "standalone_current_prospective_authority")
        self.assertEqual(amendment["authority"]["historical_context"], "historical-authority-v1.0.json")
        self.assertFalse(amendment["authority"]["historical_provenance_required_for_current_validity"])

    def test_taxonomy_is_closed_disjoint_and_nondiscretionary(self) -> None:
        contract = module.validate()["replacement_contract"]
        classes = contract["terminal_reason_classes"]
        flat = [item for values in classes.values() for item in values]
        self.assertEqual(len(flat), len(set(flat)))
        self.assertFalse(contract["operator_discretion_permitted"])
        self.assertIn("provider_timeout_or_failure_after_request_acceptance", classes["unresolved_nonreplaceable"])
        self.assertNotIn("provider_timeout_or_failure_after_request_acceptance", classes["infrastructure_invalid_replacement_eligible"])
        self.assertIn("never retroactively reclassify", contract["unlisted_terminal_reason_rule"])

    def test_exact_arithmetic_boundaries(self) -> None:
        self.assertEqual(module.probability(2, 3) - module.probability(1, 3), Fraction(1, 3))
        self.assertEqual(module.classify(Fraction(1, 10), Fraction(1, 100), Fraction(1, 10)), "bounded_positive")
        self.assertEqual(module.classify(Fraction(0), Fraction(-1, 100), Fraction(999, 10000)), "no_practical_advantage")
        self.assertEqual(module.classify(Fraction(-1, 100), Fraction(-1, 50), Fraction(-1, 1000)), "bounded_harm")
        values = [Fraction(0), Fraction(1, 3), Fraction(2, 3), Fraction(1)]
        self.assertEqual(module.type7(values, Fraction(1, 40)), Fraction(1, 40))
        self.assertEqual(module.type7(values, Fraction(39, 40)), Fraction(39, 40))

    def test_amendment_semantic_mutations_fail(self) -> None:
        source = DIR / "failure-arithmetic-amendment-v1.1.json"
        data = json.loads(source.read_text(encoding="utf-8"))
        mutations = (
            lambda d: d["replacement_contract"]["terminal_reason_classes"]["infrastructure_invalid_replacement_eligible"].append("provider_timeout_or_failure_after_request_acceptance"),
            lambda d: d["replacement_contract"].__setitem__("operator_discretion_permitted", 0),
            lambda d: d["exact_arithmetic_contract"]["classification_thresholds"]["minimum_practical_difference"].__setitem__("denominator", 20),
            lambda d: d["authority"].__setitem__("execution_authorized", 0),
            lambda d: d["authority"].__setitem__("precedence", "historical v1.0 controls everything"),
            lambda d: d["authority"].__setitem__("historical_provenance_required_for_current_validity", True),
        )
        for mutation in mutations:
            altered = json.loads(json.dumps(data))
            mutation(altered)
            with tempfile.TemporaryDirectory() as tmp:
                path = Path(tmp) / source.name
                path.write_text(json.dumps(altered, indent=2) + "\n", encoding="utf-8")
                with self.assertRaises(module.AmendmentError):
                    module.validate(amend=path)

    def _historical_fixture(self, tmp: str) -> tuple[Path, Path]:
        root = Path(tmp)
        here = root / "research/external-validation/swe-agent-v3"
        history = here / "historical-base-83c951"
        history.mkdir(parents=True)
        shutil.copy2(DIR / "historical-authority-v1.0.json", here / "historical-authority-v1.0.json")
        shutil.copy2(DIR / "historical-base-83c951/preregistration-v1.0.json", history / "preregistration-v1.0.json")
        shutil.copy2(DIR / "historical-base-83c951/evidence-and-analysis-plan-v1.0.md", history / "evidence-and-analysis-plan-v1.0.md")
        return here, here / "historical-authority-v1.0.json"

    def test_historical_authority_validates_without_git_history(self) -> None:
        source = PATH.read_text(encoding="utf-8")
        for token in ("import subprocess", "rev-parse", "cat-file", "merge-base", "--is-ancestor", "git fetch"):
            self.assertNotIn(token, source)
        with tempfile.TemporaryDirectory() as tmp:
            here, authority = self._historical_fixture(tmp)
            with mock.patch.object(module, "HERE", here):
                result = module.validate_historical_authority(authority)
            self.assertEqual(result["authority_status"], "archival_context_not_live_authority")
            self.assertFalse(result["current_design_authority"])
            self.assertEqual(result["provenance_status"], "not_self_proving")

    def test_historical_snapshot_byte_mutation_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            here, authority = self._historical_fixture(tmp)
            snapshot = here / "historical-base-83c951/preregistration-v1.0.json"
            snapshot.write_bytes(snapshot.read_bytes() + b"\n")
            with mock.patch.object(module, "HERE", here):
                with self.assertRaises(module.AmendmentError):
                    module.validate_historical_authority(authority)

    def test_missing_historical_snapshot_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            here, authority = self._historical_fixture(tmp)
            (here / "historical-base-83c951/evidence-and-analysis-plan-v1.0.md").unlink()
            with mock.patch.object(module, "HERE", here):
                with self.assertRaises(module.AmendmentError):
                    module.validate_historical_authority(authority)

    def test_false_historical_blob_claim_and_bool_int_drift_fail(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            here, authority = self._historical_fixture(tmp)
            base = json.loads(authority.read_text(encoding="utf-8"))
            mutations = (
                lambda d: d["snapshots"][0].__setitem__("archived_git_blob_sha1", "0" * 40),
                lambda d: d.__setitem__("current_design_authority", 0),
                lambda d: d.__setitem__("execution_authorized", 0),
            )
            for mutation in mutations:
                altered = json.loads(json.dumps(base)); mutation(altered)
                authority.write_text(json.dumps(altered, indent=2) + "\n", encoding="utf-8")
                with mock.patch.object(module, "HERE", here):
                    with self.assertRaises(module.AmendmentError):
                        module.validate_historical_authority(authority)
                authority.write_text(json.dumps(base, indent=2) + "\n", encoding="utf-8")

    def test_stale_narrative_precedence_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            readme = Path(tmp) / "AMENDMENT-v1.1.md"
            readme.write_text((DIR / "AMENDMENT-v1.1.md").read_text(encoding="utf-8") + "\nAll other v1.0 design fields remain unchanged.\n", encoding="utf-8")
            with self.assertRaises(module.AmendmentError):
                module.validate(readme=readme)


if __name__ == "__main__":
    unittest.main()
