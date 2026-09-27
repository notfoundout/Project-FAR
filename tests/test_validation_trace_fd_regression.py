from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import json
import os

from far_validation.tracing import RuntimePolicy, _matches, audit_trace, parse_strace


class StraceSchedulingAndFdRegressionTests(unittest.TestCase):
    def test_split_vfork_is_ordered_before_child_events_and_split_exec_is_observed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "repo"
            outside = Path(directory) / "child"
            root.mkdir()
            outside.mkdir()
            raw = (
                "100 vfork( <unfinished ...>\n"
                f'101 chdir("{outside}") = 0\n'
                '101 execve("/usr/bin/ssh-keygen", ["ssh-keygen"], 0x0 <unfinished ...>\n'
                '101 <... execve resumed>) = 0\n'
                '101 openat(AT_FDCWD, ".git/objects/temp", O_RDWR|O_CREAT, 0666) = 3\n'
                "100 <... vfork resumed>) = 101\n"
                f'100 openat(AT_FDCWD, "{root / "tracked.txt"}", O_RDONLY|O_CLOEXEC) = 3\n'
            )
            report = parse_strace(raw, cwd=root, root=root)
            self.assertEqual(report.reads, ["tracked.txt"])
            self.assertEqual(report.writes, [])
            self.assertEqual(report.executables, ["/usr/bin/ssh-keygen"])

    def test_fchdir_and_dirfd_paths_keep_temporary_repository_outside_root(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "repo"
            outside = Path(directory) / "child"
            root.mkdir()
            outside.mkdir()
            raw = (
                f'200 openat(AT_FDCWD, "{outside}", O_RDONLY|O_DIRECTORY) = 7\n'
                "200 fchdir(7) = 0\n"
                '200 openat(AT_FDCWD, ".git/objects/temp", O_WRONLY|O_CREAT, 0666) = 8\n'
                '200 openat(7, ".git/index", O_RDONLY|O_CLOEXEC) = 9\n'
            )
            report = parse_strace(raw, cwd=root, root=root)
            self.assertEqual(report.reads, [])
            self.assertEqual(report.writes, [])

    def test_dirfd_relative_access_inside_repository_is_not_dropped(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "repo"
            nested = root / "nested"
            nested.mkdir(parents=True)
            raw = (
                f'300 openat(AT_FDCWD, "{nested}", O_RDONLY|O_DIRECTORY) = 3\n'
                '300 openat(3, "tracked.txt", O_RDONLY|O_CLOEXEC) = 4\n'
                '300 unlinkat(3, "generated.txt", 0) = 0\n'
            )
            report = parse_strace(raw, cwd=root, root=root)
            self.assertIn("nested/tracked.txt", report.reads)
            self.assertIn("nested/generated.txt", report.writes)

    def test_failed_split_exec_is_not_reported(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            raw = (
                '400 execve("/missing/tool", ["tool"], 0x0 <unfinished ...>\n'
                '400 <... execve resumed>) = -1 ENOENT (No such file or directory)\n'
            )
            report = parse_strace(raw, cwd=root, root=root)
            self.assertEqual(report.executables, [])


class StraceSyscallCoverageRegressionTests(unittest.TestCase):
    """Each case below was observed or reproduced on ubuntu-24.04 (glibc 2.39, strace 6.8) and was
    silently misread by the tracer before the fix: an undeclared write or read passed the audit."""

    def setUp(self) -> None:
        self._directory = tempfile.TemporaryDirectory()
        self.root = Path(self._directory.name) / "repo"
        (self.root / "nested").mkdir(parents=True)
        self.outside = Path(self._directory.name) / "outside"
        self.outside.mkdir()

    def tearDown(self) -> None:
        self._directory.cleanup()

    def parse(self, raw: str):
        return parse_strace(raw, cwd=self.root, root=self.root)

    def test_rename_destination_is_a_write(self) -> None:
        # os.replace(tmp, target): the target is the real output of an atomic write.
        report = self.parse('10 rename("out.json.tmp", "out.json") = 0\n')
        self.assertEqual(report.writes, ["out.json", "out.json.tmp"])

    def test_renameat_resolves_each_operand_against_its_own_dirfd(self) -> None:
        report = self.parse(
            f'10 openat(AT_FDCWD, "{self.root / "nested"}", O_RDONLY|O_CLOEXEC|O_DIRECTORY) = 3\n'
            f'10 openat(AT_FDCWD, "{self.outside}", O_RDONLY|O_CLOEXEC|O_DIRECTORY) = 4\n'
            '10 renameat(3, "a.tmp", 3, "a.json") = 0\n'
            '10 renameat2(4, "scratch", AT_FDCWD, "published.json", RENAME_NOREPLACE) = 0\n'
        )
        self.assertEqual(report.writes, ["nested/a.json", "nested/a.tmp", "published.json"])

    def test_link_symlink_and_truncate_are_writes(self) -> None:
        report = self.parse(
            '10 link("source.txt", "hard.txt") = 0\n'
            '10 symlink("anything", "soft.txt") = 0\n'
            '10 symlinkat("anything", AT_FDCWD, "soft2.txt") = 0\n'
            '10 linkat(AT_FDCWD, "source2.txt", AT_FDCWD, "hard2.txt", 0) = 0\n'
            '10 truncate("cut.txt", 0) = 0\n'
        )
        self.assertEqual(report.writes, ["cut.txt", "hard.txt", "hard2.txt", "soft.txt", "soft2.txt"])
        self.assertEqual(report.reads, ["source.txt", "source2.txt"])

    def test_mode_changes_are_writes(self) -> None:
        report = self.parse(
            '10 chmod("tools/run.sh", 0755) = 0\n'
            f'10 openat(AT_FDCWD, "{self.root / "nested"}", O_RDONLY|O_DIRECTORY) = 3\n'
            '10 fchmodat(3, "script.py", 0755) = 0\n'
        )
        self.assertEqual(report.writes, ["nested/script.py", "tools/run.sh"])

    def test_statx_and_faccessat2_are_reads(self) -> None:
        # coreutils (ls, stat, cp) use statx; glibc access() may use faccessat2.
        report = self.parse(
            '10 statx(AT_FDCWD, "listed.txt", AT_STATX_SYNC_AS_STAT|AT_SYMLINK_NOFOLLOW, STATX_MODE, '
            '{stx_mask=STATX_BASIC_STATS, stx_mode=S_IFREG|0644, ...}) = 0\n'
            '10 faccessat2(AT_FDCWD, "probed.txt", R_OK, AT_EACCESS) = 0\n'
            '10 statx(3, "", AT_EMPTY_PATH, STATX_MODE, {stx_mask=STATX_BASIC_STATS, ...}) = 0\n'
        )
        self.assertEqual(report.reads, ["listed.txt", "probed.txt"])

    def test_fcntl_duplicated_directory_descriptor_keeps_its_directory(self) -> None:
        # Python's os.dup and os.scandir(fd) duplicate with fcntl(F_DUPFD_CLOEXEC), not dup().
        report = self.parse(
            f'10 openat(AT_FDCWD, "{self.root / "nested"}", O_RDONLY|O_CLOEXEC|O_DIRECTORY) = 3\n'
            '10 fcntl(3, F_DUPFD_CLOEXEC, 0) = 4\n'
            '10 newfstatat(4, "entry.txt", {st_mode=S_IFREG|0644, st_size=1, ...}, AT_SYMLINK_NOFOLLOW) = 0\n'
        )
        self.assertEqual(report.reads, ["nested", "nested/entry.txt"])
        self.assertEqual(report.violations, [])

    def test_relative_access_through_unknown_descriptor_fails_closed(self) -> None:
        report = self.parse(
            '10 openat(9, "hidden.txt", O_RDONLY|O_CLOEXEC) = 5\n'
            '10 unlinkat(8, "gone.txt", 0) = -1 EBADF (Bad file descriptor)\n'
        )
        self.assertEqual(report.reads, [])
        self.assertEqual(report.violations, ["unattributable descriptor-relative access: openat(9, 'hidden.txt')"])

    def test_descriptor_replaced_by_unknown_source_is_not_reused_stale(self) -> None:
        report = self.parse(
            f'10 openat(AT_FDCWD, "{self.outside}", O_RDONLY|O_DIRECTORY) = 3\n'
            '10 dup2(7, 3) = 3\n'
            '10 openat(3, "file.txt", O_RDONLY) = 4\n'
        )
        self.assertEqual(report.violations, ["unattributable descriptor-relative access: openat(3, 'file.txt')"])

    def test_threads_share_cwd_and_descriptors_but_fork_children_do_not(self) -> None:
        report = self.parse(
            "10 clone3({flags=CLONE_VM|CLONE_FS|CLONE_FILES|CLONE_SIGHAND|CLONE_THREAD|CLONE_SYSVSEM, "
            "exit_signal=0, stack=0x7f, stack_size=0x7ff}, 88) = 11\n"
            "10 clone(child_stack=NULL, flags=CLONE_CHILD_CLEARTID|CLONE_CHILD_SETTID|SIGCHLD) = 12\n"
            f'10 chdir("{self.outside}") = 0\n'
            '11 openat(AT_FDCWD, "thread-sees-new-cwd.txt", O_RDONLY) = 3\n'
            '12 openat(AT_FDCWD, "fork-child-keeps-old-cwd.txt", O_RDONLY) = 3\n'
            f'11 openat(AT_FDCWD, "{self.root / "nested"}", O_RDONLY|O_DIRECTORY) = 4\n'
            '10 openat(4, "shared-table.txt", O_RDONLY) = 5\n'
            '12 openat(4, "not-in-fork-copy.txt", O_RDONLY) = 5\n'
        )
        self.assertEqual(report.reads, ["fork-child-keeps-old-cwd.txt", "nested", "nested/shared-table.txt"])
        self.assertEqual(
            report.violations, ["unattributable descriptor-relative access: openat(4, 'not-in-fork-copy.txt')"]
        )

    def test_call_that_never_resumes_is_judged_conservatively(self) -> None:
        # A thread's successful execve resumes under the thread-group leader's pid, so the unfinished
        # half never pairs; it must not vanish.
        report = self.parse('21 execve("/usr/bin/curl", ["curl"], 0x0 /* 3 vars */ <unfinished ...>\n')
        self.assertEqual(report.executables, ["/usr/bin/curl"])

    def test_utf8_path_escapes_decode_to_the_real_file_name(self) -> None:
        report = self.parse('10 openat(AT_FDCWD, "caf\\303\\251.txt", O_RDONLY|O_CLOEXEC) = 3\n')
        self.assertEqual(report.reads, ["café.txt"])

    def test_commas_parentheses_and_quotes_inside_paths_do_not_shift_arguments(self) -> None:
        report = self.parse(
            '10 openat(AT_FDCWD, "we,ird) = 3 \\"q\\".txt", O_WRONLY|O_CREAT|O_TRUNC, 0666) = 3\n'
            '10 rename("a, b", "c) = 0") = 0\n'
        )
        self.assertEqual(report.writes, ["a, b", "c) = 0", 'we,ird) = 3 "q".txt'])

    def test_real_git_local_fetch_trace_reports_upload_pack(self) -> None:
        # Excerpt of tests/test_repin_gate_app.py under strace: `git fetch <local path>` runs
        # `/bin/sh -c "git-upload-pack '<path>'"`, whose vfork and execve are both split.
        report = self.parse(
            "1616  clone(child_stack=NULL, flags=CLONE_CHILD_CLEARTID|CLONE_CHILD_SETTID|SIGCHLD, "
            "child_tidptr=0x7efdb173ea10) = 1617\n"
            '1617  execve("/bin/sh", ["/bin/sh", "-c", "git-upload-pack \'/tmp/tmpim7_n0ns/remote\'", '
            '"git-upload-pack \'/tmp/tmpim7_n0ns/remote\'"], 0x55fdbd4319e0 /* 5 vars */) = 0\n'
            '1617  newfstatat(AT_FDCWD, "/usr/lib/git-core/git-upload-pack", {st_mode=S_IFREG|0755, '
            "st_size=4066232, ...}, 0) = 0\n"
            "1617  vfork( <unfinished ...>\n"
            '1618  execve("/usr/lib/git-core/git-upload-pack", ["git-upload-pack", "/tmp/tmpim7_n0ns/remote"], '
            "0x560d698a55d8 /* 6 vars */ <unfinished ...>\n"
            "1617  <... vfork resumed>)              = 1618\n"
            "1618  <... execve resumed>)             = 0\n"
        )
        self.assertEqual(report.executables, ["/bin/sh", "/usr/lib/git-core/git-upload-pack"])


class RuntimePatternAnchoringRegressionTests(unittest.TestCase):
    def test_root_level_patterns_do_not_admit_same_named_files_elsewhere(self) -> None:
        self.assertTrue(_matches("README.md", ("README.md",)))
        self.assertFalse(_matches("docs/README.md", ("README.md",)))
        self.assertFalse(_matches("research/sub/Makefile", ("Makefile",)))
        self.assertFalse(_matches("copy/validation/runtime-policy.json", ("validation/**",)))
        self.assertTrue(_matches("docs/README.md", ("**/README.md",)))

    def test_audit_flags_nested_file_that_only_shares_a_declared_name(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            previous = Path.cwd()
            os.chdir(directory)
            try:
                audited = audit_trace(
                    parse_strace(
                        '10 openat(AT_FDCWD, "docs/README.md", O_RDONLY) = 3\n', cwd=Path(directory), root=Path(directory)
                    ),
                    declared_inputs=("README.md",),
                    command=("python", "check.py"),
                    policy=RuntimePolicy((), (), ("python",), (), True),
                    sandbox_copy=False,
                )
            finally:
                os.chdir(previous)
        self.assertEqual(audited.violations, ["undeclared read: docs/README.md"])


class RuntimePolicyExecutableContractTests(unittest.TestCase):
    """Executables are admitted by exact name only, and each non-core one for a stated reason."""

    POLICY = Path(__file__).resolve().parents[1] / "validation" / "runtime-policy.json"

    def test_git_transport_helper_is_the_only_git_core_program_admitted(self) -> None:
        allowed = json.loads(self.POLICY.read_text(encoding="utf-8"))["allowed_executables"]
        # git-upload-pack is the server half of git's local transport: tests/test_repin_gate_app.py
        # exercises the gate's real `git fetch` against a local fixture remote (production fetches
        # over https). No other git-core program, and no path or glob, is admitted.
        self.assertIn("git-upload-pack", allowed)
        self.assertEqual([name for name in allowed if name.startswith("git-")], ["git-upload-pack"])
        self.assertTrue(all("/" not in name and "*" not in name for name in allowed))


    def test_declared_git_lockfiles_also_declare_the_file_they_replace(self) -> None:
        # git writes X.lock and renames it onto X. The tracer records the rename destination, so a
        # contract that declares only the lock under-declares the file the check actually modifies.
        contract = json.loads(
            (Path(__file__).resolve().parents[1] / "validation" / "runtime-dependencies.json").read_text(encoding="utf-8")
        )
        for check_id, entry in contract["checks"].items():
            outputs = set(entry.get("outputs", []))
            for output in outputs:
                if output.startswith(".git/") and output.endswith(".lock"):
                    self.assertIn(output[: -len(".lock")], outputs, check_id)


if __name__ == "__main__":
    unittest.main()
