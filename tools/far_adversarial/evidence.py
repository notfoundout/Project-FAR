"""Append-only raw-evidence store for provider invocations.

Structured research state is an index over this store, never a replacement for
it. Every provider call is preserved with its exact request identity so that a
later run can be replayed byte-for-byte without contacting a provider.

Replay is not rerun: replay reproduces a recorded execution, while rerunning a
model creates a new execution with a new invocation identity.
"""

from __future__ import annotations

import json
import time
import uuid
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any

from .safety import redact, safe_component, sha256_hex

SCHEMA_VERSION = "far-adversarial-evidence/1"


def replay_key(provider: str, model: str, prompt_hash: str, source_freeze: str) -> str:
    """Identity of a request, independent of when it ran.

    Two invocations share a replay key exactly when the provider, the exact
    model/config identity, the prompt bytes, and the frozen source all match.
    """
    return sha256_hex("\x1f".join([provider, model, prompt_hash, source_freeze]))


@dataclass
class Invocation:
    invocation_id: str
    provider: str
    model: str
    config: dict[str, Any]
    prompt_hash: str
    source_freeze: str
    raw_response: str
    raw_response_hash: str
    normalized_response: Any
    normalized_response_hash: str
    request_id: str | None
    usage: dict[str, Any]
    started_at: float
    finished_at: float
    schema_version: str = SCHEMA_VERSION
    lane: str = ""
    target_id: str = ""
    replayed_from: str | None = None
    failure: str | None = None
    prompt_text: str = ""
    tags: list[str] = field(default_factory=list)

    def key(self) -> str:
        return replay_key(self.provider, self.model, self.prompt_hash, self.source_freeze)


class EvidenceStore:
    """Filesystem-backed, append-only store.

    The orchestrator is the only writer. Analytical lanes receive a provider
    handle, never a store handle.
    """

    def __init__(self, root: Path):
        self.root = Path(root)
        self.raw_dir = self.root / "raw"
        self.index_path = self.root / "index.jsonl"
        self.raw_dir.mkdir(parents=True, exist_ok=True)

    def record(
        self,
        *,
        provider: str,
        model: str,
        config: dict[str, Any],
        prompt_text: str,
        source_freeze: str,
        raw_response: str,
        normalized_response: Any,
        request_id: str | None = None,
        usage: dict[str, Any] | None = None,
        started_at: float | None = None,
        finished_at: float | None = None,
        lane: str = "",
        target_id: str = "",
        replayed_from: str | None = None,
        failure: str | None = None,
        tags: list[str] | None = None,
    ) -> Invocation:
        safe_prompt = redact(prompt_text)
        safe_raw = redact(raw_response)
        normalized_json = json.dumps(normalized_response, sort_keys=True, ensure_ascii=False)
        inv = Invocation(
            invocation_id=uuid.uuid4().hex,
            provider=provider,
            model=model,
            config=dict(config),
            prompt_hash=sha256_hex(safe_prompt),
            source_freeze=source_freeze,
            raw_response=safe_raw,
            raw_response_hash=sha256_hex(safe_raw),
            normalized_response=normalized_response,
            normalized_response_hash=sha256_hex(normalized_json),
            request_id=request_id,
            usage=dict(usage or {}),
            started_at=started_at if started_at is not None else time.time(),
            finished_at=finished_at if finished_at is not None else time.time(),
            lane=lane,
            target_id=target_id,
            replayed_from=replayed_from,
            failure=failure,
            prompt_text=safe_prompt,
            tags=list(tags or []),
        )
        raw_path = self.raw_dir / f"{safe_component(inv.invocation_id)}.txt"
        raw_path.write_text(safe_raw, encoding="utf-8")
        with self.index_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(asdict(inv), sort_keys=True, ensure_ascii=False) + "\n")
        return inv

    def all_invocations(self) -> list[Invocation]:
        if not self.index_path.exists():
            return []
        out: list[Invocation] = []
        for line in self.index_path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                out.append(Invocation(**json.loads(line)))
        return out

    def find_for_replay(self, key: str) -> Invocation | None:
        """Earliest recorded invocation with this request identity.

        Earliest, not latest: replay must be stable as the store grows.
        """
        for inv in self.all_invocations():
            if inv.failure is None and inv.key() == key:
                return inv
        return None

    def verify_integrity(self) -> list[str]:
        """Detect tampering with stored raw evidence."""
        problems: list[str] = []
        for inv in self.all_invocations():
            raw_path = self.raw_dir / f"{safe_component(inv.invocation_id)}.txt"
            if not raw_path.exists():
                problems.append(f"{inv.invocation_id}: raw evidence missing")
                continue
            actual = sha256_hex(raw_path.read_text(encoding="utf-8"))
            if actual != inv.raw_response_hash:
                problems.append(f"{inv.invocation_id}: raw evidence hash mismatch")
        return problems
