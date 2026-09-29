#!/usr/bin/env python3
"""Adversarial assurance probe: apply each defect the validation system claims to reject.

Every probe mutates a disposable clone, commits the mutation, and runs one named detector. A probe
counts as CAUGHT only when that detector rejects the change with output matching the probe's stated
reason. A rejection for another reason, or no rejection, is MISSED. Expected reasons are fixed in
this file before the run, so a miss is a finding about the validation system, not about the probe.

Usage (from a full, non-shallow clone):
    python tools/assurance_adversarial_probe.py [--json OUT] [--signed-ref REF]

``--signed-ref`` names a commit whose protected-repin ledger carries real owner-signed
authorizations (default: origin/fix/deferred-repin-integration, PR #560). Probes that need it are
reported NOT_RUN when it is unavailable. Trace probes need strace and are NOT_RUN without it.
Exit status is 1 when any probe is MISSED or ERROR.
"""
from __future__ import annotations

import argparse
import base64
import dataclasses
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Callable

ROOT = Path(__file__).resolve().parents[1]
REPOSITORY = "notfoundout/Project-FAR"
REPOSITORY_ID = "1283452680"
LOCK = "validation_bootstrap/assurance-lock.json"
LEDGER = "validation/protected-repin-consumptions.json"
PY = sys.executable


@dataclasses.dataclass
class Outcome:
    probe: str
    defect: str
    detector: str
    expected_reason: str
    status: str  # CAUGHT, MISSED, NOT_RUN, ERROR
    returncode: int | None = None
    evidence: str = ""


class Workspace:
    """One disposable clone, reset to the probe base before every probe."""

    def __init__(self, directory: Path, source: Path) -> None:
        self.path = directory / "repo"
        subprocess.run(["git", "clone", "-q", "--no-local", str(source), str(self.path)], check=True)
        for key, value in (("user.name", "FAR probe"), ("user.email", "probe@example.invalid"), ("commit.gpgsign", "false")):
            self.git("config", key, value)
        self.base = self.git("rev-parse", "HEAD").strip()
        self.env = {
            "PATH": os.environ.get("PATH", "/usr/bin:/bin"),
            "HOME": str(directory),
            "GIT_CONFIG_NOSYSTEM": "1",
            "FAR_VALIDATION_CACHE_SIGNING_KEY": "far-probe-key",
            "FAR_VALIDATION_TRUST_DOMAIN": "far-probe",
            "GITHUB_REPOSITORY": REPOSITORY,
            "GITHUB_REPOSITORY_ID": REPOSITORY_ID,
        }

    def git(self, *args: str) -> str:
        return subprocess.run(["git", "-C", str(self.path), *args], check=True, capture_output=True, text=True).stdout

    def reset(self, ref: str | None = None) -> None:
        self.git("reset", "-q", "--hard", ref or self.base)
        self.git("clean", "-q", "-fdx")

    def commit(self, message: str) -> str:
        self.git("add", "-A")
        self.git("commit", "-q", "--allow-empty", "-m", message)
        return self.git("rev-parse", "HEAD").strip()

    def run(self, *command: str, env: dict[str, str] | None = None) -> tuple[int, str]:
        completed = subprocess.run(
            list(command), cwd=self.path, env={**self.env, **(env or {})}, capture_output=True, text=True, timeout=900
        )
        return completed.returncode, completed.stdout + completed.stderr

    def edit(self, path: str, old: str, new: str, count: int = 1) -> None:
        target = self.path / path
        text = target.read_text(encoding="utf-8")
        if old not in text:
            raise AssertionError(f"probe anchor missing in {path}: {old[:60]!r}")
        target.write_text(text.replace(old, new, count), encoding="utf-8")

    def repin(self, *paths: str) -> None:
        lock = self.path / LOCK
        raw = lock.read_text(encoding="utf-8")
        files = json.loads(raw)["files"]
        for path in paths:
            digest = hashlib.sha256((self.path / path).read_bytes()).hexdigest()
            raw = raw.replace(f'"{path}": "{files[path]}"', f'"{path}": "{digest}"')
        lock.write_text(raw, encoding="utf-8")

    def weakening(self) -> tuple[int, str]:
        return self.run(PY, "-m", "far_validation", "weakening", "--base", self.base)

    def repin_gate(self, base: str, pr: int) -> tuple[int, str]:
        return self.run(PY, "far_validation/repin.py", "--base", base, "--head", "HEAD", "--repository", REPOSITORY,
                        "--repository-id", REPOSITORY_ID, "--target-pr", str(pr))

    def traced(self, check: str) -> tuple[int, str]:
        return self.run(PY, "-m", "far_validation", "validate", check, "--no-cache", "--trace-dependencies", "--require-trace")


