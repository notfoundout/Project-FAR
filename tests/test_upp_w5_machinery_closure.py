import importlib.util
import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
PATH = ROOT / "theory" / "machinery" / "upp_machinery_closure_v1.py"
SPEC = importlib.util.spec_from_file_location("upp_machinery_closure_v1", PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = MODULE
SPEC.loader.exec_module(MODULE)

Availability = MODULE.Availability
RepresentationPackage = MODULE.RepresentationPackage
SupportEdge = MODULE.SupportEdge
SupportNode = MODULE.SupportNode
Verdict = MODULE.Verdict
closure_is_idempotent = MODULE.closure_is_idempotent
monotone_under_disclosed_support = MODULE.monotone_under_disclosed_support


def node(name, kind="runtime", availability=Availability.PRESENT, effective=True):
    return SupportNode(name, kind, availability, effective)


class MachineryClosureTests(unittest.TestCase):
    def test_transitive_closure_reaches_all_required_support(self):
        package = RepresentationPackage(
            roots=("rep",),
            nodes=(node("rep", "representation_core"), node("decoder", "decoder"), node("store", "external_store")),
            edges=(
                SupportEdge("rep", "decoder", True, True, Availability.PRESENT),
                SupportEdge("decoder", "store", True, True, Availability.PRESENT),
            ),
        )
        result = package.close()
        self.assertEqual(result.verdict, Verdict.CLOSED)
        self.assertEqual(result.reached, frozenset({"rep", "decoder", "store"}))
        self.assertTrue(closure_is_idempotent(package))

    def test_concealed_required_decoder_fails(self):
        package = RepresentationPackage(
            roots=("rep",),
            nodes=(node("rep", "representation_core"), node("decoder", "decoder")),
            edges=(SupportEdge("rep", "decoder", True, False, Availability.PRESENT),),
        )
        result = package.close()
        self.assertEqual(result.verdict, Verdict.OPEN)
        self.assertEqual(len(result.concealed_required_edges), 1)

    def test_unrealized_oracle_fails(self):
        package = RepresentationPackage(
            roots=("rep",),
            nodes=(node("rep", "representation_core"), node("oracle", "oracle_realization", Availability.ABSENT, False)),
            edges=(SupportEdge("rep", "oracle", True, True, Availability.ABSENT),),
        )
        self.assertEqual(package.close().verdict, Verdict.OPEN)

    def test_unknown_support_stays_unknown(self):
        package = RepresentationPackage(
            roots=("rep",),
            nodes=(node("rep", "representation_core"), node("scheduler", "scheduler", Availability.UNKNOWN, None)),
            edges=(SupportEdge("rep", "scheduler", True, True, Availability.UNKNOWN),),
        )
        self.assertEqual(package.close().verdict, Verdict.UNKNOWN)

    def test_optional_support_does_not_block_closure(self):
        package = RepresentationPackage(
            roots=("rep",),
            nodes=(node("rep", "representation_core"), node("telemetry", "runtime", Availability.ABSENT, False)),
            edges=(SupportEdge("rep", "telemetry", False, True, Availability.ABSENT),),
        )
        self.assertEqual(package.close().verdict, Verdict.CLOSED)

    def test_ineffective_present_support_is_invalid(self):
        package = RepresentationPackage(
            roots=("rep",),
            nodes=(node("rep", "representation_core"), node("decoder", "decoder", Availability.PRESENT, False)),
            edges=(SupportEdge("rep", "decoder", True, True, Availability.PRESENT),),
        )
        result = package.close()
        self.assertEqual(result.verdict, Verdict.OPEN)
        self.assertTrue(result.invalidities)

    def test_missing_root_is_invalid(self):
        package = RepresentationPackage(roots=("ghost",), nodes=(node("rep"),), edges=())
        self.assertEqual(package.close().verdict, Verdict.OPEN)

    def test_duplicate_node_ids_are_invalid(self):
        package = RepresentationPackage(roots=("rep",), nodes=(node("rep"), node("rep")), edges=())
        self.assertEqual(package.close().verdict, Verdict.OPEN)

    def test_cycle_terminates_at_fixed_point(self):
        package = RepresentationPackage(
            roots=("a",),
            nodes=(node("a"), node("b")),
            edges=(
                SupportEdge("a", "b", True, True, Availability.PRESENT),
                SupportEdge("b", "a", True, True, Availability.PRESENT),
            ),
        )
        result = package.close()
        self.assertEqual(result.verdict, Verdict.CLOSED)
        self.assertEqual(result.reached, frozenset({"a", "b"}))

    def test_monotone_under_disclosed_effective_support(self):
        package = RepresentationPackage(roots=("rep",), nodes=(node("rep"),), edges=())
        self.assertTrue(monotone_under_disclosed_support(
            package,
            (node("decoder", "decoder"),),
            (SupportEdge("rep", "decoder", True, True, Availability.PRESENT),),
        ))

    def test_registered_queries_must_be_unique(self):
        bad = SupportNode("rep", "representation_core", Availability.PRESENT, True, ("q", "q"))
        package = RepresentationPackage(roots=("rep",), nodes=(bad,), edges=())
        self.assertEqual(package.close().verdict, Verdict.OPEN)


if __name__ == "__main__":
    unittest.main()
