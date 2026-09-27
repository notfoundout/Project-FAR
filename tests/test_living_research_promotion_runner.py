from __future__ import annotations
import hashlib, json, os, subprocess, tempfile, unittest
from pathlib import Path
from unittest import mock
from tools import promote_living_research as p
from tools import run_living_research_promotion as runner

H=lambda b: hashlib.sha256(b).hexdigest()
CID="FAR-LIT-0123456789ABCDEF"

def write_json(path:Path,value):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(value,sort_keys=True)+"\n",encoding="utf-8")

class PromotionRunnerTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(); self.root=Path(self.tmp.name); self.old=runner.ROOT; runner.ROOT=self.root
        (self.root/"research/living").mkdir(parents=True); (self.root/"docs").mkdir()
        (self.root/p.POLICY).write_bytes(Path(p.POLICY).read_bytes())
        basis=b"review basis\n"; (self.root/"docs/review.md").write_bytes(basis)
        self.review={"candidate_id":CID,"source_key":"doi:x","disposition":"N1_PRIOR_ART_LEAD","review_basis":"docs/review.md"}
        write_json(self.root/p.REVIEWS,{"reviewed_candidates":[self.review]})
        self.candidate=b'{"candidate_id":"x"}\n'; self.item={"candidate_id":CID,"path":f"{p.CANDIDATES}{CID}.json","source_key":"doi:x","disposition":"N1_PRIOR_ART_LEAD","review_basis":"docs/review.md","source_sha256":H(self.candidate),"expected_main_sha256":"ABSENT"}
        self.plan={"snapshot_candidates":[dict(self.item)],"canonical_proposals":[],"fatal":False,"actionable":True}
        self.basis_hash=H(basis)
    def tearDown(self): runner.ROOT=self.old; self.tmp.cleanup()
    def auth(self,**changes):
        row={"candidate_id":CID,"candidate_sha256":self.item["source_sha256"],"source_key":"doi:x","disposition":"N1_PRIOR_ART_LEAD","review_basis":"docs/review.md","review_basis_sha256":self.basis_hash,"review_record_sha256":p.canonical_json_sha(self.review),"authorization_status":runner.SNAPSHOT_STATUS}; row.update(changes)
        write_json(self.root/runner.SNAPSHOT_AUTHS,{"schema_version":"1.1","program_id":"FAR-LIVING-SNAPSHOT-AUTHORIZATIONS-001","authority":"Research","authorizations":[row]})
    def empty_auth(self): write_json(self.root/runner.SNAPSHOT_AUTHS,{"schema_version":"1.1","program_id":"FAR-LIVING-SNAPSHOT-AUTHORIZATIONS-001","authority":"Research","authorizations":[]})
    def test_review_alone_is_never_snapshot_authority(self):
        self.empty_auth(); blocked=runner.exact_snapshot_authorization_gate(self.plan)
        self.assertEqual(CID,blocked[0]["candidate_id"]); self.assertEqual([],self.plan["snapshot_candidates"]); self.assertFalse(self.plan["actionable"])
    def test_exact_snapshot_authorization_passes(self):
        self.auth(); self.assertEqual([],runner.exact_snapshot_authorization_gate(self.plan)); self.assertEqual([self.item],self.plan["snapshot_candidates"]); self.assertTrue(self.plan["actionable"])
    def test_snapshot_authorization_fails_on_candidate_review_or_basis_drift(self):
        self.auth(candidate_sha256="0"*64)
        with self.assertRaises(runner.RunnerError): runner.exact_snapshot_authorization_gate(self.plan)
        self.plan["snapshot_candidates"]=[dict(self.item)]; self.auth(review_record_sha256="0"*64)
        with self.assertRaises(runner.RunnerError): runner.exact_snapshot_authorization_gate(self.plan)
        self.plan["snapshot_candidates"]=[dict(self.item)]; self.auth(); (self.root/"docs/review.md").write_text("changed\n")
        with self.assertRaises(runner.RunnerError): runner.exact_snapshot_authorization_gate(self.plan)
    def test_branch_name_binds_full_source_and_base(self):
        source="a"*40; base="b"*40; self.assertEqual(f"automation/living-promotion-{source}-{base}",runner.branch_name(source,base))
    def test_promotion_pr_is_created_and_read_only_with_the_promotion_app_token(self):
        calls=[]
        def fake_run(*args,check=True,capture=True,env=None):
            calls.append((args,env))
            stdout={"list":"","create":"https://github.com/o/r/pull/7\n","view":"7\n"}.get(args[2] if args[0]=="gh" else "","")
            return subprocess.CompletedProcess(list(args),0,stdout,"")
        plan_path=self.root/"plan.json"
        with mock.patch.object(runner,"run",fake_run), mock.patch.dict(os.environ,{"GITHUB_REPOSITORY":"o/r","GH_TOKEN":"actions-token"}):
            self.assertEqual((7,True),runner.create_or_recover_pr("automation/living-promotion-x",plan_path,"app-token"))
        gh_calls=[(args,env) for args,env in calls if args[0]=="gh"]
        self.assertEqual(["list","create","view"],[args[2] for args,_ in gh_calls])
        self.assertTrue(all(env is not None and env["GH_TOKEN"]=="app-token" for _,env in gh_calls))
    def test_runner_fails_closed_without_the_promotion_app_token_before_any_subprocess(self):
        def forbidden(*args,**kwargs): raise AssertionError(f"subprocess ran: {args}")
        with mock.patch.object(runner,"run",forbidden), mock.patch.dict(os.environ,{"GITHUB_REPOSITORY":"o/r","GH_TOKEN":"actions-token"}):
            os.environ.pop(runner.PR_TOKEN_ENV,None)
            with self.assertRaisesRegex(runner.RunnerError,runner.PR_TOKEN_ENV): runner.main()
    def test_runner_removes_the_promotion_app_token_from_the_environment_before_any_subprocess(self):
        seen=[]
        def stop(): seen.append(os.environ.get(runner.PR_TOKEN_ENV)); raise runner.RunnerError("stop")
        with mock.patch.object(runner,"source_snapshot",stop), mock.patch.dict(os.environ,{"GITHUB_REPOSITORY":"o/r","GH_TOKEN":"actions-token",runner.PR_TOKEN_ENV:"app-token"}):
            with self.assertRaisesRegex(runner.RunnerError,"stop"): runner.main()
        self.assertEqual([None],seen)
    def test_forbidden_prefix_gate_rejects_governance_and_living_targets(self):
        self.empty_auth()
        for target in ("docs/governance/x.md","research/living/x.json"):
            plan={"canonical_proposals":[{"operations":[{"path":target}]}]}
            with self.assertRaises(runner.RunnerError): runner.forbidden_target_gate(plan)

if __name__=="__main__": unittest.main()
