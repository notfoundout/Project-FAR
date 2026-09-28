"""Regression: a candidate may never protect the consumption ledger with the ledger's own lock."""
from __future__ import annotations

import hashlib
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from far_validation import repin
from far_validation import repin_signature as sig

GOLDEN_KEY = (
    "AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBMCSXvifSs8+c1itwJlTtXPGUsAslwZ+AOL26ASFmHqMp8JpEL0IdNY5Jc+34InF141oFATvy+2zfEtCOd0wQOQ="
)


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


class CandidateLedgerLockTests(unittest.TestCase):
    def test_candidate_cannot_newly_add_consumption_ledger_to_assurance_lock(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.run(["git", "init", "-q", "-b", "main", str(root)], check=True)
            subprocess.run(["git", "-C", str(root), "config", "user.name", "test"], check=True)
            subprocess.run(["git", "-C", str(root), "config", "user.email", "test@example.invalid"], check=True)

            policy_path = "validation/runtime-policy.json"
            policy = b'{"network_policy":"deny"}\n'
            ledger = (json.dumps({"schema_version": repin.LEDGER_SCHEMA, "consumptions": []}, indent=2) + "\n").encode()
            signers = f'{sig.PRINCIPAL} namespaces="{sig.NAMESPACE}" {sig.KEY_TYPE} {GOLDEN_KEY}\n'.encode()

            def write(relative: str, data: bytes) -> None:
                target = root / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(data)

            write(policy_path, policy)
            write(repin.ALLOWED_SIGNERS_PATH, signers)
            write(repin.CONSUMPTIONS_PATH, ledger)
            base_lock = {
                "schema_version": "1.0",
                "files": {
                    policy_path: digest(policy),
                    repin.ALLOWED_SIGNERS_PATH: digest(signers),
                },
            }
            write(repin.ASSURANCE_LOCK_PATH, (json.dumps(base_lock, indent=2, sort_keys=True) + "\n").encode())
            subprocess.run(["git", "-C", str(root), "add", "-A"], check=True)
            subprocess.run(["git", "-C", str(root), "commit", "-qm", "base"], check=True)
            base = subprocess.check_output(["git", "-C", str(root), "rev-parse", "HEAD"], text=True).strip()
            subprocess.run(["git", "-C", str(root), "checkout", "-qb", "candidate"], check=True)

            candidate_lock = json.loads((root / repin.ASSURANCE_LOCK_PATH).read_text(encoding="utf-8"))
            candidate_lock["files"][repin.CONSUMPTIONS_PATH] = digest(ledger)
            write(repin.ASSURANCE_LOCK_PATH, (json.dumps(candidate_lock, indent=2, sort_keys=True) + "\n").encode())
            subprocess.run(["git", "-C", str(root), "add", "-A"], check=True)
            subprocess.run(["git", "-C", str(root), "commit", "-qm", "candidate protects ledger"], check=True)

            report = repin.evaluate(
                repin.GitObjects(root), base, "HEAD", allowed_signers=signers,
                repository="notfoundout/Project-FAR", repository_id=1283452680, target_pr=538,
            )
            self.assertFalse(report.successful, report.to_dict())
            self.assertIn(repin.CONSUMPTIONS_PATH, report.failures)
            self.assertTrue(any("deadlock" in message for message in report.failures[repin.CONSUMPTIONS_PATH]))


if __name__ == "__main__":
    unittest.main()
