import importlib.util, sys, tempfile, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
P=ROOT/'tools/check_final_newline.py'
sys.path.insert(0,str(ROOT/'tools'))
s=importlib.util.spec_from_file_location('final_newline_test',P)
m=importlib.util.module_from_spec(s)
sys.modules[s.name]=m
s.loader.exec_module(m)

# b'frozen bytes\n'; the blob value is `git hash-object` on the same content.
FROZEN=b'frozen bytes\n'
SHA256='23d238dee01bfbb2ae59b9d21cce89282f89977ecf5f696f0da80f522cb17a8c'
SHA1='73866ed818cd6c9daab3c8197b864ea603f4017c'
GIT_BLOB_SHA1='4dea4dbeaf6b7c40a0d29934952220af0da18428'


class FinalNewlineRuleTests(unittest.TestCase):
    def test_missing_final_newline_is_a_violation(self):
        self.assertTrue(m.is_violation(b'x'))
    def test_present_final_newline_is_clean(self):
        self.assertFalse(m.is_violation(b'x\n'))
    def test_empty_file_is_not_a_violation(self):
        self.assertFalse(m.is_violation(b''))
    def test_repair_adds_exactly_one_newline(self):
        self.assertEqual(m.repair(b'x'), b'x\n')
    def test_repair_is_idempotent(self):
        self.assertEqual(m.repair(m.repair(b'x')), b'x\n')
    def test_repair_preserves_trailing_blank_lines(self):
        self.assertEqual(m.repair(b'x\n\n'), b'x\n\n')


class NoContentRewritingTests(unittest.TestCase):
    """The gate must change nothing but the final byte."""

    def test_trailing_whitespace_is_not_touched(self):
        self.assertEqual(m.repair(b'x   '), b'x   \n')
        self.assertFalse(m.is_violation(b'x   \n'))
    def test_markdown_hard_break_survives(self):
        self.assertEqual(m.repair(b'a  \nb'), b'a  \nb\n')
    def test_crlf_is_not_normalised(self):
        self.assertEqual(m.repair(b'a\r\nb\r\n'), b'a\r\nb\r\n')
    def test_interior_bytes_are_never_decoded_or_altered(self):
        raw=b'\xff\xfe binary-ish \x00 tail'
        self.assertEqual(m.repair(raw), raw+b'\n')


class DigestProtectionTests(unittest.TestCase):
    """A file whose identity is recorded anywhere must never be rewritten."""

    def test_digest_forms_match_known_vectors(self):
        self.assertEqual(m.content_digests(FROZEN), (SHA256, SHA1, GIT_BLOB_SHA1))

    def test_git_blob_form_matches_git_hash_object(self):
        """Regression: a SHA-256-only rule broke a Git blob SHA-1 ledger."""
        self.assertIn(GIT_BLOB_SHA1, m.content_digests(FROZEN))

    def test_exempt_when_sha256_is_recorded(self):
        self.assertEqual(m.exemption_reason('a/b.md', FROZEN, {SHA256}), 'digest-recorded')

    def test_exempt_when_sha1_is_recorded(self):
        self.assertEqual(m.exemption_reason('a/b.md', FROZEN, {SHA1}), 'digest-recorded')

    def test_exempt_when_git_blob_sha1_is_recorded(self):
        self.assertEqual(m.exemption_reason('a/b.md', FROZEN, {GIT_BLOB_SHA1}), 'digest-recorded')

    def test_digest_matching_is_case_insensitive_on_recorded_side(self):
        self.assertEqual(m.exemption_reason('a/b.md', FROZEN, {GIT_BLOB_SHA1.lower()}), 'digest-recorded')

    def test_not_exempt_when_no_digest_is_recorded(self):
        self.assertIsNone(m.exemption_reason('a/b.md', FROZEN, {'0'*64}))

    def test_unrelated_content_is_not_exempted_by_someone_elses_digest(self):
        self.assertIsNone(m.exemption_reason('a/b.md', b'other\n', {SHA256, SHA1, GIT_BLOB_SHA1}))

    def test_a_repaired_file_would_no_longer_match_its_frozen_identity(self):
        """Why the exemption must be checked before repair, not after."""
        unterminated=b'frozen bytes'
        self.assertNotEqual(m.content_digests(unterminated), m.content_digests(m.repair(unterminated)))

    def test_a_frozen_unterminated_file_is_exempt_rather_than_repaired(self):
        """The end-to-end guarantee: recorded identity wins over the rule."""
        unterminated=b'frozen bytes'
        recorded={m.content_digests(unterminated)[2]}  # its Git blob SHA-1
        self.assertTrue(m.is_violation(unterminated))
        self.assertEqual(m.exemption_reason('a/b.md', unterminated, recorded), 'digest-recorded')


