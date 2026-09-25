#!/usr/bin/env python3
"""Dedicated GitHub App that publishes the ``protected-repin-gate`` check.

It runs where nothing a pull request can change (workflow files, repository secrets, runner
environment of the protected repository) reaches the App's private key or this code: either an
owner-controlled host, or a scheduled GitHub Actions workflow in a separate, owner-only gate
repository (``actions`` subcommand; free for a public gate repository). Branch protection requires
``protected-repin-gate`` **from this App's ID**, so a check of the same name from any other source
(for example a candidate GitHub Actions job) cannot satisfy it.

Each cycle the App:

1. refuses to run inside CI unless it is the configured gate repository's scheduled or manual
   workflow on its ``main`` branch (never the protected repository), and refuses a private key
   file readable by other users;
2. verifies its own deployment: this file lives in a clean git checkout at the configured
   ``deployed_commit``;
3. mints a short-lived installation token restricted to checks:write, contents:read,
   pull_requests:read, metadata:read (JWT signed with ``openssl``; no third-party packages), and
   confirms the repository name still denotes the configured immutable repository id;
4. fetches ``main`` and each open pull request head into a private bare mirror (git objects only:
   no checkout, no submodules, no hooks; candidate bytes are never imported, executed or sourced);
5. evaluates each head against the current ``main`` tip with ``repin.evaluate``, using the key
   pinned on main (which must equal the deployment's copy) and only if the deployed evaluator files
   are byte-identical to those on main; otherwise the decision is a failure asking for a redeploy;
6. posts one completed check run on the head SHA (success only when the evaluation succeeds; any
   error fails closed or posts nothing, which leaves the required check pending). It keeps no
   state between cycles: a decision already posted is recognized from the App's own latest check
   run (its ``external_id`` records the decision key), so a cold start or a fresh runner re-posts
   nothing it already said and never suppresses a changed decision.

Configuration is a JSON file on the host (see ``Config``), or environment variables for the
``actions`` subcommand. The private key file must be readable only by the App's process.
"""
from __future__ import annotations

import argparse
import base64
import json
import os
import subprocess
import sys
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

try:
    from . import repin
except ImportError:  # Run as a standalone file from the deployment checkout.
    import importlib.util

    _spec = importlib.util.spec_from_file_location("_far_validation_repin", Path(__file__).resolve().with_name("repin.py"))
    assert _spec is not None and _spec.loader is not None
    repin = sys.modules.setdefault(_spec.name, importlib.util.module_from_spec(_spec))
    _spec.loader.exec_module(repin)

CHECK_NAME = "protected-repin-gate"
AUDIT_CHECK_NAME = "protected-repin-audit"
TOKEN_PERMISSIONS = {"checks": "write", "contents": "read", "pull_requests": "read", "metadata": "read"}
# The audit reads branch protection (needs Administration: read) and records it as a check run.
AUDIT_TOKEN_PERMISSIONS = {"administration": "read", "checks": "write", "metadata": "read"}
ACTIONS_EVENTS = frozenset({"schedule", "workflow_dispatch"})
DEPLOYMENT_FILES = ("far_validation/repin.py", "far_validation/repin_signature.py", "far_validation/repin_gate_app.py")
Http = Callable[[str, str, dict[str, str], Any], Any]


class GateError(RuntimeError):
    """The gate cannot establish a trustworthy evaluation; nothing may be reported as success."""


