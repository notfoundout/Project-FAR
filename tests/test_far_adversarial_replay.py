"""Deterministic replay reconstructs the run, or fails closed.

Regression for audit finding 7: the previous ``replay`` command only re-hashed
stored invocations. It never re-ran the parsers or the reducer, so it could not
have detected a reconstruction that lands somewhere else.
"""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from far_adversarial import ledger as L  # noqa: E402
from far_adversarial.evidence import EvidenceStore  # noqa: E402
from far_adversarial.frozen_source import GitFrozenSource  # noqa: E402
from far_adversarial.orchestrator import Orchestrator  # noqa: E402
from far_adversarial.providers import ScriptedProvider  # noqa: E402
from far_adversarial.replay import replay  # noqa: E402


def _git(repo: Path, *args: str):
    return subprocess.run(["git", *args], cwd=repo, capture_output=True, text=True,
                          check=True)


def first_pass(objections):
    return json.dumps({
        "assessment": "analysis",
        "objections": [{"claim": c, "kind": "other", "rationale": "r"} for c in objections],
        "source_requests": [],
        "formal_obligations": [],
    })


def audit(responses):
    return json.dumps({"responses": responses})


def act(issue_id, action):
    return {"issue_id": issue_id, "action": action, "rationale": "r",
            "revised_claim": None}


def _target(**overrides):
    base = dict(id="A", original_formulation="o", current_formulation="c",
                frozen_scope="s", provenance="p", authorized=True,
                frozen_evidence_paths=["docs/target.md"])
    base.update(overrides)
    return L.Target(**base)


class ReplayHarness:
    """Records a run against a real frozen git source, then replays it."""

    def __init__(self, tmp: Path):
        self.tmp = tmp
        self.repo = tmp / "repo"
        self.repo.mkdir()
        _git(self.repo, "init", "-q")
        _git(self.repo, "config", "user.email", "t@example.com")
        _git(self.repo, "config", "user.name", "t")
        (self.repo / "docs").mkdir()
        (self.repo / "docs" / "target.md").write_text("frozen evidence\n", encoding="utf-8")
        _git(self.repo, "add", "-A")
        _git(self.repo, "commit", "-q", "-m", "freeze")
        self.commit = _git(self.repo, "rev-parse", "HEAD").stdout.strip()
        self.source = GitFrozenSource(self.repo, self.commit, ["docs/target.md"])
        self.store = EvidenceStore(tmp / "evidence")
        self.issue = L.issue_id("A", "An objection.")

    def baseline(self) -> L.Ledger:
        ledger = L.Ledger()
        ledger.add_target(_target())
        return ledger

    def loader(self, target):
        return {p: self.source.read(p) for p in sorted(target.frozen_evidence_paths)}

    def record_run(self):
        ledger = self.baseline()
        baseline_digest = ledger.digest()
        orchestrator = Orchestrator(
            ledger=ledger, store=self.store,
            claude=ScriptedProvider([first_pass([]), audit([act(self.issue, "REBUT")])],
                                    name="claude", model="claude-test"),
            gpt=ScriptedProvider([first_pass(["An objection."]),
                                  audit([act(self.issue, "WITHDRAW")])],
                                 name="gpt", model="gpt-test"),
            evidence_loader=self.loader, source_freeze=self.source.identity(),
            max_rounds_per_target=1, parallel=False,
        )
        reports = orchestrator.run(max_targets=1)
        record = orchestrator.run_record("run-1", baseline_digest, reports)
        return ledger, record

    def replay(self, record, **overrides):
        kwargs = dict(store=self.store, record=record, baseline_ledger=self.baseline(),
                      frozen_source=self.source, evidence_loader=self.loader,
                      max_rounds_per_target=1)
        kwargs.update(overrides)
        return replay(**kwargs)


