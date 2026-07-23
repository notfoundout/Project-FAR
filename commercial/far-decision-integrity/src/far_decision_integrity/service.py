from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

from .adjudicate import adjudicate
from .authorization import DISPOSITIONS
from .model import DecisionPackage, PackageValidationError
from .report import report_payload
from .trace import TraceIngestionError, ingest_trace

SERVICE_SCHEMA_VERSION = "far-authorization-service/0.1"
EVIDENCE_SCHEMA_VERSION = "far-authorization-evidence/0.2"
MAX_REQUEST_BYTES = 1_048_576


class ServiceRequestError(ValueError):
    """Raised when an authorization-service request is invalid."""


@dataclass(frozen=True, slots=True)
class ServiceResult:
    status_code: int
    payload: dict[str, Any]


def authorize_payload(request: dict[str, Any], evidence_root: str | Path) -> ServiceResult:
    if not isinstance(request, dict):
        raise ServiceRequestError("request body must be a JSON object")
    input_type = request.get("input_type")
    payload = request.get("payload")
    if input_type not in {"decision_package", "trace"}:
        raise ServiceRequestError("input_type must be 'decision_package' or 'trace'")
    if not isinstance(payload, dict):
        raise ServiceRequestError("payload must be a JSON object")

    try:
        package = (
            DecisionPackage.from_dict(payload)
            if input_type == "decision_package"
            else ingest_trace(payload)
        )
    except (PackageValidationError, TraceIngestionError) as exc:
        raise ServiceRequestError(str(exc)) from exc

    adjudication = adjudicate(package)
    disposition = DISPOSITIONS[adjudication.status]
    evidence_id = _evidence_id(input_type, payload, package.decision_id)
    evidence_directory = Path(evidence_root) / evidence_id
    evidence_directory.mkdir(parents=True, exist_ok=False)

    package_data = _package_payload(package)
    authorization_data = {
        "schema_version": SERVICE_SCHEMA_VERSION,
        "decision_id": package.decision_id,
        "integrity_status": adjudication.status.value,
        "disposition": disposition,
        "adjudication": report_payload(adjudication),
    }
    _write_json(evidence_directory / "decision-package.json", package_data)
    _write_json(evidence_directory / "authorization.json", authorization_data)
    manifest = {
        "schema_version": EVIDENCE_SCHEMA_VERSION,
        "evidence_id": evidence_id,
        "decision_id": package.decision_id,
        "input_type": input_type,
        "disposition": disposition,
        "files": {
            name: _sha256(evidence_directory / name)
            for name in ("decision-package.json", "authorization.json")
        },
    }
    _write_json(evidence_directory / "manifest.json", manifest)

    return ServiceResult(
        HTTPStatus.OK,
        {
            "schema_version": SERVICE_SCHEMA_VERSION,
            "decision_id": package.decision_id,
            "integrity_status": adjudication.status.value,
            "disposition": disposition,
            "evidence_id": evidence_id,
            "evidence": {
                "manifest": f"{evidence_id}/manifest.json",
                "authorization": f"{evidence_id}/authorization.json",
                "decision_package": f"{evidence_id}/decision-package.json",
            },
        },
    )


def make_handler(evidence_root: str | Path) -> type[BaseHTTPRequestHandler]:
    root = Path(evidence_root)

    class AuthorizationHandler(BaseHTTPRequestHandler):
        server_version = "FARAuthorizationService/0.1"

        def do_GET(self) -> None:  # noqa: N802
            if self.path == "/healthz":
                self._send(HTTPStatus.OK, {"status": "ok", "schema_version": SERVICE_SCHEMA_VERSION})
                return
            self._send(HTTPStatus.NOT_FOUND, {"error": "not_found"})

        def do_POST(self) -> None:  # noqa: N802
            if self.path != "/v1/authorize":
                self._send(HTTPStatus.NOT_FOUND, {"error": "not_found"})
                return
            try:
                length = int(self.headers.get("Content-Length", "0"))
                if length <= 0 or length > MAX_REQUEST_BYTES:
                    raise ServiceRequestError(
                        f"Content-Length must be between 1 and {MAX_REQUEST_BYTES} bytes"
                    )
                raw = self.rfile.read(length)
                request = json.loads(raw.decode("utf-8"))
                result = authorize_payload(request, root)
            except (UnicodeDecodeError, json.JSONDecodeError, ServiceRequestError, FileExistsError) as exc:
                self._send(HTTPStatus.BAD_REQUEST, {"error": "invalid_request", "detail": str(exc)})
                return
            self._send(result.status_code, result.payload)

        def log_message(self, format: str, *args: Any) -> None:
            return

        def _send(self, status: int, payload: dict[str, Any]) -> None:
            body = (json.dumps(payload, sort_keys=True) + "\n").encode("utf-8")
            self.send_response(status)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

    return AuthorizationHandler


def serve(host: str, port: int, evidence_root: str | Path) -> None:
    root = Path(evidence_root)
    root.mkdir(parents=True, exist_ok=True)
    server = ThreadingHTTPServer((host, port), make_handler(root))
    server.serve_forever()


def _evidence_id(input_type: str, payload: dict[str, Any], decision_id: str) -> str:
    canonical = json.dumps(
        {"input_type": input_type, "payload": payload},
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    digest = hashlib.sha256(canonical).hexdigest()[:20]
    safe_decision = "".join(character if character.isalnum() or character in "-_" else "-" for character in decision_id)
    return f"{safe_decision}-{digest}"


def _package_payload(package: DecisionPackage) -> dict[str, Any]:
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
