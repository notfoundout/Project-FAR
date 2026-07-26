from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

import case_tools

FAILURE_SCHEMA = "far-provider-access-probe-failure/1.1"
FAILURE_PATH = case_tools.OUTPUT_DIR / "access-probe-failure.json"
REQUEST_CONTRACT = {
    "temperature": 0.0,
    "maxOutputTokens": 1024,
    "thinkingConfig": {"thinkingLevel": "low"},
}


def request_contract_sha256() -> str:
    return case_tools.sha256_bytes(case_tools.canonical(REQUEST_CONTRACT))


def validate_request_contract(manifest: dict[str, Any]) -> dict[str, Any]:
    gate = manifest.get("provider_access_gate", {})
    registered = gate.get("probe_request_contract")
    if registered != REQUEST_CONTRACT:
        raise SystemExit("Provider access probe request contract drift")
    return gate


def visible_response(payload: dict[str, Any]) -> tuple[str, dict[str, Any], list[dict[str, Any]]]:
    candidates = payload.get("candidates")
    candidate = candidates[0] if isinstance(candidates, list) and candidates else {}
    if not isinstance(candidate, dict):
        candidate = {}
    content = candidate.get("content")
    content = content if isinstance(content, dict) else {}
    raw_parts = content.get("parts")
    raw_parts = raw_parts if isinstance(raw_parts, list) else []
    parts = [part for part in raw_parts if isinstance(part, dict)]
    visible_parts = [part for part in parts if part.get("thought") is not True]
    text = "".join(str(part.get("text", "")) for part in visible_parts).strip()
    return text, candidate, parts


def usage_summary(payload: dict[str, Any]) -> dict[str, int | float | str | None]:
    usage = payload.get("usageMetadata")
    usage = usage if isinstance(usage, dict) else {}
    allowed = (
        "promptTokenCount",
        "candidatesTokenCount",
        "thoughtsTokenCount",
        "totalTokenCount",
    )
    return {key: usage.get(key) for key in allowed}


def base_failure(kind: str, *, http_status: int | None) -> dict[str, Any]:
    return {
        "schema": FAILURE_SCHEMA,
        "case_id": case_tools.CASE_ID,
        "requested_model": case_tools.MODEL,
        "observed_at": case_tools.now(),
        "failure_kind": kind,
        "http_status": http_status,
        "probe_request_contract_sha256": request_contract_sha256(),
        "api_key_persisted": False,
        "probe_is_nonbenchmark": True,
        "benchmark_task_data_accessed": False,
        "benchmark_outcomes_accessed": False,
    }


def write_failure(record: dict[str, Any]) -> Path:
    case_tools.write_json(FAILURE_PATH, record)
    return FAILURE_PATH