Probe = Callable[[Workspace], tuple[int, str]]
PROBES: list[tuple[str, str, str, str, Probe]] = []


def probe(name: str, defect: str, detector: str, reason: str):
    def register(function: Probe) -> Probe:
        PROBES.append((name, defect, detector, reason, function))
        return function
    return register


# -- tests ------------------------------------------------------------------------------------------
TEST_FILE = "tests/test_claim_status_ceiling.py"


def _require_test_file(ws: Workspace) -> None:
    if not (ws.path / TEST_FILE).is_file():
        raise LookupError(f"{TEST_FILE} is absent at this ref")


def _first_line(ws: Workspace, path: str, needle: str) -> str:
    return next(line for line in (ws.path / path).read_text(encoding="utf-8").splitlines(True) if needle in line)


@probe("U1", "removed assertion", "weakening", r"assertion count decreased")
def removed_assertion(ws: Workspace):
    _require_test_file(ws)
    line = next(item for item in (ws.path / TEST_FILE).read_text(encoding="utf-8").splitlines(True)
                if item.strip().startswith("self.assert") and item.rstrip().endswith(")"))
    ws.edit(TEST_FILE, line, line[: len(line) - len(line.lstrip())] + "pass\n")
    ws.commit("remove an assertion")
    return ws.weakening()


@probe("U2", "skipped test", "weakening", r"skip count increased")
def skipped_test(ws: Workspace):
    _require_test_file(ws)
    line = _first_line(ws, TEST_FILE, "    def test_")
    ws.edit(TEST_FILE, line, '    @unittest.skip("probe")\n' + line)
    if "import unittest" not in (ws.path / TEST_FILE).read_text(encoding="utf-8"):
        ws.edit(TEST_FILE, "from __future__ import annotations\n", "from __future__ import annotations\nimport unittest\n")
    ws.commit("skip a test")
    return ws.weakening()


@probe("U3", "removed test function", "weakening", r"test functions removed")
def removed_test_function(ws: Workspace):
    _require_test_file(ws)
    ws.edit(TEST_FILE, "    def test_", "    def helper_", 1)
    ws.commit("rename a test so unittest no longer collects it")
    return ws.weakening()


@probe("U4", "deleted test file", "weakening", r"protected validation/test source deleted")
def deleted_test_file(ws: Workspace):
    _require_test_file(ws)
    (ws.path / TEST_FILE).unlink()
    ws.commit("delete a test file")
    return ws.weakening()


@probe("U5", "test-discovery manipulation (rename out of the test_*.py pattern)", "weakening",
       r"protected validation/test source deleted|test functions removed")
def discovery_rename(ws: Workspace):
    _require_test_file(ws)
    ws.git("mv", TEST_FILE, "tests/claim_status_ceiling_disabled.py")
    ws.commit("move a test file out of discovery")
    return ws.weakening()


@probe("U6", "changed expected value (code unchanged)", "canonical test module", r"FAIL|AssertionError")
def changed_expected_value(ws: Workspace):
    _require_test_file(ws)
    ws.edit(TEST_FILE, '"unresolved"', '"supported"')
    ws.commit("change an expected value")
    return ws.run(PY, "-m", "unittest", "tests.test_claim_status_ceiling")