@dataclass(frozen=True)
class Config:
    app_id: int
    private_key: Path
    repository: str
    repository_id: int
    allowed_signers: Path
    state_dir: Path
    deployed_commit: str
    branch: str = "main"
    api_url: str = "https://api.github.com"
    git_url: str = ""
    gate_repository_id: int | None = None  # the only CI context allowed to run the App

    def __post_init__(self) -> None:
        if self.gate_repository_id is not None and self.gate_repository_id == self.repository_id:
            raise GateError("the gate must never run in the repository it protects")

    @classmethod
    def load(cls, path: Path) -> "Config":
        raw = json.loads(path.read_text(encoding="utf-8"))
        required = {"app_id", "private_key", "repository", "repository_id", "allowed_signers", "state_dir", "deployed_commit"}
        optional = {"branch", "api_url", "git_url", "gate_repository_id"}
        if not required <= set(raw) or not set(raw) <= required | optional:
            raise GateError(f"config must have fields {sorted(required)} (+ optional {', '.join(sorted(optional))})")
        return cls(
            app_id=int(raw["app_id"]), private_key=Path(raw["private_key"]), repository=raw["repository"],
            repository_id=int(raw["repository_id"]),
            allowed_signers=Path(raw["allowed_signers"]), state_dir=Path(raw["state_dir"]),
            deployed_commit=raw["deployed_commit"], branch=raw.get("branch", "main"),
            api_url=raw.get("api_url", "https://api.github.com").rstrip("/"),
            git_url=raw.get("git_url") or f"https://github.com/{raw['repository']}.git",
            gate_repository_id=int(raw["gate_repository_id"]) if raw.get("gate_repository_id") is not None else None,
        )


def verify_host(config: Config, environ: dict[str, str] | None = None) -> None:
    """Refuse to run where candidate-controlled automation could reach the App key."""
    environ = os.environ if environ is None else environ
    if environ.get("GITHUB_ACTIONS") or environ.get("CI"):
        # Only the owner's separate gate repository, on its default branch, from a trigger no pull
        # request can cause. These variables describe the runner to itself: they catch a misplaced
        # deployment (for example the key pasted into the protected repository's secrets); the
        # security boundary is that the key exists only in the gate repository's environment.
        if config.gate_repository_id is None:
            raise GateError("the gate App must not run inside GitHub Actions or CI unless gate_repository_id names "
                            "the owner's separate gate repository")
        if environ.get("GITHUB_REPOSITORY_ID") == str(config.repository_id):
            raise GateError("the gate App must never run in the protected repository's own workflows")
        if (environ.get("GITHUB_ACTIONS") != "true" or environ.get("GITHUB_REPOSITORY_ID") != str(config.gate_repository_id)
                or environ.get("GITHUB_REF") != "refs/heads/main" or environ.get("GITHUB_EVENT_NAME") not in ACTIONS_EVENTS):
            raise GateError("in CI the gate App runs only in the configured gate repository, on refs/heads/main, "
                            f"from {sorted(ACTIONS_EVENTS)}")
    mode = config.private_key.stat().st_mode
    if mode & 0o077:
        raise GateError(f"App private key {config.private_key} is accessible to other users (mode {oct(mode & 0o777)}); chmod 600")


def verify_deployment(config: Config, checkout: Path | None = None) -> None:
    """Refuse to run unless the evaluator files are exactly ``deployed_commit``'s committed bytes."""
    checkout = checkout or deployment_checkout()

    def git(*args: str) -> str:
        completed = subprocess.run(["git", "-C", str(checkout), *args], capture_output=True, text=True, check=False)
        if completed.returncode != 0:
            raise GateError(f"deployment is not a git checkout: {completed.stderr.strip()}")
        return completed.stdout.strip()

    if git("rev-parse", "HEAD") != config.deployed_commit:
        raise GateError(f"deployment checkout is not at deployed_commit {config.deployed_commit}")
    if git("status", "--porcelain", "--untracked-files=no", "--", *DEPLOYMENT_FILES):
        raise GateError("deployment evaluator files differ from deployed_commit")


def deployment_checkout() -> Path:
    return Path(__file__).resolve().parents[1]


