from __future__ import annotations

from dataclasses import dataclass

from .model import DecisionPackage, IntegrityStatus


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


def adjudicate(package: DecisionPackage) -> Adjudication:
    findings: list[Finding] = []
    nodes = {node.node_id: node for node in package.nodes}
    incoming = {dependency.source_id for dependency in package.dependencies if dependency.target_id == package.decision_root}

    missing_links = [requirement for requirement in package.authorization_requirements if requirement not in incoming]
    for requirement in sorted(missing_links):
        findings.append(Finding("authorization-dependency-missing", "error", f"Required authorization node {requirement!r} is not connected to the decision root.", requirement))

    invalid_nodes = sorted(node.node_id for node in package.nodes if node.attributes.get("valid") is False)
    for node_id in invalid_nodes:
        findings.append(Finding("required-node-invalid", "error", f"Node {node_id!r} is explicitly invalid.", node_id))

    contradicted_nodes = sorted(node.node_id for node in package.nodes if node.attributes.get("contradicted") is True)
    for node_id in contradicted_nodes:
        findings.append(Finding("evidence-contradicted", "error", f"Node {node_id!r} is contradicted.", node_id))

    alternatives = package.metadata.get("material_alternatives", [])
    if isinstance(alternatives, list) and len(alternatives) > 1:
        findings.append(Finding("material-alternatives-remain", "warning", "Multiple materially different outcomes remain compatible with the package."))

    if package.unknowns:
        findings.append(Finding("declared-unknowns", "warning", f"The package declares {len(package.unknowns)} unresolved unknown(s)."))
    if package.trace_completeness < 1.0:
        findings.append(Finding("trace-incomplete", "warning", f"Trace completeness is {package.trace_completeness:.3f}, below the required 1.000."))

    rule_ids = {finding.rule_id for finding in findings}
    unsupported = {"authorization-dependency-missing", "required-node-invalid", "evidence-contradicted"}
    if rule_ids & unsupported:
        status = IntegrityStatus.UNSUPPORTED
    elif "material-alternatives-remain" in rule_ids:
        status = IntegrityStatus.UNDERDETERMINED
    elif {"declared-unknowns", "trace-incomplete"} & rule_ids:
        status = IntegrityStatus.UNVERIFIABLE
    else:
        status = IntegrityStatus.JUSTIFIED

    return Adjudication(package.decision_id, status, tuple(findings))
