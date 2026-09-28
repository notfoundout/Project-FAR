"""Adversarial tests for protected-artifact repins authorized by offline owner signatures.

Each test builds a real git repository whose ``main`` pins protected artifacts and the owner's
public key, then plays a candidate pull request. Authorizations are signed with real
``ssh-keygen`` keys: the owner's key (pinned on main) and an attacker's key. The evaluator reads
git objects only and must accept exactly one thing: an owner-signed, unconsumed, lineage-valid
authorization for this exact transition in this pull request, recorded once in the ledger.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

from far_validation import repin
from far_validation import repin_signature as sig

REPOSITORY = "notfoundout/Project-FAR"
REPOSITORY_ID = 1283452680
POLICY = "validation/runtime-policy.json"
FORMAL = "formal/ValidationEngine.tla"
LOCK = repin.ASSURANCE_LOCK_PATH
LEDGER = repin.CONSUMPTIONS_PATH
SIGNERS = repin.ALLOWED_SIGNERS_PATH
NOW = datetime(2026, 9, 24, 12, 0, 0, tzinfo=timezone.utc)
ORIGINAL = b'{"network_policy": "deny"}\n'
REPLACEMENT = b'{"network_policy": "deny", "timeout_seconds": 60}\n'
UNSIGNED_MESSAGE = "a candidate may not authorize its own protected-artifact repin"


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def keypair(directory: Path, name: str) -> tuple[Path, bytes]:
    key = directory / name
    subprocess.run(["ssh-keygen", "-q", "-t", "ecdsa", "-b", "256", "-N", "", "-C", "", "-f", str(key)], check=True)
    kind, blob = (directory / f"{name}.pub").read_text().split()[:2]
    return key, f'{sig.PRINCIPAL} namespaces="{sig.NAMESPACE}" {kind} {blob}\n'.encode()


class RepinLedgerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.dir = Path(self.enterContext(tempfile.TemporaryDirectory()))
        self.keys = self.dir / "keys"
        self.keys.mkdir()
        self.owner, self.owner_signers = keypair(self.keys, "owner")
        self.attacker, self.attacker_signers = keypair(self.keys, "attacker")
        self.repo = self.dir / "repo"
        self.repo.mkdir()
        self.git("init", "-q", "-b", "main")
        self.git("config", "user.email", "t@example.invalid")
        self.git("config", "user.name", "t")
        self.write(POLICY, ORIGINAL)
        self.write(FORMAL, b"---- MODULE ValidationEngine ----\n====\n")
        self.write(SIGNERS, self.owner_signers)
        self.write(LOCK, self.lock_bytes({POLICY: sha256(ORIGINAL), FORMAL: sha256(self.read(FORMAL)),
                                          SIGNERS: sha256(self.owner_signers)}))
        self.write(LEDGER, self.ledger_bytes([]))
        self.base = self.commit("main")
        self.git("checkout", "-q", "-b", "candidate")

    # -- repository helpers -----------------------------------------------------------------
    def git(self, *args: str) -> str:
        return subprocess.run(["git", "-C", str(self.repo), *args], check=True, capture_output=True, text=True).stdout.strip()

    def write(self, rel: str, data: bytes) -> None:
        target = self.repo / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)

    def read(self, rel: str) -> bytes:
        return (self.repo / rel).read_bytes()

    @staticmethod
    def lock_bytes(files: dict[str, str], **contract: object) -> bytes:
        return (json.dumps({"schema_version": "1.0", "files": files, **contract}, indent=2, sort_keys=True) + "\n").encode()

    @staticmethod
    def ledger_bytes(entries: list) -> bytes:
        return (json.dumps({"schema_version": repin.LEDGER_SCHEMA, "consumptions": entries}, indent=2) + "\n").encode()

    def commit(self, message: str = "candidate") -> str:
        self.git("add", "-A")
        self.git("commit", "-qm", message, "--allow-empty")
        return self.git("rev-parse", "HEAD")

    def lock(self) -> dict:
        return json.loads(self.read(LOCK))

    def repin(self, rel: str, data: bytes) -> tuple[str, str]:
        """Change a protected file and move its pin, as any candidate can."""
        lock = self.lock()
        old = lock["files"][rel]
        self.write(rel, data)
        lock["files"][rel] = sha256(data)
        self.write(LOCK, self.lock_bytes(lock["files"], **{k: v for k, v in lock.items() if k != "files"}))
        return old, sha256(data)

    def authorization(self, path: str, old: str, new: str, *, key: Path | None = None, **overrides: object) -> dict:
        nonce = hashlib.sha256(repr((path, old, new, self.base, sorted(overrides.items()))).encode()).hexdigest()[:32]
        payload = {
            "schema": sig.SCHEMA, "domain": sig.DOMAIN, "id": nonce, "repository": REPOSITORY, "repository_id": REPOSITORY_ID,
            "path": path, "old_sha256": old,
            "new_sha256": new, "target_pr": 538, "base_sha": self.base,
            "reason": "owner-reviewed replacement of this exact protected artifact",
            "issued_at": (NOW - timedelta(hours=1)).strftime(sig.TIME_FORMAT),
            "expires_at": (NOW + timedelta(days=13)).strftime(sig.TIME_FORMAT),
        }
        payload.update(overrides)
        message = sig.canonical_bytes(payload)
        target = self.dir / "payload"
        target.write_bytes(message)
        subprocess.run(["ssh-keygen", "-q", "-Y", "sign", "-f", str(key or self.owner), "-n", sig.NAMESPACE, str(target)],
                       check=True, capture_output=True)
        signature = (self.dir / "payload.sig").read_text()
        (self.dir / "payload.sig").unlink()
        return {"payload": message.decode(), "signature": signature}

    def append(self, *entries: dict) -> None:
        ledger = json.loads(self.read(LEDGER))
        ledger["consumptions"].extend(entries)
        self.write(LEDGER, self.ledger_bytes(ledger["consumptions"]))

    def evaluate(self, *, target_pr: int | None = 538, trusted: bytes | None = None,
                 now: datetime = NOW) -> repin.RepinReport:
        return repin.evaluate(repin.GitObjects(self.repo), self.base, "HEAD",
                              allowed_signers=self.owner_signers if trusted is None else trusted,
                              repository=REPOSITORY, repository_id=REPOSITORY_ID, target_pr=target_pr, now=now)

    def assert_rejected(self, report: repin.RepinReport, path: str, fragment: str = "") -> None:
        self.assertFalse(report.successful, report.to_dict())
        self.assertIn(path, report.failures, report.failures)
        if fragment:
            self.assertTrue(any(fragment in m for m in report.failures[path]), report.failures)

    def signed_policy_transition(self, **overrides: object) -> dict:
        old, new = self.repin(POLICY, REPLACEMENT)
        return self.authorization(POLICY, old, new, **overrides)

    def merge_to_main(self) -> None:
        self.git("checkout", "-q", "main")
        self.git("merge", "-q", "--no-ff", "candidate", "-m", "merge")
        self.base = self.git("rev-parse", "HEAD")
        self.git("checkout", "-q", "-B", "candidate")

    # -- accepted ---------------------------------------------------------------------------
    def test_untouched_candidate_passes(self) -> None:
        self.write("docs/notes.md", b"unprotected change\n")
        self.commit()
        self.assertTrue(self.evaluate().successful)

    def test_real_signed_authorization_with_exact_transition_passes(self) -> None:
        entry = self.signed_policy_transition()
        self.append(entry)
        self.commit()
        report = self.evaluate()
        self.assertTrue(report.successful, report.failures)
        self.assertEqual(report.used, [sig.parse_payload(entry["payload"])["id"]])

    def test_lock_contract_transition_with_signed_authorization_passes(self) -> None:
        lock = self.lock()
        old = sig.contract_digest(lock)
        lock["workflow"] = {"required_fragments": ["python3 far_validation/repin.py"]}
        self.write(LOCK, self.lock_bytes(lock["files"], **{k: v for k, v in lock.items() if k != "files"}))
        self.commit()
        self.assert_rejected(self.evaluate(), repin.LOCK_CONTRACT_PATH, UNSIGNED_MESSAGE)
        self.append(self.authorization(repin.LOCK_CONTRACT_PATH, old, sig.contract_digest(lock)))
        self.commit()
        report = self.evaluate()
        self.assertTrue(report.successful, report.failures)

    def test_adding_a_new_protected_path_needs_no_authorization_but_must_match_its_pin(self) -> None:
        lock = self.lock()
        self.write("far_validation/new.py", b"x = 1\n")
        lock["files"]["far_validation/new.py"] = sha256(b"x = 1\n")
        self.write(LOCK, self.lock_bytes(lock["files"]))
        self.commit()
        self.assertTrue(self.evaluate().successful)
        lock["files"]["far_validation/new.py"] = "0" * 64
        self.write(LOCK, self.lock_bytes(lock["files"]))
        self.commit()
        self.assert_rejected(self.evaluate(), "far_validation/new.py", "hashes to")

    # -- self-authorization -----------------------------------------------------------------
    def test_self_repin_without_authorization_fails(self) -> None:
        self.repin(POLICY, REPLACEMENT)
        self.commit()
        self.assert_rejected(self.evaluate(), POLICY, UNSIGNED_MESSAGE)

    def test_self_written_unsigned_authorization_fails(self) -> None:
        entry = self.signed_policy_transition()
        self.append({"payload": entry["payload"], "signature": "approved by notfoundout"})
        self.commit()
        report = self.evaluate()
        self.assert_rejected(report, LEDGER, "armored SSH signature")
        self.assert_rejected(report, POLICY, UNSIGNED_MESSAGE)

    def test_owner_username_only_authorization_fails(self) -> None:
        """The retired B′ record: GitHub says the owner's account issued it, but nothing is signed."""
        old, new = self.repin(POLICY, REPLACEMENT)
        self.append({"schema_version": "1.0", "id": "GH-5005-1", "repository": REPOSITORY,
                     "workflow": ".github/workflows/issue-repin-authorization.yml", "path": POLICY,
                     "base_sha256": old, "authorized_sha256": new, "target_pr": 538,
                     "reason": "owner-issued authorization for this exact transition", "issuer": "notfoundout",
                     "issued_main_sha": self.base, "issued_at": "2026-09-24T00:00:00Z", "run_id": 5005, "run_attempt": 1})
        self.commit()
        self.assert_rejected(self.evaluate(), POLICY, UNSIGNED_MESSAGE)

    def test_signature_under_an_untrusted_key_fails(self) -> None:
        self.append(self.signed_policy_transition(key=self.attacker))
        self.commit()
        self.assert_rejected(self.evaluate(), LEDGER, "not by the pinned key")

    def test_candidate_replacing_the_pinned_key_cannot_authorize_itself(self) -> None:
        entry = self.signed_policy_transition(key=self.attacker)
        old_key, new_key = self.repin(SIGNERS, self.attacker_signers)
        self.append(entry, self.authorization(SIGNERS, old_key, new_key, key=self.attacker))
        self.commit()
        report = self.evaluate()
        self.assert_rejected(report, POLICY, UNSIGNED_MESSAGE)
        self.assert_rejected(report, SIGNERS, UNSIGNED_MESSAGE)
        # An evaluator handed the candidate's key is refused too: it must equal main's pinned key.
        self.assert_rejected(self.evaluate(trusted=self.attacker_signers), LOCK, "trusted key differs")

    def test_key_rotation_is_a_protected_transition_signed_by_the_current_key(self) -> None:
        old_key, new_key = self.repin(SIGNERS, self.attacker_signers)  # "attacker" plays the successor key
        self.commit()
        self.assert_rejected(self.evaluate(), SIGNERS, UNSIGNED_MESSAGE)
        self.append(self.authorization(SIGNERS, old_key, new_key, key=self.attacker))
        self.commit()
        self.assert_rejected(self.evaluate(), LEDGER, "not by the pinned key")  # the new key cannot authorize itself
        self.write(LEDGER, self.ledger_bytes([self.authorization(SIGNERS, old_key, new_key)]))
        self.commit()
        report = self.evaluate()
        self.assertTrue(report.successful, report.failures)  # the current key authorizes its successor

    def test_rotated_key_has_no_effect_within_the_rotating_pull_request(self) -> None:
        old_key, new_key = self.repin(SIGNERS, self.attacker_signers)
        rotation = self.authorization(SIGNERS, old_key, new_key)
        policy = self.signed_policy_transition(key=self.attacker)  # signed by the incoming key only
        self.append(rotation, policy)
        self.commit()
        report = self.evaluate()
        self.assert_rejected(report, POLICY, UNSIGNED_MESSAGE)
        self.assertNotIn(SIGNERS, report.failures)

    def test_after_rotation_the_gate_must_be_redeployed_with_the_new_key(self) -> None:
        old_key, new_key = self.repin(SIGNERS, self.attacker_signers)
        self.append(self.authorization(SIGNERS, old_key, new_key))
        self.commit()
        self.merge_to_main()
        self.write("docs/notes.md", b"any later change\n")
        self.commit()
        self.assert_rejected(self.evaluate(), LOCK, "trusted key differs")  # old deployment key: fail closed
        self.assertTrue(self.evaluate(trusted=self.attacker_signers).successful)

    def test_forged_signature_fails(self) -> None:
        genuine = self.signed_policy_transition()
        other = self.authorization(POLICY, "e" * 64, "f" * 64)
        self.append({"payload": genuine["payload"], "signature": other["signature"]})
        self.commit()
        self.assert_rejected(self.evaluate(), LEDGER, "does not verify")

    def test_one_changed_payload_byte_fails(self) -> None:
        entry = self.signed_policy_transition()
        self.append({**entry, "payload": entry["payload"].replace("exact", "exacT")})
        self.commit()
        self.assert_rejected(self.evaluate(), LEDGER, "does not verify")

    # -- binding ----------------------------------------------------------------------------
    def test_valid_owner_signature_for_another_pull_request_fails(self) -> None:
        self.append(self.signed_policy_transition(target_pr=539))
        self.commit()
        self.assert_rejected(self.evaluate(), LEDGER, "bound to pull request 539")

    def test_valid_owner_signature_for_another_new_digest_fails(self) -> None:
        old, _ = self.repin(POLICY, REPLACEMENT)
        self.append(self.authorization(POLICY, old, sha256(b'{"network_policy": "allow"}\n')))
        self.commit()
        report = self.evaluate()
        self.assert_rejected(report, POLICY, UNSIGNED_MESSAGE)
        self.assert_rejected(report, LEDGER, "matches no protected transition")

    def test_valid_owner_signature_for_another_path_fails(self) -> None:
        old, new = self.repin(POLICY, REPLACEMENT)
        self.append(self.authorization(FORMAL, old, new))
        self.commit()
        self.assert_rejected(self.evaluate(), POLICY, UNSIGNED_MESSAGE)

    def test_valid_owner_signature_for_another_repository_fails(self) -> None:
        self.append(self.signed_policy_transition(repository="someone/fork"))
        self.commit()
        self.assert_rejected(self.evaluate(), LEDGER, "not notfoundout/Project-FAR")

    def test_valid_owner_signature_for_another_repository_id_fails(self) -> None:
        """A same-named repository recreated after a rename/delete has a different immutable id."""
        self.append(self.signed_policy_transition(repository_id=REPOSITORY_ID + 1))
        self.commit()
        self.assert_rejected(self.evaluate(), LEDGER, "not 1283452680")

    def test_candidate_content_differing_from_its_pin_fails(self) -> None:
        self.append(self.signed_policy_transition())
        self.write(POLICY, b'{"network_policy": "allow"}\n')  # the pin still says REPLACEMENT
        self.commit()
        self.assert_rejected(self.evaluate(), POLICY, "hashes to")

    def test_symlink_whose_target_matches_the_pin_fails(self) -> None:
        """git stores a symlink's target as its blob; hashing blobs alone would accept it."""
        self.append(self.signed_policy_transition())
        (self.repo / POLICY).unlink()
        (self.repo / POLICY).symlink_to(REPLACEMENT.decode())
        self.commit()
        self.assert_rejected(self.evaluate(), POLICY, "not a regular file")

    def test_unchanged_pin_with_symlinked_file_fails(self) -> None:
        (self.repo / FORMAL).unlink()
        (self.repo / FORMAL).symlink_to("/etc/passwd")
        self.commit()
        self.assert_rejected(self.evaluate(), FORMAL)

    # -- lineage and time -------------------------------------------------------------------
    def test_valid_owner_signature_with_foreign_base_fails(self) -> None:
        self.git("checkout", "-q", "--orphan", "elsewhere")
        foreign = self.commit("unrelated history")
        self.git("checkout", "-q", "-f", "candidate")
        self.append(self.signed_policy_transition(base_sha=foreign))
        self.commit()
        self.assert_rejected(self.evaluate(), LEDGER, "not in the comparison base's lineage")

    def test_valid_owner_signature_for_a_stale_base_pin_fails(self) -> None:
        """Signed against a main commit where the path had other bytes; main has moved on."""
        self.git("checkout", "-q", "main")
        self.repin(POLICY, b'{"network_policy": "deny", "v": 0}\n')
        stale_base = self.commit("older pin")
        self.repin(POLICY, ORIGINAL)
        self.base = self.commit("current pin")
        self.git("checkout", "-q", "-B", "candidate")
        _, new = self.repin(POLICY, REPLACEMENT)
        self.append(self.authorization(POLICY, sha256(ORIGINAL), new, base_sha=stale_base))
        self.commit()
        self.assert_rejected(self.evaluate(), LEDGER, "was not pinned to old_sha256")

    def test_expired_and_future_authorizations_fail(self) -> None:
        self.append(self.signed_policy_transition())
        self.commit()
        self.assert_rejected(self.evaluate(now=NOW + timedelta(days=14)), LEDGER, "validity window")
        self.assert_rejected(self.evaluate(now=NOW - timedelta(hours=2)), LEDGER, "validity window")

    # -- single use -------------------------------------------------------------------------
    def test_replay_after_use_fails(self) -> None:
        entry = self.signed_policy_transition()
        self.append(entry)
        self.commit()
        self.assertTrue(self.evaluate().successful)
        self.merge_to_main()
        self.append(entry)  # a later PR tries to spend the same authorization again
        self.commit()
        self.assert_rejected(self.evaluate(), LEDGER, "already consumed")

    def test_replay_after_revert_fails(self) -> None:
        entry = self.signed_policy_transition()
        self.append(entry)
        self.commit()
        self.merge_to_main()
        old, new = self.repin(POLICY, ORIGINAL)  # an authorized revert
        self.append(self.authorization(POLICY, old, new))
        self.commit()
        report = self.evaluate()
        self.assertTrue(report.successful, report.failures)
        self.merge_to_main()
        self.repin(POLICY, REPLACEMENT)  # the original transition again, reusing its signature
        self.append(entry)
        self.commit()
        report = self.evaluate()
        self.assert_rejected(report, LEDGER, "already consumed")
        self.assert_rejected(report, POLICY, UNSIGNED_MESSAGE)

    @staticmethod
    def malleated(entry: dict) -> dict:
        """The (r, n - s) twin of an entry's ECDSA signature: a different, equally valid signature."""
        blob = sig.dearmor(entry["signature"])
        offset = 10
        fields = []
        for _ in range(5):
            value, offset = sig._read_string(blob, offset)
            fields.append(value)
        public, namespace, reserved, hash_algorithm, inner = fields
        kind, at = sig._read_string(inner, 0)
        components, _ = sig._read_string(inner, at)
        r, at = sig._read_mpint(components, 0)
        s_value, _ = sig._read_mpint(components, at)

        def string(data: bytes) -> bytes:
            return len(data).to_bytes(4, "big") + data

        def mpint(value: int) -> bytes:
            raw = value.to_bytes(33, "big").lstrip(b"\0")
            return string(b"\0" + raw if raw[0] & 0x80 else raw)

        twin_inner = string(kind) + string(mpint(r) + mpint(sig.P256_N - s_value))
        twin = (b"SSHSIG" + (1).to_bytes(4, "big") + string(public) + string(namespace) + string(reserved)
                + string(hash_algorithm) + string(twin_inner))
        return {"payload": entry["payload"], "signature": sig.armor(twin)}

    def test_malleated_signature_twin_is_valid_but_cannot_be_replayed(self) -> None:
        entry = self.signed_policy_transition()
        twin = self.malleated(entry)
        self.assertNotEqual(twin["signature"], entry["signature"])
        self.assertEqual(sig.verify_entry(twin, self.owner_signers), sig.verify_entry(entry, self.owner_signers))
        self.append(entry, twin)  # both forms in one change
        self.commit()
        self.assert_rejected(self.evaluate(), LEDGER, "duplicated")

    def test_malleated_twin_replay_after_merge_and_after_revert_fails(self) -> None:
        entry = self.signed_policy_transition()
        self.append(entry)
        self.commit()
        self.merge_to_main()
        self.append(self.malleated(entry))  # the same authorization under different signature bytes
        self.commit()
        self.assert_rejected(self.evaluate(), LEDGER, "already consumed")
        self.git("reset", "-q", "--hard", self.base)
        old, new = self.repin(POLICY, ORIGINAL)  # an authorized revert
        self.append(self.authorization(POLICY, old, new))
        self.commit()
        self.merge_to_main()
        self.repin(POLICY, REPLACEMENT)
        self.append(self.malleated(entry))
        self.commit()
        report = self.evaluate()
        self.assert_rejected(report, LEDGER, "already consumed")
        self.assert_rejected(report, POLICY, UNSIGNED_MESSAGE)

    def test_lost_key_signatures_fail_after_a_recovery_repin(self) -> None:
        """Lost phone: the Secure Enclave key cannot be recovered. After the owner's recovery bootstrap
        pins a new key on main, anything the old key signed (or anyone holding it signs) is rejected."""
        lost_entry = self.signed_policy_transition()
        self.git("stash", "-q", "--include-untracked")
        self.git("checkout", "-q", "main")
        replacement, replacement_signers = keypair(self.keys, "replacement")
        self.write(SIGNERS, replacement_signers)  # the recovery bootstrap commit (owner, outside the gate)
        lock = self.lock()
        lock["files"][SIGNERS] = sha256(replacement_signers)
        self.write(LOCK, self.lock_bytes(lock["files"]))
        self.base = self.commit("recovery: pin replacement key")
        self.git("checkout", "-q", "-B", "candidate")
        old, new = self.repin(POLICY, REPLACEMENT)
        self.append(lost_entry)
        self.commit()
        report = self.evaluate(trusted=replacement_signers)
        self.assert_rejected(report, LEDGER, "not by the pinned key")
        self.assert_rejected(report, POLICY, UNSIGNED_MESSAGE)
        self.git("reset", "-q", "--hard", self.base)
        self.repin(POLICY, REPLACEMENT)
        self.append(self.authorization(POLICY, old, new, key=replacement))
        self.commit()
        report = self.evaluate(trusted=replacement_signers)
        self.assertTrue(report.successful, report.failures)
        self.assertFalse(self.evaluate(trusted=self.owner_signers).successful)  # an undeployed gate fails closed

    def test_duplicated_authorization_fails(self) -> None:
        entry = self.signed_policy_transition()
        self.append(entry, entry)
        self.commit()
        self.assert_rejected(self.evaluate(), LEDGER, "duplicated")

    def test_two_matching_authorizations_are_ambiguous(self) -> None:
        old, new = self.repin(POLICY, REPLACEMENT)
        self.append(self.authorization(POLICY, old, new),
                    self.authorization(POLICY, old, new, reason="a second signed copy of the same exact transition"))
        self.commit()
        self.assert_rejected(self.evaluate(), POLICY, "found 2")

    def test_burning_an_authorization_without_its_transition_fails(self) -> None:
        self.append(self.authorization(POLICY, sha256(ORIGINAL), sha256(REPLACEMENT)))
        self.commit()
        self.assert_rejected(self.evaluate(), LEDGER, "matches no protected transition")

    def test_ledger_history_rewrite_fails(self) -> None:
        self.append(self.signed_policy_transition())
        self.commit()
        self.merge_to_main()
        self.write(LEDGER, self.ledger_bytes([]))
        self.commit()
        self.assert_rejected(self.evaluate(), LEDGER, "append-only")

    def test_two_pr_escalation_fails(self) -> None:
        """PR A lands ledger bytes; PR B tries to use them. Neither yields authority."""
        self.append(self.authorization(POLICY, sha256(ORIGINAL), sha256(REPLACEMENT), key=self.attacker))
        self.commit()
        self.assert_rejected(self.evaluate(), LEDGER)  # A itself is rejected
        self.merge_to_main()  # suppose A landed anyway: base entries grant nothing to B
        self.repin(POLICY, REPLACEMENT)
        self.commit()
        self.assert_rejected(self.evaluate(), POLICY, UNSIGNED_MESSAGE)

    # -- structure --------------------------------------------------------------------------
    def test_dropping_a_protected_path_fails(self) -> None:
        lock = self.lock()
        del lock["files"][FORMAL]
        self.write(LOCK, self.lock_bytes(lock["files"]))
        self.commit()
        self.assert_rejected(self.evaluate(), FORMAL, "dropped")

    def test_protecting_the_ledger_is_rejected(self) -> None:
        self.git("checkout", "-q", "main")
        lock = self.lock()
        lock["files"][LEDGER] = sha256(self.read(LEDGER))
        self.write(LOCK, self.lock_bytes(lock["files"]))
        self.base = self.commit("protect ledger")
        self.git("checkout", "-q", "-B", "candidate")
        self.assert_rejected(self.evaluate(), LEDGER, "deadlock")

    def test_uncommitted_working_tree_is_not_evaluated(self) -> None:
        self.append(self.signed_policy_transition())
        self.commit()
        self.write(POLICY, b"tampered after commit\n")
        self.assertTrue(self.evaluate().successful)  # only committed objects count; the App evaluates PR heads


if __name__ == "__main__":
    unittest.main()
