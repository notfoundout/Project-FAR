from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from far_validation.assured_engine import ValidationEngine
from far_validation.certificate import CertificateError, verify_certificate, write_certificate
from far_validation.formal_model import exhaustive_model_check
from far_validation.oracle import analyze_checker_source, run_oracle
from far_validation.tracing import RuntimePolicy, audit_trace, parse_strace
from far_validation.trust import HMACTrust, TrustError, read_attestation, write_attestation
from far_validation.weakening import detect_weakening


class SignedTrustTests(unittest.TestCase):
    def test_signed_attestation_rejects_payload_tamper(self) -> None:
        trust = HMACTrust(key=b"secret", trust_domain="test", key_id="test")
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "signed.json"
            write_attestation(path, trust=trust, kind="cache-result", payload={"value": 1})
            self.assertEqual(read_attestation(path, trust=trust, kind="cache-result"), {"value": 1})
            envelope = json.loads(path.read_text(encoding="utf-8"))
            envelope["payload"]["value"] = 2
            path.write_text(json.dumps(envelope), encoding="utf-8")
            with self.assertRaises(TrustError):
                read_attestation(path, trust=trust, kind="cache-result")

    def test_cross_runner_cache_requires_same_trust_domain_and_key(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "validation").mkdir()
            (root / "check.py").write_text("print('ok')\n", encoding="utf-8")
            manifest = {
                "schema_version": "1.0",
                "profiles": {"pr-fast": ["x"]},
                "protected_checks": [],
                "global_invalidation_paths": [],
                "checks": [{
                    "id": "x", "title": "x", "command": [sys.executable, "check.py"],
                    "profiles": ["pr-fast"], "inputs": ["check.py"],
                }],
            }
            (root / "validation" / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
            trust_a = HMACTrust(key=b"shared", trust_domain="ci", key_id="shared")
            first = ValidationEngine(root, jobs=1, trust=trust_a).run(profile="pr-fast")
            self.assertTrue(first.successful)
            second = ValidationEngine(root, jobs=1, trust=trust_a).run(profile="pr-fast")
            self.assertTrue(second.results[0].cache_hit)
            self.assertTrue(second.results[0].cache_signature_verified)
            trust_b = HMACTrust(key=b"wrong", trust_domain="ci", key_id="wrong")
            third = ValidationEngine(root, jobs=1, trust=trust_b).run(profile="pr-fast")
            self.assertFalse(third.results[0].cache_hit)


class RuntimeTraceTests(unittest.TestCase):
    def test_trace_parser_and_policy_reject_undeclared_access(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            raw = (
                f'openat(AT_FDCWD, "{root / "allowed.txt"}", O_RDONLY|O_CLOEXEC) = 3\n'
                f'openat(AT_FDCWD, "{root / "secret.txt"}", O_RDONLY|O_CLOEXEC) = 3\n'
                f'openat(AT_FDCWD, "{root / "README.md"}", O_WRONLY|O_CREAT|O_TRUNC, 0666) = 3\n'
                'execve("/usr/bin/curl", ["curl"], 0x0) = 0\n'
                'connect(3, {sa_family=AF_INET, sin_port=htons(443)}, 16) = 0\n'
            )
            report = parse_strace(raw, cwd=root, root=root)
            policy = RuntimePolicy((), (".far/**",), ("python",), (), True)
            audited = audit_trace(
                report, declared_inputs=("allowed.txt",), declared_outputs=(),
                command=("python", "check.py"), policy=policy, sandbox_copy=False,
            )
            joined = "\n".join(audited.violations)
            self.assertIn("undeclared read: secret.txt", joined)
            self.assertIn("undeclared write: README.md", joined)
            self.assertIn("undeclared executable", joined)
            self.assertIn("network access denied", joined)


class IndependentOracleTests(unittest.TestCase):
    def test_oracle_rejects_trivial_checker(self) -> None:
        finding = analyze_checker_source("print('PASS')\n", "check.py")
        self.assertFalse(finding.accepted)

    def test_oracle_covers_manifest_and_discovered_checker(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "validation").mkdir()
            (root / "tools").mkdir()
            source = (
                "from pathlib import Path\n"
                "def fail(message): raise SystemExit(message)\n"
                "def main():\n"
                "    path = Path('x.json')\n"
                "    if not path.exists(): fail('missing')\n"
                "    if path.read_text() != 'ok': fail('bad')\n"
                "    print('PASS')\n"
                "if __name__ == '__main__': main()\n"
            )
            (root / "tools" / "check_one.py").write_text(source, encoding="utf-8")
            (root / "x.json").write_text("ok", encoding="utf-8")
            manifest = {
                "schema_version": "1.0", "profiles": {"pr-fast": ["one"]},
                "protected_checks": [], "global_invalidation_paths": [],
                "checks": [{
                    "id": "one", "title": "one", "command": [sys.executable, "tools/check_one.py"],
                    "profiles": ["pr-fast"], "inputs": ["x.json", "tools/check_one.py"],
                    "failure_code": "FAR-VAL-ONE-001",
                }],
            }
            (root / "validation" / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
            report = run_oracle(root)
            self.assertTrue(report.successful, report.to_dict())
            self.assertEqual(report.manifest_command_count, 1)


class WeakeningTests(unittest.TestCase):
    def test_removed_test_and_assertion_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=root, check=True)
            subprocess.run(["git", "config", "user.name", "Test"], cwd=root, check=True)
            (root / "tests").mkdir()
            path = root / "tests" / "test_a.py"
            path.write_text(
                "import unittest\nclass T(unittest.TestCase):\n"
                "    def test_a(self): self.assertTrue(True)\n"
                "    def test_b(self): self.assertEqual(1, 1)\n",
                encoding="utf-8",
            )
            subprocess.run(["git", "add", "."], cwd=root, check=True)
            subprocess.run(["git", "commit", "-qm", "base"], cwd=root, check=True)
            base = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip()
            path.write_text("import unittest\nclass T(unittest.TestCase):\n    def test_a(self): pass\n", encoding="utf-8")
            subprocess.run(["git", "add", "."], cwd=root, check=True)
            subprocess.run(["git", "commit", "-qm", "weak"], cwd=root, check=True)
            report = detect_weakening(root, base=base)
            self.assertFalse(report.successful)


class FormalAndCertificateTests(unittest.TestCase):
    def test_formal_model_exhausts_bounded_state_space(self) -> None:
        result = exhaustive_model_check(4)
        self.assertGreater(result["runs"], 100)
        self.assertEqual(result["attestation_mutations"], 5)

    def test_certificate_is_bound_to_commit_tree_and_required_checks(self) -> None:
        trust = HMACTrust(key=b"cert", trust_domain="test", key_id="cert")
        run = {
            "run_id": "r", "profile": "release", "commit_sha": "a" * 40, "tree_sha": "b" * 40,
            "base_sha": "c" * 40, "manifest_hash": "d" * 64, "successful": True,
            "root_failures": [], "selected_checks": ["bootstrap.manifest"], "results": [],
        }
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "certificate.json"
            old = os.environ.get("GITHUB_EVENT_NAME")
            os.environ["GITHUB_EVENT_NAME"] = "merge_group"
            try:
                write_certificate(path, run, trust=trust)
            finally:
                if old is None:
                    os.environ.pop("GITHUB_EVENT_NAME", None)
                else:
                    os.environ["GITHUB_EVENT_NAME"] = old
            verify_certificate(
                path, trust=trust, expected_commit="a" * 40, expected_tree="b" * 40,
                required_checks=["bootstrap.manifest"],
            )
            with self.assertRaises(CertificateError):
                verify_certificate(path, trust=trust, expected_commit="e" * 40, expected_tree="b" * 40)


if __name__ == "__main__":
    unittest.main()
