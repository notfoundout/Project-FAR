"""Recompute and fail-closed audit the governed PCA-W5 finite-explicit result set."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Any, Mapping

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from mechanization.far_mechanization.contract_v21 import validate_contract
from tools.campaign_current_state import artifact_hash_errors

EXPECTED_SCHEMA_VERSION = "1.0"
EXPECTED_CAMPAIGN = "PCA-W5-APPROXIMATION-AND-COST"
EXPECTED_STATUS = "COMPLETE_FINITE_EXPLICIT"
EXPECTED_TERMINAL_VERDICT = "PROVED_FINITE_EXPLICIT_OPERATIONAL_SCOPE"
EXPECTED_CHECKED_RECORDS = frozenset(
    {
        "research/results/pca-w5-approximation-and-cost/frontier.json",
        "conformance/far-ir-2.1/valid-frontier.json",
        "conformance/far-ir-2.1/valid-zero-boundary.json",
    }
)
EXPECTED_ARTIFACTS = frozenset(
    {
        ".github/workflows/pca-w5.yml",
        "conformance/far-ir-2.1/valid-frontier.json",
        "conformance/far-ir-2.1/valid-zero-boundary.json",
        "docs/governance/pca-w5-approximation-cost-status-v1.0.md",
        "docs/research/pca-w5-approximation-and-cost/00-protocol.md",
        "docs/research/pca-w5-approximation-and-cost/01-execution-and-results.md",
        "docs/specification/far-ir-2.1-approximation-cost.md",
        "mechanization/far_mechanization/contract_v21.py",
        "mechanization/lean/W5ApproximationCost.lean",
        "research/results/pca-w5-approximation-and-cost/frontier.json",
        "schemas/far-contract-v2.1.schema.json",
        "tests/test_pca_w5_approximation_cost.py",
        "theory/evaluation/pca-w5-approximation-cost-v1.0.json",
        "tools/check_pca_w5_approximation_cost.py",
    }
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


SUPPLEMENT_RELATIVE_PATH = "research/results/pca-w5-approximation-and-cost/current-state-supplement.json"

# Experimental inputs, outputs, and recorded results for the completed W5 campaign. These may
# never be re-pointed at post-execution bytes through the supplement.
PROTECTED_ARTIFACTS = frozenset({
    "conformance/far-ir-2.1/valid-frontier.json",
    "conformance/far-ir-2.1/valid-zero-boundary.json",
    "docs/research/pca-w5-approximation-and-cost/00-protocol.md",
    "docs/research/pca-w5-approximation-and-cost/01-execution-and-results.md",
    "mechanization/far_mechanization/contract_v21.py",
    "mechanization/lean/W5ApproximationCost.lean",
    "research/results/pca-w5-approximation-and-cost/frontier.json",
    "schemas/far-contract-v2.1.schema.json",
    "theory/evaluation/pca-w5-approximation-cost-v1.0.json",
})


def _set_mismatch(label: str, actual: set[str], expected: frozenset[str]) -> str:
    missing = sorted(expected - actual)
    extra = sorted(actual - expected)
    return f"{label}: missing={missing} extra={extra}"


def audit_manifest(root: Path, manifest: object) -> list[str]:
    errors: list[str] = []
    if not isinstance(manifest, Mapping):
        return ["W5_MANIFEST_NOT_OBJECT"]

    metadata = {
        "schema_version": EXPECTED_SCHEMA_VERSION,
        "campaign": EXPECTED_CAMPAIGN,
        "status": EXPECTED_STATUS,
        "terminal_verdict": EXPECTED_TERMINAL_VERDICT,
    }
    for field, expected in metadata.items():
        actual = manifest.get(field)
        if actual != expected:
            errors.append(f"W5_MANIFEST_METADATA_MISMATCH {field}: {actual!r} != {expected!r}")

    checked_raw = manifest.get("checked_records")
    checked: list[str] = []
    if not isinstance(checked_raw, list) or not all(isinstance(item, str) for item in checked_raw):
        errors.append("W5_CHECKED_RECORDS_INVALID")
    else:
        checked = checked_raw
        if len(checked) != len(set(checked)):
            errors.append("W5_CHECKED_RECORDS_DUPLICATE")
        actual_checked = set(checked)
        if actual_checked != EXPECTED_CHECKED_RECORDS:
            errors.append(_set_mismatch("W5_CHECKED_RECORD_SET_MISMATCH", actual_checked, EXPECTED_CHECKED_RECORDS))

    artifacts_raw = manifest.get("artifacts")
    artifact_hashes: dict[str, str] = {}
    if not isinstance(artifacts_raw, list):
        errors.append("W5_ARTIFACTS_INVALID")
    else:
        for index, item in enumerate(artifacts_raw):
            if not isinstance(item, Mapping):
                errors.append(f"W5_ARTIFACT_ENTRY_INVALID index={index}")
                continue
            path = item.get("path")
            digest = item.get("sha256")
            if not isinstance(path, str) or not isinstance(digest, str):
                errors.append(f"W5_ARTIFACT_ENTRY_INVALID index={index}")
                continue
            if path in artifact_hashes:
                errors.append(f"W5_ARTIFACT_DUPLICATE {path}")
            artifact_hashes[path] = digest
        actual_artifacts = set(artifact_hashes)
        if actual_artifacts != EXPECTED_ARTIFACTS:
            errors.append(_set_mismatch("W5_ARTIFACT_SET_MISMATCH", actual_artifacts, EXPECTED_ARTIFACTS))

    # Recompute the required artifact set independently of what the manifest enumerates.
    for rel in sorted(EXPECTED_ARTIFACTS):
        if not (root / rel).is_file():
            errors.append(f"W5_ARTIFACT_MISSING {rel}")
    # The manifest records the bytes as of execution and is never rewritten. Documentation
    # surfaces that legitimately changed since then are declared in the current-state
    # supplement; PROTECTED_ARTIFACTS may never be declared there.
    errors.extend(
        artifact_hash_errors(
            root,
            {rel: digest for rel, digest in artifact_hashes.items() if (root / rel).is_file()},
            root / SUPPLEMENT_RELATIVE_PATH,
            PROTECTED_ARTIFACTS,
            "W5",
        )
    )

    # Recompute every governed checked record even if the manifest tries to omit it.
    for rel in sorted(EXPECTED_CHECKED_RECORDS):
        path = root / rel
        if not path.is_file():
            errors.append(f"W5_CHECKED_RECORD_MISSING {rel}")
            continue
        try:
            document = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as error:
            errors.append(f"W5_CHECKED_RECORD_UNREADABLE {rel}: {error}")
            continue
        result = validate_contract(document)
        errors.extend(f"{rel}: {diagnostic.code}: {diagnostic.message}" for diagnostic in result.diagnostics)

    return errors


def main() -> int:
    manifest_path = ROOT / "research/results/pca-w5-approximation-and-cost/manifest.json"
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        print(f"W5_MANIFEST_UNREADABLE: {error}")
        return 1

    errors = audit_manifest(ROOT, manifest)
    if errors:
        print("\n".join(errors))
        return 1
    print(
        f"PCA-W5 PASS: {len(EXPECTED_CHECKED_RECORDS)} records; "
        f"terminal verdict {EXPECTED_TERMINAL_VERDICT}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
