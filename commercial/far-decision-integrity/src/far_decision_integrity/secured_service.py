from __future__ import annotations

import json
import shutil
from dataclasses import dataclass
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any, Protocol
from urllib.parse import parse_qs, urlparse

from .external_identity import ExternalIdentityError, IdentityProvider
from .operations import FixedWindowRateLimiter, OperationsError, OperationsStore, RuntimeMetrics, audit_payload
from .store import EvidenceStore, EvidenceStoreError, record_payload
from .security import Principal, SecurityError, TenantSecurityStore, tenant_evidence_id
from .service import MAX_REQUEST_BYTES, ServiceRequestError, authorize_payload

SECURED_SERVICE_SCHEMA_VERSION = "far-secured-authorization-service/0.3"


class EventExporter(Protocol):
    def emit(self, event_type: str, payload: dict[str, Any], *, occurred_at: int | None = None) -> dict[str, Any]: ...


@dataclass(frozen=True, slots=True)
class SecuredRuntime:
    security: TenantSecurityStore
    evidence: EvidenceStore
    staging_root: Path
    operations: OperationsStore | None = None
    limiter: FixedWindowRateLimiter | None = None
    metrics: RuntimeMetrics | None = None
    identity_provider: IdentityProvider | None = None
    exporters: tuple[EventExporter, ...] = ()

    def authenticate(self, authorization: str | None, scope: str) -> Principal:
        if not authorization or not authorization.startswith("Bearer "):
            self.metric("authentication.failed")
            raise SecurityError("Authorization must use Bearer token")
        token = authorization[7:].strip()
        try:
            principal = self.identity_provider.verify(token).principal() if self.identity_provider else self.security.authenticate(token)
            principal.require(scope)
        except SecurityError:
            self.metric("authentication.failed")
            self.observe("authentication.failed", {"required_scope": scope})
            raise
        self.metric("authentication.succeeded")
        self.observe("authentication.succeeded", {"tenant_id": principal.tenant_id, "subject": principal.key_id, "required_scope": scope})
        return principal

    def enforce_rate_limit(self, principal: Principal) -> None:
        if self.limiter is not None and not self.limiter.allow(f"{principal.tenant_id}:{principal.key_id}"):
            self.metric("requests.rate_limited")
            self.observe("request.rate_limited", {"tenant_id": principal.tenant_id, "subject": principal.key_id})
            raise OperationsError("rate limit exceeded")

    def metric(self, name: str) -> None:
        if self.metrics is not None:
            self.metrics.increment(name)

    def observe(self, event_type: str, payload: dict[str, Any]) -> None:
        for exporter in self.exporters:
            try:
                exporter.emit(event_type, payload)
            except (ExternalIdentityError, OSError, ValueError):
                self.metric("observability.export_failed")

    def authorize(self, principal: Principal, request: dict[str, Any]) -> dict[str, Any]:
        principal.require("authorize")
        policy_id = request.get("policy_id")
        policy_version = request.get("policy_version")
        if not isinstance(policy_id, str) or not policy_id.strip():
            raise ServiceRequestError("policy_id must be a non-empty string")
        policy_principal = Principal(principal.tenant_id, principal.key_id, tuple(sorted(set(principal.scopes) | {"policy:read"})))
        policy = self.security.resolve_policy(policy_principal, policy_id, policy_version)
        result = authorize_payload({"input_type": request.get("input_type"), "payload": request.get("payload")}, self.staging_root / principal.tenant_id)
        raw_id = result.payload["evidence_id"]
        secured_id = tenant_evidence_id(principal.tenant_id, raw_id)
        raw_directory = self.staging_root / principal.tenant_id / raw_id
        secured_directory = self.staging_root / principal.tenant_id / secured_id
        if secured_directory.exists():
            shutil.rmtree(raw_directory, ignore_errors=True)
        else:
            raw_directory.replace(secured_directory)
        manifest_path = secured_directory / "manifest.json"
        authorization_path = secured_directory / "authorization.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        authorization = json.loads(authorization_path.read_text(encoding="utf-8"))
        policy_data = {"policy_id": policy.policy_id, "version": policy.version, "sha256": policy.sha256}
        authorization.update({"tenant_id": principal.tenant_id, "policy": policy_data})
        _write_json(authorization_path, authorization)
        import hashlib
        manifest.update({"evidence_id": secured_id, "tenant_id": principal.tenant_id, **policy_data})
        manifest["files"]["authorization.json"] = hashlib.sha256(authorization_path.read_bytes()).hexdigest()
        _write_json(manifest_path, manifest)
        self.evidence.put_directory(secured_directory)
        disposition = result.payload["disposition"]
        self.metric(f"authorization.{disposition}")
        self.observe("authorization.completed", {"tenant_id": principal.tenant_id, "subject": principal.key_id, "evidence_id": secured_id, "disposition": disposition, **policy_data})
        response = dict(result.payload)
        response.update({"schema_version": SECURED_SERVICE_SCHEMA_VERSION, "tenant_id": principal.tenant_id, "evidence_id": secured_id, "policy": policy_data, "evidence": {"record": f"/v1/evidence/{secured_id}", "manifest": f"/v1/evidence/{secured_id}/manifest"}})
        return response

    def evidence_record(self, principal: Principal, evidence_id: str) -> dict[str, Any]:
        principal.require("evidence:read")
        if not evidence_id.startswith(f"{principal.tenant_id}-"):
            raise EvidenceStoreError("evidence not found for authenticated tenant")
        payload = record_payload(self.evidence.get(evidence_id))
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

    def administer(self, principal: Principal, action: str, request: dict[str, Any]) -> dict[str, Any]:
        if self.operations is None:
            raise OperationsError("operations are not configured")
        if action == "keys/rotate":
            record = self.operations.rotate_key(principal, request.get("old_key_id"), request.get("new_key_id"), request.get("new_secret"), tuple(request.get("scopes", ())))
        elif action == "keys/revoke":
            record = self.operations.revoke_key(principal, request.get("key_id"))
        elif action == "policies/register":
            record = self.operations.register_policy(principal, request.get("policy_id"), request.get("version"), request.get("payload"), activate=bool(request.get("activate", False)))
        elif action == "policies/activate":
            record = self.operations.activate_policy(principal, request.get("policy_id"), request.get("version"))
        else:
            raise OperationsError("unknown administration action")
        self.metric(f"admin.{record.action}")
        self.observe("administration.completed", {"tenant_id": principal.tenant_id, "subject": principal.key_id, "action": record.action, "target": record.target})
        return audit_payload(record)

    def audit(self, principal: Principal, limit: int) -> dict[str, Any]:
        if self.operations is None:
            raise OperationsError("operations are not configured")
        return {"schema_version": SECURED_SERVICE_SCHEMA_VERSION, "records": [audit_payload(record) for record in self.operations.audit_log(principal, limit=limit)]}


