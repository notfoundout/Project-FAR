from __future__ import annotations
import importlib.util, json, tempfile, unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MOD = ROOT / "research/target-category-discovery/verify_program_freeze.py"
MANIFEST = ROOT / "research/target-category-discovery/freeze-manifest-v1.0.json"
PROMPTS = ROOT / "research/target-category-discovery/execution-prompts-v1.0.json"
spec = importlib.util.spec_from_file_location("verify_program_freeze", MOD); assert spec and spec.loader
module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)

class ProgramFreezeTests(unittest.TestCase):
    def test_current_freeze_passes(self):
        result = module.verify(); self.assertEqual(result["status"], "PASS")
        self.assertEqual(set(result["prompt_sha256"]), set(module.EXPECTED_PROMPTS))

    def test_prompt_text_mutation_changes_digest(self):
        data = json.loads(PROMPTS.read_text())
        original = module.verify_prompts(PROMPTS)
        data["prompts"][0]["text"] += " mutated"
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp)/"p.json"; p.write_text(json.dumps(data))
            mutated = module.verify_prompts(p)
            self.assertNotEqual(original["TCD-A1-PROMPT-001"], mutated["TCD-A1-PROMPT-001"])

    def test_same_byte_symlink_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); real = root/"real.txt"; real.write_bytes(b"x")
            link = root/"link.txt"
            try: link.symlink_to(real)
            except (OSError, NotImplementedError): self.skipTest("symlinks unavailable")
            with self.assertRaisesRegex(module.FreezeError, "symlink rejected"):
                module.safe_file(root, "link.txt")

    def test_unsafe_paths_are_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            for value in ("", "/x", "../x", "a\\b", "./x", "a//b"):
                with self.subTest(value=value), self.assertRaises(module.FreezeError): module.safe_file(root, value)

    def test_duplicate_manifest_path_is_rejected(self):
        data = json.loads(MANIFEST.read_text())
        data["files"].append(dict(data["files"][0]))
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp)/"m.json"; p.write_text(json.dumps(data))
            with self.assertRaisesRegex(module.FreezeError, "sorted|duplicate"): module.verify(p)

if __name__ == "__main__": unittest.main()
