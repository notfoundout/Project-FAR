"""Mechanical split between current (strict) and historical (baseline) far-ir/2.0 verification.

Every tracked file that imports, dynamically loads, or invokes the frozen baseline
``contract_v2`` must be declared in ``verifier_authority.HISTORICAL_BASELINE_CONSUMERS``.
Anything else, including any new tool, CLI, workflow, document command, or campaign, has to use
``contract_v2_strict``. Registry entries must stay live, so a stale allowance cannot quietly
cover a future baseline use.
"""
from __future__ import annotations

import re
import subprocess
import unittest
from pathlib import Path

from mechanization.far_mechanization import verifier_authority

ROOT = Path(__file__).resolve().parents[1]
EXCLUDED_PREFIXES = ("archive/", ".far/")
TEXT_SUFFIXES = {".py", ".md", ".json", ".yml", ".yaml", ".toml", ".cfg", ".txt", ".sh", ""}

# Module-level references to the baseline, never the strict module or far-ir/2.1.
BASELINE_PATTERNS = (
    re.compile(r"far_mechanization\.contract_v2(?![_\w])(?!\.py)"),
    re.compile(r"from\s+\.contract_v2\s+import"),
    re.compile(r"far_mechanization\s+import\s+[^\n]*\bcontract_v2\b(?![_\w])"),
    re.compile(r"^\s*import\s+contract_v2\b(?![_\w])", re.MULTILINE),
    re.compile(r"[\"']contract_v2[\"']"),
    re.compile(r"\bcontract_v2\.(?:validate_contract|load_and_validate|main)\b"),
    re.compile(r"\bbaseline\s+`?contract_v2`?(?![_\w.])"),
)


def tracked_files() -> list[str]:
    output = subprocess.run(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    return sorted(
        path
        for path in output.splitlines()
        if not path.startswith(EXCLUDED_PREFIXES)
        and Path(path).suffix in TEXT_SUFFIXES
        and (ROOT / path).is_file()
    )


def references_baseline(path: str) -> bool:
    try:
        text = (ROOT / path).read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return False
    return any(pattern.search(text) for pattern in BASELINE_PATTERNS)


class VerifierAuthorityTests(unittest.TestCase):
    def test_every_baseline_consumer_is_registered(self) -> None:
        registered = set(verifier_authority.HISTORICAL_BASELINE_CONSUMERS)
        offenders = [path for path in tracked_files() if references_baseline(path) and path not in registered]
        self.assertEqual(
            offenders,
            [],
            "these files use the frozen far-ir/2.0 baseline directly; current verification must use "
            f"{verifier_authority.CURRENT_FAR_IR_2_0_VERIFIER}",
        )

    def test_registered_consumers_are_live_and_reasoned(self) -> None:
        for path, reason in verifier_authority.HISTORICAL_BASELINE_CONSUMERS.items():
            with self.subTest(path=path):
                self.assertIn(reason, verifier_authority.REASONS)
                self.assertTrue((ROOT / path).is_file(), "stale registry entry")
                self.assertTrue(references_baseline(path), "registered consumer no longer references the baseline")

    def test_patterns_distinguish_strict_from_baseline(self) -> None:
        baseline = [
            "from mechanization.far_mechanization.contract_v2 import validate_contract",
            "from .contract_v2 import load_and_validate",
            "from mechanization.far_mechanization import contract_v2, contract_v21",
            "python -m mechanization.far_mechanization.contract_v2 RECORD --json",
            '_FORMATS = {"far-ir/2.0": ("contract_v2", "schema.json")}',
            "Run the exact baseline `contract_v2` JSON command.",
        ]
        current = [
            "from mechanization.far_mechanization.contract_v2_strict import validate_contract",
            "from .contract_v2_strict import load_and_validate",
            "python -m mechanization.far_mechanization.contract_v2_strict RECORD --json",
            "from mechanization.far_mechanization.contract_v21 import validate_contract",
            '_FORMATS = {"far-ir/2.0": ("contract_v2_strict", "schema.json")}',
            "shared = root / 'mechanization' / 'far_mechanization' / 'contract_v2.py'",
        ]
        for text in baseline:
            with self.subTest(baseline=text):
                self.assertTrue(any(p.search(text) for p in BASELINE_PATTERNS))
        for text in current:
            with self.subTest(current=text):
                self.assertFalse(any(p.search(text) for p in BASELINE_PATTERNS))

    def test_current_surfaces_use_strict_verifier(self) -> None:
        current_surfaces = {
            "mechanization/far_mechanization/contract_conformance.py": "from .contract_v2_strict import load_and_validate",
            "mechanization/far_mechanization/migrate_v1_to_v2.py": "from .contract_v2_strict import",
            "tools/check_pca_w4_domain_contracts.py": "far_mechanization.contract_v2_strict import",
            "commercial/far-decision-integrity/src/far_decision_integrity/semantic_audit.py": '"far-ir/2.0": ("contract_v2_strict",',
        }
        for path, needle in current_surfaces.items():
            with self.subTest(path=path):
                text = (ROOT / path).read_text(encoding="utf-8")
                self.assertIn(needle, text)
                self.assertNotIn(path, verifier_authority.HISTORICAL_BASELINE_CONSUMERS)


if __name__ == "__main__":
    unittest.main()