class ModuleNamespaceTests(unittest.TestCase):
    """The replay submodule must stay reachable under its own name.

    Re-exporting the function as ``far_adversarial.replay`` rebound the package
    attribute from the submodule to the function, so ``import
    far_adversarial.replay`` handed back a function with none of the module's
    contents. An audit probe checking ``hasattr(module, 'replay')`` was misled
    by exactly this.
    """

    def test_importing_the_submodule_yields_the_module_not_a_function(self):
        import importlib
        import far_adversarial  # noqa: F401

        module = importlib.import_module("far_adversarial.replay")
        self.assertTrue(hasattr(module, "replay"))
        self.assertTrue(hasattr(module, "ReplayResult"))
        self.assertFalse(callable(module))

    def test_the_package_attribute_is_the_submodule(self):
        import types
        import far_adversarial

        self.assertIsInstance(far_adversarial.replay, types.ModuleType)

    def test_the_function_is_exported_under_a_non_shadowing_name(self):
        import far_adversarial

        self.assertIn("replay_recorded_run", far_adversarial.__all__)
        self.assertTrue(callable(far_adversarial.replay_recorded_run))
        self.assertNotIn("replay", far_adversarial.__all__)

    def test_no_export_shadows_a_submodule(self):
        import importlib
        import pkgutil
        import far_adversarial

        submodules = {name for _, name, _ in pkgutil.iter_modules(far_adversarial.__path__)}
        for name in far_adversarial.__all__:
            self.assertNotIn(name, submodules,
                             f"{name} is exported and also names a submodule")
        # And every submodule still imports cleanly under its own name.
        for name in sorted(submodules):
            importlib.import_module(f"far_adversarial.{name}")


class CleanReplayTests(unittest.TestCase):
    def test_clean_replay_reproduces_the_exact_final_digest(self):
        with tempfile.TemporaryDirectory() as tmp:
            harness = ReplayHarness(Path(tmp))
            ledger, record = harness.record_run()
            self.assertEqual(ledger.targets["A"].status, L.READY_UNDER_INTERNAL_PROTOCOL)
            result = harness.replay(record)
            self.assertTrue(result.ok, result.reason)
            self.assertEqual(result.reconstructed_digest, record.final_ledger_digest)

    def test_replay_actually_re_ran_the_parsers_and_reducer(self):
        # A replay that never consults stored responses proves nothing.
        with tempfile.TemporaryDirectory() as tmp:
            harness = ReplayHarness(Path(tmp))
            _, record = harness.record_run()
            result = harness.replay(record)
            self.assertGreaterEqual(result.provider_calls, 2)

    def test_replay_does_not_append_to_the_append_only_store(self):
        with tempfile.TemporaryDirectory() as tmp:
            harness = ReplayHarness(Path(tmp))
            _, record = harness.record_run()
            before = len(harness.store.all_invocations())
            harness.replay(record)
            self.assertEqual(len(harness.store.all_invocations()), before)

    def test_the_run_record_captures_what_replay_needs(self):
        with tempfile.TemporaryDirectory() as tmp:
            harness = ReplayHarness(Path(tmp))
            _, record = harness.record_run()
            self.assertEqual(record.source_identity, harness.source.identity())
            self.assertEqual(record.reducer_version, L.REDUCER_VERSION)
            self.assertEqual(record.ledger_schema, L.LEDGER_SCHEMA)
            self.assertTrue(record.invocation_ids)
            self.assertEqual(record.resolved_models["gpt"], "gpt-test")

    def test_run_record_round_trips_on_disk(self):
        from far_adversarial.evidence import RunRecord

        with tempfile.TemporaryDirectory() as tmp:
            harness = ReplayHarness(Path(tmp))
            _, record = harness.record_run()
            path = record.save(Path(tmp))
            self.assertEqual(RunRecord.load(path).final_ledger_digest,
                             record.final_ledger_digest)


