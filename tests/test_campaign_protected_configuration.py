"""Runtime controls for campaign protected-artifact configuration."""
from __future__ import annotations

from pathlib import Path

from tools.campaign_current_state import artifact_hash_errors, sha256_of

ROOT = Path(__file__).resolve().parents[1]


def test_orphaned_protected_path_fails_closed() -> None:
    """A misspelled protected path must fail in the checker, not only in meta-tests."""
    readme_digest = sha256_of(ROOT / "README.md")
    errors = artifact_hash_errors(
        ROOT,
        {"README.md": readme_digest},
        ROOT / "does-not-exist.json",
        {"README.md", "theory/evaluation/does-not-exist.json"},
        "TEST",
    )
    assert any("TEST_PROTECTED_ARTIFACT_NOT_IN_MANIFEST" in error for error in errors)