# -- validators -------------------------------------------------------------------------------------
@probe("V1", "disabled validator (unconditional success before its rules)", "weakening",
       r"unreachable statement count increased")
def disabled_validator(ws: Workspace):
    ws.edit("tools/check_p8_theorem_role.py", "def main(", "raise SystemExit(0)\n\n\ndef main(")
    ws.commit("disable a checker")
    return ws.weakening()


def _manifest_command(ws: Workspace, check_id: str, command: list[str]) -> None:
    path = ws.path / "validation/manifest.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    for check in data["checks"]:
        if check["id"] == check_id:
            check["command"] = command
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


@probe("V2", "false-success check command in the manifest", "independent oracle",
       r"manifest|missing|coverage|command")
def false_success_command(ws: Workspace):
    _manifest_command(ws, "research.p8-role", ["python", "-c", "pass"])
    ws.commit("replace a check command with a no-op")
    return ws.run(PY, "-m", "far_validation", "oracle")


@probe("V3", "changed protected check definition", "bootstrap verifier", r"FAR-VAL-BOOT-001")
def changed_protected_check(ws: Workspace):
    _manifest_command(ws, "governance.claim-boundaries", ["python", "tools/check_p8_theorem_role.py"])
    ws.commit("point a protected check at another checker")
    return ws.run(PY, "validation_bootstrap/verify.py")


@probe("V4", "protected check unprotected in manifest and bootstrap lock together", "bootstrap verifier",
       r"FAR-VAL-BOOT-001")
def unprotected_in_lockstep(ws: Workspace):
    check_id = "governance.w5-authorization"
    for relative in ("validation/manifest.json", "validation_bootstrap/bootstrap-lock.json"):
        path = ws.path / relative
        data = json.loads(path.read_text(encoding="utf-8"))
        data["protected_checks"].remove(check_id)
        data.get("protected_check_definitions", {}).pop(check_id, None)
        for check in data.get("checks", []):
            if check["id"] == check_id:
                check["protected"] = False
        path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    ws.commit("drop a check from the protected set in manifest and lock together")
    return ws.run(PY, "validation_bootstrap/verify.py")


# -- protected artifacts and repins ---------------------------------------------------------------
PROTECTED = "far_validation/tracing.py"


@probe("P1", "protected file edited without moving its pin", "bootstrap verifier", r"FAR-VAL-BOOT-001")
def edited_protected_file(ws: Workspace):
    (ws.path / PROTECTED).write_text((ws.path / PROTECTED).read_text(encoding="utf-8") + "\n# probe\n", encoding="utf-8")
    ws.commit("edit a protected file")
    return ws.run(PY, "validation_bootstrap/verify.py")


@probe("P2", "unauthorized protected repin (file and pin moved together)", "protected-repin evaluator",
       r"requires exactly one valid signed authorization")
def unauthorized_repin(ws: Workspace):
    (ws.path / PROTECTED).write_text((ws.path / PROTECTED).read_text(encoding="utf-8") + "\n# probe\n", encoding="utf-8")
    ws.repin(PROTECTED)
    ws.commit("self-repin a protected file")
    return ws.repin_gate(ws.base, 1)


@probe("P3", "self-authorization by a key other than the pinned owner key", "protected-repin evaluator",
       r"appended authorization 0: .*(signature|signer|key)")
