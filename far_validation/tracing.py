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
        candidates: list[str] = []
        if current.startswith("**/"):
            candidates.append(current[3:])
        if "/**/" in current:
            candidates.append(current.replace("/**/", "/", 1))
        for collapsed in candidates:
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
        # fnmatch anchors the pattern at the repository root. ``Path.match`` is deliberately not used:
        # it matches relative patterns from the right, so ``README.md`` would admit ``docs/README.md``.
        if any(fnmatch.fnmatch(normalized, candidate) for candidate in variants):
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
_RESUMED = re.compile(r"^<\.\.\.\s+([A-Za-z0-9_]+)\s+resumed>(.*)$")
_RESULT = re.compile(r"^\s*=\s*(\S+)(?:\s+([A-Z][A-Z0-9_]*))?")
_ESCAPE = re.compile(r"\\(x[0-9a-fA-F]{2}|[0-7]{1,3}|.)", re.DOTALL)
_SIMPLE_ESCAPES = {"n": 10, "t": 9, "r": 13, "v": 11, "f": 12, "a": 7, "b": 8, "e": 27}
_WRITE_OPEN_FLAGS = ("O_WRONLY", "O_RDWR", "O_CREAT", "O_TRUNC", "O_APPEND")
# Path-bearing syscalls: (dirfd argument index or None, path argument index, access kind).
# "open" accesses are writes when their flags can create or modify the file, reads otherwise.
# Both operands of rename/link count: the destination of an atomic ``os.replace`` is the output.
_PATH_ARGUMENTS: dict[str, tuple[tuple[int | None, int, str], ...]] = {
    "open": ((None, 0, "open"),),
    "openat": ((0, 1, "open"),),
    "openat2": ((0, 1, "open"),),
    "creat": ((None, 0, "write"),),
    "stat": ((None, 0, "read"),),
    "lstat": ((None, 0, "read"),),
    "access": ((None, 0, "read"),),
    "readlink": ((None, 0, "read"),),
    "newfstatat": ((0, 1, "read"),),
    "statx": ((0, 1, "read"),),
    "faccessat": ((0, 1, "read"),),
    "faccessat2": ((0, 1, "read"),),
    "readlinkat": ((0, 1, "read"),),
    "truncate": ((None, 0, "write"),),
    "unlink": ((None, 0, "write"),),
    "unlinkat": ((0, 1, "write"),),
    "rmdir": ((None, 0, "write"),),
    "mkdir": ((None, 0, "write"),),
    "mkdirat": ((0, 1, "write"),),
    "rename": ((None, 0, "write"), (None, 1, "write")),
    "renameat": ((0, 1, "write"), (2, 3, "write")),
    "renameat2": ((0, 1, "write"), (2, 3, "write")),
    "link": ((None, 0, "read"), (None, 1, "write")),
    "linkat": ((0, 1, "read"), (2, 3, "write")),
    "symlink": ((None, 1, "write"),),
    "symlinkat": ((1, 2, "write"),),
}
_FD_OPENING_CALLS = {"open", "openat", "openat2"}
# A failed lookup relative to an unknown descriptor touched nothing when the descriptor itself was bad.
_HARMLESS_UNKNOWN_DIRFD_ERRORS = {"EBADF", "ENOTDIR"}
TRACED_SYSCALLS = (
    "open,openat,openat2,creat,newfstatat,stat,lstat,statx,access,faccessat,faccessat2,readlink,"
    "readlinkat,truncate,execve,execveat,connect,socket,sendto,recvfrom,unlink,unlinkat,rename,"
    "renameat,renameat2,link,linkat,symlink,symlinkat,mkdir,mkdirat,rmdir,clone,clone3,fork,vfork,"
    "chdir,fchdir,dup,dup2,dup3,fcntl"
)


def _unescape(value: str) -> str:
    """Decode strace's C-style escapes to the exact bytes of the path, then to text.

    strace prints every non-printable byte, including each byte of a UTF-8 sequence, as an escape.
    Decoding escapes as code points would turn a UTF-8 path into mojibake that no declaration matches.
    """
    data = bytearray()
    position = 0
    for match in _ESCAPE.finditer(value):
        data += value[position:match.start()].encode("utf-8", "surrogateescape")
        token = match.group(1)
        if token.startswith("x") and len(token) == 3:
            data.append(int(token[1:], 16))
        elif token[0] in "01234567":
            data.append(int(token, 8) & 0xFF)
        elif token in _SIMPLE_ESCAPES:
            data.append(_SIMPLE_ESCAPES[token])
        else:
            data += token.encode("utf-8", "surrogateescape")
        position = match.end()
    data += value[position:].encode("utf-8", "surrogateescape")
    return bytes(data).decode("utf-8", "surrogateescape")


