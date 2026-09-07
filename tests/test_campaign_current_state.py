"""Campaign manifests stay historical; current-state drift must be declared and bounded.

A completed campaign manifest records the bytes as of execution. Rewriting it when a living
documentation surface changes makes the executed bytes and the currently documented bytes
indistinguishable in the artifact the checker actually reads.

These tests enforce the separation for `PCA-W5` and `PCA-W6`:

* the executed manifests match the bytes recorded on the campaign's own completion commit;
* every current-state supplement entry is well formed and matches both digests;
* a protected artifact — experimental input, output, recorded result, or pinned protocol base —
  can never be declared in a supplement;
* undeclared drift and stale entries still fail closed.
"""
from __future__ import annotations

import json
import subprocess
import unittest
from pathlib import Path

from tools.campaign_current_state import artifact_hash_errors, sha256_of

ROOT = Path(__file__).resolve().parents[1]

CAMPAIGNS = (
    (
        "W5",
        ROOT / "research/results/pca-w5-approximation-and-cost/manifest.json",
        ROOT / "research/results/pca-w5-approximation-and-cost/current-state-supplement.json",
    ),
    (
        "W6",
        ROOT / "research/results/pca-w6-empirical-audit-utility/manifest.json",
        ROOT / "research/results/pca-w6-empirical-audit-utility/current-state-supplement.json",
    ),
)

# The commit both campaign manifests carried before the diagnostic-vocabulary work began.
EXECUTED_BASELINE_COMMIT = "e1642e3"


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


