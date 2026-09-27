"""Regressions for the CI merge gate: it must fail, not skip, and must not trust mutable inputs.

Each test pins one repaired defect (red-team RT-9/RT-10, root-of-trust R14/LIM-050). Where a
workflow step's script decides the outcome, the test executes that script rather than matching text.
"""
from __future__ import annotations

import hashlib
import json
import py_compile
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
WORKFLOWS = ROOT / ".github" / "workflows"
# Workflows whose jobs execute candidate code and produce the merge evidence, plus the governed Lean lane.
ASSURANCE_WORKFLOWS = ("validator-assurance.yml", "exact-head-assurance.yml", "lean.yml")
LEAN_ARCHIVE_URL = "https://github.com/leanprover/lean4/releases/download/v4.19.0/lean-4.19.0-linux.tar.zst"
LEAN_ARCHIVE_SHA256 = "6fe3ce97a58f44e2b3567d455b994eacec5bfe9ae7774f2a573444480ba813fe"
SORRY_GATE = "declaration uses 'sorry'"
LEAN_INVOCATION = re.compile(r"(^|[\s\"/])lean\"?\s+(-o\s+\S+\s+)?mechanization/lean/\S+\.lean", re.MULTILINE)
LEAN_TARGET = re.compile(r"(?:^|[\s\"/])lean\"?\s+(?:-o\s+\S+\s+)?(mechanization/lean/\S+\.lean)", re.MULTILINE)
# Workflow scripts call `python`; resolve it to the interpreter running these tests, not the host's.
SCRIPT_PATH = f"{Path(sys.executable).parent}:/usr/bin:/bin"


def _workflow(name: str) -> dict:
    return yaml.safe_load((WORKFLOWS / name).read_text(encoding="utf-8"))


def _steps(workflow: dict):
    for job_id, job in workflow["jobs"].items():
        for step in job.get("steps", []):
            yield job_id, step


def _bash(script: str, cwd: Path, env: dict[str, str]) -> int:
    return subprocess.run(["bash", "-e", "-c", script], cwd=cwd, env=env, capture_output=True, check=False).returncode


class MergeAuthorityCannotBeSkippedTests(unittest.TestCase):
    """GitHub counts a skipped required check as passing; a failed dependency must fail the gate."""

    def setUp(self) -> None:
        self.job = _workflow("validator-assurance.yml")["jobs"]["merge-authority"]

    def test_job_runs_after_a_failed_dependency_but_not_after_cancellation(self) -> None:
        self.assertEqual(self.job["if"], "${{ !cancelled() }}")

    def test_first_step_requires_every_dependency_to_have_succeeded(self) -> None:
        needs = self.job["needs"]
        needs = [needs] if isinstance(needs, str) else list(needs)
        guard = self.job["steps"][0]
        self.assertEqual(guard["env"], {"UPSTREAM_RESULT": "${{ needs.signed-cache-consumer.result }}"})
        self.assertEqual(needs, ["signed-cache-consumer"])
        with tempfile.TemporaryDirectory() as directory:
            for result in ("failure", "skipped", "cancelled", ""):
                self.assertNotEqual(_bash(guard["run"], Path(directory), {"UPSTREAM_RESULT": result}), 0, result)
            self.assertEqual(_bash(guard["run"], Path(directory), {"UPSTREAM_RESULT": "success"}), 0)

    def test_assurance_hash_audit_fails_on_lock_drift(self) -> None:
        audit = next(step for _job, step in _steps(_workflow("validator-assurance.yml"))
                     if step.get("name") == "Record assurance lock hash comparison")
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "validation_bootstrap").mkdir()
            (root / "artifacts" / "validation").mkdir(parents=True)
            (root / "pinned.txt").write_text("pinned\n", encoding="utf-8")
            actual = hashlib.sha256(b"pinned\n").hexdigest()
            drifted = hashlib.sha256(b"other\n").hexdigest()
            lock = root / "validation_bootstrap" / "assurance-lock.json"
            lock.write_text(json.dumps({"files": {"pinned.txt": actual}}), encoding="utf-8")
            self.assertEqual(_bash(audit["run"], root, {"PATH": SCRIPT_PATH}), 0)
            lock.write_text(json.dumps({"files": {"pinned.txt": drifted}}), encoding="utf-8")
            self.assertNotEqual(_bash(audit["run"], root, {"PATH": SCRIPT_PATH}), 0)
            report = json.loads((root / "artifacts" / "validation" / "assurance-hash-audit.json").read_text())
            self.assertFalse(report["successful"])


