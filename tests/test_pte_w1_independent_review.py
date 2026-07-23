import unittest
from theory.evaluation.pte_independent_review_v1 import *


def valid_package():
    r=Reviewer('r1',Truth.YES,Truth.YES,Truth.YES,Truth.YES,Truth.YES,Truth.YES)
    fs=tuple(ClaimFinding(c,Truth.YES,Truth.YES,Truth.NO,(f'evidence:{c}',),'Checked against frozen artifacts.') for c in REQUIRED_CLAIMS)
    return ReviewPackage(r,'UPP-W15-v1.0',fs,Truth.YES,Truth.YES,Truth.YES,Truth.YES)

class TestPTEW1(unittest.TestCase):
    def test_confirmed(self):
        a=assess(valid_package()); self.assertEqual((a.verdict,a.impact),(Verdict.CONFIRMED,Impact.EVIDENCE_UPGRADE))
    def test_unexecuted_is_blocked(self): self.assertEqual(assess(canonical_unexecuted_package()).verdict,Verdict.BLOCKED)
    def test_project_author_inadmissible(self):
        p=valid_package(); r=Reviewer('r',Truth.YES,Truth.NO,Truth.YES,Truth.YES,Truth.YES,Truth.YES)
        self.assertEqual(assess(ReviewPackage(r,p.theorem_version,p.claim_findings,Truth.YES,Truth.YES,Truth.YES,Truth.YES)).verdict,Verdict.INADMISSIBLE)
    def test_unknown_independence_blocked(self):
        p=valid_package(); r=Reviewer('r',Truth.YES,Truth.YES,Truth.YES,Truth.YES,Truth.YES,Truth.UNKNOWN)
        self.assertEqual(assess(ReviewPackage(r,p.theorem_version,p.claim_findings,Truth.YES,Truth.YES,Truth.YES,Truth.YES)).verdict,Verdict.BLOCKED)
    def test_missing_claim_inadmissible(self):
        p=valid_package(); self.assertEqual(assess(ReviewPackage(p.reviewer,p.theorem_version,p.claim_findings[:-1],Truth.YES,Truth.YES,Truth.YES,Truth.YES)).verdict,Verdict.INADMISSIBLE)
    def test_duplicate_claim_inadmissible(self):
        p=valid_package(); fs=p.claim_findings[:-1]+(p.claim_findings[0],)
        self.assertEqual(assess(ReviewPackage(p.reviewer,p.theorem_version,fs,Truth.YES,Truth.YES,Truth.YES,Truth.YES)).verdict,Verdict.INADMISSIBLE)
    def test_unknown_finding_blocked(self):
        p=valid_package(); f=p.claim_findings[0]; u=ClaimFinding(f.claim_id,Truth.YES,Truth.UNKNOWN,Truth.UNKNOWN,f.evidence_refs,f.rationale)
        self.assertEqual(assess(ReviewPackage(p.reviewer,p.theorem_version,(u,)+p.claim_findings[1:],Truth.YES,Truth.YES,Truth.YES,Truth.YES)).verdict,Verdict.BLOCKED)
    def test_material_core_defect_retracts(self):
        p=valid_package(); f=p.claim_findings[0]; d=ClaimFinding(f.claim_id,Truth.YES,Truth.NO,Truth.YES,f.evidence_refs,'Counterexample defeats target scope.')
        a=assess(ReviewPackage(p.reviewer,p.theorem_version,(d,)+p.claim_findings[1:],Truth.YES,Truth.YES,Truth.YES,Truth.YES)); self.assertEqual((a.verdict,a.impact),(Verdict.DEFECT,Impact.RETRACT))
    def test_noncore_defect_revises(self):
        p=valid_package(); i=REQUIRED_CLAIMS.index('mechanization_boundary'); f=p.claim_findings[i]; d=ClaimFinding(f.claim_id,Truth.YES,Truth.NO,Truth.YES,f.evidence_refs,'Boundary misstated.')
        fs=list(p.claim_findings); fs[i]=d
        a=assess(ReviewPackage(p.reviewer,p.theorem_version,tuple(fs),Truth.YES,Truth.YES,Truth.YES,Truth.YES)); self.assertEqual((a.verdict,a.impact),(Verdict.DEFECT,Impact.REVISE))
    def test_empty_evidence_inadmissible(self):
        p=valid_package(); f=p.claim_findings[0]; e=ClaimFinding(f.claim_id,Truth.YES,Truth.YES,Truth.NO,(),f.rationale)
        self.assertEqual(assess(ReviewPackage(p.reviewer,p.theorem_version,(e,)+p.claim_findings[1:],Truth.YES,Truth.YES,Truth.YES,Truth.YES)).verdict,Verdict.INADMISSIBLE)

if __name__=='__main__': unittest.main()
