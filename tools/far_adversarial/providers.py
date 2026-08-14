"""Provider abstraction for the two analytical lanes.

Claude runs through authenticated Claude Code noninteractive execution; GPT
runs through the OpenAI Responses API with strict structured output. Web UIs
are never automated and credentials are never written into evidence, prompts,
or logs.

Execution failures are typed separately from research dispositions. A rate
limit, a refusal, and a token ceiling are all execution outcomes. This module
never returns a research verdict.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import time
from dataclasses import dataclass
from typing import Any

from .safety import redact

INVALID_PROVIDER_OUTPUT = "INVALID_PROVIDER_OUTPUT"
PROVIDER_ERROR = "PROVIDER_ERROR"
PROVIDER_REFUSAL = "PROVIDER_REFUSAL"
RATE_LIMIT = "RATE_LIMIT"
RESOURCE_LIMIT = "RESOURCE_LIMIT"
TOKEN_LIMIT = "TOKEN_LIMIT"
SOURCE_INTEGRITY_FAILURE = "SOURCE_INTEGRITY_FAILURE"
INTERRUPTED = "INTERRUPTED"
CREDENTIALS_REQUIRED = "CREDENTIALS_REQUIRED"

EXECUTION_FAILURES = frozenset(
    {
        INVALID_PROVIDER_OUTPUT,
        PROVIDER_ERROR,
        PROVIDER_REFUSAL,
        RATE_LIMIT,
        RESOURCE_LIMIT,
        TOKEN_LIMIT,
        SOURCE_INTEGRITY_FAILURE,
        INTERRUPTED,
        CREDENTIALS_REQUIRED,
    }
)


@dataclass
class ProviderResult:
    raw: str
    request_id: str | None = None
    usage: dict[str, Any] | None = None
    failure: str | None = None
    started_at: float = 0.0
    finished_at: float = 0.0
    # The model the provider actually served, which may differ from the alias
    # that was requested. The campaign records this, not the alias.
    resolved_model: str | None = None

    @property
    def ok(self) -> bool:
        return self.failure is None


class Provider:
    name = "abstract"
    model = "abstract"

    def config(self) -> dict[str, Any]:
        return {"model": self.model}

    def complete(self, prompt: str, *, schema: dict[str, Any] | None = None) -> ProviderResult:
        raise NotImplementedError  # pragma: no cover - interface

    def available(self) -> tuple[bool, str | None]:
        return True, None


class ClaudeCodeProvider(Provider):
    """Authenticated Claude Code noninteractive execution.

    The lane is isolated by construction: every tool is denied and the process
    runs outside the repository, so it cannot read project instruction files,
    session state, or the answer to its own question. Its evidence is exactly
    what the orchestrator put in the prompt — the same contract the GPT lane
    operates under.
    """

    name = "claude"

    DISALLOWED_TOOLS = (
        "Bash,BashOutput,KillShell,Edit,Write,NotebookEdit,Read,Glob,Grep,"
        "Task,Agent,Skill,SlashCommand,TodoWrite,WebFetch,WebSearch"
    )

    def __init__(self, model: str = "claude-opus-5", timeout: int = 900,
                 binary: str = "claude", max_turns: int = 6,
                 sandbox_cwd: str | None = None):
        self.model = model
        self.timeout = timeout
        self.binary = binary
        self.max_turns = max_turns
        self.sandbox_cwd = sandbox_cwd

    def config(self) -> dict[str, Any]:
        return {
            "model": self.model,
            "max_turns": self.max_turns,
            "read_only": True,
            "tools_denied": self.DISALLOWED_TOOLS,
            "sandboxed_cwd": bool(self.sandbox_cwd),
        }

    def argv(self) -> list[str]:
        return [
            self.binary,
            "-p",
            "--model",
            self.model,
            "--disallowed-tools",
            self.DISALLOWED_TOOLS,
            "--max-turns",
            str(self.max_turns),
        ]

    def available(self) -> tuple[bool, str | None]:
        if shutil.which(self.binary) is None:
            return False, f"{CREDENTIALS_REQUIRED}: claude CLI not on PATH"
        if not self.sandbox_cwd:
            return False, (
                f"{SOURCE_INTEGRITY_FAILURE}: the Claude lane requires a sandbox "
                "working directory outside the repository; running in-repo lets it "
                "auto-load context the GPT lane never receives"
            )
        return True, None

    def complete(self, prompt: str, *, schema: dict[str, Any] | None = None) -> ProviderResult:
        started = time.time()
        ok, why = self.available()
        if not ok:
            failure = (SOURCE_INTEGRITY_FAILURE if why and
                       why.startswith(SOURCE_INTEGRITY_FAILURE) else CREDENTIALS_REQUIRED)
            return ProviderResult(raw=why or "", failure=failure, started_at=started,
                                  finished_at=time.time())
        try:
            proc = subprocess.run(
                self.argv(), input=prompt, capture_output=True, text=True,
                timeout=self.timeout, check=False, cwd=self.sandbox_cwd,
            )
        except subprocess.TimeoutExpired:
            return ProviderResult(raw="", failure=RESOURCE_LIMIT, started_at=started,
                                  finished_at=time.time())
        except KeyboardInterrupt:  # pragma: no cover - operator interrupt
            return ProviderResult(raw="", failure=INTERRUPTED, started_at=started,
                                  finished_at=time.time())
        finished = time.time()
        if proc.returncode != 0:
            combined = redact((proc.stderr or "") + (proc.stdout or ""))
            lowered = combined.lower()
            if "rate limit" in lowered:
                failure = RATE_LIMIT
            elif "max turns" in lowered:
                failure = RESOURCE_LIMIT
            else:
                failure = PROVIDER_ERROR
            return ProviderResult(raw=combined, failure=failure, started_at=started,
                                  finished_at=finished)
        return ProviderResult(raw=proc.stdout, started_at=started, finished_at=finished,
                              resolved_model=self.model)


class OpenAIProvider(Provider):
    """GPT lane over the OpenAI Responses API with strict structured output.

    A schema is mandatory in live execution. There is no path from a strict
    request to prose parsing: an output that does not conform is an
    ``INVALID_PROVIDER_OUTPUT`` execution failure, and a refusal is a
    ``PROVIDER_REFUSAL``, never an empty finding.
    """

    name = "gpt"
    ENDPOINT = "https://api.openai.com/v1/responses"

    def __init__(self, model: str = "gpt-5", timeout: int = 900,
                 api_key: str | None = None, require_schema: bool = True,
                 max_output_tokens: int | None = None):
        self.model = model
        self.timeout = timeout
        self._api_key = api_key if api_key is not None else os.environ.get("OPENAI_API_KEY")
        self.require_schema = require_schema
        self.max_output_tokens = max_output_tokens

    def config(self) -> dict[str, Any]:
        return {
            "model": self.model,
            "api": "responses",
            "strict_schema_required": self.require_schema,
            "max_output_tokens": self.max_output_tokens,
        }

    def available(self) -> tuple[bool, str | None]:
        if not self._api_key:
            return False, "LIVE_GPT_BLOCKED: OPENAI_CREDENTIALS_REQUIRED"
        return True, None

    def payload(self, prompt: str, schema: dict[str, Any] | None) -> dict[str, Any]:
        body: dict[str, Any] = {"model": self.model, "input": prompt}
        if schema:
            body["text"] = {
                "format": {
                    "type": "json_schema",
                    "name": "far_lane_output",
                    "strict": True,
                    "schema": schema,
                }
            }
        if self.max_output_tokens:
            body["max_output_tokens"] = self.max_output_tokens
        return body

    @staticmethod
    def interpret(payload: dict[str, Any]) -> ProviderResult:
        """Map a Responses API body onto a typed result.

        Every documented terminal shape is handled explicitly: completed,
        incomplete (token ceiling), refusal, failed, and anything unrecognised.
        """
        status = payload.get("status")
        usage = payload.get("usage") or {}
        request_id = payload.get("id")
        resolved = payload.get("model")
        common = dict(request_id=request_id, usage=usage, resolved_model=resolved)
        if status == "failed":
            error = payload.get("error") or {}
            code = str(error.get("code", "")).lower()
            failure = RATE_LIMIT if "rate_limit" in code else PROVIDER_ERROR
            return ProviderResult(raw=redact(json.dumps(error)), failure=failure, **common)
        if status == "incomplete":
            reason = (payload.get("incomplete_details") or {}).get("reason", "")
            failure = TOKEN_LIMIT if reason == "max_output_tokens" else RESOURCE_LIMIT
            return ProviderResult(raw=f"incomplete: {reason}", failure=failure, **common)
        message = next(
            (item for item in payload.get("output", []) if item.get("type") == "message"),
            None,
        )
        content = (message or {}).get("content") or []
        first = content[0] if content else None
        if first is None:
            return ProviderResult(raw=redact(json.dumps(payload))[:4000],
                                  failure=INVALID_PROVIDER_OUTPUT, **common)
        if first.get("type") == "refusal":
            return ProviderResult(raw=str(first.get("refusal", "")),
                                  failure=PROVIDER_REFUSAL, **common)
        if first.get("type") != "output_text":
            return ProviderResult(raw=redact(json.dumps(first))[:4000],
                                  failure=INVALID_PROVIDER_OUTPUT, **common)
        if status != "completed":
            return ProviderResult(raw=str(first.get("text", "")),
                                  failure=PROVIDER_ERROR, **common)
        return ProviderResult(raw=str(first.get("text", "")), **common)

    def complete(self, prompt: str, *, schema: dict[str, Any] | None = None) -> ProviderResult:
        import urllib.error
        import urllib.request

        started = time.time()
        if self.require_schema and schema is None:
            return ProviderResult(
                raw="strict schema required but not supplied",
                failure=INVALID_PROVIDER_OUTPUT, started_at=started, finished_at=time.time(),
            )
        ok, why = self.available()
        if not ok:
            return ProviderResult(raw=why or "", failure=CREDENTIALS_REQUIRED,
                                  started_at=started, finished_at=time.time())
        request = urllib.request.Request(
            self.ENDPOINT,
            data=json.dumps(self.payload(prompt, schema)).encode("utf-8"),
            headers={"Content-Type": "application/json",
                     "Authorization": f"Bearer {self._api_key}"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                body = json.loads(response.read().decode("utf-8"))
                header_request_id = response.headers.get("x-request-id")
        except urllib.error.HTTPError as exc:
            failure = RATE_LIMIT if exc.code == 429 else PROVIDER_ERROR
            return ProviderResult(raw=redact(str(exc)), failure=failure,
                                  started_at=started, finished_at=time.time())
        except Exception as exc:
            return ProviderResult(raw=redact(str(exc)), failure=PROVIDER_ERROR,
                                  started_at=started, finished_at=time.time())
        result = self.interpret(body)
        result.started_at = started
        result.finished_at = time.time()
        result.request_id = result.request_id or header_request_id
        return result


class ReplayProvider(Provider):
    """Deterministic replay from stored raw evidence.

    Replay never contacts a provider. A missing recording is a source-integrity
    failure, not a silent fallback to a live call.
    """

    name = "replay"

    def __init__(self, store, underlying_name: str, model: str, source_freeze: str):
        self.store = store
        self.underlying_name = underlying_name
        self.model = model
        self.source_freeze = source_freeze
        self.calls = 0

    def config(self) -> dict[str, Any]:
        return {"model": self.model, "replay_of": self.underlying_name}

    def complete(self, prompt: str, *, schema: dict[str, Any] | None = None) -> ProviderResult:
        from .evidence import replay_key
        from .safety import sha256_hex

        self.calls += 1
        key = replay_key(self.underlying_name, self.model, sha256_hex(redact(prompt)),
                         self.source_freeze)
        recorded = self.store.find_for_replay(key)
        if recorded is None:
            return ProviderResult(raw="", failure=SOURCE_INTEGRITY_FAILURE)
        return ProviderResult(
            raw=recorded.raw_response, request_id=recorded.request_id,
            usage=recorded.usage, started_at=recorded.started_at,
            finished_at=recorded.finished_at, resolved_model=recorded.resolved_model,
        )


class ScriptedProvider(Provider):
    """Fixed responses for deterministic tests. Performs no network access."""

    name = "scripted"

    def __init__(self, responses, model: str = "scripted-1", name: str = "scripted"):
        self._responses = list(responses)
        self.model = model
        self.name = name
        self.prompts: list[str] = []
        self.schemas: list[dict[str, Any] | None] = []

    def complete(self, prompt: str, *, schema: dict[str, Any] | None = None) -> ProviderResult:
        self.prompts.append(prompt)
        self.schemas.append(schema)
        if not self._responses:
            return ProviderResult(raw="", failure=INVALID_PROVIDER_OUTPUT)
        item = self._responses.pop(0)
        if isinstance(item, ProviderResult):
            return item
        if isinstance(item, str) and item in EXECUTION_FAILURES:
            return ProviderResult(raw="", failure=item)
        if not isinstance(item, str):
            item = json.dumps(item)
        return ProviderResult(raw=item, started_at=0.0, finished_at=0.0,
                              resolved_model=self.model)