class CampaignManifestProvenanceTests(unittest.TestCase):
    def test_executed_manifests_are_not_rewritten(self) -> None:
        """The manifest must still be the bytes recorded at campaign completion."""
        for label, manifest_path, _supplement in CAMPAIGNS:
            with self.subTest(campaign=label):
                relative = manifest_path.relative_to(ROOT).as_posix()
                recorded = subprocess.run(
                    ["git", "show", f"{EXECUTED_BASELINE_COMMIT}:{relative}"],
                    cwd=ROOT,
                    capture_output=True,
                    text=True,
                    check=True,
                ).stdout
                self.assertEqual(
                    json.loads(recorded),
                    load(manifest_path),
                    f"{label}: completed-campaign manifest was rewritten instead of supplemented",
                )

    def test_supplements_declare_provenance_semantics_and_no_result_change(self) -> None:
        for label, _manifest, supplement_path in CAMPAIGNS:
            with self.subTest(campaign=label):
                supplement = load(supplement_path)
                self.assertEqual(
                    supplement["manifest_status"],
                    "HISTORICAL_EXECUTED_BYTES_NOT_REWRITTEN",
                )
                self.assertTrue(supplement["recorded_result_unchanged"])
                self.assertIn("never rewritten", supplement["provenance_semantics"])

    def test_every_supplement_entry_matches_both_digests(self) -> None:
        for label, manifest_path, supplement_path in CAMPAIGNS:
            with self.subTest(campaign=label):
                executed = {a["path"]: a["sha256"] for a in load(manifest_path)["artifacts"]}
                for entry in load(supplement_path)["entries"]:
                    self.assertIn(entry["path"], executed)
                    self.assertEqual(entry["executed_sha256"], executed[entry["path"]])
                    self.assertEqual(entry["current_sha256"], sha256_of(ROOT / entry["path"]))
                    self.assertTrue(entry["reason"].strip())

    def test_declared_drift_is_documentation_or_tooling_only(self) -> None:
        permitted = {
            "documentation_surface",
            "governance_register",
            "specification_surface",
            "verification_tooling",
        }
        for label, _manifest, supplement_path in CAMPAIGNS:
            with self.subTest(campaign=label):
                for entry in load(supplement_path)["entries"]:
                    self.assertIn(entry["class"], permitted, f"{label}: {entry['path']}")

    def test_protected_artifacts_are_never_declared(self) -> None:
        """Experimental evidence may not be re-pointed at post-execution bytes."""
        import tools.check_pca_w5_approximation_cost as W5
        import tools.check_pca_w6_empirical_audit_utility as W6

        for label, protected, supplement_path in (
            ("W5", W5.PROTECTED_ARTIFACTS, CAMPAIGNS[0][2]),
            ("W6", W6.PROTECTED_ARTIFACTS, CAMPAIGNS[1][2]),
        ):
            with self.subTest(campaign=label):
                declared = {entry["path"] for entry in load(supplement_path)["entries"]}
                self.assertEqual(declared & set(protected), set())

    def test_every_protected_path_is_a_real_manifest_artifact(self) -> None:
        """A misspelled protected path silently protects nothing.

        `test_protected_artifacts_are_never_declared` passes vacuously for a path that is in
        neither the manifest nor the supplement, so a typo removes an artifact from protection
        without failing any other check. This is the control for that.
        """
        import tools.check_pca_w5_approximation_cost as W5
        import tools.check_pca_w6_empirical_audit_utility as W6

        for label, protected, manifest_path in (
            ("W5", W5.PROTECTED_ARTIFACTS, CAMPAIGNS[0][1]),
            ("W6", W6.PROTECTED_ARTIFACTS, CAMPAIGNS[1][1]),
        ):
            with self.subTest(campaign=label):
                declared = {a["path"] for a in load(manifest_path)["artifacts"]}
                orphaned = sorted(set(protected) - declared)
                self.assertEqual(
                    orphaned,
                    [],
                    f"{label}: PROTECTED_ARTIFACTS names path(s) absent from the campaign "
                    f"manifest, so nothing is protected by them: {orphaned}",
                )
                for path in protected:
                    self.assertTrue(
                        (ROOT / path).is_file(), f"{label}: protected path does not exist: {path}"
                    )

    def test_recorded_result_ledgers_are_protected(self) -> None:
        """The artifacts a campaign's verdict is read from may never be supplemented."""
        import tools.check_pca_w5_approximation_cost as W5
        import tools.check_pca_w6_empirical_audit_utility as W6

        self.assertIn(
            "theory/evaluation/pca-w5-approximation-cost-v1.0.json", W5.PROTECTED_ARTIFACTS
        )
        self.assertIn(
            "theory/evaluation/pca-w6-empirical-audit-utility-v1.0.json", W6.PROTECTED_ARTIFACTS
        )
        self.assertIn(
            "research/results/pca-w5-approximation-and-cost/frontier.json", W5.PROTECTED_ARTIFACTS
        )
        self.assertIn(
            "research/results/pca-w6-empirical-audit-utility/results.json", W6.PROTECTED_ARTIFACTS
        )

    def test_w6_protocol_base_is_protected(self) -> None:
        import tools.check_pca_w6_empirical_audit_utility as W6

        for path in W6.EXPECTED_PROTOCOL_BASE_BLOBS:
            self.assertIn(path, W6.PROTECTED_ARTIFACTS)

    def test_undeclared_drift_fails_closed(self) -> None:
        errors = artifact_hash_errors(
            ROOT,
            {"README.md": "0" * 64},
            ROOT / "does-not-exist.json",
            frozenset(),
            "TEST",
        )
        self.assertTrue(any("TEST_ARTIFACT_HASH_MISMATCH README.md" in e for e in errors))

    def test_supplementing_a_protected_artifact_fails_closed(self, ) -> None:
        import tempfile

        supplement = {
            "entries": [
                {
                    "path": "README.md",
                    "executed_sha256": "0" * 64,
                    "current_sha256": sha256_of(ROOT / "README.md"),
                    "class": "documentation_surface",
                    "reason": "attempt to launder a protected artifact",
                }
            ]
        }
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as handle:
            json.dump(supplement, handle)
            temporary = Path(handle.name)
        try:
            errors = artifact_hash_errors(
                ROOT, {"README.md": "0" * 64}, temporary, {"README.md"}, "TEST"
            )
            self.assertTrue(
                any("TEST_SUPPLEMENT_FORBIDDEN_FOR_PROTECTED_ARTIFACT" in e for e in errors)
            )
        finally:
            temporary.unlink()

    def test_stale_supplement_entry_fails_closed(self) -> None:
        """An entry for an artifact that matches the manifest again must be removed."""
        import tempfile

        readme_digest = sha256_of(ROOT / "README.md")
        supplement = {
            "entries": [
                {
                    "path": "README.md",
                    "executed_sha256": readme_digest,
                    "current_sha256": readme_digest,
                    "class": "documentation_surface",
                    "reason": "no longer applicable",
                }
            ]
        }
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as handle:
            json.dump(supplement, handle)
            temporary = Path(handle.name)
        try:
            errors = artifact_hash_errors(
                ROOT, {"README.md": readme_digest}, temporary, frozenset(), "TEST"
            )
            self.assertTrue(any("TEST_SUPPLEMENT_STALE README.md" in e for e in errors))
        finally:
            temporary.unlink()


if __name__ == "__main__":
    unittest.main()