def foreign_key_authorization(ws: Workspace):
    sys.path.insert(0, str(ws.path))
    try:
        from far_validation import repin_signature as signature  # type: ignore
    finally:
        sys.path.pop(0)
    old = json.loads((ws.path / LOCK).read_text(encoding="utf-8"))["files"][PROTECTED]
    (ws.path / PROTECTED).write_text((ws.path / PROTECTED).read_text(encoding="utf-8") + "\n# probe\n", encoding="utf-8")
    ws.repin(PROTECTED)
    new = hashlib.sha256((ws.path / PROTECTED).read_bytes()).hexdigest()
    keydir = Path(tempfile.mkdtemp(dir=ws.path.parent))
    subprocess.run(["ssh-keygen", "-q", "-t", "ecdsa", "-b", "256", "-N", "", "-C", "", "-f", str(keydir / "k")], check=True)
    payload_path = keydir / "payload.json"
    subprocess.run([PY, "far_validation/repin_signature.py", "prepare", "--repository", REPOSITORY, "--repository-id",
                    REPOSITORY_ID, "--path", PROTECTED, "--old", old, "--new", new, "--target-pr", "1", "--base-sha", ws.base,
                    "--reason", "Probe: a signature by a key that is not the pinned owner key.", "--out", str(payload_path)],
                   cwd=ws.path, check=True, capture_output=True)
    subprocess.run(["ssh-keygen", "-q", "-Y", "sign", "-f", str(keydir / "k"), "-n", signature.NAMESPACE, str(payload_path)],
                   check=True, capture_output=True)
    ledger = json.loads((ws.path / LEDGER).read_text(encoding="utf-8"))
    ledger["consumptions"].append({"payload": payload_path.read_text(encoding="utf-8"),
                                   "signature": (keydir / "payload.json.sig").read_text(encoding="utf-8")})
    (ws.path / LEDGER).write_text(json.dumps(ledger, indent=2) + "\n", encoding="utf-8")
    ws.commit("authorize with a foreign key")
    return ws.repin_gate(ws.base, 1)


def _signed(ws: Workspace, signed_ref: str | None) -> str | None:
    if not signed_ref:
        return None
    try:
        ws.git("fetch", "-q", str(ROOT), f"{signed_ref}:refs/probe/signed")
    except subprocess.CalledProcessError:
        return None
    return ws.git("rev-parse", "refs/probe/signed").strip()


SIGNED_REF: str | None = None


def _signed_probe(function: Callable[[Workspace, str, str], tuple[int, str]]) -> Probe:
    def run(ws: Workspace) -> tuple[int, str]:
        head = _signed(ws, SIGNED_REF)
        if head is None:
            raise LookupError("signed ref unavailable")
        base = ws.git("merge-base", head, ws.base).strip()
        if base == head:
            # A probe base that already contains the signed ref has consumed its authorizations, so
            # there is nothing appended to tamper with or replay.
            raise LookupError("signed ref is already contained in the probe base")
        ws.reset(head)
        return function(ws, head, base)
    return run


@probe("S1", "tampered owner signature", "protected-repin evaluator", r"appended authorization \d+: .*signature")
@_signed_probe
def tampered_signature(ws: Workspace, head: str, base: str):
    ledger = json.loads((ws.path / LEDGER).read_text(encoding="utf-8"))
    entry = ledger["consumptions"][-1]
    lines = entry["signature"].splitlines()
    body = next(index for index, line in enumerate(lines) if line and not line.startswith("-----"))
    raw = bytearray(base64.b64decode("".join(lines[body:-1])))
    raw[-5] ^= 0x01
    encoded = base64.b64encode(bytes(raw)).decode()
    entry["signature"] = "\n".join([lines[0], *[encoded[i:i + 70] for i in range(0, len(encoded), 70)], lines[-1]]) + "\n"
    (ws.path / LEDGER).write_text(json.dumps(ledger, indent=2) + "\n", encoding="utf-8")
    ws.commit("flip one signature bit")
    return ws.repin_gate(base, 560)


@probe("S2", "signed authorization replayed on another pull request", "protected-repin evaluator",
       r"is bound to pull request 560, not 555")
@_signed_probe
def replayed_on_other_pr(ws: Workspace, head: str, base: str):
    return ws.repin_gate(base, 555)


@probe("S3", "authorized file changed after signing (exact-bytes binding)", "protected-repin evaluator",
       r"far_validation/weakening.py transition .* requires exactly one valid signed authorization")
