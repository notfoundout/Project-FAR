"""Deterministic replay.

Replay reconstructs a recorded run from stored raw evidence and checks that the
reconstruction lands on the same final state. It is not a rerun: no provider is
contacted, no new execution identity is created, and nothing is resampled.

The reconstruction is only meaningful if it goes through the same code path the
original run went through. So replay re-runs the real orchestrator with a
replay-backed provider: the same prompts are rebuilt from the same frozen
source, the same parsers run over the same raw bytes, and the same reducer
applies the same events in the same order.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

from .evidence import EvidenceStore, RunRecord
from .frozen_source import FrozenSource, SourceIntegrityError
from .ledger import LEDGER_SCHEMA, Ledger, REDUCER_VERSION, Target
from .orchestrator import Orchestrator
from .protocol import PROTOCOL_VERSION
from .providers import ReplayProvider


@dataclass
class ReplayResult:
    ok: bool
    reason: str = ""
    expected_digest: str = ""
    reconstructed_digest: str = ""
    integrity_problems: list[str] = field(default_factory=list)
    provider_calls: int = 0

    def __bool__(self) -> bool:  # pragma: no cover - convenience
        return self.ok


def replay(
    *,
    store: EvidenceStore,
    record: RunRecord,
    baseline_ledger: Ledger,
    frozen_source: FrozenSource,
    evidence_loader: Callable[[Target], dict[str, str]],
    max_rounds_per_target: int,
    max_targets: int = 8,
    allow_migration: bool = False,
) -> ReplayResult:
    """Rebuild the recorded run's final state and compare digests.

    Fails closed on: a drifted frozen source, tampered raw or normalized
    evidence, a reducer/schema/protocol version the record was not produced
    under, a missing recording, or any digest divergence.
    """
    # 1. Version gates. A reducer change silently reinterpreting old events is
    #    exactly the failure replay exists to catch.
    if not allow_migration:
        for label, expected, actual in (
            ("reducer", record.reducer_version, REDUCER_VERSION),
            ("ledger schema", record.ledger_schema, LEDGER_SCHEMA),
            ("protocol", record.protocol_version, PROTOCOL_VERSION),
        ):
            if expected != actual:
                return ReplayResult(
                    ok=False,
                    reason=(f"{label} version mismatch: run recorded under {expected!r}, "
                            f"current is {actual!r}; migrate explicitly"),
                    expected_digest=record.final_ledger_digest,
                )

    # 2. Frozen source identity.
    try:
        frozen_source.verify()
        identity = frozen_source.identity()
    except SourceIntegrityError as exc:
        return ReplayResult(ok=False, reason=f"frozen source unusable: {exc}")
    if identity != record.source_identity:
        return ReplayResult(
            ok=False,
            reason=(f"frozen source drifted: run used {record.source_identity}, "
                    f"current resolves to {identity}"),
        )

    # 3. Stored-evidence integrity, raw and normalized.
    problems = store.verify_integrity()
    if problems:
        return ReplayResult(ok=False, reason="stored evidence failed integrity check",
                            integrity_problems=problems)

    # 4. Baseline must be the state the run actually started from.
    if baseline_ledger.digest() != record.baseline_ledger_digest:
        return ReplayResult(
            ok=False,
            reason=(f"baseline ledger digest {baseline_ledger.digest()} does not match "
                    f"recorded baseline {record.baseline_ledger_digest}"),
        )

    # 5. Re-run the real loop with replay-backed providers.
    claude = ReplayProvider(store, "claude", record.lane_models["claude"], identity)
    gpt = ReplayProvider(store, "gpt", record.lane_models["gpt"], identity)
    orchestrator = Orchestrator(
        ledger=baseline_ledger,
        store=_ReplayIdStore(record.invocation_ids),
        claude=claude,
        gpt=gpt,
        evidence_loader=evidence_loader,
        source_freeze=identity,
        max_rounds_per_target=max_rounds_per_target,
        parallel=False,
    )
    orchestrator.run(max_targets=max_targets)
    reconstructed = baseline_ledger.digest()
    calls = claude.calls + gpt.calls
    if reconstructed != record.final_ledger_digest:
        return ReplayResult(
            ok=False,
            reason="reconstructed final state diverges from the recorded final state",
            expected_digest=record.final_ledger_digest,
            reconstructed_digest=reconstructed,
            provider_calls=calls,
        )
    return ReplayResult(ok=True, expected_digest=record.final_ledger_digest,
                        reconstructed_digest=reconstructed, provider_calls=calls)


class _ReplayIdStore:
    """Hands back the original invocation ids instead of writing new evidence.

    Replay must not append to the append-only store: reconstructing a run is
    not a new execution and must leave no trace that looks like one. It also
    must reissue the recorded identities in order, because invocation ids are
    embedded in issue provenance — inventing fresh ones would make a faithful
    reconstruction look like a divergence.
    """

    def __init__(self, invocation_ids: list[str]):
        self._ids = list(invocation_ids)
        self._index = 0

    def record(self, **kwargs):
        from .evidence import Invocation

        if self._index < len(self._ids):
            invocation_id = self._ids[self._index]
        else:
            # More calls than the original run made: the reconstruction has
            # already diverged, and the digest comparison will say so.
            invocation_id = f"unrecorded-{self._index}"
        self._index += 1
        return Invocation(
            invocation_id=invocation_id, provider=kwargs.get("provider", ""),
            model=kwargs.get("model", ""), config={}, prompt_hash="",
            source_freeze=kwargs.get("source_freeze", ""), raw_response="",
            raw_response_hash="", normalized_response=None,
            normalized_response_hash="", request_id=None, usage={},
            started_at=0.0, finished_at=0.0,
        )


def load_baseline(path: Path) -> Ledger:
    return Ledger.load(path)
