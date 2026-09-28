"""Kernel-level axiom census for every Lean module compiled by the required assurance lane.

This test is intentionally skipped outside the required assurance jobs, where ``FAR_LEAN_HOME``
is not installed.  In those jobs it recompiles every governed module to a fresh temporary olean
set and asks Lean's own ``collectAxioms`` for every non-internal declaration defined by those
modules.  Only Lean's three standard proof axioms are permitted.
"""
from __future__ import annotations

import os
import subprocess
import tempfile
import textwrap
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Dependency order mirrors the required governed compile step; ValidationEngine is also included.
GOVERNED = (
    "ValidationEngine",
    "FARCore",
    "SCoreW5",
    "UPPSemanticKernel",
    "G2OpenWorldLowerBound",
    "G3EpistemicMaximality",
    "Canonicality",
    "RepresentationInvariance",
    "QuotientMinimality",
    "DefinitionalCompleteness",
    "ConservativeExtensibility",
    "MaximalKnowability",
    "CanonicalUniversalityTerminal",
    "FARCanonicalBridge",
    "FARCanonicalUniversalityDecision",
    "FARCanonicalCountermodel",
    "W5ApproximationCost",
    "FARCoreV11Substrate",
    "FARCoreV11Claims001To012",
    "FARCoreV11Omega",
    "FARCoreV11SSS",
    "FARCoreV11Mutations",
)
ALLOWED = ("propext", "Classical.choice", "Quot.sound")


def lean_binary() -> Path | None:
    home = os.environ.get("FAR_LEAN_HOME")
    if not home:
        return None
    lean = Path(home) / "bin" / "lean"
    return lean if lean.is_file() else None


def audit_source(modules: tuple[str, ...]) -> str:
    imports = "\n".join(f"import {module}" for module in modules)
    module_names = ", ".join(f"`{module}" for module in modules)
    allowed = ", ".join(f"``{name}" for name in ALLOWED)
    return textwrap.dedent(
        f"""
        import Lean
        {imports}

        open Lean Elab Command

        def farGovernedModules : Array Name := #[{module_names}]
        def farAllowedAxioms : Array Name := #[{allowed}]

        run_cmd do
          let env ← getEnv
          let mut checked : Nat := 0
          for (name, _info) in env.constants.toList do
            if !name.isInternal then
              if let some idx := env.getModuleIdxFor? name then
                if let some moduleName := env.header.moduleNames[idx]? then
                  if farGovernedModules.contains moduleName then
                    checked := checked + 1
                    let axioms ← collectAxioms name
                    for axiom in axioms do
                      unless farAllowedAxioms.contains axiom do
                        throwError m!"governed declaration {{name}} depends on forbidden axiom {{axiom}}"
          if checked == 0 then
            throwError "governed axiom census was vacuous"
          logInfo m!"FAR governed axiom census checked {{checked}} declarations"
        """
    ).lstrip()


class GovernedLeanAxiomCensusTests(unittest.TestCase):
    def setUp(self) -> None:
        self.lean = lean_binary()
        if self.lean is None:
            self.skipTest("FAR_LEAN_HOME is installed by the required assurance lanes")

    def compile_module(self, module: str, output: Path, *, source_root: Path = ROOT / "mechanization" / "lean") -> None:
        source = source_root / f"{module}.lean"
        self.assertTrue(source.is_file(), module)
        env = dict(os.environ, LEAN_PATH=str(output))
        result = subprocess.run(
            [str(self.lean), "-o", str(output / f"{module}.olean"), str(source)],
            cwd=ROOT, env=env, capture_output=True, text=True, check=False,
        )
        self.assertEqual(result.returncode, 0, f"{module}\n{result.stdout}\n{result.stderr}")

    def run_audit(self, output: Path, modules: tuple[str, ...]) -> subprocess.CompletedProcess[str]:
        audit = output / "FARGovernedAxiomCensus.lean"
        audit.write_text(audit_source(modules), encoding="utf-8")
        return subprocess.run(
            [str(self.lean), str(audit)], cwd=ROOT,
            env=dict(os.environ, LEAN_PATH=str(output)),
            capture_output=True, text=True, check=False,
        )

    def test_all_governed_declarations_use_only_allowed_kernel_axioms(self) -> None:
        with tempfile.TemporaryDirectory(prefix="far-governed-lean-") as directory:
            output = Path(directory)
            for module in GOVERNED:
                self.compile_module(module, output)
            result = self.run_audit(output, GOVERNED)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("FAR governed axiom census checked", result.stdout + result.stderr)

    def test_census_rejects_a_declared_axiom_even_when_no_sorry_warning_exists(self) -> None:
        with tempfile.TemporaryDirectory(prefix="far-axiom-attack-") as directory:
            output = Path(directory)
            source = output / "Attack.lean"
            source.write_text(
                "axiom attackerAxiom : False\n"
                "theorem attackerTheorem : False := attackerAxiom\n",
                encoding="utf-8",
            )
            result = subprocess.run(
                [str(self.lean), "-o", str(output / "Attack.olean"), str(source)],
                cwd=ROOT, env=dict(os.environ, LEAN_PATH=str(output)),
                capture_output=True, text=True, check=False,
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            audit = self.run_audit(output, ("Attack",))
            self.assertNotEqual(audit.returncode, 0)
            self.assertIn("forbidden axiom", audit.stdout + audit.stderr)


if __name__ == "__main__":
    unittest.main()
