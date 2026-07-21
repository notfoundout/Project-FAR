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


def _pattern_variants(pattern: str) -> set[str]:
    variants = {pattern}
    pending = [pattern]
    while pending:
        current = pending.pop()
        if "/**/" not in current:
            continue
        collapsed = current.replace("/**/", "/", 1)
        if collapsed not in variants:
            variants.add(collapsed)
            pending.append(collapsed)
    return variants


def _literal_prefix(pattern: str) -> str:
    positions = [pattern.find(char) for char in "*?[" if char in pattern]
    end = min(positions) if positions else len(pattern)
    return pattern[:end].rstrip("/")


def _matches(path: str, patterns: Iterable[str]) -> bool:
    normalized = path.replace(os.sep, "/")
    for pattern in patterns:
        variants = _pattern_variants(pattern)
        if any(
            fnmatch.fnmatch(normalized, candidate) or Path(normalized).match(candidate)
            for candidate in variants
        ):
            return True
        if pattern.endswith("/**"):
            prefix = pattern[:-3].rstrip("/")
            if normalized == prefix or normalized.startswith(prefix + "/"):
                return True
        prefix = _literal_prefix(pattern)
        if prefix and (prefix == normalized or prefix.startswith(normalized + "/")):
            return True
    return False


def _inside(path: Path, root: Path) -> str | None:
    try:
        return path.resolve(strict=False).relative_to(root.resolve()).as_posix()
    except ValueError:
        return None


def _absolute_observed(raw: str, cwd: Path) -> Path | None:
    if raw in {"", ".", ".."}:
        return None
    candidate = Path(raw)
    if not candidate.is_absolute():
        candidate = cwd / candidate
    return candidate.resolve(strict=False)


def _normalize_observed(raw: str, cwd: Path, root: Path) -> str | None:
    candidate = _absolute_observed(raw, cwd)
    if candidate is None:
        return None
    relative = _inside(candidate, root)
    return None if relative in {None, "."} else relative


_QUOTED = re.compile(r'"((?:[^"\\]|\\.)*)"')
_OPEN_FLAGS = re.compile(r"\b(O_[A-Z0-9_|]+)\b")
_PID_PREFIX = re.compile(r"^(?:(?:\[pid\s+(\d+)\])|(\d+))\s+")
_CHILD_RESULT = re.compile(r"=\s+(\d+)\s*$")
_FAILED_RESULT = re.compile(r"=\s+-1\b")


def _unescape(value: str) -> str:
    try:
        return bytes(value, "utf-8").decode("unicode_escape")
    except UnicodeDecodeError:
        return value


def _split_pid(line: str) -> tuple[int, str]:
    match = _PID_PREFIX.match(line)
    if not match:
        return 0, line
    return int(match.group(1) or match.group(2)), line[match.end():]


def _at_path(call: str, stripped: str, quoted: list[str]) -> str | None:
    if not quoted:
        return None
    if call in {"openat", "newfstatat", "unlinkat", "mkdirat", "readlinkat", "renameat", "renameat2"}:
        before_quote = stripped.split('"', 1)[0]
        if "AT_FDCWD" not in before_quote and not Path(quoted[0]).is_absolute():
            return None
        return quoted[0]
    return quoted[0]


def parse_strace(text: str, *, cwd: Path, root: Path) -> TraceReport:
    report = TraceReport(backend="strace", raw_trace=text[-1_000_000:])
    reads: set[str] = set()
    writes: set[str] = set()
    executables: set[str] = set()
    network: set[str] = set()
    cwd_by_pid: dict[int, Path] = {0: cwd.resolve()}

    for line in text.splitlines():
        raw = line.strip()
        pid, stripped = _split_pid(raw)
        current_cwd = cwd_by_pid.setdefault(pid, cwd.resolve())
        if "<unfinished ...>" in stripped or "resumed>" in stripped:
            continue
        call = stripped.split("(", 1)[0].split()[-1] if "(" in stripped else ""
        quoted = [_unescape(item) for item in _QUOTED.findall(stripped)]

        if call in {"clone", "clone3", "fork", "vfork"}:
            child = _CHILD_RESULT.search(stripped)
            if child:
                cwd_by_pid[int(child.group(1))] = current_cwd
            continue
        if call == "chdir" and quoted and not _FAILED_RESULT.search(stripped):
            new_cwd = _absolute_observed(quoted[0], current_cwd)
            if new_cwd is not None:
                cwd_by_pid[pid] = new_cwd
            continue
        if call == "execve" and quoted:
            if not _FAILED_RESULT.search(stripped):
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
        raw_path = _at_path(call, stripped, quoted)
        if raw_path is None:
            continue
        relative = _normalize_observed(raw_path, current_cwd, root)
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
        "trace=open,openat,newfstatat,stat,lstat,access,readlink,readlinkat,execve,connect,socket,sendto,recvfrom,unlink,unlinkat,rename,renameat,renameat2,mkdir,mkdirat,rmdir,clone,clone3,fork,vfork,chdir,fchdir",
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


def _derived_python_cache(path: str) -> bool:
    parts = Path(path).parts
    return "__pycache__" in parts or path.endswith((".pyc", ".pyo"))


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
        if _derived_python_cache(path):
            continue
        if not _matches(path, read_patterns):
            report.violations.append(f"undeclared read: {path}")
    if not sandbox_copy:
        write_patterns = tuple(declared_outputs) + policy.allow_write_patterns
        for path in report.writes:
            if _derived_python_cache(path):
                continue
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
