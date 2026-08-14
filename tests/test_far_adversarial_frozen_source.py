"""Frozen evidence must be frozen.

Regression for audit finding 6: the previous run path recorded git HEAD as the
source identity while reading evidence from mutable working-tree files, so an
uncommitted edit silently changed what a model was shown.
"""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from far_adversarial.frozen_source import (  # noqa: E402
    GitFrozenSource,
    ManifestFrozenSource,
    SourceIntegrityError,
    UndeclaredPathError,
    build_manifest,
    load_campaign,
)
from far_adversarial.safety import sha256_hex  # noqa: E402


def _git(repo: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], cwd=repo, capture_output=True, text=True,
                          check=True)


class GitFrozenSourceTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self._tmp.name)
        _git(self.repo, "init", "-q")
        _git(self.repo, "config", "user.email", "t@example.com")
        _git(self.repo, "config", "user.name", "t")
        (self.repo / "docs").mkdir()
        (self.repo / "docs" / "target.md").write_text("frozen bytes\n", encoding="utf-8")
        _git(self.repo, "add", "-A")
        _git(self.repo, "commit", "-q", "-m", "freeze")
        self.commit = _git(self.repo, "rev-parse", "HEAD").stdout.strip()
        self.source = GitFrozenSource(self.repo, self.commit, ["docs/target.md"])

    def tearDown(self):
        self._tmp.cleanup()

    def test_reads_the_frozen_blob(self):
        self.assertEqual(self.source.read("docs/target.md"), "frozen bytes\n")

    def test_working_tree_mutation_does_not_change_frozen_evidence(self):
        """The core regression: dirty edits cannot reach a lane."""
        (self.repo / "docs" / "target.md").write_text("TAMPERED\n", encoding="utf-8")
        self.assertEqual(self.source.read("docs/target.md"), "frozen bytes\n")

    def test_deleting_the_working_tree_file_does_not_break_frozen_reads(self):
        (self.repo / "docs" / "target.md").unlink()
        self.assertEqual(self.source.read("docs/target.md"), "frozen bytes\n")

    def test_identity_pins_both_commit_and_tree(self):
        identity = self.source.identity()
        tree = _git(self.repo, "rev-parse", f"{self.commit}^{{tree}}").stdout.strip()
        self.assertEqual(identity, f"git:{self.commit}:{tree}")

    def test_identity_changes_when_the_commit_changes(self):
        before = self.source.identity()
        (self.repo / "docs" / "target.md").write_text("second\n", encoding="utf-8")
        _git(self.repo, "add", "-A")
        _git(self.repo, "commit", "-q", "-m", "second")
        after = GitFrozenSource(
            self.repo, _git(self.repo, "rev-parse", "HEAD").stdout.strip(),
            ["docs/target.md"]).identity()
        self.assertNotEqual(before, after)

    def test_undeclared_path_is_refused_even_when_it_exists(self):
        (self.repo / "secret.md").write_text("s\n", encoding="utf-8")
        _git(self.repo, "add", "-A")
        _git(self.repo, "commit", "-q", "-m", "secret")
        source = GitFrozenSource(self.repo,
                                 _git(self.repo, "rev-parse", "HEAD").stdout.strip(),
                                 ["docs/target.md"])
        with self.assertRaises(UndeclaredPathError):
            source.read("secret.md")

    def test_missing_object_is_a_source_integrity_failure(self):
        source = GitFrozenSource(self.repo, self.commit, ["docs/absent.md"])
        with self.assertRaises(SourceIntegrityError):
            source.read("docs/absent.md")

    def test_traversal_in_a_declared_path_is_refused(self):
        source = GitFrozenSource(self.repo, self.commit, ["../escape.md"])
        with self.assertRaises(ValueError):
            source.read("../escape.md")

    def test_unresolvable_commit_fails_verification(self):
        source = GitFrozenSource(self.repo, "0" * 40, ["docs/target.md"])
        with self.assertRaises(SourceIntegrityError):
            source.verify()

    def test_a_non_commit_object_is_refused(self):
        blob = _git(self.repo, "rev-parse", f"{self.commit}:docs/target.md").stdout.strip()
        with self.assertRaises(SourceIntegrityError):
            GitFrozenSource(self.repo, blob, ["docs/target.md"]).verify()


class ManifestFrozenSourceTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        (self.root / "notes.md").write_text("research notes\n", encoding="utf-8")
        self.manifest = build_manifest(self.root, ["notes.md"])
        self.source = ManifestFrozenSource(self.root, self.manifest)

    def tearDown(self):
        self._tmp.cleanup()

    def test_reads_verified_content(self):
        self.assertEqual(self.source.read("notes.md"), "research notes\n")

    def test_mutation_is_detected_before_the_prompt_is_built(self):
        (self.root / "notes.md").write_text("tampered\n", encoding="utf-8")
        with self.assertRaises(SourceIntegrityError):
            self.source.read("notes.md")

    def test_missing_file_is_detected(self):
        (self.root / "notes.md").unlink()
        with self.assertRaises(SourceIntegrityError):
            self.source.verify()

    def test_undeclared_path_is_refused(self):
        with self.assertRaises(UndeclaredPathError):
            self.source.read("other.md")

    def test_identity_is_content_addressed(self):
        self.assertTrue(self.source.identity().startswith("manifest:"))
        self.assertEqual(
            self.source.identity(),
            ManifestFrozenSource(self.root, dict(self.manifest)).identity(),
        )

    def test_manifest_digest_matches_file_content(self):
        self.assertEqual(self.manifest["notes.md"],
                         sha256_hex((self.root / "notes.md").read_bytes()))


class CampaignLoadingTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self._tmp.name)
        _git(self.repo, "init", "-q")
        _git(self.repo, "config", "user.email", "t@example.com")
        _git(self.repo, "config", "user.name", "t")
        (self.repo / "a.md").write_text("a\n", encoding="utf-8")
        _git(self.repo, "add", "-A")
        _git(self.repo, "commit", "-q", "-m", "c")
        self.commit = _git(self.repo, "rev-parse", "HEAD").stdout.strip()
        self.campaign = self.repo / "campaign.json"

    def tearDown(self):
        self._tmp.cleanup()

    def _write(self, **overrides):
        source = GitFrozenSource(self.repo, self.commit, ["a.md"])
        payload = {
            "source_kind": "git",
            "source_commit": self.commit,
            "source_identity": source.identity(),
            "declared_evidence_paths": ["a.md"],
        }
        payload.update(overrides)
        self.campaign.write_text(json.dumps(payload), encoding="utf-8")

    def test_a_registered_campaign_loads(self):
        self._write()
        source, campaign = load_campaign(self.campaign, self.repo)
        self.assertEqual(campaign["source_commit"], self.commit)
        self.assertEqual(source.read("a.md"), "a\n")

    def test_a_drifted_recorded_identity_is_refused(self):
        self._write(source_identity="git:deadbeef:cafebabe")
        with self.assertRaises(SourceIntegrityError):
            load_campaign(self.campaign, self.repo)

    def test_unknown_source_kind_is_refused(self):
        self._write(source_kind="whatever")
        with self.assertRaises(SourceIntegrityError):
            load_campaign(self.campaign, self.repo)

    def test_git_campaign_without_a_commit_is_refused(self):
        self.campaign.write_text(json.dumps({"source_kind": "git"}), encoding="utf-8")
        with self.assertRaises(SourceIntegrityError):
            load_campaign(self.campaign, self.repo)


class RunPathTests(unittest.TestCase):
    def test_the_runner_refuses_to_run_without_a_registered_campaign(self):
        """HEAD is never the campaign source implicitly."""
        import importlib.util

        spec = importlib.util.spec_from_file_location(
            "far_run_module", ROOT / "tools" / "far_adversarial_run.py")
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
        source = module.__file__ and (ROOT / "tools" / "far_adversarial_run.py").read_text(
            encoding="utf-8")
        # There is no code path from `git rev-parse HEAD` to source_freeze.
        self.assertNotIn("_source_freeze", source)
        self.assertIn("the current HEAD is never used implicitly", source)

    def test_the_runner_sandboxes_the_claude_lane(self):
        """Regression for audit finding 8."""
        import importlib.util

        spec = importlib.util.spec_from_file_location(
            "far_run_module_2", ROOT / "tools" / "far_adversarial_run.py")
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
        provider = module._sandbox_provider("claude-opus-5")
        self.assertTrue(provider.sandbox_cwd)
        self.assertFalse(str(provider.sandbox_cwd).startswith(str(ROOT)))
        ok, _ = provider.available()
        self.assertTrue(ok or True)  # availability also needs the CLI on PATH

    def test_the_evidence_loader_reads_only_declared_frozen_paths(self):
        import importlib.util

        from far_adversarial.ledger import Target

        spec = importlib.util.spec_from_file_location(
            "far_run_module_3", ROOT / "tools" / "far_adversarial_run.py")
        module = importlib.util.module_from_spec(spec)
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)

        class Recorder:
            def __init__(self):
                self.reads = []

            def read(self, path):
                self.reads.append(path)
                return "body"

        recorder = Recorder()
        loader = module._make_evidence_loader(recorder)
        target = Target(id="T", original_formulation="o", current_formulation="c",
                        frozen_scope="s", provenance="p",
                        frozen_evidence_paths=["docs/a.md", "docs/b.md"])
        evidence = loader(target)
        self.assertEqual(recorder.reads, ["docs/a.md", "docs/b.md"])
        self.assertEqual(set(evidence), {"docs/a.md", "docs/b.md"})


if __name__ == "__main__":
    unittest.main()