def _b64url(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def app_jwt(app_id: int, private_key: Path, now: float | None = None) -> str:
    """RS256 JWT for the App, signed by ``openssl`` with the host-held private key."""
    now = int(now if now is not None else time.time())
    header = _b64url(json.dumps({"alg": "RS256", "typ": "JWT"}, separators=(",", ":")).encode())
    claims = _b64url(json.dumps({"iat": now - 60, "exp": now + 540, "iss": app_id}, separators=(",", ":")).encode())
    signing_input = f"{header}.{claims}".encode("ascii")
    completed = subprocess.run(["openssl", "dgst", "-sha256", "-sign", str(private_key)], input=signing_input,
                               capture_output=True, check=False)
    if completed.returncode != 0:
        raise GateError(f"cannot sign App JWT: {completed.stderr.decode(errors='replace').strip()}")
    return f"{header}.{claims}.{_b64url(completed.stdout)}"


def urllib_http(method: str, url: str, headers: dict[str, str], body: Any) -> Any:
    data = json.dumps(body).encode() if body is not None else None
    request = urllib.request.Request(url, data=data, method=method, headers={
        "Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28", **headers})
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            payload = response.read()
    except urllib.error.HTTPError as exc:
        raise GateError(f"{method} {url} -> HTTP {exc.code}") from exc
    return json.loads(payload) if payload else None


class Gate:
    def __init__(self, config: Config, http: Http = urllib_http, now: Callable[[], datetime] | None = None,
                 checkout: Path | None = None, environ: dict[str, str] | None = None) -> None:
        self.config = config
        self.environ = environ
        self.checkout = checkout or deployment_checkout()
        self.http = http
        self.now = now or (lambda: datetime.now(timezone.utc))
        self.mirror = config.state_dir / "mirror.git"

    # -- GitHub -----------------------------------------------------------------------------
    def installation_token(self, permissions: dict[str, str] = TOKEN_PERMISSIONS) -> str:
        auth = {"Authorization": f"Bearer {app_jwt(self.config.app_id, self.config.private_key)}"}
        installation = self.http("GET", f"{self.config.api_url}/repos/{self.config.repository}/installation", auth, None)
        name = self.config.repository.split("/", 1)[1]
        token = self.http("POST", f"{self.config.api_url}/app/installations/{installation['id']}/access_tokens", auth,
                          {"repositories": [name], "permissions": permissions})
        return token["token"]

    def verify_repository(self, token: str) -> None:
        """The configured repository name must still denote the configured immutable repository id."""
        repo = self.http("GET", f"{self.config.api_url}/repos/{self.config.repository}", {"Authorization": f"Bearer {token}"}, None)
        if repo.get("id") != self.config.repository_id or repo.get("full_name") != self.config.repository:
            raise GateError(f"{self.config.repository} is repository id {repo.get('id')}, not the configured {self.config.repository_id}")

    def open_pulls(self, token: str) -> list[dict[str, Any]]:
        pulls, page = [], 1
        while True:
            batch = self.http("GET", f"{self.config.api_url}/repos/{self.config.repository}/pulls?state=open"
                                     f"&base={self.config.branch}&per_page=100&page={page}",
                              {"Authorization": f"Bearer {token}"}, None)
            pulls.extend(batch)
            if len(batch) < 100:
                return pulls
            page += 1

    def latest_decision(self, token: str, head_sha: str, name: str = CHECK_NAME) -> str | None:
        """``external_id`` of this App's newest completed ``name`` check run on ``head_sha``, if any."""
        runs = self.http("GET", f"{self.config.api_url}/repos/{self.config.repository}/commits/{head_sha}/check-runs"
                                f"?check_name={name}&app_id={self.config.app_id}&filter=latest&per_page=100",
                         {"Authorization": f"Bearer {token}"}, None)
        own = [r for r in runs.get("check_runs", [])
               if r.get("name") == name and (r.get("app") or {}).get("id") == self.config.app_id
               and r.get("status") == "completed"]
        return max(own, key=lambda r: r["id"]).get("external_id") if own else None

    def post_check(self, token: str, head_sha: str, success: bool, title: str, summary: str, key: str,
                   name: str = CHECK_NAME, conclusion: str | None = None) -> None:
        self.http("POST", f"{self.config.api_url}/repos/{self.config.repository}/check-runs",
                  {"Authorization": f"Bearer {token}"},
                  {"name": name, "head_sha": head_sha, "status": "completed", "external_id": key,
                   "conclusion": conclusion or ("success" if success else "failure"),
                   "output": {"title": title, "summary": summary[:65000]}})

    # -- git ---------------------------------------------------------------------------------
    def fetch(self, token: str, numbers: list[int]) -> None:
        if not (self.mirror / "HEAD").exists():
            subprocess.run(["git", "init", "-q", "--bare", str(self.mirror)], check=True)
        refspecs = [f"+refs/heads/{self.config.branch}:refs/gate/base"]
        refspecs += [f"+refs/pull/{n}/head:refs/gate/pull/{n}" for n in numbers]
        env = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "GIT_TERMINAL_PROMPT": "0", "HOME": str(self.config.state_dir)}
        if self.config.git_url.startswith("https://"):
            basic = base64.b64encode(f"x-access-token:{token}".encode()).decode()
            env.update({"GIT_CONFIG_COUNT": "1", "GIT_CONFIG_KEY_0": "http.extraHeader",
                        "GIT_CONFIG_VALUE_0": f"Authorization: Basic {basic}"})
        completed = subprocess.run(["git", "-C", str(self.mirror), "-c", "core.hooksPath=/dev/null", "fetch", "-q",
                                    "--no-tags", "--prune", "--no-recurse-submodules", self.config.git_url, *refspecs],
                                   env=env, capture_output=True, check=False)
        if completed.returncode != 0:
            raise GateError(f"fetch failed: {completed.stderr.decode(errors='replace').strip()}")

    # -- evaluation --------------------------------------------------------------------------
    def evaluate(self, number: int, head_sha: str) -> repin.RepinReport:
        git = repin.GitObjects(self.mirror)
        if git.commit(f"refs/gate/pull/{number}") != head_sha:
            raise GateError(f"pull request #{number} head moved during evaluation")
        report = repin.evaluate(git, "refs/gate/base", head_sha, allowed_signers=self.config.allowed_signers.read_bytes(),
                                repository=self.config.repository, repository_id=self.config.repository_id,
                                target_pr=number, now=self.now())
        base = git.commit("refs/gate/base")
        for name in DEPLOYMENT_FILES:  # decide only with the evaluator that main currently pins
            if git.blob(base, name, label="base evaluator") != (self.checkout / name).read_bytes():
                report.fail(name, f"the deployed evaluator differs from {name} on {self.config.branch}; "
                                  "redeploy the App at the current main commit before it can decide")
        return report

    def run_once(self) -> list[dict[str, Any]]:
        verify_host(self.config, self.environ)
        verify_deployment(self.config, self.checkout)
        token = self.installation_token()
        self.verify_repository(token)
        pulls = [p for p in self.open_pulls(token) if p["base"]["ref"] == self.config.branch]
        self.fetch(token, [p["number"] for p in pulls])
        mirror = repin.GitObjects(self.mirror)
        base_tip = mirror.commit("refs/gate/base")
        missing = [name for name in DEPLOYMENT_FILES if name not in mirror.tree(base_tip)]
        if missing:  # before the bootstrap merge there is nothing to enforce; silence leaves the check pending
            raise GateError(f"{self.config.branch} {base_tip[:12]} carries no protected-repin evaluator ({missing[0]}); "
                            "nothing is decided before the bootstrap merge")
        # A check run belongs to a commit, not to a pull request: when one head is open as several pull
        # requests, it is decided once, and passes only if it passes as every one of them.
        by_head: dict[str, list[int]] = {}
        for pull in pulls:
            by_head.setdefault(pull["head"]["sha"], []).append(pull["number"])
        results = []
        for head_sha, numbers in by_head.items():
            numbers = sorted(numbers)
            reports: dict[int, repin.RepinReport | None] = {}
            failures: dict[str, list[str]] = {}
            try:
                for number in numbers:
                    try:
                        reports[number] = report = self.evaluate(number, head_sha)
                        for path, messages in report.failures.items():
                            failures.setdefault(path, []).extend(
                                messages if len(numbers) == 1 else [f"as #{number}: {m}" for m in messages])
                    except (repin.LedgerError, OSError, ValueError) as exc:
                        reports[number] = None
                        failures.setdefault("<gate>", []).append(f"evaluation error as #{number}: {exc}")
            except GateError as exc:  # head moved: say nothing now, the next cycle evaluates the new head
                results.append({"numbers": numbers, "head": head_sha, "skipped": str(exc)})
                continue
            success = not failures
            label = ",".join(str(n) for n in numbers)
            key = f"{label}:{head_sha}:{base_tip}:{self.config.deployed_commit}:{success}"
            if self.latest_decision(token, head_sha) != key:
                used = sorted({i for r in reports.values() if r for i in r.used})
                lines = [f"Evaluated head {head_sha} of {', '.join(f'#{n}' for n in numbers)} against {self.config.branch} {base_tip}.",
                         f"Evaluator: deployment {self.config.deployed_commit}.",
                         f"Authorizations used: {', '.join(used) if used else 'none'}."]
                report = next((r for r in reports.values() if r), None)
                if report and report.transitions:
                    lines += ["", "Protected transitions in this head. An authorization must name exactly these values "
                                  f"(repository_id {self.config.repository_id}, target_pr {label}):"]
                    for t in report.transitions:
                        lines += [f"- path: {t['path']}", f"  old_sha256: {t['old_sha256']}", f"  new_sha256: {t['new_sha256']}"]
                    lines.append("")
                for path, messages in sorted(failures.items()):
                    lines += [f"- {path}: {message}" for message in messages]
                self.post_check(token, head_sha, success, "protected transitions authorized" if success
                                else "unauthorized or invalid protected transition", "\n".join(lines), key)
            results.append({"numbers": numbers, "head": head_sha, "success": success})
        return results

    def audit(self) -> dict[str, Any]:
        """Record main's live protection and rulesets as an App-authored ``protected-repin-audit`` check.

        The owner (on a phone) and anyone else can read the result on the commit; it replaces
        command-line exports. ``neutral`` means problems were found, ``success`` that there were none.
        """
        verify_host(self.config, self.environ)
        verify_deployment(self.config, self.checkout)
        token = self.installation_token(AUDIT_TOKEN_PERMISSIONS)
        self.verify_repository(token)
        auth, api = {"Authorization": f"Bearer {token}"}, f"{self.config.api_url}/repos/{self.config.repository}"
        protection = self.http("GET", f"{api}/branches/{self.config.branch}/protection", auth, None)
        rulesets = self.http("GET", f"{api}/rulesets?includes_parents=true", auth, None)
        rules = self.http("GET", f"{api}/rules/branches/{self.config.branch}", auth, None)
        tip = self.http("GET", f"{api}/commits/{self.config.branch}", auth, None)["sha"]
        problems = check_protection(protection, self.config.app_id)
        record = {"branch": self.config.branch, "tip": tip, "app_id": self.config.app_id, "problems": problems,
                  "protection": protection, "rulesets": rulesets, "rules": rules}
        body = json.dumps(record, indent=1, sort_keys=True)
        summary = ("PASS: " if not problems else "FAIL: ") + ("; ".join(problems) or "protection matches the gate") \
            + "\n\n```json\n" + body[:60000] + "\n```"
        self.post_check(token, tip, not problems, "protection audit " + ("PASS" if not problems else "FAIL"), summary,
                        f"audit:{tip}:{int(self.now().timestamp())}", name=AUDIT_CHECK_NAME,
                        conclusion="success" if not problems else "neutral")
        return record