def access_probe() -> Path:
    manifest = case_tools.validate_repository()
    if manifest["status"] != case_tools.PENDING:
        raise SystemExit("Access probe is only valid before freeze")
    key = os.environ.get("GEMINI_API_KEY", "")
    if not key:
        raise SystemExit("GEMINI_API_KEY is required for the access probe")

    gate = validate_request_contract(manifest)
    prompt = gate["probe_prompt"]
    if case_tools.sha256_bytes(prompt.encode()) != gate["probe_prompt_sha256"]:
        raise SystemExit("Preregistered probe prompt hash mismatch")

    body = {
        "contents": [{"role": "user", "parts": [{"text": prompt}]}],
        "generationConfig": REQUEST_CONTRACT,
    }
    request = urllib.request.Request(
        gate["probe_endpoint"],
        data=json.dumps(body).encode(),
        headers={"Content-Type": "application/json", "x-goog-api-key": key},
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            status = int(response.status)
            raw = response.read().decode(errors="replace")
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode(errors="replace")
        try:
            provider_error = json.loads(raw).get("error", {})
        except json.JSONDecodeError:
            provider_error = {"message": raw[:1000]}
        record = base_failure("provider_http_error", http_status=int(exc.code))
        record["provider_error"] = {
            "code": provider_error.get("code"),
            "status": provider_error.get("status"),
            "message": str(provider_error.get("message", ""))[:1000],
        }
        write_failure(record)
        raise SystemExit(f"Exact model access probe failed with HTTP {exc.code}") from None
    except urllib.error.URLError as exc:
        record = base_failure("provider_transport_error", http_status=None)
        record["transport_error"] = str(exc.reason)[:1000]
        write_failure(record)
        raise SystemExit("Exact model access probe failed before receiving an HTTP response") from None

    try:
        payload = json.loads(raw)
    except json.JSONDecodeError:
        record = base_failure("provider_response_not_json", http_status=status)
        record["response_bytes"] = len(raw.encode())
        record["response_sha256"] = case_tools.sha256_bytes(raw.encode())
        write_failure(record)
        raise SystemExit("Provider returned a non-JSON access-probe response") from None
    if not isinstance(payload, dict):
        record = base_failure("provider_response_not_object", http_status=status)
        record["response_type"] = type(payload).__name__
        write_failure(record)
        raise SystemExit("Provider returned a non-object access-probe response")

    text, candidate, parts = visible_response(payload)
    expected = gate["required_exact_response"]
    if status != 200 or text != expected:
        record = base_failure("response_contract_mismatch", http_status=status)
        record.update(
            {
                "provider_model_version": payload.get("modelVersion"),
                "finish_reason": candidate.get("finishReason"),
                "candidate_count": len(payload.get("candidates", []))
                if isinstance(payload.get("candidates"), list)
                else 0,
                "part_count": len(parts),
                "thought_part_count": sum(part.get("thought") is True for part in parts),
                "visible_text_length": len(text),
                "visible_text_sha256": case_tools.sha256_bytes(text.encode()),
                "expected_response_sha256": case_tools.sha256_bytes(expected.encode()),
                "usage_metadata": usage_summary(payload),
                "raw_response_persisted": False,
            }
        )
        write_failure(record)
        usage = record["usage_metadata"]
        raise SystemExit(
            "Provider returned HTTP "
            f"{status} but failed the exact response contract: "
            f"finish_reason={record['finish_reason']!r}, "
            f"visible_text_length={record['visible_text_length']}, "
            f"thoughts_tokens={usage.get('thoughtsTokenCount')!r}"
        )

    attestation = {
        "schema": case_tools.ACCESS_SCHEMA,
        "case_id": case_tools.CASE_ID,
        "requested_model": case_tools.MODEL,
        "provider_endpoint": gate["probe_endpoint"],
        "observed_at": case_tools.now(),
        "http_status": status,
        "provider_model_version": payload.get("modelVersion"),
        "prompt_sha256": gate["probe_prompt_sha256"],
        "expected_response": expected,
        "response_text_sha256": case_tools.sha256_bytes(text.encode()),
        "probe_request_contract_sha256": request_contract_sha256(),
        "thinking_level": REQUEST_CONTRACT["thinkingConfig"]["thinkingLevel"],
        "max_output_tokens": REQUEST_CONTRACT["maxOutputTokens"],
        "usage_metadata": usage_summary(payload),
        "exact_response": True,
        "probe_is_nonbenchmark": True,
        "benchmark_task_data_accessed": False,
        "benchmark_outcomes_accessed": False,
        "api_key_persisted": False,
    }
    target = case_tools.CASE_DIR / "access-freeze/provider-access-attestation.json"
    case_tools.write_json(target, attestation)
    (target.parent / "provider-access-attestation.sha256").write_text(
        case_tools.sha256_file(target) + "\n"
    )
    FAILURE_PATH.unlink(missing_ok=True)
    print(
        f"Exact {case_tools.MODEL} access verified with low thinking and a fixed "
        "non-benchmark probe."
    )
    return target


def main() -> None:
    access_probe()


if __name__ == "__main__":
    main()
