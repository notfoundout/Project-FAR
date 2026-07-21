from __future__ import annotations

import json
import os
import subprocess
import tempfile
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Callable

from .certificate import verify_certificate, write_certificate
from .formal_model import exhaustive_model_check
from .oracle import _manifest_commands, _mutations, analyze_checker_source, discover_legacy_checkers
from .tracing import RuntimePolicy, TraceReport, audit_trace
from .trust import HMACTrust, read_attestation, write_attestation
from .weakening import detect_weakening


@dataclass
class MutationResult:
    mutation_id: str
    detector: str
    rejected: bool
    detail: str = ""


@dataclass
class CampaignReport:
    schema: str
    registered_mutations: int
    results: list[MutationResult]
    checker_coverage: int

    @property
    def successful(self) -> bool:
        return self.registered_mutations > 0 and all(item.rejected for item in self.results)

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["successful"] = self.successful
        payload["mutation_score"] = (
            sum(item.rejected for item in self.results) / len(self.results) if self.results else 0.0
        )
        return payload


def _expect_rejection(mutation_id: str, detector: str, action: Callable[[], None]) -> MutationResult:
    try:
        action()
    except Exception as exc:
        return MutationResult(mutation_id, detector, True, str(exc))
    return MutationResult(mutation_id, detector, False, "mutation was accepted")


def _trust_mutations() -> list[MutationResult]:
    trust = HMACTrust(key=b"campaign-key", trust_domain="campaign", key_id="campaign")
    payload = {"check_id": "x", "cache_key": "k", "result": {"status": "passed"}}
    results: list[MutationResult] = []
    with tempfile.TemporaryDirectory() as directory:
        path = Path(directory) / "cache.json"
        write_attestation(path, trust=trust, kind="cache-result", payload=payload)
        original = json.loads(path.read_text(encoding="utf-8"))
        for field, value in (
            ("payload", {"check_id": "x", "cache_key": "evil"}),
            ("signature", "0" * 64),
            ("trust_domain", "other"),
            ("key_id", "other"),
            ("kind", "validation-certificate"),
        ):
            mutated = dict(original)
            mutated[field] = value
            path.write_text(json.dumps(mutated), encoding="utf-8")
            results.append(
                _expect_rejection(
                    f"CACHE-{field.upper()}",
                    "signed-cache",
                    lambda p=path: read_attestation(p, trust=trust, kind="cache-result"),
                )
            )
    return results


def _certificate_mutations() -> list[MutationResult]:
    trust = HMACTrust(key=b"certificate-key", trust_domain="campaign", key_id="certificate")
    run = {
        "run_id": "r1", "profile": "release", "commit_sha": "a" * 40, "tree_sha": "b" * 40,
        "base_sha": "c" * 40, "manifest_hash": "d" * 64, "successful": True,
        "root_failures": [], "selected_checks": ["bootstrap.manifest", "assurance.oracles"], "results": [],
    }
    results: list[MutationResult] = []
    old_event = os.environ.get("GITHUB_EVENT_NAME")
    os.environ["GITHUB_EVENT_NAME"] = "merge_group"
    try:
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "certificate.json"
            write_certificate(path, run, trust=trust)
            results.append(
                _expect_rejection(
                    "CERT-WRONG-COMMIT", "merge-certificate",
                    lambda: verify_certificate(path, trust=trust, expected_commit="e" * 40, expected_tree="b" * 40),
                )
            )
            results.append(
                _expect_rejection(
                    "CERT-WRONG-TREE", "merge-certificate",
                    lambda: verify_certificate(path, trust=trust, expected_commit="a" * 40, expected_tree="e" * 40),
                )
            )
            results.append(
                _expect_rejection(
                    "CERT-MISSING-CHECK", "merge-certificate",
                    lambda: verify_certificate(
                        path, trust=trust, expected_commit="a" * 40, expected_tree="b" * 40,
                        required_checks=["assurance.mutation-campaign"],
                    ),
                )
            )
            envelope = json.loads(path.read_text(encoding="utf-8"))
            envelope["payload"]["successful"] = False
            path.write_text(json.dumps(envelope), encoding="utf-8")
            results.append(
                _expect_rejection(
                    "CERT-UNSIGNED-TAMPER", "merge-certificate",
                    lambda: verify_certificate(path, trust=trust, expected_commit="a" * 40, expected_tree="b" * 40),
                )
            )
    finally:
        if old_event is None:
            os.environ.pop("GITHUB_EVENT_NAME", None)
        else:
            os.environ["GITHUB_EVENT_NAME"] = old_event
    return results


