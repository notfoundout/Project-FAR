from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

from check_orphaned_docs import find_orphans
from check_proof_object import (
    conclusion_aligns_with_theorem,
    source_items,
    summary_aligns_with_statement,
    warn_on_weak_metadata_alignment,
)


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


def test_exact_orphan_ok_marker_exempts_intentionally_standalone_doc(tmp_path: Path) -> None:
    root = basic_root(tmp_path)
    write(root, "docs/standalone.md", "# Standalone\n\n<!-- orphan-ok -->\n")
    assert find_orphans(root) == []


def test_orphan_ok_near_match_and_incidental_mention_do_not_exempt(tmp_path: Path) -> None:
    root = basic_root(tmp_path)
    near_match = write(root, "docs/near.md", "# Near\n\n<!-- orphan-ok: because -->\n")
    incidental = write(root, "docs/incidental.md", "# Policy discussion\n\nUse `<!-- orphan-ok -->` sparingly.\n")
    assert find_orphans(root) == [incidental, near_match]


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


def test_concise_summary_uses_permissive_warning_alignment() -> None:
    assert summary_aligns_with_statement(
        "Representation is necessary.",
        "Every scoped reasoning process requires an explicit Representation to remain auditable.",
    )


def test_exact_and_faithful_theorem_conclusions_pass() -> None:
    theorem = "Every registered derived concept is constructible from the primitive architecture by finite substitution."
    assert conclusion_aligns_with_theorem(theorem, theorem)
    assert conclusion_aligns_with_theorem(
        "Every registered derived concept is constructible from the primitive architecture.", theorem
    )


def test_long_conclusion_with_unsupported_additions_fails() -> None:
    theorem = "Every registered derived concept is constructible from the primitive architecture."
    conclusion = (
        theorem
        + " It is universally optimal, independently verified, complete for every future domain, "
        "and proves that no alternative architecture can exist."
    )
    assert not conclusion_aligns_with_theorem(conclusion, theorem)


def test_small_fraction_of_conclusion_vocabulary_fails() -> None:
    assert not conclusion_aligns_with_theorem(
        "Representation exists, while unrelated safety, performance, deployment, economics, and universal correctness are established.",
        "Every scoped reasoning process has a Representation.",
    )


def test_duplicate_lineage_source_is_one_authority_and_mismatch_warns() -> None:
    source = {"statement": {"kind": "lemma", "claim": "Representation is necessary for scoped reasoning."}}
    sources = source_items(["left", "right"], {"left": {"L-001"}, "right": {"L-001"}}, {"L-001": source}, r"L-\d{3}")
    warnings: list[str] = []
    warn_on_weak_metadata_alignment("s1", "lemma_application", "Calculus is optional.", sources, [], warnings)
    assert [source_id for source_id, _ in sources] == ["L-001"]
    assert len(warnings) == 1


def test_duplicate_aligned_source_produces_no_warning() -> None:
    source = {"statement": {"kind": "lemma", "claim": "Representation is necessary for scoped reasoning."}}
    sources = source_items(["left", "right"], {"left": {"L-001"}, "right": {"L-001"}}, {"L-001": source}, r"L-\d{3}")
    warnings: list[str] = []
    warn_on_weak_metadata_alignment("s1", "lemma_application", "Representation is necessary.", sources, [], warnings)
    assert warnings == []


def test_distinct_authorities_retain_multi_source_synthesis_behavior() -> None:
    body = {"statement": {"kind": "lemma", "claim": "Representation is necessary."}}
    sources = source_items(
        ["left", "right"], {"left": {"L-001"}, "right": {"L-002"}},
        {"L-001": body, "L-002": body}, r"L-\d{3}",
    )
    warnings: list[str] = []
    warn_on_weak_metadata_alignment("s1", "lemma_application", "Unrelated synthesis.", sources, [], warnings)
    assert [source_id for source_id, _ in sources] == ["L-001", "L-002"]
    assert warnings == []
