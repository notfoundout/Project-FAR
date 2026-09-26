from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from far_validation.tracing import parse_strace


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


if __name__ == "__main__":
    unittest.main()
