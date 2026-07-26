from __future__ import annotations

import unittest

import access_probe_v2
import case_tools


class AccessProbeV2Tests(unittest.TestCase):
    def test_manifest_freezes_low_thinking_and_safe_output_budget(self) -> None:
        manifest = case_tools.load_manifest()
        gate = access_probe_v2.validate_request_contract(manifest)
        contract = gate["probe_request_contract"]
        self.assertEqual(contract["thinkingConfig"]["thinkingLevel"], "low")
        self.assertEqual(contract["temperature"], 0.0)
        self.assertGreaterEqual(contract["maxOutputTokens"], 256)
        self.assertEqual(contract, access_probe_v2.REQUEST_CONTRACT)

    def test_visible_response_excludes_thought_parts(self) -> None:
        payload = {
            "candidates": [
                {
                    "finishReason": "STOP",
                    "content": {
                        "parts": [
                            {"thought": True, "text": "internal reasoning"},
                            {"text": " FAR_ACCESS_OK\n"},
                        ]
                    },
                }
            ]
        }
        text, candidate, parts = access_probe_v2.visible_response(payload)
        self.assertEqual(text, "FAR_ACCESS_OK")
        self.assertEqual(candidate["finishReason"], "STOP")
        self.assertEqual(len(parts), 2)

    def test_empty_or_exhausted_candidate_is_diagnosable(self) -> None:
        payload = {
            "candidates": [
                {
                    "finishReason": "MAX_TOKENS",
                    "content": {"parts": []},
                }
            ],
            "usageMetadata": {
                "promptTokenCount": 12,
                "candidatesTokenCount": 0,
                "thoughtsTokenCount": 16,
                "totalTokenCount": 28,
            },
        }
        text, candidate, parts = access_probe_v2.visible_response(payload)
        self.assertEqual(text, "")
        self.assertEqual(candidate["finishReason"], "MAX_TOKENS")
        self.assertEqual(parts, [])
        self.assertEqual(
            access_probe_v2.usage_summary(payload)["thoughtsTokenCount"], 16
        )

    def test_failure_base_never_contains_raw_secret_or_benchmark_data(self) -> None:
        record = access_probe_v2.base_failure(
            "response_contract_mismatch", http_status=200
        )
        serialized = str(record)
        self.assertNotIn("GEMINI_API_KEY", serialized)
        self.assertNotIn("problem_statement", serialized)
        self.assertIs(record["api_key_persisted"], False)
        self.assertIs(record["benchmark_task_data_accessed"], False)
        self.assertIs(record["benchmark_outcomes_accessed"], False)

    def test_request_contract_hash_is_stable(self) -> None:
        self.assertEqual(
            access_probe_v2.request_contract_sha256(),
            case_tools.sha256_bytes(
                case_tools.canonical(access_probe_v2.REQUEST_CONTRACT)
            ),
        )


if __name__ == "__main__":
    unittest.main()
