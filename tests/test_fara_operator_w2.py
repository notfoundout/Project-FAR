import copy, importlib.util, json, pathlib, unittest
ROOT=pathlib.Path(__file__).resolve().parents[1]
SPEC=importlib.util.spec_from_file_location("w2", ROOT/"tools/check_fara_operator_w2.py")
W2=importlib.util.module_from_spec(SPEC); SPEC.loader.exec_module(W2)
DATA=json.loads((ROOT/"theory/evaluation/fara-operator-w2-proof-v1.0.json").read_text())
class FaraOperatorW2Tests(unittest.TestCase):
    def test_canonical_proof_object_passes(self): self.assertEqual([], W2.validate(DATA))
    def test_all_eliminations_and_witnesses_are_registered(self):
        self.assertEqual(7,len(DATA["elimination_subsets_tested"])); self.assertEqual({"Construct","Differentiate","Restrict"},{w["requires"] for w in DATA["witnesses"]})
    def test_adversarial_operator_duplication_fails(self):
        bad=copy.deepcopy(DATA); bad["operators"][1]["coordinate"]="R"; self.assertTrue(W2.validate(bad))
    def test_adversarial_missing_elimination_fails(self):
        bad=copy.deepcopy(DATA); bad["elimination_subsets_tested"].pop(); self.assertTrue(W2.validate(bad))
    def test_adversarial_false_global_promotion_fails(self):
        for field, value in (("global_claim","established"),("status","global_minimality_established"),("strongest_claim","global minimality")):
            bad=copy.deepcopy(DATA); bad[field]=value; self.assertTrue(W2.validate(bad), field)
    def test_adversarial_bounded_claim_promotion_fails(self):
        bad=copy.deepcopy(DATA); bad["bounded_model"]["claim"]="Construct, Differentiate, and Restrict are globally minimal."; self.assertTrue(W2.validate(bad))
    def test_adversarial_model_name_drift_fails(self):
        bad=copy.deepcopy(DATA); bad["bounded_model"]["name"]="global_reasoning"; self.assertTrue(W2.validate(bad))
    def test_adversarial_authority_redefinition_fails(self):
        bad=copy.deepcopy(DATA); bad["authority"]["operators"]["Construct"]="Create anything."; self.assertTrue(W2.validate(bad))
    def test_required_nonclaims_and_obligations_are_pinned(self):
        bad=copy.deepcopy(DATA); bad["nonclaims"].pop(); self.assertTrue(W2.validate(bad))
        bad=copy.deepcopy(DATA); bad["remaining_obligations"].pop(); self.assertTrue(W2.validate(bad))
    def test_historical_resolve_and_select_classifications_are_preserved(self):
        actual={c["name"]:c["classification"] for c in DATA["fourth_candidates"]}
        self.assertEqual("outside_scope_unresolved",actual["Resolve"])
        self.assertEqual("outside_scope_unresolved",actual["Select"])
        rendered=W2.render(DATA)
        self.assertIn("Resolve is derived rule application",rendered)
        self.assertIn("global finite-basis search is closed",rendered)
    def test_fourth_search_retains_counterexample_and_unknowns(self):
        classes={c["classification"] for c in DATA["fourth_candidates"]}; self.assertIn("outside_scope_counterexample",classes); self.assertIn("outside_scope_unresolved",classes)
if __name__=="__main__": unittest.main()