def check_protection(protection: dict[str, Any], app_id: int) -> list[str]:
    """Problems with a ``GET /repos/{repo}/branches/main/protection`` response for this gate."""
    problems = []
    checks = (protection.get("required_status_checks") or {})
    ours = [c for c in checks.get("checks", []) if c.get("context") == CHECK_NAME]
    if ours != [{"context": CHECK_NAME, "app_id": app_id}]:
        problems.append(f"required checks must contain exactly {{context: {CHECK_NAME}, app_id: {app_id}}}; found {ours}")
    if checks.get("strict") is not True:
        problems.append("required status checks must be strict (branches up to date before merging)")
    if not (protection.get("enforce_admins") or {}).get("enabled"):
        problems.append("enforce_admins must be enabled")
    if (protection.get("allow_force_pushes") or {}).get("enabled"):
        problems.append("force pushes must be disabled")
    if (protection.get("allow_deletions") or {}).get("enabled"):
        problems.append("branch deletion must be disabled")
    return problems


ACTIONS_ENV = ("FAR_APP_ID", "FAR_APP_PRIVATE_KEY", "FAR_REPOSITORY", "FAR_REPOSITORY_ID", "FAR_DEPLOYED_COMMIT",
               "FAR_GATE_REPOSITORY_ID", "RUNNER_TEMP")


