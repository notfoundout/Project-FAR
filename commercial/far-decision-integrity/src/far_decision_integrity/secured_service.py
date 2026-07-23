from __future__ import annotations

import json
import shutil
from dataclasses import dataclass
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlparse

from .store import EvidenceStore, EvidenceStoreError, record_payload
from .security import Principal, SecurityError, TenantSecurityStore, tenant_evidence_id
from .service import MAX_REQUEST_BYTES, ServiceRequestError, authorize_payload

SECURED_SERVICE_SCHEMA_VERSION = "far-secured-authorization-service/0.1"


@dataclass(frozen=True, slots=True)
class SecuredRuntime:
    security: TenantSecurityStore
    evidence: EvidenceStore
    staging_root: Path

    def authenticate(self, authorization: str | None, scope: str) -> Principal:
        if not authorization or not authorization.startswith("Bearer "):
            raise SecurityError("Authorization must use Bearer token")
        principal = self.security.authenticate(authorization[7:].strip())
        principal.require(scope)
        return principal

    def authorize(self, principal: Principal, request: dict[str, Any]) -> dict[str, Any]:
        principal.require("authorize")
        policy_id = request.get("policy_id")
        policy_version = request.get("policy_version")
        if not isinstance(policy_id, str) or not policy_id.strip():
            raise ServiceRequestError("policy_id must be a non-empty string")
        policy_principal = Principal(principal.tenant_id, principal.key_id, tuple(sorted(set(principal.scopes) | {"policy:read"})))
        policy = self.security.resolve_policy(policy_principal, policy_id, policy_version)
        service_request = {"input_type": request.get("input_type"), "payload": request.get("payload")}
        tenant_staging = self.staging_root / principal.tenant_id
        result = authorize_payload(service_request, tenant_staging)
        raw_evidence_id = result.payload["evidence_id"]
        secured_id = tenant_evidence_id(principal.tenant_id, raw_evidence_id)
        raw_directory = tenant_staging / raw_evidence_id
        secured_directory = tenant_staging / secured_id
        if secured_directory.exists():
            shutil.rmtree(raw_directory, ignore_errors=True)
        else:
            raw_directory.replace(secured_directory)
        manifest_path = secured_directory / "manifest.json"
        authorization_path = secured_directory / "authorization.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        authorization = json.loads(authorization_path.read_text(encoding="utf-8"))
        authorization.update({"tenant_id": principal.tenant_id, "policy": {"policy_id": policy.policy_id, "version": policy.version, "sha256": policy.sha256}})
        _write_json(authorization_path, authorization)
        manifest.update({"evidence_id": secured_id, "tenant_id": principal.tenant_id, "policy_id": policy.policy_id, "policy_version": policy.version, "policy_sha256": policy.sha256})
        import hashlib
        manifest["files"]["authorization.json"] = hashlib.sha256(authorization_path.read_bytes()).hexdigest()
        _write_json(manifest_path, manifest)
        self.evidence.put_directory(secured_directory)
        response = dict(result.payload)
        response.update({"schema_version": SECURED_SERVICE_SCHEMA_VERSION, "tenant_id": principal.tenant_id, "evidence_id": secured_id, "policy": {"policy_id": policy.policy_id, "version": policy.version, "sha256": policy.sha256}, "evidence": {"record": f"/v1/evidence/{secured_id}", "manifest": f"/v1/evidence/{secured_id}/manifest"}})
        return response

    def evidence_record(self, principal: Principal, evidence_id: str) -> dict[str, Any]:
        principal.require("evidence:read")
        if not evidence_id.startswith(f"{principal.tenant_id}-"):
            raise EvidenceStoreError("evidence not found for authenticated tenant")
        record = self.evidence.get(evidence_id)
        payload = record_payload(record)
        payload["verification"] = self.evidence.verify(evidence_id)
        return payload

    def evidence_manifest(self, principal: Principal, evidence_id: str) -> dict[str, Any]:
        self.evidence_record(principal, evidence_id)
        try:
            return json.loads((self.evidence.blob_root / evidence_id / "manifest.json").read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise EvidenceStoreError(f"unable to read stored manifest: {exc}") from exc

    def policy(self, principal: Principal, policy_id: str, version: str | None) -> dict[str, Any]:
        record = self.security.resolve_policy(principal, policy_id, version)
        return {"schema_version": SECURED_SERVICE_SCHEMA_VERSION, "tenant_id": record.tenant_id, "policy_id": record.policy_id, "version": record.version, "sha256": record.sha256, "active": record.active, "payload": record.payload}


def make_secured_handler(runtime: SecuredRuntime) -> type[BaseHTTPRequestHandler]:
    class SecuredAuthorizationHandler(BaseHTTPRequestHandler):
        server_version = "FARSecuredAuthorizationService/0.1"
        def do_GET(self) -> None:  # noqa: N802
            parsed = urlparse(self.path)
            if parsed.path == "/healthz":
                self._send(HTTPStatus.OK, {"status": "ok", "schema_version": SECURED_SERVICE_SCHEMA_VERSION}); return
            try:
                if parsed.path.startswith("/v1/evidence/"):
                    principal = runtime.authenticate(self.headers.get("Authorization"), "evidence:read")
                    suffix = parsed.path.removeprefix("/v1/evidence/")
                    payload = runtime.evidence_manifest(principal, suffix.removesuffix("/manifest")) if suffix.endswith("/manifest") else runtime.evidence_record(principal, suffix)
                    self._send(HTTPStatus.OK, payload); return
                if parsed.path.startswith("/v1/policies/"):
                    principal = runtime.authenticate(self.headers.get("Authorization"), "policy:read")
                    policy_id = parsed.path.removeprefix("/v1/policies/")
                    version = parse_qs(parsed.query).get("version", [None])[0]
                    self._send(HTTPStatus.OK, runtime.policy(principal, policy_id, version)); return
            except SecurityError as exc:
                self._send(HTTPStatus.FORBIDDEN, {"error": "forbidden", "detail": str(exc)}); return
            except EvidenceStoreError as exc:
                self._send(HTTPStatus.NOT_FOUND, {"error": "not_found", "detail": str(exc)}); return
            self._send(HTTPStatus.NOT_FOUND, {"error": "not_found"})

        def do_POST(self) -> None:  # noqa: N802
            if self.path != "/v1/authorize":
                self._send(HTTPStatus.NOT_FOUND, {"error": "not_found"}); return
            try:
                principal = runtime.authenticate(self.headers.get("Authorization"), "authorize")
                if self.headers.get("Content-Type", "").split(";", 1)[0] != "application/json":
                    raise ServiceRequestError("Content-Type must be application/json")
                length = int(self.headers.get("Content-Length", "0"))
                if length <= 0 or length > MAX_REQUEST_BYTES:
                    raise ServiceRequestError(f"Content-Length must be between 1 and {MAX_REQUEST_BYTES} bytes")
                payload = runtime.authorize(principal, json.loads(self.rfile.read(length).decode("utf-8")))
            except SecurityError as exc:
                self._send(HTTPStatus.FORBIDDEN, {"error": "forbidden", "detail": str(exc)}); return
            except (UnicodeDecodeError, json.JSONDecodeError, ServiceRequestError, EvidenceStoreError, ValueError) as exc:
                self._send(HTTPStatus.BAD_REQUEST, {"error": "invalid_request", "detail": str(exc)}); return
            self._send(HTTPStatus.OK, payload)

        def log_message(self, format: str, *args: Any) -> None:
            return

        def _send(self, status: int, payload: dict[str, Any]) -> None:
            body = (json.dumps(payload, sort_keys=True) + "\n").encode("utf-8")
            self.send_response(status); self.send_header("Content-Type", "application/json"); self.send_header("Content-Length", str(len(body))); self.end_headers(); self.wfile.write(body)

    return SecuredAuthorizationHandler


def serve_secured(host: str, port: int, runtime: SecuredRuntime) -> None:
    runtime.staging_root.mkdir(parents=True, exist_ok=True)
    ThreadingHTTPServer((host, port), make_secured_handler(runtime)).serve_forever()


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