class CandidateJobKeyMaterialTests(unittest.TestCase):
    """RT-9: jobs that run candidate code must hold no persistent secret or token as key material."""

    def test_no_workflow_uses_a_secret_or_job_token_as_validation_key(self) -> None:
        pattern = re.compile(r"FAR_VALIDATION_CACHE_SIGNING_KEY\s*[:=]\s*[\"']?\$\{\{[^}]*(secrets\.|github\.token)")
        for path in sorted(WORKFLOWS.glob("*.yml")):
            self.assertIsNone(pattern.search(path.read_text(encoding="utf-8")), path.name)

    def test_merge_evidence_jobs_derive_a_masked_per_job_key(self) -> None:
        for name, job_id in (("validator-assurance.yml", "merge-authority"),
                             ("exact-head-assurance.yml", "exact-head-assurance")):
            job = _workflow(name)["jobs"][job_id]
            self.assertNotIn("FAR_VALIDATION_CACHE_SIGNING_KEY", job.get("env", {}), name)
            derive = next(step for step in job["steps"] if step.get("name") == "Derive per-job ephemeral validation signing key")
            self.assertIn('key="$(openssl rand -hex 32)"', derive["run"])
            self.assertLess(derive["run"].index("::add-mask::"), derive["run"].index("GITHUB_ENV"))

    def test_candidate_code_jobs_never_persist_checkout_credentials(self) -> None:
        for name in ASSURANCE_WORKFLOWS:
            for job_id, step in _steps(_workflow(name)):
                if str(step.get("uses", "")).startswith("actions/checkout@"):
                    self.assertIs((step.get("with") or {}).get("persist-credentials"), False, f"{name}:{job_id}")


class MutableAcquisitionTests(unittest.TestCase):
    """RT-10: no mutable installer or tag decides what executes in the assurance lanes."""

    def test_no_workflow_pipes_the_moving_elan_installer(self) -> None:
        for path in sorted(WORKFLOWS.glob("*.yml")):
            self.assertNotIn("elan/master", path.read_text(encoding="utf-8"), path.name)

    def test_lean_is_installed_from_the_digest_bound_release_archive(self) -> None:
        toolchain = (ROOT / "lean-toolchain").read_text(encoding="utf-8").strip()
        self.assertEqual(toolchain, "leanprover/lean4:v4.19.0")
        for name in ASSURANCE_WORKFLOWS:
            installs = [step for _job, step in _steps(_workflow(name)) if step.get("name") == "Install pinned Lean toolchain"]
            self.assertEqual(len(installs), 1, name)
            script = installs[0]["run"]
            self.assertIn(LEAN_ARCHIVE_URL, script)
            self.assertIn(f'echo "{LEAN_ARCHIVE_SHA256}  $archive" | sha256sum -c -', script)
            self.assertLess(script.index("sha256sum -c"), script.index("tar --zstd"), name)

    def test_every_workflow_that_runs_lean_installs_the_digest_bound_archive(self) -> None:
        # elan-init resolves the latest elan release and fetches the toolchain by tag, so even a
        # digest-checked installer script leaves the executed Lean unbound.
        seen = 0
        for path in sorted(WORKFLOWS.glob("*.yml")):
            scripts = "\n".join(step.get("run", "") for _job, step in _steps(_workflow(path.name)))
            self.assertNotIn("elan-init", scripts, path.name)
            if LEAN_INVOCATION.search(scripts):
                seen += 1
                self.assertIn(f'echo "{LEAN_ARCHIVE_SHA256}  $archive" | sha256sum -c -', scripts, path.name)
        self.assertGreaterEqual(seen, 5)

    def test_assurance_actions_are_pinned_to_commits(self) -> None:
        for name in ASSURANCE_WORKFLOWS:
            for job_id, step in _steps(_workflow(name)):
                if "uses" in step:
                    self.assertRegex(step["uses"], r"^[\w.-]+/[\w.-]+@[0-9a-f]{40}$", f"{name}:{job_id}")


