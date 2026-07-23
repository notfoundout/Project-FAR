"""Deterministic reference agent used by FAR adversarial demonstrations.

The agent models a customer-support refund decision with explicit identity, policy,
evidence, machinery, and revision events. It is intentionally small enough that
conventional output assertions and FAR integrity assertions can be compared.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Mapping

from .model import EvidenceStatus, MachineryItem, ReasoningEvent, ReleasePackage


@dataclass(frozen=True, slots=True)
class AgentConfiguration:
    release_id: str
    source_commit: str
    policy_source: str = "policy-v4.json"
    policy_version: str | None = "4"
    policy_mutable: bool = False
    customer_source: str = "approved-customer-api"
    customer_source_declared: bool = True
    memory_store: str | None = None
    memory_declared: bool = True
    customer_id_before_handoff: str = "customer-123"
    customer_id_after_handoff: str = "customer-123"
    revalidate_identity: bool = True
    invalidate_eligibility_support: bool = False
    withdraw_dependent_conclusion: bool = True
    benchmark_source: str | None = None
    benchmark_declared: bool = True
    external_state_source: str | None = None
    external_state_status: EvidenceStatus = EvidenceStatus.CONFIRMED


@dataclass(frozen=True, slots=True)
class AgentRun:
    output: str
    package: ReleasePackage


def _item(
    machinery_id: str,
    kind: str,
    name: str,
    *,
    version: str | None = None,
    declared: bool = True,
    mutable: bool = False,
    external: bool = False,
    evidence_status: EvidenceStatus = EvidenceStatus.CONFIRMED,
    required_dependencies: tuple[str, ...] = (),
) -> MachineryItem:
    return MachineryItem(
        machinery_id=machinery_id,
        kind=kind,
        name=name,
        version=version,
        required_dependencies=required_dependencies,
        evidence_status=evidence_status,
        declared=declared,
        effective=True if evidence_status is EvidenceStatus.CONFIRMED else None,
        valid=True if evidence_status is EvidenceStatus.CONFIRMED else None,
        mutable=mutable,
        external=external,
    )


def run_reference_agent(config: AgentConfiguration) -> AgentRun:
    machinery: list[MachineryItem] = [
        _item("runtime", "runtime", "python-reference-runtime", version="1"),
        _item("model", "model", "deterministic-rule-model", version="1", required_dependencies=("runtime",)),
        _item(
            "policy",
            "policy",
            config.policy_source,
            version=config.policy_version,
            mutable=config.policy_mutable,
            external=config.policy_source.startswith("http"),
            required_dependencies=("runtime",),
        ),
        _item(
            "customer-data",
            "api",
            config.customer_source,
            version="1",
            declared=config.customer_source_declared,
            external=True,
            required_dependencies=("runtime",),
        ),
        _item("identity-registry", "identity_registry", "customer-registry", version="1", required_dependencies=("customer-data",)),
    ]

    decision_dependencies = ["model", "policy", "customer-data", "identity-registry"]

    if config.memory_store:
        machinery.append(
            _item(
                "memory",
                "memory_store",
                config.memory_store,
                version="1",
                declared=config.memory_declared,
                external=True,
                required_dependencies=("runtime",),
            )
        )
        decision_dependencies.append("memory")

    if config.benchmark_source:
        machinery.append(
            _item(
                "benchmark",
                "benchmark",
                config.benchmark_source,
                version="1",
                declared=config.benchmark_declared,
                required_dependencies=("runtime",),
            )
        )
        decision_dependencies.append("benchmark")

    if config.external_state_source:
        machinery.append(
            _item(
                "external-state",
                "external_state_store",
                config.external_state_source,
                version=None,
                declared=True,
                external=True,
                evidence_status=config.external_state_status,
                required_dependencies=("runtime",),
            )
        )
        decision_dependencies.append("external-state")

    events: list[ReasoningEvent] = []

    def emit(event_type: str, subject: str, *, objects: tuple[str, ...] = (), evidence: tuple[str, ...] = (), machinery_refs: tuple[str, ...] = (), identity: str | None = None, status: EvidenceStatus = EvidenceStatus.CONFIRMED, attributes: Mapping[str, object] | None = None) -> None:
        events.append(
            ReasoningEvent(
                event_id=f"event-{len(events) + 1:02d}",
                run_id=f"run-{config.release_id}",
                release_id=config.release_id,
                sequence=len(events) + 1,
                event_type=event_type,
                subject_id=subject,
                object_ids=objects,
                evidence_refs=evidence,
                machinery_refs=machinery_refs,
                identity_context={"customer_id": identity} if identity else {},
                status=status,
                source_ref="reference-agent",
                attributes=attributes or {},
            )
        )

    emit("commitment_introduced", "refund-request", identity=config.customer_id_before_handoff)
    emit("evidence_attached", "identity-evidence", machinery_refs=("customer-data", "identity-registry"), identity=config.customer_id_before_handoff)
    emit("evidence_attached", "eligibility-evidence", machinery_refs=("customer-data",), identity=config.customer_id_before_handoff)
    emit("constraint_applied", "refund-policy", evidence=("policy",), machinery_refs=("policy",), identity=config.customer_id_before_handoff)

    if config.customer_id_after_handoff != config.customer_id_before_handoff:
        emit(
            "identity_changed",
            "customer-identity",
            objects=(config.customer_id_before_handoff, config.customer_id_after_handoff),
            machinery_refs=("identity-registry",),
            identity=config.customer_id_after_handoff,
        )
        if config.revalidate_identity:
            emit("identity_revalidated", "customer-identity", machinery_refs=("customer-data", "identity-registry"), identity=config.customer_id_after_handoff)

    emit(
        "conclusion_derived",
        "refund-approved",
        evidence=("identity-evidence", "eligibility-evidence", "refund-policy"),
        machinery_refs=tuple(decision_dependencies),
        identity=config.customer_id_after_handoff,
        attributes={"active": True},
    )

    if config.invalidate_eligibility_support:
        emit("support_invalidated", "eligibility-evidence", identity=config.customer_id_after_handoff)
        if config.withdraw_dependent_conclusion:
            emit("commitment_withdrawn", "refund-approved", objects=("eligibility-evidence",), identity=config.customer_id_after_handoff, attributes={"active": False})

    output = "REFUND_APPROVED"
    package = ReleasePackage(
        release_id=config.release_id,
        source_commit=config.source_commit,
        machinery=tuple(machinery),
        events=tuple(events),
        decision_roots=("model", "policy", "customer-data", "identity-registry", *tuple(x for x in ("memory" if config.memory_store else None, "benchmark" if config.benchmark_source else None, "external-state" if config.external_state_source else None) if x)),
        release_roots=("runtime",),
        replay_completeness=1.0 if all(item.declared and item.evidence_status is EvidenceStatus.CONFIRMED for item in machinery) else 0.8,
        output_metrics={"accuracy": 1.0},
    )
    return AgentRun(output=output, package=package)


def baseline_configuration() -> AgentConfiguration:
    return AgentConfiguration(release_id="baseline", source_commit="baseline-commit")
