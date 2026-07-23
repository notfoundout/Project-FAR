from __future__ import annotations

import importlib.util
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODEL = ROOT / "theory/foundation/upp_foundation_v1.py"


def load_model():
    spec = importlib.util.spec_from_file_location("upp_foundation_v1_test", MODEL)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class UPPW1FoundationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.m = load_model()

    def valid_system(self):
        m = self.m
        c1 = m.Commitment("c1", "claim:a", "agent", 0)
        c2 = m.Commitment("c2", "claim:b", "agent", 1)
        s0 = m.State("s0", 0, frozenset({"c1"}))
        s1 = m.State("s1", 1, frozenset({"c1", "c2"}))
        fact = m.ReasoningFact("f1", "conclusion", "claim:b", 1, True)
        transition = m.Transition("t1", "s0", "s1", m.TransitionStatus.ADMISSIBLE, frozenset({"c1"}))
        dependency = m.Dependency("c1", "f1", "support", 1)
        event = m.HistoryEvent("h1", 1, "commitment_added", "s0", "s1", frozenset({"c1"}))
        observation = m.Observation("o1", "query:current", "claim:b", 1)
        return m.ReasoningSystem(
            "sys",
            (s0, s1),
            (transition,),
            (c1, c2),
            (dependency,),
            (event,),
            (fact,),
            (observation,),
        )

    def test_checker_passes(self) -> None:
        cp = subprocess.run(
            [sys.executable, str(ROOT / "tools/check_upp_w1_foundation.py")],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        self.assertEqual(cp.returncode, 0, cp.stdout + cp.stderr)
        self.assertIn("PASS", cp.stdout)

    def test_valid_system(self) -> None:
        self.assertEqual(self.valid_system().validate(), ())

    def test_missing_commitment_reference_fails(self) -> None:
        m = self.m
        system = m.ReasoningSystem(
            "sys",
            (m.State("s0", 0, frozenset({"missing"})),),
            (), (), (), (), (), (),
        )
        self.assertTrue(any("missing commitments" in error for error in system.validate()))

    def test_dependency_endpoint_must_resolve(self) -> None:
        m = self.m
        system = self.valid_system()
        broken = m.ReasoningSystem(
            system.id,
            system.states,
            system.transitions,
            system.commitments,
            (m.Dependency("missing", "f1", "support", 0),),
            system.history,
            system.reasoning_facts,
            system.observations,
        )
        self.assertTrue(any("dependency endpoints" in error for error in broken.validate()))

    def test_history_order_is_checked(self) -> None:
        m = self.m
        system = self.valid_system()
        later = m.HistoryEvent("h2", 2, "later", "s0", "s1", frozenset())
        earlier = m.HistoryEvent("h3", 1, "earlier", "s0", "s1", frozenset())
        broken = m.ReasoningSystem(
            system.id,
            system.states,
            system.transitions,
            system.commitments,
            system.dependencies,
            (later, earlier),
            system.reasoning_facts,
            system.observations,
        )
        self.assertIn("history must be stored in nondecreasing time order", broken.validate())

    def test_unknown_recovery_is_distinct(self) -> None:
        m = self.m
        witness = m.RecoveryWitness("f1", "r1", "p1", m.RecoveryStatus.UNKNOWN, None, None)
        self.assertEqual(witness.validate(), ())
        self.assertNotEqual(m.RecoveryStatus.UNKNOWN, m.RecoveryStatus.RECOVERED)
        self.assertNotEqual(m.RecoveryStatus.UNKNOWN, m.RecoveryStatus.NOT_RECOVERED)

    def test_recovered_witness_requires_output(self) -> None:
        m = self.m
        witness = m.RecoveryWitness("f1", "r1", "p1", m.RecoveryStatus.RECOVERED, None, 3)
        self.assertIn("recovered witness requires output_key", witness.validate())

    def test_duplicate_global_identity_fails(self) -> None:
        m = self.m
        c = m.Commitment("same", "claim:a", "agent", 0)
        s = m.State("same", 0, frozenset())
        system = m.ReasoningSystem("sys", (s,), (), (c,), (), (), (), ())
        self.assertTrue(any("duplicate id" in error for error in system.validate()))

    def test_assumption_taxonomy_is_frozen(self) -> None:
        self.assertEqual(
            {x.value for x in self.m.AssumptionKind},
            {"definitional", "logical", "computational", "normative", "empirical", "methodological"},
        )

    def test_foundation_does_not_assert_rccd(self) -> None:
        prohibited = self.m.RCCD_TERMS_PROHIBITED_IN_CLASS_DEFINITION
        self.assertIn("RCCD", prohibited)
        self.assertIn("uniform effective recovery", prohibited)


if __name__ == "__main__":
    unittest.main()