@_signed_probe
def changed_after_signing(ws: Workspace, head: str, base: str):
    target = "far_validation/weakening.py"
    (ws.path / target).write_text((ws.path / target).read_text(encoding="utf-8") + "\n# probe\n", encoding="utf-8")
    ws.repin(target)
    ws.commit("change signed bytes")
    return ws.repin_gate(base, 560)


@probe("S4", "consumed authorization appended again after merge", "protected-repin evaluator",
       r"already consumed or is duplicated")
@_signed_probe
def consumed_replay(ws: Workspace, head: str, base: str):
    ledger = json.loads((ws.path / LEDGER).read_text(encoding="utf-8"))
    ledger["consumptions"].append(ledger["consumptions"][0])
    (ws.path / LEDGER).write_text(json.dumps(ledger, indent=2) + "\n", encoding="utf-8")
    ws.commit("replay a consumed authorization")
    return ws.repin_gate(head, 560)


@probe("S5", "evaluation against a stale comparison base", "protected-repin evaluator",
       r"trusted key differs|not in the comparison base's lineage|failing closed|FAR-VAL-REPIN-001")
@_signed_probe
def stale_base(ws: Workspace, head: str, base: str):
    stale = ws.git("rev-parse", f"{base}~40").strip()
    return ws.repin_gate(stale, 560)


# -- certificates, evidence, cache ----------------------------------------------------------------
def _certificate(ws: Workspace, evidence_ok: bool = True) -> tuple[int, str]:
    code, output = ws.run(PY, "-m", "far_validation", "validate", "bootstrap.manifest", "--no-cache")
    if code != 0:
        return code, output
    runtime = ws.path / "artifacts" / "validation" / "runtime"
    runtime.mkdir(parents=True, exist_ok=True)
    (runtime / "e.json").write_text(json.dumps({"successful": evidence_ok}), encoding="utf-8")
    return ws.run(PY, "tools/assemble_validation_certificate.py", "--evidence", "probe=artifacts/validation/runtime/e.json")


def _verify(ws: Workspace, commit: str, tree: str) -> tuple[int, str]:
    return ws.run(PY, "-m", "far_validation", "certificate", "verify", "--require-signed", "--expected-commit", commit,
                  "--expected-tree", tree, "--required-evidence", "probe")


@probe("C1", "certificate presented for a stale head", "certificate verifier", r"certificate commit does not match")
def stale_head_certificate(ws: Workspace):
    ws.commit("certified head")
    code, output = _certificate(ws)
    if code:
        return 0, "certificate setup failed: " + output
    return _verify(ws, ws.base, ws.git("rev-parse", "HEAD^{tree}").strip())


@probe("C2", "certificate presented for the wrong tree", "certificate verifier", r"certificate tree does not match")
def wrong_tree_certificate(ws: Workspace):
    code, output = _certificate(ws)
    if code:
        return 0, "certificate setup failed: " + output
    return _verify(ws, ws.git("rev-parse", "HEAD").strip(), ws.git("rev-parse", f"{ws.base}~1^{{tree}}").strip())


@probe("C3", "malformed or failed assurance evidence", "certificate assembler", r"assurance evidence failed: probe")
def failed_evidence(ws: Workspace):
    return _certificate(ws, evidence_ok=False)


@probe("C4", "tampered signed certificate", "certificate verifier", r"signature|tamper|attestation|digest")
def tampered_certificate(ws: Workspace):
    code, output = _certificate(ws)
    if code:
        return 0, "certificate setup failed: " + output
    path = ws.path / ".far" / "artifacts" / "validation" / "certificate.json"
    envelope = json.loads(path.read_text(encoding="utf-8"))
    envelope["payload"]["selected_checks"] = envelope["payload"].get("selected_checks", []) + ["forged.check"]
    path.write_text(json.dumps(envelope), encoding="utf-8")
    return _verify(ws, ws.git("rev-parse", "HEAD").strip(), ws.git("rev-parse", "HEAD^{tree}").strip())


