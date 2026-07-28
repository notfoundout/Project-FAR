import copy, json, unittest

from tools.check_fara_vocabulary_sufficiency import OBJECT, REPORT, build, render, run, fixture, validate


class VocabularyCampaignTests(unittest.TestCase):
    def setUp(self):
        self.base = build()

    def reject(self, mutate):
        candidate = copy.deepcopy(self.base)
        mutate(candidate)
        self.assertTrue(validate(candidate))

    def test_canonical_artifacts_match_fresh_build(self):
        disk = json.loads(OBJECT.read_text())
        self.assertEqual(build(), disk)
        self.assertEqual([], validate(disk))
        self.assertEqual(render(build()), REPORT.read_text())

    def test_registered_families_execute_distinct_behaviors(self):
        probability = run(fixture('probabilistic_update'), True)
        causal = run(fixture('causal_intervention'), True)
        proof = run(fixture('proof_identity_binding'), True)
        self.assertNotEqual(probability, causal)
        self.assertNotEqual(causal, proof)
        self.assertEqual([[3, 11], [8, 11]], probability['result'])
        self.assertEqual(0, causal['result'])
        self.assertEqual(2, proof['result'])

    def test_reduced_execution_exposes_pressure(self):
        for family in ('probabilistic_update', 'causal_intervention', 'distributed_partial_order', 'proof_identity_binding'):
            source = fixture(family)
            self.assertNotEqual(run(source, True), run(source, False))

    def test_unknown_external_cases_remain_unavailable(self):
        for family in ('oracle_behavior', 'continuous_hybrid', 'embodied_tacit'):
            self.assertFalse(run(fixture(family), True)['available'])

    def test_rejects_broader_catchall(self):
        self.reject(lambda o: o['vocabulary']['primitives'].append('Payload'))

    def test_rejects_removed_family(self):
        self.reject(lambda o: o['benchmarks'].pop())

    def test_rejects_duplicate_benchmark(self):
        self.reject(lambda o: o['benchmarks'].__setitem__(1, dict(o['benchmarks'][1], id=o['benchmarks'][0]['id'])))

    def test_rejects_changed_execution(self):
        self.reject(lambda o: o['benchmarks'][1]['full_execution'].__setitem__('result', [1, 2]))

    def test_rejects_promoted_failure(self):
        self.reject(lambda o: o['benchmarks'][1].__setitem__('recovery', 'exact'))

    def test_rejects_missing_dimension(self):
        self.reject(lambda o: o['benchmarks'][0]['preservation'].pop('semantic'))

    def test_rejects_extension_promotion(self):
        self.reject(lambda o: o['extensions'][1].__setitem__('global_primitive', True))

    def test_rejects_global_necessity(self):
        self.reject(lambda o: o['ablations'][0].__setitem__('global_necessity', True))

    def test_rejects_changed_obligation(self):
        self.reject(lambda o: o['remaining_obligations'].__setitem__(0, 'x' * len(o['remaining_obligations'][0])))

    def test_rejects_omitted_counterexample(self):
        self.reject(lambda o: o['counterexamples'].pop())

    def test_rejects_duplicate_owner(self):
        self.reject(lambda o: o.__setitem__('duplicate', {'id': 'FARA-VOC-001'}))


if __name__ == '__main__':
    unittest.main()
