"""Provider abstraction for the two analytical lanes.

Claude runs through authenticated Claude Code noninteractive execution; GPT
runs through the OpenAI HTTP API. Web UIs are never automated and credentials
are never written into evidence, prompts, or logs.

Execution failures are typed separately from research dispositions. A rate
limit is not a stalemate, and this module never returns a research verdict.
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


class ExecutionFailure(str):
    """Typed non-epistemic failure codes."""


INVALID_PROVIDER_OUTPUT = "INVALID_PROVIDER_OUTPUT"
PROVIDER_ERROR = "PROVIDER_ERROR"
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

    @property
    def ok(self) -> bool:
        return self.failure is None


class Provider:
    name = "abstract"
    model = "abstract"

    def config(self) -> dict[str, Any]:
        return {"model": self.model}

    def complete(self, prompt: str) -> ProviderResult:  # pragma: no cover - interface
        raise NotImplementedError

    def available(self) -> tuple[bool, str | None]:
        return True, None


class ClaudeCodeProvider(Provider):
    """Authenticated Claude Code noninteractive execution.

    The analytical lane is read-only by construction: the subprocess is started
    with every tool disallowed, so a lane cannot write canonical or frozen
    content even if its own output asks it to.
    """

    name = "claude"

    # Every tool is denied, not just the writing ones. A lane must reason from
    # the frozen evidence the orchestrator put in its prompt and from nothing
    # else: a lane that can read the repository can read the answer, which
    # destroys both blindness between lanes and blind historical calibration.
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
        # Run outside the repository so project instruction files are not
        # auto-loaded into the lane's context.
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
        return True, None

    def complete(self, prompt: str) -> ProviderResult:
        started = time.time()
        ok, why = self.available()
        if not ok:
            return ProviderResult(raw="", failure=CREDENTIALS_REQUIRED, started_at=started,
                                  finished_at=time.time())
        try:
            proc = subprocess.run(
                self.argv(),
                input=prompt,
                capture_output=True,
                text=True,
                timeout=self.timeout,
                check=False,
                cwd=self.sandbox_cwd,
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
        return ProviderResult(raw=proc.stdout, started_at=started, finished_at=finished)


class OpenAIProvider(Provider):
    """GPT lane over the supported OpenAI HTTP API.

    Structured output is requested where the model supports it; a response that
    does not parse is an ``INVALID_PROVIDER_OUTPUT`` execution failure, never a
    research finding.
    """

    name = "gpt"
    ENDPOINT = "https://api.openai.com/v1/chat/completions"

    def __init__(self, model: str = "gpt-5", timeout: int = 900, api_key: str | None = None,
                 schema: dict[str, Any] | None = None):
        self.model = model
        self.timeout = timeout
        self._api_key = api_key if api_key is not None else os.environ.get("OPENAI_API_KEY")
        self.schema = schema

    def config(self) -> dict[str, Any]:
        return {"model": self.model, "structured_output": bool(self.schema)}

    def available(self) -> tuple[bool, str | None]:
        if not self._api_key:
            return False, "LIVE_GPT_BLOCKED: OPENAI_CREDENTIALS_REQUIRED"
        return True, None

    def _payload(self, prompt: str) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
        }
        if self.schema:
            payload["response_format"] = {
                "type": "json_schema",
                "json_schema": {"name": "far_lane_output", "strict": True,
                                "schema": self.schema},
            }
        return payload

    def complete(self, prompt: str) -> ProviderResult:
        import urllib.error
        import urllib.request

        started = time.time()
        ok, why = self.available()
        if not ok:
            return ProviderResult(raw=why or "", failure=CREDENTIALS_REQUIRED,
                                  started_at=started, finished_at=time.time())
        body = json.dumps(self._payload(prompt)).encode("utf-8")
        request = urllib.request.Request(
            self.ENDPOINT,
            data=body,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self._api_key}",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                payload = json.loads(response.read().decode("utf-8"))
                request_id = response.headers.get("x-request-id")
        except urllib.error.HTTPError as exc:
            failure = RATE_LIMIT if exc.code == 429 else PROVIDER_ERROR
            return ProviderResult(raw=redact(str(exc)), failure=failure, started_at=started,
                                  finished_at=time.time())
        except Exception as exc:  # network/parse level
            return ProviderResult(raw=redact(str(exc)), failure=PROVIDER_ERROR,
                                  started_at=started, finished_at=time.time())
        finished = time.time()
        try:
            choice = payload["choices"][0]
            text = choice["message"]["content"]
            if choice.get("finish_reason") == "length":
                return ProviderResult(raw=text or "", failure=TOKEN_LIMIT,
                                      started_at=started, finished_at=finished)
        except (KeyError, IndexError, TypeError):
            return ProviderResult(raw=json.dumps(payload)[:4000], failure=INVALID_PROVIDER_OUTPUT,
                                  started_at=started, finished_at=finished)
        return ProviderResult(
            raw=text or "",
            request_id=request_id or payload.get("id"),
            usage=payload.get("usage") or {},
            started_at=started,
            finished_at=finished,
        )


class ReplayProvider(Provider):
    """Deterministic replay from stored raw evidence.

    Replay never contacts a provider. A missing recording is an error, not a
    silent fallback to a live call.
    """

    name = "replay"

    def __init__(self, store, underlying_name: str, model: str, source_freeze: str):
        self.store = store
        self.underlying_name = underlying_name
        self.model = model
        self.source_freeze = source_freeze

    def config(self) -> dict[str, Any]:
        return {"model": self.model, "replay_of": self.underlying_name}

    def complete(self, prompt: str) -> ProviderResult:
        from .evidence import replay_key
        from .safety import sha256_hex

        key = replay_key(self.underlying_name, self.model, sha256_hex(redact(prompt)),
                         self.source_freeze)
        recorded = self.store.find_for_replay(key)
        if recorded is None:
            return ProviderResult(raw="", failure=SOURCE_INTEGRITY_FAILURE)
        return ProviderResult(
            raw=recorded.raw_response,
            request_id=recorded.request_id,
            usage=recorded.usage,
            started_at=recorded.started_at,
            finished_at=recorded.finished_at,
        )


class ScriptedProvider(Provider):
    """Fixed responses for deterministic tests. Performs no network access."""

    name = "scripted"

    def __init__(self, responses, model: str = "scripted-1", name: str = "scripted"):
        self._responses = list(responses)
        self.model = model
        self.name = name
        self.prompts: list[str] = []

    def complete(self, prompt: str) -> ProviderResult:
        self.prompts.append(prompt)
        if not self._responses:
            return ProviderResult(raw="", failure=INVALID_PROVIDER_OUTPUT)
        item = self._responses.pop(0)
        if isinstance(item, ProviderResult):
            return item
        if isinstance(item, str) and item in EXECUTION_FAILURES:
            return ProviderResult(raw="", failure=item)
        if not isinstance(item, str):
            item = json.dumps(item)
        return ProviderResult(raw=item, started_at=0.0, finished_at=0.0)
