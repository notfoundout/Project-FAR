import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from far_release_assurance.closure import assess_closure
from far_release_assurance.decision import adjudicate
from far_release_assurance.model import (
    ClosureStatus,
    Decision,
    EvidenceStatus,
    Finding,
    FindingDisposition,
    MachineryItem,
    Severity,
)


def confirmed_item(identifier: str, *dependencies: str) -> MachineryItem:
    return MachineryItem(
        machinery_id=identifier,
        kind="test",
        name=identifier,
        version="1",
        required_dependencies=dependencies,
        evidence_status=EvidenceStatus.CONFIRMED,
        effective=True,
        valid=True,
    )


class MachineryClosureTests(unittest.TestCase):
    def test_closed_transitive_graph(self):
        result = assess_closure(
            (
                confirmed_item("agent", "prompt", "policy"),
                confirmed_item("prompt", "model"),
                confirmed_item("policy"),
                confirmed_item("model"),
            ),
            ("agent",),
        )
        self.assertEqual(result.status, ClosureStatus.CLOSED)
        self.assertEqual(result.reached, ("agent", "model", "policy", "prompt"))

    def test_cycle_safe_and_idempotent(self):
        items = (
            confirmed_item("a", "b"),
            confirmed_item("b", "a"),
        )
        first = assess_closure(items, ("a",))
        second = assess_closure(items, ("a",))
        self.assertEqual(first, second)
        self.assertEqual(first.status, ClosureStatus.CLOSED)

    def test_missing_transitive_dependency_opens_closure(self):
        result = assess_closure((confirmed_item("agent", "hidden-memory"),), ("agent",))
        self.assertEqual(result.status, ClosureStatus.OPEN)
        self.assertEqual(result.defects, ("hidden-memory",))

    def test_unknown_is_not_closed(self):
        result = assess_closure(
            (
                MachineryItem(
                    machinery_id="remote-policy",
                    kind="policy",
                    name="remote-policy",
                    evidence_status=EvidenceStatus.DISCLOSED_UNVERIFIED,
                    effective=None,
                    valid=None,
                    mutable=True,
                    external=True,
                ),
            ),
            ("remote-policy",),
        )
        self.assertEqual(result.status, ClosureStatus.UNKNOWN)
        self.assertEqual(result.unresolved, ("remote-policy",))

    def test_duplicate_identity_is_open(self):
        result = assess_closure(
            (confirmed_item("model"), confirmed_item("model")),
            ("model",),
        )
        self.assertEqual(result.status, ClosureStatus.OPEN)
        self.assertEqual(result.duplicates, ("model",))

    def test_undeclared_root_is_reported(self):
        result = assess_closure((), ("agent",))
        self.assertEqual(result.status, ClosureStatus.OPEN)
        self.assertEqual(result.undeclared_roots, ("agent",))


class DecisionTests(unittest.TestCase):
    def test_confirmed_critical_blocker_blocks(self):
        finding = Finding(
            finding_id="F-001",
            rule_id="identity-revalidation/0.1",
            severity=Severity.CRITICAL,
            disposition=FindingDisposition.CONFIRMED,
            rationale="Identity changed without revalidation.",
            blocking=True,
        )
        decision, _ = adjudicate((finding,), ClosureStatus.CLOSED)
        self.assertEqual(decision, Decision.BLOCKED)

    def test_inferred_high_requires_review(self):
        finding = Finding(
            finding_id="F-002",
            rule_id="hidden-machinery/0.1",
            severity=Severity.HIGH,
            disposition=FindingDisposition.INFERRED,
            rationale="Observed state cannot be explained by disclosed machinery.",
            blocking=True,
        )
        decision, _ = adjudicate((finding,), ClosureStatus.CLOSED)
        self.assertEqual(decision, Decision.REVIEW_REQUIRED)

    def test_unknown_closure_cannot_pass(self):
        decision, _ = adjudicate((), ClosureStatus.UNKNOWN)
        self.assertEqual(decision, Decision.UNKNOWN)

    def test_clean_closed_release_passes(self):
        decision, _ = adjudicate((), ClosureStatus.CLOSED)
        self.assertEqual(decision, Decision.PASS)


if __name__ == "__main__":
    unittest.main()
