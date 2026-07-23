from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Iterable

class Truth(str, Enum):
    YES='yes'; NO='no'; UNKNOWN='unknown'
class Verdict(str, Enum):
    ADMISSIBLE='admissible'; INADMISSIBLE='inadmissible'; BLOCKED='blocked'; CONFIRMED='confirmed'; DEFECT='defect'
class Impact(str, Enum):
    NONE='none'; EVIDENCE_UPGRADE='evidence_upgrade'; CLARIFY='clarify'; NARROW='narrow'; REVISE='revise'; RETRACT='retract'

REQUIRED_CLAIMS=(
 'target_class_and_scope','faithfulness_contract','machinery_closure','commitment_equivalence',
 'five_component_necessity','component_independence','relative_sufficiency','relative_maximality',
 'terminal_weakened_outcome','mechanization_boundary','open_world_boundary','unknown_discipline')

@dataclass(frozen=True)
class ClaimFinding:
    claim_id: str
    reviewed: Truth
    sound: Truth
    material_defect: Truth
    evidence_refs: tuple[str,...]
    rationale: str

@dataclass(frozen=True)
class Reviewer:
    reviewer_id: str
    formal_methods_competence: Truth
    no_project_authorship: Truth
    no_prior_mapping_access: Truth
    conflicts_disclosed: Truth
    tools_disclosed: Truth
    independent_organization: Truth

@dataclass(frozen=True)
class ReviewPackage:
    reviewer: Reviewer
    theorem_version: str
    claim_findings: tuple[ClaimFinding,...]
    exact_artifacts_frozen: Truth
    complete_dependency_coverage: Truth
    failure_unknown_separated: Truth
    signed_declaration: Truth

@dataclass(frozen=True)
class Assessment:
    verdict: Verdict
    impact: Impact
    reasons: tuple[str,...]


def assess(pkg: ReviewPackage) -> Assessment:
    r=pkg.reviewer
    if not r.reviewer_id.strip() or r.formal_methods_competence is Truth.NO or r.no_project_authorship is Truth.NO or r.conflicts_disclosed is Truth.NO or r.tools_disclosed is Truth.NO:
        return Assessment(Verdict.INADMISSIBLE,Impact.NONE,('reviewer eligibility or disclosure failed',))
    if Truth.UNKNOWN in (r.formal_methods_competence,r.no_project_authorship,r.conflicts_disclosed,r.tools_disclosed,r.independent_organization):
        return Assessment(Verdict.BLOCKED,Impact.NONE,('reviewer independence or competence unresolved',))
    if r.no_prior_mapping_access is Truth.NO:
        # exposure is permitted only if disclosed; it prevents strongest independence grade
        return Assessment(Verdict.BLOCKED,Impact.NONE,('prior-artifact independence not established',))
    if not pkg.theorem_version.strip() or pkg.exact_artifacts_frozen is Truth.NO or pkg.signed_declaration is Truth.NO:
        return Assessment(Verdict.INADMISSIBLE,Impact.NONE,('review object or declaration malformed',))
    if Truth.UNKNOWN in (pkg.exact_artifacts_frozen,pkg.complete_dependency_coverage,pkg.failure_unknown_separated,pkg.signed_declaration):
        return Assessment(Verdict.BLOCKED,Impact.NONE,('review package completeness unresolved',))
    ids=[f.claim_id for f in pkg.claim_findings]
    if len(ids)!=len(set(ids)) or set(ids)!=set(REQUIRED_CLAIMS):
        return Assessment(Verdict.INADMISSIBLE,Impact.NONE,('claim ledger is incomplete or duplicated',))
    for f in pkg.claim_findings:
        if not f.rationale.strip() or not f.evidence_refs:
            return Assessment(Verdict.INADMISSIBLE,Impact.NONE,(f'finding {f.claim_id} lacks rationale or evidence',))
    if any(f.reviewed is Truth.UNKNOWN or f.sound is Truth.UNKNOWN or f.material_defect is Truth.UNKNOWN for f in pkg.claim_findings):
        return Assessment(Verdict.BLOCKED,Impact.NONE,('one or more claim findings remain Unknown',))
    defects=[f for f in pkg.claim_findings if f.material_defect is Truth.YES or f.sound is Truth.NO]
    if defects:
        severe={'target_class_and_scope','faithfulness_contract','relative_sufficiency','terminal_weakened_outcome'}
        impact=Impact.RETRACT if any(f.claim_id in severe and f.sound is Truth.NO for f in defects) else Impact.REVISE
        return Assessment(Verdict.DEFECT,impact,tuple(f.claim_id for f in defects))
    return Assessment(Verdict.CONFIRMED,Impact.EVIDENCE_UPGRADE,('independent review supports the reviewed claim set only',))


def canonical_unexecuted_package() -> ReviewPackage:
    reviewer=Reviewer('external-reviewer-pending',Truth.UNKNOWN,Truth.UNKNOWN,Truth.UNKNOWN,Truth.YES,Truth.YES,Truth.UNKNOWN)
    findings=tuple(ClaimFinding(c,Truth.UNKNOWN,Truth.UNKNOWN,Truth.UNKNOWN,('pending',),'Independent finding not yet supplied.') for c in REQUIRED_CLAIMS)
    return ReviewPackage(reviewer,'UPP-W15-v1.0',findings,Truth.YES,Truth.UNKNOWN,Truth.YES,Truth.NO)