class LeanSorryGateTests(unittest.TestCase):
    """`lean` exits 0 when a declaration uses `sorry`; every governed compile must reject it."""

    def test_every_lean_invocation_is_in_a_step_that_rejects_sorry(self) -> None:
        seen = 0
        for path in sorted(WORKFLOWS.glob("*.yml")):
            for job_id, step in _steps(_workflow(path.name)):
                script = step.get("run", "")
                if LEAN_INVOCATION.search(script):
                    seen += 1
                    self.assertIn(SORRY_GATE, script, f"{path.name}:{job_id}:{step.get('name')}")
        self.assertGreaterEqual(seen, 6)

    def test_sorry_gate_rejects_a_sorry_warning_and_passes_clean_output(self) -> None:
        compile_step = next(step for _job, step in _steps(_workflow("lean.yml"))
                            if step.get("name") == "Compile governed Lean mechanization and reject sorry")
        with tempfile.TemporaryDirectory() as directory:
            fake_bin = Path(directory) / "bin"
            fake_bin.mkdir()
            fake = fake_bin / "lean"
            env = {"PATH": f"{fake_bin}:/usr/bin:/bin", "RUNNER_TEMP": directory}
            fake.write_text("#!/bin/sh\necho \"x.lean:1:0: warning: declaration uses 'sorry'\"\n", encoding="utf-8")
            fake.chmod(0o755)
            self.assertNotEqual(_bash(compile_step["run"], ROOT, env), 0)
            fake.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
            self.assertEqual(_bash(compile_step["run"], ROOT, env), 0)
            # A failing compile stops the step even though later compiles would succeed.
            fake.write_text("#!/bin/sh\ncase \"$*\" in *FARCore.lean*) exit 3;; esac\nexit 0\n", encoding="utf-8")
            self.assertEqual(_bash(compile_step["run"], ROOT, env), 3)

    def test_w5_compile_rejects_sorry_and_compile_failures(self) -> None:
        # Only steps whose scripts use declared executables are run here; the FAR-CORE v1.1 step
        # also runs mkdir and tee, so its gate is covered by the structural test above.
        steps = {"pca-w5.yml": "Compile PCA-W5 formal control and reject sorry"}
        for name, step_name in steps.items():
            script = next(step for _job, step in _steps(_workflow(name)) if step.get("name") == step_name)["run"]
            with self.subTest(name), tempfile.TemporaryDirectory() as directory:
                work = Path(directory)
                fake_bin = work / "bin"
                fake_bin.mkdir()
                fake = fake_bin / "lean"
                env = {"PATH": f"{fake_bin}:/usr/bin:/bin", "RUNNER_TEMP": directory}
                fake.write_text("#!/bin/sh\necho \"x.lean:1:0: warning: declaration uses 'sorry'\"\n", encoding="utf-8")
                fake.chmod(0o755)
                self.assertNotEqual(_bash(script, work, env), 0)
                fake.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
                self.assertEqual(_bash(script, work, env), 0)
                fake.write_text("#!/bin/sh\nexit 3\n", encoding="utf-8")
                self.assertNotEqual(_bash(script, work, env), 0)


class GovernedLeanIsPartOfTheRequiredCheckTests(unittest.TestCase):
    """Only `merge-authority` is a required Actions check, so a governed compile elsewhere is advisory."""

    STEP = "Compile governed Lean modules and reject sorry"

    def _targets(self, steps) -> set[str]:
        return {target for step in steps for target in LEAN_TARGET.findall(step.get("run", ""))}

    def test_merge_authority_compiles_every_lean_module_that_any_workflow_compiles(self) -> None:
        advisory = set()
        for path in sorted(WORKFLOWS.glob("*.yml")):
            if path.name not in ("validator-assurance.yml", "exact-head-assurance.yml"):
                advisory |= self._targets(step for _job, step in _steps(_workflow(path.name)))
        self.assertIn("mechanization/lean/FARCoreV11Mutations.lean", advisory)
        self.assertIn("mechanization/lean/W5ApproximationCost.lean", advisory)
        for name, job_id in (("validator-assurance.yml", "merge-authority"),
                             ("exact-head-assurance.yml", "exact-head-assurance")):
            steps = _workflow(name)["jobs"][job_id]["steps"]
            self.assertEqual(sorted(advisory - self._targets(steps)), [], name)
            names = [step.get("name") for step in steps]
            # Compiling unlocked Lean can run code, so it belongs after the trusted steps.
            self.assertGreater(names.index(self.STEP), names.index(TrustedStepsPrecedeCandidateCodeTests.BOUNDARY))
            self.assertGreater(names.index("Enforce FAR-CORE v1.1 kernel assumptions"), names.index(self.STEP))

    def test_governed_compile_rejects_sorry_and_stops_at_a_failing_module(self) -> None:
        script = next(step for _job, step in _steps(_workflow("validator-assurance.yml"))
                      if step.get("name") == self.STEP)["run"]
        with tempfile.TemporaryDirectory() as directory:
            work = Path(directory)
            fake = work / "bin" / "lean"
            fake.parent.mkdir()
            env = {"PATH": "/usr/bin:/bin", "RUNNER_TEMP": directory, "FAR_LEAN_HOME": directory}
            fake.write_text("#!/bin/sh\necho \"x.lean:1:0: warning: declaration uses 'sorry'\"\n", encoding="utf-8")
            fake.chmod(0o755)
            self.assertNotEqual(_bash(script, ROOT, env), 0)
            fake.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
            self.assertEqual(_bash(script, ROOT, env), 0)
            fake.write_text("#!/bin/sh\ncase \"$*\" in *Canonicality.lean*) exit 3;; esac\nexit 0\n", encoding="utf-8")
            self.assertEqual(_bash(script, ROOT, env), 3)

