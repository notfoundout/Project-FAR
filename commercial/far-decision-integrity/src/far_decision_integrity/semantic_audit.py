from __future__ import annotations

import hashlib
import importlib
import os
import sys
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any, Callable

_SUPPORTED_FORMATS = {
    "far-ir/2.0": ("contract_v2", "schemas/far-contract-v2.schema.json"),
    "far-ir/2.1": ("contract_v21", "schemas/far-contract-v2.1.schema.json"),
}


class SemanticDisposition(str, Enum):
    PRESERVES = "preserves"
    MATERIAL_LOSS = "material_loss"
    UNKNOWN = "unknown"
    INVALID = "invalid"
    UNAVAILABLE = "unavailable"


@dataclass(frozen=True, slots=True)
class SemanticDiagnostic:
    code: str
    message: str
    path: tuple[object, ...] = ()


@dataclass(frozen=True, slots=True)
class SemanticArtifact:
    role: str
    path: str
    sha256: str


@dataclass(frozen=True, slots=True)
class SemanticAudit:
    document_id: str | None
    contract_id: str | None
    format_version: str | None
    outcome: str | None
    disposition: SemanticDisposition
    verifier_success: bool
    diagnostics: tuple[SemanticDiagnostic, ...]
    verifier_artifacts: tuple[SemanticArtifact, ...] = ()


@dataclass(frozen=True, slots=True)
class _ValidatorBundle:
    validate: Callable[[object], Any]
    artifacts: tuple[SemanticArtifact, ...]


class SemanticVerifierUnavailable(RuntimeError):
    """Raised when the canonical FAR semantic verifier cannot be loaded exactly."""


def audit_semantic_contract(document: object) -> SemanticAudit:
    """Validate one embedded FAR IR contract using the canonical repository verifier.

    The commercial product deliberately delegates semantic truth to the governed
    FAR IR verifier instead of reimplementing factorization, collision, quotient,
    or approximation/cost semantics. Failure to locate or execute that verifier
    is therefore an explicit UNAVAILABLE result, never a successful audit.
    """

    if not isinstance(document, dict):
        return _result(
            document,
            disposition=SemanticDisposition.INVALID,
            verifier_success=False,
            diagnostics=(
                SemanticDiagnostic(
                    "SEMANTIC_CONTRACT_NOT_OBJECT",
                    "Embedded semantic contract must be a JSON object.",
                ),
            ),
        )

    format_version = document.get("format_version")
    if not isinstance(format_version, str) or format_version not in _SUPPORTED_FORMATS:
        return _result(
            document,
            disposition=SemanticDisposition.INVALID,
            verifier_success=False,
            diagnostics=(
                SemanticDiagnostic(
                    "SEMANTIC_CONTRACT_FORMAT_UNSUPPORTED",
                    f"Unsupported semantic contract format {format_version!r}; "
                    f"expected one of {sorted(_SUPPORTED_FORMATS)}.",
                    ("format_version",),
                ),
            ),
        )

    try:
        bundle = _load_validator(format_version)
    except SemanticVerifierUnavailable as exc:
        return _result(
            document,
            disposition=SemanticDisposition.UNAVAILABLE,
            verifier_success=False,
            diagnostics=(SemanticDiagnostic("SEMANTIC_VERIFIER_UNAVAILABLE", str(exc)),),
        )

    try:
        validation = bundle.validate(document)
    except Exception as exc:  # fail closed around the governed verifier boundary
        return _result(
            document,
            disposition=SemanticDisposition.UNAVAILABLE,
            verifier_success=False,
            diagnostics=(
                SemanticDiagnostic(
                    "SEMANTIC_VERIFIER_EXECUTION_FAILED",
                    f"Canonical FAR semantic verifier raised {type(exc).__name__}: {exc}",
                ),
            ),
            artifacts=bundle.artifacts,
        )

    if not bool(getattr(validation, "success", False)):
        diagnostics = tuple(
            SemanticDiagnostic(
                str(getattr(item, "code", "SEMANTIC_VERIFIER_DIAGNOSTIC")),
                str(getattr(item, "message", "Canonical verifier rejected the record.")),
                tuple(getattr(item, "path", ()) or ()),
            )
            for item in tuple(getattr(validation, "diagnostics", ()) or ())
        )
        if not diagnostics:
            diagnostics = (
                SemanticDiagnostic(
                    "SEMANTIC_VERIFIER_REJECTED",
                    "Canonical FAR semantic verifier rejected the record without diagnostics.",
                ),
            )
        return _result(
            document,
            disposition=SemanticDisposition.INVALID,
            verifier_success=False,
            diagnostics=diagnostics,
            artifacts=bundle.artifacts,
        )

    report = document.get("report")
    outcome = report.get("outcome") if isinstance(report, dict) else None
    if outcome == "PROVED":
        disposition = SemanticDisposition.PRESERVES
    elif outcome == "REFUTED":
        disposition = SemanticDisposition.MATERIAL_LOSS
    elif outcome == "Unknown":
        disposition = SemanticDisposition.UNKNOWN
    else:
        return _result(
            document,
            disposition=SemanticDisposition.INVALID,
            verifier_success=True,
            diagnostics=(
                SemanticDiagnostic(
                    "SEMANTIC_CONTRACT_OUTCOME_INVALID",
                    f"Canonical verifier accepted a record with unsupported outcome {outcome!r}.",
                    ("report", "outcome"),
                ),
            ),
            artifacts=bundle.artifacts,
        )

    return _result(
        document,
        disposition=disposition,
        verifier_success=True,
        diagnostics=(),
        artifacts=bundle.artifacts,
    )


