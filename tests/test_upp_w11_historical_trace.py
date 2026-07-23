from __future__ import annotations

import importlib.util
import pathlib
import subprocess
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
PATH = ROOT / "theory" / "history" / "upp_historical_trace_v1.py"
SPEC = importlib.util.spec_from_file_location("upp_historical_trace_v1", PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)

Evidence = MODULE.Evidence
Verdict = MODULE.Verdict
EventKind = MODULE.EventKind
TraceEvent = MODULE.TraceEvent
HistoricalTraceWitness = MODULE.HistoricalTraceWitness
HistoricalTraceTheoremCase = MODULE.HistoricalTraceTheoremCase


def valid_witness(**overrides):
    e0 = TraceEvent("e0", EventKind.ASSERT, 0, "p", frozenset(), frozenset(), frozenset(), frozenset())
    e1 = TraceEvent("e1", EventKind.DERIVE, 1, "q", frozenset({"e0"}), frozenset({"e0"}), frozenset({"e0"}), frozenset())
    values = dict(
        events=(e0, e1),
        effective_recovery=Evidence.TRUE,
        event_identity_stable=Evidence.TRUE,
        temporal_order_total_for_registered_events=Evidence.TRUE,
        predecessor_links_complete=Evidence.TRUE,
        dependency_lineage_complete=Evidence.TRUE,
        revision_lineage_complete=Evidence.TRUE,
        reasons_recoverable=Evidence.TRUE,
        rollback_or_replay_fidelity=Evidence.TRUE,
        equivalence_invariant=Evidence.TRUE,
        machinery_fully_accounted=Evidence.TRUE,
        registered_queries_total=Evidence.TRUE,
        failure_unknown_separated=Evidence.TRUE,
    )
    values.update(overrides)
    return HistoricalTraceWitness(**values)


def valid_case(**overrides):
    values = dict(
        target_class_member=Evidence.TRUE,
        admissible_representation=Evidence.TRUE,
        machinery_closed=Evidence.TRUE,
        fully_faithful=Evidence.TRUE,
        commitment_equivalence_preserved=Evidence.TRUE,
        history_sensitive_behavior=Evidence.TRUE,
        registered_history_queries_total=Evidence.TRUE,
        witness=valid_witness(),
    )
    values.update(overrides)
    return HistoricalTraceTheoremCase(**values)


class HistoricalTraceTests(unittest.TestCase):
    def test_valid_case_proves(self):
        self.assertEqual(valid_case().evaluate(), Verdict.PROVED)

    def test_false_antecedent_refutes(self):
        self.assertEqual(valid_case(fully_faithful=Evidence.FALSE).evaluate(), Verdict.REFUTED)

    def test_unknown_is_not_promoted(self):
        self.assertEqual(valid_case(history_sensitive_behavior=Evidence.UNKNOWN).evaluate(), Verdict.UNKNOWN)

    def test_final_snapshot_is_not_history(self):
        event = TraceEvent("e0", EventKind.ASSERT, 0, "p")
        self.assertEqual(valid_case(witness=valid_witness(events=(event,))).evaluate(), Verdict.REFUTED)

    def test_duplicate_event_identity_refutes(self):
        e0 = TraceEvent("x", EventKind.ASSERT, 0, "p")
        e1 = TraceEvent("x", EventKind.DERIVE, 1, "q", frozenset({"x"}))
        self.assertEqual(valid_case(witness=valid_witness(events=(e0, e1))).evaluate(), Verdict.REFUTED)

    def test_dangling_reference_refutes(self):
        e0 = TraceEvent("e0", EventKind.ASSERT, 0, "p")
        e1 = TraceEvent("e1", EventKind.DERIVE, 1, "q", frozenset({"missing"}))
        self.assertEqual(valid_case(witness=valid_witness(events=(e0, e1))).evaluate(), Verdict.REFUTED)

    def test_backward_predecessor_refutes(self):
        e0 = TraceEvent("e0", EventKind.ASSERT, 2, "p")
        e1 = TraceEvent("e1", EventKind.DERIVE, 1, "q", frozenset({"e0"}))
        self.assertEqual(valid_case(witness=valid_witness(events=(e0, e1))).evaluate(), Verdict.REFUTED)

    def test_hidden_log_refutes(self):
        witness = valid_witness(machinery_fully_accounted=Evidence.FALSE)
        self.assertEqual(valid_case(witness=witness).evaluate(), Verdict.REFUTED)

    def test_unresolved_rollback_remains_unknown(self):
        witness = valid_witness(rollback_or_replay_fidelity=Evidence.UNKNOWN)
        self.assertEqual(valid_case(witness=witness).evaluate(), Verdict.UNKNOWN)

    def test_unknown_history_not_collapsed(self):
        witness = valid_witness(failure_unknown_separated=Evidence.FALSE)
        self.assertEqual(valid_case(witness=witness).evaluate(), Verdict.REFUTED)

    def test_equivalence_instability_refutes(self):
        witness = valid_witness(equivalence_invariant=Evidence.FALSE)
        self.assertEqual(valid_case(witness=witness).evaluate(), Verdict.REFUTED)

    def test_revision_requires_lineage(self):
        witness = valid_witness(revision_lineage_complete=Evidence.FALSE)
        self.assertEqual(valid_case(witness=witness).evaluate(), Verdict.REFUTED)

    def test_each_witness_evidence_is_required(self):
        names = [
            "effective_recovery", "event_identity_stable",
            "temporal_order_total_for_registered_events", "predecessor_links_complete",
            "dependency_lineage_complete", "revision_lineage_complete",
            "reasons_recoverable", "rollback_or_replay_fidelity",
            "equivalence_invariant", "machinery_fully_accounted",
            "registered_queries_total", "failure_unknown_separated",
        ]
        for name in names:
            with self.subTest(name=name):
                self.assertEqual(valid_case(witness=valid_witness(**{name: Evidence.FALSE})).evaluate(), Verdict.REFUTED)

    def test_checker_passes(self):
        proc = subprocess.run(
            [sys.executable, str(ROOT / "tools" / "check_upp_w11_historical_trace.py")],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)


if __name__ == "__main__":
    unittest.main()
