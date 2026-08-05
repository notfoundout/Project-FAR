from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "research/target-category-discovery/restricted_package_commitment.py"
spec = importlib.util.spec_from_file_location("restricted_package_commitment", MODULE_PATH)
assert spec and spec.loader
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class RestrictedPackageCommitmentTests(unittest.TestCase):
    def test_order_independent_commitment(self) -> None:
        with tempfile.TemporaryDirectory() as first, tempfile.TemporaryDirectory() as second:
            a = Path(first)
            b = Path(second)
            (a / "z.txt").write_bytes(b"z")
            (a / "a.txt").write_bytes(b"a")
            (b / "a.txt").write_bytes(b"a")
            (b / "z.txt").write_bytes(b"z")
            one = module.build_commitment(a, "pilot-1", "decl-1", "after-freeze")
            two = module.build_commitment(b, "pilot-1", "decl-1", "after-freeze")
            self.assertEqual(one["canonical_manifest_sha256"], two["canonical_manifest_sha256"])
            self.assertEqual(one["merkle_root"], two["merkle_root"])

    def test_byte_mutation_changes_root(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = root / "a.txt"
            path.write_bytes(b"a")
            first = module.build_commitment(root, "v1", "d1", "gate")
            path.write_bytes(b"b")
            second = module.build_commitment(root, "v1", "d1", "gate")
            self.assertNotEqual(first["merkle_root"], second["merkle_root"])

    def test_path_mutation_changes_root(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = root / "a.txt"
            path.write_bytes(b"a")
            first = module.build_commitment(root, "v1", "d1", "gate")
            path.rename(root / "b.txt")
            second = module.build_commitment(root, "v1", "d1", "gate")
            self.assertNotEqual(first["merkle_root"], second["merkle_root"])

    def test_symlink_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            target = root / "target.txt"
            target.write_bytes(b"x")
            link = root / "link.txt"
            try:
                link.symlink_to(target)
            except (OSError, NotImplementedError):
                self.skipTest("symlinks unavailable")
            with self.assertRaises(module.CommitmentError):
                module.collect_entries(root)


    def test_hard_link_alias_is_rejected(self) -> None:
        import os
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            first = root / "first.txt"
            second = root / "second.txt"
            first.write_bytes(b"x")
            try:
                os.link(first, second)
            except (OSError, NotImplementedError):
                self.skipTest("hard links unavailable")
            with self.assertRaises(module.CommitmentError):
                module.collect_entries(root)

    def test_unsafe_paths_are_rejected(self) -> None:
        for value in ("../x", "/x", "a\\b", "./x", "a//b", "a/./b", ""):
            with self.subTest(value=value):
                with self.assertRaises(module.CommitmentError):
                    module.normalize_relative_path(value)

    def test_empty_package_is_deterministic(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            result = module.build_commitment(Path(tmp), "v1", "d1", "gate")
            self.assertEqual(result["file_count"], 0)
            self.assertEqual(
                result["merkle_root"],
                module.hashlib.sha256(b"empty\0").hexdigest(),
            )


if __name__ == "__main__":
    unittest.main()