def make_secured_handler(runtime: SecuredRuntime) -> type[BaseHTTPRequestHandler]:
    class Handler(BaseHTTPRequestHandler):
        server_version = "FARSecuredAuthorizationService/0.3"
        def do_GET(self) -> None:  # noqa: N802
            parsed = urlparse(self.path)
            if parsed.path == "/healthz":
                self._send(HTTPStatus.OK, {"status": "ok", "schema_version": SECURED_SERVICE_SCHEMA_VERSION}); return
            try:
                if parsed.path == "/metrics":
                    principal = runtime.authenticate(self.headers.get("Authorization"), "metrics:read"); runtime.enforce_rate_limit(principal)
                    self._send(HTTPStatus.OK, runtime.metrics.snapshot() if runtime.metrics else {"schema_version": SECURED_SERVICE_SCHEMA_VERSION, "counters": {}}); return
                if parsed.path == "/v1/admin/audit":
                    principal = runtime.authenticate(self.headers.get("Authorization"), "audit:read"); runtime.enforce_rate_limit(principal)
                    limit = int(parse_qs(parsed.query).get("limit", ["100"])[0]); self._send(HTTPStatus.OK, runtime.audit(principal, limit)); return
                if parsed.path.startswith("/v1/evidence/"):
                    principal = runtime.authenticate(self.headers.get("Authorization"), "evidence:read"); runtime.enforce_rate_limit(principal)
                    suffix = parsed.path.removeprefix("/v1/evidence/")
                    payload = runtime.evidence_manifest(principal, suffix.removesuffix("/manifest")) if suffix.endswith("/manifest") else runtime.evidence_record(principal, suffix)
                    self._send(HTTPStatus.OK, payload); return
                if parsed.path.startswith("/v1/policies/"):
                    principal = runtime.authenticate(self.headers.get("Authorization"), "policy:read"); runtime.enforce_rate_limit(principal)
                    policy_id = parsed.path.removeprefix("/v1/policies/"); version = parse_qs(parsed.query).get("version", [None])[0]
                    self._send(HTTPStatus.OK, runtime.policy(principal, policy_id, version)); return
            except OperationsError as exc:
                self._send(HTTPStatus.TOO_MANY_REQUESTS if "rate limit" in str(exc) else HTTPStatus.BAD_REQUEST, {"error": "operations_error", "detail": str(exc)}); return
            except SecurityError as exc:
                self._send(HTTPStatus.FORBIDDEN, {"error": "forbidden", "detail": str(exc)}); return
            except EvidenceStoreError as exc:
                self._send(HTTPStatus.NOT_FOUND, {"error": "not_found", "detail": str(exc)}); return
            except ValueError as exc:
                self._send(HTTPStatus.BAD_REQUEST, {"error": "invalid_request", "detail": str(exc)}); return
            self._send(HTTPStatus.NOT_FOUND, {"error": "not_found"})
        def do_POST(self) -> None:  # noqa: N802
            try:
                if self.path == "/v1/authorize":
                    principal = runtime.authenticate(self.headers.get("Authorization"), "authorize")
                elif self.path.startswith("/v1/admin/"):
                    principal = runtime.authenticate(self.headers.get("Authorization"), "keys:write" if "/keys/" in self.path else "policy:write")
                else:
                    self._send(HTTPStatus.NOT_FOUND, {"error": "not_found"}); return
                runtime.enforce_rate_limit(principal)
                if self.headers.get("Content-Type", "").split(";", 1)[0] != "application/json":
                    raise ServiceRequestError("Content-Type must be application/json")
                length = int(self.headers.get("Content-Length", "0"))
                if length <= 0 or length > MAX_REQUEST_BYTES:
                    raise ServiceRequestError(f"Content-Length must be between 1 and {MAX_REQUEST_BYTES} bytes")
                request = json.loads(self.rfile.read(length).decode("utf-8"))
                payload = runtime.authorize(principal, request) if self.path == "/v1/authorize" else runtime.administer(principal, self.path.removeprefix("/v1/admin/"), request)
            except OperationsError as exc:
                self._send(HTTPStatus.TOO_MANY_REQUESTS if "rate limit" in str(exc) else HTTPStatus.BAD_REQUEST, {"error": "operations_error", "detail": str(exc)}); return
            except SecurityError as exc:
                self._send(HTTPStatus.FORBIDDEN, {"error": "forbidden", "detail": str(exc)}); return
            except (UnicodeDecodeError, json.JSONDecodeError, ServiceRequestError, EvidenceStoreError, ValueError) as exc:
                self._send(HTTPStatus.BAD_REQUEST, {"error": "invalid_request", "detail": str(exc)}); return
            self._send(HTTPStatus.OK, payload)
        def log_message(self, format: str, *args: Any) -> None:
            return
        def _send(self, status: int, payload: dict[str, Any]) -> None:
            runtime.metric(f"http.{int(status)}")
            body = (json.dumps(payload, sort_keys=True) + "\n").encode("utf-8")
            self.send_response(status); self.send_header("Content-Type", "application/json"); self.send_header("Content-Length", str(len(body))); self.end_headers(); self.wfile.write(body)
    return Handler


def serve_secured(host: str, port: int, runtime: SecuredRuntime) -> None:
    runtime.staging_root.mkdir(parents=True, exist_ok=True)
    ThreadingHTTPServer((host, port), make_secured_handler(runtime)).serve_forever()


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
