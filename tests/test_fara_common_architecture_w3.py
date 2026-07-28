import copy, importlib.util, json, pathlib, unittest
ROOT=pathlib.Path(__file__).resolve().parents[1]
SPEC=importlib.util.spec_from_file_location("w3",ROOT/"tools/check_fara_common_architecture_w3.py")
W3=importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(W3)
DATA=json.loads((ROOT/"theory/evaluation/fara-w3-common-architecture-v1.0.json").read_text())
class FaraCommonArchitectureW3Tests(unittest.TestCase):
    def test_canonical_object_passes(self): self.assertEqual([],W3.validate(DATA))
    def mutate(self,fn): bad=copy.deepcopy(DATA); fn(bad); self.assertTrue(W3.validate(bad))
    def test_scope_expansion_detected(self): self.mutate(lambda d:d["proposition"].__setitem__("system_class","all reasoning systems"))
    def test_omitted_failure_detected(self): self.mutate(lambda d:d["family_results"][6].__setitem__("loss_failure_ambiguity",""))
    def test_hidden_machinery_detected(self): self.mutate(lambda d:d["family_results"][4].__setitem__("added_machinery",[]))
    def test_preservation_overclaim_detected(self):
        def change(d):
            x=d["family_results"][-1]; x["preservation"]={k:"preserved" for k in W3.DIMENSIONS}
        self.mutate(change)
    def test_bounded_to_universal_promotion_detected(self): self.mutate(lambda d:d["adjudication"].__setitem__("strongest_established","universal architecture established"))
    def test_family_omission_detected(self): self.mutate(lambda d:d["family_results"].pop())
    def test_dimension_omission_detected(self): self.mutate(lambda d:d["family_results"][0]["preservation"].pop("historical"))
    def test_countermodel_search_omission_detected(self): self.mutate(lambda d:d["family_results"][8].__setitem__("countermodel_search",""))
    def test_necessity_promotion_detected(self): self.mutate(lambda d:d["proposition"]["separated_claims"].__setitem__("necessity","necessity established"))
    def test_obligation_weakening_detected(self): self.mutate(lambda d:d["remaining_obligations"].pop())
if __name__=="__main__": unittest.main()
