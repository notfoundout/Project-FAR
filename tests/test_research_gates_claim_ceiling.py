"""The protected research-gate check enforces the central-claim status ceilings."""
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLAIMS = "theory/evaluation/central-claim-registry.json"


class ResearchGateClaimCeilingTest(unittest.TestCase):
    def run_gate(self, root: Path) -> subprocess.CompletedProcess:
        return subprocess.run([sys.executable, "tools/check_research_gates.py"], cwd=root, capture_output=True, text=True)

    def test_repository_passes(self):
        completed = self.run_gate(ROOT)
        self.assertEqual(0, completed.returncode, completed.stdout)

    def test_unpinned_claim_promotion_fails_the_protected_gate(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "repo"
            shutil.copytree(ROOT / "tools", root / "tools", ignore=shutil.ignore_patterns("__pycache__"))
            shutil.copytree(ROOT / "theory/evaluation", root / "theory/evaluation")
            path = root / CLAIMS
            data = json.loads(path.read_text(encoding="utf-8"))
            for claim in data["claims"]:
                if claim["id"] in {"CLM-EXISTENCE", "CLM-ECONOMY", "CLM-INDEPENDENCE"}:
                    claim["current_status"] = "supported"
            path.write_text(json.dumps(data), encoding="utf-8")
            completed = self.run_gate(root)
            self.assertEqual(1, completed.returncode, completed.stdout)
            self.assertEqual(3, completed.stdout.count("exceeds governed ceiling"), completed.stdout)


if __name__ == "__main__":
    unittest.main()