class TrustedStepsPrecedeCandidateCodeTests(unittest.TestCase):
    """Once candidate code runs in a job, it can rewrite every later step.

    It can write GITHUB_PATH or GITHUB_ENV, or change site-packages. Checks that need no candidate
    code therefore run first, and the validator runs isolated from the checkout.
    """

    BOUNDARY = "Install dependencies and trace backend"
    TRUSTED = ("Verify independent bootstrap", "Run independent legacy-checker oracle",
               "Detect test and validator weakening", "Exhaustively model-check engine state space",
               "Install pinned Lean toolchain", "Machine-check validation-engine assurance theorems")
    SHADOW_JSON = (
        "import atexit, importlib.machinery, os, sys\n"
        "spec = importlib.machinery.PathFinder.find_spec('json', [p for p in sys.path if p not in ('', os.getcwd())])\n"
        "sys.modules['json'] = spec.loader.load_module('json')\n"
        "atexit.register(lambda: os._exit(0))\n"
    )

    def test_checks_that_need_no_candidate_code_run_first_and_isolated(self) -> None:
        for name, job_id in (("validator-assurance.yml", "merge-authority"),
                             ("exact-head-assurance.yml", "exact-head-assurance")):
            steps = _workflow(name)["jobs"][job_id]["steps"]
            names = [step.get("name") for step in steps]
            boundary = names.index(self.BOUNDARY)
            for trusted in self.TRUSTED:
                self.assertLess(names.index(trusted), boundary, f"{name}: {trusted}")
            for step in steps[:boundary]:
                script = step.get("run", "")
                self.assertNotIn("pip ", script, f"{name}: {step.get('name')}")
                for match in re.finditer(r"(?<![\w/.-])python3?(?=\s)", script):
                    self.assertTrue(script[match.end():].lstrip().startswith("-I"), f"{name}: {step.get('name')}")
                if "run_isolated.py" in script:
                    self.assertIn('-X "pycache_prefix=$RUNNER_TEMP/far-pycache"', script)
        audit = next(step for _job, step in _steps(_workflow("validator-assurance.yml"))
                     if step.get("name") == "Record assurance lock hash comparison")
        self.assertIn("python -I - <<", audit["run"])

    def test_isolated_launcher_ignores_modules_and_bytecode_planted_in_the_checkout(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            shutil.copytree(ROOT / "far_validation", root / "far_validation",
                            ignore=shutil.ignore_patterns("__pycache__"))
            (root / "validation_bootstrap").mkdir()
            shutil.copyfile(ROOT / "validation_bootstrap" / "run_isolated.py", root / "validation_bootstrap" / "run_isolated.py")
            (root / "json.py").write_text(self.SHADOW_JSON, encoding="utf-8")
            planted = root / "planted.py"
            planted.write_text("raise SystemExit(0)\n", encoding="utf-8")
            py_compile.compile(str(planted), cfile=str(root / "far_validation" / "__pycache__" /
                                                        f"__main__.{sys.implementation.cache_tag}.pyc"),
                               invalidation_mode=py_compile.PycInvalidationMode.UNCHECKED_HASH)
            env = {"PATH": SCRIPT_PATH}
            command = ["no-such-command"]  # far_validation rejects it with exit status 2
            # Control: `python -m far_validation` from the checkout runs the planted code, which reports success.
            unsafe = subprocess.run([sys.executable, "-m", "far_validation", *command], cwd=root, env=env,
                                    capture_output=True, check=False)
            self.assertEqual(unsafe.returncode, 0)
            safe = subprocess.run([sys.executable, "-I", "-X", f"pycache_prefix={root / 'pycache'}",
                                   str(root / "validation_bootstrap" / "run_isolated.py"), *command],
                                  cwd=root, env=env, capture_output=True, check=False)
            self.assertEqual(safe.returncode, 2, safe.stderr)


if __name__ == "__main__":
    unittest.main()
