from __future__ import annotations
import os, re, subprocess, sys, time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP_DIRS = {'.git', '.mypy_cache', '.pytest_cache', '__pycache__', '.venv', 'venv', 'node_modules'}
LINK_RE = re.compile(r'(!?)\[([^\]\n]*)\]\(([^)\n]*)\)')
HEADING_RE = re.compile(r'^(#{1,6})\s+(.+?)\s*#*\s*$')

def rel(path: Path) -> str:
    try: return path.resolve().relative_to(ROOT).as_posix()
    except Exception: return path.as_posix()

def iter_files(suffixes, roots=None):
    bases = [ROOT / r for r in (roots or ['.'])]
    for base in bases:
        if not base.exists(): continue
        if base.is_file():
            if base.suffix.lower() in suffixes: yield base
            continue
        for dirpath, dirnames, filenames in os.walk(base):
            dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
            for name in filenames:
                p = Path(dirpath) / name
                if p.suffix.lower() in suffixes:
                    yield p

def is_external(target: str) -> bool:
    t = target.strip().lower()
    return bool(re.match(r'^[a-z][a-z0-9+.-]*:', t)) or t.startswith('//')

def is_ignored_link(target: str) -> bool:
    t = target.strip()
    low = t.lower()
    return (not t or low.startswith(('mailto:', '#')) or is_external(t)
            or 'github.com/' in low and '/releases/' in low
            or any(x in low for x in ('img.shields.io', 'badge.svg', 'badgen.net', 'codecov.io')))

def strip_anchor(target: str) -> str:
    return target.split('#', 1)[0].split('?', 1)[0].replace('%20', ' ')

def markdown_links(text: str):
    for i, line in enumerate(text.splitlines(), 1):
        for m in LINK_RE.finditer(line):
            yield i, m.group(3).strip(), bool(m.group(1)), m.group(2)

DEFAULT_HEALTH_TIMEOUT_SECONDS = int(os.environ.get("PROJECT_FAR_HEALTH_TIMEOUT", "120"))

def run(cmd, cwd=ROOT, timeout: int | float | None = DEFAULT_HEALTH_TIMEOUT_SECONDS):
    start = time.monotonic()
    try:
        return subprocess.run(cmd, cwd=cwd, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=timeout)
    except subprocess.TimeoutExpired as exc:
        elapsed = time.monotonic() - start
        stdout = exc.stdout or ""
        stderr = exc.stderr or ""
        if isinstance(stdout, bytes):
            stdout = stdout.decode(errors="replace")
        if isinstance(stderr, bytes):
            stderr = stderr.decode(errors="replace")
        output = stdout + stderr
        message = (
            f"TIMEOUT after {timeout} seconds (elapsed {elapsed:.1f}s): {' '.join(map(str, cmd))}\n"
            f"{output}"
        )
        return subprocess.CompletedProcess(cmd, 124, message, "")
