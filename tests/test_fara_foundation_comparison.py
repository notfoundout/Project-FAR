import copy
import importlib
import json
import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT)); sys.path.insert(0, str(ROOT / "tools"))
import check_fara_foundation_comparison as checker
from theory.foundation.fara_foundation_comparison.translation import execute_source, source_model, translate
from theory.foundation.fara_foundation_comparison.reconstruction import compare, reconstruct


class FoundationComparisonTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.spec = json.loads(checker.SPEC.read_text())
        cls.proof = json.loads(checker.PROOF.read_text())

    def rejected(self, mutator, proof=False):
        spec = copy.deepcopy(self.spec); artifact = copy.deepcopy(self.proof)
        mutator(artifact if proof else spec)
        self.assertTrue(checker.validate(spec, artifact), "mutation was accepted")

    def test_fresh_build_report_and_disk_traces_are_exact(self):
        fresh = checker.build(copy.deepcopy(self.spec))
        self.assertEqual(self.proof, fresh)
        self.assertEqual(checker.REPORT.read_text(), checker.render(self.spec, fresh))
        disk = {path.stem: json.loads(path.read_text()) for path in checker.TRACE_DIR.glob("*.json")}
        self.assertEqual(fresh["traces"], disk)

    def test_three_modules_execute_independently(self):
        modules = [importlib.import_module(foundation["module"]) for foundation in self.spec["foundations"]]
        self.assertEqual(3, len({pathlib.Path(module.__file__).read_bytes() for module in modules}))
        self.assertFalse(any("many_sorted" in pathlib.Path(module.__file__).read_text() for module in modules[1:]))

    def test_each_finite_benchmark_has_a_distinct_executable_target(self):
        for foundation in self.spec["foundations"]:
            targets = []
            for benchmark in self.spec["benchmarks"][:16]:
                trace = self.proof["traces"][f"{foundation['name']}--{benchmark['id']}"]
                self.assertEqual("Pass", trace["candidate_execution"]["status"])
                targets.append(json.dumps(trace["target_model"], sort_keys=True))
            self.assertEqual(16, len(set(targets)))

    def test_preservation_is_recomputed_from_reconstruction(self):
        benchmark = self.spec["benchmarks"][8]
        foundation = self.spec["foundations"][0]
        module = importlib.import_module(foundation["module"])
        translated = translate(benchmark, foundation["name"])
        execution = module.execute(translated["target_model"])
        reconstructed = reconstruct(translated["source_model"], translated, execution)
        comparison = compare(translated["source_model"], reconstructed, execute_source(translated["source_model"]))
        self.assertEqual("Fail", comparison["preservation"]["structural"])
        self.assertFalse(comparison["result_equivalent"])

    def test_many_sorted_transition_execution_reaches_fixed_point_independent_of_order(self):
        module = importlib.import_module("theory.foundation.fara_foundation_comparison.many_sorted")
        model = {
            "candidate": "many-sorted-relational",
            "initial": {"states": ["s0"]},
            "rules": [
                {"id": "later", "opcode": "transition", "arguments": {"source": "s1", "target": "s2"}},
                {"id": "first", "opcode": "transition", "arguments": {"source": "s0", "target": "s1"}},
            ],
            "semantic_relations": {}, "dependency_relations": [], "information_relations": {}, "history_relations": [],
        }
        self.assertEqual(["s0", "s1", "s2"], module.execute(model)["state"]["states"])
        model["rules"].reverse()
        self.assertEqual(["s0", "s1", "s2"], module.execute(model)["state"]["states"])

    def test_ablations_are_execution_derived(self):
        self.assertEqual(21, len(self.proof["ablations"]))
        for ablation in self.proof["ablations"]:
            self.assertEqual(16, len(ablation["executions"]))
            observed = [row["benchmark"] for row in ablation["executions"] if row["loss_observed"]]
            self.assertEqual(observed, ablation["fails"])
            self.assertEqual(sum(row["structural_saving"] for row in ablation["executions"]), ablation["structural_saving"])
            self.assertEqual(bool(observed), ablation["expressive_loss"])

    def test_pareto_failure_dimensions_are_measured_from_traces(self):
        for foundation, vector in self.proof["pareto_vectors"].items():
            rows = [trace for trace in self.proof["traces"].values() if trace["foundation"] == foundation]
            self.assertEqual(-sum(row["preservation"]["structural"] == "Fail" for row in rows), vector["identity_failures"])
            self.assertEqual(-sum(row["preservation"]["semantic"] == "Fail" for row in rows), vector["semantic_failures"])
            self.assertEqual(-sum(row["preservation"]["historical"] == "Fail" for row in rows), vector["historical_failures"])
            operational = -sum(row["preservation"]["operational"] == "Fail" or not row["comparison"]["result_equivalent"] for row in rows if row["status"] != "Unknown")
            self.assertEqual(operational, vector["operational_failures"])

    def test_unknown_is_not_promoted(self):
        self.assertTrue(all(row["status"] == "Unknown" for row in self.proof["results"] if row["benchmark"] in ("BFC-017", "BFC-018", "BFC-019")))

    def test_spec_mutations_fail_closed(self):
        mutations = [
            lambda spec: spec["foundations"][0]["sorts"].append("Undeclared"),
            lambda spec: spec["foundations"][0]["native_symbols"].append("bad"),
            lambda spec: spec["foundations"][0].pop("admissible_models"),
            lambda spec: spec["foundations"].__setitem__(1, {**spec["foundations"][1], "module": spec["foundations"][0]["module"]}),
            lambda spec: spec["benchmarks"].pop(),
            lambda spec: spec["preservation_dimensions"].pop(),
            lambda spec: spec.__setitem__("weights", [1]),
            lambda spec: spec["campaign"]["pr421_artifact_hashes"].__setitem__("proof", "0" * 40),
            lambda spec: spec["nonclaims"].pop(),
            lambda spec: spec["remaining_obligations"].pop(),
            lambda spec: spec["benchmarks"][1].__setitem__("id", spec["benchmarks"][0]["id"]),
            lambda spec: spec["foundations"][0].__setitem__("arbitrary_payload_renamed", "opaque semantic blob"),
            lambda spec: spec["foundations"][1].__setitem__("decoding_service", "hidden_decoder"),
            lambda spec: spec["comparison_dimensions"].pop(),
            lambda spec: spec["terminal_vocabulary"].pop(),
            lambda spec: spec["benchmarks"][0].__setitem__("expected_answer", "Pass"),
        ]
        for mutation in mutations: self.rejected(mutation)

    def test_proof_mutations_fail_closed(self):
        first = next(iter(self.proof["traces"]))
        mutations = [
            lambda proof: proof["results"][0].__setitem__("status", "Fail"),
            lambda proof: proof["traces"][first]["execution_steps"].pop(),
            lambda proof: proof["traces"][first]["correspondence_map"].clear(),
            lambda proof: proof["traces"][first]["recovered_commitments"].clear(),
            lambda proof: proof["results"][0].__setitem__("commitment_equivalent", False),
            lambda proof: proof["non_equivalence_witnesses"].pop(),
            lambda proof: proof["non_equivalence_witnesses"][0].pop("models"),
            lambda proof: proof["structural_accounting"]["many-sorted-relational"]["aggregate"].__setitem__("native", 0),
            lambda proof: proof["results"][-1].__setitem__("status", "Pass"),
            lambda proof: proof["pareto_matrix"]["many-sorted-relational"].__setitem__("typed-hypergraph", True),
            lambda proof: proof["ablations"].pop(),
            lambda proof: proof["counterexamples"].pop(),
            lambda proof: proof["traces"][first]["target_model"].clear(),
        ]
        for mutation in mutations: self.rejected(mutation, proof=True)

    def test_human_and_generated_reports_are_distinct(self):
        human = ROOT / "docs/research/fara-foundation-comparison-v1.0.md"
        if human.exists(): self.assertNotEqual(human.read_text(), checker.REPORT.read_text())


if __name__ == "__main__": unittest.main()
