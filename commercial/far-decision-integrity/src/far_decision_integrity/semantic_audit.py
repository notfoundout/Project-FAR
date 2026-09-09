from __future__ import annotations

import hashlib
import importlib.util
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
_SUPPORTED_PURPOSES = {
    "exact_sufficiency",
    "approximation_candidate",
    "analysis_only",
}


class SemanticDisposition(str, Enum):
    SATISFIES = "satisfies"
    MATERIAL_LOSS = "material_loss"
    OUTSIDE_TOLERANCE = "outside_tolerance"
    VERIFIED_ANALYSIS = "verified_analysis"
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
    binding_id: str | None
    target_node_id: str | None
    purpose: str | None
    selected_candidate_id: str | None
    document_id: str | None
    contract_id: str | None
    format_version: str | None
    outcome: str | None
    disposition: SemanticDisposition
    verifier_success: bool
    diagnostics: tuple[SemanticDiagnostic, ...]
    verifier_artifacts: tuple[SemanticArtifact, ...] = ()

    @property
    def is_gating(self) -> bool:
        return self.purpose in {"exact_sufficiency", "approximation_candidate"}


@dataclass(frozen=True, slots=True)
class _ValidatorBundle:
    validate: Callable[[object], Any]
    artifacts: tuple[SemanticArtifact, ...]


class SemanticVerifierUnavailable(RuntimeError):
    """Raised when the canonical FAR semantic verifier cannot be loaded exactly."""


