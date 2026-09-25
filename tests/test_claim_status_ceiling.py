import copy
import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("claim_status_ceiling", ROOT / "tools/check_claim_status_ceiling.py")
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(MODULE)
DATA = json.loads(MODULE.CLAIMS.read_text(encoding="utf-8"))


def with_status(**statuses):
    data = copy.deepcopy(DATA)
    for claim in data["claims"]:
        key = claim["id"].replace("CLM-", "").replace("-", "_")
        if key in statuses:
            claim["current_status"] = statuses[key]
    return data


class ClaimStatusCeilingTest(unittest.TestCase):
    def test_registry_is_at_or_below_every_ceiling(self):
        self.assertEqual([], MODULE.validate())

    def test_checker_command_passes(self):
        completed = subprocess.run([sys.executable, "tools/check_claim_status_ceiling.py"], cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(0, completed.returncode, completed.stdout + completed.stderr)

    def test_ceilings_cover_exactly_the_registered_claims(self):
        self.assertEqual({claim["id"] for claim in DATA["claims"]}, set(MODULE.CEILINGS))

    def test_every_ceiling_is_a_ranked_status(self):
        for cid, ceiling in MODULE.CEILINGS.items():
            self.assertIn(ceiling, MODULE.STATUS_RANK, cid)

    def test_promotion_of_each_claim_is_rejected(self):
        for cid, ceiling in MODULE.CEILINGS.items():
            for status, rank in MODULE.STATUS_RANK.items():
                if rank <= MODULE.STATUS_RANK[ceiling]:
                    continue
                data = copy.deepcopy(DATA)
                next(c for c in data["claims"] if c["id"] == cid)["current_status"] = status
                errors = MODULE.validate(data)
                self.assertTrue(any(cid in e and "exceeds governed ceiling" in e for e in errors), (cid, status, errors))

    def test_audit_promotions_are_rejected(self):
        # The three-claim promotion that passed every test and health check before this checker.
        errors = MODULE.validate(with_status(EXISTENCE="supported", ECONOMY="supported", INDEPENDENCE="supported"))
        self.assertEqual(3, sum("exceeds governed ceiling" in e for e in errors), errors)
        self.assertTrue(MODULE.validate(with_status(UNIVERSALITY="partially_supported")))
        self.assertTrue(MODULE.validate(with_status(NECESSITY="supported_at_registered_control_scope")))

    def test_demotion_is_allowed(self):
        self.assertEqual([], MODULE.validate(with_status(REP_CAPACITY="unresolved", NONTRIVIALITY="weakened", SUFFICIENCY="refuted")))

    def test_unknown_status_is_rejected(self):
        errors = MODULE.validate(with_status(EXISTENCE="established"))
        self.assertTrue(any("unranked status 'established'" in e for e in errors), errors)

    def test_unregistered_claim_is_rejected(self):
        data = copy.deepcopy(DATA)
        data["claims"].append({"id": "CLM-NEW", "current_status": "unresolved"})
        self.assertTrue(any("CLM-NEW: no governed status ceiling" in e for e in MODULE.validate(data)))

    def test_removed_claim_is_rejected(self):
        data = copy.deepcopy(DATA)
        data["claims"] = [c for c in data["claims"] if c["id"] != "CLM-NECESSITY"]
        self.assertTrue(any("claims removed from registry: CLM-NECESSITY" in e for e in MODULE.validate(data)))

    def test_duplicate_claim_is_rejected(self):
        data = copy.deepcopy(DATA)
        data["claims"].append(copy.deepcopy(data["claims"][0]))
        self.assertTrue(any("duplicate claim id" in e for e in MODULE.validate(data)))

    def test_positive_status_without_scope_is_rejected(self):
        data = copy.deepcopy(DATA)
        claim = next(c for c in data["claims"] if c["id"] == "CLM-REP-CAPACITY")
        claim["maximum_supported_scope"] = "none"
        self.assertTrue(any("with no supported scope" in e for e in MODULE.validate(data)))

    def test_missing_claims_list_is_rejected(self):
        self.assertEqual(["central claim registry requires a claims list"], MODULE.validate({}))


if __name__ == "__main__":
    unittest.main()