def _cache_hits(ws: Workspace, env: dict[str, str] | None = None) -> tuple[int, list[str], str]:
    code, output = ws.run(PY, "-m", "far_validation", "validate", "bootstrap.manifest", "--require-signed-cache", "--format", "json", env=env)
    try:
        payload = json.loads(output[output.index("{"):])
    except ValueError:
        return code, [], output
    return code, list(payload.get("signed_cache_hits", [])), output


@probe("K1", "tampered signed cache entry", "signed cache", r"not reused")
def tampered_cache(ws: Workspace):
    _cache_hits(ws)
    entries = sorted((ws.path / ".far" / "cache").rglob("*.json"))
    if not entries:
        return 0, "no cache entry was written"
    for entry in entries:
        envelope = json.loads(entry.read_text(encoding="utf-8"))
        if isinstance(envelope.get("payload"), dict):
            envelope["payload"]["status"] = "passed"
            envelope["payload"]["probe"] = "tampered"
        entry.write_text(json.dumps(envelope), encoding="utf-8")
    code, hits, output = _cache_hits(ws)
    return (1, "tampered entry not reused") if "bootstrap.manifest" not in hits else (0, "tampered entry reused: " + output)


@probe("K2", "signed cache consumed under another trust domain", "signed cache", r"not reused")
def foreign_domain_cache(ws: Workspace):
    _cache_hits(ws)
    code, hits, output = _cache_hits(ws, {"FAR_VALIDATION_TRUST_DOMAIN": "another-domain"})
    return (1, "foreign-domain entry not reused") if "bootstrap.manifest" not in hits else (0, "reused: " + output)


# -- governance -------------------------------------------------------------------------------------
@probe("G1", "central claim promoted above its governed ceiling", "claim ceiling checker", r"CLM-EXISTENCE")
def promoted_claim(ws: Workspace):
    path = ws.path / "theory/evaluation/central-claim-registry.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    for claim in data["claims"]:
        if claim["id"] == "CLM-EXISTENCE":
            claim["current_status"] = "supported"
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    ws.commit("promote a claim")
    return ws.run(PY, "tools/check_claim_status_ceiling.py")


@probe("G2", "research gate marked satisfied without evidence", "research-gates checker",
       r"cannot be satisfied without evidence|must remain|must be")
def satisfied_gate(ws: Workspace):
    path = ws.path / "theory/evaluation/research-gates.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    gates = data["gates"] if isinstance(data.get("gates"), list) else list(data["gates"].values())
    gate = next(item for item in gates if item.get("status") == "not_satisfied")
    gate["status"] = "satisfied"
    for key in ("evidence", "satisfied_by", "evidence_artifacts"):
        if key in gate:
            gate[key] = []
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    ws.commit("mark a gate satisfied")
    return ws.run(PY, "tools/check_research_gates.py")


# -- strict runtime tracing -------------------------------------------------------------------------
def _needs_strace() -> None:
    if not shutil.which("strace"):
        raise LookupError("strace unavailable")


RUNTIME_DEPENDENCIES = "validation/runtime-dependencies.json"


@probe("T1", "missing runtime input declaration", "strict tracer", r"undeclared read: docs/planning/deduction-first-proof-roadmap.md")
def missing_declaration(ws: Workspace):
    _needs_strace()
    path = ws.path / RUNTIME_DEPENDENCIES
    data = json.loads(path.read_text(encoding="utf-8"))
    inputs = data["checks"]["governance.claim-boundaries"]["inputs"]
    inputs.remove("docs/planning/deduction-first-proof-roadmap.md")
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    ws.repin(RUNTIME_DEPENDENCIES)
    ws.commit("drop a runtime input")
    return ws.traced("governance.claim-boundaries")


