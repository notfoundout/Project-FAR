import copy, importlib.util, json, pathlib, unittest
ROOT=pathlib.Path(__file__).resolve().parents[1]
SPEC=importlib.util.spec_from_file_location("w3",ROOT/"tools/check_fara_common_architecture_w3.py")
W3=importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(W3)
DATA=json.loads((ROOT/"theory/evaluation/fara-w3-common-architecture-v1.0.json").read_text())
class FaraCommonArchitectureW3Tests(unittest.TestCase):
    def test_canonical_object_passes(self): self.assertEqual([],W3.validate(DATA))
    def mutate(self,fn): bad=copy.deepcopy(DATA); fn(bad); self.assertTrue(W3.validate(bad))
    def test_scope_expansion_detected(self): self.mutate(lambda d:d["proposition"].__setitem__("system_class","all reasoning systems"))
    def test_embedded_scope_expansion_detected(self): self.mutate(lambda d:d["proposition"].__setitem__("system_class","C_W3 contains all reasoning systems; exactly the ten named specimens are examples"))
    def test_omitted_failure_detected(self): self.mutate(lambda d:d["family_results"][6].__setitem__("loss_failure_ambiguity",""))
    def test_hidden_machinery_detected(self): self.mutate(lambda d:d["family_results"][4].__setitem__("added_machinery",[]))
    def test_preservation_overclaim_detected(self):
        def change(d):
            x=d["family_results"][-1]; x["preservation"]={k:"preserved" for k in W3.DIMENSIONS}
        self.mutate(change)
    def test_unresolved_family_promotion_detected(self):
        def change(d): d["family_results"][5]["preservation"]={k:"preserved" for k in W3.DIMENSIONS}
        self.mutate(change)
    def test_invalid_preservation_vocabulary_detected(self): self.mutate(lambda d:d["family_results"][5]["preservation"].__setitem__("semantic","Pass"))
    def test_bounded_to_universal_promotion_detected(self): self.mutate(lambda d:d["adjudication"].__setitem__("strongest_established","universal architecture established"))
    def test_family_omission_detected(self): self.mutate(lambda d:d["family_results"].pop())
    def test_dimension_omission_detected(self): self.mutate(lambda d:d["family_results"][0]["preservation"].pop("historical"))
    def test_countermodel_search_omission_detected(self): self.mutate(lambda d:d["family_results"][8].__setitem__("countermodel_search",""))
    def test_necessity_promotion_detected(self): self.mutate(lambda d:d["proposition"]["separated_claims"].__setitem__("necessity","necessity established"))
    def test_uniqueness_promotion_detected(self): self.mutate(lambda d:d["proposition"]["separated_claims"].__setitem__("uniqueness","unique architecture established"))
    def test_existential_claim_drift_detected(self): self.mutate(lambda d:d["proposition"]["separated_claims"].__setitem__("existential_common_structure","globally established"))
    def test_reconstruction_claim_drift_detected(self): self.mutate(lambda d:d["proposition"]["separated_claims"].__setitem__("representational_reconstruction","established for all ten"))
    def test_obligation_weakening_detected(self): self.mutate(lambda d:d["remaining_obligations"].pop())
    def test_obligation_content_replacement_detected(self): self.mutate(lambda d:d.__setitem__("remaining_obligations",["arbitrary"]*7))
if __name__=="__main__": unittest.main()
