from __future__ import annotations

import json
import os
import shutil
import subprocess
import tempfile
import time
from pathlib import Path

from .certificate import write_certificate
from .engine import (
    ENGINE_VERSION as BASE_ENGINE_VERSION,
    ValidationEngine as BaseValidationEngine,
    ValidationEngineError,
    _git,
    _snapshot_files,
)
from .model import CheckDefinition, CheckResult, RunSummary
from .tracing import RuntimePolicy, audit_trace, run_traced
from .trust import HMACTrust, TrustError, read_attestation, write_attestation

ENGINE_VERSION = "0.2.0"


class ValidationEngine(BaseValidationEngine):
    """Hardened validation engine retaining the proven base scheduler."""

    def __init__(
        self,
        root: Path,
        manifest_path: Path | None = None,
        jobs: int | None = None,
        use_cache: bool = True,
        verbose: bool = False,
        trace_dependencies: bool = False,
        require_trace_backend: bool = False,
        require_signed_cache: bool = False,
        trust: HMACTrust | None = None,
    ) -> None:
        super().__init__(root, manifest_path, jobs, use_cache, verbose)
        self.trace_dependencies = trace_dependencies
        self.require_trace_backend = require_trace_backend
        self.require_signed_cache = require_signed_cache
        self.trust = trust or HMACTrust.from_environment(require_signature=require_signed_cache)
        policy_path = self.root / "validation" / "runtime-policy.json"
        self.runtime_policy = RuntimePolicy.load(policy_path) if policy_path.is_file() else RuntimePolicy(
            allow_read_patterns=("tools/**/*.py", "far_validation/**/*.py", "validation_bootstrap/**/*.py"),
            allow_write_patterns=(".far/**", "artifacts/validation/runtime/**"),
            allowed_executables=("python", "python3", "git", "bash", "sh", "make"),
            skip_checks=(),
            deny_network=True,
        )

    def _cache_key(
        self,
        definition: CheckDefinition,
        input_hashes: dict[str, str],
        dependency_fingerprints: dict[str, object],
    ) -> str:
        import hashlib

        base = super()._cache_key(definition, input_hashes, dependency_fingerprints)
        material = {
            "base": base,
            "assurance_engine": ENGINE_VERSION,
            "trace_dependencies": self.trace_dependencies,
            "trace_contract": definition.trace_dependencies,
            "allow_network": definition.allow_network,
            "outputs": definition.outputs,
        }
        return hashlib.sha256(json.dumps(material, sort_keys=True).encode("utf-8")).hexdigest()

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
            try:
                payload = read_attestation(cache_path, trust=self.trust, kind="cache-result")
                if payload.get("cache_key") != cache_key or payload.get("check_id") != definition.check_id:
                    raise TrustError("cache identity mismatch")
                result = CheckResult(**payload["result"])
                result.cache_hit = True
                result.cache_signature_verified = self.trust.signed
                result.cache_trust_domain = self.trust.trust_domain
                result.selected_because = reasons
                return result
            except (TrustError, KeyError, TypeError, ValueError, json.JSONDecodeError):
                cache_path.unlink(missing_ok=True)

        started = time.monotonic()
        result = self._run_builtin(definition) if definition.builtin else self._run_command(definition)
        result.duration_ms = int((time.monotonic() - started) * 1000)
        result.input_hashes = input_hashes
        result.cache_key = cache_key
        result.selected_because = reasons
        result.cache_trust_domain = self.trust.trust_domain
        if self.use_cache and definition.cacheable and result.successful:
            write_attestation(
                cache_path,
                trust=self.trust,
                kind="cache-result",
                payload={"cache_key": cache_key, "check_id": definition.check_id, "result": result.to_dict()},
                metadata={"engine_version": ENGINE_VERSION, "manifest_hash": self.manifest.manifest_hash},
            )
        return result

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
            env = self._subprocess_environment()
            should_trace = (
                self.trace_dependencies
                and definition.trace_dependencies
                and definition.check_id not in self.runtime_policy.skip_checks
            )
            if should_trace:
                completed, trace = run_traced(
                    command, cwd=cwd, repository_root=cwd, env=env, timeout=definition.timeout_seconds
                )
                if self.require_trace_backend and trace.backend == "unavailable":
                    return CheckResult(
                        check_id=definition.check_id,
                        title=definition.title,
                        status="infrastructure_error",
                        failure_code="FAR-VAL-TRACE-001",
                        summary="required runtime dependency trace backend is unavailable",
                        command=command,
                        stdout=completed.stdout,
                        stderr=completed.stderr,
                        trace_backend=trace.backend,
                    )
                policy = self.runtime_policy
                if definition.allow_network:
                    policy = RuntimePolicy(
                        allow_read_patterns=policy.allow_read_patterns,
                        allow_write_patterns=policy.allow_write_patterns,
                        allowed_executables=policy.allowed_executables,
                        skip_checks=policy.skip_checks,
                        deny_network=False,
                    )
                trace = audit_trace(
                    trace,
                    declared_inputs=definition.inputs,
                    declared_outputs=definition.outputs,
                    command=command,
                    policy=policy,
                    sandbox_copy=definition.sandbox_copy,
                )
            else:
                completed = subprocess.run(
                    command,
                    cwd=cwd,
                    text=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    timeout=definition.timeout_seconds,
                    check=False,
                    env=env,
                )
                trace = None
            changed_files: list[str] = []
            drift_summary = ""
            if definition.expect_no_changes:
                after = _snapshot_files(cwd)
                changed_files = sorted(
                    path for path in set(before) | set(after) if before.get(path) != after.get(path)
                )
                if changed_files:
                    drift_summary = f"; generated drift in {len(changed_files)} file(s)"
            dependency_violations = trace.violations if trace is not None else []
            trace_summary = f"; {len(dependency_violations)} dependency violation(s)" if dependency_violations else ""
            successful = completed.returncode == 0 and not changed_files and not dependency_violations
            return CheckResult(
                check_id=definition.check_id,
                title=definition.title,
                status="passed" if successful else "validation_failure",
                failure_code=None if successful else (
                    "FAR-VAL-TRACE-001" if dependency_violations else definition.failure_code
                ),
                summary=(
                    "command completed successfully"
                    if successful
                    else f"command exited {completed.returncode}{drift_summary}{trace_summary}"
                ),
                command=command,
                stdout=completed.stdout,
                stderr=completed.stderr,
                changed_files=changed_files,
                observed_reads=trace.reads if trace is not None else [],
                observed_writes=trace.writes if trace is not None else [],
                observed_executables=trace.executables if trace is not None else [],
                network_attempts=trace.network_attempts if trace is not None else [],
                dependency_violations=dependency_violations,
                trace_backend=trace.backend if trace is not None else "",
                metadata={"trace_raw_tail": trace.raw_trace[-20_000:] if trace is not None else ""},
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
        env = super()._subprocess_environment()
        for key in (
            "GITHUB_EVENT_NAME", "GITHUB_REPOSITORY", "GITHUB_WORKFLOW", "GITHUB_RUN_ID",
            "GITHUB_RUN_ATTEMPT", "FAR_VALIDATION_CACHE_SIGNING_KEY", "FAR_VALIDATION_TRUST_DOMAIN",
            "FAR_VALIDATION_BASE_SHA",
        ):
            if key in os.environ:
                env[key] = os.environ[key]
        return env

    def _environment(self) -> dict[str, str]:
        environment = super()._environment()
        environment.update(
            {
                "engine_version": ENGINE_VERSION,
                "base_engine_version": BASE_ENGINE_VERSION,
                "trust_domain": self.trust.trust_domain,
                "key_id": self.trust.key_id,
                "trace_dependencies": str(self.trace_dependencies),
            }
        )
        return environment

    def _write_run(self, summary: RunSummary) -> None:
        summary.tree_sha = _git(self.root, "rev-parse", "HEAD^{tree}")
        summary.assurance.update(
            {
                "dependency_tracing": self.trace_dependencies,
                "trace_backend_required": self.require_trace_backend,
                "signed_cache_required": self.require_signed_cache,
                "trust_domain": self.trust.trust_domain,
                "key_id": self.trust.key_id,
            }
        )
        payload = summary.to_dict()
        run_path = self.runs_dir / f"{summary.run_id}.json"
        run_path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
        (self.runs_dir / "latest.json").write_text(
            json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8"
        )
        certificate_dir = self.far_dir / "artifacts" / "validation"
        certificate_dir.mkdir(parents=True, exist_ok=True)
        write_certificate(certificate_dir / "certificate.json", payload, trust=self.trust)

    def _write_failure_bundles(self, summary: RunSummary) -> None:
        super()._write_failure_bundles(summary)
        for result in summary.results:
            if not result.metadata.get("trace_raw_tail") or result.successful:
                continue
            failure_id = result.failure_code or "FAR-VAL-UNKNOWN-001"
            bundle = self.failures_dir / f"{failure_id}-{result.check_id.replace('.', '_')}"
            bundle.mkdir(parents=True, exist_ok=True)
            (bundle / "trace.log").write_text(
                str(result.metadata["trace_raw_tail"]), encoding="utf-8"
            )


def format_text(summary: RunSummary) -> str:
    lines = [
        f"Project FAR validation profile: {summary.profile}",
        f"Commit: {summary.commit_sha}",
        f"Tree: {summary.tree_sha}",
        f"Checks: {len(summary.results)}",
    ]
    for result in summary.results:
        marker = "PASS" if result.successful else (
            "BLOCK" if result.status in {"blocked", "blocked_by_root_failure"} else "FAIL"
        )
        cache = " [signed-cache]" if result.cache_hit and result.cache_signature_verified else (
            " [cache]" if result.cache_hit else ""
        )
        trace = f" [trace:{result.trace_backend}]" if result.trace_backend else ""
        lines.append(
            f"[{marker}] {result.check_id}{cache}{trace} ({result.duration_ms} ms) — "
            f"{result.summary or result.status}"
        )
        if not result.successful and result.failure_code:
            lines.append(f"       {result.failure_code}")
            if result.command:
                lines.append(f"       reproduce: {' '.join(result.command)}")
            for violation in result.dependency_violations[:20]:
                lines.append(f"       dependency: {violation}")
    if summary.selection_notes:
        lines.append("Selection notes:")
        lines.extend(f"  - {note}" for note in summary.selection_notes)
    lines.append(f"Result: {'SUCCESS' if summary.successful else 'FAILED'} in {summary.duration_ms} ms")
    return "\n".join(lines)


__all__ = ["ValidationEngine", "ValidationEngineError", "format_text"]
