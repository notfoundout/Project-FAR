import copy, json, pathlib, subprocess, tempfile, unittest

from tools.check_fara_vocabulary_sufficiency import OBJECT, REPORT, build, render, validate

class VocabularyCampaignTests(unittest.TestCase):
    def setUp(self): self.base=build()
    def reject(self, mutate):
        o=copy.deepcopy(self.base); mutate(o); self.assertTrue(validate(o))
    def test_canonical_artifacts_fresh(self):
        disk=json.loads(OBJECT.read_text()); self.assertEqual([],validate(disk)); self.assertEqual(REPORT.read_text(),render(disk))
    def test_broader_catchall(self): self.reject(lambda o:o["frozen_vocabulary"]["candidate_primitives"].append("Payload"))
    def test_remove_primitive(self): self.reject(lambda o:o["frozen_vocabulary"]["candidate_primitives"].pop())
    def test_remove_family(self): self.reject(lambda o:o["benchmarks"].pop())
    def test_duplicate_benchmark(self): self.reject(lambda o:o["benchmarks"].__setitem__(1,dict(o["benchmarks"][1],id=o["benchmarks"][0]["id"])))
    def test_prose_fixture(self): self.reject(lambda o:o["benchmarks"][0].__setitem__("fixture_kind","prose"))
    def test_failure_changed_to_pass(self): self.reject(lambda o:o["benchmarks"][1]["preservation"].update({k:"Pass" for k in o["benchmarks"][1]["preservation"]}))
    def test_opaque_entire_source(self): self.reject(lambda o:(o["benchmarks"][0]["structural_accounting"].__setitem__("opaque_content",1),o["benchmarks"][0].__setitem__("recovery","exact")))
    def test_semantics_in_interpretation(self): self.reject(lambda o:o["escape_hatch_mutations"][3].__setitem__("result","accepted"))
    def test_embedded_interpreter(self): self.reject(lambda o:o["benchmarks"][0]["structural_accounting"].__setitem__("hidden_machinery",1))
    def test_missing_dimension(self): self.reject(lambda o:o["benchmarks"][0]["preservation"].pop("semantic"))
    def test_invalid_status(self): self.reject(lambda o:o["benchmarks"][0]["preservation"].__setitem__("semantic","Maybe"))
    def test_exact_when_execution_fails(self): self.reject(lambda o:o["benchmarks"][1].__setitem__("recovery","exact"))
    def test_failed_when_execution_succeeds(self): self.reject(lambda o:o["benchmarks"][0].__setitem__("recovery","failed"))
    def test_irreducible_without_attempt(self): self.reject(lambda o:o["extension_candidates"][1]["derivation_attempt"].__setitem__("executed",False))
    def test_ablation_without_alternative(self): self.reject(lambda o:o["ablations"][0].__setitem__("alternative_encoding_attempt",""))
    def test_universal_promotion(self): self.reject(lambda o:o.__setitem__("status","universal sufficiency"))
    def test_global_minimality(self): self.reject(lambda o:o["ablations"][0].__setitem__("global_necessity",True))
    def test_same_length_obligation_replacement(self): self.reject(lambda o:o["remaining_obligations"].__setitem__(0,"x"*len(o["remaining_obligations"][0])))
    def test_compact_duplicate_owner(self): self.reject(lambda o:o.__setitem__("compact",{"id":"FARA-VOC-001"}))
    def test_omitted_counterexample(self): self.reject(lambda o:o["counterexamples"].pop())
    def test_extension_classification(self): self.reject(lambda o:o["extension_candidates"][1].__setitem__("classification","derivable"))
    def test_stale_report_cli(self):
        with tempfile.TemporaryDirectory() as d:
            p=pathlib.Path(d)/"o.json"; p.write_text(json.dumps(self.base))
            self.assertEqual(0,subprocess.run(["python","tools/check_fara_vocabulary_sufficiency.py","--object",str(p)],capture_output=True).returncode)

if __name__=="__main__": unittest.main()