def _result(
    document: object,
    *,
    disposition: SemanticDisposition,
    verifier_success: bool,
    diagnostics: tuple[SemanticDiagnostic, ...],
    artifacts: tuple[SemanticArtifact, ...] = (),
) -> SemanticAudit:
    payload = document if isinstance(document, dict) else {}
    contract = payload.get("contract")
    report = payload.get("report")
    return SemanticAudit(
        document_id=_optional_text(payload.get("id")),
        contract_id=_optional_text(contract.get("id")) if isinstance(contract, dict) else None,
        format_version=_optional_text(payload.get("format_version")),
        outcome=_optional_text(report.get("outcome")) if isinstance(report, dict) else None,
        disposition=disposition,
        verifier_success=verifier_success,
        diagnostics=diagnostics,
        verifier_artifacts=artifacts,
    )


def _load_validator(format_version: str) -> _ValidatorBundle:
    module_name, schema_rel = _SUPPORTED_FORMATS[format_version]
    for root in _candidate_repo_roots():
        module_path = root / "mechanization" / "far_mechanization" / f"{module_name}.py"
        schema_path = root / schema_rel
        if not module_path.is_file() or not schema_path.is_file():
            continue

        root_text = str(root)
        mechanization_text = str(root / "mechanization")
        if root_text not in sys.path:
            sys.path.insert(0, root_text)
        if mechanization_text not in sys.path:
            sys.path.insert(0, mechanization_text)

        qualified_name = f"far_mechanization.{module_name}"
        try:
            module = importlib.import_module(qualified_name)
        except Exception as exc:
            raise SemanticVerifierUnavailable(
                f"Found canonical FAR repository at {root} but could not import "
                f"{qualified_name}: {type(exc).__name__}: {exc}"
            ) from exc

        loaded_path = Path(getattr(module, "__file__", "")).resolve()
        if loaded_path != module_path.resolve():
            raise SemanticVerifierUnavailable(
                f"Refusing non-canonical verifier {loaded_path}; expected {module_path.resolve()}."
            )
        validate = getattr(module, "validate_contract", None)
        if not callable(validate):
            raise SemanticVerifierUnavailable(
                f"Canonical verifier {module_path} does not export validate_contract()."
            )

        artifacts = [
            _artifact("semantic-verifier", module_path, root),
            _artifact("semantic-schema", schema_path, root),
        ]
        if format_version == "far-ir/2.1":
            shared = root / "mechanization" / "far_mechanization" / "contract_v2.py"
            if not shared.is_file():
                raise SemanticVerifierUnavailable(
                    f"far-ir/2.1 requires shared exact verifier {shared}, which is missing."
                )
            artifacts.append(_artifact("shared-exact-verifier", shared, root))
        return _ValidatorBundle(validate=validate, artifacts=tuple(artifacts))

    locations = ", ".join(str(path) for path in _candidate_repo_roots())
    raise SemanticVerifierUnavailable(
        "Canonical Project FAR semantic verifier was not found. Run from a Project FAR checkout "
        "or set FAR_REPO_ROOT to its repository root. Searched: " + locations
    )


def _candidate_repo_roots() -> tuple[Path, ...]:
    candidates: list[Path] = []
    env_root = os.environ.get("FAR_REPO_ROOT")
    if env_root:
        candidates.append(Path(env_root).expanduser().resolve())

    source = Path(__file__).resolve()
    # In a source checkout: <repo>/commercial/far-decision-integrity/src/package/file.py
    if len(source.parents) > 4:
        candidates.append(source.parents[4])

    cwd = Path.cwd().resolve()
    candidates.append(cwd)
    candidates.extend(cwd.parents)

    unique: list[Path] = []
    seen: set[str] = set()
    for candidate in candidates:
        key = str(candidate)
        if key not in seen:
            seen.add(key)
            unique.append(candidate)
    return tuple(unique)


def _artifact(role: str, path: Path, root: Path) -> SemanticArtifact:
    try:
        display = str(path.resolve().relative_to(root.resolve()))
    except ValueError:
        display = str(path.resolve())
    return SemanticArtifact(role=role, path=display, sha256=_sha256(path))


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _optional_text(value: object) -> str | None:
    return value if isinstance(value, str) and value else None
