"""The bootstrap verifier pins each protected check's whole definition, and its own lock is pinned.

Adversarial probe V3 pointed `governance.claim-boundaries` at a different checker: the flag, severity,
and profile membership were unchanged, so `validation_bootstrap/verify.py` passed. The protected set
itself lived in `bootstrap-lock.json`, which no assurance pin covered, so a candidate could also drop
a check from the manifest and the lock together.
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BOOTSTRAP_LOCK = "validation_bootstrap/bootstrap-lock.json"
MANIFEST = "validation/manifest.json"


class ProtectedCheckDefinitionTests(unittest.TestCase):
    def setUp(self) -> None:
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        assurance = json.loads((ROOT / "validation_bootstrap" / "assurance-lock.json").read_text(encoding="utf-8"))
        needed = {MANIFEST, BOOTSTRAP_LOCK, "validation_bootstrap/assurance-lock.json",
                  assurance["workflow"]["path"], assurance["runtime_policy"], *assurance["files"]}
        for relative in needed:
            (self.root / relative).parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / relative, self.root / relative)

    def _edit(self, relative: str, change) -> None:
        path = self.root / relative
        data = json.loads(path.read_text(encoding="utf-8"))
        change(data)
        path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")

    def _check(self, data: dict, check_id: str) -> dict:
        return next(check for check in data["checks"] if check["id"] == check_id)

    def _verify(self) -> subprocess.CompletedProcess[str]:
        return subprocess.run([sys.executable, str(self.root / "validation_bootstrap" / "verify.py")],
                              capture_output=True, text=True, check=False)

    def test_unchanged_repository_verifies(self) -> None:
        completed = self._verify()
        self.assertEqual(completed.returncode, 0, completed.stderr)

    def test_protected_check_pointed_at_another_checker_is_rejected(self) -> None:
        self._edit(MANIFEST, lambda data: self._check(data, "governance.claim-boundaries").update(
            command=["python", "tools/check_p8_theorem_role.py"]))
        completed = self._verify()
        self.assertEqual(completed.returncode, 1)
        self.assertIn("protected check definition changed: governance.claim-boundaries", completed.stderr)

    def test_narrowed_protected_check_inputs_are_rejected(self) -> None:
        self._edit(MANIFEST, lambda data: self._check(data, "governance.research-gates").update(inputs=[]))
        self.assertIn("protected check definition changed: governance.research-gates", self._verify().stderr)

    def test_unprotected_check_may_change(self) -> None:
        self._edit(MANIFEST, lambda data: self._check(data, "research.p8-role").update(title="renamed"))
        completed = self._verify()
        self.assertEqual(completed.returncode, 0, completed.stderr)

    def test_definition_pins_must_cover_exactly_the_protected_set(self) -> None:
        self._edit(BOOTSTRAP_LOCK, lambda data: data["protected_check_definitions"].pop("governance.w5-authorization"))
        self.assertIn("protected check definition pins must name exactly the protected checks", self._verify().stderr)

    def test_unprotecting_a_check_in_manifest_and_lock_together_breaks_the_lock_pin(self) -> None:
        check_id = "governance.w5-authorization"

        def unprotect_manifest(data: dict) -> None:
            data["protected_checks"].remove(check_id)
            self._check(data, check_id)["protected"] = False

        def unprotect_lock(data: dict) -> None:
            data["protected_checks"].remove(check_id)
            data["protected_check_definitions"].pop(check_id)

        self._edit(MANIFEST, unprotect_manifest)
        self._edit(BOOTSTRAP_LOCK, unprotect_lock)
        completed = self._verify()
        self.assertEqual(completed.returncode, 1)
        self.assertIn(f"assurance file hash mismatch: {BOOTSTRAP_LOCK}", completed.stderr)


if __name__ == "__main__":
    unittest.main()
