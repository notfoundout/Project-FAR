from __future__ import annotations

from dataclasses import dataclass

from .model import DecisionPackage, IntegrityStatus
from .semantic_audit import SemanticAudit, SemanticDisposition, audit_semantic_contract


@dataclass(frozen=True, slots=True)
class Finding:
    rule_id: str
    severity: str
    message: str
    node_id: str | None = None


@dataclass(frozen=True, slots=True)
class Adjudication:
    decision_id: str
    status: IntegrityStatus
    findings: tuple[Finding, ...]
    semantic_audits: tuple[SemanticAudit, ...] = ()


def adjudicate(
    package: DecisionPackage,
    *,
    require_semantic_contract: bool = False,
) -> Adjudication:
    findings: list[Finding] = []
    authorizing = {
        dependency.source_id
        for dependency in package.dependencies
        if dependency.target_id == package.decision_root
        and dependency.relation.strip().lower() == "authorizes"
    }

    for requirement in sorted(
        requirement
        for requirement in package.authorization_requirements
        if requirement not in authorizing
    ):
        findings.append(
            Finding(
                "authorization-dependency-missing",
                "error",
                f"Required authorization node {requirement!r} is not connected to the decision root by an 'authorizes' edge.",
                requirement,
            )
        )

    for node_id in sorted(
        node.node_id for node in package.nodes if node.attributes.get("valid") is False
    ):
        findings.append(
            Finding("required-node-invalid", "error", f"Node {node_id!r} is explicitly invalid.", node_id)
        )

    for node_id in sorted(
        node.node_id for node in package.nodes if node.attributes.get("contradicted") is True
    ):
        findings.append(
            Finding("evidence-contradicted", "error", f"Node {node_id!r} is contradicted.", node_id)
        )

    alternatives = package.metadata.get("material_alternatives", [])
    if isinstance(alternatives, list) and len(alternatives) > 1:
        findings.append(
            Finding(
                "material-alternatives-remain",
                "warning",
                "Multiple materially different outcomes remain compatible with the package.",
            )
        )
    if package.unknowns:
        findings.append(
            Finding(
                "declared-unknowns",
                "warning",
                f"The package declares {len(package.unknowns)} unresolved unknown(s).",
            )
        )
    if package.trace_completeness < 1.0:
        findings.append(
            Finding(
                "trace-incomplete",
                "warning",
                f"Trace completeness is {package.trace_completeness:.3f}, below the required 1.000.",
            )
        )

    semantic_audits = tuple(audit_semantic_contract(item) for item in package.semantic_contracts)
    gating_audits = tuple(audit for audit in semantic_audits if audit.is_gating)
    if require_semantic_contract and not gating_audits:
        findings.append(
            Finding(
                "semantic-contract-required",
                "warning",
                "A decision-gating FAR IR semantic contract is required but none was supplied; "
                "analysis_only records do not satisfy this requirement.",
                package.decision_root,
            )
        )

    for audit in semantic_audits:
        identity = audit.binding_id or audit.contract_id or audit.document_id or "<unnamed>"
        target = audit.target_node_id
        if audit.disposition is SemanticDisposition.MATERIAL_LOSS:
            findings.append(
                Finding(
                    "semantic-material-loss",
                    "error",
                    f"Semantic binding {identity!r} is a valid REFUTED collision for target "
                    f"{target!r}; the declared representation loses behavior required by its "
                    "frozen exact contract.",
                    target,
                )
            )
        elif audit.disposition is SemanticDisposition.OUTSIDE_TOLERANCE:
            findings.append(
                Finding(
                    "semantic-outside-tolerance",
                    "error",
                    f"Semantic binding {identity!r} selected candidate "
                    f"{audit.selected_candidate_id!r}, which is outside the verified feasible set "
                    "for the frozen approximation/cost contract.",
                    target,
                )
            )
        elif audit.disposition is SemanticDisposition.UNKNOWN:
            findings.append(
                Finding(
                    "semantic-contract-unknown",
                    "warning",
                    f"Semantic binding {identity!r} has valid typed Unknown evidence; "
                    "semantic sufficiency is not established.",
                    target,
                )
            )
        elif audit.disposition is SemanticDisposition.INVALID:
            codes = ", ".join(item.code for item in audit.diagnostics) or "no-diagnostic"
            findings.append(
                Finding(
                    "semantic-contract-invalid",
                    "warning",
                    f"Semantic binding {identity!r} failed binding or canonical FAR IR validation "
                    f"({codes}); it cannot support the target decision node.",
                    target,
                )
            )
        elif audit.disposition is SemanticDisposition.UNAVAILABLE:
            detail = audit.diagnostics[0].message if audit.diagnostics else "unknown verifier failure"
            findings.append(
                Finding(
                    "semantic-verifier-unavailable",
                    "warning",
                    f"Semantic binding {identity!r} could not be checked by canonical FAR IR machinery: "
                    f"{detail}",
                    target,
                )
            )

    rule_ids = {finding.rule_id for finding in findings}
    unsupported = {
        "authorization-dependency-missing",
        "required-node-invalid",
        "evidence-contradicted",
        "semantic-material-loss",
        "semantic-outside-tolerance",
    }
    unverifiable = {
        "declared-unknowns",
        "trace-incomplete",
        "semantic-contract-required",
        "semantic-contract-unknown",
        "semantic-contract-invalid",
        "semantic-verifier-unavailable",
    }
    if rule_ids & unsupported:
        status = IntegrityStatus.UNSUPPORTED
    elif "material-alternatives-remain" in rule_ids:
        status = IntegrityStatus.UNDERDETERMINED
    elif rule_ids & unverifiable:
        status = IntegrityStatus.UNVERIFIABLE
    else:
        status = IntegrityStatus.JUSTIFIED

    return Adjudication(package.decision_id, status, tuple(findings), semantic_audits)
