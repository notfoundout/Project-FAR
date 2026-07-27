from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

from check_orphaned_docs import find_orphans
from check_proof_object import warn_on_weak_metadata_alignment


def write(root: Path, relative: str, text: str = "# Document\n") -> Path:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path.resolve()


def basic_root(tmp_path: Path, readme: str = "# Root\n") -> Path:
    write(tmp_path, "README.md", readme)
    return tmp_path


def test_substantive_orphan_still_fails(tmp_path: Path) -> None:
    root = basic_root(tmp_path)
    orphan = write(root, "docs/decision.md", "# Substantive decision\n")
    assert orphan in find_orphans(root)


def test_indexed_document_and_inline_path_pass(tmp_path: Path) -> None:
    root = basic_root(tmp_path, "# Root\n\n[Docs](docs/README.md)\n")
    write(root, "docs/README.md", "# Index\n\nCanonical record: `decision.md`.\n")
    write(root, "docs/decision.md")
    assert find_orphans(root) == []


def test_archival_and_research_evidence_follow_policy(tmp_path: Path) -> None:
    root = basic_root(tmp_path)
    write(root, "docs/archive/historical.md")
    write(root, "docs/research/generated-result.md", "# Generated result\n")
    assert find_orphans(root) == []


def test_linked_summary_and_canonical_source_pass_overlap_check() -> None:
    warnings: list[str] = []
    source = {"statement": {"kind": "lemma", "claim": "Representation is necessary for scoped reasoning."}}
    warn_on_weak_metadata_alignment(
        "s1", "lemma_application", "Removing Representation reduces expressive power.",
        [("L-001", source)], ["Representation is necessary for scoped reasoning."], warnings,
    )
    assert warnings == []


def test_real_competing_authority_overlap_is_reported() -> None:
    warnings: list[str] = []
    source = {"statement": {"kind": "lemma", "claim": "Representation is necessary for scoped reasoning."}}
    warn_on_weak_metadata_alignment(
        "s1", "lemma_application", "Calculus rules are optional.",
        [("L-001", source)], ["Calculus rules are optional."], warnings,
    )
    assert warnings == ["step s1 lemma_application has weak semantic overlap with L-001 metadata statement"]
