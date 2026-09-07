import json, shutil, subprocess, sys, tempfile, unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PKG=ROOT/'docs/research/external-falsification-and-replication/external-handoff-v1.0'

def run_verify(pkg):
    return subprocess.run([sys.executable,str(pkg/'verify_packet.py')],cwd=pkg,text=True,capture_output=True)

def rehash(pkg, rel='packet.json'):
    import hashlib
    m=json.loads((pkg/'MANIFEST.json').read_text(encoding='utf-8'))
    m['files'][rel]=hashlib.sha256((pkg/rel).read_bytes()).hexdigest()
    (pkg/'MANIFEST.json').write_text(json.dumps(m,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')

class EFRExternalHandoffTests(unittest.TestCase):
    def test_frozen_package_verifies(self):
        p=run_verify(PKG); self.assertEqual(p.returncode,0,p.stdout+p.stderr); self.assertIn('VALID PACKET',p.stdout)

    def mutate(self, fn):
        td=tempfile.TemporaryDirectory(); self.addCleanup(td.cleanup)
        dst=Path(td.name)/'pkg'; shutil.copytree(PKG,dst)
        data=json.loads((dst/'packet.json').read_text(encoding='utf-8')); fn(data)
        (dst/'packet.json').write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n',encoding='utf-8'); rehash(dst)
        return run_verify(dst)

    def test_rejects_decoder_domain_drift(self):
        p=self.mutate(lambda d:d['common_definitions'].__setitem__('exact_decoder_domain','d:R→V^T'))
        self.assertNotEqual(p.returncode,0); self.assertIn('decoder domain',p.stdout)

    def test_rejects_far_core_010_dependency_drift(self):
        p=self.mutate(lambda d:d['far_core_010_dependency'].__setitem__('depends_on',['L','J','I','Γ']))
        self.assertNotEqual(p.returncode,0); self.assertIn('FAR-CORE-010',p.stdout)

    def test_rejects_far_core_014_missing_bounded_surface(self):
        p=self.mutate(lambda d:d['far_core_014_bounded_definitions']['decoder_class']['members'].pop('NONEMPTY'))
        self.assertNotEqual(p.returncode,0); self.assertIn('FAR-CORE-014 decoder class',p.stdout)

    def test_rejects_pr453_promoted_to_authority(self):
        p=self.mutate(lambda d:d['far_core_014_bounded_definitions']['authority'].__setitem__('path','PR #453'))
        self.assertNotEqual(p.returncode,0); self.assertIn('authoritative source lock',p.stdout)

    def test_rejects_efr_execution_promotion(self):
        p=self.mutate(lambda d:d['execution_status'].__setitem__('efr_executed',True))
        self.assertNotEqual(p.returncode,0); self.assertIn('execution/nonclaim',p.stdout)

    def test_rejects_claim_binding_drift(self):
        p=self.mutate(lambda d:d['claims'][13].__setitem__('status','proved'))
        self.assertNotEqual(p.returncode,0); self.assertIn('14/14',p.stdout)

if __name__=='__main__': unittest.main()
