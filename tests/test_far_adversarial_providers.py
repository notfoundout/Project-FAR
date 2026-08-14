"""Provider contracts.

Regression for audit finding 9: the live path built the GPT provider with no
schema, so a strict request silently degraded to prose parsing, and the
campaign recorded the requested alias rather than the model actually served.

No test here performs a network call: ``interpret`` is exercised directly on
recorded response bodies.
"""

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from far_adversarial import protocol  # noqa: E402
from far_adversarial.providers import (  # noqa: E402
    ClaudeCodeProvider,
    INVALID_PROVIDER_OUTPUT,
    OpenAIProvider,
    PROVIDER_ERROR,
    PROVIDER_REFUSAL,
    RATE_LIMIT,
    RESOURCE_LIMIT,
    SOURCE_INTEGRITY_FAILURE,
    TOKEN_LIMIT,
)


def _body(**overrides):
    body = {
        "id": "resp_123",
        "model": "gpt-5-2026-05-01",
        "status": "completed",
        "usage": {"input_tokens": 10, "output_tokens": 20},
        "output": [
            {"type": "message",
             "content": [{"type": "output_text", "text": '{"responses": []}'}]}
        ],
    }
    body.update(overrides)
    return body


class StrictSchemaTests(unittest.TestCase):
    def test_a_strict_request_without_a_schema_is_refused(self):
        provider = OpenAIProvider(api_key="x", require_schema=True)
        result = provider.complete("prompt")
        self.assertFalse(result.ok)
        self.assertEqual(result.failure, INVALID_PROVIDER_OUTPUT)

    def test_the_payload_carries_the_strict_json_schema(self):
        provider = OpenAIProvider(api_key="x")
        payload = provider.payload("prompt", protocol.FIRST_PASS_SCHEMA)
        fmt = payload["text"]["format"]
        self.assertEqual(fmt["type"], "json_schema")
        self.assertTrue(fmt["strict"])
        self.assertEqual(fmt["schema"], protocol.FIRST_PASS_SCHEMA)

    def test_it_targets_the_responses_api(self):
        self.assertTrue(OpenAIProvider().ENDPOINT.endswith("/v1/responses"))
        payload = OpenAIProvider(api_key="x").payload("p", protocol.FIRST_PASS_SCHEMA)
        self.assertIn("input", payload)
        self.assertNotIn("messages", payload)

    def test_first_pass_schema_is_closed_and_fully_required(self):
        schema = protocol.FIRST_PASS_SCHEMA
        self.assertFalse(schema["additionalProperties"])
        self.assertEqual(set(schema["required"]), set(schema["properties"]))
        item = schema["properties"]["objections"]["items"]
        self.assertFalse(item["additionalProperties"])
        self.assertEqual(set(item["required"]), set(item["properties"]))

    def test_cross_audit_schema_is_closed_and_fully_required(self):
        schema = protocol.cross_audit_schema(["REBUT", "CONCEDE"])
        item = schema["properties"]["responses"]["items"]
        self.assertFalse(item["additionalProperties"])
        self.assertEqual(set(item["required"]), set(item["properties"]))
        self.assertEqual(item["properties"]["action"]["enum"], ["CONCEDE", "REBUT"])