def _trace_mutations(root: Path) -> list[MutationResult]:
    policy = RuntimePolicy(
        allow_read_patterns=("tools/**/*.py",),
        allow_write_patterns=(".far/**",),
        allowed_executables=("python", "python3"),
        skip_checks=(),
        deny_network=True,
    )
    cases = [
        ("TRACE-UNDECLARED-READ", TraceReport("synthetic", reads=["secret.txt"]), "undeclared read"),
        ("TRACE-UNDECLARED-WRITE", TraceReport("synthetic", writes=["README.md"]), "undeclared write"),
        ("TRACE-NETWORK", TraceReport("synthetic", network_attempts=["connect(example.com:443)"]), "network access denied"),
        ("TRACE-EXECUTABLE", TraceReport("synthetic", executables=["/usr/bin/curl"]), "undeclared executable"),
    ]
    results: list[MutationResult] = []
    for mutation_id, report, expected in cases:
        audited = audit_trace(
            report, declared_inputs=("declared/**",), declared_outputs=(), command=("python", "tools/check.py"),
            policy=policy, sandbox_copy=False,
        )
        results.append(
            MutationResult(mutation_id, "runtime-trace", any(expected in item for item in audited.violations), "; ".join(audited.violations))
        )
    return results


def _checker_mutations(root: Path) -> tuple[list[MutationResult], int]:
    commands, failures = _manifest_commands(root)
    if failures:
        raise RuntimeError("manifest oracle precondition failed: " + "; ".join(failures))
    checkers = discover_legacy_checkers(root, set(commands.values()))
    results: list[MutationResult] = []
    for path in checkers:
        source = (root / path).read_text(encoding="utf-8")
        for mutation_id, mutated in _mutations(source).items():
            finding = analyze_checker_source(mutated, path)
            results.append(
                MutationResult(
                    f"ORACLE-{path.replace('/', '_')}-{mutation_id}", "independent-oracle",
                    not finding.accepted, "; ".join(finding.failures),
                )
            )
    return results, len(checkers)


def _weakening_mutations() -> list[MutationResult]:
    results: list[MutationResult] = []
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        subprocess.run(["git", "init", "-q"], cwd=root, check=True)
        subprocess.run(["git", "config", "user.email", "campaign@example.com"], cwd=root, check=True)
        subprocess.run(["git", "config", "user.name", "Campaign"], cwd=root, check=True)
        (root / "tests").mkdir()
        path = root / "tests" / "test_sample.py"
        path.write_text(
            "import unittest\nclass T(unittest.TestCase):\n    def test_a(self):\n        self.assertEqual(1, 1)\n    def test_b(self):\n        self.assertTrue(True)\n",
            encoding="utf-8",
        )
        subprocess.run(["git", "add", "."], cwd=root, check=True)
        subprocess.run(["git", "commit", "-qm", "base"], cwd=root, check=True)
        base = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip()
        path.write_text(
            "import unittest\nclass T(unittest.TestCase):\n    def test_a(self):\n        pass\n",
            encoding="utf-8",
        )
        subprocess.run(["git", "add", "."], cwd=root, check=True)
        subprocess.run(["git", "commit", "-qm", "weaken"], cwd=root, check=True)
        report = detect_weakening(root, base=base)
        results.append(
            MutationResult("WEAKEN-DELETE-TEST-AND-ASSERTIONS", "test-weakening", not report.successful, json.dumps(report.to_dict(), sort_keys=True))
        )
    return results


def run_campaign(root: Path) -> CampaignReport:
    results: list[MutationResult] = []
    checker_results, checker_count = _checker_mutations(root)
    results.extend(checker_results)
    results.extend(_trust_mutations())
    results.extend(_certificate_mutations())
    results.extend(_trace_mutations(root))
    results.extend(_weakening_mutations())
    model = exhaustive_model_check(4)
    results.append(
        MutationResult(
            "FORMAL-EXHAUSTIVE-STATE-SPACE", "formal-model", model["runs"] > 0 and model["attestation_mutations"] == 5,
            json.dumps(model, sort_keys=True),
        )
    )
    return CampaignReport(
        schema="project-far-validator-mutation-campaign-v1",
        registered_mutations=len(results),
        results=results,
        checker_coverage=checker_count,
    )


def main(argv: list[str] | None = None) -> int:
    import argparse

    parser = argparse.ArgumentParser(description="Run the complete registered validator mutation and hostile-acceptance campaign")
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--report", type=Path)
    args = parser.parse_args(argv)
    report = run_campaign(args.root.resolve())
    payload = report.to_dict()
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    else:
        failed = [item for item in report.results if not item.rejected]
        print(
            f"validator assurance campaign: {len(report.results) - len(failed)}/{len(report.results)} mutations rejected; "
            f"legacy checker coverage={report.checker_coverage}"
        )
        for item in failed:
            print(f"[FAIL] {item.mutation_id} via {item.detector}: {item.detail}")
        print("Result:", "PASS" if report.successful else "FAIL")
    return 0 if report.successful else 1


if __name__ == "__main__":
    raise SystemExit(main())
