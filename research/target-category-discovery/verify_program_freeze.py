#!/usr/bin/env python3
"""Verify exact public-control blobs, prompt registry shape, and path safety."""
from __future__ import annotations

import hashlib, json, re, subprocess, sys, unicodedata
from pathlib import Path

PROGRAM_DIR = Path(__file__).resolve().parent
REPO_ROOT = PROGRAM_DIR.parents[1]
DEFAULT_MANIFEST = PROGRAM_DIR / "freeze-manifest-v1.0.json"
PROMPTS_PATH = PROGRAM_DIR / "execution-prompts-v1.0.json"
HEX40 = re.compile(r"[0-9a-f]{40}\Z")
EXPECTED_PROMPTS = ["TCD-A1-PROMPT-001", "TCD-A2-PROMPT-001", "TCD-B1-PROMPT-001"]
EXPECTED_NORMALIZATION = "UTF-8; Unicode NFC; LF; trim trailing horizontal whitespace; exactly one terminal LF"

class FreezeError(RuntimeError): pass

def normalize_prompt(text: str) -> bytes:
    text = unicodedata.normalize("NFC", text.replace("\r\n", "\n").replace("\r", "\n"))
    return ("\n".join(line.rstrip(" \t") for line in text.split("\n")).rstrip("\n") + "\n").encode("utf-8")

def safe_file(root: Path, rel: str) -> Path:
    if not rel or rel.startswith("/") or "\\" in rel or any(p in {"", ".", ".."} for p in rel.split("/")):
        raise FreezeError(f"unsafe path: {rel!r}")
    cur = root
    for part in rel.split("/"):
        cur = cur / part
        if cur.is_symlink(): raise FreezeError(f"symlink rejected: {rel}")
    if not cur.is_file(): raise FreezeError(f"missing regular file: {rel}")
    return cur

def git_blob(path: Path) -> str:
    return subprocess.check_output(["git", "hash-object", "--no-filters", str(path)], text=True).strip()

def verify_prompts(path: Path = PROMPTS_PATH) -> dict[str, str]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("execution_authorized") is not False: raise FreezeError("prompts must keep execution blocked")
    if data.get("normalization") != EXPECTED_NORMALIZATION: raise FreezeError("prompt normalization mismatch")
    prompts = data.get("prompts")
    if not isinstance(prompts, list) or [p.get("id") for p in prompts] != EXPECTED_PROMPTS:
        raise FreezeError("prompt ID/order mismatch")
    result = {}
    for prompt in prompts:
        text = prompt.get("text")
        if not isinstance(text, str) or not text.strip(): raise FreezeError("empty prompt text")
        result[prompt["id"]] = hashlib.sha256(normalize_prompt(text)).hexdigest()
    return result

def verify(manifest_path: Path = DEFAULT_MANIFEST, root: Path = REPO_ROOT) -> dict[str, object]:
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    if data.get("schema_version") != "1.0" or data.get("program_id") != "TCD-CLEANROOM-001": raise FreezeError("manifest identity mismatch")
    if data.get("artifact_status") != "Research" or data.get("execution_authorized") is not False: raise FreezeError("status/gate mismatch")
    entries = data.get("files")
    if not isinstance(entries, list): raise FreezeError("files must be a list")
    paths = [e.get("path") for e in entries if isinstance(e, dict)]
    if len(paths) != len(entries) or paths != sorted(paths): raise FreezeError("paths must be complete and sorted")
    if len(set(paths)) != len(paths): raise FreezeError("duplicate path")
    for entry in entries:
        rel, expected = entry["path"], entry.get("git_blob_sha1")
        if not isinstance(expected, str) or not HEX40.fullmatch(expected): raise FreezeError(f"invalid blob ID: {rel}")
        actual = git_blob(safe_file(root, rel))
        if actual != expected: raise FreezeError(f"blob mismatch: {rel}: {actual} != {expected}")
    prompt_hashes = verify_prompts(root / "research/target-category-discovery/execution-prompts-v1.0.json")
    return {"status": "PASS", "files_checked": len(entries), "prompt_sha256": prompt_hashes}

def main() -> int:
    try: result = verify()
    except (OSError, subprocess.CalledProcessError, json.JSONDecodeError, FreezeError) as exc:
        print(f"FAIL: {exc}", file=sys.stderr); return 1
    print(f"PASS: {result['files_checked']} governed public artifacts match exact Git blob identities; prompt registry valid.")
    print(json.dumps(result["prompt_sha256"], sort_keys=True))
    return 0

if __name__ == "__main__": raise SystemExit(main())