class ResponseInterpretationTests(unittest.TestCase):
    def test_completed_response_returns_the_output_text(self):
        result = OpenAIProvider.interpret(_body())
        self.assertTrue(result.ok)
        self.assertEqual(result.raw, '{"responses": []}')

    def test_the_served_model_identity_is_recorded_not_the_alias(self):
        result = OpenAIProvider.interpret(_body())
        self.assertEqual(result.resolved_model, "gpt-5-2026-05-01")

    def test_request_id_and_usage_are_captured(self):
        result = OpenAIProvider.interpret(_body())
        self.assertEqual(result.request_id, "resp_123")
        self.assertEqual(result.usage["output_tokens"], 20)

    def test_token_ceiling_is_a_token_limit_not_a_finding(self):
        result = OpenAIProvider.interpret(_body(
            status="incomplete", incomplete_details={"reason": "max_output_tokens"}))
        self.assertEqual(result.failure, TOKEN_LIMIT)

    def test_other_incompleteness_is_a_resource_limit(self):
        result = OpenAIProvider.interpret(_body(
            status="incomplete", incomplete_details={"reason": "content_filter"}))
        self.assertEqual(result.failure, RESOURCE_LIMIT)

    def test_a_refusal_is_typed_as_a_refusal(self):
        result = OpenAIProvider.interpret(_body(output=[
            {"type": "message", "content": [{"type": "refusal", "refusal": "no"}]}
        ]))
        self.assertEqual(result.failure, PROVIDER_REFUSAL)
        self.assertEqual(result.raw, "no")

    def test_a_failed_response_is_a_provider_error(self):
        result = OpenAIProvider.interpret(_body(status="failed",
                                                error={"code": "server_error"}))
        self.assertEqual(result.failure, PROVIDER_ERROR)

    def test_a_failed_rate_limit_is_typed_as_a_rate_limit(self):
        result = OpenAIProvider.interpret(_body(status="failed",
                                                error={"code": "rate_limit_exceeded"}))
        self.assertEqual(result.failure, RATE_LIMIT)

    def test_a_response_with_no_message_is_malformed(self):
        result = OpenAIProvider.interpret(_body(output=[]))
        self.assertEqual(result.failure, INVALID_PROVIDER_OUTPUT)

    def test_an_unexpected_content_type_is_malformed(self):
        result = OpenAIProvider.interpret(_body(output=[
            {"type": "message", "content": [{"type": "reasoning", "text": "..."}]}
        ]))
        self.assertEqual(result.failure, INVALID_PROVIDER_OUTPUT)

    def test_every_failure_path_is_typed_and_none_returns_a_finding(self):
        bodies = [
            _body(status="failed", error={}),
            _body(status="incomplete", incomplete_details={"reason": "max_output_tokens"}),
            _body(output=[]),
            _body(output=[{"type": "message",
                           "content": [{"type": "refusal", "refusal": "no"}]}]),
        ]
        for body in bodies:
            result = OpenAIProvider.interpret(body)
            self.assertFalse(result.ok)
            self.assertIsNotNone(result.failure)

    def test_missing_credentials_are_reported_without_a_network_call(self):
        provider = OpenAIProvider(api_key="")
        ok, why = provider.available()
        self.assertFalse(ok)
        self.assertIn("OPENAI_CREDENTIALS_REQUIRED", why)


class ClaudeLaneIsolationTests(unittest.TestCase):
    """Regression for audit finding 8: the live lane is isolated like calibration."""

    def test_an_unsandboxed_claude_lane_refuses_to_run(self):
        provider = ClaudeCodeProvider(sandbox_cwd=None)
        ok, why = provider.available()
        self.assertFalse(ok)
        self.assertIn(SOURCE_INTEGRITY_FAILURE, why)
        result = provider.complete("prompt")
        self.assertEqual(result.failure, SOURCE_INTEGRITY_FAILURE)

    def test_every_tool_is_denied_including_readers(self):
        denied = ClaudeCodeProvider.DISALLOWED_TOOLS
        for tool in ("Read", "Glob", "Grep", "Bash", "Write", "Edit", "Task",
                     "WebFetch", "WebSearch", "Skill"):
            self.assertIn(tool, denied)

    def test_config_records_the_isolation_it_actually_had(self):
        import tempfile

        with tempfile.TemporaryDirectory() as tmp:
            config = ClaudeCodeProvider(sandbox_cwd=tmp).config()
            self.assertTrue(config["sandboxed_cwd"])
            self.assertTrue(config["read_only"])
            self.assertIn("Read", config["tools_denied"])

    def test_analytical_lanes_get_no_store_or_ledger_handle(self):
        for provider in (ClaudeCodeProvider(sandbox_cwd="/tmp"),
                         OpenAIProvider(api_key="x")):
            self.assertFalse(hasattr(provider, "ledger"))
            self.assertFalse(hasattr(provider, "store"))


if __name__ == "__main__":
    unittest.main()