class FailClosedTests(unittest.TestCase):
    def test_tampered_raw_response_fails_replay(self):
        with tempfile.TemporaryDirectory() as tmp:
            harness = ReplayHarness(Path(tmp))
            _, record = harness.record_run()
            victim = harness.store.all_invocations()[0]
            (harness.store.raw_dir / f"{victim.invocation_id}.txt").write_text(
                first_pass(["fabricated objection"]), encoding="utf-8")
            result = harness.replay(record)
            self.assertFalse(result.ok)
            self.assertIn("integrity", result.reason)

    def test_tampered_normalized_response_fails_replay(self):
        with tempfile.TemporaryDirectory() as tmp:
            harness = ReplayHarness(Path(tmp))
            _, record = harness.record_run()
            lines = harness.store.index_path.read_text(encoding="utf-8").splitlines()
            rows = [json.loads(line) for line in lines]
            rows[0]["normalized_response"] = {"objections": [{"claim": "fabricated"}]}
            harness.store.index_path.write_text(
                "\n".join(json.dumps(r) for r in rows) + "\n", encoding="utf-8")
            result = harness.replay(record)
            self.assertFalse(result.ok)
            self.assertTrue(any("normalized" in p for p in result.integrity_problems))

    def test_a_changed_reducer_version_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            harness = ReplayHarness(Path(tmp))
            _, record = harness.record_run()
            record.reducer_version = "far-adversarial-reducer/0"
            result = harness.replay(record)
            self.assertFalse(result.ok)
            self.assertIn("reducer version mismatch", result.reason)

    def test_a_changed_ledger_schema_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            harness = ReplayHarness(Path(tmp))
            _, record = harness.record_run()
            record.ledger_schema = "far-adversarial-ledger/1"
            result = harness.replay(record)
            self.assertFalse(result.ok)
            self.assertIn("ledger schema version mismatch", result.reason)

    def test_a_changed_protocol_version_fails_closed(self):
        with tempfile.TemporaryDirectory() as tmp:
            harness = ReplayHarness(Path(tmp))
            _, record = harness.record_run()
            record.protocol_version = "far-adversarial-protocol/1"
            result = harness.replay(record)
            self.assertFalse(result.ok)
            self.assertIn("protocol version mismatch", result.reason)

    def test_migration_must_be_requested_explicitly(self):
        with tempfile.TemporaryDirectory() as tmp:
            harness = ReplayHarness(Path(tmp))
            _, record = harness.record_run()
            record.reducer_version = "far-adversarial-reducer/0"
            self.assertFalse(harness.replay(record).ok)
            # With migration allowed the version gate is skipped; the digest
            # check still runs and still has to hold.
            self.assertTrue(harness.replay(record, allow_migration=True).ok)

    def test_a_drifted_frozen_source_fails_replay(self):
        with tempfile.TemporaryDirectory() as tmp:
            harness = ReplayHarness(Path(tmp))
            _, record = harness.record_run()
            record.source_identity = "git:deadbeef:cafebabe"
            result = harness.replay(record)
            self.assertFalse(result.ok)
            self.assertIn("frozen source drifted", result.reason)

    def test_a_wrong_baseline_fails_replay(self):
        with tempfile.TemporaryDirectory() as tmp:
            harness = ReplayHarness(Path(tmp))
            _, record = harness.record_run()
            wrong = L.Ledger()
            wrong.add_target(_target(current_formulation="a different baseline"))
            result = harness.replay(record, baseline_ledger=wrong)
            self.assertFalse(result.ok)
            self.assertIn("baseline", result.reason)

    def test_a_diverging_final_digest_fails_replay(self):
        with tempfile.TemporaryDirectory() as tmp:
            harness = ReplayHarness(Path(tmp))
            _, record = harness.record_run()
            record.final_ledger_digest = "0" * 64
            result = harness.replay(record)
            self.assertFalse(result.ok)
            self.assertIn("diverges", result.reason)

    def test_a_mutated_working_tree_cannot_change_the_reconstruction(self):
        with tempfile.TemporaryDirectory() as tmp:
            harness = ReplayHarness(Path(tmp))
            _, record = harness.record_run()
            (harness.repo / "docs" / "target.md").write_text("TAMPERED\n", encoding="utf-8")
            self.assertTrue(harness.replay(record).ok)


if __name__ == "__main__":
    unittest.main()
