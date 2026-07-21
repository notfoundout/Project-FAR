from __future__ import annotations

import fnmatch
import hashlib
import json
import os
import platform
import shutil
import subprocess
import sys
import tempfile
import time
import uuid
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

from .manifest import load_manifest
from .model import CheckDefinition, CheckResult, RunSummary

ENGINE_VERSION = "0.1.0"


class ValidationEngineError(RuntimeError):
    pass


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _git(root: Path, *args: str) -> str:
    completed = subprocess.run(
        ["git", *args],
        cwd=root,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if completed.returncode != 0:
        return "unknown"
    return completed.stdout.strip() or "unknown"


def _safe_relative(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def _iter_input_files(root: Path, patterns: Iterable[str]) -> list[Path]:
    files: dict[str, Path] = {}
    for pattern in patterns:
        if any(char in pattern for char in "*?["):
            for path in root.glob(pattern):
                if path.is_file() and ".git" not in path.parts and ".far" not in path.parts:
                    files[_safe_relative(path, root)] = path
        else:
            path = root / pattern
            if path.is_file():
                files[_safe_relative(path, root)] = path
            elif path.is_dir():
                for child in path.rglob("*"):
                    if child.is_file() and ".git" not in child.parts and ".far" not in child.parts:
                        files[_safe_relative(child, root)] = child
    return [files[name] for name in sorted(files)]


def _snapshot_files(root: Path) -> dict[str, str]:
    snapshot: dict[str, str] = {}
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        if ".git" in path.parts or ".far" in path.parts or "__pycache__" in path.parts:
            continue
        snapshot[_safe_relative(path, root)] = _sha256_file(path)
    return snapshot


def _matches(path: str, patterns: Iterable[str]) -> bool:
    normalized = path.replace(os.sep, "/")
    for pattern in patterns:
        if fnmatch.fnmatch(normalized, pattern) or Path(normalized).match(pattern):
            return True
        prefix = pattern.rstrip("/**")
        if pattern.endswith("/**") and (normalized == prefix or normalized.startswith(prefix + "/")):
            return True
    return False


class ValidationEngine:
    def __init__(
        self,
        root: Path,
        manifest_path: Path | None = None,
        jobs: int | None = None,
        use_cache: bool = True,
        verbose: bool = False,
    ) -> None:
        self.root = root.resolve()
        self.manifest_path = manifest_path or self.root / "validation" / "manifest.json"
        self.manifest = load_manifest(self.manifest_path)
        self.jobs = max(1, jobs or min(8, (os.cpu_count() or 2)))
        self.use_cache = use_cache
        self.verbose = verbose
        self.far_dir = self.root / ".far"
        self.cache_dir = self.far_dir / "cache"
        self.runs_dir = self.far_dir / "runs"
        self.failures_dir = self.far_dir / "failures"
        for directory in (self.cache_dir, self.runs_dir, self.failures_dir):
            directory.mkdir(parents=True, exist_ok=True)

    def run(
        self,
        profile: str = "pr-fast",
        check_ids: Iterable[str] | None = None,
        changed_base: str | None = None,
        explain: bool = False,
        continue_after_failure: bool = False,
    ) -> RunSummary:
        started_at = _utc_now()
        start = time.monotonic()
        changed_files: list[str] = []
        selection_notes: list[str] = []
        fallback = False

        if check_ids:
            requested = list(dict.fromkeys(check_ids))
            unknown = sorted(set(requested) - set(self.manifest.checks))
            if unknown:
                raise ValidationEngineError(f"unknown checks: {unknown}")
            selected = self._dependency_closure(requested)
            reasons = {check_id: ["explicitly requested"] for check_id in selected}
        elif changed_base:
            changed_files = self._changed_files(changed_base)
            selected, reasons, fallback, selection_notes = self._select_changed(
                profile, changed_files
            )
        else:
            selected = self._profile_checks(profile)
            reasons = {check_id: [f"selected by profile {profile}"] for check_id in selected}

        if explain:
            for check_id in selected:
                why = "; ".join(reasons.get(check_id, ["dependency closure"]))
                print(f"{check_id}: {why}")

        results_by_id: dict[str, CheckResult] = {}
        pending = set(selected)
        dependents = self._dependents_map()

        while pending:
            ready = sorted(
                check_id
                for check_id in pending
                if all(dep in results_by_id for dep in self.manifest.checks[check_id].depends_on)
            )
            if not ready:
                unresolved = sorted(pending)
                raise ValidationEngineError(
                    "cannot schedule checks; unresolved dependency closure: " + ", ".join(unresolved)
                )

            runnable: list[str] = []
            for check_id in ready:
                definition = self.manifest.checks[check_id]
                failed_dependencies = [
                    dep for dep in definition.depends_on if not results_by_id[dep].successful
                ]
                if failed_dependencies and not continue_after_failure:
                    results_by_id[check_id] = CheckResult(
                        check_id=check_id,
                        title=definition.title,
                        status="blocked_by_root_failure",
                        summary="blocked by failed dependencies",
                        dependency_failures=failed_dependencies,
                        selected_because=reasons.get(check_id, []),
                    )
                else:
                    runnable.append(check_id)
                pending.remove(check_id)

            with ThreadPoolExecutor(max_workers=min(self.jobs, max(1, len(runnable)))) as pool:
                futures = {
                    pool.submit(
                        self._run_one,
                        self.manifest.checks[check_id],
                        reasons.get(check_id, []),
                        {
                            dependency: {
                                "status": results_by_id[dependency].status,
                                "cache_key": results_by_id[dependency].cache_key,
                                "input_hashes": results_by_id[dependency].input_hashes,
                            }
                            for dependency in self.manifest.checks[check_id].depends_on
                        },
                    ): check_id
                    for check_id in runnable
                }
                for future in as_completed(futures):
                    check_id = futures[future]
                    try:
                        results_by_id[check_id] = future.result()
                    except Exception as exc:
                        definition = self.manifest.checks[check_id]
                        results_by_id[check_id] = CheckResult(
                            check_id=check_id,
                            title=definition.title,
                            status="infrastructure_error",
                            failure_code="FAR-VAL-ENGINE-001",
                            summary=f"validation engine exception: {exc}",
                            selected_because=reasons.get(check_id, []),
                        )

            if not continue_after_failure:
                newly_failed = [
                    check_id for check_id in runnable if not results_by_id[check_id].successful
                ]
                for failed in newly_failed:
                    for dependent in dependents.get(failed, ()):
                        if dependent in pending:
                            reasons.setdefault(dependent, []).append(
                                f"depends on failed check {failed}"
                            )

        ordered_results = [results_by_id[check_id] for check_id in selected]
        finished_at = _utc_now()
        summary = RunSummary(
            run_id=f"{int(time.time())}-{uuid.uuid4().hex[:8]}",
            profile=profile,
            selected_checks=selected,
            results=ordered_results,
            repository_root=str(self.root),
            commit_sha=_git(self.root, "rev-parse", "HEAD"),
            tree_sha=_git(self.root, "rev-parse", "HEAD^{tree}"),
            base_sha=_git(self.root, "merge-base", "HEAD", changed_base) if changed_base else "unknown",
            manifest_hash=self.manifest.manifest_hash,
            started_at=started_at,
            finished_at=finished_at,
            duration_ms=int((time.monotonic() - start) * 1000),
            changed_files=changed_files,
            selection_fallback_to_full=fallback,
            selection_notes=selection_notes,
            environment=self._environment(),
        )
        self._write_run(summary)
        self._write_failure_bundles(summary)
        return summary

    def _profile_checks(self, profile: str) -> list[str]:
        if profile not in self.manifest.profiles:
            raise ValidationEngineError(
                f"unknown profile {profile!r}; available={sorted(self.manifest.profiles)}"
            )
        return self._dependency_closure(self.manifest.profiles[profile])

    def _dependency_closure(self, check_ids: Iterable[str]) -> list[str]:
        included: set[str] = set()

        def include(check_id: str) -> None:
            if check_id in included:
                return
            for dependency in self.manifest.checks[check_id].depends_on:
                include(dependency)
            included.add(check_id)

        for check_id in check_ids:
            include(check_id)
        return self._topological_order(included)

    def _topological_order(self, check_ids: set[str]) -> list[str]:
        ordered: list[str] = []
        temporary: set[str] = set()
        permanent: set[str] = set()

        def visit(check_id: str) -> None:
            if check_id in permanent or check_id not in check_ids:
                return
            if check_id in temporary:
                raise ValidationEngineError(f"dependency cycle at {check_id}")
            temporary.add(check_id)
            for dependency in self.manifest.checks[check_id].depends_on:
                visit(dependency)
            temporary.remove(check_id)
            permanent.add(check_id)
            ordered.append(check_id)

        for check_id in self.manifest.checks:
            visit(check_id)
        return ordered

    def _dependents_map(self) -> dict[str, set[str]]:
        result: dict[str, set[str]] = {check_id: set() for check_id in self.manifest.checks}
        for check in self.manifest.checks.values():
            for dependency in check.depends_on:
                result[dependency].add(check.check_id)
        return result

    def _changed_files(self, base: str) -> list[str]:
        commands = [
            ["git", "diff", "--name-only", f"{base}...HEAD"],
            ["git", "diff", "--name-only"],
            ["git", "diff", "--name-only", "--cached"],
            ["git", "ls-files", "--others", "--exclude-standard"],
        ]
        changed: set[str] = set()
        for index, command in enumerate(commands):
            completed = subprocess.run(
                command,
                cwd=self.root,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False,
            )
            if completed.returncode != 0:
                if index == 0:
                    raise ValidationEngineError(
                        f"cannot determine changed files against {base}: {completed.stderr.strip()}"
                    )
                continue
            changed.update(line.strip() for line in completed.stdout.splitlines() if line.strip())
        return sorted(changed)

    def _select_changed(
        self, profile: str, changed_files: list[str]
    ) -> tuple[list[str], dict[str, list[str]], bool, list[str]]:
        profile_checks = set(self._profile_checks(profile))
        reasons: dict[str, list[str]] = {}
        notes: list[str] = []
        if not changed_files:
            checks = self._dependency_closure(["bootstrap.manifest"])
            return checks, {item: ["no changed files; bootstrap only"] for item in checks}, False, notes

        if any(_matches(path, self.manifest.global_invalidation_paths) for path in changed_files):
            checks = self._profile_checks(profile)
            for check_id in checks:
                reasons[check_id] = ["global invalidation path changed"]
            return checks, reasons, False, notes

        direct: set[str] = set()
        uncovered: list[str] = []
        for path in changed_files:
            matched = [
                check_id
                for check_id in profile_checks
                if _matches(path, self.manifest.checks[check_id].inputs)
            ]
            if not matched:
                uncovered.append(path)
            for check_id in matched:
                direct.add(check_id)
                reasons.setdefault(check_id, []).append(f"input changed: {path}")

        if uncovered:
            notes.append(
                "selection completeness could not prove coverage for: " + ", ".join(uncovered)
            )
            notes.append("falling back to full requested profile")
            checks = self._profile_checks(profile)
            for check_id in checks:
                reasons.setdefault(check_id, []).append("full fallback after incomplete coverage")
            return checks, reasons, True, notes

        expanded = set(self._dependency_closure(direct))
        dependents = self._dependents_map()
        queue = list(direct)
        while queue:
            current = queue.pop()
            for dependent in dependents.get(current, ()):
                if dependent in profile_checks and dependent not in expanded:
                    expanded.add(dependent)
                    reasons.setdefault(dependent, []).append(f"affected by {current}")
                    queue.append(dependent)
        return self._topological_order(expanded), reasons, False, notes

    def _input_hashes(self, definition: CheckDefinition) -> dict[str, str]:
        hashes: dict[str, str] = {}
        for path in _iter_input_files(self.root, definition.inputs):
            hashes[_safe_relative(path, self.root)] = _sha256_file(path)
        return hashes

    def _engine_hash(self) -> str:
        digest = hashlib.sha256()
        paths = list((self.root / "far_validation").rglob("*.py"))
        paths.extend((self.root / "validation_bootstrap").rglob("*.py"))
        for path in sorted((item for item in paths if item.is_file()), key=lambda item: item.as_posix()):
            digest.update(path.relative_to(self.root).as_posix().encode("utf-8"))
            digest.update(path.read_bytes())
        return digest.hexdigest()

    def _cache_key(
        self,
        definition: CheckDefinition,
        input_hashes: dict[str, str],
        dependency_fingerprints: dict[str, object],
    ) -> str:
        payload = {
            "engine_version": ENGINE_VERSION,
            "engine_hash": self._engine_hash(),
            "python": platform.python_version(),
            "manifest_hash": self.manifest.manifest_hash,
            "check": {
                "id": definition.check_id,
                "command": definition.command,
                "builtin": definition.builtin,
                "timeout": definition.timeout_seconds,
                "sandbox_copy": definition.sandbox_copy,
                "expect_no_changes": definition.expect_no_changes,
            },
            "inputs": input_hashes,
            "dependencies": dependency_fingerprints,
        }
        return _sha256_bytes(json.dumps(payload, sort_keys=True).encode("utf-8"))

    def _run_one(
        self,
        definition: CheckDefinition,
        reasons: list[str],
        dependency_fingerprints: dict[str, object],
    ) -> CheckResult:
        input_hashes = self._input_hashes(definition)
        cache_key = self._cache_key(definition, input_hashes, dependency_fingerprints)
        cache_path = self.cache_dir / f"{definition.check_id.replace('/', '_')}-{cache_key}.json"
        if self.use_cache and definition.cacheable and cache_path.is_file():
            payload = json.loads(cache_path.read_text(encoding="utf-8"))
            result = CheckResult(**payload)
            result.cache_hit = True
            result.selected_because = reasons
            return result

        started = time.monotonic()
        if definition.builtin:
            result = self._run_builtin(definition)
        else:
            result = self._run_command(definition)
        result.duration_ms = int((time.monotonic() - started) * 1000)
        result.input_hashes = input_hashes
        result.cache_key = cache_key
        result.selected_because = reasons
        if self.use_cache and definition.cacheable and result.successful:
            cache_path.write_text(json.dumps(result.to_dict(), indent=2, sort_keys=True), encoding="utf-8")
        return result

    def _run_builtin(self, definition: CheckDefinition) -> CheckResult:
        if definition.builtin == "manifest":
            return CheckResult(
                check_id=definition.check_id,
                title=definition.title,
                status="passed",
                summary=(
                    f"manifest schema {self.manifest.schema_version}; "
                    f"{len(self.manifest.checks)} checks; protected checks present"
                ),
            )
        if definition.builtin == "selection_completeness":
            uncovered_checks = [
                check.check_id for check in self.manifest.checks.values() if not check.profiles
            ]
            if uncovered_checks:
                return CheckResult(
                    check_id=definition.check_id,
                    title=definition.title,
                    status="validation_failure",
                    failure_code="FAR-VAL-SELECT-001",
                    summary=f"checks without profiles: {uncovered_checks}",
                )
            return CheckResult(
                check_id=definition.check_id,
                title=definition.title,
                status="passed",
                summary="all checks have profiles and manifest dependency closure is valid",
            )
        if definition.builtin == "doctor":
            requirements = [self.root / "requirements.txt", self.root / "tools" / "run_tests.py"]
            missing = [str(path.relative_to(self.root)) for path in requirements if not path.exists()]
            if missing:
                return CheckResult(
                    check_id=definition.check_id,
                    title=definition.title,
                    status="infrastructure_error",
                    failure_code="FAR-VAL-ENV-001",
                    summary=f"required repository files missing: {missing}",
                )
            return CheckResult(
                check_id=definition.check_id,
                title=definition.title,
                status="passed",
                summary=f"Python {platform.python_version()} on {platform.platform()}",
            )
        raise ValidationEngineError(f"unknown builtin validator: {definition.builtin}")

    def _run_command(self, definition: CheckDefinition) -> CheckResult:
        command = list(definition.command)
        cwd = self.root
        temporary: tempfile.TemporaryDirectory[str] | None = None
        before: dict[str, str] = {}
        try:
            if definition.sandbox_copy:
                temporary = tempfile.TemporaryDirectory(prefix="far-validation-")
                sandbox = Path(temporary.name) / "repo"
                shutil.copytree(
                    self.root,
                    sandbox,
                    ignore=shutil.ignore_patterns(".git", ".far", "__pycache__", "*.pyc"),
                )
                cwd = sandbox
                before = _snapshot_files(sandbox)
            completed = subprocess.run(
                command,
                cwd=cwd,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=definition.timeout_seconds,
                check=False,
                env=self._subprocess_environment(),
            )
            changed_files: list[str] = []
            drift_summary = ""
            if definition.expect_no_changes:
                after = _snapshot_files(cwd)
                changed_files = sorted(
                    path for path in set(before) | set(after) if before.get(path) != after.get(path)
                )
                if changed_files:
                    drift_summary = f"; generated drift in {len(changed_files)} file(s)"
            successful = completed.returncode == 0 and not changed_files
            return CheckResult(
                check_id=definition.check_id,
                title=definition.title,
                status="passed" if successful else "validation_failure",
                failure_code=None if successful else definition.failure_code,
                summary=(
                    f"command exited {completed.returncode}{drift_summary}"
                    if not successful
                    else "command completed successfully"
                ),
                command=command,
                stdout=completed.stdout,
                stderr=completed.stderr,
                changed_files=changed_files,
            )
        except subprocess.TimeoutExpired as exc:
            return CheckResult(
                check_id=definition.check_id,
                title=definition.title,
                status="timed_out",
                failure_code="FAR-VAL-TIMEOUT-001",
                summary=f"timed out after {definition.timeout_seconds}s",
                command=command,
                stdout=exc.stdout or "",
                stderr=exc.stderr or "",
            )
        except OSError as exc:
            return CheckResult(
                check_id=definition.check_id,
                title=definition.title,
                status="infrastructure_error",
                failure_code="FAR-VAL-ENV-001",
                summary=f"cannot execute command: {exc}",
                command=command,
            )
        finally:
            if temporary is not None:
                temporary.cleanup()

    def _subprocess_environment(self) -> dict[str, str]:
        allowed = {
            "PATH",
            "HOME",
            "USERPROFILE",
            "SYSTEMROOT",
            "WINDIR",
            "TMP",
            "TEMP",
            "TMPDIR",
            "CI",
            "GITHUB_ACTIONS",
            "GITHUB_SHA",
            "GITHUB_BASE_REF",
            "GITHUB_HEAD_REF",
        }
        env = {key: value for key, value in os.environ.items() if key in allowed}
        env.update(
            {
                "PYTHONHASHSEED": "0",
                "PYTHONDONTWRITEBYTECODE": "1",
                "TZ": "UTC",
                "LC_ALL": os.environ.get("LC_ALL", "C.UTF-8"),
                "LANG": os.environ.get("LANG", "C.UTF-8"),
            }
        )
        return env

    def _environment(self) -> dict[str, str]:
        return {
            "engine_version": ENGINE_VERSION,
            "python": platform.python_version(),
            "platform": platform.platform(),
            "machine": platform.machine(),
            "github_sha": os.environ.get("GITHUB_SHA", ""),
            "github_base_ref": os.environ.get("GITHUB_BASE_REF", ""),
            "github_head_ref": os.environ.get("GITHUB_HEAD_REF", ""),
        }

    def _write_run(self, summary: RunSummary) -> None:
        payload = summary.to_dict()
        run_path = self.runs_dir / f"{summary.run_id}.json"
        run_path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
        latest = self.runs_dir / "latest.json"
        latest.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
        certificate_dir = self.far_dir / "artifacts" / "validation"
        certificate_dir.mkdir(parents=True, exist_ok=True)
        certificate = certificate_dir / "certificate.json"
        certificate.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")

    def _write_failure_bundles(self, summary: RunSummary) -> None:
        for result in summary.results:
            if result.successful or result.status in {"blocked", "blocked_by_root_failure"}:
                continue
            failure_id = result.failure_code or "FAR-VAL-UNKNOWN-001"
            bundle = self.failures_dir / f"{failure_id}-{result.check_id.replace('.', '_')}"
            bundle.mkdir(parents=True, exist_ok=True)
            (bundle / "summary.json").write_text(
                json.dumps(result.to_dict(), indent=2, sort_keys=True), encoding="utf-8"
            )
            (bundle / "stdout.log").write_text(result.stdout[-500_000:], encoding="utf-8")
            (bundle / "stderr.log").write_text(result.stderr[-500_000:], encoding="utf-8")
            reproduce = [sys.executable, "-m", "far_validation", "validate", result.check_id, "--no-cache"]
            (bundle / "reproduction-command.txt").write_text(
                " ".join(reproduce) + "\n", encoding="utf-8"
            )
            summary_text = (
                f"{failure_id} — {result.title}\n\n"
                f"Check: {result.check_id}\n"
                f"Status: {result.status}\n"
                f"Summary: {result.summary}\n"
                f"Reproduce: {' '.join(reproduce)}\n"
            )
            (bundle / "summary.md").write_text(summary_text, encoding="utf-8")


def format_text(summary: RunSummary) -> str:
    lines = [
        f"Project FAR validation profile: {summary.profile}",
        f"Commit: {summary.commit_sha}",
        f"Checks: {len(summary.results)}",
    ]
    for result in summary.results:
        marker = "PASS" if result.successful else (
            "BLOCK" if result.status in {"blocked", "blocked_by_root_failure"} else "FAIL"
        )
        cache = " [cache]" if result.cache_hit else ""
        lines.append(
            f"[{marker}] {result.check_id}{cache} ({result.duration_ms} ms) — "
            f"{result.summary or result.status}"
        )
        if not result.successful and result.failure_code:
            lines.append(f"       {result.failure_code}")
            if result.command:
                lines.append(f"       reproduce: {' '.join(result.command)}")
            if result.changed_files:
                lines.append(f"       changed: {', '.join(result.changed_files[:20])}")
    if summary.selection_notes:
        lines.append("Selection notes:")
        lines.extend(f"  - {note}" for note in summary.selection_notes)
    lines.append(
        f"Result: {'SUCCESS' if summary.successful else 'FAILED'} in {summary.duration_ms} ms"
    )
    return "\n".join(lines)
