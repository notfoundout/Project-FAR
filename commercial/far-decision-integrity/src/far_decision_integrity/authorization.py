from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from .adjudicate import Adjudication, adjudicate
from .model import IntegrityStatus, PackageValidationError
from .refund import RefundRequest, build_refund_package
from .report import report_payload

DISPOSITIONS = {
    IntegrityStatus.JUSTIFIED: "allow",
    IntegrityStatus.UNSUPPORTED: "block",
    IntegrityStatus.UNDERDETERMINED: "escalate",
    IntegrityStatus.UNVERIFIABLE: "escalate",
}
EXIT_CODES = {"allow": 0, "block": 30, "escalate": 31}


@dataclass(frozen=True, slots=True)
class AuthorizationResult:
    disposition: str
    adjudication: Adjudication
    evidence_directory: Path


def load_refund_request(path: str | Path) -> RefundRequest:
    source = Path(path)
    try:
        payload = json.loads(source.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise PackageValidationError(f"unable to load refund request {source}: {exc}") from exc
    if not isinstance(payload, dict):
        raise PackageValidationError("refund request must be a JSON object")
    required = ("request_id", "order_id", "amount")
    missing = [key for key in required if key not in payload]
    if missing:
        raise PackageValidationError(f"refund request is missing required fields: {missing}")
    try:
        amount = float(payload["amount"])
    except (TypeError, ValueError) as exc:
        raise PackageValidationError("amount must be numeric") from exc
    if amount < 0:
        raise PackageValidationError("amount must be non-negative")
    return RefundRequest(
        request_id=_text(payload["request_id"], "request_id"),
        order_id=_text(payload["order_id"], "order_id"),
        amount=amount,
        order_exists=_optional_bool(payload.get("order_exists"), "order_exists"),
        payment_confirmed=_optional_bool(payload.get("payment_confirmed"), "payment_confirmed"),
        days_since_purchase=_optional_int(payload.get("days_since_purchase"), "days_since_purchase"),
        previous_refund=_optional_bool(payload.get("previous_refund"), "previous_refund"),
        agent_authorized=_optional_bool(payload.get("agent_authorized"), "agent_authorized"),
        policy_version=_text(payload.get("policy_version", "refund-policy/2026-07"), "policy_version"),
        conflicting_delivery_status=_optional_bool(payload.get("conflicting_delivery_status", False), "conflicting_delivery_status") or False,
    )


def authorize_refund(request: RefundRequest, output_directory: str | Path) -> AuthorizationResult:
    package = build_refund_package(request)
    adjudication = adjudicate(package)
    disposition = DISPOSITIONS[adjudication.status]
    output = Path(output_directory)
    output.mkdir(parents=True, exist_ok=True)

    package_payload = _package_payload(package)
    authorization_payload = {
        "decision_id": adjudication.decision_id,
        "integrity_status": adjudication.status.value,
        "disposition": disposition,
        "adjudication": report_payload(adjudication),
    }
    _write_json(output / "decision-package.json", package_payload)
    _write_json(output / "authorization.json", authorization_payload)
    manifest = {
        "schema_version": "far-authorization-evidence/0.1",
        "decision_id": adjudication.decision_id,
        "disposition": disposition,
        "files": {
            name: _sha256(output / name)
            for name in ("decision-package.json", "authorization.json")
        },
    }
    _write_json(output / "manifest.json", manifest)
    return AuthorizationResult(disposition, adjudication, output)


def _package_payload(package: Any) -> dict[str, Any]:
    payload = asdict(package)
    payload["nodes"] = list(payload["nodes"])
    payload["dependencies"] = list(payload["dependencies"])
    payload["authorization_requirements"] = list(payload["authorization_requirements"])
    payload["unknowns"] = list(payload["unknowns"])
    return payload


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _text(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise PackageValidationError(f"{field} must be a non-empty string")
    return value


def _optional_bool(value: Any, field: str) -> bool | None:
    if value is None or isinstance(value, bool):
        return value
    raise PackageValidationError(f"{field} must be boolean or null")


def _optional_int(value: Any, field: str) -> int | None:
    if value is None:
        return None
    if isinstance(value, bool) or not isinstance(value, int):
        raise PackageValidationError(f"{field} must be an integer or null")
    if value < 0:
        raise PackageValidationError(f"{field} must be non-negative")
    return value