def _set_p8_command(ws: Workspace, script: str) -> None:
    path = ws.path / "validation/manifest.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    for check in data["checks"]:
        if check["id"] == "research.p8-role":
            check["command"] = ["bash", "-c", script + "; exec python tools/check_p8_theorem_role.py"]
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    ws.commit("instrument a check command")


@probe("T2", "undeclared executable", "strict tracer", r"undeclared executable: \S*/id\b")
def undeclared_executable(ws: Workspace):
    _needs_strace()
    _set_p8_command(ws, "/usr/bin/id >/dev/null")
    return ws.traced("research.p8-role")


@probe("T3", "undeclared write into the repository", "strict tracer", r"undeclared write: docs/probe-write.txt")
def undeclared_write(ws: Workspace):
    _needs_strace()
    _set_p8_command(ws, "python -c \"open('docs/probe-write.txt','w').write('x')\"")
    return ws.traced("research.p8-role")


@probe("T4", "undeclared write through an atomic rename", "strict tracer", r"undeclared write: docs/probe-renamed.txt")
def undeclared_rename_write(ws: Workspace):
    _needs_strace()
    _set_p8_command(ws, "python -c \"import os,tempfile; f=tempfile.NamedTemporaryFile('w',dir='.far',delete=False); "
                        "f.write('x'); f.close(); os.replace(f.name,'docs/probe-renamed.txt')\"")
    return ws.traced("research.p8-role")


@probe("T5", "network access", "strict tracer", r"network access denied")
def network_access(ws: Workspace):
    _needs_strace()
    _set_p8_command(ws, "python -c \"import socket; s=socket.socket(); s.settimeout(0.2); s.connect_ex(('127.0.0.1', 9))\"")
    return ws.traced("research.p8-role")


def main(argv: list[str] | None = None) -> int:
    global SIGNED_REF
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--json", type=Path)
    parser.add_argument("--signed-ref", default="origin/fix/deferred-repin-integration")
    parser.add_argument("--source", type=Path, default=ROOT, help="repository to clone (default: this one)")
    parser.add_argument("--ref", help="commit or branch of --source to probe (default: its HEAD)")
    parser.add_argument("probes", nargs="*")
    args = parser.parse_args(argv)
    SIGNED_REF = args.signed_ref
    outcomes: list[Outcome] = []
    with tempfile.TemporaryDirectory() as directory:
        ws = Workspace(Path(directory), args.source)
        if args.ref:
            ws.git("checkout", "-q", "--detach", args.ref)
            ws.base = ws.git("rev-parse", "HEAD").strip()
        for name, defect, detector, reason, function in PROBES:
            if args.probes and name not in args.probes:
                continue
            ws.reset()
            try:
                code, output = function(ws)
            except LookupError as exc:
                outcomes.append(Outcome(name, defect, detector, reason, "NOT_RUN", None, str(exc)))
                continue
            except Exception as exc:  # a probe that cannot be applied is itself a finding
                outcomes.append(Outcome(name, defect, detector, reason, "ERROR", None, f"{type(exc).__name__}: {exc}"))
                continue
            match = re.search(reason, output)
            status = "CAUGHT" if code != 0 and match else "MISSED"
            evidence = match.group(0) if match and code != 0 else output.strip()[-600:]
            outcomes.append(Outcome(name, defect, detector, reason, status, code, evidence))
            print(f"{status:8} {name:3} {defect} [{detector}]: {evidence[:160]!r}", flush=True)
    report = {"schema": "far-assurance-adversarial-probe-v1", "base": ws.base, "signed_ref": SIGNED_REF,
              "outcomes": [dataclasses.asdict(item) for item in outcomes]}
    if args.json:
        args.json.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    for item in outcomes:
        if item.status in {"NOT_RUN", "ERROR"}:
            print(f"{item.status:8} {item.probe:3} {item.defect}: {item.evidence[:200]}")
    return 1 if any(item.status in {"MISSED", "ERROR"} for item in outcomes) else 0


if __name__ == "__main__":
    raise SystemExit(main())