def audit_semantic_contract(binding: object) -> SemanticAudit:
    """Audit one decision-bound semantic contract with canonical FAR IR machinery."""
    if not isinstance(binding, dict):
        return _binding_result(
            {},
            {},
            disposition=SemanticDisposition.INVALID,
            verifier_success=False,
            diagnostics=(
                SemanticDiagnostic(
                    "SEMANTIC_BINDING_NOT_OBJECT",
                    "semantic_contracts entries must be binding objects.",
                ),
            ),
        )

    binding_id = binding.get("binding_id")
    target_node_id = binding.get("target_node_id")
    purpose = binding.get("purpose")
    selected_candidate_id = binding.get("selected_candidate_id")
    record = binding.get("record")

    errors: list[SemanticDiagnostic] = []
    if not isinstance(binding_id, str) or not binding_id.strip():
        errors.append(
            SemanticDiagnostic(
                "SEMANTIC_BINDING_ID_INVALID",
                "binding_id must be a non-empty string.",
                ("binding_id",),
            )
        )
    if not isinstance(target_node_id, str) or not target_node_id.strip():
        errors.append(
            SemanticDiagnostic(
                "SEMANTIC_BINDING_TARGET_INVALID",
                "target_node_id must be a non-empty string.",
                ("target_node_id",),
            )
        )
    if not isinstance(purpose, str) or purpose not in _SUPPORTED_PURPOSES:
        errors.append(
            SemanticDiagnostic(
                "SEMANTIC_BINDING_PURPOSE_UNSUPPORTED",
                f"purpose must be one of {sorted(_SUPPORTED_PURPOSES)}.",
                ("purpose",),
            )
        )
    if purpose == "approximation_candidate":
        if not isinstance(selected_candidate_id, str) or not selected_candidate_id.strip():
            errors.append(
                SemanticDiagnostic(
                    "SEMANTIC_SELECTED_CANDIDATE_REQUIRED",
                    "approximation_candidate bindings require selected_candidate_id.",
                    ("selected_candidate_id",),
                )
            )
    elif selected_candidate_id is not None:
        errors.append(
            SemanticDiagnostic(
                "SEMANTIC_SELECTED_CANDIDATE_NOT_ALLOWED",
                "selected_candidate_id is only valid for approximation_candidate bindings.",
                ("selected_candidate_id",),
            )
        )
    if not isinstance(record, dict):
        errors.append(
            SemanticDiagnostic(
                "SEMANTIC_RECORD_NOT_OBJECT",
                "record must contain one FAR IR JSON object.",
                ("record",),
            )
        )
    if errors:
        return _binding_result(
            binding,
            record if isinstance(record, dict) else {},
            disposition=SemanticDisposition.INVALID,
            verifier_success=False,
            diagnostics=tuple(errors),
        )

    format_version = record.get("format_version")
    if not isinstance(format_version, str) or format_version not in _SUPPORTED_FORMATS:
        return _binding_result(
            binding,
            record,
            disposition=SemanticDisposition.INVALID,
            verifier_success=False,
            diagnostics=(
                SemanticDiagnostic(
                    "SEMANTIC_CONTRACT_FORMAT_UNSUPPORTED",
                    f"Unsupported semantic contract format {format_version!r}; "
                    f"expected one of {sorted(_SUPPORTED_FORMATS)}.",
                    ("record", "format_version"),
                ),
            ),
        )

    if purpose == "exact_sufficiency" and format_version != "far-ir/2.0":
        return _binding_result(
            binding,
            record,
            disposition=SemanticDisposition.INVALID,
            verifier_success=False,
            diagnostics=(
                SemanticDiagnostic(
                    "SEMANTIC_PURPOSE_FORMAT_MISMATCH",
                    "exact_sufficiency requires a far-ir/2.0 exact semantic record.",
                    ("purpose",),
                ),
            ),
        )
    if purpose == "approximation_candidate" and format_version != "far-ir/2.1":
        return _binding_result(
            binding,
            record,
            disposition=SemanticDisposition.INVALID,
            verifier_success=False,
            diagnostics=(
                SemanticDiagnostic(
                    "SEMANTIC_PURPOSE_FORMAT_MISMATCH",
                    "approximation_candidate requires a far-ir/2.1 approximation/cost record.",
                    ("purpose",),
                ),
            ),
        )

    try:
        bundle = _load_validator(format_version)
    except SemanticVerifierUnavailable as exc:
        return _binding_result(
            binding,
            record,
            disposition=SemanticDisposition.UNAVAILABLE,
            verifier_success=False,
            diagnostics=(SemanticDiagnostic("SEMANTIC_VERIFIER_UNAVAILABLE", str(exc)),),
        )

    try:
        validation = bundle.validate(record)
    except Exception as exc:
        return _binding_result(
            binding,
            record,
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
                ("record",) + tuple(getattr(item, "path", ()) or ()),
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
        return _binding_result(
            binding,
            record,
            disposition=SemanticDisposition.INVALID,
            verifier_success=False,
            diagnostics=diagnostics,
            artifacts=bundle.artifacts,
        )

    report = record.get("report")
    evidence = report.get("evidence") if isinstance(report, dict) else None
    outcome = report.get("outcome") if isinstance(report, dict) else None
    evidence_kind = evidence.get("kind") if isinstance(evidence, dict) else None

    if purpose == "analysis_only":
        return _binding_result(
            binding,
            record,
            disposition=SemanticDisposition.VERIFIED_ANALYSIS,
            verifier_success=True,
            diagnostics=(),
            artifacts=bundle.artifacts,
        )

    if purpose == "exact_sufficiency":
        if outcome == "PROVED" and evidence_kind == "factorization":
            disposition = SemanticDisposition.SATISFIES
        elif outcome == "REFUTED" and evidence_kind == "collision":
            disposition = SemanticDisposition.MATERIAL_LOSS
        elif outcome == "Unknown" and evidence_kind == "unknown":
            disposition = SemanticDisposition.UNKNOWN
        else:
            return _binding_result(
                binding,
                record,
                disposition=SemanticDisposition.INVALID,
                verifier_success=True,
                diagnostics=(
                    SemanticDiagnostic(
                        "SEMANTIC_PURPOSE_EVIDENCE_MISMATCH",
                        "exact_sufficiency accepts only PROVED factorization, REFUTED collision, "
                        "or typed Unknown evidence; a quotient proof is analysis, not a proof that "
                        "the package representation is sufficient.",
                        ("record", "report", "evidence", "kind"),
                    ),
                ),
                artifacts=bundle.artifacts,
            )
        return _binding_result(
            binding,
            record,
            disposition=disposition,
            verifier_success=True,
            diagnostics=(),
            artifacts=bundle.artifacts,
        )

    if outcome != "PROVED" or evidence_kind != "approximation_cost":
        return _binding_result(
            binding,
            record,
            disposition=SemanticDisposition.INVALID,
            verifier_success=True,
            diagnostics=(
                SemanticDiagnostic(
                    "SEMANTIC_PURPOSE_EVIDENCE_MISMATCH",
                    "approximation_candidate requires a PROVED approximation_cost record.",
                    ("record", "report", "evidence", "kind"),
                ),
            ),
            artifacts=bundle.artifacts,
        )

    candidates = evidence.get("candidates") if isinstance(evidence, dict) else None
    candidate_ids = (
        {
            item.get("id")
            for item in candidates
            if isinstance(item, dict) and isinstance(item.get("id"), str)
        }
        if isinstance(candidates, list)
        else set()
    )
    if selected_candidate_id not in candidate_ids:
        return _binding_result(
            binding,
            record,
            disposition=SemanticDisposition.INVALID,
            verifier_success=True,
            diagnostics=(
                SemanticDiagnostic(
                    "SEMANTIC_SELECTED_CANDIDATE_UNKNOWN",
                    f"selected_candidate_id {selected_candidate_id!r} is not a declared candidate.",
                    ("selected_candidate_id",),
                ),
            ),
            artifacts=bundle.artifacts,
        )

    feasible = evidence.get("claimed_feasible") if isinstance(evidence, dict) else None
    feasible_ids = (
        {item for item in feasible if isinstance(item, str)}
        if isinstance(feasible, list)
        else set()
    )
    disposition = (
        SemanticDisposition.SATISFIES
        if selected_candidate_id in feasible_ids
        else SemanticDisposition.OUTSIDE_TOLERANCE
    )
    return _binding_result(
        binding,
        record,
        disposition=disposition,
        verifier_success=True,
        diagnostics=(),
        artifacts=bundle.artifacts,
    )


def _binding_result(
    binding: dict[str, Any],
    record: dict[str, Any],
    *,
    disposition: SemanticDisposition,
    verifier_success: bool,
    diagnostics: tuple[SemanticDiagnostic, ...],
    artifacts: tuple[SemanticArtifact, ...] = (),
) -> SemanticAudit:
    contract = record.get("contract")
    report = record.get("report")
    return SemanticAudit(
        binding_id=_optional_text(binding.get("binding_id")),
        target_node_id=_optional_text(binding.get("target_node_id")),
        purpose=_optional_text(binding.get("purpose")),
        selected_candidate_id=_optional_text(binding.get("selected_candidate_id")),
        document_id=_optional_text(record.get("id")),
        contract_id=_optional_text(contract.get("id")) if isinstance(contract, dict) else None,
        format_version=_optional_text(record.get("format_version")),
        outcome=_optional_text(report.get("outcome")) if isinstance(report, dict) else None,
        disposition=disposition,
        verifier_success=verifier_success,
        diagnostics=diagnostics,
        verifier_artifacts=artifacts,
    )


def _load_validator(format_version: str) -> _ValidatorBundle:
    module_name, schema_rel = _SUPPORTED_FORMATS[format_version]
    searched: list[Path] = []
    for root in _candidate_repo_roots():
        module_path = root / "mechanization" / "far_mechanization" / f"{module_name}.py"
        schema_path = root / schema_rel
        searched.append(root)
        if not module_path.is_file() or not schema_path.is_file():
            continue

        # Load only the governed verifier module. Importing far_mechanization as a
        # package executes its broad convenience __init__ (including YAML parsing),
        # which is unrelated to contract verification and made the bridge depend on
        # optional mechanization dependencies. The contract modules themselves are
        # intentionally self-contained and depend only on stdlib + jsonschema.
        unique_name = (
            f"_far_semantic_{module_name}_"
            f"{hashlib.sha256(str(module_path.resolve()).encode('utf-8')).hexdigest()[:16]}"
        )
        spec = importlib.util.spec_from_file_location(unique_name, module_path)
        if spec is None or spec.loader is None:
            raise SemanticVerifierUnavailable(
                f"Could not create a loader for canonical FAR verifier {module_path}."
            )
        module = importlib.util.module_from_spec(spec)
        sys.modules[unique_name] = module
        try:
            spec.loader.exec_module(module)
        except Exception as exc:
            sys.modules.pop(unique_name, None)
            raise SemanticVerifierUnavailable(
                f"Found canonical FAR repository at {root} but could not load "
                f"{module_path}: {type(exc).__name__}: {exc}"
            ) from exc

        loaded_path = Path(getattr(module, "__file__", "")).resolve()
        if loaded_path != module_path.resolve():
            sys.modules.pop(unique_name, None)
            raise SemanticVerifierUnavailable(
                f"Refusing non-canonical verifier {loaded_path}; expected {module_path.resolve()}."
            )
        validate = getattr(module, "validate_contract", None)
        if not callable(validate):
            sys.modules.pop(unique_name, None)
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

    locations = ", ".join(str(path) for path in searched)
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
