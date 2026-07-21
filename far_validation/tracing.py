from __future__ import annotations

import fnmatch
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Iterable


@dataclass
class TraceReport:
    backend: str
    reads: list[str] = field(default_factory=list)
    writes: list[str] = field(default_factory=list)
    executables: list[str] = field(default_factory=list)
    network_attempts: list[str] = field(default_factory=list)
    violations: list[str] = field(default_factory=list)
    raw_trace: str = ""

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


@dataclass(frozen=True)
class RuntimePolicy:
    allow_read_patterns: tuple[str, ...]
    allow_write_patterns: tuple[str, ...]
    allowed_executables: tuple[str, ...]
    skip_checks: tuple[str, ...]
    deny_network: bool

    @classmethod
    def load(cls, path: Path) -> "RuntimePolicy":
        payload = json.loads(path.read_text(encoding="utf-8"))
        if payload.get("schema_version") != "1.0":
            raise ValueError("unsupported runtime policy schema")
        return cls(
            allow_read_patterns=tuple(payload.get("allow_read_patterns", [])),
            allow_write_patterns=tuple(payload.get("allow_write_patterns", [])),
            allowed_executables=tuple(payload.get("allowed_executables", [])),
            skip_checks=tuple(payload.get("skip_checks", [])),
            deny_network=payload.get("network_policy", "deny") == "deny",
        )


def _matches(path: str, patterns: Iterable[str]) -> bool:
    normalized = path.replace(os.sep, "/")
    for pattern in patterns:
        if fnmatch.fnmatch(normalized, pattern) or Path(normalized).match(pattern):
            return True
        if pattern.endswith("/**"):
            prefix = pattern[:-3].rstrip("/")
            if normalized == prefix or normalized.startswith(prefix + "/"):
                return True
    return False


def _inside(path: Path, root: Path) -> str | None:
    try:
        return path.resolve(strict=False).relative_to(root.resolve()).as_posix()
    except ValueError:
        return None


def _normalize_observed(raw: str, cwd: Path, root: Path) -> str | None:
    if raw in {"", ".", ".."}:
        return None
    candidate = Path(raw)
    if not candidate.is_absolute():
        candidate = cwd / candidate
    return _inside(candidate, root)


_QUOTED = re.compile(r'"((?:[^"\\]|\\.)*)"')
_OPEN_FLAGS = re.compile(r"\b(O_[A-Z0-9_|]+)\b")


def _unescape(value: str) -> str:
    try:
        return bytes(value, "utf-8").decode("unicode_escape")
    except UnicodeDecodeError:
        return value


def parse_strace(text: str, *, cwd: Path, root: Path) -> TraceReport:
    report = TraceReport(backend="strace", raw_trace=text[-1_000_000:])
    reads: set[str] = set()
    writes: set[str] = set()
    executables: set[str] = set()
    network: set[str] = set()
    for line in text.splitlines():
        stripped = re.sub(r"^\[pid\s+\d+\]\s*", "", line.strip())
        if "<unfinished ...>" in stripped or "resumed>" in stripped:
            continue
        call = stripped.split("(", 1)[0].split()[-1] if "(" in stripped else ""
        quoted = [_unescape(item) for item in _QUOTED.findall(stripped)]
        if call == "execve" and quoted:
            executables.add(quoted[0])
            continue
        if call == "connect":
            if "AF_INET" in stripped or "AF_INET6" in stripped:
                network.add(stripped[:500])
            continue
        if call in {"sendto", "recvfrom"}:
            if "AF_INET" in stripped or "AF_INET6" in stripped:
                network.add(stripped[:500])
            continue
        if call not in {
            "open", "openat", "newfstatat", "stat", "lstat", "access", "readlink", "readlinkat",
            "unlink", "unlinkat", "rename", "renameat", "renameat2", "mkdir", "mkdirat", "rmdir",
        }:
            continue
        if not quoted:
            continue
        raw_path = quoted[0]
        if call in {"openat", "newfstatat", "unlinkat", "mkdirat", "readlinkat"} and len(quoted) > 1:
            raw_path = quoted[1]
        relative = _normalize_observed(raw_path, cwd, root)
        if relative is None:
            continue
        is_write = call in {"unlink", "unlinkat", "rename", "renameat", "renameat2", "mkdir", "mkdirat", "rmdir"}
        flags = _OPEN_FLAGS.search(stripped)
        if flags and any(token in flags.group(1) for token in ("O_WRONLY", "O_RDWR", "O_CREAT", "O_TRUNC", "O_APPEND")):
            is_write = True
        (writes if is_write else reads).add(relative)
    report.reads = sorted(reads)
    report.writes = sorted(writes)
    report.executables = sorted(executables)
    report.network_attempts = sorted(network)
    return report


def run_traced(
    command: list[str],
    *,
    cwd: Path,
    repository_root: Path,
    env: dict[str, str],
    timeout: int,
) -> tuple[subprocess.CompletedProcess[str], TraceReport]:
    strace = shutil.which("strace") if sys.platform.startswith("linux") else None
    if not strace:
        completed = subprocess.run(
            command,
            cwd=cwd,
            env=env,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout,
            check=False,
        )
        return completed, TraceReport(backend="unavailable")
    with tempfile.NamedTemporaryFile(prefix="far-trace-", suffix=".log", delete=False) as handle:
        trace_path = Path(handle.name)
    traced = [
        strace,
        "-f",
        "-qq",
        "-s",
        "4096",
        "-e",
        "trace=open,openat,newfstatat,stat,lstat,access,readlink,readlinkat,execve,connect,socket,sendto,recvfrom,unlink,unlinkat,rename,renameat,renameat2,mkdir,mkdirat,rmdir",
        "-o",
        str(trace_path),
        "--",
        *command,
    ]
    try:
        completed = subprocess.run(
            traced,
            cwd=cwd,
            env=env,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout,
            check=False,
        )
        raw = trace_path.read_text(encoding="utf-8", errors="replace") if trace_path.exists() else ""
        return completed, parse_strace(raw, cwd=cwd, root=repository_root)
    finally:
        trace_path.unlink(missing_ok=True)


def audit_trace(
    report: TraceReport,
    *,
    declared_inputs: Iterable[str],
    declared_outputs: Iterable[str] = (),
    command: Iterable[str],
    policy: RuntimePolicy,
    sandbox_copy: bool,
) -> TraceReport:
    command_paths = [item for item in command if "/" in item or item.endswith(".py")]
    read_patterns = tuple(declared_inputs) + policy.allow_read_patterns + tuple(command_paths)
    for path in report.reads:
        if not _matches(path, read_patterns):
            report.violations.append(f"undeclared read: {path}")
    if not sandbox_copy:
        write_patterns = tuple(declared_outputs) + policy.allow_write_patterns
        for path in report.writes:
            if not _matches(path, write_patterns):
                report.violations.append(f"undeclared write: {path}")
    allowed = set(policy.allowed_executables)
    for executable in report.executables:
        name = Path(executable).name
        if name not in allowed and executable not in allowed:
            report.violations.append(f"undeclared executable: {executable}")
    if policy.deny_network and report.network_attempts:
        for attempt in report.network_attempts[:20]:
            report.violations.append(f"network access denied: {attempt}")
    report.violations = sorted(set(report.violations))
    return report
