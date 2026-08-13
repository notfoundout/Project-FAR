import importlib.util, sys, unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
P=ROOT/'tools/check_whitespace_hygiene.py'
s=importlib.util.spec_from_file_location('whitespace_hygiene_test',P)
m=importlib.util.module_from_spec(s)
sys.modules[s.name]=m
sys.path.insert(0,str(ROOT/'tools'))
s.loader.exec_module(m)


class FinalNewlineTests(unittest.TestCase):
    def test_missing_final_newline_is_reported(self):
        self.assertIn('1: missing final newline', m.violations('x'))
    def test_present_final_newline_is_clean(self):
        self.assertEqual(m.violations('x\n'), [])
    def test_repair_adds_exactly_one_newline(self):
        self.assertEqual(m.repair('x'), 'x\n')
    def test_repair_preserves_existing_blank_final_lines(self):
        self.assertEqual(m.repair('x\n\n'), 'x\n\n')
    def test_empty_file_is_left_alone(self):
        self.assertEqual(m.violations(''), [])
        self.assertEqual(m.repair(''), '')


class ContentPreservationTests(unittest.TestCase):
    """Trailing whitespace that carries meaning must survive repair."""

    def test_markdown_hard_break_is_not_a_violation(self):
        self.assertEqual(m.violations('a  \nb\n', trim_trailing=False), [])
    def test_markdown_hard_break_survives_repair(self):
        self.assertEqual(m.repair('a  \nb', trim_trailing=False), 'a  \nb\n')
    def test_python_multiline_string_trailing_space_is_preserved(self):
        src = 'T = """\nStatus: `x`  \nNext\n"""\n'
        self.assertEqual(m.violations(src, suffix='.py'), [])
        self.assertEqual(m.repair(src, suffix='.py'), src)
    def test_python_code_trailing_space_is_still_repaired(self):
        self.assertIn('1: trailing whitespace', m.violations('x = 1  \n', suffix='.py'))
        self.assertEqual(m.repair('x = 1  \n', suffix='.py'), 'x = 1\n')
    def test_unparseable_python_is_left_alone(self):
        self.assertEqual(m.violations('def (  \n', suffix='.py'), [])


class ExemptionTests(unittest.TestCase):
    def test_archive_and_generated_roots_are_exempt(self):
        for path in ('archive/x.md', 'artifacts/x.json', 'exports/x.md',
                     'conformance/x.json', 'tests/fixtures/x.json'):
            self.assertTrue(m.is_path_exempt(path), path)
    def test_freeze_and_external_validation_directories_are_exempt(self):
        self.assertTrue(m.is_path_exempt('a/primary-freeze/b.json'))
        self.assertTrue(m.is_path_exempt('a/external-validation/b/c.py'))
    def test_manifest_lock_and_digest_files_are_exempt(self):
        for path in ('a/manifest.json', 'a/checksum-lock.json', 'a/b.sha256'):
            self.assertTrue(m.is_path_exempt(path), path)
    def test_ordinary_source_is_not_exempt(self):
        self.assertFalse(m.is_path_exempt('tools/x.py'))

    def test_all_three_digest_forms_are_recognised(self):
        """A frozen file is identified by sha256, sha1, or git blob sha1."""
        blob = b'frozen bytes\n'
        self.assertEqual(len(set(m.content_digests(blob))), 3)


if __name__ == '__main__':
    unittest.main()