def _split_pid(line: str) -> tuple[int, str]:
    match = _PID_PREFIX.match(line)
    if not match:
        return 0, line
    return int(match.group(1) or match.group(2)), line[match.end():]


def _logical_strace_lines(text: str) -> list[str]:
    """Reassemble strace's scheduler-dependent unfinished/resumed syscall pairs.

    The combined syscall is ordered where it started, not where it resumed. This is essential for
    fork/vfork/clone: the child can run before the parent prints the resumed result, but its inherited
    cwd/fd state must already exist when the child events are interpreted. A call that never resumes
    (the process was killed, or a thread's successful execve resumed under the thread-group leader's
    pid) is kept without a result rather than dropped, so it is judged conservatively.
    """
    pending: dict[int, tuple[int, str]] = {}
    complete: list[tuple[int, str]] = []
    for index, line in enumerate(text.splitlines()):
        raw = line.strip()
        pid, stripped = _split_pid(raw)
        if "<unfinished ...>" in stripped:
            prefix = stripped.split("<unfinished ...>", 1)[0].rstrip()
            pending[pid] = (index, prefix)
            continue
        resumed = _RESUMED.match(stripped)
        if resumed:
            started = pending.pop(pid, None)
            if started is not None:
                start_index, prefix = started
                complete.append((start_index, f"{pid} {prefix}{resumed.group(2)}"))
            continue
        complete.append((index, raw))
    complete.extend((start_index, f"{pid} {prefix}") for pid, (start_index, prefix) in pending.items())
    complete.sort(key=lambda item: item[0])
    return [line for _index, line in complete]


@dataclass
class _Syscall:
    name: str
    arguments: list[str]
    result: str | None  # None when the call never returned in the trace
    errno: str | None

    @property
    def failed(self) -> bool:
        return self.result is not None and self.result.startswith("-")

    def number(self) -> int | None:
        return int(self.result) if self.result is not None and self.result.isdigit() else None


def _parse_syscall(stripped: str) -> _Syscall | None:
    """Split ``name(arg, arg, ...) = result ERRNO`` at top-level commas, respecting strings and nesting."""
    open_index = stripped.find("(")
    head = stripped[:open_index].split() if open_index > 0 else []
    if not head:
        return None
    arguments: list[str] = []
    current: list[str] = []
    depth = 0
    in_string = False
    rest = ""
    index = open_index + 1
    while index < len(stripped):
        char = stripped[index]
        if in_string:
            current.append(char)
            if char == "\\" and index + 1 < len(stripped):
                current.append(stripped[index + 1])
                index += 2
                continue
            if char == '"':
                in_string = False
        elif char == '"':
            in_string = True
            current.append(char)
        elif char in "([{":
            depth += 1
            current.append(char)
        elif char == ")" and depth == 0:
            rest = stripped[index + 1:]
            break
        elif char in ")]}":
            depth -= 1
            current.append(char)
        elif char == "," and depth == 0:
            arguments.append("".join(current).strip())
            current = []
        else:
            current.append(char)
        index += 1
    last = "".join(current).strip()
    if last or arguments:
        arguments.append(last)
    outcome = _RESULT.match(rest)
    return _Syscall(head[-1], arguments, outcome.group(1) if outcome else None, outcome.group(2) if outcome else None)


def _argument_path(argument: str) -> str | None:
    quoted = _QUOTED.match(argument)
    return _unescape(quoted.group(1)) if quoted else None


def _descriptor(argument: str) -> int | str | None:
    token = argument.split("<", 1)[0].strip()
    if token == "AT_FDCWD":
        return token
    return int(token) if token.isdigit() else None


class _PathUnattributable(Exception):
    """A relative path was resolved against a descriptor whose directory the trace never observed."""


def _resolve(
    call: _Syscall, dirfd_index: int | None, path_index: int, cwd: Path, fds: dict[int, Path]
) -> Path | None:
    if path_index >= len(call.arguments):
        return None
    raw = _argument_path(call.arguments[path_index])
    if raw is None or raw == "":
        return None  # a NULL/pointer argument, or AT_EMPTY_PATH: the descriptor itself was opened earlier
    candidate = Path(raw)
    if candidate.is_absolute():
        return candidate.resolve(strict=False)
    if dirfd_index is None:
        return (cwd / candidate).resolve(strict=False)
    descriptor = _descriptor(call.arguments[dirfd_index]) if dirfd_index < len(call.arguments) else None
    if descriptor == "AT_FDCWD":
        return (cwd / candidate).resolve(strict=False)
    base = fds.get(descriptor) if isinstance(descriptor, int) else None
    if base is None:
        raise _PathUnattributable(raw)
    return (base / candidate).resolve(strict=False)