def run_actions(mode: str, environ: dict[str, str] | None = None, http: Http = urllib_http,
                checkout: Path | None = None, api_url: str = "https://api.github.com", git_url: str | None = None) -> int:
    """One cycle in the gate repository's workflow: key from the environment secret, code from here.

    The evaluator and the pinned key are taken from this deployment checkout (the workflow checks
    out ``FAR_DEPLOYED_COMMIT``); main must still match them, as on any host. The key is written to a
    mode-600 file in the runner's temporary directory and removed before returning. Prints only
    decisions, never secrets.
    """
    environ = dict(os.environ if environ is None else environ)
    checkout = checkout or deployment_checkout()
    missing = [name for name in ACTIONS_ENV if not environ.get(name)]
    if missing:
        print(f"protected-repin-gate: missing environment {missing}; nothing posted", file=sys.stderr)
        return 1
    temp = Path(environ["RUNNER_TEMP"]) / "far-repin-gate"
    temp.mkdir(mode=0o700, parents=True, exist_ok=True)
    key = temp / "app.pem"
    try:
        descriptor = os.open(key, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600)
        with os.fdopen(descriptor, "w", encoding="ascii") as handle:
            handle.write(environ["FAR_APP_PRIVATE_KEY"].strip() + "\n")
        config = Config(app_id=int(environ["FAR_APP_ID"]), private_key=key, repository=environ["FAR_REPOSITORY"],
                        repository_id=int(environ["FAR_REPOSITORY_ID"]),
                        allowed_signers=checkout / repin.ALLOWED_SIGNERS_PATH, state_dir=temp / "state",
                        deployed_commit=environ["FAR_DEPLOYED_COMMIT"], api_url=api_url,
                        git_url=git_url or f"https://github.com/{environ['FAR_REPOSITORY']}.git",
                        gate_repository_id=int(environ["FAR_GATE_REPOSITORY_ID"]))
        gate = Gate(config, http=http, checkout=checkout, environ=environ)
        if mode == "audit":
            record = gate.audit()
            print(json.dumps({"audit": "PASS" if not record["problems"] else "FAIL", "problems": record["problems"]}))
            return 0 if not record["problems"] else 1
        for result in gate.run_once():
            print(json.dumps(result, sort_keys=True), flush=True)
        return 0
    except (GateError, OSError, subprocess.SubprocessError, KeyError, ValueError) as exc:
        print(f"protected-repin-gate cycle failed (nothing posted): {exc}", file=sys.stderr, flush=True)
        return 1
    finally:
        key.unlink(missing_ok=True)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="protected-repin-gate GitHub App")
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("once", "serve"):
        command = sub.add_parser(name)
        command.add_argument("--config", type=Path, required=True)
        if name == "serve":
            command.add_argument("--interval", type=int, default=120)
    actions = sub.add_parser("actions", help="one cycle inside the owner's gate-repository workflow (config from env)")
    actions.add_argument("--mode", choices=("evaluate", "audit"), default="evaluate")
    protection = sub.add_parser("check-protection", help="validate a saved branch-protection API response")
    protection.add_argument("response", type=Path)
    protection.add_argument("--app-id", type=int, required=True)
    args = parser.parse_args(argv)
    if args.command == "check-protection":
        problems = check_protection(json.loads(args.response.read_text(encoding="utf-8")), args.app_id)
        for problem in problems:
            print(f"[FAIL] {problem}")
        print("Result:", "FAIL" if problems else "PASS")
        return 1 if problems else 0
    if args.command == "actions":
        return run_actions(args.mode)
    gate = Gate(Config.load(args.config))
    while True:
        try:
            for result in gate.run_once():
                print(json.dumps(result, sort_keys=True), flush=True)
        except (GateError, OSError, subprocess.SubprocessError, KeyError) as exc:
            print(f"protected-repin-gate cycle failed (nothing posted): {exc}", file=sys.stderr, flush=True)
            if args.command == "once":
                return 1
        if args.command == "once":
            return 0
        time.sleep(max(30, args.interval))


if __name__ == "__main__":
    raise SystemExit(main())