class WalkExclusionTests(unittest.TestCase):
    """Generated, gitignored tool state must never become eligible content.

    Regression: running the validation framework writes JSON runtime state
    under .far/ (cache, runs, failures). That directory is gitignored and
    absent from a fresh checkout, so walking it was previously untested; the
    gate must not treat framework-generated state as repository content.
    """

    def test_skip_dirs_covers_far_runtime_directory(self):
        self.assertIn('.far', m.SKIP_DIRS)

    def test_files_under_a_skip_dir_are_never_yielded_as_candidates(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            skipped = root / '.far' / 'cache'
            skipped.mkdir(parents=True)
            (skipped / 'run.json').write_bytes(b'{}')  # missing final newline
            kept = root / 'docs'
            kept.mkdir()
            (kept / 'x.md').write_bytes(b'x')
            original_root = m.ROOT
            m.ROOT = root
            try:
                candidates = {p.relative_to(root).as_posix() for p in m.candidate_files()}
            finally:
                m.ROOT = original_root
            self.assertNotIn('.far/cache/run.json', candidates)
            self.assertIn('docs/x.md', candidates)


class PathExemptionTests(unittest.TestCase):
    def test_generated_archive_and_fixture_roots_are_exempt(self):
        for path in ('archive/x.md', 'artifacts/x.json', 'exports/x.md',
                     'conformance/x.json', 'tests/fixtures/x.json'):
            self.assertTrue(m.is_path_exempt(path), path)
    def test_freeze_and_external_validation_directories_are_exempt(self):
        self.assertTrue(m.is_path_exempt('a/primary-freeze/b.json'))
        self.assertTrue(m.is_path_exempt('a/environment-freeze/b.json'))
        self.assertTrue(m.is_path_exempt('a/external-validation/b/c.py'))
    def test_manifest_lock_and_digest_files_are_exempt(self):
        for path in ('a/manifest.json', 'a/package-manifest.json',
                     'a/checksum-lock.json', 'a/b.sha256'):
            self.assertTrue(m.is_path_exempt(path), path)
    def test_ordinary_source_is_not_exempt(self):
        for path in ('tools/x.py', 'docs/x.md', 'theory/x.json'):
            self.assertFalse(m.is_path_exempt(path), path)
    def test_path_exemption_reported_before_digest_lookup(self):
        self.assertEqual(m.exemption_reason('archive/x.md', b'x', set()), 'path')

    def test_bounded_v1_closure_campaign_root_is_exempt_but_not_all_of_docs_audits(self):
        """#451's adjudicated immutable campaign evidence: exempt by path, exactly."""
        self.assertTrue(m.is_path_exempt(
            'docs/audits/bounded-v1-closure-campaign/lane-a-first-pass.txt'))
        self.assertTrue(m.is_path_exempt(
            'docs/audits/bounded-v1-closure-campaign/cross-audit-adjudication-full.txt'))
        self.assertFalse(m.is_path_exempt('docs/audits/some-other-audit.md'))
        self.assertFalse(m.is_path_exempt(
            'docs/audits/bounded-v1-closure-campaign-similar-name/x.txt'))

    def test_unterminated_campaign_file_is_a_violation_yet_exempt_and_unrepaired(self):
        """The end-to-end guarantee for #451's evidence root: a hypothetical
        protected campaign file missing its final newline is a violation in
        isolation, but main() checks exemption_reason() before is_violation()
        (see the loop in main()), so it is reported exempt rather than fixed."""
        unterminated = b'campaign evidence with no trailing newline'
        path = 'docs/audits/bounded-v1-closure-campaign/hypothetical-lane-d.txt'
        self.assertTrue(m.is_violation(unterminated))
        self.assertEqual(m.exemption_reason(path, unterminated, set()), 'path')


if __name__ == '__main__':
    unittest.main()