def _clone_shares(line: str, flag: str) -> bool:
    return re.search(rf"\b{flag}\b", line) is not None


def parse_strace(text: str, *, cwd: Path, root: Path) -> TraceReport:
    report = TraceReport(backend="strace", raw_trace=text[-1_000_000:])
    reads: set[str] = set()
    writes: set[str] = set()
    executables: set[str] = set()
    network: set[str] = set()
    unattributable: set[str] = set()
    initial_cwd = cwd.resolve()
    # Filesystem context and descriptor table per pid. Threads and CLONE_FS/CLONE_FILES children share
    # the parent's objects (a chdir or open in one is visible to all); fork/vfork children get copies.
    fs_by_pid: dict[int, list[Path]] = {}
    fds_by_pid: dict[int, dict[int, Path]] = {}

    for line in _logical_strace_lines(text):
        raw = line.strip()
        pid, stripped = _split_pid(raw)
        call = _parse_syscall(stripped)
        if call is None:
            continue
        fs = fs_by_pid.setdefault(pid, [initial_cwd])
        fds = fds_by_pid.setdefault(pid, {})
        name = call.name

        if name in {"clone", "clone3", "fork", "vfork"}:
            child = call.number()
            if child is not None:
                fs_by_pid[child] = fs if _clone_shares(stripped, "CLONE_FS") else [fs[0]]
                fds_by_pid[child] = fds if _clone_shares(stripped, "CLONE_FILES") else dict(fds)
            continue
        if name == "chdir" and not call.failed:
            try:
                target = _resolve(call, None, 0, fs[0], fds)
            except _PathUnattributable:
                target = None
            if target is not None:
                fs[0] = target
            continue
        if name == "fchdir" and not call.failed:
            descriptor = _descriptor(call.arguments[0]) if call.arguments else None
            if isinstance(descriptor, int) and descriptor in fds:
                fs[0] = fds[descriptor]
            continue
        if name in {"dup", "dup2", "dup3", "fcntl"}:
            if name == "fcntl" and (len(call.arguments) < 2 or not call.arguments[1].startswith("F_DUPFD")):
                continue
            target_fd = call.number()
            source = _descriptor(call.arguments[0]) if call.arguments else None
            if target_fd is not None and not call.failed:
                if isinstance(source, int) and source in fds:
                    fds[target_fd] = fds[source]
                else:
                    fds.pop(target_fd, None)
            continue
        if name in {"execve", "execveat"}:
            if not call.failed:
                path_index = 1 if name == "execveat" else 0
                executable = _argument_path(call.arguments[path_index]) if len(call.arguments) > path_index else None
                if executable:
                    executables.add(executable)
            continue
        if name in {"connect", "sendto", "recvfrom"}:
            if "AF_INET" in stripped or "AF_INET6" in stripped:
                network.add(stripped[:500])
            continue
        operands = _PATH_ARGUMENTS.get(name)
        if operands is None:
            continue

        opened: Path | None = None
        for dirfd_index, path_index, kind in operands:
            try:
                observed = _resolve(call, dirfd_index, path_index, fs[0], fds)
            except _PathUnattributable as exc:
                if call.errno not in _HARMLESS_UNKNOWN_DIRFD_ERRORS:
                    unattributable.add(f"{name}({call.arguments[dirfd_index or 0]}, {exc.args[0]!r})")
                continue
            if observed is None:
                continue
            opened = observed
            relative = _inside(observed, root)
            if relative in {None, "."}:
                continue
            if kind == "open":
                flags = _OPEN_FLAGS.search(" ".join(call.arguments[path_index + 1:]))
                kind = "write" if flags and any(token in flags.group(1) for token in _WRITE_OPEN_FLAGS) else "read"
            (writes if kind == "write" else reads).add(relative)
        if name in _FD_OPENING_CALLS and not call.failed:
            descriptor = call.number()
            if descriptor is not None:
                if opened is not None:
                    fds[descriptor] = opened
                else:
                    fds.pop(descriptor, None)

    report.reads = sorted(reads)
    report.writes = sorted(writes)
    report.executables = sorted(executables)
    report.network_attempts = sorted(network)
    report.violations = [f"unattributable descriptor-relative access: {item}" for item in sorted(unattributable)]
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
        f"trace={TRACED_SYSCALLS}",
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


def _directory_metadata(path: str) -> bool:
    return (Path.cwd() / path).is_dir()


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
        if _derived_python_cache(path) or _directory_metadata(path):
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
