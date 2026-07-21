from __future__ import annotations

from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Literal

CheckStatus = Literal[
    "not_started", "running", "passed", "terminal_positive_result", "terminal_negative_result",
    "unresolved", "blocked", "blocked_by_root_failure", "inapplicable", "skipped", "cancelled",
    "timed_out", "validation_failure", "infrastructure_error",
]

ACCEPTABLE_TERMINAL_STATUSES: frozenset[str] = frozenset(
    {"passed", "terminal_positive_result", "terminal_negative_result", "unresolved", "inapplicable", "skipped"}
)


@dataclass(frozen=True)
class CheckDefinition:
    check_id: str
    title: str
    command: tuple[str, ...] = ()
    builtin: str | None = None
    track: str = "repository"
    category: str = "validation"
    severity: str = "required"
    profiles: tuple[str, ...] = ()
    depends_on: tuple[str, ...] = ()
    inputs: tuple[str, ...] = ()
    outputs: tuple[str, ...] = ()
    timeout_seconds: int = 300
    cacheable: bool = True
    deterministic: bool = True
    sandbox_copy: bool = False
    expect_no_changes: bool = False
    trace_dependencies: bool = True
    allow_network: bool = False
    protected: bool = False
    failure_code: str = "FAR-VAL-TEST-001"
    description: str = ""


@dataclass
class CheckResult:
    check_id: str
    title: str
    status: CheckStatus
    duration_ms: int = 0
    failure_code: str | None = None
    summary: str = ""
    command: list[str] = field(default_factory=list)
    stdout: str = ""
    stderr: str = ""
    dependency_failures: list[str] = field(default_factory=list)
    selected_because: list[str] = field(default_factory=list)
    input_hashes: dict[str, str] = field(default_factory=dict)
    cache_key: str | None = None
    cache_hit: bool = False
    cache_signature_verified: bool = False
    cache_trust_domain: str = ""
    changed_files: list[str] = field(default_factory=list)
    observed_reads: list[str] = field(default_factory=list)
    observed_writes: list[str] = field(default_factory=list)
    observed_executables: list[str] = field(default_factory=list)
    network_attempts: list[str] = field(default_factory=list)
    dependency_violations: list[str] = field(default_factory=list)
    trace_backend: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def successful(self) -> bool:
        return self.status in ACCEPTABLE_TERMINAL_STATUSES

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class Manifest:
    schema_version: str
    profiles: dict[str, tuple[str, ...]]
    protected_checks: tuple[str, ...]
    global_invalidation_paths: tuple[str, ...]
    checks: dict[str, CheckDefinition]
    manifest_path: Path
    manifest_hash: str


@dataclass
class RunSummary:
    run_id: str
    profile: str
    selected_checks: list[str]
    results: list[CheckResult]
    repository_root: str
    commit_sha: str
    tree_sha: str
    base_sha: str
    manifest_hash: str
    started_at: str
    finished_at: str
    duration_ms: int
    changed_files: list[str] = field(default_factory=list)
    selection_fallback_to_full: bool = False
    selection_notes: list[str] = field(default_factory=list)
    environment: dict[str, Any] = field(default_factory=dict)
    assurance: dict[str, Any] = field(default_factory=dict)

    @property
    def successful(self) -> bool:
        required = [result for result in self.results if result.status != "skipped"]
        return bool(required) and all(result.successful for result in required)

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["successful"] = self.successful
        payload["root_failures"] = [
            result.check_id
            for result in self.results
            if result.status in {"validation_failure", "infrastructure_error", "timed_out"}
            and not result.dependency_failures
        ]
        payload["blocked_checks"] = [
            result.check_id for result in self.results if result.status in {"blocked", "blocked_by_root_failure"}
        ]
        payload["trace_violations"] = {
            result.check_id: result.dependency_violations
            for result in self.results
            if result.dependency_violations
        }
        payload["signed_cache_hits"] = [
            result.check_id for result in self.results if result.cache_hit and result.cache_signature_verified
        ]
        return payload
